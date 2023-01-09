Changelog
---------

0.5.2 (2023-01-09)
++++++++++++++++++

Bug fixes:

- Require bemserver-api still >=0.5.0 and <0.6.0

Other changes:

- Remove unusable 0.5.1 release from PyPI

0.5.1 (2023-01-06)
++++++++++++++++++

Bug fixes:

- Remove obsolete event_levels resources

Other changes:

- Support Python 3.11

0.5.0 (2022-12-15)
++++++++++++++++++

Features:

- Event API updates on query args:
    - replace `level_id` with `level` enum
    - add `level_min` and `in_source`
- Timeseries API: add `event_id` query arg

Other changes:

- Require bemserver-api >=0.5.0 and <0.6.0

0.4.0 (2022-12-15)
++++++++++++++++++

Features:

- Add events by sites/buildings/storeys/spaces/zones resources
- Remove update on timeseries_by_events resources

Other changes:

- Require bemserver-api >=0.4.0 and <0.5.0

0.3.0 (2022-12-07)
++++++++++++++++++

Features:

- Add Events (levels, categories...) resources
- Add check missing service resources

Other changes:

- Require bemserver-api >=0.3.0 and <0.4.0

0.2.0 (2022-11-30)
++++++++++++++++++

Features:

- Timeseries data upload/download in JSON format
- Add DataFormat, Aggregation and BucketWidthUnit enums

Other changes:

- Require bemserver-api >=0.2.0 and <0.3.0

0.1.0 (2022-11-22)
++++++++++++++++++

Features:

- Authentication (HTTP BASIC)
- Check required BEMServer API version
- Implement all BEMServer API endpoints
- Manage BEMServer API responses (errors, ETag, pagination...)

Other changes:

- Require bemserver-api >=0.1.0 and <0.2.0
