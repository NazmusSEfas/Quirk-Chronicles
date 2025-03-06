from django import forms
from django.forms import modelformset_factory#ask gpt what this is 
from .models import Paragraph, Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title','summery']
        widgets = {
            'summery':forms.Textarea(attrs={

                'rows': 1,
                'cols': 20,
                'id':'paragraph-textarea'

            })
        }

class ParagraphForm(forms.ModelForm):
    class Meta:
        model = Paragraph
        fields = ['content']


ParagraphFormSet = modelformset_factory(Paragraph, form=ParagraphForm, extra=1)#as what is