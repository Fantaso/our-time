from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from .models import Task


class TaskList(ListView):
    model = Task
    template_name = 'todo/task_list.html'
    context_object_name = 'task_list'


class TaskDetail(DetailView):
    model = Task
    template_name = 'todo/task_detail.html'


class TaskCreate(CreateView):
    model = Task
    template_name = 'todo/task_create.html'
    success_url = reverse_lazy('todos:task-list')
    fields = '__all__'


class TaskUpdate(UpdateView):
    model = Task
    template_name = 'todo/task_update.html'
    success_url = reverse_lazy('todos:task-list')
    fields = '__all__'

class TaskDelete(DeleteView):
    model = Task
    template_name = 'todo/task_delete.html'
    success_url = reverse_lazy('todos:task-list')
    context_object_name = 'task'
