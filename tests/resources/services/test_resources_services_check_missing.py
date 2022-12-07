"""BEMServer API client services check missing resources tests"""
from bemserver_api_client.resources.base import BaseResources
from bemserver_api_client.resources import (
    ST_CheckMissingByCampaignResources,
)
from bemserver_api_client.response import BEMServerApiClientResponse


class TestAPIClientResourcesServicesCleanup:
    def test_api_client_resources_services_check_missing(self):
        assert issubclass(ST_CheckMissingByCampaignResources, BaseResources)
        assert ST_CheckMissingByCampaignResources.endpoint_base_uri == (
            "/st_check_missings_by_campaigns/"
        )
        assert ST_CheckMissingByCampaignResources.disabled_endpoints == []
        assert hasattr(ST_CheckMissingByCampaignResources, "get_full")

    def test_api_client_resources_services_check_missing_endpoints(self, mock_request):
        cleanup_camp_res = ST_CheckMissingByCampaignResources(mock_request)
        resp = cleanup_camp_res.get_full()
        assert isinstance(resp, BEMServerApiClientResponse)
        assert resp.status_code == 200
        assert resp.is_json
        assert resp.pagination == {}
        assert len(resp.data) == 3
