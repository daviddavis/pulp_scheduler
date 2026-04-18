# pulp-scheduler

A Pulp plugin that exposes full CRUD operations for `TaskSchedule` resources.

Pulpcore ships a read-only `TaskScheduleViewSet` (list + retrieve). This plugin
adds a writable viewset so that admins can create, update, and delete task
schedules through the REST API.

## Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/pulp/api/v3/scheduler/task-schedules/` | List task schedules |
| POST | `/pulp/api/v3/scheduler/task-schedules/` | Create a task schedule |
| GET | `/pulp/api/v3/scheduler/task-schedules/<pk>/` | Retrieve a task schedule |
| PUT | `/pulp/api/v3/scheduler/task-schedules/<pk>/` | Update a task schedule |
| PATCH | `/pulp/api/v3/scheduler/task-schedules/<pk>/` | Partial update a task schedule |
| DELETE | `/pulp/api/v3/scheduler/task-schedules/<pk>/` | Delete a task schedule |

## Installation

```bash
pip install -e ./pulp_scheduler
```
