from django.utils import timezone
from django.http import Http404
from django.views.generic import TemplateView, FormView, RedirectView
from django.core.urlresolvers import reverse_lazy

from .models import Project, NotSetTrelloBoardID, Task
from .forms import ProjectForm, TaskForm


class ProjectIndex(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(ProjectIndex, self).get_context_data(**kwargs)
        context['projects'] = Project.objects.all()
        return context


class ProjectDetails(TemplateView):
    template_name = 'details.html'

    def get_context_data(self, **kwargs):
        context = super(ProjectDetails, self).get_context_data(**kwargs)
        project = Project.objects.get(id=kwargs['id'])
        context['project'] = project
        context['tasks'] = project.tasks.all()
        return context


class ProjectCreate(FormView):
    template_name = 'create.html'
    form_class = ProjectForm
    success_url = reverse_lazy('projects_manager:index')

    def form_valid(self, form):
        form.save()
        return super(ProjectCreate, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ProjectCreate, self).get_context_data(**kwargs)
        context['header'] = "Add new project"
        return context


class SyncWithTrello(RedirectView):
    permanent = False
    query_string = True,

    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy('projects_manager:details', kwargs={
            "id": kwargs['id']
        })

    def dispatch(self, request, *args, **kwargs):
        try:
            bms = Project.objects.get(id=kwargs['id'])
            bms.sync_trello_cards()
        except (Project.DoesNotExist, NotSetTrelloBoardID):
            raise Http404

        return super(SyncWithTrello, self).dispatch(request, *args, **kwargs)


class TaskDetails(TemplateView):
    template_name = 'task_details.html'

    def get_context_data(self, **kwargs):
        context = super(TaskDetails, self).get_context_data(**kwargs)
        context['task'] = Task.objects.get(id=kwargs['id'])
        return context


class TaskCreate(FormView):
    template_name = 'create.html'
    form_class = TaskForm
    success_url = reverse_lazy('projects_manager:index')

    def get_context_data(self, **kwargs):
        context = super(TaskCreate, self).get_context_data(**kwargs)
        context['header'] = "Add new task"
        return context

    def form_valid(self, form):
        form.save()
        return super(TaskCreate, self).form_valid(form)


class TaskTimerView(RedirectView):
    permanent = False
    query_string = True
    task = None

    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy('projects_manager:details', kwargs={
            "id": self.task.project.id
        })

    def dispatch(self, request, *args, **kwargs):
        self.task = Task.objects.get(id=kwargs['id'])
        self.set_task_time()
        return super(TaskTimerView, self).dispatch(request, *args, **kwargs)

    def set_task_time(self):
        raise NotImplementedError


class TaskStartTimer(TaskTimerView):
    def set_task_time(self):
        self.task.start_time = timezone.now()
        self.task.save()


class TaskStopTimer(TaskTimerView):
    def set_task_time(self):
        time_stop = timezone.now()
        delta = time_stop - self.task.start_time
        self.task.time += int(delta.total_seconds())
        self.task.start_time = None
        self.task.save()
