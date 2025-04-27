from django.shortcuts import render

#Dummy Pengguna 
pengguna = [
    {
         "email" : "akuindividuklien@gmail.com",
         "password" : "Akun123!!",
         "alamat" : "test",
         "no_telp" : "123",
         "no_identitas" : "2306206281",
         "tanggal_reg" : "20-01-2023",
         "nama_depan" : "test",
         "nama_tengah" : "test",
         "nama_belakang" : "test",
    },
    {
        "email" : "akuperusahaanklien@gmail.com",
         "password" : "Perusahaan123!!",
         "alamat" : "test",
         "no_telp" : "123",
         "no_identitas" : "2306206282",
         "tanggal_reg" : "20-01-2023",
         "nama_perushan" : "test.inc",
    }
]

# Create your views here.
def home(request):
    return render(request, 'home.html')

def register_selection(request):
    return render(request, 'register_selection.html')

def register_role(request, role):
    return render(request, f'register_{role}.html', {'role': role})

def login_view(request):
    return render(request, 'login.html')  