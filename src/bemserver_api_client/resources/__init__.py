"""BEMServer API client resources"""

from . import (
    about,
    analysis,
    auth,
    campaigns,
    energy,
    events,
    io,
    notifications,
    services,
    structural_elements,
    timeseries,
    users,
    weather,
)

__all__ = [
    about.AboutResources,
    analysis.AnalysisResources,
    auth.AuthenticationResources,
    campaigns.CampaignResources,
    campaigns.UserGroupByCampaignResources,
    campaigns.CampaignScopeResources,
    campaigns.UserGroupByCampaignScopeResources,
    energy.EnergyResources,
    energy.EnergyEndUseResources,
    energy.EnergyConsumptionTimseriesBySiteResources,
    energy.EnergyConsumptionTimseriesByBuildingResources,
    energy.EnergyProductionTechnologyResources,
    energy.EnergyProductionTimseriesBySiteResources,
    energy.EnergyProductionTimseriesByBuildingResources,
    events.EventResources,
    events.EventCategoryResources,
    events.EventCategoryByUserResources,
    events.EventBySiteResources,
    events.EventByBuildingResources,
    events.EventByStoreyResources,
    events.EventBySpaceResources,
    events.EventByZoneResources,
    io.IOResources,
    notifications.NotificationResources,
    services.ST_CleanupByCampaignResources,
    services.ST_CleanupByTimeseriesResources,
    services.ST_CheckMissingByCampaignResources,
    services.ST_CheckOutlierByCampaignResources,
    services.ST_DownloadWeatherDataBySiteResources,
    services.ST_DownloadWeatherForecastDataBySiteResources,
    structural_elements.SiteResources,
    structural_elements.BuildingResources,
    structural_elements.StoreyResources,
    structural_elements.SpaceResources,
    structural_elements.ZoneResources,
    structural_elements.StructuralElementPropertyResources,
    structural_elements.SitePropertyResources,
    structural_elements.BuildingPropertyResources,
    structural_elements.StoreyPropertyResources,
    structural_elements.SpacePropertyResources,
    structural_elements.ZonePropertyResources,
    structural_elements.SitePropertyDataResources,
    structural_elements.BuildingPropertyDataResources,
    structural_elements.StoreyPropertyDataResources,
    structural_elements.SpacePropertyDataResources,
    structural_elements.ZonePropertyDataResources,
    timeseries.TimeseriesResources,
    timeseries.TimeseriesDataStateResources,
    timeseries.TimeseriesPropertyResources,
    timeseries.TimeseriesPropertyDataResources,
    timeseries.TimeseriesDataResources,
    timeseries.TimeseriesBySiteResources,
    timeseries.TimeseriesByBuildingResources,
    timeseries.TimeseriesByStoreyResources,
    timeseries.TimeseriesBySpaceResources,
    timeseries.TimeseriesByZoneResources,
    timeseries.TimeseriesByEventResources,
    users.UserResources,
    users.UserGroupResources,
    users.UserByUserGroupResources,
    weather.WeatherTimseriesBySiteResources,
]


RESOURCES_MAP = {
    resource_cls.client_entrypoint: resource_cls for resource_cls in __all__
}
