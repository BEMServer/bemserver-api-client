"""BEMServer API client structural element resources tests"""
from bemserver_api_client.resources.base import BaseResources
from bemserver_api_client.resources.structural_elements import (
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
        assert SiteResources.client_entrypoint == "sites"

        assert issubclass(BuildingResources, BaseResources)
        assert BuildingResources.endpoint_base_uri == "/buildings/"
        assert BuildingResources.disabled_endpoints == []
        assert BuildingResources.client_entrypoint == "buildings"

        assert issubclass(StoreyResources, BaseResources)
        assert StoreyResources.endpoint_base_uri == "/storeys/"
        assert StoreyResources.disabled_endpoints == []
        assert StoreyResources.client_entrypoint == "storeys"

        assert issubclass(SpaceResources, BaseResources)
        assert SpaceResources.endpoint_base_uri == "/spaces/"
        assert SpaceResources.disabled_endpoints == []
        assert SpaceResources.client_entrypoint == "spaces"

        assert issubclass(ZoneResources, BaseResources)
        assert ZoneResources.endpoint_base_uri == "/zones/"
        assert ZoneResources.disabled_endpoints == []
        assert ZoneResources.client_entrypoint == "zones"

        assert issubclass(StructuralElementPropertyResources, BaseResources)
        assert StructuralElementPropertyResources.endpoint_base_uri == (
            "/structural_element_properties/"
        )
        assert StructuralElementPropertyResources.disabled_endpoints == []
        assert StructuralElementPropertyResources.client_entrypoint == (
            "structural_element_properties"
        )

        assert issubclass(SitePropertyResources, BaseResources)
        assert SitePropertyResources.endpoint_base_uri == "/site_properties/"
        assert SitePropertyResources.disabled_endpoints == ["update"]
        assert SitePropertyResources.client_entrypoint == "site_properties"

        assert issubclass(BuildingPropertyResources, BaseResources)
        assert BuildingPropertyResources.endpoint_base_uri == "/building_properties/"
        assert BuildingPropertyResources.disabled_endpoints == ["update"]
        assert BuildingPropertyResources.client_entrypoint == "building_properties"

        assert issubclass(StoreyPropertyResources, BaseResources)
        assert StoreyPropertyResources.endpoint_base_uri == "/storey_properties/"
        assert StoreyPropertyResources.disabled_endpoints == ["update"]
        assert StoreyPropertyResources.client_entrypoint == "storey_properties"

        assert issubclass(SpacePropertyResources, BaseResources)
        assert SpacePropertyResources.endpoint_base_uri == "/space_properties/"
        assert SpacePropertyResources.disabled_endpoints == ["update"]
        assert SpacePropertyResources.client_entrypoint == "space_properties"

        assert issubclass(ZonePropertyResources, BaseResources)
        assert ZonePropertyResources.endpoint_base_uri == "/zone_properties/"
        assert ZonePropertyResources.disabled_endpoints == ["update"]
        assert ZonePropertyResources.client_entrypoint == "zone_properties"

        assert issubclass(SitePropertyDataResources, BaseResources)
        assert SitePropertyDataResources.endpoint_base_uri == "/site_property_data/"
        assert SitePropertyDataResources.disabled_endpoints == []
        assert SitePropertyDataResources.client_entrypoint == "site_property_data"

        assert issubclass(BuildingPropertyDataResources, BaseResources)
        assert BuildingPropertyDataResources.endpoint_base_uri == (
            "/building_property_data/"
        )
        assert BuildingPropertyDataResources.disabled_endpoints == []
        assert BuildingPropertyDataResources.client_entrypoint == (
            "building_property_data"
        )

        assert issubclass(StoreyPropertyDataResources, BaseResources)
        assert StoreyPropertyDataResources.endpoint_base_uri == (
            "/storey_property_data/"
        )
        assert StoreyPropertyDataResources.disabled_endpoints == []
        assert StoreyPropertyDataResources.client_entrypoint == "storey_property_data"

        assert issubclass(SpacePropertyDataResources, BaseResources)
        assert SpacePropertyDataResources.endpoint_base_uri == "/space_property_data/"
        assert SpacePropertyDataResources.disabled_endpoints == []
        assert SpacePropertyDataResources.client_entrypoint == "space_property_data"

        assert issubclass(ZonePropertyDataResources, BaseResources)
        assert ZonePropertyDataResources.endpoint_base_uri == "/zone_property_data/"
        assert ZonePropertyDataResources.disabled_endpoints == []
        assert ZonePropertyDataResources.client_entrypoint == "zone_property_data"
