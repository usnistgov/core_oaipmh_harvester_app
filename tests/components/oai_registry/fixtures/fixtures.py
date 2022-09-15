""" fixtures files for Data
"""
import json
import os

from core_main_app.settings import XML_POST_PROCESSOR
from core_main_app.utils import xml as xml_utils
from core_main_app.utils.integration_tests.fixture_interface import FixtureInterface
from core_oaipmh_common_app.utils import UTCdatetime
from core_oaipmh_harvester_app.components.oai_record.models import OaiRecord
from core_oaipmh_harvester_app.components.oai_registry.models import OaiRegistry
from core_oaipmh_harvester_app.utils import transform_operations
from tests.test_settings import OAI_HARVESTER_ROOT

DUMP_OAI_PMH_TEST_PATH = os.path.join(OAI_HARVESTER_ROOT, "utils", "data")


class OaiPmhFixtures(FixtureInterface):
    """
    Represent OaiPmh Integration Fixture
    """

    url = "http://www.server.com"
    harvest_rate = 5000
    harvest = True
    registry = None
    oai_identify = None
    oai_sets = []
    oai_metadata_formats = []
    oai_metadata_format_sets = []
    oai_records = []
    name = "Registry"

    """
        Registry's methods
    """

    def insert_data(self):
        """insert_data

        Args:

        Returns:

        """
        pass

    def insert_registry(
        self, name="Registry", insert_related_collections=True, insert_records=True
    ):
        """insert_registry

        Args:
            name:
            insert_related_collections:
            insert_records:

        Returns:

        """
        self.registry = OaiRegistry(
            name=name,
            url=self.url,
            harvest_rate=self.harvest_rate,
            harvest=self.harvest,
        )
        self.registry.save()

        if insert_related_collections:
            self.oai_identify = self.insert_oai_identify()
            self.oai_sets = self.insert_oai_sets()
            self.oai_metadata_formats = self.insert_oai_metadata_formats()

        if insert_records:
            self.oai_records = self.insert_oai_records()

    """
        OaiIdentify's methods
    """

    def insert_oai_identify(self):
        """insert_oai_identify

        Args:

        Returns:

        """
        identify = OaiPmhMock.mock_oai_identify(version=1)
        identify.registry = self.registry
        identify.save()
        return identify

    """
       OaiSet's methods
    """

    def insert_oai_sets(self):
        """insert_oai_sets

        Args:

        Returns:

        """
        sets = OaiPmhMock.mock_oai_set(version=1)
        saved_sets = []
        for set_ in sets:
            set_.registry = self.registry
            set_.harvest = True
            set_.save()
            saved_sets.append(set_)

        return saved_sets

    """
       OaiMetadataFormat's methods
    """

    def insert_oai_metadata_formats(self):
        """insert_oai_metadata_formats

        Args:

        Returns:

        """
        metadata_formats = OaiPmhMock.mock_oai_metadata_format(version=1)
        saved_metadata_formats = []
        for metadata_format in metadata_formats:
            metadata_format.registry = self.registry
            metadata_format.harvest = True
            metadata_format.save()
            saved_metadata_formats.append(metadata_format)

        return saved_metadata_formats

    """
       OaiRecord's methods
    """

    def insert_oai_records(self):
        """insert_oai_records

        Args:

        Returns:

        """
        oai_records = OaiPmhMock.mock_oai_record(version=1)
        saved_oai_records = []
        for oai_record in oai_records:
            oai_record.title = oai_record.identifier
            oai_record.registry = self.registry
            oai_record.harvester_metadata_format = self.oai_metadata_formats[0]
            oai_record.dict_content = xml_utils.raw_xml_to_dict(
                oai_record.xml_content, postprocessor=XML_POST_PROCESSOR
            )
            oai_record.save()
            saved_oai_records.append(oai_record)

        return saved_oai_records


class OaiPmhMock:
    """OaiPmh Mock"""

    @staticmethod
    def mock_oai_identify(version=1):
        """mock_oai_identify

        Args:
            version:

        Returns:

        """
        with open(
            os.path.join(
                DUMP_OAI_PMH_TEST_PATH, "oai_identify_v{0}.json".format(version)
            )
        ) as file:
            data = file.read()
        data_json = json.loads(data)
        oai_identifier = (
            transform_operations.transform_dict_identifier_to_oai_identifier(data_json)
        )
        return oai_identifier

    @staticmethod
    def mock_oai_metadata_format(version=1):
        """mock_oai_metadata_format

        Args:
            version:

        Returns:

        """
        with open(
            os.path.join(
                DUMP_OAI_PMH_TEST_PATH, "oai_metadata_format_v{0}.json".format(version)
            )
        ) as file:
            data = file.read()
        data_json = json.loads(data)
        list_oai_metadata_formats = transform_operations.transform_dict_metadata_format_to_oai_harvester_metadata_format(
            data_json
        )
        return list_oai_metadata_formats

    @staticmethod
    def mock_oai_set(version=1):
        """mock_oai_set

        Args:
            version:

        Returns:

        """
        with open(
            os.path.join(DUMP_OAI_PMH_TEST_PATH, "oai_set_v{0}.json".format(version))
        ) as file:
            data = file.read()
        data_json = json.loads(data)
        list_sets = transform_operations.transform_dict_set_to_oai_harvester_set(
            data_json
        )
        return list_sets

    @staticmethod
    def mock_oai_first_set(version=1):
        """mock_oai_first_set

        Args:

        Returns:
            version:

        """
        list_sets = OaiPmhMock.mock_oai_set(version)
        return list_sets[0]

    @staticmethod
    def mock_oai_first_metadata_format(version=1):
        """mock_oai_first_metadata_format

        Args:

        Returns:
            version:

        """
        list_oai_metadata_formats = OaiPmhMock.mock_oai_metadata_format(version)
        return list_oai_metadata_formats[0]

    @staticmethod
    def mock_oai_record(version=1):
        """mock_oai_record

        Args:

        Returns:
            version:

        """
        with open(
            os.path.join(DUMP_OAI_PMH_TEST_PATH, "oai_record_v{0}.json".format(version))
        ) as file:
            data = file.read()
        data_json = json.loads(data)

        return [
            OaiRecord(
                identifier=item["identifier"],
                last_modification_date=(
                    UTCdatetime.utc_datetime_iso8601_to_datetime(item["datestamp"])
                ),
                deleted=item["deleted"],
                xml_content=(
                    str(item["metadata"]) if item["metadata"] is not None else None
                ),
            )
            for item in data_json
        ]

    @staticmethod
    def mock_oai_first_record(version=1, as_json=False):
        """mock_oai_first_record

        Args:
            version:
            as_json:

        Returns:

        """
        list_records = OaiPmhMock.mock_oai_record(version)
        return (
            list_records[0]
            if not as_json
            else {
                "identifier": list_records[0].identifier,
                "datestamp": str(list_records[0].last_modification_date),
                "deleted": list_records[0].deleted,
                "metadata": list_records[0].xml_content,
            }
        )

    @staticmethod
    def mock_oai_response_list_records(with_resumption_token=True):
        """mock_oai_response_list_records

        Args:
            with_resumption_token:

        Returns:

        """
        xml_file = "response_list_records_oai_demo.xml"
        if not with_resumption_token:
            xml_file = "response_list_records_oai_demo_no_token.xml"

        with open(os.path.join(DUMP_OAI_PMH_TEST_PATH, xml_file)) as file:
            data = file.read()

        return data
