from django.test import TestCase
from django.test.client import Client

c = Client()


class TestCSV(TestCase):

    @classmethod
    def setUpTestData(cls):
        print("setUpTestData: Run once to set up non-modified data for all class methods.")
        pass

    def setUp(self):
        print("setUp: Run once for every test method to setup clean data.")
        pass

    def testGetCSV(self):
        response = c.get('/api/make-csv')
        self.assertEqual(response.status_code, 200)


class TestQuery(TestCase):

    @classmethod
    def setUpTestData(cls):
        print("setUpTestData: Run once to set up non-modified data for all class methods.")
        pass

    def setUp(self):
        print("setUp: Run once for every test method to setup clean data.")
        pass

    def testGetResults(self):
        response = c.get('/api/process-query')
        self.assertEqual(response.status_code, 200)
