from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text', 'point']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
        }