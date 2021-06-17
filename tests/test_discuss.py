import pytest
from utility import utility
from web_test_base import WebTestBase


class TestIATIDiscuss(WebTestBase):
    """
    Test discuss (discuss.iatistandard.org)
    """
    requests_to_load = {
        'IATI Discuss': {
            'url': 'http://discuss.iatistandard.org/?iati-website-tests'
        },
        'IATI Discuss Welcome Thread': {
            'url': 'http://discuss.iatistandard.org/t/welcome-to-iati-discuss/6?iati-website-tests'
        }
    }

    def test_contains_links(self, loaded_request):
        """
        Test the page contains a link to:

        http://iatistandard.org/en/about/
        """
        result = utility.get_links_from_page(loaded_request)

        assert "http://iatistandard.org/en/about/" in result

    @pytest.mark.parametrize("target_request", ["IATI Discuss Welcome Thread"])
    def test_welcome_thread_welcomingness(self, target_request):
        """
        Test the Welcome Thread says 'Welcome to IATI Discuss'.
        """
        req = self.loaded_request_from_test_name(target_request)
        title_xpath = '/html/head/title'
        heading_xpath = '//*[@id="main-outlet"]/div[@id="topic-title"]/h1/a'
        subtitle_xpath = '//*[@class="post"]/h1'
        post_body_xpath = '//*[@class="post"]/p'

        title_text = utility.get_text_from_xpath(req, title_xpath)
        heading_text = utility.get_text_from_xpath(req, heading_xpath)
        subtitle_text = utility.get_text_from_xpath(req, subtitle_xpath)
        post_body_text = utility.get_text_from_xpath(req, post_body_xpath)

        assert utility.substring_in_list('Welcome to IATI Discuss', title_text)
        assert utility.substring_in_list('Welcome to IATI Discuss', heading_text)
        assert utility.substring_in_list('Welcome', subtitle_text)
        assert utility.substring_in_list('Welcome', post_body_text)
