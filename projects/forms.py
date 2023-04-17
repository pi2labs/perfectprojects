from django.forms import ModelForm
from django import forms
from .models import Project, Review

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'featured_image', 'description', 'demo_link', 'source_link', 'tags']
        widgets = {
            'tags': forms.CheckboxSelectMultiple
        }

    # Update the original class and so use the same class inside super and then select the field type to update and enter widgets attributes and
    # update the class type as input for title field , basic idea is to overwrite the field type
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

        # self.fields['title'].widget.attrs.update({'class': 'input', 'placeholder': 'Add Title'})
        # self.fields['description'].widget.attrs.update({'class': 'text', 'placeholder': 'Enter Description'})


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['value', 'body']
        # labels = {
        #     'value': 'Place your vote',
        #     'body': 'Add a comment with your vote'
        # }
    
    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)
        self.fields['value'].label = 'Place your vote'
        self.fields['body'].label = 'Add a comment with your vote'

        self.fields['value'].widget.attrs.update({'class': 'input'})
        self.fields['body'].widget.attrs.update({'class': 'input', 'placeholder': 'Add a comment with your vote'})
        # for name, field in self.fields.items():
        #     field.widget.attrs.update({'class': 'input'})