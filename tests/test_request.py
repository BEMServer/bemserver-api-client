"""BEMServer API client request tests"""
import io
import pytest

from bemserver_api_client.request import BEMServerApiClientRequest
from bemserver_api_client.exceptions import BEMServerAPIClientValueError
from bemserver_api_client.enums import DataFormat

from tests.conftest import FakeEnum


class TestAPIClientRequest:
    def test_api_client_request(self):
        req = BEMServerApiClientRequest("http://localhost:5000", None)
        assert req._build_uri("/test/") == "http://localhost:5000/test/"

    def test_api_client_request_etag(self):
        assert "GET" in BEMServerApiClientRequest._ETAG_HEADER_BY_HTTP_METHOD
        assert BEMServerApiClientRequest._ETAG_HEADER_BY_HTTP_METHOD["GET"] == (
            "If-None-Match"
        )
        assert "PUT" in BEMServerApiClientRequest._ETAG_HEADER_BY_HTTP_METHOD
        assert BEMServerApiClientRequest._ETAG_HEADER_BY_HTTP_METHOD["PUT"] == (
            "If-Match"
        )
        assert "DELETE" in BEMServerApiClientRequest._ETAG_HEADER_BY_HTTP_METHOD
        assert BEMServerApiClientRequest._ETAG_HEADER_BY_HTTP_METHOD["DELETE"] == (
            "If-Match"
        )

        req = BEMServerApiClientRequest("http://localhost:5000", None)
        assert req._prepare_etag_header("GET", "etag_value") == {
            "If-None-Match": "etag_value"
        }
        assert req._prepare_etag_header("POST", "etag_value") == {}
        assert req._prepare_etag_header("PUT", "etag_value") == {
            "If-Match": "etag_value"
        }
        assert req._prepare_etag_header("DELETE", "etag_value") == {
            "If-Match": "etag_value"
        }
        assert req._prepare_etag_header("GET", None) == {}

    def test_api_client_request_dataformat_header(self):
        req = BEMServerApiClientRequest("http://localhost:5000", None)
        assert req._prepare_dataformat_header(DataFormat.csv) == {
            "Content-Type": DataFormat.csv.value
        }
        assert req._prepare_dataformat_header(DataFormat.json) == {
            "Content-Type": DataFormat.json.value
        }

        with pytest.raises(TypeError):
            req._prepare_dataformat_header(None)
        with pytest.raises(TypeError):
            req._prepare_dataformat_header("other")

        with pytest.raises(
            BEMServerAPIClientValueError, match=f"Invalid data format: {FakeEnum.a}"
        ):
            req._prepare_dataformat_header(FakeEnum.a)

    def test_api_client_request_exclude_empty_files(self):
        sites_csv_data = "Name,Description,IFC_ID,Area\n" "Site 1,Great site,,2000\n"
        sites_csv = io.BytesIO(sites_csv_data.encode())
        assert BEMServerApiClientRequest._exclude_empty_files(
            {
                "sites_csv": sites_csv,
                "buildings_csv": None,
                "zones_csv": io.BytesIO(),
            },
        ) == {"sites_csv": sites_csv}

    def test_api_client_request_fixture(self, mock_request):
        assert isinstance(mock_request, BEMServerApiClientRequest)
        assert mock_request._build_uri("/test/") == "http+mock://localhost:5050/test/"
