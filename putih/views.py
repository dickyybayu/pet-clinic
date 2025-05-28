import re
from django.http import HttpResponseNotFound
from django.shortcuts import redirect, render
import uuid
from datetime import datetime 
from django.contrib import messages
from utils.query import query
from utils.validators import *

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
        "no_pegawai" : "1234",
        "email" : "emailfrontdesk@gmail.com",
        "password" : "Frontdesk123!!",
        "phone" : "123",
        "start_date" : datetime(2023, 1, 20),
        "address" : "test",
        "role" : "Frontdesk",
    },
    {
        "doctor_id" : "123",
        "no_pegawai": "2306206283",
        "password" : "Akun123!!",
        "start_date" : datetime(2023, 1, 20),
        "end_date" : datetime(2023, 1, 20),
        "email" : "akundokter@gmail.com",
        "role"  : "Doctor"
    },
    {
        "role" : "perawat",
        "no_perawat" : "12345"
    }
    ]

logged_pengguna = {}

def home(request):
    return render(request, 'home.html')

def register_selection(request):
    return render(request, 'register_selection.html')

def register_role(request, role):
    if role == 'dokter':
        return redirect('putih:register_dokter')
    elif role == 'front_desk':
        return redirect('putih:register_front_desk')
    elif role == 'perawat':
        return redirect('putih:register_perawat')
    elif role == 'klien_individu':
        return redirect('putih:register_klien_individu')
    elif role == 'klien_perusahaan':
        return redirect('putih:register_klien_perusahaan')
    else:
        return HttpResponseNotFound("Role tidak ditemukan.")
    
def register_klien_individu(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        nama_depan = request.POST.get('first_name')
        nama_tengah = request.POST.get('middle_name')
        nama_belakang = request.POST.get('last_name')

        if not all([email, password, phone, address, nama_depan, nama_belakang]):
            return render(request, 'register_klien_individu.html', {'error_message': 'All fields marked with * are required.'})

        if query(f"SELECT * FROM \"USER\" WHERE email = '{email}'"):
            return render(request, 'register_klien_individu.html', {'error_message': 'Email is already registered.'})

        user_id = str(uuid.uuid4())
        today = date.today()

        query(f"""INSERT INTO "USER" (email, password, alamat, nomor_telepon)
                  VALUES ('{email}', '{password}', '{address}', '{phone}')""")
        query(f"""INSERT INTO KLIEN (no_identitas, tanggal_registrasi, email)
                  VALUES ('{user_id}', '{today}', '{email}')""")
        query(f"""INSERT INTO INDIVIDU (no_identitas_klien, nama_depan, nama_tengah, nama_belakang)
                  VALUES ('{user_id}', '{nama_depan}', {'NULL' if not nama_tengah else f"'{nama_tengah}'"}, '{nama_belakang}')""")

        messages.success(request, 'Registration successful! You may now login.')
        return redirect('putih:login')

    return render(request, 'register_klien_individu.html')

def register_klien_perusahaan(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        nama_perusahaan = request.POST.get('company_name')

        if not all([email, password, phone, address, nama_perusahaan]):
            return render(request, 'register_klien_perusahaan.html', {'error_message': 'All fields are required.'})

        if query(f"SELECT * FROM \"USER\" WHERE email = '{email}'"):
            return render(request, 'register_klien_perusahaan.html', {'error_message': 'Email is already registered.'})

        user_id = str(uuid.uuid4())
        today = date.today()

        query(f"""INSERT INTO "USER" (email, password, alamat, nomor_telepon)
                  VALUES ('{email}', '{password}', '{address}', '{phone}')""")
        query(f"""INSERT INTO KLIEN (no_identitas, tanggal_registrasi, email)
                  VALUES ('{user_id}', '{today}', '{email}')""")
        query(f"""INSERT INTO PERUSAHAAN (no_identitas_klien, nama_perusahaan)
                  VALUES ('{user_id}', '{nama_perusahaan}')""")

        messages.success(request, 'Registration successful! You may now login.')
        return redirect('putih:login')

    return render(request, 'register_klien_perusahaan.html')


def register_front_desk(request):
    context = {
        'form_data': request.POST if request.method == 'POST' else {}
    }

    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        phone = request.POST.get('phone', '').strip()
        start_date = request.POST.get('start_date', '').strip()
        address = request.POST.get('address', '').strip()

        field_errors = {}

        email_val_errors = validate_email(email)
        if email_val_errors:
            field_errors['email'] = email_val_errors

        password_val_errors = validate_password(password)
        if password_val_errors:
            field_errors['password'] = password_val_errors
        
        phone_val_errors = validate_phone(phone)
        if phone_val_errors:
            field_errors['phone'] = phone_val_errors

        address_val_errors = validate_address(address)
        if address_val_errors:
            field_errors['address'] = address_val_errors

        start_date_val_errors = validate_start_date(start_date)
        if start_date_val_errors:
            field_errors['start_date'] = start_date_val_errors

        if field_errors:
            context['errors'] = field_errors
            return render(request, 'register_front_desk.html', context)

        try:
            query_str_user = f'''
                INSERT INTO "USER" (email, password, alamat, nomor_telepon)
                VALUES ('{email}', '{password}', '{address}', '{phone}')
            ''' 
            result_user = query(query_str_user)

            if result_user != 1:
                error_detail = ""
                context['error_message'] = result_user["data"]
                return render(request, 'register_front_desk.html', context)

            employee_num = str(uuid.uuid4())
            query_str_pegawai = f'''
                INSERT INTO PEGAWAI (no_pegawai, tanggal_mulai_kerja, tanggal_akhir_kerja, email_user)
                VALUES ('{employee_num}', '{start_date}', NULL, '{email}')
            ''' 
            result_pegawai = query(query_str_pegawai)

            if result_pegawai != 1:
                error_detail = "" 
                context['error_message'] = f"Failed to create employee record.{error_detail}"
                return render(request, 'register_front_desk.html', context)

            query_str_front_desk = f'''
                INSERT INTO FRONT_DESK (no_front_desk)
                VALUES ('{employee_num}')
            ''' 
            result_front_desk = query(query_str_front_desk)

            if result_front_desk != 1:
                error_detail = "" 
                context['error_message'] = f"Failed to create front desk record.{error_detail}"
                return render(request, 'register_front_desk.html', context)

            messages.success(request, 'Registration successful!')
            return redirect('putih:login')

        except Exception as e:
            context['error_message'] = f"An unexpected error occurred: {str(e)}"
            return render(request, 'register_front_desk.html', context)

    return render(request, 'register_front_desk.html', context)

def register_dokter(request):
    if request.method == 'POST':
        print(request.POST)
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        start_date = request.POST.get('start_date')
        address = request.POST.get('address')
        no_izin_praktik = request.POST.get('nip')

        sertifikat_nos = request.POST.getlist('sertifikat_no[]')
        sertifikat_names = request.POST.getlist('sertifikat_name[]')
        hari_list = request.POST.getlist('jadwal_day[]')
        jam_list = request.POST.getlist('jadwal_time[]')

        if not all([email, password, phone, start_date, address, no_izin_praktik]):
            return render(request, 'register_dokter.html', {
                'error_message': 'Semua field wajib diisi.'
            })

        if not sertifikat_nos or not sertifikat_names:
            return render(request, 'register_dokter.html', {
                'error_message': 'Minimal satu sertifikat wajib diisi.'
            })
        for i, (no, name) in enumerate(zip(sertifikat_nos, sertifikat_names), 1):
            if not no.strip() or not name.strip():
                return render(request, 'register_dokter.html', {
                    'error_message': f'Sertifikat ke-{i} tidak lengkap.'
                })

        if not hari_list or not jam_list:
            return render(request, 'register_dokter.html', {
                'error_message': 'Minimal satu jadwal praktik wajib diisi.'
            })
        for i, (hari, jam) in enumerate(zip(hari_list, jam_list), 1):
            if not hari.strip() or not jam.strip():
                return render(request, 'register_dokter.html', {
                    'error_message': f'Jadwal praktik ke-{i} tidak lengkap.'
                })

        pegawai_id = str(uuid.uuid4())

        result = query(f"""INSERT INTO "USER" (email, password, alamat, nomor_telepon)
                           VALUES ('{email}', '{password}', '{address}', '{phone}')""")
        if isinstance(result, dict) and result.get('status') == 'error':
            return render(request, 'register_dokter.html', {'error_message': result['data']})

        result = query(f"""INSERT INTO PEGAWAI (no_pegawai, tanggal_mulai_kerja, tanggal_akhir_kerja, email_user)
                           VALUES ('{pegawai_id}', '{start_date}', NULL, '{email}')""")
        if isinstance(result, dict) and result.get('status') == 'error':
            return render(request, 'register_dokter.html', {'error_message': result['data']})

        result = query(f"""INSERT INTO TENAGA_MEDIS (no_tenaga_medis, no_izin_praktik)
                           VALUES ('{pegawai_id}', '{no_izin_praktik}')""")
        if isinstance(result, dict) and result.get('status') == 'error':
            return render(request, 'register_dokter.html', {'error_message': result['data']})

        result = query(f"""INSERT INTO DOKTER_HEWAN (no_dokter_hewan)
                           VALUES ('{pegawai_id}')""")
        if isinstance(result, dict) and result.get('status') == 'error':
            return render(request, 'register_dokter.html', {'error_message': result['data']})

        for no, name in zip(sertifikat_nos, sertifikat_names):
            result = query(f"""INSERT INTO SERTIFIKAT_KOMPETENSI (no_sertifikat_kompetensi, no_tenaga_medis, nama_sertifikat)
                               VALUES ('{no}', '{pegawai_id}', '{name}')""")
            if isinstance(result, dict) and result.get('status') == 'error':
                return render(request, 'register_dokter.html', {'error_message': result['data']})

        for hari, jam in zip(hari_list, jam_list):
            result = query(f"""INSERT INTO JADWAL_PRAKTIK (no_dokter_hewan, hari, jam)
                               VALUES ('{pegawai_id}', '{hari}', '{jam}')""")
            if isinstance(result, dict) and result.get('status') == 'error':
                return render(request, 'register_dokter.html', {'error_message': result['data']})

        messages.success(request, 'Registrasi berhasil! Silakan login.')
        return redirect('putih:login')

    return render(request, 'register_dokter.html')


def register_perawat(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        start_date = request.POST.get('start_date')
        address = request.POST.get('address')
        no_izin_praktik = request.POST.get('nip')

        sertifikat_nos = request.POST.getlist('sertifikat_no[]')
        sertifikat_names = request.POST.getlist('sertifikat_name[]')

        if not all([email, password, phone, start_date, address, no_izin_praktik]):
            return render(request, 'register_perawat.html', {
                'error_message': 'Semua field wajib diisi.'
            })

        if not sertifikat_nos or not sertifikat_names:
            return render(request, 'register_perawat.html', {
                'error_message': 'Minimal satu sertifikat wajib diisi.'
            })
        for i, (no, name) in enumerate(zip(sertifikat_nos, sertifikat_names), 1):
            if not no.strip() or not name.strip():
                return render(request, 'register_perawat.html', {
                    'error_message': f'Sertifikat ke-{i} tidak lengkap.'
                })

        pegawai_id = str(uuid.uuid4())
        query(f"""INSERT INTO "USER" (email, password, alamat, nomor_telepon)
                  VALUES ('{email}', '{password}', '{address}', '{phone}')""")
        query(f"""INSERT INTO PEGAWAI (no_pegawai, tanggal_mulai_kerja, tanggal_akhir_kerja, email_user)
                  VALUES ('{pegawai_id}', '{start_date}', NULL, '{email}')""")
        query(f"""INSERT INTO TENAGA_MEDIS (no_tenaga_medis, no_izin_praktik)
                  VALUES ('{pegawai_id}', '{no_izin_praktik}')""")
        query(f"""INSERT INTO PERAWAT_HEWAN (no_perawat_hewan)
                  VALUES ('{pegawai_id}')""")

        for no, name in zip(sertifikat_nos, sertifikat_names):
            query(f"""INSERT INTO SERTIFIKAT_KOMPETENSI (no_sertifikat_kompetensi, no_tenaga_medis, nama_sertifikat)
                      VALUES ('{no}', '{pegawai_id}', '{name}')""")

        messages.success(request, 'Registrasi berhasil! Silakan login.')
        return redirect('putih:login')

    return render(request, 'register_perawat.html')



def login_view(request):
    context = {
        "message" : ""
    }

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        query_str = f'''
            SELECT * FROM "USER" WHERE email = '{email}' AND password = '{password}'
        '''
        result = query(query_str)
        if len(result) == 1:
            logged_user = {
                'email': result[0]['email'],
                'address': result[0]['alamat'],
                'phone': result[0]['nomor_telepon'],
            }

            query_str = f'''
                SELECT * FROM klien WHERE email = '{email}'
            '''
            klien_result = query(query_str)

            if len(klien_result) == 1:
                logged_user['no_identitas'] = klien_result[0]['no_identitas']
                logged_user['tanggal_registrasi'] = klien_result[0]['tanggal_registrasi'].isoformat()

                query_str   = f'''
                    SELECT * FROM individu WHERE no_identitas_klien = '{logged_user['no_identitas']}'
                '''
                individu_result = query(query_str) 
                if len(individu_result) == 1:
                    logged_user['nama_depan'] = individu_result[0]['nama_depan']
                    logged_user['nama_tengah'] = individu_result[0]['nama_tengah']
                    logged_user['nama_belakang'] = individu_result[0]['nama_belakang']
                    logged_user['role'] = 'klien_individu'
                else:
                    query_str = f'''
                        SELECT * FROM perusahaan WHERE no_identitas_klien = '{logged_user['no_identitas']}'
                    '''
                    perusahaan_result = query(query_str)
                    if len(perusahaan_result) == 1:
                        logged_user['nama_perusahaan'] = perusahaan_result[0]['nama_perusahaan']
                        logged_user['role'] = 'klien_perusahaan'
                
            else:
                query_str = f'''
                    SELECT * FROM pegawai WHERE email_user = '{email}'
                '''
                pegawai_result = query(query_str)
                logged_user['no_pegawai'] = pegawai_result[0]['no_pegawai']
                logged_user['tanggal_mulai_kerja'] = pegawai_result[0]['tanggal_mulai_kerja'].isoformat()
                logged_user['tanggal_akhir_kerja'] = pegawai_result[0]['tanggal_akhir_kerja'].isoformat() if pegawai_result[0]['tanggal_akhir_kerja'] else None

                query_str = f'''
                    SELECT * FROM tenaga_medis WHERE no_tenaga_medis = '{logged_user['no_pegawai']}'
                '''
                tenaga_medis_result = query(query_str)
                
                if len(tenaga_medis_result) == 1:
                    logged_user['no_tenaga_medis'] = tenaga_medis_result[0]['no_tenaga_medis']
                    logged_user['no_izin_praktik'] = tenaga_medis_result[0]['no_izin_praktik']

                    query_str = f'''
                        SELECT * FROM dokter_hewan WHERE no_dokter_hewan = '{logged_user['no_tenaga_medis']}'
                    '''
                    dokter_result = query(query_str)
                    if isinstance(dokter_result, list) and len(dokter_result) == 1:
                        logged_user['role'] = 'dokter'
                    else:
                        query_str = f'''
                            SELECT * FROM perawat_hewan WHERE no_perawat_hewan = '{logged_user['no_tenaga_medis']}'
                        '''
                        perawat_result = query(query_str)
                        if isinstance(perawat_result, list) and len(perawat_result) == 1:
                            logged_user['role'] = 'perawat'
                        else:
                            context['message'] = "Role tenaga medis tidak valid."
                            return render(request, 'login.html', context)

                else:
                    query_str = f'''
                        SELECT * FROM front_desk WHERE no_front_desk = '{logged_user['no_pegawai']}'
                    '''
                    front_desk_result = query(query_str)
                    if len(front_desk_result) == 0:
                        context['message'] = "Invalid email or password"
                        return render(request, 'login.html', context)

                    logged_user['no_front_desk'] = front_desk_result[0]['no_front_desk']
                    logged_user['role'] = 'front_desk'

            request.session['logged_user'] = logged_user   
            return redirect('putih:show_profile', role=logged_user['role'])

        context['message'] = "Invalid email or password"
    return render(request, 'login.html', context)
  
def show_profile(request, role):
    logged_user = request.session.get('logged_user', {})
    context = {'logged_user': logged_user}

    if role in ['klien_individu', 'klien_perusahaan']:
        return render(request, 'profil_klien.html', context)
    elif role == 'dokter':
        return render(request, 'profil_dokter.html', context)
    elif role == 'perawat':
        return render(request, 'profil_perawat.html', context)
    elif role == 'front_desk':
        return render(request, 'profil_front_desk.html', context)
    else:
        return HttpResponseNotFound("Role tidak ditemukan.")


def logout(request):
    request.session.flush()
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

def update_front_desk(request):
    logged_user = request.session.get('logged_user')
    if not logged_user or logged_user.get('role') != 'front_desk':
        messages.error(request, "Akses ditolak. Anda harus login sebagai Front Desk Officer.")
        return redirect('putih:login')

    user_email = logged_user.get('email')
    no_pegawai = logged_user.get('no_pegawai')

    context = {'logged_user': logged_user, 'form_values': {}}

    if request.method == 'POST':
        new_alamat = request.POST.get('alamat', '').strip()
        new_nomor_telepon = request.POST.get('nomor_telepon', '').strip()
        new_tanggal_akhir_kerja_str = request.POST.get('tanggal_akhir_kerja', '').strip()

        context['form_values'] = {
            'alamat': new_alamat,
            'nomor_telepon': new_nomor_telepon,
            'tanggal_akhir_kerja': new_tanggal_akhir_kerja_str,
        }

        errors = {}
        addr_errors = validate_address(new_alamat)
        if addr_errors: errors['alamat'] = addr_errors
        
        phone_errors = validate_phone(new_nomor_telepon)
        if phone_errors: errors['nomor_telepon'] = phone_errors

        tanggal_mulai_kerja_session_str = logged_user.get('tanggal_mulai_kerja')
        tgl_akhir_errors = validate_end_date(new_tanggal_akhir_kerja_str, tanggal_mulai_kerja_session_str)
        if tgl_akhir_errors: errors['tanggal_akhir_kerja'] = tgl_akhir_errors

        if errors:
            context['errors'] = errors
            return render(request, 'update_front_desk.html', context)

        try:
            query_user_update_str = f"UPDATE \"USER\" SET alamat = '{new_alamat}', nomor_telepon = '{new_nomor_telepon}' WHERE email = '{user_email}'" # UNSAFE
            query(query_user_update_str) 

            db_tanggal_akhir_kerja = new_tanggal_akhir_kerja_str if new_tanggal_akhir_kerja_str else None
            
            if db_tanggal_akhir_kerja is None:
                query_pegawai_update_str = f"UPDATE \"PEGAWAI\" SET tanggal_akhir_kerja = NULL WHERE no_pegawai = '{no_pegawai}'" # UNSAFE
            else:
                query_pegawai_update_str = f"UPDATE \"PEGAWAI\" SET tanggal_akhir_kerja = '{db_tanggal_akhir_kerja}' WHERE no_pegawai = '{no_pegawai}'" # UNSAFE
            query(query_pegawai_update_str)

            # Update session data
            request.session['logged_user']['address'] = new_alamat
            request.session['logged_user']['phone'] = new_nomor_telepon
            request.session['logged_user']['tanggal_akhir_kerja'] = db_tanggal_akhir_kerja 
            request.session.modified = True

            messages.success(request, "Profil berhasil diperbarui.")
            return redirect('putih:show_profile', role=logged_user['role'])

        except Exception as e:
            messages.error(request, f"Terjadi kesalahan saat memperbarui profil: {str(e)}")
            return render(request, 'update_front_desk.html', context)

    else: 
        context['form_values'] = {
            'alamat': logged_user.get('address', ''),
            'nomor_telepon': logged_user.get('phone', ''),
            'tanggal_akhir_kerja': logged_user.get('tanggal_akhir_kerja', '') or ''
        }
        return render(request, 'update_front_desk.html', context)

def update_password_placeholder(request):
    return render(request, 'update_password_placeholder.html')

def update_password(request):
    logged_user = request.session.get('logged_user')
    if not logged_user:
        messages.error(request, "You must be logged in to update your password.")
        return redirect('putih:login')
    user_email = logged_user.get('email')
    if not user_email:
        messages.error(request, "User session data is incomplete. Please log in again.")
        return redirect('putih:login')

    context = {
        'logged_user': logged_user,
        'form_values': {}
    }

    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')

        context['form_values'] = {'old_password': old_password}

        errors = validate_password_update(user_email, old_password, new_password1, new_password2, query)

        if errors:
            context['errors'] = errors
            return render(request, 'update_password.html', context)

        password_to_store_in_db = new_password1
        update_query_str = f"UPDATE \"USER\" SET password = '{password_to_store_in_db}' WHERE email = '{user_email}'" 
        
        try:
            update_result = query(update_query_str) 
            if update_result is not None and int(update_result) >= 0:
                messages.success(request, "Your password has been updated successfully.")
            
                user_role = logged_user.get('role')
                return redirect('putih:show_profile', role=user_role)
            
            else:
                messages.error(request, "Failed to update password in the database. No changes were made or an error occurred.")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}. Please try again.")
        
        context['form_values'] = {'old_password': old_password}
        return render(request, 'update_password.html', context)

    return render(request, 'update_password.html', context)

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