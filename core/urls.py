
from django.contrib import admin
from django.urls import path
from posts.views import MainView, export

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", MainView.as_view(), name="index"),
    path('<str:format>/export', export, name="export"),
]
