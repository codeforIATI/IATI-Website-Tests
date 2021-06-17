from utility import utility
from web_test_base import WebTestBase


class TestIATIStandard(WebTestBase):
    """
    Test IATI website (iatistandard.org)
    """
    requests_to_load = {
        'iatistandard.org': {
            'url': 'http://www.iatistandard.org'
        }
    }

    def test_contains_links(self, loaded_request):
        """
        Confirm the page contains links to:

        * /en/news/
        * /en/about/
        * /en/iati-standard/
        * /en/using-data/
        * /en/contact/
        * /en/privacy-policy/
        """
        result = utility.get_links_from_page(loaded_request)

        # Selection of header links
        assert "/en/news/" in result
        assert "/en/about/" in result
        assert "/en/iati-standard/" in result
        assert "/en/using-data/" in result

        # Selection of footer links
        assert "/en/contact/" in result
        assert "/en/privacy-policy/" in result

    def test_contains_expected_text(self, loaded_request):
        """
        Confirm the page contains the following text:

        IATI is a global initiative to improve the transparency
        of development and humanitarian resources
        """
        text_to_find = "IATI is a global initiative to improve the " + \
                       "transparency of development and humanitarian " + \
                       "resources"

        assert text_to_find in loaded_request.text

    def test_contains_newsletter_signup_form(self, loaded_request):
        """
        Confirm the page includes a newsletter signup form.
        """

        assert utility.locate_xpath_result(
            loaded_request,
            '//*[@id="mc-embedded-subscribe-form"]')
