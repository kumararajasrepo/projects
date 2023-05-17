from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Task
from .forms import TaskForm


class Tasks(LoginRequiredMixin, ListView):
    login_url = "url-signin"
    model = Task
    form_class = TaskForm
    template_name = "task_list/tasks.html"
    context_object_name = "tasks"

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)


class AddTask(LoginRequiredMixin, CreateView):
    login_url = "url-signin"
    model = Task
    form_class = TaskForm
    template_name = "task_list/task.html"

    def get_success_url(self) -> str:
        return reverse_lazy("url-tasks")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class UpdateTask(LoginRequiredMixin, UpdateView):
    login_url = "url-signin"
    model = Task
    form_class = TaskForm
    template_name = "task_list/task.html"

    def get_object(self) -> Task:
        pk = self.kwargs.get("pk")
        return get_object_or_404(Task, pk=pk)

    def get_success_url(self) -> str:
        return reverse_lazy("url-tasks")


@login_required(login_url="url-signin")
def complete_task(request: HttpRequest, pk, is_completed) -> HttpResponse:
    task = Task.objects.get(pk=pk)
    if task is not None:
        task.is_completed = is_completed
        task.save()
    return redirect("url-tasks")


class DeleteTask(LoginRequiredMixin, DeleteView):
    login_url = "url-signin"
    model = Task

    def get_object(self) -> Task:
        pk = self.kwargs.get("pk")
        return get_object_or_404(Task, pk=pk)

    def get_success_url(self) -> str:
        pk = self.kwargs.get("pk")
        return reverse("url-tasks")


@login_required(login_url="url-signin")
def delete_task(request: HttpRequest, pk) -> HttpResponse:
    task = Task.objects.get(pk=pk)
    if task is not None:
        task.delete()
    return redirect("url-tasks")


@login_required(login_url="url-signin")
def confirm_delete_tasks(request: HttpRequest) -> HttpResponse:
    return render(request, "task_list/tasks_confirm_delete.html")


@login_required(login_url="url-signin")
def delete_tasks(request: HttpRequest) -> HttpResponse:
    Task.objects.filter(user=request.user).delete()
    return redirect("url-tasks")
