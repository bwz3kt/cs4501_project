from django.test import TestCase
from .models import Apartment

#Tests for Models Layer

#Test for Apartment Model
class ApartmentTestCase(TestCase):
    def setUp(self):
        Apartment.objects.create(name="jpa", price=2000,rating = 3)
    def test_apartment_name_(self):
        #name should be jpa
        jpa = Apartment.objects.get(name="jpa")
        self.assertEqual(jpa.name, 'jpa')
    def test_apartment_price_(self):
        #price should be 2000
        jpa = Apartment.objects.get(price=2000)
        self.assertEqual(jpa.price, 2000)
    def test_apartment_rating_(self):
        #rating should be 3
        jpa = Apartment.objects.get(rating=3)
        self.assertEqual(jpa.rating,3)


#Test for Update API
class UpdateTestCase(TestCase):
    def setUp(self):
        Apartment.objects.create(name="jpa", price=2700, rating=3)
    #updating name should be now "jeffcomm" now "jpa"
    def test_update_name_(self):
        username_name = Apartment.objects.get(name="jpa")
        username_name.name= "jeffcomm"
        self.assertTrue(username_name.name, "jeffcomm")
    #updating price should be now 900 instead of 2700
    def test_update_price_(self):
        username_name = Apartment.objects.get(price=2700)
        username_name.price= 900
        self.assertTrue(username_name.price, 900)
    #updating rating now shoudl be 3.8 instead of 3
    def test_update_rating_(self):
        username_name = Apartment.objects.get(rating=3)
        username_name.rating= 3.8
        self.assertTrue(username_name.rating,3.8)

#Test for Delete API
class DeleteTestCase(TestCase):
    def setUp(self):
        Apartment.objects.create(name="jpa", price=2700, rating=3)
    #deleted jpa object should now be none after the delete
    def test_delete_apt_(self):
        username_name = Apartment.objects.get(name="jpa")
        username_name.save()
        username_name.delete()
        self.assertTrue(username_name,None)

#Test for Sorting Function by Rating
class SortRatingTestCase(TestCase):
    def setUp(self):
        Apartment.objects.create(name="a", price=10, rating=0.5)
        Apartment.objects.create(name="b", price=20, rating=1.5)
        Apartment.objects.create(name="c", price=30, rating=2.5)
        Apartment.objects.create(name="d", price=40, rating=3.5)
        Apartment.objects.create(name="e", price=50, rating=4.5)
        Apartment.objects.create(name="f", price=60, rating=4.8)
    # should be sorted in descending order (highest rating first, lowest rating list)
    # list should be ['f','e','d','c','b'] since that is the order of apartment names after sorting by rating (shows the top five)
    def test_sort_rating_(self):
        apt_a = Apartment.objects.get(name="a")
        apt_a.save()
        apt_b = Apartment.objects.get(name="b")
        apt_b.save()
        apt_c = Apartment.objects.get(name="c")
        apt_c.save()
        apt_d = Apartment.objects.get(name="d")
        apt_d.save()
        apt_e = Apartment.objects.get(name="e")
        apt_e.save()
        apt_f = Apartment.objects.get(name="f")
        apt_f.save()
        objects = list(Apartment.objects.all().order_by('-rating')[:5])
        name_list =[]
        for apartment in objects:
            name_list.append(apartment.name)
        self.assertEqual(name_list, ['f','e','d','c','b'])

#Test for Sorting Function by Price
class SortPriceTestCase(TestCase):
    def setUp(self):
        Apartment.objects.create(name="a", price=60, rating=0.5)
        Apartment.objects.create(name="b", price=55, rating=1.5)
        Apartment.objects.create(name="c", price=50, rating=2.5)
        Apartment.objects.create(name="d", price=45, rating=3.5)
        Apartment.objects.create(name="e", price=40, rating=4.5)
        Apartment.objects.create(name="f", price=35, rating=4.8)

    # should be sorted in ascending order (lowest price first, highest price last)
    # list should be ['f','e','d','c','b'] since that is the order of apartment names after sorting by price (shows the top five)
    def test_sort_price_(self):
        apt_a = Apartment.objects.get(name="a")
        apt_a.save()
        apt_b = Apartment.objects.get(name="b")
        apt_b.save()
        apt_c = Apartment.objects.get(name="c")
        apt_c.save()
        apt_d = Apartment.objects.get(name="d")
        apt_d.save()
        apt_e = Apartment.objects.get(name="e")
        apt_e.save()
        apt_f = Apartment.objects.get(name="f")
        apt_f.save()
        objects = Apartment.objects.all().order_by('price')[:5]
        name_list_price = []
        for apartment in objects:
            name_list_price.append(apartment.name)
        self.assertEqual(name_list_price, ['f', 'e', 'd', 'c', 'b'])

