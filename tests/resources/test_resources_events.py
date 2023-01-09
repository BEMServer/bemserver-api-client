"""BEMServer API client events resources tests"""
from bemserver_api_client.resources.base import BaseResources
from bemserver_api_client.resources import (
    EventResources,
    EventCategoryResources,
    EventCategoryByUserResources,
    EventBySiteResources,
    EventByBuildingResources,
    EventByStoreyResources,
    EventBySpaceResources,
    EventByZoneResources,
)
from bemserver_api_client.response import BEMServerApiClientResponse


class TestAPIClientResourcesEvents:
    def test_api_client_resources_events(self, mock_request):
        assert issubclass(EventResources, BaseResources)
        assert EventResources.endpoint_base_uri == "/events/"
        assert EventResources.disabled_endpoints == []
        assert hasattr(EventResources, "getall_by_site")
        assert hasattr(EventResources, "getall_by_building")
        assert hasattr(EventResources, "getall_by_storey")
        assert hasattr(EventResources, "getall_by_space")
        assert hasattr(EventResources, "getall_by_zone")
        res = EventResources(mock_request)
        assert res.endpoint_uri_getall_by("whatever", 42) == "/events/by_whatever/42"

        assert issubclass(EventCategoryResources, BaseResources)
        assert EventCategoryResources.endpoint_base_uri == "/event_categories/"
        assert EventCategoryResources.disabled_endpoints == []

        assert issubclass(EventCategoryByUserResources, BaseResources)
        assert EventCategoryByUserResources.endpoint_base_uri == (
            "/event_categories_by_users/"
        )
        assert EventCategoryByUserResources.disabled_endpoints == []

        assert issubclass(EventBySiteResources, BaseResources)
        assert EventBySiteResources.endpoint_base_uri == "/events_by_sites/"
        assert EventBySiteResources.disabled_endpoints == ["update"]

        assert issubclass(EventByBuildingResources, BaseResources)
        assert EventByBuildingResources.endpoint_base_uri == "/events_by_buildings/"
        assert EventByBuildingResources.disabled_endpoints == ["update"]

        assert issubclass(EventByStoreyResources, BaseResources)
        assert EventByStoreyResources.endpoint_base_uri == "/events_by_storeys/"
        assert EventByStoreyResources.disabled_endpoints == ["update"]

        assert issubclass(EventBySpaceResources, BaseResources)
        assert EventBySpaceResources.endpoint_base_uri == "/events_by_spaces/"
        assert EventBySpaceResources.disabled_endpoints == ["update"]

        assert issubclass(EventByZoneResources, BaseResources)
        assert EventByZoneResources.endpoint_base_uri == "/events_by_zones/"
        assert EventByZoneResources.disabled_endpoints == ["update"]

    def test_api_client_resources_events_endpoints(self, mock_request):
        event_res = EventResources(mock_request)

        resp = event_res.getall(page_size=5)
        assert isinstance(resp, BEMServerApiClientResponse)
        assert resp.status_code == 200
        assert resp.is_json
        assert resp.pagination == {
            "total": 12,
            "total_pages": 3,
            "first_page": 1,
            "last_page": 3,
            "page": 1,
            "next_page": 2,
        }
        assert resp.etag == "5e848c32d0338815a739fa470e2d518aba47a077"
        assert len(resp.data) == 5

    def test_api_client_resources_events_getall_by(self, mock_request):
        event_res = EventResources(mock_request)

        resp = event_res.getall_by_site(1)
        assert isinstance(resp, BEMServerApiClientResponse)
        assert resp.status_code == 200
        assert resp.is_json
        assert resp.pagination == {
            "total": 1,
            "total_pages": 1,
            "first_page": 1,
            "last_page": 1,
            "page": 1,
        }
        assert resp.etag == "355357a06f8251097b114b6627bcc97a229c948b"
        assert len(resp.data) == 1

        resp = event_res.getall_by_site(1, recurse=False)
        assert isinstance(resp, BEMServerApiClientResponse)
        assert resp.status_code == 200
        assert resp.is_json
        assert resp.pagination == {
            "total": 1,
            "total_pages": 1,
            "first_page": 1,
            "last_page": 1,
            "page": 1,
        }
        assert resp.etag == "355357a06f8251097b114b6627bcc97a229c948b"
        assert len(resp.data) == 1

        resp = event_res.getall_by_site(1, recurse=True)
        assert isinstance(resp, BEMServerApiClientResponse)
        assert resp.status_code == 200
        assert resp.is_json
        assert resp.pagination == {
            "total": 2,
            "total_pages": 1,
            "first_page": 1,
            "last_page": 1,
            "page": 1,
        }
        assert resp.etag == "7cf1cc641ff08204a4a570cc15dcda2325590181"
        assert len(resp.data) == 2

        resp = event_res.getall_by_building(1)
        assert isinstance(resp, BEMServerApiClientResponse)
        assert resp.status_code == 200
        assert resp.is_json
        assert resp.pagination == {
            "total": 1,
            "total_pages": 1,
            "first_page": 1,
            "last_page": 1,
            "page": 1,
        }
        assert resp.etag == "6b87edffd8984b43b687c3e7b4fda04ae12c390e"
        assert len(resp.data) == 1

        for struct_elmt in ["storey", "space", "zone"]:
            resp = getattr(event_res, f"getall_by_{struct_elmt}")(1)
            assert isinstance(resp, BEMServerApiClientResponse)
            assert resp.status_code == 200
            assert resp.is_json
            assert resp.pagination == {
                "total": 0,
                "total_pages": 0,
            }
            assert resp.etag == "1f2784cf3037459bf0bf4c44d7856a43e001a55a"
            assert len(resp.data) == 0
