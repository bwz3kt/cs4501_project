from pyspark import SparkContext
import MySQLdb
import itertools

print("Coview script started.")

# Read data in as pairs of (user_id, item_id clicked on by the user) (Step 1)
# Group data into (user_id, list of item ids they clicked on) (Step 2)
# Transform into (user_id, (item1, item2) where item1 and item2 are pairs of items the user clicked on (Step 3)
# Transform into ((item1, item2), list of user1, user2 etc) where users are all the ones who co-clicked (item1, item2) (Step 4)
# Transform into ((item1, item2), count of distinct users who co-clicked (item1, item2) (Step 5)
# Filter out any results where less than 3 users co-clicked the same pair of items (Step 6)


sc = SparkContext("spark://spark-master:7077", "PopularItems")

data = sc.textFile("/tmp/data/access.log", 2)     # each worker loads a piece of the data file

pairs = data.map(lambda line: line.split("\t"))   # tell each worker to split each line of it's partition
pages = pairs.map(lambda pair: (pair[0], pair[1]))      # re-layout the data to ignore the user id (Step 1)
distinct_pages = pages.distinct() #produces RDD with distinct rows
user_clicked = distinct_pages.groupByKey()        # (Step 2)

#  Used by flatMap to find all possible pairings
def find_pairs(list):
    pairs_list=[]
    user_id = list[0]
    for x in list[1]:
        for y in list[1]:
            if (y>x) and (x!=y):
                pairs_list.append(((user_id), (x, y)))
    return pairs_list

#Step 3
all_pairs = user_clicked.flatMap(lambda pair: find_pairs(pair))

#Step 4
group_by_val = all_pairs.groupBy(lambda pair: pair[1])

#Step 5
count_list = group_by_val.map(lambda pair: ((pair[0]), len(pair[1])))

#Step 6
filtered = count_list.filter(lambda pair: pair[1] >= 3)
output = filtered.collect()                          # bring the data back to the master node so we can print it out
print(output)

file = open("/tmp/data/recommendation_log.txt", "a+")
db = MySQLdb.connect(host="db", port=3306, user="www", passwd="$3cureUS", db="cs4501")
cursor = db.cursor()

cursor.execute("Truncate table api_recommendations")

db.commit()

for page_id, count in output:
    x_str = page_id[0]
    y_str = page_id[1]
    x = int(page_id[0])
    y = int(page_id[1])

    cursor.execute("""
        INSERT INTO api_recommendations
            (item_id,recommended_items)
        VALUES 
            (%s, %s) 
        ON DUPLICATE KEY UPDATE 
            -- no need to update the PK 
            recommended_items= CONCAT(recommended_items, ",", %s) ;
                   """, (x, y_str, y_str)  # python variables
                   )
    cursor.execute("""
        INSERT INTO api_recommendations
            (item_id,recommended_items)
        VALUES 
            (%s, %s) 
        ON DUPLICATE KEY UPDATE 
            -- no need to update the PK 
            recommended_items= CONCAT(recommended_items, ",", %s) ;
                   """, (y, x_str, x_str)  # python variables
                   )
    db.commit()
    file.write(str(page_id) + '\t' + str(count) + '\n')
    print("page_id %s count %d" % (str(page_id), count))

print("Popular items done")
db.close()

sc.stop()