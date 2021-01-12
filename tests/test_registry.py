import pytest
from utility import utility
from web_test_base import WebTestBase


class TestIATIRegistry(WebTestBase):
    """
    Test registry (iatiregistry.org)
    """
    requests_to_load = {
        'iatiregistry.org': {
            'url': 'http://iatiregistry.org/'
        },
        'IATI Registry registration page': {
            'url': 'http://iatiregistry.org/user/register'
        },
        'IATI Registry login page': {
            'url': 'http://iatiregistry.org/user/login'
        },
        'IATI Registry: Random publisher page': {
            'url': 'http://iatiregistry.org/publisher/worldbank'
        },
        'IATI Registry: Random dataset': {
            'url': 'http://iatiregistry.org/dataset/fcdo-af'
        },
        'IATI Registry API: Package search call': {
            'url': 'http://iatiregistry.org/api/3/action/package_search'
        }
    }

    @pytest.mark.parametrize("target_request", [
        "iatiregistry.org",
        "IATI Registry registration page",
        "IATI Registry login page",
        "IATI Registry: Random dataset",
        "IATI Registry: Random publisher page"
    ])
    def test_contains_links(self, target_request):
        """
        Test that each page contains links to the defined URLs.
        """
        req = self.loaded_request_from_test_name(target_request)
        result = utility.get_links_from_page(req)

        assert "http://iatistandard.org/en/about/" in result

    @pytest.mark.parametrize("target_request", ["IATI Registry registration page"])
    def test_registration_form_presence(self, target_request):
        """
        Test that there is a valid registration form on the Registry Registration Page.
        """
        req = self.loaded_request_from_test_name(target_request)
        form_xpath = '//*[@id="user-register-form"]'
        form_method_xpath = '//*[@id="user-register-form"]/@method'
        input_xpath = '//*[@id="user-register-form"]/div/div/input'
        button_xpath = '//*[@id="user-register-form"]/div/button'

        forms = utility.locate_xpath_result(req, form_xpath)
        form_method = utility.locate_xpath_result(req, form_method_xpath)
        form_inputs = utility.locate_xpath_result(req, input_xpath)
        form_buttons = utility.locate_xpath_result(req, button_xpath)

        assert len(forms) == 1
        assert form_method == ['post']
        assert len(form_inputs) == 5
        assert len(form_buttons) == 1

    @pytest.mark.parametrize("target_request", ["IATI Registry login page"])
    def test_login_form_presence(self, target_request):
        """
        Test that there is a valid login form on the Registry Login Page.
        """
        req = self.loaded_request_from_test_name(target_request)
        form_xpath = '//*[@id="content"]/div[3]/div/section/div/form'
        form_action_xpath = '//*[@id="content"]/div[3]/div/section/div/form/@action'
        form_method_xpath = '//*[@id="content"]/div[3]/div/section/div/form/@method'
        input_xpath = '//*[@id="content"]/div[3]/div/section/div/form/div/div/input'
        button_xpath = '//*[@id="content"]/div[3]/div/section/div/form/div/button'

        forms = utility.locate_xpath_result(req, form_xpath)
        form_action = utility.locate_xpath_result(req, form_action_xpath)
        form_method = utility.locate_xpath_result(req, form_method_xpath)
        form_inputs = utility.locate_xpath_result(req, input_xpath)
        form_buttons = utility.locate_xpath_result(req, button_xpath)

        assert len(forms) == 1
        assert form_action == ['/login_generic?came_from=/user/logged_in']
        assert form_method == ['post']
        assert len(form_inputs) == 2
        assert len(form_buttons) == 1
