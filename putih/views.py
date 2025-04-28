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
         "company_name" : "test.inc",
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
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        no_identitas = str(uuid.uuid4())
        tanggal_reg = datetime.now().strftime("%d-%m-%Y")
        
        if request.POST.get('company_name'):
            company_name = request.POST.get('company_name')
            error_message = validate_registration_data(email, no_identitas, password, phone, company_name)
            if error_message:
                return render(request, 'register_klien_perusahaan.html', {'error_message': error_message})
            pengguna.append({
            "email": email,
            "password": password,
            "address": address,
            "phone": phone,
            "no_identitas": no_identitas,
            "tanggal_reg": tanggal_reg,
            "company_name": company_name
        }) 

        else:
            first_name = request.POST.get('first_name')
            middle_name = request.POST.get('middle_name', "")
            last_name = request.POST.get('last_name')
            error_message = validate_registration_data(email, no_identitas, password, phone, first_name, middle_name, last_name)
            if error_message:
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
                # messages.success(request, f"Welcome back, {user['first_name']}!")
                return redirect('putih:show_profile')

        messages.error(request, 'Invalid email or password')
        return render(request, 'login.html')

    return render(request, 'login.html')
  

def show_profile(request):
    global logged_pengguna
    print(logged_pengguna)
    return render(request, "profil_klien.html", logged_pengguna)

def logout(request):
    global penggunalogin
    penggunalogin = {}
    messages.success(request, 'Berhasil logout!')
    return redirect('putih:login')

def validate_registration_data(email, no_identitas, password, phone, first_name=None, middle_name=None, last_name=None, company_name=None):

    FIELD_LENGTH_LIMITS = {
        'email': 50,
        'password': 50,
        'phone': 15,
        'first_name': 50,
        'middle_name': 50,
        'last_name': 50,
        'company_name': 50,
    }

    # Unik
    if any(user['email'] == email for user in pengguna):
        return 'Email already exists'
    if any(user['no_identitas'] == no_identitas for user in pengguna):
        return 'No Identitas already exists'
    
    # Panjang Var
    if len(email) > FIELD_LENGTH_LIMITS['email']:
        return 'Email exceeds character limit'
    if len(password) > FIELD_LENGTH_LIMITS['password']:
        return 'Password exceeds character limit'
    if len(phone) > FIELD_LENGTH_LIMITS['phone']:
        return 'No Telepon exceeds character limit'
    
    # Format Nomor Telepon
    if not phone.isnumeric():
        return 'No Telepon must be numeric'
    
    # Name Fields
    name_fields = [
        ('Nama Depan', first_name, FIELD_LENGTH_LIMITS['first_name']),
        ('Nama Tengah', middle_name, FIELD_LENGTH_LIMITS['middle_name']),
        ('Nama Belakang', last_name, FIELD_LENGTH_LIMITS['last_name']),
        ('Nama Perusahaan', company_name, FIELD_LENGTH_LIMITS['company_name']),
    ]
    
    for field_name, field_value, limit in name_fields:
        if field_value and len(field_value) > limit:
            return f'{field_name} exceeds character limit'

    return None