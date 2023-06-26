from django.contrib import admin
from django.urls import path
from django.urls import path
from rest_framework.routers import SimpleRouter

from tasks.apiViews import TaskViewSet, TaskHistoryViewSet
from django.contrib.auth.views import LogoutView
from tasks.views import (
    delete_task,
    redirect_to_login,
    report_view,
    delete_all,
    GenericTaskVew,
    GenericTaskCreateView,
    GenericTaskUpdateView,
    GenericTaskDeleteView,
    UserCreateView,
    UserLoginView,
    GenericTaskDetailView,
    GenericCompletedTasksView,
)

router = SimpleRouter()

router.register("api/task", TaskViewSet)
router.register("api/task_history", TaskHistoryViewSet)

urlpatterns = [
    path("", redirect_to_login),
    path("admin/", admin.site.urls),
    path("signup", UserCreateView.as_view()),
    path("login", UserLoginView.as_view()),
    path("logout", LogoutView.as_view()),
    # Add all your views here
    path("tasks/", GenericTaskVew.as_view()),
    path("create_task", GenericTaskCreateView.as_view()),
    path("update_task/<pk>", GenericTaskUpdateView.as_view()),
    path("delete_task/<pk>", GenericTaskDeleteView.as_view()),
    path("delete-task/<int:task_id>/", delete_task),
    path("task/<pk>", GenericTaskDetailView.as_view()),
    path("completed_tasks/", GenericCompletedTasksView.as_view()),
    path("all_tasks/", report_view),
    path("delete_all/", delete_all),
] + router.urls
