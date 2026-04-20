from pulp_scheduler.app.viewsets import SchedulerTaskScheduleViewSet


def test_access_policy_requires_view_for_read():
    """Read actions require view_taskschedule permission."""
    policy = SchedulerTaskScheduleViewSet.DEFAULT_ACCESS_POLICY
    read_stmt = policy["statements"][0]
    assert set(read_stmt["action"]) == {"list", "retrieve", "my_permissions"}
    assert "view_taskschedule" in read_stmt["condition"]


def test_access_policy_requires_change_for_write():
    """Write actions require change_taskschedule permission."""
    policy = SchedulerTaskScheduleViewSet.DEFAULT_ACCESS_POLICY
    write_stmt = policy["statements"][1]
    assert "create" in write_stmt["action"]
    assert "destroy" in write_stmt["action"]
    assert "change_taskschedule" in write_stmt["condition"]


def test_locked_roles():
    """Admin and viewer roles are defined."""
    roles = SchedulerTaskScheduleViewSet.LOCKED_ROLES
    assert "core.taskschedule_admin" in roles
    assert "core.taskschedule_viewer" in roles
    assert "core.view_taskschedule" in roles["core.taskschedule_viewer"]
    assert "core.change_taskschedule" in roles["core.taskschedule_admin"]
