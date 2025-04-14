from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("", views.landing_page, name="landing_page"),
    path("dashboard/", views.task_list, name="task_list"),
    path("add/", views.add_task, name="add_task"),
    path("complete/<int:task_id>/", views.complete_task, name="complete_task"),
    path("delete/<int:task_id>/", views.delete_task, name="delete_task"),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("edit/<int:task_id>/", views.edit_task, name="edit_task"),
    path("profile/", views.profile_view, name="profile"),
    path(
        "password_change/",
        auth_views.PasswordChangeView.as_view(
            template_name="registration/password_change_form.html",
            success_url="/password_change_done/",
        ),
        name="password_change",
    ),
    path(
        "password_change_done/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="registration/password_change_done.html"
        ),
        name="password_change_done",
    ),
]
