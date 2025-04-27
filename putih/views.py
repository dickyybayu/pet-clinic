from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'home.html')

def register_selection(request):
    return render(request, 'register_selection.html')

def register_role(request, role):
    return render(request, f'register_{role}.html', {'role': role})

def login_view(request):
    return render(request, 'login.html')  