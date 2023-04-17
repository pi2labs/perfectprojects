from django.db import models
import uuid
from users.models import Profile

# Create your models here.

class Project(models.Model):
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    featured_image = models.ImageField(null=True, blank=True, default="default.jpg")
    demo_link = models.CharField(max_length=2000, null=True, blank=True)
    source_link = models.CharField(max_length=2000, null=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True)
    vote_total = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio = models.IntegerField(default=0, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(unique=True, primary_key=True, editable=False, default=uuid.uuid4)


    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering = ['-vote_ratio', '-vote_total', 'title']
    
    @property
    def reviewers(self):
        # get all the owners id by using the values_list not only the owner review, converting to a true list using flat (just like)
        # flatting to an array from an object
        querySet = self.review_set.all().values_list('owner__id', flat=True)
        return querySet

    # to make this as property just add a decorator and to make ratio dynamic just add a new method
    @property
    def getVoteCount(self):
        reviews = self.review_set.all()
        upVotes = reviews.filter(value='up').count()
        totalVotes = reviews.count()

        ratio = (upVotes / totalVotes) * 100 
        self.vote_total = totalVotes
        self.vote_ratio = ratio
        self.save()


class Review(models.Model):
    VOTE_TYPE = (('up', 'Up Vote'), ('down', 'Down Vote'))
    # One to many relationship
    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    value = models.CharField(max_length=2000, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(unique=True, primary_key=True, editable=False, default=uuid.uuid4)

    # Make sure that only one comment is added per project
    class Meta:
        unique_together=[['owner', 'project']]

    def __str__(self) -> str:
        return self.value

class Tag(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(unique=True, primary_key=True, editable=False, default=uuid.uuid4)

    def __str__(self) -> str:
        return self.name