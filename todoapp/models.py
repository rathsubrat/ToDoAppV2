from django.db import models
from django.contrib.auth.models import User,Group
from django.db.models import Count, JSONField
from datetime import datetime
from django.core.exceptions import ValidationError
# Create your models here.

class Card(models.Model):
    card_name = models.CharField(max_length=30)
    def __str__(self):
        return self.card_name

class Projects(models.Model):
    id = models.AutoField(primary_key=True)  
    name = models.CharField(max_length=255)
    deadline = models.DateField()
    team = models.ManyToManyField(User, related_name='project')
    # team = models.CharField(max_length=255)  
    # status = models.CharField(max_length=255)  
    status = models.ForeignKey(Card, on_delete=models.CASCADE,default = "")
    manager = models.CharField(max_length=255, default="Default Manager")
    project_wallet = models.IntegerField()
    ETA = JSONField(default=list, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Check if done_date has changed
        if self.pk is not None:
            orig = Projects.objects.get(pk=self.pk)
            if orig.deadline != self.deadline:
                if self.ETA is None:
                    self.ETA = []
                # Append the new done_date as a string
                self.ETA.append(self.deadline.strftime("%Y-%m-%d"))
        super(Projects, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
class ProgressDetail(models.Model):
    date = models.DateField(auto_now_add=True)
    username = models.CharField(max_length=150)
    task_name = models.CharField(max_length=255)
    progress_percentage = models.FloatField()

    def __str__(self):
        return f"{self.date} - {self.username} - {self.task_name} - {self.progress_percentage}%"
    
    
class Task(models.Model):
    taskName = models.CharField(max_length=255)
    taskStatus = models.ForeignKey(Card, on_delete=models.CASCADE)
    assignedTo = models.ManyToManyField(User, related_name='tasks',blank=True)
    assigned_groups = models.ManyToManyField(Group, related_name='group_tasks',blank=True)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE,null=True)
    description = models.CharField(max_length=100,null=True,blank=True)
    startdate = models.DateField(null=True, blank=True)
    enddate = models.DateField(null=True, blank=True)
    deadline = models.DateField(null=True, blank=True)
    file = models.FileField(max_length=100, upload_to="media/", null=True, blank=True)
    Priority_High = 'high'
    Priority_Medium = 'medium'
    Priority_Low = 'low'

    MY_CHOICES = [
        (Priority_High, 'high'),
        (Priority_Medium, 'medium'),
        (Priority_Low, 'low'),
    ]

    priority = models.CharField(
        max_length=20,
        choices=MY_CHOICES,
        default=Priority_Low,
    )
    checklist = models.TextField(default="Not Available",null=True, blank=True)
    cover = models.CharField(max_length=100, default='#ffff', null=True, blank = True)
    tech_stack = models.CharField(max_length=50, null=True, blank=True)
    task_progress = models.IntegerField(default=0)
    task_wallet = models.IntegerField(null=True,blank=True)
    ETA = JSONField(default=list, null=True, blank=True)
    achieved_points = models.IntegerField(null=True,blank=True,default=0)
    is_completed = models.BooleanField('Completed',default=False)
    is_flaged = models.BooleanField('Flaged', default=False)
    approvals = models.BooleanField('Approved', default=False)

    def save(self, *args, **kwargs):
    # Check if done_date has changed
        if self.pk is not None:
            orig = Task.objects.get(pk=self.pk)
            if orig.deadline != self.deadline:
                if self.ETA is None:
                    self.ETA = []
                # Append the new done_date as a string
                self.ETA.append(self.deadline.strftime("%Y-%m-%d"))

    # Set priority to high if ETA is within 3 days
        if self.ETA:
            today = datetime.now().date()
            for eta_date_str in self.ETA:
                eta_date = datetime.strptime(eta_date_str, "%Y-%m-%d").date()
                if (eta_date - today).days <= 2:
                    self.priority = self.Priority_High
                    break

        if self.task_progress is not None:
            if self.pk is not None:
                orig = Task.objects.get(pk=self.pk)
                if orig.task_progress > int(self.task_progress):
                    raise ValidationError("Task Progress Cannot Decrease")

                progress_increase = int(self.task_progress) - orig.task_progress
                if progress_increase > 0:
                    assigned_users = self.assignedTo.all()
                    if assigned_users.exists():
                        progress_per_user = progress_increase / assigned_users.count()
                        today = datetime.now().date()
                        for user in assigned_users:
                            progress_detail, created = ProgressDetail.objects.get_or_create(
                                date=today,
                                username=user.username,
                                task_name=self.taskName,
                                defaults={'progress_percentage': progress_per_user}
                            )
                            if not created:
                                progress_detail.progress_percentage += progress_per_user
                                progress_detail.save()

        if self.task_wallet is not None:
            # Check if achieved_points is greater than task_wallet
            orig = Task.objects.get(pk = self.pk)
            if int(self.achieved_points) > orig.task_wallet:
                raise ValidationError("Achieved Points cannot exceed Task Wallet value.")

        super(Task, self).save(*args, **kwargs)

    def __str__(self):
        return self.taskName
 

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tech_stack = models.CharField(max_length=50, null=True, blank=True)
    role = models.CharField(
        max_length=50, null=True,blank=True,
        choices=[
            ('UI/UX Designer', 'UI/UX Designer'),
            ('Backend Developer', 'Backend Developer'),
            ('Full Stack Developer', 'Full Stack Developer'),
            ('Cloud Developer', 'Cloud Developer')
        ]
    )
    designation = models.CharField(
        max_length=50,null=True,blank=True,
        choices=[
            ('User', 'User'),
            ('Super User', 'Super User'),
            ('Manager', 'Manager'),
            ('Team Lead', 'Team Lead')
        ],
        default='User'
    )
    assigned_project = models.ForeignKey(Projects, on_delete=models.CASCADE, null=True, blank=True)
    # profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)

    # def __str__(self):
    #    return self.user.username



    # current_status = models.CharField(max_length=30, default='Not Started')

class Message(models.Model):
    task = models.ForeignKey(Task,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    message = models.TextField(max_length=5000)
    date_time = models.DateTimeField(auto_now_add=True)
    is_flagged = models.BooleanField('flagged',default=False)
    reply_to = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
 