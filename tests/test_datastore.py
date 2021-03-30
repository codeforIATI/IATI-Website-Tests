# import pytest
# from datetime import date, datetime, timedelta
# from utility import utility
# from web_test_base import WebTestBase


# class TestIATIDatastore(WebTestBase):
#     """
#     Test datastore (datastore.iatistandard.org)
#     """
#     requests_to_load = {
#         'datastore.iatistandard.org': {
#             'url': 'http://datastore.iatistandard.org/'
#         },
#         'Activities updated since 2 days ago': {
#             'url': 'http://datastore.iatistandard.org/api/1/access/activity.xml?limit=0&last-change__gt=' + str(date.today() - timedelta(days=2)),
#             'min_response_size': 295
#         },
#         'Activities updated since 3 days ago': {
#             'url': 'http://datastore.iatistandard.org/api/1/access/activity.xml?limit=0&last-change__gt=' + str(date.today() - timedelta(days=3)),
#             'min_response_size': 295
#         },
#         'Datastore download: CSV': {
#             'url': 'http://datastore.iatistandard.org/api/1/access/activity.csv'
#         },
#         'Datastore download: XML': {
#             'url': 'http://datastore.iatistandard.org/api/1/access/activity.xml'
#         },
#         'Datastore download: JSON': {
#             'url': 'http://datastore.iatistandard.org/api/1/access/activity.json'
#         },
#         'Datastore list of datasets': {
#             'url': 'http://datastore.iatistandard.org/api/1/about/datasets/fetch_status'
#         }
#     }

#     @pytest.mark.parametrize("target_request", ["Activities updated since 2 days ago", "Activities updated since 3 days ago"])
#     def test_recent_activities(self, target_request):
#         """
#         Confirm the datastore API knows of activities updated recently.
#         """
#         req = self.loaded_request_from_test_name(target_request)
#         xpath = '//result/iati-activities/query/total-count'

#         updated_recently = utility.get_single_int_from_xpath(req, xpath)

#         assert updated_recently > 0

#     @pytest.mark.parametrize("expected_content_type", ["application/xml", "application/json", "text/csv"])
#     def test_api_output_filetype(self, expected_content_type):
#         """
#         Confirm the datastore returns data of the requested filetype.

#         The test is conducted based on the data returned in the
#         `Content-Type` response header. E.g.:

#             Content-Type: application/xml; charset=utf-8
#         """
#         file_extension = expected_content_type.split("/")[1]
#         loaded_request = self.loaded_request_from_test_name("Datastore download: {}".format(file_extension.upper()))

#         content_type = loaded_request.headers["content-type"]

#         assert content_type.startswith(expected_content_type)

#     @pytest.mark.parametrize("target_request", ["Datastore list of datasets"])
#     def test_last_successful_fetch(self, target_request):
#         """
#         Confirm the datastore has fetched data within the last 7 days.
#         """
#         loaded_request = self.loaded_request_from_test_name(target_request)
#         successful_fetch_dates = list()
#         json_datasets = loaded_request.json()
#         list_of_datasets = json_datasets['datasets']

#         resources = [list(dataset.values())[0] for dataset in list_of_datasets]
#         successful_fetch_dates = [datetime.strptime(resource['last_successful_fetch'][:10], '%Y-%m-%d') for resource in resources if resource['last_successful_fetch'] is not None]

#         assert max(successful_fetch_dates) >= (datetime.now() - timedelta(days=7))
