"""BEMServer API client tasks resources tests"""

from bemserver_api_client.resources.base import BaseResources
from bemserver_api_client.resources.tasks import TaskByCampaignResources


class TestAPIClientResourcesTasks:
    def test_api_client_resources_task_by_campaign(self):
        assert issubclass(TaskByCampaignResources, BaseResources)
        assert TaskByCampaignResources.endpoint_base_uri == ("/tasks_by_campaigns/")
        assert TaskByCampaignResources.disabled_endpoints == []
        assert TaskByCampaignResources.client_entrypoint == ("task_by_campaign")
