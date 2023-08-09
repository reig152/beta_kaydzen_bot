from django import forms

class ExcelUploadForm(forms.Form):
    file = forms.FileField(
        label='Выберите Excel-файл',
        help_text='(допустимые форматы: .xls, .xlsx)'
    )
