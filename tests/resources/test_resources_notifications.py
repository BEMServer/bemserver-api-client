"""BEMServer API client notifications resources tests"""
from bemserver_api_client.resources.base import BaseResources
from bemserver_api_client.resources import (
    NotificationResources,
)


class TestAPIClientResourcesNotifications:
    def test_api_client_resources_events(self):
        assert issubclass(NotificationResources, BaseResources)
        assert NotificationResources.endpoint_base_uri == "/notifications/"
        assert NotificationResources.disabled_endpoints == []
