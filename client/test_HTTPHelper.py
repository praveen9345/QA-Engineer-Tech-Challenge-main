import unittest
from unittest.mock import MagicMock

from client import HTTPHelper

"""
What can be the unit test?
-local hostexist-->hard-coded=>Done
-can create an object=>Done
-post payload test=> Done
"""

#initialization of MagicMock object
def mock_dict(d):
    m = MagicMock()
    m.__getitem__.side_effect = d.__getitem__
    return m


class TestCourse(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.httpHelper= HTTPHelper("http://localhost:8000/")
       
    def test_canCreateObj(self):
        #sad path test
        with self.assertRaises(TypeError):
            HTTPHelper("Dummy","http://localhost:8081/")    
        
    def test_localHostExist(self):
        self.assertIsNotNone(self.httpHelper.server_address)

    def test_post_pyloadReturnInt(self):

       """
       # in success of request --> return status code(int) - 200
       # in not success of request --> return status code(int) - 401
       """
       d={
            'series_instance_uid': "1.2.840.113619.2.410.2807.1589496.16368.1623732908.744",
            'patient_id': "ANO0001",
            'patient_name': "ANO0001",
            'study_instance_uid': "1.2.276.0.37.1.354.201605.50651742",
            'instances_in_series': 4
        }
       #Happy path testing
       self.mockPostPayload= mock_dict(d)
       statusCode = self.httpHelper.post_payload(self.mockPostPayload)
       # error message in case if test case got failed
       message = "test post pyload failed , status code: "+ statusCode
       self.assertEqual(statusCode, 201,message)

    def test_post_pyloadReturnNone(self):

       #Sad path testing
       self.mockPostPayload= mock_dict({})
       none = self.httpHelper.post_payload(self.mockPostPayload)
       self.assertIsNone(none)

