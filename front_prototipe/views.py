from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'home.html')


def agent_anamnesis_detail(request):
    return render(request, 'agent_anamnesis_detail.html')

def agent_anamnesis_register(request):
    return render(request, 'agent_anamnesis_register.html')

def agent_card_profile(request):
    return render(request, 'agent_card_profile.html')
def agent_crm_customer_detail(request):
    return render(request, 'agent_crm_customer_detail.html')
def agent_crm_home(request):
    return render(request, 'agent_crm_home.html')
def agent_crm_register_customer(request):

    return render(request, 'agent_crm_register_customer.html')
def agent_home(request):
    return render(request, 'agent_home.html')
def agent_mls_home(request):
    return render(request, 'agent_mls_home.html')
def agent_mls_property_detail(request):
    return render(request, 'agent_mls_property_detail.html')
def agent_mls_property_register(request):
    return render(request, 'agent_mls_property_register.html')
def agent_profile(request):
    return render(request, 'agent_profile.html')
def agent_requirement_detail(request):
    return render(request, 'agent_requirement_detail.html')
def agent_wallet_home(request):
    return render(request, 'agent_wallet_home.html')
def agente_register_requirement(request):
    return render(request, 'agente_register_requirement.html')
def blog_article(request):
    return render(request, 'blog_article.html')
def blogs(request):
    return render(request, 'blogs.html')
def business_presentation(request):
    return render(request, 'business_presentation.html')
def calendar(request):
    return render(request, 'calendar.html')
def contact(request):
    return render(request, 'contact.html')

def customer_anamnesis(request):
    return render(request, 'customer_anamnesis.html')

def customer_home(request):
    return render(request, 'customer_home.html')

def customer_requirement_detail(request):
    return render(request, 'customer_requirement_detail.html')

def customer_wallet_home(request):
    return render(request, 'customer_wallet_home.html')

def market_place(request):
    return render(request, 'market_place.html')

def property_technical_sheet(request):
    return render(request, 'property_technical_sheet.html')

def schedule_consultancy(request):
    return render(request, 'schedule_consultancy.html')

def signin(request):
    return render(request, 'signin.html')

def signup(request):
    return render(request, 'signup.html')