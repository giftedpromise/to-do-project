from django.shortcuts import render, redirect
from .models import Task
from .forms import TaskForm

def task_list(request):
    # Handle form submission for creating or updating a task
    if request.method == 'POST':
        if 'save_task' in request.POST:  # Adding a new task
            form = TaskForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('task_list')
        elif 'update_task' in request.POST:  # Updating an existing task
            task_id = request.POST.get('task_id')
            try:
                task = Task.objects.get(id=task_id)
                form = TaskForm(request.POST, instance=task)
                if form.is_valid():
                    form.save()
                    return redirect('task_list')
            except Task.DoesNotExist:
                pass
        elif 'toggle_task' in request.POST:  # Toggling task completion
            task_id = request.POST.get('task_id')
            try:
                task = Task.objects.get(id=task_id)
                task.completed = not task.completed
                task.save()
            except Task.DoesNotExist:
                pass
            return redirect('task_list')
        elif 'delete_task' in request.POST:  # Deleting a task
            task_id = request.POST.get('task_id')
            try:
                task = Task.objects.get(id=task_id)
                task.delete()
            except Task.DoesNotExist:
                pass
            return redirect('task_list')

    # For GET requests or failed POSTs, show the form and task list
    edit_task = None
    if request.GET.get('edit_task'):
        try:
            edit_task = Task.objects.get(id=request.GET.get('edit_task'))
            form = TaskForm(instance=edit_task)
        except Task.DoesNotExist:
            form = TaskForm()
    else:
        form = TaskForm()

    tasks = Task.objects.all().order_by('-created_at')
    return render(request, 'tasks/task_list.html', {
        'tasks': tasks,
        'form': form,
        'edit_task': edit_task
    })