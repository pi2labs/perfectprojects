from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Skill, Message

# pass the class as an attribute mean we are inheriting all the properties and method of the Usercreation form class
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model= User
        fields = ['first_name', 'email', 'username', 'password1', 'password2']
        labels = {
            'first_name': 'Name'
        }


    def __init__(self, *args, **kwargs) -> None:
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        # for name, field in self.fields.items():
        #     field.widget.attrs.update({'class': 'input'})

        self.fields['first_name'].widget.attrs.update(
            {'class': 'input input--text', 'id':'formInput#text', 'type':'text', 'name':'text', 'placeholder':'e.g. Nagarjun Bagalore'})
        self.fields['email'].widget.attrs.update(
            {'class': 'input input--email', 'id':'formInput#email', 'type':'email', 'name':'email', 'placeholder':'e.g. user@domain.com'})
        self.fields['username'].widget.attrs.update(
            {'class': 'input input--text', 'id':'formInput#text', 'type':'text', 'name':'text', 'placeholder':'e.g. Nagarjunbs'})
        self.fields['password1'].widget.attrs.update(
            {'class': 'input input--password', 'id':'formInput#passowrd', 'type':'password', 'name':'password', 'placeholder':'••••••••'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'input input--password', 'id':'formInput#confirm-passowrd', 'type':'password', 'name':'confirm-password', 'placeholder':'••••••••'})


class ProfileForm(ModelForm):
    class Meta:
        model=Profile
        # fields = '__all__' # using this we can get all the fields in the form by default else we need to specify as array, see above implementation
        fields = ['name', 'email', 'username', 'location', 'short_intro', 'bio', 'profile_image', 'social_github', 
                  'social_twitter', 'social_linkedin', 'social_youtube', 'social_website']
        
    def __init__(self, *args, **kwargs) -> None:
        super(ProfileForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class SkillForm(ModelForm):
    class Meta:
        model=Skill
        fields = '__all__'
        # we can specify exclude to exclude a particular field
        exclude = ['owner']

    def __init__(self, *args, **kwargs) -> None:
        super(SkillForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'email', 'subject', 'body']
    
    def __init__(self, *args, **kwargs) -> None:
        super(MessageForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})