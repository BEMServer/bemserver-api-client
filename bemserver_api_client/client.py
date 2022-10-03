"""BEMServer API client"""
import logging
from requests.auth import HTTPBasicAuth

from .request import BEMServerApiClientRequest
from .resources import (
    AboutResources,
    UserResources,
    UserGroupResources,
    UserByUserGroupResources,
    CampaignResources,
    UserGroupByCampaignResources,
    CampaignScopeResources,
    UserGroupByCampaignScopeResources,
    TimeseriesResources,
    TimeseriesDataStateResources,
    TimeseriesPropertyResources,
    TimeseriesPropertyDataResources,
    TimeseriesDataResources,
    EventResources,
    EventStateResources,
    EventLevelResources,
    EventCategoryResources,
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
    TimeseriesBySiteResources,
    TimeseriesByBuildingResources,
    TimeseriesByStoreyResources,
    TimeseriesBySpaceResources,
    TimeseriesByZoneResources,
    IOResources,
    AnalysisResources,
    ST_CleanupByCampaignResources,
    ST_CleanupByTimeseriesResources,
)


APICLI_LOGGER = logging.getLogger(__name__)


class BEMServerApiClient:
    """API client"""

    def __init__(
        self, host, use_ssl=True, authentication_method=None, uri_prefix="http"
    ):
        self.base_uri_prefix = uri_prefix or "http"
        self.host = host
        self.use_ssl = use_ssl

        self._request_manager = BEMServerApiClientRequest(
            self.base_uri,
            authentication_method,
            logger=APICLI_LOGGER,
        )

        self.about = AboutResources(self._request_manager)
        self.io = IOResources(self._request_manager)

        self.users = UserResources(self._request_manager)
        self.user_groups = UserGroupResources(self._request_manager)
        self.user_by_user_groups = UserByUserGroupResources(self._request_manager)

        self.campaigns = CampaignResources(self._request_manager)
        self.user_groups_by_campaigns = UserGroupByCampaignResources(
            self._request_manager
        )
        self.campaign_scopes = CampaignScopeResources(self._request_manager)
        self.user_groups_by_campaign_scopes = UserGroupByCampaignScopeResources(
            self._request_manager
        )

        self.timeseries = TimeseriesResources(self._request_manager)
        self.timeseries_datastates = TimeseriesDataStateResources(self._request_manager)
        self.timeseries_properties = TimeseriesPropertyResources(self._request_manager)
        self.timeseries_property_data = TimeseriesPropertyDataResources(
            self._request_manager
        )
        self.timeseries_data = TimeseriesDataResources(self._request_manager)

        self.events = EventResources(self._request_manager)
        self.event_states = EventStateResources(self._request_manager)
        self.event_levels = EventLevelResources(self._request_manager)
        self.event_categories = EventCategoryResources(self._request_manager)

        self.sites = SiteResources(self._request_manager)
        self.buildings = BuildingResources(self._request_manager)
        self.storeys = StoreyResources(self._request_manager)
        self.spaces = SpaceResources(self._request_manager)
        self.zones = ZoneResources(self._request_manager)

        self.structural_element_properties = StructuralElementPropertyResources(
            self._request_manager
        )
        self.site_properties = SitePropertyResources(self._request_manager)
        self.building_properties = BuildingPropertyResources(self._request_manager)
        self.storey_properties = StoreyPropertyResources(self._request_manager)
        self.space_properties = SpacePropertyResources(self._request_manager)
        self.zone_properties = ZonePropertyResources(self._request_manager)

        self.site_property_data = SitePropertyDataResources(self._request_manager)
        self.building_property_data = BuildingPropertyDataResources(
            self._request_manager
        )
        self.storey_property_data = StoreyPropertyDataResources(self._request_manager)
        self.space_property_data = SpacePropertyDataResources(self._request_manager)
        self.zone_property_data = ZonePropertyDataResources(self._request_manager)

        self.timeseries_by_sites = TimeseriesBySiteResources(self._request_manager)
        self.timeseries_by_buildings = TimeseriesByBuildingResources(
            self._request_manager
        )
        self.timeseries_by_storeys = TimeseriesByStoreyResources(self._request_manager)
        self.timeseries_by_spaces = TimeseriesBySpaceResources(self._request_manager)
        self.timeseries_by_zones = TimeseriesByZoneResources(self._request_manager)

        self.analysis = AnalysisResources(self._request_manager)

        self.st_cleanup_by_campaign = ST_CleanupByCampaignResources(
            self._request_manager
        )
        self.st_cleanup_by_timeseries = ST_CleanupByTimeseriesResources(
            self._request_manager
        )

    @property
    def uri_prefix(self):
        uri_prefix = self.base_uri_prefix
        if self.use_ssl:
            uri_prefix = self.base_uri_prefix.replace("http", "https")
        return f"{uri_prefix}://"

    @property
    def base_uri(self):
        return f"{self.uri_prefix}{self.host}"

    @staticmethod
    def make_http_basic_auth(email, password):
        return HTTPBasicAuth(
            email.encode(encoding="utf-8"),
            password.encode(encoding="utf-8"),
        )
