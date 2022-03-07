from django.contrib.auth.forms import AuthenticationForm
from django import forms

from attendance.models import Employee, basic_inf
"ログオンフォーム"
class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label   


class FindForm(forms.Form):
    find = forms.CharField(label='Find', required=False)

class EmployeeForm(forms.ModelForm):
    class Meta:
        model =Employee
        fields =["status"]



class InfForm(forms.ModelForm):
    class Meta:
        model =basic_inf
        fields =["transportation_expenses","hourly_wage"]


