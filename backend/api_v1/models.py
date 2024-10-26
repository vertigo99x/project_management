from django.db import models
from accounts.models import User
from django.utils import timezone
import uuid 



status = [
    ('done', 'done'),
    ('in_progress', 'in_progress'),
    ('abandoned', 'abandoned'),
    ('cancelled', 'cancelled'),
]

priority = [
    ('low', 'low'),
    ('mid','mid'),
    ('high', 'high'),
]

class Project(models.Model):
    uuid=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    project_name = models.CharField(max_length=127, null=False, blank=False)
    project_description = models.TextField(null=False, blank=False)
    status = models.CharField(blank=True, null=True, choices=status, max_length=20)
    priority = models.CharField(blank=True, null=True, choices=priority, max_length=20)
    #assigned_to = models.ManyToManyField(User, related_name="project_assign_list", blank=True, null=True) # another angle in the implementation for bulk project allocation. 
    assigned_to = models.ForeignKey(User, related_name="assigned_to",  on_delete=models.DO_NOTHING, blank=True, null=True)
    created_by = models.ForeignKey(User, related_name="created_by", on_delete=models.DO_NOTHING)
    date_created = models.DateTimeField(default=timezone.now)
    

    def __str__(self) -> str:
        return f"{self.created_by.email} -> {self.project_name}"


    class Meta:
        ordering = ('-date_created',)
        


class Activities(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=150, blank=True, null=True)
    status = models.CharField(max_length=25, choices=[
                                                      ('primary','primary'),
                                                      ('pending','pending'),
                                                      ('success','success'),
                                                      ('cancelled','cancelled'),
                                                      ], default='primary')
    
    date_added = models.DateTimeField(auto_now_add=True)
    
    
    class Meta:
        ordering = ('-date_added',)