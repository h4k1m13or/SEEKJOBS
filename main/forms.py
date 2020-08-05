from django import forms


class RegistrationForm(forms.Form):
    email = forms.EmailField(required=True)
    username = forms.CharField(max_length=32)
    password1 = forms.CharField(widget=forms.PasswordInput, max_length=32)
    sexe = forms.CharField(max_length=10)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    type = forms.CharField(max_length=15)
    user_address = forms.CharField(max_length=200)


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, max_length=32)


class ResumeUpload(forms.Form):
    cv = forms.FileField()


class CompanyInformation(forms.Form):
    name = forms.CharField(max_length=100)
    website = forms.CharField(max_length=100)
    tagline = forms.CharField(max_length=250)
    # logo = forms.ImageField()
    description = forms.CharField()
    linkedin = forms.CharField(max_length=200)
    email = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=15)
    location = forms.CharField(max_length=150)


class newJob(forms.Form):
    title = forms.CharField()
    location = forms.CharField()
    we = forms.CharField()
    degree = forms.CharField()
    type = forms.CharField()
    description = forms.CharField()


class resumeUpload(forms.Form):
    cv = forms.FileField()


class SearchtitledocumentForm(forms.Form):
    title = forms.CharField()


class SearchregionForm(forms.Form):
    region = forms.CharField()


class JobTypeFilterForm(forms.Form):
    freelance = forms.CharField()
    fullTime = forms.CharField()
    internship = forms.CharField()
    partTime = forms.CharField()
    temporary = forms.CharField()
