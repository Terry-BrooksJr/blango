from django.contrib import admin
from blog.models import Tag, Post
from django.utils.translation import ngettext
from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.db.models.query import QuerySet

# SECTION - Admin Models Defintions
class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = 'created_at'
    list_display = ['title', 'author', 'created_at', 'published_at']
    actions = ['make_published']
    
    # SECTION - Custom Admin Actions
    @admin.action(description='Mark selected posts as published')
    def make_published(self, request: HttpRequest, queryset: QuerySet[Post]) -> None:
        if queryset.exists():
            updated = queryset.update(status='P')
            self.message_user(request, ngettext(
                '%d post was successfully marked as published.',
                '%d posts were successfully marked as published.',
                updated,
            ) % updated, messages.SUCCESS)
        else:
            self.message_user(request, "No posts were selected.", messages.WARNING)

class TagAdmin(admin.ModelAdmin):
    actions = None


    
# SECTION - Model and Model Admin Registration 
admin.site.register(model_or_iterable=Tag, admin_class=TagAdmin)
admin.site.register(model_or_iterable=Post, admin_class=PostAdmin)