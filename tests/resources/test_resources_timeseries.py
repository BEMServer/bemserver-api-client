"""BEMServer API client timeseries resources tests"""
import io

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
            "delete",
        ]
        assert hasattr(TimeseriesDataResources, "upload_csv")
        assert hasattr(TimeseriesDataResources, "upload_csv_by_names")
        assert hasattr(TimeseriesDataResources, "download_csv")
        assert hasattr(TimeseriesDataResources, "download_csv_by_names")
        assert hasattr(TimeseriesDataResources, "download_csv_aggregate")
        assert hasattr(TimeseriesDataResources, "download_csv_aggregate_by_names")
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

        tsdata_res = TimeseriesDataResources(mock_request)

        tsdata_csv = (
            "2020-01-01T00:00:00+00:00,0\n"
            "2020-01-01T01:00:00+00:00,1\n"
            "2020-01-01T02:00:00+00:00,2\n"
            "2020-01-01T03:00:00+00:00,3\n"
        )
        tsdata_csv_header_ids = "Datetime,0\n"
        resp = tsdata_res.upload_csv(
            1,
            {
                "csv_file": io.BytesIO((tsdata_csv + tsdata_csv_header_ids).encode()),
            },
        )
        assert isinstance(resp, BEMServerApiClientResponse)
        assert resp.status_code == 201

        tsdata_csv_header_names = "Datetime,Timeseries 1\n"
        resp = tsdata_res.upload_csv_by_names(
            0,
            1,
            {
                "csv_file": io.BytesIO((tsdata_csv + tsdata_csv_header_names).encode()),
            },
        )
        assert isinstance(resp, BEMServerApiClientResponse)
        assert resp.status_code == 201

        resp = tsdata_res.download_csv(
            "2020-01-01T00:00:00+00:00",
            "2020-01-01T00:30:00+00:00",
            1,
            [0, 1, 2],
        )
        assert isinstance(resp, BEMServerApiClientResponse)
        assert resp.status_code == 200
        assert not resp.is_json
        ret_csv_lines = resp.data.decode("utf-8").splitlines()
        assert ret_csv_lines[0] == "Datetime,0,1,2"
        assert ret_csv_lines[1] == "2020-01-01T00:00:00+00:00,0.1,1.1,2.1"

        file = resp.get_data_as_file()
        assert file[0] == "timeseries.csv"
        assert file[1].read() == resp.data

        resp = tsdata_res.download_csv_by_names(
            0,
            "2020-01-01T00:00:00+00:00",
            "2020-01-01T00:30:00+00:00",
            1,
            ["Timeseries 1", "Timeseries 2", "Timeseries 3"],
        )
        assert isinstance(resp, BEMServerApiClientResponse)
        assert resp.status_code == 200
        assert not resp.is_json
        ret_csv_lines = resp.data.decode("utf-8").splitlines()
        assert ret_csv_lines[0] == "Datetime,Timeseries 1,Timeseries 2,Timeseries 3"
        assert ret_csv_lines[1] == "2020-01-01T00:00:00+00:00,0.1,1.1,2.1"

        resp = tsdata_res.download_csv_aggregate(
            "2020-01-01T00:00:00+00:00",
            "2020-01-01T00:30:00+00:00",
            1,
            [0, 1, 2],
            aggregation="sum",
        )
        assert isinstance(resp, BEMServerApiClientResponse)
        assert resp.status_code == 200
        assert not resp.is_json
        ret_csv_lines = resp.data.decode("utf-8").splitlines()
        assert ret_csv_lines[0] == "Datetime,0,1,2"
        assert ret_csv_lines[1] == "2020-01-01T00:00:00+00:00,0.6,3.6,6.6"

        resp = tsdata_res.download_csv_aggregate_by_names(
            0,
            "2020-01-01T00:00:00+00:00",
            "2020-01-01T00:30:00+00:00",
            1,
            ["Timeseries 1", "Timeseries 2", "Timeseries 3"],
            aggregation="sum",
        )
        assert isinstance(resp, BEMServerApiClientResponse)
        assert resp.status_code == 200
        assert not resp.is_json
        ret_csv_lines = resp.data.decode("utf-8").splitlines()
        assert ret_csv_lines[0] == "Datetime,Timeseries 1,Timeseries 2,Timeseries 3"
        assert ret_csv_lines[1] == "2020-01-01T00:00:00+00:00,0.6,3.6,6.6"

        resp = tsdata_res.delete(
            "2020-01-01T00:00:00+00:00",
            "2020-01-01T00:30:00+00:00",
            1,
            [0, 1, 2],
        )
        assert isinstance(resp, BEMServerApiClientResponse)
        assert resp.status_code == 204
        assert resp.is_json
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
        assert resp.pagination == {}
        assert resp.etag == ""
        assert resp.data == {}
