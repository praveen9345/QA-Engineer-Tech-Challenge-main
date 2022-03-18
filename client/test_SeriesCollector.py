import unittest
import mock 

from client import SeriesCollector

"""
What can be the unit test?
-can create an object=>Done
-add instent test =>

"""


class TestCourse(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.mockDatasetObj=mock.Mock()
        cls.mockDatasetObj.SeriesInstanceUID= "1.2.840.113619.2.410.2807.1589496.16368.1623732908.744"
        cls.mockDatasetObj.PatientID="ANO0001"
        cls.mockDatasetObj.PatientName="ANO0001"
        cls.mockDatasetObj.StudyInstanceUID="1.2.276.0.37.1.354.201605.50651742"
        cls.seriesCollector= SeriesCollector(cls.mockDatasetObj)
       
    def test_canCreateObj(self):
        #sad path test
        with self.assertRaises(TypeError):
            SeriesCollector()    
        
    def test_add_instance(self):
        """
        SeriesInstanceUID is same than return-->true=>Done
        SeriesInstanceUID is same than return-->false=>Done
        """
        boolAddInstance=self.seriesCollector.add_instance(self.mockDatasetObj)
        # error message in case if test case got failed
        message = "SeriesInstanceUID is not same."
        # assertTrue() to check true of test value
        self.assertTrue( boolAddInstance, message)

    def test_extract_data(self):
        """
        return dic is not empty--{.......}=>Done
        return dic is empty-->{}=>Done
        """
        boolExtractData=bool(self.seriesCollector.extract_data())
        # error message in case if test case got failed
        message = "dataset is empty."
        # assertTrue() to check true of test value
        self.assertTrue( boolExtractData, message)    