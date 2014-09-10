from django import forms


class BlogPostForm(forms.Form):
	title = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
	content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))