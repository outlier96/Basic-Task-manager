from django.shortcuts import render, redirect
from .models import Task
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from datetime import date
from django.contrib import messages
from .forms import ProfileUpdateForm


@login_required
def task_list(request):
    filter_type = request.GET.get("filter", "")
    tasks = Task.objects.filter(user=request.user)

    if filter_type == "pending":
        tasks = tasks.filter(completed=False)
    elif filter_type == "completed":
        tasks = tasks.filter(completed=True)
    elif filter_type == "high":
        tasks = tasks.filter(priority="high")
    elif filter_type == "overdue":
        tasks = tasks.filter(completed=False, due_date__lt=date.today())

    completed_tasks = tasks.filter(completed=True).count()
    pending_tasks = tasks.filter(completed=False).count()
    high_priority = tasks.filter(priority="high").count()

    context = {
        "tasks": tasks.order_by("-created_at"),
        "completed_count": completed_tasks,
        "pending_count": pending_tasks,
        "high_priority_count": high_priority,
        "today": date.today(),
    }
    return render(request, "tasks/task_list.html", context)


@login_required
def add_task(request):
    if request.method == "POST":
        title = request.POST["title"]
        priority = request.POST["Priority"]
        Task.objects.create(user=request.user, title=title)

        return redirect("task_list")
    return render(request, "tasks/add_task.html")


@login_required
def complete_task(request, task_id):
    task = Task.objects.get(id=task_id, user=request.user)
    task.completed = True
    task.save()
    return redirect("task_list")


@login_required
def delete_task(request, task_id):
    task = Task.objects.get(id=task_id, user=request.user)
    task.delete()
    return redirect("task_list")


def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("task_list")
    else:
        form = UserCreationForm()
    return render(request, "tasks/register.html", {"form": form})


@login_required
def edit_task(request, task_id):
    task = Task.objects.get(id=task_id, user=request.user)

    if request.method == "POST":
        task.title = request.POST["title"]
        task.due_date = request.POST["due_date"] or None
        task.priority = request.POST["priority"]
        task.save()
        return redirect("task_list")

    return render(request, "tasks/edit_task.html", {"task": task})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("task_list")
    else:
        form = AuthenticationForm()
    return render(request, "tasks/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")


def landing_page(request):
    if request.user.is_authenticated:
        return redirect("task_list")
    return render(request, "tasks/landing.html")


@login_required
def profile_view(request):
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("profile")
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, "tasks/profile.html", {"form": form})
