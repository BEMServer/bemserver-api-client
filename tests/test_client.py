"""BEMServer API client tests"""

import pytest

from requests.auth import HTTPBasicAuth

from bemserver_api_client import BEMServerApiClient
from bemserver_api_client.client import REQUIRED_API_VERSION
from bemserver_api_client.exceptions import BEMServerAPIVersionError
from bemserver_api_client.request import BEMServerApiClientRequest
from bemserver_api_client.resources import RESOURCES_MAP


class TestAPIClient:
    def test_api_client_auth(self):
        ret = BEMServerApiClient.make_http_basic_auth("chuck@test.com", "N0rr1s")
        assert isinstance(ret, HTTPBasicAuth)
        assert isinstance(ret.username, bytes)
        assert isinstance(ret.password, bytes)
        assert ret.username.decode(encoding="utf-8") == "chuck@test.com"
        assert ret.password.decode(encoding="utf-8") == "N0rr1s"

    def test_api_client_class(self):
        apicli = BEMServerApiClient("localhost:5050")
        assert apicli.use_ssl
        assert apicli.base_uri_prefix == "http"
        assert apicli.uri_prefix == "https://"
        assert apicli.base_uri == "https://localhost:5050"
        apicli.use_ssl = False
        assert apicli.uri_prefix == "http://"
        assert apicli.base_uri == "http://localhost:5050"

        apicli.base_uri_prefix = "http+mock"
        assert apicli.uri_prefix == "http+mock://"
        assert apicli.base_uri == "http+mock://localhost:5050"
        apicli.use_ssl = True
        assert apicli.uri_prefix == "https+mock://"
        assert apicli.base_uri == "https+mock://localhost:5050"

        assert isinstance(apicli._request_manager, BEMServerApiClientRequest)

    def test_api_client_resources(self):
        assert len(RESOURCES_MAP) == 60

        apicli = BEMServerApiClient("localhost:5050")

        for resource_name, resource_cls in RESOURCES_MAP.items():
            assert resource_cls.client_entrypoint is not None
            assert hasattr(apicli, resource_name)
            assert isinstance(getattr(apicli, resource_name), resource_cls)

        assert not hasattr(apicli, "whatever_resources_that_does_not_exist")

    def test_api_client_required_api_version_manual(self):
        req_version_min = REQUIRED_API_VERSION["min"]
        v = f"{req_version_min.major}.{req_version_min.minor}.42"
        BEMServerApiClient.check_api_version(str(v))

        # API version not compatible with client.
        with pytest.raises(BEMServerAPIVersionError):
            BEMServerApiClient.check_api_version("1.0.0")

        # Invalid API versionning.
        with pytest.raises(BEMServerAPIVersionError):
            BEMServerApiClient.check_api_version(None)
        with pytest.raises(BEMServerAPIVersionError):
            BEMServerApiClient.check_api_version("invalid")

    def test_api_client_required_api_version_auto_check(self, mock_request):
        host = "localhost:5000"
        auto_check = True
        req_mngr = mock_request

        BEMServerApiClient(host, auto_check=auto_check, request_manager=req_mngr)

        # API version not compatible with client.
        with pytest.raises(BEMServerAPIVersionError):
            BEMServerApiClient(host, auto_check=auto_check, request_manager=req_mngr)

        # Invalid API versionning.
        with pytest.raises(BEMServerAPIVersionError):
            BEMServerApiClient(host, auto_check=auto_check, request_manager=req_mngr)
