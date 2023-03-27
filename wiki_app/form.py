from django import forms

class SearchForm(forms.Form):
    kwd = forms.CharField(max_length=100, label='キーワード')