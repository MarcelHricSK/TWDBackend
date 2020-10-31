from django.contrib import admin
import api.models as Models

# Register your models here.
class TokenInline(admin.StackedInline):
    model = Models.AuthToken

class PostsInline(admin.StackedInline):
    model = Models.Post
    extra = 1

class BaseAdmin(admin.ModelAdmin):
    pass

class UserAdmin(admin.ModelAdmin):
    sortable_by = ["id", "created_at", "username"]
    readonly_fields = ["created_at"]
    inlines = [TokenInline, PostsInline]

admin.site.register(Models.User, UserAdmin)
admin.site.register(Models.Post, BaseAdmin)
admin.site.register(Models.AuthToken, BaseAdmin)
admin.site.register(Models.Tag, BaseAdmin)
admin.site.register(Models.Category, BaseAdmin)
admin.site.register(Models.Comment, BaseAdmin)
