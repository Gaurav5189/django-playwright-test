from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import DemoItem


class DemoLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {"data-testid": "login-username", "autocomplete": "username"}
        )
        self.fields["password"].widget.attrs.update(
            {"data-testid": "login-password", "autocomplete": "current-password"}
        )


class DemoItemForm(forms.ModelForm):
    class Meta:
        model = DemoItem
        fields = ["title", "notes"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "data-testid": "item-title",
                    "autocomplete": "off",
                }
            ),
            "notes": forms.Textarea(
                attrs={
                    "rows": 3,
                    "data-testid": "item-notes",
                }
            ),
        }


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"data-testid": "contact-name"}),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"data-testid": "contact-email"}),
    )
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={"rows": 4, "data-testid": "contact-message"}
        ),
    )
