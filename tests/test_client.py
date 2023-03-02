"""BEMServer API client tests"""
import pytest
from requests.auth import HTTPBasicAuth

from bemserver_api_client import BEMServerApiClient
from bemserver_api_client.exceptions import BEMServerAPIVersionError
from bemserver_api_client.client import REQUIRED_API_VERSION
from bemserver_api_client.request import BEMServerApiClientRequest
from bemserver_api_client.resources import (
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
    ST_CheckMissingByCampaignResources,
    ST_CheckOutlierByCampaignResources,
    EnergyResources,
    EnergyEndUseResources,
    EnergyConsumptionTimseriesBySiteResources,
    EnergyConsumptionTimseriesByBuildingResources,
    EventResources,
    EventCategoryResources,
    EventCategoryByUserResources,
    EventBySiteResources,
    EventByBuildingResources,
    EventByStoreyResources,
    EventBySpaceResources,
    EventByZoneResources,
    TimeseriesByEventResources,
    NotificationResources,
)


class TestAPIClient:
    def test_api_client_auth(self):
        ret = BEMServerApiClient.make_http_basic_auth("chuck@test.com", "N0rr1s")
        assert isinstance(ret, HTTPBasicAuth)
        assert isinstance(ret.username, bytes)
        assert isinstance(ret.password, bytes)
        assert ret.username.decode(encoding="utf-8") == "chuck@test.com"
        assert ret.password.decode(encoding="utf-8") == "N0rr1s"

    def test_api_client(self):
        apicli = BEMServerApiClient("localhost:5050")
        assert apicli.use_ssl
        assert apicli.base_uri_prefix == "http"
        assert apicli.uri_prefix == "https://"
        assert apicli.base_uri == "https://localhost:5050"
        apicli.use_ssl = False
        assert apicli.uri_prefix == "http://"
        assert apicli.base_uri == "http://localhost:5050"

        apicli.base_uri_prefix = "http+mock"
        assert apicli.uri_prefix == "http+mock://"
        assert apicli.base_uri == "http+mock://localhost:5050"
        apicli.use_ssl = True
        assert apicli.uri_prefix == "https+mock://"
        assert apicli.base_uri == "https+mock://localhost:5050"

        assert isinstance(apicli._request_manager, BEMServerApiClientRequest)

    def test_api_client_resources(self):
        apicli = BEMServerApiClient("localhost:5050")

        assert hasattr(apicli, "about")
        assert isinstance(apicli.about, AboutResources)
        assert hasattr(apicli, "io")
        assert isinstance(apicli.io, IOResources)

        assert hasattr(apicli, "users")
        assert isinstance(apicli.users, UserResources)
        assert hasattr(apicli, "user_groups")
        assert isinstance(apicli.user_groups, UserGroupResources)
        assert hasattr(apicli, "user_by_user_groups")
        assert isinstance(apicli.user_by_user_groups, UserByUserGroupResources)

        assert hasattr(apicli, "campaigns")
        assert isinstance(apicli.campaigns, CampaignResources)
        assert hasattr(apicli, "user_groups_by_campaigns")
        assert isinstance(apicli.user_groups_by_campaigns, UserGroupByCampaignResources)
        assert hasattr(apicli, "campaign_scopes")
        assert isinstance(apicli.campaign_scopes, CampaignScopeResources)
        assert hasattr(apicli, "user_groups_by_campaign_scopes")
        assert isinstance(
            apicli.user_groups_by_campaign_scopes, UserGroupByCampaignScopeResources
        )

        assert hasattr(apicli, "timeseries")
        assert isinstance(apicli.timeseries, TimeseriesResources)
        assert hasattr(apicli, "timeseries_datastates")
        assert isinstance(apicli.timeseries_datastates, TimeseriesDataStateResources)
        assert hasattr(apicli, "timeseries_properties")
        assert isinstance(apicli.timeseries_properties, TimeseriesPropertyResources)
        assert hasattr(apicli, "timeseries_property_data")
        assert isinstance(
            apicli.timeseries_property_data, TimeseriesPropertyDataResources
        )
        assert hasattr(apicli, "timeseries_data")
        assert isinstance(apicli.timeseries_data, TimeseriesDataResources)

        assert hasattr(apicli, "sites")
        assert isinstance(apicli.sites, SiteResources)
        assert hasattr(apicli, "buildings")
        assert isinstance(apicli.buildings, BuildingResources)
        assert hasattr(apicli, "storeys")
        assert isinstance(apicli.storeys, StoreyResources)
        assert hasattr(apicli, "spaces")
        assert isinstance(apicli.spaces, SpaceResources)
        assert hasattr(apicli, "zones")
        assert isinstance(apicli.zones, ZoneResources)

        assert hasattr(apicli, "structural_element_properties")
        assert isinstance(
            apicli.structural_element_properties, StructuralElementPropertyResources
        )
        assert hasattr(apicli, "site_properties")
        assert isinstance(apicli.site_properties, SitePropertyResources)
        assert hasattr(apicli, "building_properties")
        assert isinstance(apicli.building_properties, BuildingPropertyResources)
        assert hasattr(apicli, "storey_properties")
        assert isinstance(apicli.storey_properties, StoreyPropertyResources)
        assert hasattr(apicli, "space_properties")
        assert isinstance(apicli.space_properties, SpacePropertyResources)
        assert hasattr(apicli, "zone_properties")
        assert isinstance(apicli.zone_properties, ZonePropertyResources)
        assert hasattr(apicli, "site_property_data")
        assert isinstance(apicli.site_property_data, SitePropertyDataResources)
        assert hasattr(apicli, "building_property_data")
        assert isinstance(apicli.building_property_data, BuildingPropertyDataResources)
        assert hasattr(apicli, "storey_property_data")
        assert isinstance(apicli.storey_property_data, StoreyPropertyDataResources)
        assert hasattr(apicli, "space_property_data")
        assert isinstance(apicli.space_property_data, SpacePropertyDataResources)
        assert hasattr(apicli, "zone_property_data")
        assert isinstance(apicli.zone_property_data, ZonePropertyDataResources)

        assert hasattr(apicli, "timeseries_by_sites")
        assert isinstance(apicli.timeseries_by_sites, TimeseriesBySiteResources)
        assert hasattr(apicli, "timeseries_by_buildings")
        assert isinstance(apicli.timeseries_by_buildings, TimeseriesByBuildingResources)
        assert hasattr(apicli, "timeseries_by_storeys")
        assert isinstance(apicli.timeseries_by_storeys, TimeseriesByStoreyResources)
        assert hasattr(apicli, "timeseries_by_spaces")
        assert isinstance(apicli.timeseries_by_spaces, TimeseriesBySpaceResources)
        assert hasattr(apicli, "timeseries_by_zones")
        assert isinstance(apicli.timeseries_by_zones, TimeseriesByZoneResources)

        assert hasattr(apicli, "analysis")
        assert isinstance(apicli.analysis, AnalysisResources)

        assert hasattr(apicli, "st_cleanup_by_campaign")
        assert isinstance(apicli.st_cleanup_by_campaign, ST_CleanupByCampaignResources)
        assert hasattr(apicli, "st_cleanup_by_timeseries")
        assert isinstance(
            apicli.st_cleanup_by_timeseries, ST_CleanupByTimeseriesResources
        )

        assert hasattr(apicli, "st_check_missing_by_campaign")
        assert isinstance(
            apicli.st_check_missing_by_campaign, ST_CheckMissingByCampaignResources
        )

        assert hasattr(apicli, "st_check_outlier_by_campaign")
        assert isinstance(
            apicli.st_check_outlier_by_campaign, ST_CheckOutlierByCampaignResources
        )

        assert hasattr(apicli, "energies")
        assert isinstance(apicli.energies, EnergyResources)
        assert hasattr(apicli, "energy_end_uses")
        assert isinstance(apicli.energy_end_uses, EnergyEndUseResources)
        assert hasattr(apicli, "energy_cons_ts_by_sites")
        assert isinstance(
            apicli.energy_cons_ts_by_sites, EnergyConsumptionTimseriesBySiteResources
        )
        assert hasattr(apicli, "energy_cons_ts_by_buildings")
        assert isinstance(
            apicli.energy_cons_ts_by_buildings,
            EnergyConsumptionTimseriesByBuildingResources,
        )

        assert hasattr(apicli, "events")
        assert isinstance(apicli.events, EventResources)
        assert hasattr(apicli, "event_categories")
        assert isinstance(apicli.event_categories, EventCategoryResources)
        assert hasattr(apicli, "event_categories_by_users")
        assert isinstance(
            apicli.event_categories_by_users, EventCategoryByUserResources
        )

        assert hasattr(apicli, "event_by_sites")
        assert isinstance(apicli.event_by_sites, EventBySiteResources)
        assert hasattr(apicli, "event_by_buildings")
        assert isinstance(apicli.event_by_buildings, EventByBuildingResources)
        assert hasattr(apicli, "event_by_storeys")
        assert isinstance(apicli.event_by_storeys, EventByStoreyResources)
        assert hasattr(apicli, "event_by_spaces")
        assert isinstance(apicli.event_by_spaces, EventBySpaceResources)
        assert hasattr(apicli, "event_by_zones")
        assert isinstance(apicli.event_by_zones, EventByZoneResources)
        assert hasattr(apicli, "timeseries_by_events")
        assert isinstance(apicli.timeseries_by_events, TimeseriesByEventResources)

        assert hasattr(apicli, "notifications")
        assert isinstance(apicli.notifications, NotificationResources)

        assert not hasattr(apicli, "whatever_resources_that_does_not_exist")

    def test_api_client_required_api_version_manual(self):
        req_version_min = REQUIRED_API_VERSION["min"]
        v = f"{req_version_min.major}.{req_version_min.minor}.42"
        BEMServerApiClient.check_api_version(str(v))

        # API version not compatible with client.
        with pytest.raises(BEMServerAPIVersionError):
            BEMServerApiClient.check_api_version("1.0.0")

        # Invalid API versionning.
        with pytest.raises(BEMServerAPIVersionError):
            BEMServerApiClient.check_api_version(None)
        with pytest.raises(BEMServerAPIVersionError):
            BEMServerApiClient.check_api_version("invalid")

    def test_api_client_required_api_version_auto_check(self, mock_request):
        host = "localhost:5000"
        auto_check = True
        req_mngr = mock_request

        BEMServerApiClient(host, auto_check=auto_check, request_manager=req_mngr)

        # API version not compatible with client.
        with pytest.raises(BEMServerAPIVersionError):
            BEMServerApiClient(host, auto_check=auto_check, request_manager=req_mngr)

        # Invalid API versionning.
        with pytest.raises(BEMServerAPIVersionError):
            BEMServerApiClient(host, auto_check=auto_check, request_manager=req_mngr)
