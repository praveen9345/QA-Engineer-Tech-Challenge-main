import asyncio
import time
from pydicom import Dataset
from scp import ModalityStoreSCP
import requests

## due to time constrain we have only added two unit tests
## both test are checking if errors are thrown if none dataset is input to the client
## praveen

class HTTPHelper:
    """A helper class to send HTTP post requests to the server
    """
    def __init__(self, server_address: str ="http://localhost:8000/") -> None:
        self.server_address = server_address

    async def post_payload(self, payload) -> None:
        """Sends post request to 'add_series/' path of the server to add a single
        instance of series.

        Args:
            payload: A dict with data intended to be sent to the server

        Returns:
            int: Status code of the server response
        """
        request = requests.post(self.server_address + "add_series/", json=payload)
        print(request.json())
        return request.status_code


class SeriesCollector:
    """A Series Collector is used to build up a list of instances (a DICOM series) as they are received by the modality.
    It stores the (during collection incomplete) series, the Series (Instance) UID, the time the series was last updated
    with a new instance and the information whether the dispatch of the series was started.
    """
    def __init__(self, first_dataset: Dataset) -> None:
        """Initialization of the Series Collector with the first dataset (instance).

        Args:
            first_dataset (Dataset): The first dataset or the regarding series received from the modality.
        """
        self.series_instance_uid = first_dataset.SeriesInstanceUID
        self.series: list[Dataset] = [first_dataset]
        self.patient_id = first_dataset.PatientID
        self.patient_name = first_dataset.PatientName
        self.study_instance_uid = first_dataset.StudyInstanceUID
        self.last_update_time = time.time()
        self.dispatch_started = False

    def add_instance(self, dataset: Dataset) -> bool:
        """Add an dataset to the series collected by this Series Collector if it has the correct Series UID.

        Args:
            dataset (Dataset): The dataset to add.

        Returns:
            bool: `True`, if the Series UID of the dataset to add matched and the dataset was therefore added, `False` otherwise.
        """
        if self.series_instance_uid == dataset.SeriesInstanceUID:
            self.series.append(dataset)
            self.last_update_time = time.time()
            return True

        return False

    def extract_data(self):
        """ Extract required data and set dispatch_started to TRUE to avoid conflicts
        Returns:
            A dict with the following:
                series_instance_uid: str,
                patient_id: str,
                patient_name: str,
                study_instance_uid: str,
                InstancesInSeries: int
        """
        self.dispatch_started = True
        return {
            'series_instance_uid': self.series_instance_uid,
            'patient_id': self.patient_id,
            'patient_name': str(self.patient_name),
            'study_instance_uid': self.study_instance_uid,
            'instances_in_series': len(self.series)
        }


class SeriesDispatcher:
    """This code provides a template for receiving data from a modality using DICOM.
    Be sure to understand how it works, then try to collect incoming series (hint: there is no attribute indicating how
    many instances are in a series, so you have to wait for some time to find out if a new instance is transmitted).
    For simplyfication, you can assume that only one series is transmitted at a time.
    You can use the given template, but you don't have to!
    """

    def __init__(self) -> None:
        """Initialize the Series Dispatcher.
        """

        self.loop: asyncio.AbstractEventLoop
        self.lock = asyncio.Lock()
        self.series_collector = {}
        self.dataset_queue = asyncio.Queue(loop=asyncio.get_event_loop())
        self.modality_scp = ModalityStoreSCP(self.dataset_queue, asyncio.get_event_loop())
        self.http_helper = HTTPHelper()

    async def main(self) -> None:
        """An infinitely running method used as hook for the asyncio event loop.
        Keeps the event loop alive whether or not datasets are received from the modality and prints a message
        regulary when no datasets are received.
        """
        while True:
            # TODO: Regulary check if new datasets are received and act if they are.
            # Information about Python asyncio: https://docs.python.org/3/library/asyncio.html
            # When datasets are received you should collect and process them
            # (e.g. using `asyncio.create_task(self.run_series_collector()`)
            print("Waiting for Modality")

            # Wait for the SCP server to add dataset to the queue rather than polling
            dataset = await self.dataset_queue.get()
            asyncio.create_task(self.run_series_collectors(dataset))

            #print("my unit test 1")
            # should receive error "exception=AttributeError("'NoneType' object has no attribute 'SeriesInstanceUID'")"" since the passed dataset is none
            #dataset = None
            #asyncio.create_task(self.run_series_collectors(dataset))


    async def run_series_collectors(self, dataset) -> None:
        """Runs the collection of datasets, which results in the Series Collector being filled.
        """
        # Check if the given dataset already exists, and handle accordingly
        uid = dataset.SeriesInstanceUID

        # Lock while accessing series_collector to avoid race conditions
        async with self.lock:
            if uid not in self.series_collector:
                self.series_collector[uid] = SeriesCollector(dataset)
            elif not self.series_collector[uid].dispatch_started:
                self.series_collector[uid].add_instance(dataset)

        # Create a task to dispatch current dataset
        asyncio.create_task(self.dispatch_series_collector(uid))


        
        #print("my unit test 2")
        # should receive error "exception=AttributeError("'NoneType' object has no attribute 'SeriesInstanceUID'")"" since the passed dataset is none
        #asyncio.create_task(self.dispatch_series_collector(None))
         

    async def dispatch_series_collector(self, UID) -> None:
        """Tries to dispatch a Series Collector, i.e. to finish it's dataset collection and scheduling of further
        methods to extract the desired information.
        """
        # Check if the series collector hasn't had an update for a long enough timespan and send the series to the
        # server if it is complete
        # NOTE: This is the last given function, you should create more for extracting the information and
        # sending the data to the server

        # Wait for the max time before trying to dispatch
        maximum_wait_time = 1
        await asyncio.sleep(maximum_wait_time + 0.1)

        # Lock while accessing series_collector to avoid race condition
        async with self.lock:
            elapsed_time = time.time() - self.series_collector[UID].last_update_time
            if elapsed_time >= maximum_wait_time:
                print("Ready to dispatch " + str(UID))
                payload = self.series_collector[UID].extract_data()
                asyncio.create_task(self.http_helper.post_payload(payload))
            else:
                print("Recently Updated: " + str(elapsed_time))

        


if __name__ == "__main__":
    """Create a Series Dispatcher object and run it's infinite `main()` method in a event loop.
    """
    engine = SeriesDispatcher()
    engine.loop = asyncio.get_event_loop()
    engine.loop.run_until_complete(engine.main())
