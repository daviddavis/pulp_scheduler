import pytest
import uuid

from pulpcore.tests.functional.utils import BindingsNamespace


@pytest.fixture(scope="session")
def scheduler_bindings(_api_client_set, bindings_cfg):
    """
    A namespace providing preconfigured pulp_scheduler api clients.

    e.g. `scheduler_bindings.SchedulerTaskSchedulesApi.list()`.
    """
    from pulpcore.client import pulp_scheduler as scheduler_bindings_module

    api_client = scheduler_bindings_module.ApiClient(bindings_cfg)
    _api_client_set.add(api_client)
    yield BindingsNamespace(scheduler_bindings_module, api_client)
    _api_client_set.remove(api_client)


@pytest.fixture
def task_schedule_factory(scheduler_bindings, add_to_cleanup):
    """A factory to generate a TaskSchedule with auto-cleanup."""

    def _create_task_schedule(**kwargs):
        kwargs.setdefault("name", str(uuid.uuid4()))
        kwargs.setdefault("task_name", "pulpcore.app.tasks.orphan_cleanup")
        kwargs.setdefault("dispatch_interval", "P1D")
        schedule = scheduler_bindings.SchedulerTaskSchedulesApi.create(kwargs)
        add_to_cleanup(scheduler_bindings.SchedulerTaskSchedulesApi, schedule.pulp_href)
        return schedule

    return _create_task_schedule
