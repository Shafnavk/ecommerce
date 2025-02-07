from django import forms
from .models import Account

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(
    widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Password'
    })
)
    confirm_password = forms.CharField(
    widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password'
    })
)
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter last Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter E mail address'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter phone number'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            self.add_error('confirm_password', "Passwords don't match.")

        return cleaned_data
class SetNewPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput(), label="New Password", min_length=8)
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label="Confirm Password", min_length=8)

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError("Passwords do not match")