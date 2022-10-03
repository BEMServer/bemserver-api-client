"""BEMServer API client resources

/timeseries/ endpoints
/timeseries_data_states/ endpoints
/timeseries_properties/ endpoints
/timeseries_property_data/ endpoints
/timeseries_data/ endpoints
/timeseries_by_sites/ endpoints
/timeseries_by_buildings/ endpoints
/timeseries_by_storeys/ endpoints
/timeseries_by_spaces/ endpoints
/timeseries_by_zones/ endpoints
"""
from .base import BaseResources


class TimeseriesResources(BaseResources):
    endpoint_base_uri = "/timeseries/"


class TimeseriesDataStateResources(BaseResources):
    endpoint_base_uri = "/timeseries_data_states/"


class TimeseriesPropertyResources(BaseResources):
    endpoint_base_uri = "/timeseries_properties/"


class TimeseriesPropertyDataResources(BaseResources):
    endpoint_base_uri = "/timeseries_property_data/"


class TimeseriesDataResources(BaseResources):
    endpoint_base_uri = "/timeseries_data/"
    disabled_endpoints = ["getall", "getone", "create", "update", "delete"]

    def endpoint_uri_by_campaign(self, campaign_id):
        return f"{self.endpoint_base_uri}campaign/{str(campaign_id)}/"

    def upload_csv(self, data_state, csv_files):
        """

        :param dict csv_files:
            key is the upload field name (csv_file)
            value is a file stream (tempfile.SpooledTemporaryFile)
        """
        return self._req.upload(
            self.endpoint_base_uri,
            params={"data_state": data_state},
            files=csv_files,
        )

    def upload_csv_by_names(self, campaign_id, data_state, csv_files):
        """

        :param dict csv_files:
            key is the upload field name (csv_file)
            value is a file stream (tempfile.SpooledTemporaryFile)
        """
        return self._req.upload(
            self.endpoint_uri_by_campaign(campaign_id),
            params={"data_state": data_state},
            files=csv_files,
        )

    def download_csv(
        self,
        start_time,
        end_time,
        data_state,
        timeseries_ids,
        timezone="UTC",
    ):
        return self._req.download(
            self.endpoint_base_uri,
            params={
                "start_time": start_time,
                "end_time": end_time,
                "data_state": data_state,
                "timeseries": timeseries_ids,
                "timezone": timezone,
            },
        )

    def download_csv_by_names(
        self,
        campaign_id,
        start_time,
        end_time,
        data_state,
        timeseries_names,
        timezone="UTC",
    ):
        return self._req.download(
            self.endpoint_uri_by_campaign(campaign_id),
            params={
                "start_time": start_time,
                "end_time": end_time,
                "data_state": data_state,
                "timeseries": timeseries_names,
                "timezone": timezone,
            },
        )

    def download_csv_aggregate(
        self,
        start_time,
        end_time,
        data_state,
        timeseries_ids,
        timezone="UTC",
        aggregation="avg",
        bucket_width_value="1",
        bucket_width_unit="hour",
    ):
        return self._req.download(
            f"{self.endpoint_base_uri}aggregate",
            params={
                "start_time": start_time,
                "end_time": end_time,
                "data_state": data_state,
                "timeseries": timeseries_ids,
                "timezone": timezone,
                "aggregation": aggregation,
                "bucket_width_value": bucket_width_value,
                "bucket_width_unit": bucket_width_unit,
            },
        )

    def download_csv_aggregate_by_names(
        self,
        campaign_id,
        start_time,
        end_time,
        data_state,
        timeseries_names,
        timezone="UTC",
        aggregation="avg",
        bucket_width_value="1",
        bucket_width_unit="hour",
    ):
        return self._req.download(
            f"{self.endpoint_uri_by_campaign(campaign_id)}aggregate",
            params={
                "start_time": start_time,
                "end_time": end_time,
                "data_state": data_state,
                "timeseries": timeseries_names,
                "timezone": timezone,
                "aggregation": aggregation,
                "bucket_width_value": bucket_width_value,
                "bucket_width_unit": bucket_width_unit,
            },
        )

    def delete(self, start_time, end_time, data_state, timeseries_ids):
        return self._req._execute(
            "DELETE",
            self.endpoint_base_uri,
            params={
                "start_time": start_time,
                "end_time": end_time,
                "data_state": data_state,
                "timeseries": timeseries_ids,
            },
        )

    def delete_by_names(
        self,
        campaign_id,
        start_time,
        end_time,
        data_state,
        timeseries_names,
    ):
        return self._req._execute(
            "DELETE",
            self.endpoint_uri_by_campaign(campaign_id),
            params={
                "start_time": start_time,
                "end_time": end_time,
                "data_state": data_state,
                "timeseries": timeseries_names,
            },
        )


class TimeseriesBySiteResources(BaseResources):
    endpoint_base_uri = "/timeseries_by_sites/"
    disabled_endpoints = ["update"]


class TimeseriesByBuildingResources(BaseResources):
    endpoint_base_uri = "/timeseries_by_buildings/"
    disabled_endpoints = ["update"]


class TimeseriesByStoreyResources(BaseResources):
    endpoint_base_uri = "/timeseries_by_storeys/"
    disabled_endpoints = ["update"]


class TimeseriesBySpaceResources(BaseResources):
    endpoint_base_uri = "/timeseries_by_spaces/"
    disabled_endpoints = ["update"]


class TimeseriesByZoneResources(BaseResources):
    endpoint_base_uri = "/timeseries_by_zones/"
    disabled_endpoints = ["update"]
