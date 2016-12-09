from django import forms

class NameForm(forms.Form):
    searchItem = forms.CharField(label='Items to search for', max_length=100)