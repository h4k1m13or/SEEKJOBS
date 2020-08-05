import math
from datetime import datetime

from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.utils import timezone


# Create your models here.
class company(models.Model):
    id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=100, unique=True)
    profile_description = models.TextField()
    establishment_date = models.DateField(default=datetime.now)
    company_website_url = models.CharField(max_length=100)
    company_logo = models.ImageField(upload_to='company_logos/')
    company_location = models.CharField(max_length=150, blank=True)
    company_tagline = models.CharField(max_length=250, blank=True)
    company_linkedin = models.CharField(max_length=200, blank=True)
    company_email = models.CharField(max_length=100, blank=True)
    company_phone = models.CharField(max_length=15, blank=True)


class user_account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=15)
    contact_number = models.CharField(max_length=10)
    registration_date = models.DateField(default=datetime.now)
    user_address = models.CharField(max_length=200, blank=True)
    profile_picture = models.ImageField(upload_to='Profile_pictures/')

    def get_full_name(self):
        return self.user.first_name + " " + self.user.last_name

    def email(self):
        return self.user.email

    def last_login(self):
        return str(self.user.last_login.date())


class recruiter(models.Model):
    recruiter_company = models.ForeignKey(company, on_delete=models.CASCADE, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=15)
    contact_number = models.CharField(max_length=10)
    registration_date = models.DateField(default=datetime.now)
    user_address = models.CharField(max_length=200, blank=True)



class seeker_resume(models.Model):
    user = models.OneToOneField(user_account, on_delete=models.CASCADE)
    resume_path = models.FileField(upload_to='userResume/')
    education = models.TextField(blank=True, null=True)
    experience = models.IntegerField(blank=True, null=True)
    skills = models.TextField(blank=True, null=True)
    degree = models.TextField(null=True, blank=True)


class Jobs(models.Model):
    id = models.AutoField(primary_key=True)
    job_title = models.CharField(max_length=200)
    job_published = models.DateTimeField('Date published', default=datetime.now)
    job_description = models.TextField()
    job_company = models.ForeignKey(company, on_delete=models.CASCADE)
    job_location = models.CharField(max_length=50)
    job_experience = models.IntegerField()
    job_education = models.CharField(max_length=20)
    job_type = models.CharField(max_length=20, default='Full time')
    views = models.IntegerField(default=0)
    job_skills = models.TextField(blank=True)

    def __str__(self):
        return self.job_title + ', ' + self.job_company.company_name + '- ' + str(self.job_published)

    def company(self):
        return str(self.job_company.company_name)

    def whenpublished(self):

        diff = datetime.now(timezone.utc) - self.job_published

        if diff.days == 0 and 0 <= diff.seconds < 60:
            seconds = diff.seconds

            if seconds == 1:
                return str(seconds) + "second ago"

            else:
                return str(seconds) + " seconds ago"

        if diff.days == 0 and 60 <= diff.seconds < 3600:
            minutes = math.floor(diff.seconds / 60)

            if minutes == 1:
                return str(minutes) + " minute ago"

            else:
                return str(minutes) + " minutes ago"

        if diff.days == 0 and 3600 <= diff.seconds < 86400:
            hours = math.floor(diff.seconds / 3600)

            if hours == 1:
                return str(hours) + " hour ago"

            else:
                return str(hours) + " hours ago"

        # 1 day to 30 days
        if 1 <= diff.days < 30:
            days = diff.days

            if days == 1:
                return str(days) + " day ago"

            else:
                return str(days) + " days ago"

        if 30 <= diff.days < 365:
            months = math.floor(diff.days / 30)

            if months == 1:
                return str(months) + " month ago"

            else:
                return str(months) + " months ago"

        if diff.days >= 365:
            years = math.floor(diff.days / 365)

            if years == 1:
                return str(years) + " year ago"

            else:
                return str(years) + " years ago"

    def type(self):
        if self.job_type == 'Full':
            return 'Full Time'
        if self.job_type == 'Freelance':
            return 'Freelance'
        if self.job_type == 'Part':
            return 'Part Time'
        else:
            return self.job_type


class applications(models.Model):
    user = models.ForeignKey(user_account, on_delete=models.CASCADE)
    job = models.ForeignKey(Jobs, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    status = models.TextField(default='pending')
