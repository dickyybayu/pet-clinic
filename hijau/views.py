from django.shortcuts import render

# Create your views here.

def list_kunjungan(request):
    return render(request, 'list_kunjungan.html')

def create_kunjungan(request):
    return render(request, 'create_kunjungan.html')

def update_kunjungan(request):
    return render(request, 'update_kunjungan.html')

def create_rekam_medis(request):   
    return render(request, 'create_rekam_medis.html')

def list_treatment(request):
    return render(request, 'list_treatment.html')

def create_treatment(request):
    return render(request, 'create_treatment.html')

def update_treatment(request):
    return render(request, 'update_treatment.html')

def show_rekam_medis(request):
    return render(request, 'rekam_medis.html')

def update_rekam_medis(request):
    return render(request, 'update_rekam_medis.html')
