from django.shortcuts import redirect, render
import uuid
from datetime import datetime 
from django.contrib import messages

#Dummy Pengguna 
pengguna = [
    {
         "email" : "akuindividuklien@gmail.com",
         "password" : "Akun123!!",
         "address" : "test",
         "phone" : "123",
         "no_identitas" : "2306206281",
         "tanggal_reg" : datetime(2023, 1, 20),
         "first_name" : "test",
         "middle_name" : "test",
         "last_name" : "test",
    },
    {
         "email" : "akuperusahaanklien@gmail.com",
         "password" : "Perusahaan123!!",
         "address" : "test",
         "phone" : "123",
         "no_identitas" : "2306206282",
         "tanggal_reg" : datetime(2023, 1, 20),
         "nama_perushan" : "test.inc",
    }
]

logged_pengguna = {}

# Create your views here.
def home(request):
    return render(request, 'home.html')

def register_selection(request):
    return render(request, 'register_selection.html')

def register_role(request, role):
    return render(request, f'register_{role}.html', {'role': role})

def register_klien_individu(request):
    print("masuk function")
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        no_identitas = str(uuid.uuid4())
        tanggal_reg = datetime.now().strftime("%d-%m-%Y")
        first_name = request.POST.get('first_name')
        middle_name = request.POST.get('middle_name', "")
        last_name = request.POST.get('last_name')

        print("is post")

        error_message = validate_registration_data(email, no_identitas, password, phone, first_name, last_name)
        if error_message:
            print("is error message")
            return render(request, 'register_klien_individu.html', {'error_message': error_message})

        pengguna.append({
            "email": email,
            "password": password,
            "address": address,
            "phone": phone,
            "no_identitas": no_identitas,
            "tanggal_reg": tanggal_reg,
            "first_name": first_name,
            "middle_name": middle_name,
            "last_name": last_name,
        }) 
        print("is append")
        messages.success(request, 'Registration successful!')
        return redirect('putih:login')
    return render(request, 'register_klien_individu.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        global logged_pengguna
        logged_pengguna = {}

        for user in pengguna:
            if user['email'] == email and user['password'] == password:
                logged_pengguna = user
                messages.success(request, f"Welcome back, {user['first_name']}!")
                return redirect('putih:show_profile')

        messages.error(request, 'Invalid email or password')
        return render(request, 'login.html')

    return render(request, 'login.html')
  

def show_profile(request):
    global logged_pengguna
    print(logged_pengguna)
    return render(request, "profil_klien.html", logged_pengguna)


def validate_registration_data(email, no_identitas, password, phone, first_name, last_name):
    for user in pengguna:
        if user['email'] == email:
            return 'Email already exists'
        if user['no_identitas'] == no_identitas:
            return 'No Identitas already exists'
        if len(email) > 50:
            return 'Email exceeds character limit'
        if len(password) > 50:
            return 'Password exceeds character limit'
        if phone.isnumeric() == False:
            return 'No Telepon must be numeric'
        if len(phone) > 15:
            return 'No Telepon exceeds character limit'
        if len(first_name) > 50:
            return 'Nama Depan exceeds character limit'
        if len(last_name) > 50:
            return 'Nama Belakang exceeds character limit'
        return None