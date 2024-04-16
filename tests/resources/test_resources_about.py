"""BEMServer API client about resources tests"""

import pytest

from bemserver_api_client.resources.about import AboutResources
from bemserver_api_client.resources.base import BaseResources


class TestAPIClientResourcesAbout:
    def test_api_client_resources_about(self):
        assert issubclass(AboutResources, BaseResources)
        assert AboutResources.endpoint_base_uri == "/about/"
        assert AboutResources.disabled_endpoints == [
            "getone",
            "create",
            "update",
            "delete",
        ]
        assert AboutResources.client_entrypoint == "about"

    def test_api_client_resources_about_errors(self, mock_request):
        res = AboutResources(mock_request)
        with pytest.raises(NotImplementedError):
            res._verify_disabled("delete")
        with pytest.raises(NotImplementedError):
            res.delete(0)
