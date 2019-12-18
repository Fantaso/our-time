from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView,
    CreateView, DeleteView, UpdateView
)

from .forms import DateForm
from .models import Task

TODOS_TASK_LIST_NAMESPACE_URL = 'todos:task-list'


class TaskBaseView:
    model = Task


class TaskList(TaskBaseView, ListView):
    template_name = 'todos/task_list.html'
    context_object_name = 'task_list'


class TaskDetail(TaskBaseView, DetailView):
    template_name = 'todos/task_detail.html'


class TaskCreate(TaskBaseView, CreateView):
    form_class = DateForm
    template_name = 'todos/task_create.html'
    success_url = reverse_lazy(TODOS_TASK_LIST_NAMESPACE_URL)


class TaskUpdate(TaskBaseView, UpdateView):
    template_name = 'todos/task_update.html'
    success_url = reverse_lazy(TODOS_TASK_LIST_NAMESPACE_URL)
    fields = '__all__'


class TaskDelete(TaskBaseView, DeleteView):
    template_name = 'todos/task_delete.html'
    success_url = reverse_lazy(TODOS_TASK_LIST_NAMESPACE_URL)
    context_object_name = 'task'
