"""BEMServer API client structural element resources tests"""
from bemserver_api_client.resources.base import BaseResources
from bemserver_api_client.resources import (
    StructuralElementPropertyResources,
    SiteResources,
    SitePropertyResources,
    SitePropertyDataResources,
    BuildingResources,
    BuildingPropertyResources,
    BuildingPropertyDataResources,
    StoreyResources,
    StoreyPropertyResources,
    StoreyPropertyDataResources,
    SpaceResources,
    SpacePropertyResources,
    SpacePropertyDataResources,
    ZoneResources,
    ZonePropertyResources,
    ZonePropertyDataResources,
)


class TestAPIClientResourcesStructuralElements:
    def test_api_client_resources_structural_elements(self):
        assert issubclass(SiteResources, BaseResources)
        assert SiteResources.endpoint_base_uri == "/sites/"
        assert SiteResources.disabled_endpoints == []

        assert issubclass(BuildingResources, BaseResources)
        assert BuildingResources.endpoint_base_uri == "/buildings/"
        assert BuildingResources.disabled_endpoints == []

        assert issubclass(StoreyResources, BaseResources)
        assert StoreyResources.endpoint_base_uri == "/storeys/"
        assert StoreyResources.disabled_endpoints == []

        assert issubclass(SpaceResources, BaseResources)
        assert SpaceResources.endpoint_base_uri == "/spaces/"
        assert SpaceResources.disabled_endpoints == []

        assert issubclass(ZoneResources, BaseResources)
        assert ZoneResources.endpoint_base_uri == "/zones/"
        assert ZoneResources.disabled_endpoints == []

        assert issubclass(StructuralElementPropertyResources, BaseResources)
        assert StructuralElementPropertyResources.endpoint_base_uri == (
            "/structural_element_properties/"
        )
        assert StructuralElementPropertyResources.disabled_endpoints == []

        assert issubclass(SitePropertyResources, BaseResources)
        assert SitePropertyResources.endpoint_base_uri == "/site_properties/"
        assert SitePropertyResources.disabled_endpoints == ["update"]

        assert issubclass(BuildingPropertyResources, BaseResources)
        assert BuildingPropertyResources.endpoint_base_uri == "/building_properties/"
        assert BuildingPropertyResources.disabled_endpoints == ["update"]

        assert issubclass(StoreyPropertyResources, BaseResources)
        assert StoreyPropertyResources.endpoint_base_uri == "/storey_properties/"
        assert StoreyPropertyResources.disabled_endpoints == ["update"]

        assert issubclass(SpacePropertyResources, BaseResources)
        assert SpacePropertyResources.endpoint_base_uri == "/space_properties/"
        assert SpacePropertyResources.disabled_endpoints == ["update"]

        assert issubclass(ZonePropertyResources, BaseResources)
        assert ZonePropertyResources.endpoint_base_uri == "/zone_properties/"
        assert ZonePropertyResources.disabled_endpoints == ["update"]

        assert issubclass(SitePropertyDataResources, BaseResources)
        assert SitePropertyDataResources.endpoint_base_uri == "/site_property_data/"
        assert SitePropertyDataResources.disabled_endpoints == []

        assert issubclass(BuildingPropertyDataResources, BaseResources)
        assert BuildingPropertyDataResources.endpoint_base_uri == (
            "/building_property_data/"
        )
        assert BuildingPropertyDataResources.disabled_endpoints == []

        assert issubclass(StoreyPropertyDataResources, BaseResources)
        assert StoreyPropertyDataResources.endpoint_base_uri == (
            "/storey_property_data/"
        )
        assert StoreyPropertyDataResources.disabled_endpoints == []

        assert issubclass(SpacePropertyDataResources, BaseResources)
        assert SpacePropertyDataResources.endpoint_base_uri == "/space_property_data/"
        assert SpacePropertyDataResources.disabled_endpoints == []

        assert issubclass(ZonePropertyDataResources, BaseResources)
        assert ZonePropertyDataResources.endpoint_base_uri == "/zone_property_data/"
        assert ZonePropertyDataResources.disabled_endpoints == []
