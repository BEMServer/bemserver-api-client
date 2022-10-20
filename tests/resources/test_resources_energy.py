"""BEMServer API client energy resources tests"""
from bemserver_api_client.resources.base import BaseResources
from bemserver_api_client.resources import (
    EnergySourceResources,
    EnergyEndUseResources,
    EnergyConsumptionTimseriesBySiteResources,
    EnergyConsumptionTimseriesByBuildingResources,
)


class TestAPIClientResourcesEnergySources:
    def test_api_client_resources_energy_sources(self):
        assert issubclass(EnergySourceResources, BaseResources)
        assert EnergySourceResources.endpoint_base_uri == "/energy_sources/"
        assert EnergySourceResources.disabled_endpoints == [
            "getone",
            "create",
            "update",
            "delete",
        ]


class TestAPIClientResourcesEnergyEndUses:
    def test_api_client_resources_energy_end_uses(self):
        assert issubclass(EnergyEndUseResources, BaseResources)
        assert EnergyEndUseResources.endpoint_base_uri == "/energy_end_uses/"
        assert EnergyEndUseResources.disabled_endpoints == [
            "getone",
            "create",
            "update",
            "delete",
        ]


class TestAPIClientResourcesEnergyConsumption:
    def test_api_client_resources_energy_consumption(self):
        assert issubclass(EnergyConsumptionTimseriesBySiteResources, BaseResources)
        assert EnergyConsumptionTimseriesBySiteResources.endpoint_base_uri == (
            "/energy_consumption_timeseries_by_sites/"
        )
        assert EnergyConsumptionTimseriesBySiteResources.disabled_endpoints == []

        assert issubclass(EnergyConsumptionTimseriesByBuildingResources, BaseResources)
        assert EnergyConsumptionTimseriesByBuildingResources.endpoint_base_uri == (
            "/energy_consumption_timeseries_by_buildings/"
        )
        assert EnergyConsumptionTimseriesByBuildingResources.disabled_endpoints == []
