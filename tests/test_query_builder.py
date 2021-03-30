# import pytest
# from utility import utility
# from web_test_base import WebTestBase


# class TestQueryBuilder(WebTestBase):
#     """
#     Test query builder (datastore.iatistandard.org/query/)
#     """
#     requests_to_load = {
#         'datastore.iatistandard.org/query/': {
#             'url': 'http://datastore.iatistandard.org/query/'
#         },
#         'POST Example': {
#             'url': 'http://datastore.iatistandard.org/query/index.php',
#             'method': 'POST',
#             'data': {
#                 'format': 'activity',
#                 'grouping': 'summary',
#                 'sample-size': '50 rows',
#                 'reporting-org[]': 'XM-DAC-3-1',
#                 'sector[]': '12181',
#                 'recipient-region[]': '298',
#                 'submit': 'Submit'
#             }
#         },
#         'Publisher Information': {
#             'url': 'http://datastore.iatistandard.org/query/helpers/groups_cache_dc.json',
#             'min_response_size': 1500000
#         }
#     }

#     @pytest.mark.parametrize("target_request", ["datastore.iatistandard.org/query/", "POST Example"])
#     def test_locate_links(self, target_request):
#         """
#         Confirm the page contains a link to:

#         * https://iatistandard.org/en/using-data/IATI-tools-and-resources/IATI-datastore/
#         """
#         req = self.loaded_request_from_test_name(target_request)

#         result = utility.get_links_from_page(req)

#         assert "https://iatistandard.org/en/using-data/IATI-tools-and-resources/IATI-datastore/" in result

#     @pytest.mark.parametrize("target_request", ["POST Example"])
#     def test_form_submit_link(self, target_request):
#         """
#         Confirm result page contains a link to the relevant search.
#         """
#         req = self.loaded_request_from_test_name(target_request)

#         result = utility.get_links_from_page(req)

#         assert "http://datastore.iatistandard.org/api/1/access/activity.csv?reporting-org=XM-DAC-3-1&sector=12181&recipient-region=298" in result
