from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Post, Portfolio


class UserAdmin(UserAdmin):
    model = User

    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ('avatar', 'facebook', 'twitter', 'github', 'instagram', 'linkedin', 'description',)}),
    )

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'resume', 'user',)
    readonly_fields = ('slug',)
    

class PortfolioAdmin(admin.ModelAdmin):
    list_display = ('skills', 'duration', 'cost', 'user', 'image',)


admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Portfolio)

