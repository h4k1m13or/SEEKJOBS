from django.contrib import admin
from django.db import models
from tinymce.widgets import TinyMCE

from .models import Jobs, company,applications


# Register your models here.
class JobAdmin(admin.ModelAdmin):
    fields = ["job_title",
              "job_description", "job_published", "job_experience",
              "job_company",
              "job_location",
              "job_education",
              "job_type",
              "job_description",
              
              ]
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()}
    }


class CompanyAdmin(admin.ModelAdmin):
    fields = [

        "company_name",
        "establishment_date",
        "company_website_url",
        "company_logo",

        "company_location",
        "company_tagline",
        "company_linkedin",
        "company_email",
        "company_phone",
        "profile_description",

    ]


admin.site.register(Jobs)
admin.site.register(company, CompanyAdmin)
admin.site.register(applications)
