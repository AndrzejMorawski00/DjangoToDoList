from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ToDo
from django.utils.text import slugify
# Create your views here.

def tasks_left(task_query):
    return len(list(task_query)) - len(list(task_query.filter(task_done = True)))

def index(request):
    if request.user.is_authenticated:
        task_query = ToDo.objects.filter(author=request.user)
        print(1)
        return render(request, 'todo/todo.html', {"tasks": list(task_query), "tasks_left": tasks_left(task_query)})
    return render(request, 'todo/todo.html',{})

def add_new(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            task_name = request.POST['task_name']
            task_details = request.POST['task_details']
            task_important = True if request.POST.get(
                'task_important') == 'on' else False
            task_deadline = None if len(request.POST.get(
                'task_deadline')) == 0 else request.POST.get('task_deadline')
            new_todo = ToDo(author=request.user, task_name=task_name, task_details=task_details,
                            task_important=task_important, task_deadline=task_deadline)
            new_todo.save()
            new_todo.task_slug = slugify(
                f"{new_todo.task_name} {new_todo.task_id}")
            new_todo.save()

            return redirect('todo:home-view')
        else:
            return render(request, "todo/new-todo.html", {})
    else:
        return redirect("todo:home-view")


def edit_task(request, task_slug):
    if request.user.is_authenticated:
        if request.method == "POST":
            task_name = request.POST['task_name']
            task_details = request.POST['task_details']
            task_important = True if request.POST.get(
                'task_important') == 'on' else False
            task_done = True if request.POST.get(
                'task_done') == 'on' else False
            task_deadline = None if len(request.POST.get(
                'task_deadline')) == 0 else request.POST.get('task_deadline')

            todo = list(ToDo.objects.filter(
                task_slug=task_slug).filter(author=request.user))[0]
            todo.task_name = task_name
            todo.task_details = task_details
            todo.task_important = task_important
            todo.task_done = task_done
            todo.task_deadline = task_deadline
            todo.save()

            return redirect("todo:home-view")
        else:
            task = list(ToDo.objects.filter(
                task_slug=task_slug).filter(author=request.user))[0]
            return render(request, "todo/edit-todo.html", {'task': task,
                                                           "date": str(task.task_deadline)})
    else:
        return redirect("todo:home-view")


def task_operation(request, task_slug, operation):
    if request.user.is_authenticated:
        task = list(ToDo.objects.filter(
        author=request.user).filter(task_slug=task_slug))[0]
        if operation == 'switch-done':
            task.task_done = not task.task_done
        elif operation == 'switch-details':
            task.task_expand = not task.task_expand
        elif operation == 'delete':
            task.delete()
            return redirect("todo:home-view")
        task.save()
        return redirect("todo:home-view")
    else:
        return redirect("todo:home-view")

def task_sorting(request, order):
    if request.user.is_authenticated:
        task_query = ToDo.objects.filter(author = request.user)
        result_tasks = []
        if order == 'important':
            result_tasks = task_query.order_by('-task_important')
        elif order == 'done':
            result_tasks = task_query.order_by('-task_done')
        elif order == 'deadline':
            tasks_none = list(task_query.filter(task_deadline = None))
            tasks_date = list(task_query.exclude(task_deadline=None).order_by("task_deadline"))
            result_tasks = tasks_date + tasks_none
        else:
            return redirect("todo:home-view")
        return render(request, "todo/todo.html", {"tasks": result_tasks, "tasks_left": tasks_left(task_query)})
    return redirect("todo:home-view")

