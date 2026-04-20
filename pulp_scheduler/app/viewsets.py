from rest_framework import mixins

from pulpcore.app.models import TaskSchedule
from pulpcore.app.viewsets import NamedModelViewSet, RolesMixin

from .serializers import SchedulerTaskScheduleSerializer


class SchedulerTaskScheduleViewSet(
    NamedModelViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    RolesMixin,
):
    """
    A ViewSet for managing TaskSchedules with full CRUD support.
    """

    queryset = TaskSchedule.objects.all()
    endpoint_name = "task-schedules"

    @classmethod
    def endpoint_pieces(cls):
        return ["scheduler", "task-schedules"]

    serializer_class = SchedulerTaskScheduleSerializer
    ordering = "-pulp_created"
    filterset_fields = {
        "name": ["exact", "contains"],
        "task_name": ["exact", "contains"],
    }
    queryset_filtering_required_permission = "core.view_taskschedule"

    DEFAULT_ACCESS_POLICY = {
        "statements": [
            {
                "action": ["list", "retrieve", "my_permissions"],
                "principal": "authenticated",
                "effect": "allow",
                "condition": "has_model_or_domain_or_obj_perms:core.view_taskschedule",
            },
            {
                "action": [
                    "create",
                    "update",
                    "partial_update",
                    "destroy",
                    "list_roles",
                    "add_role",
                    "remove_role",
                ],
                "principal": "authenticated",
                "effect": "allow",
                "condition": "has_model_or_domain_or_obj_perms:core.change_taskschedule",
            },
        ],
        "queryset_scoping": {"function": "scope_queryset"},
    }
    LOCKED_ROLES = {
        "core.taskschedule_admin": [
            "core.view_taskschedule",
            "core.change_taskschedule",
        ],
        "core.taskschedule_viewer": ["core.view_taskschedule"],
    }
