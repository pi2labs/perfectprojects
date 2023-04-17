from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Project, Tag
from .forms import ProjectForm, ReviewForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .utils import searchProjects, paginateProjects


def projects(request):
    projects, search_query = searchProjects(request)

    custom_range, projects = paginateProjects(request, projects, 3)
    
    context = {'projects': projects, 'search_query': search_query, 'custom_range': custom_range}
    return render(request, 'projects/projects.html', context)

def singleProject(request, pk):
    projectObj = Project.objects.get(id=pk)

    form = ReviewForm()
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = projectObj
        review.owner = request.user.profile
        review.save()

        projectObj.getVoteCount

        messages.success(request, 'Review is successfully submitted')
        # to refresh the page we just need to redirect to the same page
        return redirect('fetch_project', pk=projectObj.id)


    return render(request, 'projects/single_project.html', {'project': projectObj, 'form': form})

# This decorator make sure that in order to access this page we need to be logged in
@login_required(login_url='login')
def createProject(request):
    # Get the current logged in profile with the user
    profile = request.user.profile

    myform = ProjectForm()

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            # this is done as when we add a new project from my account page then we will  not display new project in account page
            # instead we used to display in the project, so in order to connect both we need to assign project owner the currently
            # being created project, so the project is connected to the owner and it will be displayed in account page
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect('account')

    context = {'form': myform}
    return render(request, 'projects/project_form.html', context)

@login_required(login_url='login')
def updateProject(request, pk):
    profile = request.user.profile

    # Make sure only the owner can update the project and no one else, this is the reason we take all projects based on profile
    project = profile.project_set.get(id=pk)
    myform = ProjectForm(instance=project)

    if request.method == 'POST':
        # Request. files to link user added images to the DB
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('account')

    context = {'form': myform}
    return render(request, 'projects/project_form.html', context)

@login_required(login_url='login')
def deleteProject(request, pk):
    profile = request.user.profile

    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('account')
        
    context = {'object': project}
    # For route directory templates, just add the html file name
    return render(request, 'delete_objects.html', context)


