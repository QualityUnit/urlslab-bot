from typing import Callable

from fastapi import APIRouter, Depends, Request

from backend.app.controllers import TaskController
from backend.app.models.task import TaskPermission
from backend.app.schemas.requests.tasks import TaskCreate
from backend.app.schemas.responses.tasks import TaskResponse
from backend.core.factory import Factory
from backend.core.fastapi.dependencies.permissions import Permissions

task_router = APIRouter()


@task_router.get("/", response_model=list[TaskResponse])
def get_tasks(
    request: Request,
    task_controller: TaskController = Depends(Factory().get_task_controller),
    assert_access: Callable = Depends(Permissions(TaskPermission.READ)),
) -> list[TaskResponse]:
    tasks = task_controller.get_by_author_id(request.user.id)

    assert_access(tasks)
    return tasks


@task_router.post("/", response_model=TaskResponse, status_code=201)
def create_task(
    request: Request,
    task_create: TaskCreate,
    task_controller: TaskController = Depends(Factory().get_task_controller),
) -> TaskResponse:
    task = task_controller.add(
        title=task_create.title,
        description=task_create.description,
        author_id=request.user.id,
    )
    return task


@task_router.get("/{task_uuid}", response_model=TaskResponse)
def get_task(
    task_uuid: str,
    task_controller: TaskController = Depends(Factory().get_task_controller),
    assert_access: Callable = Depends(Permissions(TaskPermission.READ)),
) -> TaskResponse:
    task = task_controller.get_by_uuid(task_uuid)

    assert_access(task)
    return task
