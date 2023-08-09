import pandas as pd
from django.shortcuts import render, redirect
from .forms import ExcelUploadForm
from .models import CustomUser, Role
from app.apps.companies.models import Company, Department

def register_users_from_excel(request):
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['file']
            df = pd.read_excel(excel_file)
            print(df.columns)


            for index, row in df.iterrows():
                user = CustomUser(
                    username=row['username'],
                    password=row['password'],
                    first_name=row['first_name'],
                    last_name=row['last_name'],
                    middle_name=row['middle_name'],
                    email=row['email'],
                    mobile=row['mobile'],
                    position=row['position'],
                )

                if 'role' in row:
                    role_name = row['role']
                    if role_name:
                        role, created = Role.objects.get_or_create(name=role_name)
                        user.role = role
                
                department = Department(
                    department_name=row['department_name']
                )

                company = row['company_name']
                if company:
                    company_name, created = Company.objects.get_or_create(
                        company_name=company
                    )
                    department.company_name = company_name

                department_n = row['department_name']
                if department_n:
                    department_name, created = Department.objects.get_or_create(
                        department_name=department
                    )
                    user.company_name=company_name
                    user.department_name = department_name


                user.save()

            return redirect('/admin/users/customuser/')
    else:
        form = ExcelUploadForm()

    return render(request, 'upload_excel.html', {'form': form})
