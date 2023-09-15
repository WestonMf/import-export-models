
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from posts.views import MainView, export

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", MainView.as_view(), name="index"),
    path('<str:format>/export', export, name="export"),
    path('books/', include('books.urls')),
    path("unicorn/", include("django_unicorn.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
