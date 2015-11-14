from django.forms import ModelForm
from .models import Project, Task


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = [
            'name',
            'description',
            'start_date',
            'finish_date',
            'sum_hours_work',
            'link_repository'
        ]

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'time', 'project']
