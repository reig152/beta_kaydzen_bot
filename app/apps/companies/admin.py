from django.contrib import admin
from .models import Company, Department

from app.apps.users.models import CustomUser

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'display_users']

    @admin.display(description="Сотрудники компании")
    def display_users(self, obj):
        users = CustomUser.objects.filter(company_name=obj)
        user_list = ', '.join([user.username for user in users])
        return user_list


@admin.register(Department)
class CompanyAdmin(admin.ModelAdmin):
    list_display = [
        'company_name',
        'department_name'
    ]
