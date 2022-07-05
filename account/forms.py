from account.models import Profile
from django import forms


class ProfileForm(forms.ModelForm):
    uuid = forms.UUIDField(disabled=True)

    class Meta:
        model = Profile
        fields = ["uuid", "server_address"]
