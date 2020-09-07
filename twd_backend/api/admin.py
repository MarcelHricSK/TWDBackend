from django.contrib import admin
import api.models as Models

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    pass

admin.site.register(Models.User, UserAdmin)
admin.site.register(Models.Post, UserAdmin)
admin.site.register(Models.AuthToken, UserAdmin)
admin.site.register(Models.Tag, UserAdmin)
admin.site.register(Models.Category, UserAdmin)