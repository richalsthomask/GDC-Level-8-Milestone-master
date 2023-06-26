from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic.list import ListView
from tasks.models import Task, TaskHistory
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.forms import ModelForm, ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin


def priority_leeway_creater(priority):
    if Task.objects.filter(priority=priority).exists():
        priority_leeway_creater(priority + 1)
        Task.objects.filter(priority=priority).update(priority=priority + 1)


class AuthorisedTasks(LoginRequiredMixin):
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user, deleted=False)


class UserCreateView(CreateView):
    form_class = UserCreationForm
    template_name = "signup.html"
    success_url = "/login"


class UserLoginView(LoginView):
    template_name = "signin.html"
    success_url = "/tasks/"


class TaskCreateForm(ModelForm):
    def clean_title(self):
        title = self.cleaned_data["title"]
        if len(title) < 5:
            raise ValidationError("Title must be greater than 5 characters")
        return title

    def clean_priority(self):
        priority = self.cleaned_data["priority"]
        priority_leeway_creater(priority)
        return priority

    class Meta:
        model = Task
        fields = ["title", "description", "priority", "status"]


class GenericTaskCreateView(CreateView, LoginRequiredMixin):
    form_class = TaskCreateForm
    template_name = "create_task.html"
    success_url = "/all_tasks"

    def form_valid(self, form):
        self.object = form.save()
        self.object.user = self.request.user
        self.object.save()
        task_history_object = TaskHistory(
            task=self.object,
            old_status="CREATED",
            new_status=self.object.status,
            user=self.request.user,
        )
        task_history_object.save()
        return HttpResponseRedirect(self.get_success_url())


class GenericTaskUpdateView(UpdateView, AuthorisedTasks):
    model = Task
    form_class = TaskCreateForm
    template_name = "update_task.html"
    success_url = "/all_tasks"


class GenericTaskDeleteView(DeleteView, AuthorisedTasks):
    model = Task
    template_name = "delete_task.html"
    success_url = "/all_tasks"


class GenericTaskVew(ListView, LoginRequiredMixin):
    template_name = "tasks.html"
    context_object_name = "pending_tasks"
    paginate_by = 5

    def get_queryset(self):
        search = self.request.GET.get("search")
        tasks = Task.objects.filter(
            deleted=False, status="PENDING", user=self.request.user
        ).order_by("priority")
        if search:
            tasks = tasks.filter(title__icontains=search)
        return tasks


class GenericTaskDetailView(DetailView, AuthorisedTasks):
    model = Task
    template_name = "task_detail.html"


class GenericCompletedTasksView(ListView, AuthorisedTasks):
    template_name = "completed_tasks.html"
    context_object_name = "completed_tasks"
    paginate_by = 10

    def get_queryset(self):
        search = self.request.GET.get("search")
        tasks = Task.objects.filter(
            deleted=False, status="COMPLETED", user=self.request.user
        )
        if search:
            tasks = tasks.filter(title__icontains=search)
        return tasks


def report_view(request):
    return render(
        request,
        "report_view.html",
        {
            "tasks": Task.objects.filter(
                deleted=False,
            ).order_by("priority"),
            "tasks_completed_line": str(
                Task.objects.filter(deleted=False, status="COMPLETED").count()
            )
            + " out of "
            + str(Task.objects.filter(deleted=False).count()),
        },
    )


def delete_all(request):
    Task.objects.all().delete()
    return HttpResponseRedirect("/tasks/")


def redirect_to_login(request):
    return HttpResponseRedirect("/login")


def delete_task(request, task_id):
    Task.objects.filter(id=task_id).update(deleted=True)
    return HttpResponseRedirect("/tasks/")
