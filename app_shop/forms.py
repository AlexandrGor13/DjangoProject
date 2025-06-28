from django import forms


class SetCaregoryForm(forms.Form):
    category = forms.CharField()
