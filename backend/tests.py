from django.test import TestCase
from django.test.client import Client

c = Client()


class TestIndex(TestCase):

    @classmethod
    def setUpTestData(cls):
        print("setUpTestData: Run once to set up non-modified data for all class methods.")
        pass

    def setUp(self):
        print("setUp: Run once for every test method to setup clean data.")
        pass

    def testGetIndex(self):
        response = c.get('/api/')
        self.assertEqual(response.status_code, 200)

    def testPostIndex(self):
        # TODO: change body of request
        response = c.post('/api/', {'username': 'admin', 'password': 'qwerty'})
        self.assertEqual(response.status_code, 200)


class TestResults(TestCase):

    @classmethod
    def setUpTestData(cls):
        print("setUpTestData: Run once to set up non-modified data for all class methods.")
        pass

    def setUp(self):
        print("setUp: Run once for every test method to setup clean data.")
        pass

    def testGetResults(self):
        response = c.get('/api/results')
        self.assertEqual(response.status_code, 200)
