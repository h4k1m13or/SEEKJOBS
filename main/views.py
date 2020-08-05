from operator import itemgetter

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect

import main.backend as backend
from main.forms import RegistrationForm, CompanyInformation, LoginForm, newJob, resumeUpload, SearchtitledocumentForm, \
    SearchregionForm, JobTypeFilterForm
# Create your views here.
from main.models import Jobs, company, seeker_resume, recruiter, applications
from main.models import user_account


def homepage(request):
    if request.user.is_anonymous:
        return render(request=request, template_name='main/index.html',
                      context={'jobs': Jobs.objects.all().order_by("-id")[:5],}
                      )
    else:
        candidate = True
        if request.method == 'POST':
            return searchJob(request)
        else:
            print(candidate)
            if recruiter.objects.filter(user_id=request.user.id).exists():
                candidate = False
                print(request.user.username)
            print(candidate)
            return render(request=request, template_name='main/index.html',
                          context={'jobs': Jobs.objects.all().order_by("-id")[:5], 'candidate': candidate}
                          )


@login_required
def dashboard(request):
    candidate = True
    if request.user.is_anonymous:
        return redirect('main:register')
    if recruiter.objects.filter(user_id=request.user.id).exists():
        candidate = False
        result = []
        jobs = Jobs.objects.filter(job_company=recruiter.objects.get(user=request.user).recruiter_company)
        for job in jobs:
            result.append((job, applications.objects.filter(job=job).count()))
        return render(request=request, template_name='main/dashboard.html',
                      context={'result': result, 'candidate': candidate}
                      )
    else:
        return HttpResponse('mazel')


def jobs(request):
    candidate = True
    if recruiter.objects.filter(user_id=request.user.id).exists():
        candidate = False
    jobs_list = Jobs.objects.all().order_by("-id")
    paginator = Paginator(jobs_list, 8)  # Show 25 contacts per page

    page = request.GET.get('page')
    jobs = paginator.get_page(page)

    return render(request=request, template_name='main/jobs.html', context={'jobs': jobs, 'candidate': candidate})


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            sexe = form.cleaned_data['sexe']
            user_address = form.cleaned_data['user_address']
            type = form.cleaned_data['type']

            user = User.objects.create_user(username=username, password=password, email=email,
                                            last_name=last_name, first_name=first_name)
            user = authenticate(username=username, password=password)
            login(request, user)
            if type == 'candidate':
                user_account(user=user, user_address=user_address, gender=sexe).save()
                return jobs(request)
            else:
                recruiter(user=user, user_address=user_address, gender=sexe).save()
                return redirect('main:complete-company')

    return render(request=request, template_name='main/signin.html', context={'form': RegistrationForm}
                  )


@login_required
def CompanyInfo(request):
    if request.method == 'POST':
        form = CompanyInformation(request.POST)
        user = request.user
        print(user.username)
        if form.is_valid():
            print("company form is valid")
            name = form.cleaned_data['name']
            tagline = form.cleaned_data['tagline']
            website = form.cleaned_data['website']
            linkedin = form.cleaned_data['linkedin']
            # logo = form.cleaned_data['logo']
            description = form.cleaned_data['description']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            location = form.cleaned_data['location']
            cmp = company(company_name=name, company_tagline=tagline, company_email=email, company_linkedin=linkedin,
                          company_website_url=website, profile_description=description,
                          company_phone=phone, company_location=location)
            cmp.save()

            rec = recruiter.objects.get(user=request.user)
            rec.recruiter_company = cmp
            rec.save()
            print(rec.recruiter_company.company_name)
            return redirect('main:dashboard')
    return render(request=request, template_name='main/company.html', context={'form': CompanyInformation}
                  )


@login_required
def post(request):
    if recruiter.objects.filter(user_id=request.user.id).exists():
        if request.method == 'POST':
            print("post")
            form = newJob(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                location = form.cleaned_data['location']
                we = form.cleaned_data['we']
                degree = form.cleaned_data['degree']
                description = form.cleaned_data['description']
                type = form.cleaned_data['type']
                skills = ','.join(backend.extract_skills(backend.html_to_txt(description)))
                print(skills)
                cmp = recruiter.objects.get(user=request.user).recruiter_company
                j = Jobs(job_title=title, job_description=description, job_location=location, job_experience=we,
                         job_education=degree, job_company=cmp, job_type=type, job_skills=skills)
                j.save()
                print(j.id)
                return redirect('main:job', job_id=j.id)

    return render(request=request, template_name='main/Postjob.html', context={'form': newJob})


def loginview(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('main:jobs')
            else:
                return render(request=request, template_name='main/login.html', context={'form': LoginForm}
                              )
    return render(request=request, template_name='main/login.html', context={'form': LoginForm}
                  )


@login_required
def uploadcv(request):
    if not recruiter.objects.filter(user_id=request.user.id).exists():

        if request.method == 'POST':
            form = resumeUpload(request.POST, request.FILES)
            if form.is_valid():
                file = request.FILES['cv']

                file.name = request.user.username + '_resume.' + file.name.split('.')[-1]
                user = user_account.objects.get(user=request.user)

                if seeker_resume.objects.filter(user=user).exists():
                    cv = seeker_resume.objects.get(user=user)
                    print(cv.resume_path)
                    cv.resume_path = file
                    print(cv.resume_path)
                    cv.save()
                else:
                    cv = seeker_resume(resume_path=file, user=user)
                    cv.save()
                return redirect('main:recommendations')
    else:
        return HttpResponse('you are a recruiter, you can not upload a cv. Please login as job seeker')


def job(request, job_id):
    candidate = True
    if recruiter.objects.filter(user_id=request.user.id).exists():
        candidate = False
    job = Jobs.objects.get(id=job_id)
    job.views = job.views + 1
    job.save()
    t = True
    if recruiter.objects.filter(user_id=request.user.id).exists():
        t = False
    return render(request=request, template_name='main/job.html',
                  context={'job': job, 'type': t, 'candidate': candidate})


def logout_view(request):
    logout(request)
    return redirect('main:homepage')


def application(request, job_id):
    j = Jobs.objects.get(id=job_id)

    result = []
    try:
        candidates = applications.objects.filter(job=j)
        for c in candidates:
            resume = seeker_resume.objects.get(user=c.user)

            result.append((c, resume))
        return render(request=request, template_name='main/applications.html',
                      context={'result': result, 'job': j})

    except:
        return HttpResponse('error')


@login_required
def apply(request):
    job_id = request.GET.get('id')
    if recruiter.objects.filter(user_id=request.user.id).exists():
        return HttpResponse(
            'you are a recruiter, you can not apply to a job <a href="../dashboard">return to dashboard</a>')
    print(job_id)
    user = user_account.objects.get(user=request.user)
    if user_account.objects.filter(user=request.user).exists():
        if seeker_resume.objects.filter(user=user).exists():
            print('True')
            job = Jobs.objects.get(id=job_id)
            job_skills = job.job_skills.split(",")
            resume_skills = backend.extract_skills(seeker_resume.objects.get(user=user).skills)
            score = int(backend.calculate_similarity(resume_skills, job_skills) * 100)
            app = applications(user=user, job=job, score=score).save()
            return redirect('main:job', job_id=job_id)

    else:
        return HttpResponse('please upload a resume to your profile <a href="recommendations">click here</a>')


def resume(request, username):
    usr = User.objects.get(username=username)
    user = user_account.objects.get(user=usr)
    cv = seeker_resume.objects.get(user=user)
    print(cv.resume_path)
    return render(request=request, template_name='main/resume.html', context={'user': user, 'cv': cv})


def recommendations(request):

    if recruiter.objects.filter(user_id=request.user.id).exists():
        return redirect('main:dashboard')
    elif user_account.objects.filter(user=request.user).exists():
        user = user_account.objects.get(user=request.user)
        if seeker_resume.objects.filter(user=user).exists():
            hasresume = True
            cv = seeker_resume.objects.get(user=user)
            print(cv.resume_path.path)
            segments = backend.parser_pdf_docx('' + cv.resume_path.path)
            cv.experience = backend.extract_experience(segments['Experience'])
            print(cv.experience)
            cv.education = ','.join(backend.extract_education(segments['Education'].lower())['education'])
            cv.skills = ''.join(segments['Skills'])
            cv.degree = ','.join(backend.extract_education(segments['Education'].lower())['degree'])
            cv.save()
            degrees = cv.degree.split(',')
            jobs = Jobs.objects.filter(job_experience__lte=cv.experience, job_education__in=degrees)
            job_similarity = []
            resume = backend.extract_skills("".join(segments['Skills']))

            for job in jobs:
                desc = job.job_skills.split(',')
                job_similarity.append((job, int(backend.calculate_similarity(resume, desc) * 100)))
            job_similarity = sorted(job_similarity, key=itemgetter(1), reverse=True)
            return render(request, template_name='main/recommendations.html',
                          context={'hasresume': hasresume, 'jobs': job_similarity,'candidate':True})
        else:
            hasresume = False
            return render(request, template_name='main/recommendations.html',
                          context={'hasresume': hasresume,'candidate':True })


def searchJob(request):
    def search_offres(title=None, region=None, type=None):
        # & ( Q(job_type = type['freelance']) | Q(job_type = type['freelance']) | Q(job_type = type['fullTime']) | Q(job_type = type['partTime']) | Q(job_type = type['temporary']) )
        if title and region:
            return Jobs.objects.filter(Q(job_location__contains=region) & (
                    Q(job_title__contains=title) | Q(job_description__contains=title) | Q(
                job_education__contains=title) | Q(job_skills__contains=title) | Q(
                job_company__company_name__contains=title)))
        elif title:
            print('title')
            return Jobs.objects.filter((Q(job_title__contains=title) | Q(job_description__contains=title) | Q(
                job_education__contains=title) | Q(job_skills__contains=title) | Q(
                job_company__company_name__contains=title)))
        elif region:
            return Jobs.objects.filter(job_location__contains=region)
        else:
            print('None')
            return None

    form_adr = SearchregionForm(request.POST or None)
    form_title = SearchtitledocumentForm(request.POST or None)
    form_type = JobTypeFilterForm(request.POST or None)
    documents = []
    type = None
    if form_type.is_valid():
        type = {
            'freelance': form_type.cleaned_data['freelance'],
            'full': form_type.cleaned_data['fullTime'],
            'internship': form_type.cleaned_data['internship'],
            'part': form_type.cleaned_data['partTime'],
            'temporary': form_type.cleaned_data['temporary'],
        }

    if form_title.is_valid():
        title = form_title.cleaned_data['title']
        if form_adr.is_valid():
            # recherche les deux le titre et l'adresse
            region = form_adr.cleaned_data['region']
            documents = search_offres(title=title, region=region, type=type)
        else:
            # recherche le titre
            documents = search_offres(title=title, type=type)
    elif form_adr.is_valid():
        # recherche l'offre d'emploi de l'adresse
        region = form_adr.cleaned_data['region']
        documents = search_offres(region=region, type=type)

    return render(request=request, template_name='main/jobs.html', context={'jobs': documents})


def companyprofile(request, name):
    candidate = True
    if recruiter.objects.filter(user_id=request.user.id).exists():
        candidate = False
    cmp = company.objects.get(company_name=name)
    jobs = Jobs.objects.filter(job_company=cmp).order_by("-id")[:4]
    return render(request=request, template_name='main/companyProfile.html',
                  context={'company': cmp, 'jobs': jobs, 'candidate': candidate})


def companies(request):
    candidate = True
    if recruiter.objects.filter(user_id=request.user.id).exists():
        candidate = False
    return render(request=request, template_name='main/companies.html',
                  context={'companies': company.objects.all(), 'candidate': candidate})
