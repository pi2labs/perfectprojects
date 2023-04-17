from .models import Project, Tag
from django.db.models import Q # Q lookup for searching with OR , as filter used AND gate
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def paginateProjects(request, projects, results):
    page = request.GET.get('page')
    paginator = Paginator(projects, results)

    # Try the first page
    try:
        projects = paginator.page(page)
    # by default the first page is provided
    except PageNotAnInteger:
        page = 1
        projects = paginator.page(page)
    # When a page number above the expected number of pages are provided, we by default set to the last page
    except EmptyPage:
        page = paginator.num_pages
        projects = paginator.page(page)

    # This is like a rolling window when we have 100 pages, we only show 4 pages in the window with prev and next button
    leftIndex = (int(page) - 4)
    if leftIndex < 1:
        leftIndex = 1
    
    rightIndex = (int(page) + 5)
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)

    return custom_range, projects


def searchProjects(request):
    search_query = ''
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    tags = Tag.objects.filter(name__icontains=search_query)


    projects = Project.objects.distinct().filter(
        Q(title__icontains=search_query) |
        # select owner and go into the parent by adding owner__name
        Q(owner__name__icontains=search_query) |
        # since tag is many to many field tags = models.ManyToManyField('Tag', blank=True) so we need to use plural like tags for the model 
        # name
        Q(tags__in=tags)
    )

    return projects, search_query