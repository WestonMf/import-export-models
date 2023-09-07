from django.contrib import admin
from .models import Post
from import_export import resources
from import_export.admin import ExportActionMixin
from import_export.fields import Field


class PostResource(resources.ModelResource):
    author = Field()
    liked = Field()
    created = Field()

    class Meta:
        model = Post
        fields = ("id", "author", "body", "liked", "created")

    def dehydrate_author(self, obj):
        return str(obj.author.username)

    def dehydrate_liked(self, obj):
        data = [d.username for d in obj.liked.all()]
        users_liked = ", ".join(data)
        return users_liked

    def dehydrate_created(self, obj):
        return obj.created.strftime('%d-%m-%Y')


class PostAdmin(ExportActionMixin, admin.ModelAdmin):
    resource_class = PostResource


admin.site.register(Post, PostAdmin)
