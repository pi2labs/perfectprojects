from .models import Profile, Skill
from django.db.models import Q # Q lookup for searching with OR , as filter used AND gate
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def paginateProfiles(request, profiles, results):
    page = request.GET.get('page')
    paginator = Paginator(profiles, results)

    # Try the first page
    try:
        profiles = paginator.page(page)
    # by default the first page is provided
    except PageNotAnInteger:
        page = 1
        profiles = paginator.page(page)
    # When a page number above the expected number of pages are provided, we by default set to the last page
    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page)

    # This is like a rolling window when we have 100 pages, we only show 4 pages in the window with prev and next button
    leftIndex = (int(page) - 4)
    if leftIndex < 1:
        leftIndex = 1
    
    rightIndex = (int(page) + 5)
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1

    custom_range = range(leftIndex, rightIndex)

    return custom_range, profiles


def searchProfiles(request):
    search_query = ''

    # Q lookup
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    skills = Skill.objects.filter(name__icontains=search_query)

    # Q lookup because OR operator is performed, use | to search for either of the 2 values
    profiles = Profile.objects.distinct().filter(
        Q(name__icontains=search_query) | 
        Q(short_intro__icontains=search_query) |
        # Does a profile have ths skill that is listed in the search_query, if so then return the profile
        Q(skill__in=skills)
    )

    return profiles, search_query