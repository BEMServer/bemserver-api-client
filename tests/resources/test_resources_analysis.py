"""BEMServer API client analysis resources tests"""
from bemserver_api_client.resources.base import BaseResources
from bemserver_api_client.resources import AnalysisResources
from bemserver_api_client.response import BEMServerApiClientResponse


class TestAPIClientResourcesAnalysis:
    def test_api_client_resources_analysis(self):
        assert issubclass(AnalysisResources, BaseResources)
        assert AnalysisResources.endpoint_base_uri == "/analysis/"
        assert AnalysisResources.disabled_endpoints == [
            "getall",
            "getone",
            "create",
            "update",
            "delete",
        ]
        assert hasattr(AnalysisResources, "get_completeness")

    def test_api_client_resources_analysis_endpoints(self, mock_request):
        analysis_res = AnalysisResources(mock_request)
        resp = analysis_res.get_completeness(
            start_time="2020-01-01T00:00:00+00:00",
            end_time="2020-02-01T00:00:00+00:00",
            timeseries=[1, 2],
            data_state=1,
            bucket_width_value=1,
            bucket_width_unit="week",
        )
        assert isinstance(resp, BEMServerApiClientResponse)
        assert resp.status_code == 200
        assert resp.is_json
        assert resp.pagination == {}
        assert resp.etag == "etag_analysis_completeness"
        assert resp.data == {
            "timeseries": {
                "1": {
                    "avg_count": 893.4,
                    "avg_ratio": 1.0007539682539683,
                    "count": [721, 1008, 1009, 1008, 721],
                    "expected_count": [720, 1008, 1008, 1008, 720],
                    "interval": 600,
                    "name": "AirTempAngF1Off",
                    "ratio": [1, 1, 1, 1, 1],
                    "total_count": 4467,
                    "undefined_interval": False,
                },
                "2": {
                    "avg_count": 893.4,
                    "avg_ratio": 1.0007539682539683,
                    "count": [721, 1008, 1009, 1008, 721],
                    "expected_count": [720, 1008, 1008, 1008, 720],
                    "interval": 600,
                    "name": "AirTempAngF2Off",
                    "ratio": [1, 1, 1, 1, 1],
                    "total_count": 4467,
                    "undefined_interval": False,
                },
            },
            "timestamps": [
                "2019-12-30T00:00:00+00:00",
                "2020-01-06T00:00:00+00:00",
                "2020-01-13T00:00:00+00:00",
                "2020-01-20T00:00:00+00:00",
                "2020-01-27T00:00:00+00:00",
            ],
        }
