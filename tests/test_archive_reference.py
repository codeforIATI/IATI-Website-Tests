import pytest
from utility import utility
from web_test_base import WebTestBase


class TestArchiveReference(WebTestBase):
    """
    Test archive reference (archivereference.iatistandard.org)
    """
    requests_to_load = {
        'IATI Standard Homepage': {
            'url': 'http://archivereference.iatistandard.org/'
        },
        'IATI Standard - Summary Page': {
            'url': 'http://archivereference.iatistandard.org/202/organisation-standard/summary-table/'
        },
        'IATI Standard - Schema Page': {
            'url': 'http://archivereference.iatistandard.org/202/schema/'
        },
        'IATI Standard - Old Schema Version, Developer Docs': {
            'url': 'http://archivereference.iatistandard.org/105/developer/'
        },
        'IATI Standard - Misc Developer Docs Page': {
            'url': 'http://archivereference.iatistandard.org/105/developer/xquery/'
        },
        'IATI Standard - Activity Standard Docs Page': {
            'url': 'http://archivereference.iatistandard.org/105/activity-standard/iati-activities/iati-activity/contact-info/'
        },
        'IATI Standard - Schema Version Homepage': {
            'url': 'http://archivereference.iatistandard.org/201/'
        }
    }

    def test_locate_links(self, loaded_request):
        """
        Tests that each page contains links to the defined URLs.
        """
        result = utility.get_links_from_page(loaded_request)

        assert "/" in result
        assert "http://iatiregistry.org" in result
        assert utility.regex_match_in_list(r'^(\.\./)*license/$', result)
        assert "http://glyphicons.com" in result
        assert "http://creativecommons.org/licenses/by/3.0/" in result

    def test_footer_license_information(self, loaded_request):
        """
        Tests that the footer contains license information.
        This should include information about each text and icon licensing.
        """
        footer_xpath = '//*[@id="footer-credits"]/span'

        result = utility.get_text_from_xpath(loaded_request, footer_xpath)

        assert utility.substring_in_list('Text licensed under CC BY 4.0', result)

    @pytest.mark.parametrize("target_request", ["IATI Standard Homepage"])
    def test_locate_text(self, target_request):
        """
        Tests that each page contains the text
        'technical publishing framework' in the heading.
        """
        req = self.loaded_request_from_test_name(target_request)
        text_to_find = "technical publishing framework"
        xpath_to_locate = '//*[@id="home-strapline"]/h1'

        result = utility.get_text_from_xpath(req, xpath_to_locate)

        assert utility.substring_in_list(text_to_find, result)
