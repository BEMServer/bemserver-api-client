"""BEMServer API client resources

/energies/ endpoints
/energy_end_uses/ endpoints
/energy_consumption_timeseries_by_sites/ endpoints
/energy_consumption_timeseries_by_buildings/ endpoints
/energy_production_technologies/ endpoints
/energy_production_timeseries_by_sites/ endpoints
/energy_production_timeseries_by_buildings/ endpoints
"""
from .base import BaseResources


class EnergyResources(BaseResources):
    endpoint_base_uri = "/energies/"
    disabled_endpoints = ["getone", "create", "update", "delete"]


class EnergyEndUseResources(BaseResources):
    endpoint_base_uri = "/energy_end_uses/"
    disabled_endpoints = ["getone", "create", "update", "delete"]


class EnergyConsumptionTimseriesBySiteResources(BaseResources):
    endpoint_base_uri = "/energy_consumption_timeseries_by_sites/"


class EnergyConsumptionTimseriesByBuildingResources(BaseResources):
    endpoint_base_uri = "/energy_consumption_timeseries_by_buildings/"


class EnergyProductionTechnologyResources(BaseResources):
    endpoint_base_uri = "/energy_production_technologies/"
    disabled_endpoints = ["getone", "create", "update", "delete"]


class EnergyProductionTimseriesBySiteResources(BaseResources):
    endpoint_base_uri = "/energy_production_timeseries_by_sites/"


class EnergyProductionTimseriesByBuildingResources(BaseResources):
    endpoint_base_uri = "/energy_production_timeseries_by_buildings/"
