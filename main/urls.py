"""SEEKJOBS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.main, name='main')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='main')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

import main.views as views

app_name = 'main'
urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('jobs', views.jobs, name='jobs'),
    path('searchJob', views.searchJob, name='searchJob'),
    path('recommendations', views.recommendations, name='recommendations'),
    path('register', views.register, name='register'),
    path('login', views.loginview, name='login'),
    path('uploadcv', views.uploadcv, name='uploadcv'),
    path('job/<int:job_id>', views.job, name='job'),
    path('<str:username>/resume', views.resume, name='resume'),
    path('applications/<int:job_id>', views.application, name='applications'),
    path('complete-company', views.CompanyInfo, name="complete-company"),
    path('jobs/new', views.post, name="post-a-job"),
    path('logout', views.logout_view, name="logout"),
    path('dashboard', views.dashboard, name="dashboard"),
    path('job/apply', views.apply, name="apply"),
    path('company/<str:name>', views.companyprofile, name="company"),
    path('companies', views.companies, name="companies")

]
