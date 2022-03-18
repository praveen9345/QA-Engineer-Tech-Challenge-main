import unittest

from client import  SeriesDispatcher

"""
What can be the unit test?
-can create an object=>Done

"""


class TestCourse(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.seriesDispatcher= SeriesDispatcher()
       
    def test_canCreateObj(self):
        #sad path test
        with self.assertRaises(TypeError):
            SeriesDispatcher("Dummy")    
        
    