import json
import uuid

import pytest


@pytest.mark.parallel
def test_crud_task_schedule(scheduler_bindings, task_schedule_factory):
    """Test basic CRUD operations on TaskSchedules."""
    # CREATE
    name = str(uuid.uuid4())
    schedule = task_schedule_factory(
        name=name,
        task_name="pulpcore.app.tasks.orphan_cleanup",
        dispatch_interval="P1D",
    )
    assert schedule.name == name
    assert schedule.task_name == "pulpcore.app.tasks.orphan_cleanup"
    assert schedule.dispatch_interval == "1 00:00:00"
    assert schedule.pulp_href is not None

    # READ
    read_schedule = scheduler_bindings.SchedulerTaskSchedulesApi.read(
        schedule.pulp_href
    )
    assert read_schedule.name == name
    assert read_schedule.task_name == schedule.task_name

    # UPDATE (partial)
    new_name = str(uuid.uuid4())
    updated = scheduler_bindings.SchedulerTaskSchedulesApi.partial_update(
        schedule.pulp_href,
        {"name": new_name},
    )
    assert updated.name == new_name

    # UPDATE (full)
    another_name = str(uuid.uuid4())
    updated = scheduler_bindings.SchedulerTaskSchedulesApi.update(
        schedule.pulp_href,
        {
            "name": another_name,
            "task_name": "pulpcore.app.tasks.orphan_cleanup",
            "dispatch_interval": "P7D",
        },
    )
    assert updated.name == another_name
    assert updated.dispatch_interval == "7 00:00:00"

    # DELETE
    scheduler_bindings.SchedulerTaskSchedulesApi.delete(schedule.pulp_href)
    with pytest.raises(scheduler_bindings.ApiException) as exc:
        scheduler_bindings.SchedulerTaskSchedulesApi.read(schedule.pulp_href)
    assert exc.value.status == 404


@pytest.mark.parallel
def test_list_task_schedules(scheduler_bindings, task_schedule_factory):
    """Test listing and filtering task schedules."""
    name = str(uuid.uuid4())
    schedule = task_schedule_factory(name=name)

    # LIST with filter
    results = scheduler_bindings.SchedulerTaskSchedulesApi.list(name=name)
    assert results.count == 1
    assert results.results[0].name == name

    # LIST with task_name filter
    results = scheduler_bindings.SchedulerTaskSchedulesApi.list(
        task_name="pulpcore.app.tasks.orphan_cleanup"
    )
    assert results.count >= 1


@pytest.mark.parallel
def test_create_duplicate_name_fails(scheduler_bindings, task_schedule_factory):
    """Test that creating a task schedule with a duplicate name fails."""
    name = str(uuid.uuid4())
    task_schedule_factory(name=name)

    with pytest.raises(scheduler_bindings.ApiException) as exc:
        scheduler_bindings.SchedulerTaskSchedulesApi.create(
            {
                "name": name,
                "task_name": "pulpcore.app.tasks.orphan_cleanup",
                "dispatch_interval": "P1D",
            }
        )
    assert exc.value.status == 400


@pytest.mark.parallel
def test_create_without_required_fields(scheduler_bindings):
    """Test that creating a task schedule without required fields fails client-side."""
    with pytest.raises(Exception):
        scheduler_bindings.SchedulerTaskSchedulesApi.create({})


@pytest.mark.parallel
def test_null_dispatch_interval(scheduler_bindings, task_schedule_factory):
    """Test creating a one-shot schedule with null dispatch_interval."""
    schedule = task_schedule_factory(dispatch_interval=None)
    assert schedule.dispatch_interval is None


@pytest.mark.parallel
def test_read_only_fields(scheduler_bindings, task_schedule_factory):
    """Test that next_dispatch and last_task are read-only and present."""
    schedule = task_schedule_factory()
    assert schedule.next_dispatch is not None
    assert schedule.last_task is None
