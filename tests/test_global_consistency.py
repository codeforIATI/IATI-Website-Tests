import pytest
from utility import utility
from web_test_base import WebTestBase


class TestGlobalConsistency(WebTestBase):
    requests_to_load = {
        'IATI Registry - Homepage': {
            'url': 'https://iatiregistry.org/'
        },
        'IATI Registry - Activity Dataset Page': {
            'url': 'https://iatiregistry.org/dataset?q=&filetype=Activity'
        },
        'IATI Registry - Organisation Dataset Page': {
            'url': 'https://iatiregistry.org/dataset?q=&filetype=Organisation'
        },
        'IATI Standard - Homepage': {
            'url': 'https://iatistandard.org/'
        },
        'IATI Dashboard - Homepage': {
            'url': 'http://dashboard.iatistandard.org/'
        },
        'IATI Dashboard - Activities Page': {
            'url': 'http://dashboard.iatistandard.org/activities.html'
        },
        'IATI Dashboard - Files Page': {
            'url': 'http://dashboard.iatistandard.org/files.html'
        },
        'IATI Dashboard - Publisher Page': {
            'url': 'http://dashboard.iatistandard.org/publishers.html'
        },
        'Datastore API - Activity Count': {
            'url': 'http://datastore.iatistandard.org/api/1/access/activity.xml?limit=0', 'min_response_size': 295
        },
        'Query Builder': {
            'url': 'http://datastore.iatistandard.org/query/'
        }
    }

    def _count_element_on_page(self, test_name, xpath):
        req = self.loaded_request_from_test_name(test_name)

        located_elements = utility.locate_xpath_result(req, xpath)
        result = len(located_elements)

        return result

    def _locate_int_on_page(self, test_name, xpath):
        req = self.loaded_request_from_test_name(test_name)

        result = utility.get_single_int_from_xpath(req, xpath)

        return result

    @pytest.fixture
    def dash_home_activity_count(cls):
        return cls._locate_int_on_page('IATI Dashboard - Homepage', '//td[@id="activities-count"]/a')

    @pytest.fixture
    def dash_home_unique_activity_count(cls):
        return cls._locate_int_on_page('IATI Dashboard - Homepage', '//td[@id="unique-activities-count"]/a')

    @pytest.fixture
    def dash_home_activity_file_count(cls):
        return cls._locate_int_on_page('IATI Dashboard - Homepage', '//td[@id="activity-files-count"]/a')

    @pytest.fixture
    def dash_home_org_file_count(cls):
        return cls._locate_int_on_page('IATI Dashboard - Homepage', '//td[@id="organisation-files-count"]/a')

    @pytest.fixture
    def dash_home_publisher_count(cls):
        return cls._locate_int_on_page('IATI Dashboard - Homepage', '//td[@id="publishers-count"]/a')

    @pytest.fixture
    def dash_activities_activity_count(cls):
        return cls._locate_int_on_page('IATI Dashboard - Activities Page', '//span[@id="total-activities"]')

    @pytest.fixture
    def dash_activities_unique_activity_count(cls):
        return cls._locate_int_on_page('IATI Dashboard - Activities Page', '//span[@id="unique-activities"]')

    @pytest.fixture
    def dash_files_activity_file_count(cls):
        return cls._locate_int_on_page('IATI Dashboard - Files Page', '//span[@id="total-activity-files"]')

    @pytest.fixture
    def dash_files_org_file_count(cls):
        return cls._locate_int_on_page('IATI Dashboard - Files Page', '//span[@id="total-organisation-files"]')

    @pytest.fixture
    def dash_publishers_publisher_count(cls):
        return cls._locate_int_on_page('IATI Dashboard - Publisher Page', '//span[@id="publishers"]')

    @pytest.fixture
    def datastore_api_activity_count(cls):
        return cls._locate_int_on_page('Datastore API - Activity Count', '//result/iati-activities/query/total-count')

    @pytest.fixture
    def registry_home_publisher_count(cls):
        return cls._locate_int_on_page('IATI Registry - Homepage', '//*[@id="home-icons"]/div/div[2]/div/a/strong')

    @pytest.fixture
    def registry_activity_count(cls):
        return utility.get_total_num_activities()

    @pytest.fixture
    def registry_activity_file_count(cls):
        return cls._locate_int_on_page('IATI Registry - Activity Dataset Page', '//*[@id="content"]/div[3]/div/section[1]/div[1]/form/h2')

    @pytest.fixture
    def registry_organisation_file_count(cls):
        return cls._locate_int_on_page('IATI Registry - Organisation Dataset Page', '//*[@id="content"]/div[3]/div/section[1]/div[1]/form/h2')

    @pytest.fixture
    def query_builder_publisher_count(cls):
        return cls._count_element_on_page('Query Builder', '//*[@id="reporting-org"]/option')

    @pytest.fixture
    def standard_home_activity_count(cls):
        return cls._locate_int_on_page('IATI Standard - Homepage', '//*[@id="stat-activities"]')

    @pytest.fixture
    def standard_home_publisher_count(cls):
        return cls._locate_int_on_page('IATI Standard - Homepage', '//*[@id="stat-publishers"]')

    def test_activity_count_above_min(self, dash_home_activity_count, dash_home_unique_activity_count, dash_activities_activity_count, dash_activities_unique_activity_count, datastore_api_activity_count):
        """
        Test to ensure the unique activity count is above a specified minumum value.
        This checks both the dashboard and datastore.
        """
        min_activity_count = 850000

        assert dash_home_activity_count >= min_activity_count
        assert dash_home_unique_activity_count >= min_activity_count
        assert dash_activities_activity_count >= min_activity_count
        assert dash_activities_unique_activity_count >= min_activity_count
        assert datastore_api_activity_count >= min_activity_count

    def test_activity_count_dash_value_consistency(self, dash_home_activity_count, dash_home_unique_activity_count, dash_activities_activity_count, dash_activities_unique_activity_count):
        """
        Test to ensure activity counts are consistent within the dashboard.
        """
        assert dash_home_activity_count == dash_activities_activity_count
        assert dash_home_unique_activity_count == dash_activities_unique_activity_count

    def test_unique_vs_total_dash_activity_values(self, dash_home_activity_count, dash_home_unique_activity_count, dash_activities_activity_count, dash_activities_unique_activity_count):
        """
        Test to ensure unique activity counts within the dashboard are not higher
        than the overall activity counts.
        """
        assert dash_home_activity_count >= dash_home_unique_activity_count
        assert dash_activities_activity_count >= dash_activities_unique_activity_count

    @pytest.mark.skip(reason="Data is often wrong due to delays between dashboard regeneration cycles")
    def test_activity_count_consistency_datastore_dashboard(self, datastore_api_activity_count, dash_home_unique_activity_count):
        """
        Test to ensure the activity count is consistent, within a margin of error,
        between the datastore and dashboard.
        """
        max_datastore_disparity = 0.1

        assert datastore_api_activity_count >= dash_home_unique_activity_count * (1 - max_datastore_disparity)
        assert datastore_api_activity_count <= dash_home_unique_activity_count * (1 + max_datastore_disparity)

    def test_activity_count_consistency_iatistandard_homepage(self, registry_activity_count, standard_home_activity_count):
        """
        Test to ensure the activity count is consistent, within a margin of error,
        between the registry and the IATI Standard homepage.
        """
        max_registry_disparity = 0.03

        assert registry_activity_count >= standard_home_activity_count * (1 - max_registry_disparity)
        assert registry_activity_count <= standard_home_activity_count * (1 + max_registry_disparity)

    def test_activity_file_count_above_min(self, registry_activity_file_count, dash_home_activity_file_count, dash_files_activity_file_count):
        """
        Test to ensure the unique activity file count is above a specified minumum value.
        This checks both the dashboard and registry.
        """
        min_file_count = 4700

        assert registry_activity_file_count >= min_file_count
        assert dash_home_activity_file_count >= min_file_count
        assert dash_files_activity_file_count >= min_file_count

    def test_activity_file_count_dash_values(self, dash_home_activity_file_count, dash_files_activity_file_count):
        """
        Test to ensure activity file counts are consistent within the dashboard.
        """
        assert dash_home_activity_file_count == dash_files_activity_file_count

    @pytest.mark.skip(reason="Skipping until we get more consistency on these numbers")
    def test_activity_file_count_consistency(self, registry_activity_file_count, dash_home_activity_file_count, dash_files_activity_file_count):
        """
        Test to ensure the activity file count is consistent, within a margin of error,
        between the registry and dashboard.
        """
        max_registry_disparity = 0.15

        assert registry_activity_file_count >= dash_files_activity_file_count * (1 - max_registry_disparity)
        assert registry_activity_file_count <= dash_files_activity_file_count * (1 + max_registry_disparity)

    def test_org_file_count_above_min(self, registry_organisation_file_count, dash_home_org_file_count, dash_files_org_file_count):
        """
        Test to ensure the organisation file count is above a specified minumum value.
        This checks both the dashboard and registry.
        """
        min_file_count = 450

        assert registry_organisation_file_count >= min_file_count
        assert dash_home_org_file_count >= min_file_count
        assert dash_files_org_file_count >= min_file_count

    def test_org_file_count_dash_values(self, dash_home_org_file_count, dash_files_org_file_count):
        """
        Test to ensure organisation file counts are consistent within the dashboard.
        """
        assert dash_home_org_file_count == dash_files_org_file_count

    @pytest.mark.skip(reason="Skipping until we get more consistency on these numbers")
    def test_organisation_dataset_count_consistency(self, registry_organisation_file_count, dash_home_org_file_count, dash_files_org_file_count):
        """
        Test to ensure the activity file count is consistent, within a margin of error,
        between the registry and dashboard.
        """
        max_registry_disparity = 0.05

        assert registry_organisation_file_count >= dash_files_org_file_count * (1 - max_registry_disparity)
        assert registry_organisation_file_count <= dash_files_org_file_count * (1 + max_registry_disparity)

    def test_publisher_count_above_min(self, registry_home_publisher_count, dash_home_publisher_count, dash_publishers_publisher_count):
        """
        Test to ensure the publisher count is above a specified minumum value.
        This checks both the dashboard and registry.
        """
        min_publisher_count = 630

        assert registry_home_publisher_count >= min_publisher_count
        assert dash_home_publisher_count >= min_publisher_count
        assert dash_publishers_publisher_count >= min_publisher_count

    def test_publisher_count_dash_values(self, dash_home_publisher_count, dash_publishers_publisher_count):
        """
        Test to ensure organisation file counts are consistent within the dashboard.
        """
        assert dash_home_publisher_count == dash_publishers_publisher_count

    @pytest.mark.skip(reason="Skipping until we get more consistency on these numbers")
    def test_publisher_count_consistency_dashboard(self, registry_home_publisher_count, dash_home_publisher_count):
        """
        Test to ensure the publisher count is consistent, within a margin of error,
        between the registry and dashboard.
        """
        max_registry_disparity = 0.03

        assert registry_home_publisher_count >= dash_home_publisher_count * (1 - max_registry_disparity)
        assert registry_home_publisher_count <= dash_home_publisher_count * (1 + max_registry_disparity)

    def test_publisher_count_consistency_query_builder(self, registry_home_publisher_count, query_builder_publisher_count):
        """
        Test to ensure the publisher count is consistent, within a margin of error,
        between the registry and query builder.
        """
        max_registry_disparity = 0.01

        assert registry_home_publisher_count >= query_builder_publisher_count * (1 - max_registry_disparity)
        assert registry_home_publisher_count <= query_builder_publisher_count * (1 + max_registry_disparity)

    def test_publisher_count_consistency_iatistandard_homepage(self, registry_home_publisher_count, standard_home_publisher_count):
        """
        Test to ensure the publisher count is consistent, within a margin of error,
        between the registry and the IATI Standard homepage.
        """
        max_registry_disparity = 0.03

        assert registry_home_publisher_count >= standard_home_publisher_count * (1 - max_registry_disparity)
        assert registry_home_publisher_count <= standard_home_publisher_count * (1 + max_registry_disparity)
