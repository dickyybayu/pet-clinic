from django.shortcuts import render

# Create your views here.
def list_hewan(request):
    return render(request, 'list_hewan.html')

def list_kunjungan(request):
    return render(request, 'list_kunjungan.html')