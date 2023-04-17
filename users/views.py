from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile, Message
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm
from .utils import searchProfiles, paginateProfiles

# Create your views here.
def loginUser(request):
    page = 'login'
    context = {'page':page}

    if request.user.is_authenticated:
        return redirect('profiles')
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username doesnt exist')

        # Authenticate will take in the username ans password and make sure that the password matches the username provided
        # return either user instance or none, this func will query the database
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # will create a new session in the database and add that session in the browser
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
        else:
            messages.error(request, 'Username or password is incorrect')

    return render(request, 'users/login_register.html', context)

def logoutUser(request):
    logout(request)
    messages.info(request, 'User is successfully logged out')
    return redirect('login')

def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        # Checks if everything is correct and everthing has been manipulated and is correct
        if form.is_valid():
            # We save and we are holding a temperory instance of it, so we provide commit=False, this is done in order for us to modify
            # something, by saving it to a variable and then make username capital or lower case by default 
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'User account was created successfully')
            login(request=request, user=user)
            return redirect('edit')
        else:
            messages.error(request, 'An Error has occured during registration')
        
    context = {'page': page, 'form':form}
    return render(request, 'users/login_register.html', context)


def profiles(request):
    profiles, search_query = searchProfiles(request)

    custom_range, profiles = paginateProfiles(request, profiles, 3)

    context = {'profiles': profiles, 'search_query':search_query, 'custom_range': custom_range}
    return render(request, 'users/profiles.html', context)

def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)

    topSkills = profile.skill_set.exclude(description__exact="")
    otherSkills = profile.skill_set.filter(description="")

    context = {'userProfile': profile, 'topSkills': topSkills, 'otherSkills': otherSkills}
    return render(request, 'users/user_profile.html', context)

# Function based view
@login_required(login_url='login')
def userAccount(request):
    # When a user is logged in we can directly get the user profile and details
    userProfile = request.user.profile

    # skill_set here set is used as a foreign key since skill has a foreign key profile and we can get all the skills for the profile
    # using the set keyword attached to the skill model
    skills = userProfile.skill_set.all()

    context = {'profile':userProfile, 'skills': skills}

    return render(request, 'users/account.html', context)

@login_required(login_url='login')
def editUserAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        # request.FILES is used to process the image updated or added by the user
        # instance is provided because we need to update this particular user and we get it from request.user.profile, logged in user
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()

            return redirect('account')

    context = {'form':form}
    return render(request, 'users/profile_form.html', context)

@login_required(login_url='login')
def createSkill(request):
    profile = request.user.profile
    form = SkillForm()

    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid:
            # Create instance of the save and then update the skill owner with the profile, i.e the current profile will get the skill
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, 'Skill was successfully created and added to your account!!')

            return redirect('account')

    context = {'form': form}
    return render(request, 'users/skill_form.html', context)

@login_required(login_url='login')
def updateSkill(request, pk):
    profile = request.user.profile

    skill = profile.skill_set.get(id=pk)
    # adding instance to skill will prefill the data of the skill for editing purpose
    form = SkillForm(instance=skill)

    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid:
            form.save()
            messages.success(request, 'Skill was successfully updated!!')
            return redirect('account')

    context = {'form': form}
    return render(request, 'users/skill_form.html', context)

@login_required(login_url='login')
def deleteSkill(request, pk):
    profile = request.user.profile

    skill = profile.skill_set.get(id=pk)

    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill was successfully deleted!!')
        return redirect('account')
        
    context = {'object': skill}
    # For route directory templates, just add the html file name
    return render(request, 'delete_objects.html', context)

@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    inbox_message = profile.messages.all()
    unreadCount = inbox_message.filter(is_read=False).count()


    context = {'inbox_messages':inbox_message, 'unreadCount': unreadCount}
    return render(request, 'users/inbox.html', context)

login_required(login_url='login')
def viewMessage(request, pk):
    profile = request.user.profile
    view_message = profile.messages.get(id=pk)
    if view_message.is_read == False:
        view_message.is_read = True
        view_message.save()

    context = {'viewMessage': view_message}
    return render(request, 'users/message.html', context)


def createMessage(request, pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()

    # Check if sender is present
    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email

            message.save()

            messages.success(request, 'Your message was successfully sent')

            return redirect('user_profile', pk=recipient.id)


    context = {'form':form, 'recipient': recipient}
    return render(request, 'users/message_form.html', context)
