import pytest
import requests
import requests_mock
import json
import urllib

from bemserver_api_client.request import BEMServerApiClientRequest
from bemserver_api_client.resources import (
    UserResources,
    IOResources,
    TimeseriesResources,
    TimeseriesDataResources,
    AnalysisResources,
    ST_CleanupByCampaignResources,
    ST_CleanupByTimeseriesResources,
)


@pytest.fixture(params=[{"status_code": 500}])
def mock_raw_response_internal_error(request):
    status_code = request.param.get("status_code", 500)

    resp = requests.Response()
    resp.status_code = status_code
    resp.headers["Content-Type"] = "application/json"

    resp_content = {
        "code": status_code,
        "status": "Not found",
        "errors": {},
    }
    resp._content = json.dumps(resp_content).encode("utf-8")

    return (
        resp,
        status_code,
    )


@pytest.fixture(params=[{"is_general": False, "is_json": True}])
def mock_raw_response_409(request):
    is_general = request.param.get("is_general", False)
    is_json = request.param.get("is_json", True)

    resp = requests.Response()
    resp.status_code = 409
    if is_json:
        resp.headers["Content-Type"] = "application/json"
        resp_content = {
            "code": 409,
            "errors": {},
            "status": "Conflict",
        }
        if not is_general:
            resp_content["errors"] = {
                "type": "unique_constraint",
                "fields": ["name"],
            }
        resp._content = json.dumps(resp_content).encode("utf-8")

    return (
        resp,
        is_general,
        is_json,
    )


@pytest.fixture(params=[{"is_general": False, "is_schema": False}])
def mock_raw_response_422(request):
    is_general = request.param.get("is_general", False)
    is_schema = request.param.get("is_schema", False)

    resp = requests.Response()
    resp.status_code = 422
    resp.headers["Content-Type"] = "application/json"

    resp_content = {
        "code": 422,
        "status": "Unprocessable Entity",
    }
    if is_general:
        resp_content["message"] = "Validation error message."
    elif is_schema:
        resp_content["errors"] = {
            "query": {
                "_schema": ["Schema error."],
            },
        }
    else:
        resp_content["errors"] = {
            "query": {
                "is_admin": ["Not a valid boolean."],
            },
        }
    resp._content = json.dumps(resp_content).encode("utf-8")

    return (
        resp,
        is_general,
        is_schema,
    )


@pytest.fixture(params=[{"host": "localhost:5050", "use_ssl": False}])
def mock_request(request):
    host = request.param.get("host", "localhost:5050")
    use_ssl = request.param.get("use_ssl", False)

    uri_prefix = "https+mock" if use_ssl else "http+mock"
    base_uri = f"{uri_prefix}://{host}"

    req = BEMServerApiClientRequest(base_uri, None)
    req._session = mock_session(uri_prefix, base_uri)

    yield req


def mock_session(uri_prefix, base_uri):
    adapter = requests_mock.Adapter()
    mock_fake_uris(adapter, base_uri)
    mock_users_uris(adapter, base_uri)
    mock_io_uris(adapter, base_uri)
    mock_timeseries_uris(adapter, base_uri)
    mock_analysis_uris(adapter, base_uri)
    mock_cleanup_uris(adapter, base_uri)

    session = requests.Session()
    session.mount(f"{uri_prefix}://", adapter)
    return session


def mock_fake_uris(mock_adapter, base_uri):
    fake_api_uri = "/fake/"

    # Get all
    #  - First time unauthorized (401),
    #  - Second time ok (200),
    #  - Third time not modified (304)
    mock_adapter.register_uri(
        "GET",
        f"{base_uri}{fake_api_uri}",
        [
            {
                "headers": {
                    "Content-Type": "application/json",
                },
                "status_code": 401,
            },
            {
                "headers": {
                    "Content-Type": "application/json",
                    "ETag": "etag_fake_list",
                },
                "json": [
                    {
                        "id": 0,
                        "name": "Fake #1",
                    },
                    {
                        "id": 1,
                        "name": "Fake #2",
                    },
                    {
                        "id": 2,
                        "name": "Fake #3",
                    },
                ],
            },
            {
                "headers": {
                    "Content-Type": "application/json",
                },
                "status_code": 304,
            },
        ],
    )

    # Get one
    #  - First time ok (200),
    #  - Second time not found (404)
    mock_adapter.register_uri(
        "GET",
        f"{base_uri}{fake_api_uri}0",
        [
            {
                "headers": {
                    "Content-Type": "application/json",
                    "ETag": "etag_fake_0",
                },
                "json": {
                    "id": 0,
                    "name": "Fake #1",
                },
            },
            {
                "headers": {
                    "Content-Type": "application/json",
                },
                "status_code": 404,
            },
        ],
    )

    # Create
    #  - First time validation error (422),
    #  - Second time conflict (409),
    #  - Third time ok (201)
    mock_adapter.register_uri(
        "POST",
        f"{base_uri}{fake_api_uri}",
        [
            {
                "headers": {
                    "Content-Type": "application/json",
                },
                "json": {
                    "code": 422,
                    "errors": {
                        "json": {"name": ["Missing data for required field."]},
                    },
                    "status": "Unprocessable Entity",
                },
                "status_code": 422,
            },
            {
                "headers": {
                    "Content-Type": "application/json",
                },
                "json": {
                    "code": 409,
                    "errors": {
                        "json": {"name": ["Must be unique."]},
                    },
                    "status": "Unprocessable Entity",
                },
                "status_code": 422,
            },
            {
                "headers": {
                    "Content-Type": "application/json",
                    "ETag": "etag_fake_3",
                },
                "json": {
                    "id": 3,
                    "name": "Fake #4",
                },
                "status_code": 201,
            },
        ],
    )

    # Update
    #  - First time missing etag (428)
    #  - Second time bad etag (412)
    #  - Third time ok (200)
    mock_adapter.register_uri(
        "PUT",
        f"{base_uri}{fake_api_uri}0",
        [
            {
                "headers": {
                    "Content-Type": "application/json",
                },
                "status_code": 428,
            },
            {
                "headers": {
                    "Content-Type": "application/json",
                },
                "status_code": 412,
            },
            {
                "headers": {
                    "Content-Type": "application/json",
                    "ETag": "etag_fake_0",
                },
                "json": {
                    "id": 0,
                    "name": "Fake #1 updated",
                },
            },
        ],
    )

    # Delete
    mock_adapter.register_uri(
        "DELETE",
        f"{base_uri}{fake_api_uri}0",
        headers={
            "Content-Type": "application/json",
        },
        json={},
        status_code=204,
    )

    # Forbidden access (403)
    mock_adapter.register_uri(
        "GET",
        f"{base_uri}{fake_api_uri}42",
        headers={
            "Content-Type": "application/json",
        },
        status_code=403,
    )

    # Internal bad request (400)
    mock_adapter.register_uri(
        "GET",
        f"{base_uri}{fake_api_uri}999",
        status_code=400,
    )

    # Internal server error (500)
    mock_adapter.register_uri(
        "GET",
        f"{base_uri}{fake_api_uri}666",
        status_code=500,
    )

    # Not JSON response
    mock_adapter.register_uri(
        "GET",
        f"{base_uri}{fake_api_uri}notjson",
        text="Hello!",
    )

    # Request exception (ConnectionTimeout)
    mock_adapter.register_uri(
        "GET",
        f"{base_uri}{fake_api_uri}timeout",
        exc=requests.exceptions.ConnectTimeout,
    )


def mock_users_uris(mock_adapter, base_uri):
    # Set admin
    mock_adapter.register_uri(
        "PUT",
        f"{base_uri}{UserResources.endpoint_base_uri}0/set_admin",
        headers={
            "Content-Type": "application/json",
            "ETag": "etag_user_0",
        },
        status_code=204,
    )

    # Set active
    mock_adapter.register_uri(
        "PUT",
        f"{base_uri}{UserResources.endpoint_base_uri}0/set_active",
        headers={
            "Content-Type": "application/json",
            "ETag": "etag_user_0",
        },
        status_code=204,
    )


def mock_io_uris(mock_adapter, base_uri):
    # Upload timeseries CSV
    mock_adapter.register_uri(
        "POST",
        f"{base_uri}{IOResources.endpoint_base_uri}timeseries?campaign_id=0",
        status_code=201,
    )

    # Upload structural elements CSV
    mock_adapter.register_uri(
        "POST",
        f"{base_uri}{IOResources.endpoint_base_uri}sites?campaign_id=0",
        status_code=201,
    )


def mock_timeseries_uris(mock_adapter, base_uri):
    # Get paginated timeseries list
    mock_adapter.register_uri(
        "GET",
        f"{base_uri}{TimeseriesResources.endpoint_base_uri}?page_size=5",
        headers={
            "Content-Type": "application/json",
            "ETag": "482a37693019e59f16f1d0c36bdbd0a4f8f4fff3",
            "X-Pagination": json.dumps(
                {
                    "total": 11,
                    "total_pages": 3,
                    "first_page": 1,
                    "last_page": 3,
                    "page": 1,
                    "next_page": 2,
                },
            ),
        },
        json=[
            {
                "campaign_id": 3,
                "campaign_scope_id": 10,
                "description": "Air temperature in Anglet Floor 1 offices",
                "id": 1,
                "name": "AirTempAngF1Off",
                "unit_symbol": "°C",
            },
            {
                "campaign_id": 3,
                "campaign_scope_id": 10,
                "description": "Air temperature in Anglet Floor 2 offices",
                "id": 2,
                "name": "AirTempAngF2Off",
                "unit_symbol": "°C",
            },
            {
                "campaign_id": 3,
                "campaign_scope_id": 10,
                "description": "Air temperature in Bordeaux Floor 1 offices",
                "id": 3,
                "name": "AirTempBdxF1Off",
                "unit_symbol": "°C",
            },
            {
                "campaign_id": 3,
                "campaign_scope_id": 11,
                "description": "Electric power consumption of Anglet building",
                "id": 4,
                "name": "ElecPowerAng",
                "unit_symbol": "W",
            },
            {
                "campaign_id": 3,
                "campaign_scope_id": 11,
                "description": "Electric power consumption of Bordeaux building",
                "id": 5,
                "name": "ElecPowerBdx",
                "unit_symbol": "W",
            },
        ],
    )

    endpoint_uri = f"{base_uri}{TimeseriesDataResources.endpoint_base_uri}"

    # Upload timeseries data CSV (by ids)
    mock_adapter.register_uri(
        "POST",
        f"{endpoint_uri}?data_state=1",
        status_code=201,
    )

    # Upload timeseries data CSV (by names)
    mock_adapter.register_uri(
        "POST",
        f"{endpoint_uri}campaign/0/?data_state=1",
        status_code=201,
    )

    # Download timeseries data CSV (by ids)
    data_csv = (
        "2020-01-01T00:00:00+00:00,0.1,1.1,2.1\n"
        "2020-01-01T00:10:00+00:00,0.2,1.2,2.2\n"
        "2020-01-01T00:20:00+00:00,0.3,1.3,2.3\n"
    )
    data_csv_header_ids = "Datetime,0,1,2\n"
    q_params = {
        "start_time": "2020-01-01T00:00:00+00:00",
        "end_time": "2020-01-01T00:30:00+00:00",
        "data_state": 1,
        "timeseries": [0, 1, 2],
    }
    mock_adapter.register_uri(
        "GET",
        f"{endpoint_uri}?{urllib.parse.urlencode(q_params, True)}",
        headers={
            "Content-Type": "text/csv; charset=utf-8",
            "Content-Disposition": "attachment; filename=timeseries.csv",
        },
        content=(data_csv_header_ids + data_csv).encode(),
    )

    # Download timeseries data CSV (by names)
    data_csv_header_names = "Datetime,Timeseries 1,Timeseries 2,Timeseries 3\n"
    endpoint_uri_camp = f"{endpoint_uri}campaign/0/"
    q_params["timeseries"] = ["Timeseries 1", "Timeseries 2", "Timeseries 3"]
    mock_adapter.register_uri(
        "GET",
        f"{endpoint_uri_camp}?{urllib.parse.urlencode(q_params, True)}",
        headers={
            "Content-Type": "text/csv; charset=utf-8",
            "Content-Disposition": "attachment; filename=timeseries.csv",
        },
        content=(data_csv_header_names + data_csv).encode(),
    )

    # Download aggregated timeseries data CSV (by ids)
    data_csv_agg = "2020-01-01T00:00:00+00:00,0.6,3.6,6.6\n"
    q_params = {
        "start_time": "2020-01-01T00:00:00+00:00",
        "end_time": "2020-01-01T00:30:00+00:00",
        "data_state": 1,
        "timeseries": [0, 1, 2],
        "aggregation": "sum",
    }
    mock_adapter.register_uri(
        "GET",
        f"{endpoint_uri}aggregate?{urllib.parse.urlencode(q_params, True)}",
        headers={
            "Content-Type": "text/csv; charset=utf-8",
            "Content-Disposition": "attachment; filename=timeseries.csv",
        },
        content=(data_csv_header_ids + data_csv_agg).encode(),
    )

    # Download aggregated timeseries data CSV (by names)
    q_params["timeseries"] = ["Timeseries 1", "Timeseries 2", "Timeseries 3"]
    mock_adapter.register_uri(
        "GET",
        f"{endpoint_uri_camp}aggregate?{urllib.parse.urlencode(q_params, True)}",
        headers={
            "Content-Type": "text/csv; charset=utf-8",
            "Content-Disposition": "attachment; filename=timeseries.csv",
        },
        content=(data_csv_header_names + data_csv_agg).encode(),
    )

    # Delete timeseries data (by ids)
    q_params = {
        "start_time": "2020-01-01T00:00:00+00:00",
        "end_time": "2020-01-01T00:30:00+00:00",
        "data_state": 1,
        "timeseries": [0, 1, 2],
    }
    mock_adapter.register_uri(
        "DELETE",
        f"{endpoint_uri}?{urllib.parse.urlencode(q_params, True)}",
        headers={
            "Content-Type": "application/json",
        },
        json={},
        status_code=204,
    )

    # Delete timeseries data (by names)
    q_params = {
        "start_time": "2020-01-01T00:00:00+00:00",
        "end_time": "2020-01-01T00:30:00+00:00",
        "data_state": 1,
        "timeseries": ["Timeseries 1", "Timeseries 2", "Timeseries 3"],
    }
    mock_adapter.register_uri(
        "DELETE",
        f"{endpoint_uri_camp}?{urllib.parse.urlencode(q_params, True)}",
        headers={
            "Content-Type": "application/json",
        },
        json={},
        status_code=204,
    )


def mock_analysis_uris(mock_adapter, base_uri):
    # Get completeness
    q_params = {
        "start_time": "2020-01-01T00:00:00+00:00",
        "end_time": "2020-02-01T00:00:00+00:00",
        "timeseries": [1, 2],
        "data_state": 1,
        "bucket_width_value": 1,
        "bucket_width_unit": "week",
        "timezone": "UTC",
    }
    endpoint_uri = f"{base_uri}{AnalysisResources.endpoint_base_uri}completeness"
    mock_adapter.register_uri(
        "GET",
        f"{endpoint_uri}?{urllib.parse.urlencode(q_params, True)}",
        headers={
            "Content-Type": "application/json",
            "ETag": "etag_analysis_completeness",
        },
        json={
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
        },
    )


def mock_cleanup_uris(mock_adapter, base_uri):
    # Get cleanup state for all campaigns
    mock_adapter.register_uri(
        "GET",
        f"{base_uri}{ST_CleanupByCampaignResources.endpoint_base_uri}full",
        headers={
            "Content-Type": "application/json",
            "ETag": "etag_cleanup_campaigns",
        },
        json=[
            {
                "campaign_id": 3,
                "campaign_name": "Nobatek offices EPC",
                "id": 1,
                "is_enabled": True,
            },
            {
                "campaign_id": 4,
                "campaign_name": "BET windows tests",
                "id": 2,
                "is_enabled": False,
            },
            {
                "campaign_id": 5,
                "campaign_name": "test",
                "id": 3,
                "is_enabled": False,
            },
        ],
    )

    # Get cleanup state for all timeseries
    mock_adapter.register_uri(
        "GET",
        f"{base_uri}{ST_CleanupByTimeseriesResources.endpoint_base_uri}full",
        headers={
            "Content-Type": "application/json",
            "ETag": "etag_cleanup_timeseries",
        },
        json=[
            {
                "id": 3,
                "last_timestamp": None,
                "timeseries_id": 1,
                "timeseries_name": "AirTempAngF1Off",
                "timeseries_unit_symbol": "°C",
            },
            {
                "id": 1,
                "last_timestamp": "2021-05-31T22:00:00+00:00",
                "timeseries_id": 2,
                "timeseries_name": "AirTempAngF2Off",
                "timeseries_unit_symbol": "°C",
            },
            {
                "id": None,
                "last_timestamp": None,
                "timeseries_id": 3,
                "timeseries_name": "AirTempBdxF1Off",
                "timeseries_unit_symbol": "°C",
            },
            {
                "id": 2,
                "last_timestamp": "2021-09-27T09:54:07+00:00",
                "timeseries_id": 4,
                "timeseries_name": "ElecPowerAng",
                "timeseries_unit_symbol": "W",
            },
            {
                "id": None,
                "last_timestamp": None,
                "timeseries_id": 5,
                "timeseries_name": "ElecPowerBdx",
                "timeseries_unit_symbol": "W",
            },
        ],
    )