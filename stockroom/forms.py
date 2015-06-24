from django import forms

class CommentForm(forms.Form):
    user_comment = forms.CharField( label='', required=True, widget=forms.TextInput)