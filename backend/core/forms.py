from django import forms

from core.models import SourceLink


class SourceLinkForm(forms.ModelForm):
    class Meta:
        model = SourceLink
        fields = ['source_link', 'forward_link', 'session']


