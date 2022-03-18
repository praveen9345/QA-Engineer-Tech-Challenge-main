import unittest
import asyncio
import mock
from pynetdicom  import events
from scp import  ModalityStoreSCP

"""
What can be the unit test?
-can create an object=>Done

"""


class TestCourse(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.mockAsyncioObj=mock.Mock()
        cls.mockAsyncioObj.dataset_queue=asyncio.Queue(loop=asyncio.get_event_loop())
        cls.mockAsyncioObj.asyncio_get_event_loop=asyncio.get_event_loop()
        cls.modalityStoreSCP= ModalityStoreSCP(cls.mockAsyncioObj.dataset_queue,cls.mockAsyncioObj.asyncio_get_event_loop)
       
    def test_canCreateObj(self):
        #sad path test
        with self.assertRaises(TypeError):
            ModalityStoreSCP()    
        
    def test_configure_aeExist(self):
        self.assertIsNotNone(self.modalityStoreSCP._configure_ae())
    
    def test_configure_aeNone(self):
        self.assertIsNone(self.modalityStoreSCP._configure_ae())

    def test_handle_store(self):
        #Happy path testing
       statusCode = self.modalityStoreSCP.handle_store()
       # error message in case if test case got failed
       message = "test handle store failed , status code: "+ statusCode
       self.assertEqual(statusCode, 0,message)