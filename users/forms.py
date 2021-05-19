from django import forms
from django.contrib.auth import get_user_model
from crispy_forms.helper import FormHelper
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm


class LoginForm(AuthenticationForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_id = 'login-form'

class CreateAccountForm(SetPasswordForm):
    email = forms.EmailField(max_length=250, required=True, widget=forms.EmailInput())

    def __init__(self,*args,**kwargs):
        super().__init__(self,*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_id = 'set-password-form'

    def clean(self):
        cleaned_data = super().clean()
        email=cleaned_data.get('email')
        UserModel=get_user_model()

        if not UserModel.objects.filter(email=email).exists():
            print("email doesn't exist")
            msg="We don't have record of a purchase under that email. Please enter the email used at the time of purchase."
            self.add_error('email',msg)

        elif UserModel.objects.get(email=email).has_usable_password():
            msg="You already set your password. Please login to view or re-download your purchase."
            self.add_error('email',msg)
        return cleaned_data
