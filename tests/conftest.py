import pytest
import requests
import requests_mock
import json
import urllib
import copy
import enum

from bemserver_api_client.client import REQUIRED_API_VERSION
from bemserver_api_client.request import BEMServerApiClientRequest
from bemserver_api_client.resources.users import UserResources
from bemserver_api_client.resources.io import IOResources
from bemserver_api_client.resources.timeseries import (
    TimeseriesResources,
    TimeseriesDataResources,
)
from bemserver_api_client.resources.analysis import AnalysisResources
from bemserver_api_client.resources.events import EventResources
from bemserver_api_client.resources.notifications import NotificationResources
from bemserver_api_client.resources.services import (
    ST_CleanupByCampaignResources,
    ST_CleanupByTimeseriesResources,
    ST_CheckMissingByCampaignResources,
    ST_CheckOutlierByCampaignResources,
    ST_DownloadWeatherDataBySiteResources,
)
from bemserver_api_client.resources.structural_elements import SiteResources
from bemserver_api_client.enums import (
    DataFormat,
    Aggregation,
    BucketWidthUnit,
    StructuralElement,
    DegreeDaysPeriod,
    DegreeDaysType,
)


class FakeEnum(enum.Enum):
    a = "a"
    b = "b"


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


@pytest.fixture(params=[{"is_json": True}])
def mock_raw_response_409(request):
    is_json = request.param.get("is_json", True)

    resp = requests.Response()
    resp.status_code = 409
    if is_json:
        resp.headers["Content-Type"] = "application/json"
        resp_content = {
            "code": 409,
            "errors": {},
            "status": "Conflict",
            "message": "Unique constraint violation",
        }
        resp._content = json.dumps(resp_content).encode("utf-8")

    return (
        resp,
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
    mock_about_uris(adapter, base_uri)
    mock_users_uris(adapter, base_uri)
    mock_io_uris(adapter, base_uri)
    mock_events_uris(adapter, base_uri)
    mock_notifications_uris(adapter, base_uri)
    mock_timeseries_uris(adapter, base_uri)
    mock_timeseries_data_uris(adapter, base_uri)
    mock_analysis_uris(adapter, base_uri)
    mock_cleanup_uris(adapter, base_uri)
    mock_check_missing_uris(adapter, base_uri)
    mock_check_outlier_uris(adapter, base_uri)
    mock_download_weather_uris(adapter, base_uri)
    mock_site_weather_data_uris(adapter, base_uri)

    session = requests.Session()
    session.mount(f"{uri_prefix}://", adapter)
    return session


def mock_about_uris(mock_adapter, base_uri):
    about_api_uri = "/about/"

    # Get all
    #  - First time: check version OK,
    #  - Second time: check version NOK,
    #  - Third time: invalid API version,
    mock_adapter.register_uri(
        "GET",
        f"{base_uri}{about_api_uri}",
        [
            {
                "headers": {
                    "Content-Type": "application/json",
                    "ETag": "etag_about",
                },
                "json": {
                    "versions": {
                        "bemserver_core": "0.0.1",
                        "bemserver_api": str(REQUIRED_API_VERSION["min"]),
                    },
                },
            },
            {
                "headers": {
                    "Content-Type": "application/json",
                    "ETag": "etag_about",
                },
                "json": {
                    "versions": {
                        "bemserver_core": "9999.0.0",
                        "bemserver_api": "9999.0.0",
                    },
                },
            },
            {
                "headers": {
                    "Content-Type": "application/json",
                    "ETag": "etag_about",
                },
                "json": {
                    "versions": {
                        "bemserver_core": "9999.0.0",
                        "bemserver_api": "invalid",
                    },
                },
            },
        ],
    )


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


def mock_events_uris(mock_adapter, base_uri):
    # Get paginated events list
    mock_adapter.register_uri(
        "GET",
        f"{base_uri}{EventResources.endpoint_base_uri}?page_size=5",
        headers={
            "Content-Type": "application/json",
            "ETag": "5e848c32d0338815a739fa470e2d518aba47a077",
            "X-Pagination": json.dumps(
                {
                    "total": 12,
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
                "campaign_scope_id": 3,
                "category_id": 3,
                "description": "",
                "id": 1,
                "level": "DEBUG",
                "source": "bemserver-ui",
                "timestamp": "2022-12-09T14:46:00+00:00",
            },
            {
                "campaign_scope_id": 1,
                "category_id": 1,
                "id": 2,
                "level": "ERROR",
                "source": "bemserver-ui",
                "timestamp": "2022-12-09T19:00:00+00:00",
            },
            {
                "campaign_scope_id": 4,
                "category_id": 4,
                "id": 3,
                "level": "WARNING",
                "source": "bemserver-ui",
                "timestamp": "2022-12-09T18:47:00+00:00",
            },
            {
                "campaign_scope_id": 2,
                "category_id": 1,
                "id": 5,
                "level": "CRITICAL",
                "source": "other source",
                "timestamp": "2022-12-09T19:01:00+00:00",
            },
            {
                "campaign_scope_id": 3,
                "category_id": 3,
                "id": 6,
                "level": "INFO",
                "source": "bemserver-ui",
                "timestamp": "2022-12-12T15:52:00+00:00",
            },
        ],
    )


def mock_notifications_uris(mock_adapter, base_uri):
    # GET count by campaign
    mock_adapter.register_uri(
        "GET",
        (
            f"{base_uri}{NotificationResources.endpoint_base_uri}"
            "count_by_campaign?user_id=42"
        ),
        headers={
            "Content-Type": "application/json",
            "ETag": "734ab7a416e0c0b1b1ded1a96cd53425f9bcd7f8",
        },
        json={
            "campaigns": [
                {
                    "campaign_id": 1,
                    "campaign_name": "Nobatek offices EPC",
                    "count": 1,
                }
            ],
            "total": 1,
        },
    )

    # PUT mark all as read
    mock_adapter.register_uri(
        "PUT",
        (
            f"{base_uri}{NotificationResources.endpoint_base_uri}"
            "mark_all_as_read?user_id=42"
        ),
        headers={
            "Content-Type": "application/json",
        },
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


def mock_timeseries_data_uris(mock_adapter, base_uri):
    endpoint_uri = f"{base_uri}{TimeseriesDataResources.endpoint_base_uri}"

    # Upload timeseries data CSV (by ids)
    mock_adapter.register_uri(
        "POST",
        f"{endpoint_uri}?data_state=1",
        request_headers={
            "Content-Type": DataFormat.csv.value,
        },
        headers={
            "Content-Type": "application/json",
        },
        status_code=201,
    )

    # Upload timeseries data CSV (by names)
    mock_adapter.register_uri(
        "POST",
        f"{endpoint_uri}campaign/0/?data_state=1",
        request_headers={
            "Content-Type": DataFormat.csv.value,
        },
        headers={
            "Content-Type": "application/json",
        },
        status_code=201,
    )

    # Upload timeseries data JSON (by ids)
    mock_adapter.register_uri(
        "POST",
        f"{endpoint_uri}?data_state=1",
        request_headers={
            "Content-Type": DataFormat.json.value,
        },
        headers={
            "Content-Type": "application/json",
        },
        status_code=201,
    )

    # Upload timeseries data JSON (by names)
    mock_adapter.register_uri(
        "POST",
        f"{endpoint_uri}campaign/0/?data_state=1",
        request_headers={
            "Content-Type": DataFormat.json.value,
        },
        headers={
            "Content-Type": "application/json",
        },
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
        request_headers={
            "Accept": DataFormat.csv.value,
        },
        headers={
            "Content-Type": DataFormat.csv.value,
        },
        content=(data_csv_header_ids + data_csv).encode(),
    )
    # Download timeseries data CSV (by ids), with convert_to
    data_csv_converted = (
        "2020-01-01T00:00:00+00:00,273.16,274.16,275.16\n"
        "2020-01-01T00:10:00+00:00,0.2,1.2,2.2\n"
        "2020-01-01T00:20:00+00:00,0.3,1.3,2.3\n"
    )
    q_params["convert_to"] = ["kelvin", "", ""]
    mock_adapter.register_uri(
        "GET",
        f"{endpoint_uri}?{urllib.parse.urlencode(q_params, True)}",
        request_headers={
            "Accept": DataFormat.csv.value,
        },
        headers={
            "Content-Type": DataFormat.csv.value,
        },
        content=(data_csv_header_ids + data_csv_converted).encode(),
    )

    # Download timeseries data CSV (by names)
    data_csv_header_names = "Datetime,Timeseries 1,Timeseries 2,Timeseries 3\n"
    endpoint_uri_camp = f"{endpoint_uri}campaign/0/"
    q_params["timeseries"] = ["Timeseries 1", "Timeseries 2", "Timeseries 3"]
    del q_params["convert_to"]
    mock_adapter.register_uri(
        "GET",
        f"{endpoint_uri_camp}?{urllib.parse.urlencode(q_params, True)}",
        request_headers={
            "Accept": DataFormat.csv.value,
        },
        headers={
            "Content-Type": DataFormat.csv.value,
        },
        content=(data_csv_header_names + data_csv).encode(),
    )
    # Download timeseries data CSV (by names), with convert_to
    data_csv_header_names = "Datetime,Timeseries 1,Timeseries 2,Timeseries 3\n"
    q_params["convert_to"] = ["kelvin", "", ""]
    mock_adapter.register_uri(
        "GET",
        f"{endpoint_uri_camp}?{urllib.parse.urlencode(q_params, True)}",
        request_headers={
            "Accept": DataFormat.csv.value,
        },
        headers={
            "Content-Type": DataFormat.csv.value,
        },
        content=(data_csv_header_names + data_csv_converted).encode(),
    )

    # Download timeseries data JSON (by ids)
    data_json = {
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
    q_params = {
        "start_time": "2020-01-01T00:00:00+00:00",
        "end_time": "2020-01-01T00:30:00+00:00",
        "data_state": 1,
        "timeseries": [0, 1, 2],
    }
    mock_adapter.register_uri(
        "GET",
        f"{endpoint_uri}?{urllib.parse.urlencode(q_params, True)}",
        request_headers={
            "Accept": DataFormat.json.value,
        },
        headers={
            "Content-Type": DataFormat.json.value,
        },
        json=data_json,
    )

    # Download timeseries data JSON (by names)
    data_json_names = copy.deepcopy(data_json)
    q_params["timeseries"] = []
    for i in range(len(data_json_names.keys())):
        data_json_names[f"Timeseries {i+1}"] = data_json_names[str(i)]
        del data_json_names[str(i)]
        q_params["timeseries"].append(f"Timeseries {i+1}")
    endpoint_uri_camp = f"{endpoint_uri}campaign/0/"
    mock_adapter.register_uri(
        "GET",
        f"{endpoint_uri_camp}?{urllib.parse.urlencode(q_params, True)}",
        request_headers={
            "Accept": DataFormat.json.value,
        },
        headers={
            "Content-Type": DataFormat.json.value,
        },
        json=data_json_names,
    )

    # Download aggregated timeseries data CSV (by ids)
    data_csv_agg = "2020-01-01T00:00:00+00:00,0.6,3.6,6.6\n"
    q_params = {
        "start_time": "2020-01-01T00:00:00+00:00",
        "end_time": "2020-01-01T00:30:00+00:00",
        "data_state": 1,
        "timeseries": [0, 1, 2],
        "aggregation": Aggregation.sum.value,
    }
    mock_adapter.register_uri(
        "GET",
        f"{endpoint_uri}aggregate?{urllib.parse.urlencode(q_params, True)}",
        request_headers={
            "Accept": DataFormat.csv.value,
        },
        headers={
            "Content-Type": DataFormat.csv.value,
        },
        content=(data_csv_header_ids + data_csv_agg).encode(),
    )

    # Download aggregated timeseries data CSV (by ids), with convert_to
    data_csv_agg_converted = "2020-01-01T00:00:00+00:00,820.05,823.45,826.45\n"
    q_params["convert_to"] = ["kelvin", "kelvin", "kelvin"]
    mock_adapter.register_uri(
        "GET",
        f"{endpoint_uri}aggregate?{urllib.parse.urlencode(q_params, True)}",
        request_headers={
            "Accept": DataFormat.csv.value,
        },
        headers={
            "Content-Type": DataFormat.csv.value,
        },
        content=(data_csv_header_ids + data_csv_agg_converted).encode(),
    )

    # Download aggregated timeseries data CSV (by names)
    del q_params["convert_to"]
    q_params["timeseries"] = ["Timeseries 1", "Timeseries 2", "Timeseries 3"]
    mock_adapter.register_uri(
        "GET",
        f"{endpoint_uri_camp}aggregate?{urllib.parse.urlencode(q_params, True)}",
        request_headers={
            "Accept": DataFormat.csv.value,
        },
        headers={
            "Content-Type": DataFormat.csv.value,
        },
        content=(data_csv_header_names + data_csv_agg).encode(),
    )

    # Download aggregated timeseries data CSV (by names), with convert_to
    q_params["convert_to"] = ["kelvin", "kelvin", "kelvin"]
    mock_adapter.register_uri(
        "GET",
        f"{endpoint_uri_camp}aggregate?{urllib.parse.urlencode(q_params, True)}",
        request_headers={
            "Accept": DataFormat.csv.value,
        },
        headers={
            "Content-Type": DataFormat.csv.value,
        },
        content=(data_csv_header_names + data_csv_agg_converted).encode(),
    )

    # Download aggregated timeseries data JSON (by ids)
    data_json_agg = {
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
    q_params = {
        "start_time": "2020-01-01T00:00:00+00:00",
        "end_time": "2020-01-01T00:30:00+00:00",
        "data_state": 1,
        "timeseries": [0, 1, 2],
        "aggregation": Aggregation.sum.value,
    }
    mock_adapter.register_uri(
        "GET",
        f"{endpoint_uri}aggregate?{urllib.parse.urlencode(q_params, True)}",
        request_headers={
            "Accept": DataFormat.json.value,
        },
        headers={
            "Content-Type": "application/json",
        },
        json=data_json_agg,
    )

    # Download aggregated timeseries data JSON (by names)
    data_json_agg_names = copy.deepcopy(data_json_agg)
    q_params["timeseries"] = []
    for i in range(len(data_json_agg_names.keys())):
        data_json_agg_names[f"Timeseries {i+1}"] = data_json_agg_names[str(i)]
        del data_json_agg_names[str(i)]
        q_params["timeseries"].append(f"Timeseries {i+1}")
    mock_adapter.register_uri(
        "GET",
        f"{endpoint_uri_camp}aggregate?{urllib.parse.urlencode(q_params, True)}",
        request_headers={
            "Accept": DataFormat.json.value,
        },
        headers={
            "Content-Type": "application/json",
        },
        json=data_json_agg_names,
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
        "bucket_width_unit": BucketWidthUnit.week.value,
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

    # Get energy consumption breakdown for site
    q_params = {
        "start_time": "2020-01-01T00:00:00+00:00",
        "end_time": "2020-02-01T00:00:00+00:00",
        "bucket_width_value": 1,
        "bucket_width_unit": BucketWidthUnit.week.value,
        "timezone": "UTC",
    }
    endpoint_uri = (
        f"{base_uri}{AnalysisResources.endpoint_base_uri}"
        f"energy_consumption/{StructuralElement.site.value}/1"
    )
    mock_adapter.register_uri(
        "GET",
        f"{endpoint_uri}?{urllib.parse.urlencode(q_params, True)}",
        headers={
            "Content-Type": "application/json",
            "ETag": "etag_analysis_energy_cons_site",
        },
        json={
            "energy": {
                "all": {
                    "all": [0, 0, 0, 0, 0],
                    "appliances": [0, 0, 0, 0, 0],
                    "lighting": [0, 0, 0, 0, 0],
                    "ventilation": [0, 0, 0, 0, 0],
                },
                "electricity": {
                    "all": [0, 0, 0, 0, 0],
                    "heating": [0, 0, 0, 0, 0],
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


def mock_check_missing_uris(mock_adapter, base_uri):
    # Get check missing state for all campaigns
    mock_adapter.register_uri(
        "GET",
        f"{base_uri}{ST_CheckMissingByCampaignResources.endpoint_base_uri}full",
        headers={
            "Content-Type": "application/json",
            "ETag": "etag_check_missing_campaigns",
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


def mock_check_outlier_uris(mock_adapter, base_uri):
    # Get check outlier service state for all campaigns
    mock_adapter.register_uri(
        "GET",
        f"{base_uri}{ST_CheckOutlierByCampaignResources.endpoint_base_uri}full",
        headers={
            "Content-Type": "application/json",
            "ETag": "etag_check_outlier_campaigns",
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


def mock_download_weather_uris(mock_adapter, base_uri):
    # Get download weather data service state for all sites
    mock_adapter.register_uri(
        "GET",
        f"{base_uri}{ST_DownloadWeatherDataBySiteResources.endpoint_base_uri}full",
        headers={
            "Content-Type": "application/json",
            "ETag": "etag_download_weather_data_sites",
        },
        json=[
            {
                "id": 1,
                "is_enabled": True,
                "site_id": 1,
                "site_name": "Anglet",
            },
            {
                "id": 2,
                "is_enabled": False,
                "site_id": 2,
                "site_name": "Bordeaux",
            },
            {
                "id": None,
                "is_enabled": False,
                "site_id": 3,
                "site_name": "Talence",
            },
        ],
    )


def mock_site_weather_data_uris(mock_adapter, base_uri):
    endpoint_uri = f"{base_uri}{SiteResources.endpoint_base_uri}1"

    # Download weather data from external weather service.
    q_params = {
        "start_time": "2020-01-01T00:00:00+00:00",
        "end_time": "2020-01-01T00:30:00+00:00",
    }
    mock_adapter.register_uri(
        "PUT",
        (
            f"{endpoint_uri}/download_weather_data"
            f"?{urllib.parse.urlencode(q_params, True)}"
        ),
        headers={
            "Content-Type": "application/json",
        },
        json={},
        status_code=204,
    )

    # Get degree days.
    data_json = {
        "degree_days": {
            "2020-01-01T00:00:00+00:00": 7.1,
            "2020-01-02T00:00:00+00:00": 7.2,
            "2020-01-03T00:00:00+00:00": 7.3,
            "2020-01-04T00:00:00+00:00": 7.4,
        }
    }
    q_params = {
        "start_date": "2020-01-01",
        "end_date": "2020-01-05",
    }
    mock_adapter.register_uri(
        "GET",
        f"{endpoint_uri}/degree_days?{urllib.parse.urlencode(q_params, True)}",
        headers={
            "Content-Type": "application/json",
        },
        json=data_json,
    )

    data_json = {
        "degree_days": {
            "2020-07-01T00:00:00+00:00": 297.4,
        }
    }
    q_params = {
        "start_date": "2020-07-01",
        "end_date": "2020-08-01",
        "period": DegreeDaysPeriod.month.value,
        "type": DegreeDaysType.cooling.value,
        "base": 24,
    }
    mock_adapter.register_uri(
        "GET",
        f"{endpoint_uri}/degree_days?{urllib.parse.urlencode(q_params, True)}",
        headers={
            "Content-Type": "application/json",
        },
        json=data_json,
    )
