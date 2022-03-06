from django import forms

from account.models import Profile


class ProfileForm(forms.ModelForm):
    uuid = forms.UUIDField(disabled=True)

    class Meta:
        model = Profile
        fields = ["uuid", "server_address"]
