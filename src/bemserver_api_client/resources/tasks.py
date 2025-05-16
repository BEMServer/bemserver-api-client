"""BEMServer API client resources

/tasks_by_campaigns/ endpoints
"""

from .base import BaseResources


class TaskByCampaignResources(BaseResources):
    endpoint_base_uri = "/tasks_by_campaigns/"
    client_entrypoint = "task_by_campaign"
