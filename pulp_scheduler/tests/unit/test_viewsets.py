from pulp_scheduler.app.viewsets import TaskPlanViewSet


def test_access_policy_requires_view_for_read():
    """Read actions require view_taskplan permission."""
    policy = TaskPlanViewSet.DEFAULT_ACCESS_POLICY
    read_stmt = policy["statements"][0]
    assert set(read_stmt["action"]) == {"list", "retrieve", "my_permissions"}
    assert "view_taskplan" in read_stmt["condition"]


def test_access_policy_requires_change_for_write():
    """Write actions require change_taskplan permission."""
    policy = TaskPlanViewSet.DEFAULT_ACCESS_POLICY
    write_stmt = policy["statements"][1]
    assert "create" in write_stmt["action"]
    assert "destroy" in write_stmt["action"]
    assert "change_taskplan" in write_stmt["condition"]


def test_locked_roles():
    """Admin and viewer roles are defined."""
    roles = TaskPlanViewSet.LOCKED_ROLES
    assert "scheduler.taskplan_admin" in roles
    assert "scheduler.taskplan_viewer" in roles
    assert "scheduler.view_taskplan" in roles["scheduler.taskplan_viewer"]
    assert "scheduler.change_taskplan" in roles["scheduler.taskplan_admin"]
