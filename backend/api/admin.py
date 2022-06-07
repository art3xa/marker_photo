from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, UserChangeForm
from .models import *


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')


@admin.register(Classification)
class ClassificationAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'project')


@admin.action(description='Снять блокировку')
def reset_lock(modeladmin, request, queryset):
    queryset.filter(state=Entity.EntityState.LOCKED).update(state=Entity.EntityState.UNANNOTATED)


@admin.register(Entity)
class EntityAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'state', 'assigned_user', 'project')
    actions = [reset_lock]


class StaffChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = Staff


class StaffAdmin(UserAdmin):
    form = StaffChangeForm

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('project', )}),
    )


admin.site.register(Staff, StaffAdmin)
