from django import forms

class BuscadorForm(forms.Form):
    query = forms.CharField(label='', required=True, widget=forms.Textarea(
        attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese texto.',
        }))
