from rest_framework import mixins

from pulpcore.plugin.viewsets import NamedModelViewSet, RolesMixin

from pulp_scheduler.app.models import TaskPlan
from pulp_scheduler.app.serializers import TaskPlanSerializer


class TaskPlanViewSet(
    NamedModelViewSet,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    RolesMixin,
):
    """
    A ViewSet for managing TaskPlans.

    Plans are created with their full set of steps and are immutable thereafter; to
    change a plan, delete it and create a new one.
    """

    queryset = TaskPlan.objects.all().prefetch_related("steps")
    endpoint_name = "task-plans"

    @classmethod
    def endpoint_pieces(cls):
        return ["scheduler", "task-plans"]

    serializer_class = TaskPlanSerializer
    ordering = "-pulp_created"
    filterset_fields = {
        "name": ["exact", "contains"],
        "state": ["exact", "in"],
    }
    queryset_filtering_required_permission = "scheduler.view_taskplan"

    DEFAULT_ACCESS_POLICY = {
        "statements": [
            {
                "action": ["list", "retrieve", "my_permissions"],
                "principal": "authenticated",
                "effect": "allow",
                "condition": "has_model_or_domain_or_obj_perms:scheduler.view_taskplan",
            },
            {
                "action": [
                    "create",
                    "destroy",
                    "list_roles",
                    "add_role",
                    "remove_role",
                ],
                "principal": "authenticated",
                "effect": "allow",
                "condition": "has_model_or_domain_or_obj_perms:scheduler.change_taskplan",
            },
        ],
        "queryset_scoping": {"function": "scope_queryset"},
    }
    LOCKED_ROLES = {
        "scheduler.taskplan_admin": [
            "scheduler.view_taskplan",
            "scheduler.change_taskplan",
            "scheduler.delete_taskplan",
            "scheduler.manage_roles_taskplan",
        ],
        "scheduler.taskplan_viewer": ["scheduler.view_taskplan"],
    }
