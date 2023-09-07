from django.shortcuts import render
from django.views.generic import ListView
from django.http import HttpResponse
from .models import Post
from .admin import PostResource


class MainView(ListView):
    template_name = "posts/index.html"
    queryset = Post.objects.all()


def export(request, format):
    posts_resource = PostResource()
    dataset = posts_resource.export()
    if format == "csv":
        data_format = dataset.csv
    else:
        data_format = dataset.xls
    response = HttpResponse(data_format, content_type=f"text/{format}")
    response["Content-Disposition"] = f"attachment; filename=posts.{format}"
    return response
