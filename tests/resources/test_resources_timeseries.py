"""BEMServer API client timeseries resources tests"""
from bemserver_api_client.resources.base import BaseResources
from bemserver_api_client.resources import (
    TimeseriesResources,
    TimeseriesDataStateResources,
    TimeseriesPropertyResources,
    TimeseriesPropertyDataResources,
    TimeseriesDataResources,
    TimeseriesBySiteResources,
    TimeseriesByBuildingResources,
    TimeseriesByStoreyResources,
    TimeseriesBySpaceResources,
    TimeseriesByZoneResources,
)
from bemserver_api_client.response import BEMServerApiClientResponse
from bemserver_api_client.enums import DataFormat, Aggregation


class TestAPIClientResourcesTimeseries:
    def test_api_client_resources_timeseries(self, mock_request):
        assert issubclass(TimeseriesResources, BaseResources)
        assert TimeseriesResources.endpoint_base_uri == "/timeseries/"
        assert TimeseriesResources.disabled_endpoints == []

        assert issubclass(TimeseriesDataStateResources, BaseResources)
        assert TimeseriesDataStateResources.endpoint_base_uri == (
            "/timeseries_data_states/"
        )
        assert TimeseriesDataStateResources.disabled_endpoints == []

        assert issubclass(TimeseriesPropertyResources, BaseResources)
        assert TimeseriesPropertyResources.endpoint_base_uri == (
            "/timeseries_properties/"
        )
        assert TimeseriesPropertyResources.disabled_endpoints == []

        assert issubclass(TimeseriesPropertyDataResources, BaseResources)
        assert TimeseriesPropertyDataResources.endpoint_base_uri == (
            "/timeseries_property_data/"
        )
        assert TimeseriesPropertyDataResources.disabled_endpoints == []

        assert issubclass(TimeseriesDataResources, BaseResources)
        assert TimeseriesDataResources.endpoint_base_uri == "/timeseries_data/"
        assert TimeseriesDataResources.disabled_endpoints == [
            "getall",
            "getone",
            "create",
            "update",
        ]
        assert hasattr(TimeseriesDataResources, "upload")
        assert hasattr(TimeseriesDataResources, "upload_by_names")
        assert hasattr(TimeseriesDataResources, "download")
        assert hasattr(TimeseriesDataResources, "download_by_names")
        assert hasattr(TimeseriesDataResources, "download_aggregate")
        assert hasattr(TimeseriesDataResources, "download_aggregate_by_names")
        assert hasattr(TimeseriesDataResources, "delete")
        assert hasattr(TimeseriesDataResources, "delete_by_names")
        res = TimeseriesDataResources(mock_request)
        assert res.endpoint_uri_by_campaign("42") == "/timeseries_data/campaign/42/"

        assert issubclass(TimeseriesBySiteResources, BaseResources)
        assert TimeseriesBySiteResources.endpoint_base_uri == "/timeseries_by_sites/"
        assert TimeseriesBySiteResources.disabled_endpoints == ["update"]

        assert issubclass(TimeseriesByBuildingResources, BaseResources)
        assert TimeseriesByBuildingResources.endpoint_base_uri == (
            "/timeseries_by_buildings/"
        )
        assert TimeseriesByBuildingResources.disabled_endpoints == ["update"]

        assert issubclass(TimeseriesByStoreyResources, BaseResources)
        assert TimeseriesByStoreyResources.endpoint_base_uri == (
            "/timeseries_by_storeys/"
        )
        assert TimeseriesByStoreyResources.disabled_endpoints == ["update"]

        assert issubclass(TimeseriesBySpaceResources, BaseResources)
        assert TimeseriesBySpaceResources.endpoint_base_uri == "/timeseries_by_spaces/"
        assert TimeseriesBySpaceResources.disabled_endpoints == ["update"]

        assert issubclass(TimeseriesByZoneResources, BaseResources)
        assert TimeseriesByZoneResources.endpoint_base_uri == "/timeseries_by_zones/"
        assert TimeseriesByZoneResources.disabled_endpoints == ["update"]

    def test_api_client_resources_timeseries_endpoints(self, mock_request):
        ts_res = TimeseriesResources(mock_request)

        resp = ts_res.getall(page_size=5)
        assert isinstance(resp, BEMServerApiClientResponse)
        assert resp.status_code == 200
        assert resp.is_json
        assert resp.pagination == {
            "total": 11,
            "total_pages": 3,
            "first_page": 1,
            "last_page": 3,
            "page": 1,
            "next_page": 2,
        }
        assert resp.etag == "482a37693019e59f16f1d0c36bdbd0a4f8f4fff3"
        assert len(resp.data) == 5

    def test_api_client_resources_timeseries_data_upload_csv(self, mock_request):
        tsdata_res = TimeseriesDataResources(mock_request)

        tsdata_csv = (
            "2020-01-01T00:00:00+00:00,0\n"
            "2020-01-01T01:00:00+00:00,1\n"
            "2020-01-01T02:00:00+00:00,2\n"
            "2020-01-01T03:00:00+00:00,3\n"
        )
        tsdata_csv_header_ids = "Datetime,0\n"
        resp = tsdata_res.upload(
            1,
            (tsdata_csv + tsdata_csv_header_ids).encode(),
            format=DataFormat.csv,
        )
        assert isinstance(resp, BEMServerApiClientResponse)
        assert resp.status_code == 201
        assert resp.is_json
        assert not resp.is_csv

        tsdata_csv_header_names = "Datetime,Timeseries 1\n"
        resp = tsdata_res.upload_by_names(
            0,
            1,
            (tsdata_csv + tsdata_csv_header_names).encode(),
            format=DataFormat.csv,
        )
        assert isinstance(resp, BEMServerApiClientResponse)
        assert resp.status_code == 201
        assert resp.is_json
        assert not resp.is_csv

    def test_api_client_resources_timeseries_data_upload_json(self, mock_request):
        tsdata_res = TimeseriesDataResources(mock_request)

        tsdata_json = {
            "0": {
                "2020-01-01T00:00:00+00:00": 0,
                "2020-01-01T01:00:00+00:00": 1,
                "2020-01-01T02:00:00+00:00": 2,
                "2020-01-01T03:00:00+00:00": 3,
            },
        }
        resp = tsdata_res.upload(1, tsdata_json)
        assert isinstance(resp, BEMServerApiClientResponse)
        assert resp.status_code == 201
        assert resp.is_json
        assert not resp.is_csv

        tsdata_json["Timeseries 1"] = tsdata_json["0"]
        del tsdata_json["0"]
        resp = tsdata_res.upload_by_names(0, 1, tsdata_json)
        assert isinstance(resp, BEMServerApiClientResponse)
        assert resp.status_code == 201
        assert resp.is_json
        assert not resp.is_csv

    def test_api_client_resources_timeseries_data_download_csv(self, mock_request):
        tsdata_res = TimeseriesDataResources(mock_request)

        resp = tsdata_res.download(
            "2020-01-01T00:00:00+00:00",
            "2020-01-01T00:30:00+00:00",
            1,
            [0, 1, 2],
            format=DataFormat.csv,
        )
        assert isinstance(resp, BEMServerApiClientResponse)
        assert resp.status_code == 200
        assert resp.is_csv
        assert not resp.is_json
        ret_csv_lines = resp.data.decode("utf-8").splitlines()
        assert ret_csv_lines[0] == "Datetime,0,1,2"
        assert ret_csv_lines[1] == "2020-01-01T00:00:00+00:00,0.1,1.1,2.1"

        resp = tsdata_res.download_by_names(
            0,
            "2020-01-01T00:00:00+00:00",
            "2020-01-01T00:30:00+00:00",
            1,
            ["Timeseries 1", "Timeseries 2", "Timeseries 3"],
            format=DataFormat.csv,
        )
        assert isinstance(resp, BEMServerApiClientResponse)
        assert resp.status_code == 200
        assert resp.is_csv
        assert not resp.is_json
        ret_csv_lines = resp.data.decode("utf-8").splitlines()
        assert ret_csv_lines[0] == "Datetime,Timeseries 1,Timeseries 2,Timeseries 3"
        assert ret_csv_lines[1] == "2020-01-01T00:00:00+00:00,0.1,1.1,2.1"

        resp = tsdata_res.download_aggregate(
            "2020-01-01T00:00:00+00:00",
            "2020-01-01T00:30:00+00:00",
            1,
            [0, 1, 2],
            aggregation=Aggregation.sum,
            format=DataFormat.csv,
        )
        assert isinstance(resp, BEMServerApiClientResponse)
        assert resp.status_code == 200
        assert resp.is_csv
        assert not resp.is_json
        ret_csv_lines = resp.data.decode("utf-8").splitlines()
        assert ret_csv_lines[0] == "Datetime,0,1,2"
        assert ret_csv_lines[1] == "2020-01-01T00:00:00+00:00,0.6,3.6,6.6"

        resp = tsdata_res.download_aggregate_by_names(
            0,
            "2020-01-01T00:00:00+00:00",
            "2020-01-01T00:30:00+00:00",
            1,
            ["Timeseries 1", "Timeseries 2", "Timeseries 3"],
            aggregation=Aggregation.sum,
            format=DataFormat.csv,
        )
        assert isinstance(resp, BEMServerApiClientResponse)
        assert resp.status_code == 200
        assert resp.is_csv
        assert not resp.is_json
        ret_csv_lines = resp.data.decode("utf-8").splitlines()
        assert ret_csv_lines[0] == "Datetime,Timeseries 1,Timeseries 2,Timeseries 3"
        assert ret_csv_lines[1] == "2020-01-01T00:00:00+00:00,0.6,3.6,6.6"

    def test_api_client_resources_timeseries_data_download_json(self, mock_request):
        tsdata_res = TimeseriesDataResources(mock_request)

        tsdata_json = {
            "0": {
                "2020-01-01T00:00:00+00:00": 0.1,
                "2020-01-01T00:10:00+00:00": 0.2,
                "2020-01-01T00:20:00+00:00": 0.3,
            },
            "1": {
                "2020-01-01T00:00:00+00:00": 1.1,
                "2020-01-01T00:10:00+00:00": 1.2,
                "2020-01-01T00:20:00+00:00": 1.3,
            },
            "2": {
                "2020-01-01T00:00:00+00:00": 2.1,
                "2020-01-01T00:10:00+00:00": 2.2,
                "2020-01-01T00:20:00+00:00": 2.3,
            },
        }
        resp = tsdata_res.download(
            "2020-01-01T00:00:00+00:00",
            "2020-01-01T00:30:00+00:00",
            1,
            [0, 1, 2],
        )
        assert isinstance(resp, BEMServerApiClientResponse)
        assert resp.status_code == 200

        assert resp.is_json
        assert not resp.is_csv
        assert len(resp.data.keys()) == len(tsdata_json.keys())
        for k, v in resp.data.items():
            assert k in tsdata_json
            assert v == tsdata_json[k]

        for i in range(len(tsdata_json.keys())):
            tsdata_json[f"Timeseries {i+1}"] = tsdata_json[str(i)]
            del tsdata_json[str(i)]
        resp = tsdata_res.download_by_names(
            0,
            "2020-01-01T00:00:00+00:00",
            "2020-01-01T00:30:00+00:00",
            1,
            ["Timeseries 1", "Timeseries 2", "Timeseries 3"],
        )
        assert isinstance(resp, BEMServerApiClientResponse)
        assert resp.status_code == 200
        assert resp.is_json
        assert not resp.is_csv
        assert len(resp.data.keys()) == len(tsdata_json.keys())
        for k, v in resp.data.items():
            assert k in tsdata_json
            assert v == tsdata_json[k]

        tsdata_json_agg = {
            "0": {
                "2020-01-01T00:00:00+00:00": 0.6,
            },
            "1": {
                "2020-01-01T00:00:00+00:00": 3.6,
            },
            "2": {
                "2020-01-01T00:00:00+00:00": 6.6,
            },
        }
        resp = tsdata_res.download_aggregate(
            "2020-01-01T00:00:00+00:00",
            "2020-01-01T00:30:00+00:00",
            1,
            [0, 1, 2],
            aggregation=Aggregation.sum,
        )
        assert isinstance(resp, BEMServerApiClientResponse)
        assert resp.status_code == 200
        assert resp.is_json
        assert not resp.is_csv
        assert len(resp.data.keys()) == len(tsdata_json_agg.keys())
        for k, v in resp.data.items():
            assert k in tsdata_json_agg
            assert v == tsdata_json_agg[k]

        for i in range(len(tsdata_json_agg.keys())):
            tsdata_json_agg[f"Timeseries {i+1}"] = tsdata_json_agg[str(i)]
            del tsdata_json_agg[str(i)]
        resp = tsdata_res.download_aggregate_by_names(
            0,
            "2020-01-01T00:00:00+00:00",
            "2020-01-01T00:30:00+00:00",
            1,
            ["Timeseries 1", "Timeseries 2", "Timeseries 3"],
            aggregation=Aggregation.sum,
        )
        assert isinstance(resp, BEMServerApiClientResponse)
        assert resp.status_code == 200
        assert resp.is_json
        assert not resp.is_csv
        assert len(resp.data.keys()) == len(tsdata_json_agg.keys())
        for k, v in resp.data.items():
            assert k in tsdata_json_agg
            assert v == tsdata_json_agg[k]

    def test_api_client_resources_timeseries_data_endpoints(self, mock_request):
        tsdata_res = TimeseriesDataResources(mock_request)

        resp = tsdata_res.delete(
            "2020-01-01T00:00:00+00:00",
            "2020-01-01T00:30:00+00:00",
            1,
            [0, 1, 2],
        )
        assert isinstance(resp, BEMServerApiClientResponse)
        assert resp.status_code == 204
        assert resp.is_json
        assert not resp.is_csv
        assert resp.pagination == {}
        assert resp.etag == ""
        assert resp.data == {}

        resp = tsdata_res.delete_by_names(
            0,
            "2020-01-01T00:00:00+00:00",
            "2020-01-01T00:30:00+00:00",
            1,
            ["Timeseries 1", "Timeseries 2", "Timeseries 3"],
        )
        assert isinstance(resp, BEMServerApiClientResponse)
        assert resp.status_code == 204
        assert resp.is_json
        assert not resp.is_csv
        assert resp.pagination == {}
        assert resp.etag == ""
        assert resp.data == {}
