"""BEMServer API client resources"""

from .about import AboutResources  # noqa
from .analysis import AnalysisResources  # noqa
from .campaigns import (  # noqa
    CampaignResources,
    UserGroupByCampaignResources,
    CampaignScopeResources,
    UserGroupByCampaignScopeResources,
)
from .events import (  # noqa
    EventResources,
    EventStateResources,
    EventLevelResources,
    EventCategoryResources,
)
from .io import IOResources  # noqa
from .services import (  # noqa
    ST_CleanupByCampaignResources,
    ST_CleanupByTimeseriesResources,
)
from .structural_elements import (  # noqa
    SiteResources,
    BuildingResources,
    StoreyResources,
    SpaceResources,
    ZoneResources,
    StructuralElementPropertyResources,
    SitePropertyResources,
    BuildingPropertyResources,
    StoreyPropertyResources,
    SpacePropertyResources,
    ZonePropertyResources,
    SitePropertyDataResources,
    BuildingPropertyDataResources,
    StoreyPropertyDataResources,
    SpacePropertyDataResources,
    ZonePropertyDataResources,
)
from .timeseries import (  # noqa
    TimeseriesResources,
    TimeseriesDataStateResources,
    TimeseriesPropertyResources,
    TimeseriesPropertyDataResources,
    TimeseriesDataResources,
    TimeseriesBySiteResources,
    TimeseriesByBuildingResources,
    TimeseriesByStoreyResources,
    TimeseriesBySpaceResources,
    TimeseriesByZoneResources,
)
from .users import (  # noqa
    UserResources,
    UserGroupResources,
    UserByUserGroupResources,
)
