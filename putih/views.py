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
    },
    {
        "email" : "emailfrontdesk@gmail.com",
        "password" : "Frontdesk123!!",
        "phone" : "123",
        "start_date" : datetime(2023, 1, 20),
        "address" : "test",
        "role" : "Frontdesk",
    },
    {
        "no_pegawai": "2306206283",
        "password" : "Akun123!!",
        "start_date" : datetime(2023, 1, 20),
        "end_date" : datetime(2023, 1, 20),
        "email" : "akundokter@gmail.com",
        "role"  : "Doctor"
    }
    ]

logged_pengguna = {}

def home(request):
    return render(request, 'home.html')

def register_selection(request):
    return render(request, 'register_selection.html')

def register_role(request, role):
    return render(request, f'register_{role}.html', {'role': role})

def register_klien(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        no_identitas = str(uuid.uuid4())
        tanggal_reg = datetime.now().strftime("%d-%m-%Y")
        
        if request.POST.get('company_name'):  # If company_name exists, process as company client
            company_name = request.POST.get('company_name')
            error_message = validate_registration_data(email, no_identitas, password, phone, company_name=company_name)
            
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

        else:  # If company_name doesn't exist, process as individual client
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

    # Dynamic render based on the role
    if request.POST.get('company_name'):
        return render(request, 'register_klien_perusahaan.html')
    else:
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
                return redirect('putih:show_profile')

        messages.error(request, 'Invalid email or password')
        return render(request, 'login.html')

    return render(request, 'login.html')
  
def show_profile(request):
    global logged_pengguna
    print(logged_pengguna)
    if logged_pengguna.get('doctor_id'):
        return render(request, "profil_dokter.html", logged_pengguna)
    return render(request, "profil_klien.html", logged_pengguna)

def show_profile_frontdesk(request):
    return render(request, "profil_frontdesk.html", logged_pengguna)

def show_profile_dokter(request):
    return render(request, "profil_dokter.html", logged_pengguna)

def show_profile_perawat(request):
    return render(request, "profil_perawat.html", logged_pengguna)

def logout(request):
    global logged_pengguna
    logged_pengguna = {}
    messages.success(request, 'Berhasil logout!')
    return redirect('putih:login')

def update_klien(request):
    if request.method == 'POST':
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        first_name = request.POST.get('first_name')
        middle_name = request.POST.get('middle_name', "")
        last_name = request.POST.get('last_name')
        company_name = request.POST.get('company_name')

        if company_name:
            errors = validate_update_data(address, phone, company_name=company_name)
        else:
            errors = validate_update_data(address, phone, first_name=first_name, middle_name=middle_name, last_name=last_name)

        if errors:
            context = {
                'errors': errors,
                **logged_pengguna,
            }
            return render(request, 'update_klien.html', context)
        
        logged_pengguna['address'] = address
        logged_pengguna['phone'] = phone

        if company_name:
            logged_pengguna['company_name'] = company_name
        else:
            logged_pengguna['first_name'] = first_name
            logged_pengguna['middle_name'] = middle_name
            logged_pengguna['last_name'] = last_name

        return redirect('putih:show_profile')

    context = {
        **logged_pengguna,
    }
    return render(request, 'update_klien.html', context)

def update_klien_individu(request):
    return render(request, 'update_klien_individu.html')

def update_klien_perusahaan(request):
    return render(request, 'update_klien_perusahaan.html')

def update_dokter(request):
    return render(request, 'update_dokter.html')

def update_perawat(request):
    return render(request, 'update_perawat.html')

def update_frontdesk(request):
    return render(request, 'update_frontdesk.html')

def update_password_placeholder(request):
    return render(request, 'update_password_placeholder.html')

def update_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        errors = validate_password_update(old_password, new_password1, new_password2)

        if errors:
            context = {
                'errors': errors,
                'old_password': old_password,
                'new_password1': new_password1,
                'new_password2': new_password2,
            }
            return render(request, 'update_password.html', context)

        logged_pengguna['password'] = new_password1

        messages.success(request, "Your password has been updated successfully.")
        return redirect('putih:show_profile') 

    return render(request, 'update_password.html')

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
    if any(user.get('no_identitas') == no_identitas for user in pengguna):
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
    
    if not company_name:
        name_fields = [
            ('First Name', first_name, FIELD_LENGTH_LIMITS['first_name']),
            ('Last Name', last_name, FIELD_LENGTH_LIMITS['last_name']),
        ]
        
        for field_name, field_value, limit in name_fields:
            if field_value and len(field_value) > limit:
                return f"{field_name} exceeds character limit."
            
        if middle_name and len(middle_name) > FIELD_LENGTH_LIMITS['middle_name']:
            return 'Middle Name exceeds character limit'

                
    if company_name and len(company_name) > FIELD_LENGTH_LIMITS['company_name']:
        return "Company Name exceeds character limit."
    
    return None

def validate_update_data(address, phone, first_name=None, middle_name=None, last_name=None, company_name=None):
    FIELD_LENGTH_LIMITS = {
        'address': 255,
        'phone': 15,
        'first_name': 50,
        'middle_name': 50,
        'last_name': 50,
        'company_name': 50,
    }
    
    errors = {}

    if not address:
        errors['address'] = "Address is required."
    elif len(address) > FIELD_LENGTH_LIMITS['address']:
        errors['address'] = "Address exceeds character limit."
    
    if not phone:
        errors['phone'] = "Phone number is required."
    elif len(phone) > FIELD_LENGTH_LIMITS['phone']:
        errors['phone'] = "Phone number exceeds character limit."
    elif not phone.isnumeric():
        errors['phone'] = "Phone number must be numeric."

    if not company_name:
        name_fields = [
            ('First Name', first_name, FIELD_LENGTH_LIMITS['first_name']),
            ('Middle Name', middle_name, FIELD_LENGTH_LIMITS['middle_name']),
            ('Last Name', last_name, FIELD_LENGTH_LIMITS['last_name']),
        ]
        
        for field_name, field_value, limit in name_fields:
            if field_value and len(field_value) > limit:
                errors[field_name.lower().replace(" ", "_")] = f"{field_name} exceeds character limit."

        if middle_name and len(middle_name) > FIELD_LENGTH_LIMITS['middle_name']:
            errors['middle_name'] = 'Middle Name exceeds character limit'
    
    if company_name and len(company_name) > FIELD_LENGTH_LIMITS['company_name']:
        errors['company_name'] = "Company Name exceeds character limit."

    return errors

def validate_password_update(old_password, new_password1, new_password2):

    errors = {}

    if not logged_pengguna or logged_pengguna.get('password') != old_password:
        errors['old_password'] = 'Incorrect old password.'
    
    if old_password == new_password1:
        errors['new_password1'] = 'New password cannot be the same as the old password.'

    if len(new_password1) < 8:
        errors['new_password1'] = 'New password must be at least 8 characters long.'
    elif not any(char.isdigit() for char in new_password1) or not any(char.isalpha() for char in new_password1):
        errors['new_password1'] = 'Password must contain both letters and numbers.'
    
    if new_password1 != new_password2:
        errors['new_password2'] = 'New passwords do not match.'

    return errors

#<!-- DUMMY FATHUR -->
def get_logged_user():
    return logged_pengguna if logged_pengguna else None

