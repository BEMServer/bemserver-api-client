Changelog
---------

0.13.0 (2023-03-03)
+++++++++++++++++++

Features:

- Rename ``EnergySourceResources`` to ``EnergyResources``
- Add energy_production_technologies endpoints (``EnergyProductionTechnologyResources``)
- Add energy_production_timeseries_by_* endpoints (``EnergyProductionTimseriesBySiteResources`` and ``EnergyProductionTimseriesByBuildingResources``)
- Add weather_timeseries_by_sites endpoints (``WeatherTimseriesBySiteResources``)

Fixes:

- Raise ``BEMServerAPIClientValueError`` when ``AnalysisResources.get_completeness()`` is called with an unsupported bucket width
- Raise ``BEMServerAPIClientValueError`` when ``AnalysisResources.get_energy_consumption_breakdown()`` is called with an unsupported structural element type (not site or building)
- Raise ``BEMServerAPIClientValueError`` when ``TimeseriesDataResources.download_aggregate()`` is called with an unsupported aggregation or bucket width
- Raise ``BEMServerAPIClientValueError`` when ``TimeseriesDataResources.download_aggregate_by_names()`` is called with an unsupported aggregation or bucket width

Other changes:

- Require bemserver-api >=0.13.0 and <0.14.0
- Require bemserver-core 0.11.0

Follows `API update 0.13.0 <https://github.com/BEMServer/bemserver-api/blob/master/CHANGELOG.rst#0130-2023-03-01>`_

0.12.1 (2023-03-01)
+++++++++++++++++++

Fixes:

- Improve 409 client error processing (raises BEMServerAPIConflictError, with message)

Other changes:

- Require bemserver-api >=0.12.1 and <0.13.0

0.12.0 (2023-02-28)
+++++++++++++++++++

Other changes:

- Require bemserver-api >=0.12.0 and <0.13.0
- Require bemserver-core 0.10.1

0.11.1 (2023-02-13)
+++++++++++++++++++

Other changes:

- Require bemserver-api >=0.11.1 and <0.12.0

0.11.0 (2023-02-09)
+++++++++++++++++++

Features:

- Add ``StructuralElement`` enum
- Change ``AnalysisResources.get_energy_consumption_breakdown()``'s ``structural_element_type`` parameter type to use ``StructuralElement`` enum

Other changes:

- Require bemserver-api >=0.11.0 and <0.12.0
- Require bemserver-core 0.9.1

0.10.2 (2023-02-07)
+++++++++++++++++++

Other changes:

- Require bemserver-api >=0.10.3 and <0.11.0

0.10.1 (2023-02-01)
+++++++++++++++++++

Features:

- Update notifications resources:

  - add *campaign_id* filter on list endpoint
  - add *count_by_campaign* endpoint
  - add *mark_all_as_read* endpoint

Other changes:

- Require bemserver-api >=0.10.2 and <0.11.0
- Require bemserver-core 0.8.1

0.10.0 (2023-01-23)
+++++++++++++++++++

Features:

- Add check outliers data service resources

Other changes:

- Require bemserver-api >=0.10.0 and <0.11.0
- Require bemserver-core 0.8.0

0.9.0 (2023-01-12)
++++++++++++++++++

Client not really affected by API changes in version 0.9.0 (some ETags removed...).

Other changes:

- Require bemserver-api >=0.9.0 and <0.10.0
- Require bemserver-core 0.7.0

0.8.0 (2023-01-12)
++++++++++++++++++

Features:

- Remove timeseries get by sites/buildings/storeys/spaces/zones and by events resources
- Remove get events by sites/buildings/storeys/spaces/zones resources

Other changes:

- Require bemserver-api >=0.8.0 and <0.9.0
- Require bemserver-core 0.7.0

0.7.0 (2023-01-09)
++++++++++++++++++

Features:

- Add event categories by users resources
- Add notifications resources

Other changes:

- Require bemserver-api >=0.7.0 and <0.8.0
- Require bemserver-core 0.6.0

0.6.0 (2023-01-09)
++++++++++++++++++

Features:

- Add get events by sites/buildings/storeys/spaces/zones resources
- Add timeseries get by sites/buildings/storeys/spaces/zones and events resources

Other changes:

- Require bemserver-api >=0.6.0 and <0.7.0
- Require bemserver-core 0.5.0

0.5.2 (2023-01-09)
++++++++++++++++++

Fixes:

- Require bemserver-api still >=0.5.0 and <0.6.0

Other changes:

- Remove unusable 0.5.1 release from PyPI

0.5.1 (2023-01-06)
++++++++++++++++++

Fixes:

- Remove obsolete event_levels resources

Other changes:

- Support Python 3.11

0.5.0 (2022-12-15)
++++++++++++++++++

Features:

- Event API updates on query args:

  - replace ``level_id`` with ``EventLevel`` enum
  - add ``level_min`` and ``in_source``

- Timeseries API: add ``event_id`` query arg

Other changes:

- Require bemserver-api >=0.5.0 and <0.6.0
- Require bemserver-core 0.4.0

0.4.0 (2022-12-15)
++++++++++++++++++

Features:

- Add events by sites/buildings/storeys/spaces/zones resources
- Remove update on timeseries_by_events resources

Other changes:

- Require bemserver-api >=0.4.0 and <0.5.0
- Require bemserver-core 0.3.0

0.3.0 (2022-12-07)
++++++++++++++++++

Features:

- Add Events (levels, categories...) resources
- Add check missing service resources

Other changes:

- Require bemserver-api >=0.3.0 and <0.4.0
- Require bemserver-core 0.2.1

0.2.0 (2022-11-30)
++++++++++++++++++

Features:

- Timeseries data upload/download in JSON format
- Add ``DataFormat``, ``Aggregation`` and ``BucketWidthUnit`` enums

Other changes:

- Require bemserver-api >=0.2.0 and <0.3.0
- Require bemserver-core 0.2.0

0.1.0 (2022-11-22)
++++++++++++++++++

Features:

- Authentication (HTTP BASIC)
- Check required BEMServer API version
- Implement all BEMServer API endpoints
- Manage BEMServer API responses (errors, ETag, pagination...)

Other changes:

- Require bemserver-api >=0.1.0 and <0.2.0
- Require bemserver-core 0.1.0
