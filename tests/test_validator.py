# from lxml import etree
# import pytest
# from utility import utility
# from web_test_base import WebTestBase


# class TestIATIValidator(WebTestBase):
#     """
#     Test validator (validator.iatistandard.org)
#     """
#     requests_to_load = {
#         'validator.iatistandard.org': {
#             'url': 'http://validator.iatistandard.org/'
#         },
#         'Valid paste data': {
#             'url': 'http://validator.iatistandard.org/index.php',
#             'method': 'POST',
#             'data': {
#                 'paste': utility.load_file_contents('data/valid.xml')
#             }
#         },
#         'Invalid paste data': {
#             'url': 'http://validator.iatistandard.org/index.php',
#             'method': 'POST',
#             'data': {
#                 'paste': utility.load_file_contents('data/invalid.xml')
#             }
#         },
#         'Valid URL data': {
#             'url': 'http://validator.iatistandard.org/index.php',
#             'method': 'POST',
#             'data': {
#                 'url': 'https://raw.githubusercontent.com/IATI/IATI-Extra-Documentation/version-2.01/en/activity-standard/activity-standard-example-annotated.xml'
#             }
#         },
#         'Invalid URL data': {
#             'url': 'http://validator.iatistandard.org/index.php',
#             'method': 'POST',
#             'data': {
#                 'url': 'http://validator.iatistandard.org/index.php'
#             }
#         }
#     }

#     @pytest.mark.parametrize("target_request", ["validator.iatistandard.org"])
#     def test_contains_links(self, target_request):
#         """
#         Confirm the validator contains a link to iatistandard.org
#         """
#         response = self.loaded_request_from_test_name(target_request)
#         page_links = utility.get_links_from_page(response)

#         assert "http://iatistandard.org/" in page_links

#     @pytest.mark.parametrize("target_request", ["validator.iatistandard.org"])
#     def test_contains_form(self, target_request):
#         """
#         Confirm the validator contains a form on each of three tabs.
#         """
#         response = self.loaded_request_from_test_name(target_request)

#         assert utility.locate_xpath_result(
#             response, '//*[@id="status"]/div/form')
#         assert utility.locate_xpath_result(
#             response, '//*[@id="fileTab"]/div/form')
#         assert utility.locate_xpath_result(
#             response, '//*[@id="extra"]/div/form')

#     @pytest.mark.parametrize("target_request", ["Valid paste data", "Valid URL data"])
#     def test_valid_input_xml(self, target_request):
#         """
#         Confirm the validator correctly identifies valid XML as such.
#         """
#         response = self.loaded_request_from_test_name(target_request)
#         text = utility.get_text_from_xpath(response, '//*[@id="status"]/div[2]')
#         assert text[0].strip() == "This is a well formed xml file."

#     @pytest.mark.parametrize("target_request", ["Invalid paste data", "Invalid URL data"])
#     def test_invalid_input_xml(self, target_request):
#         """
#         Confirm the validator correctly identifies invalid XML as such.
#         """
#         response = self.loaded_request_from_test_name(target_request)
#         text = utility.get_text_from_xpath(response, '//*[@id="status"]/div[2]')
#         assert text[0].strip() == "This is not a well-formed xml file"
