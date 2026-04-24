from gettext import gettext as _

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from pulpcore.plugin.models import TaskSchedule
from pulpcore.plugin.serializers import IdentityField, ModelSerializer, RelatedField


class SchedulerTaskScheduleSerializer(ModelSerializer):
    """Serializer for TaskSchedule with full create/update support."""

    pulp_href = IdentityField(view_name="scheduler-task-schedules-detail")
    name = serializers.CharField(
        help_text=_("The name of the task schedule."),
        allow_blank=False,
        validators=[UniqueValidator(queryset=TaskSchedule.objects.all())],
    )
    task_name = serializers.CharField(
        help_text=_("The name of the task to be scheduled."),
    )
    dispatch_interval = serializers.DurationField(
        help_text=_("Periodicity of the schedule."),
        allow_null=True,
    )
    next_dispatch = serializers.DateTimeField(
        help_text=_("Timestamp of the next time the task will be dispatched."),
        read_only=True,
        allow_null=True,
    )
    last_task = RelatedField(
        help_text=_("The last task dispatched by this schedule."),
        read_only=True,
        view_name="tasks-detail",
    )

    class Meta:
        model = TaskSchedule
        fields = ModelSerializer.Meta.fields + (
            "name",
            "task_name",
            "dispatch_interval",
            "next_dispatch",
            "last_task",
        )
