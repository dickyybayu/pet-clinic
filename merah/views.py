from django.shortcuts import redirect, render
from django.urls import reverse
from datetime import datetime
from django.contrib import messages
import uuid

from utils.query import query


logged_doctor = {
    "email"  : "akudokter@gmail.com",
      "password" : "dokter123", 
      "address" : "test",
      "phone" : "123",
      "worker_id" : "2306206283",
      "start_date" : datetime(2023, 1, 20),
      "end_date" : None,
      "medic_id" : "123",
      "doctor_id": "123",
      "sertifikat" :[{
          "sertifikat_id": "1",
          "nama" : "aaa"
      }, {
          "sertifikat_id": "2",
          "nama" : "bbb"
      }],
      "jadwal" : [{"hari" : "senin",
        "jam_mulai" : "08:00",
        "jam_selesai" : "17:00"}]
        }

kunjungan = [
  {
    "id_kunjungan": "KJN001",
    "no_identitas_klien": "123456789",
    "nama_hewan": "Kucing",
    "no_front_desk": "FD123",
    "no_perawat_hewan": "PW1",
    "no_dokter_hewan": "123",
    "kode_vaksin": "VAK123",
    "tipe_kunjungan": "Vaksinasi",
    "timetamp_awal": datetime(2023,10,1,10,0,0),
    "timetamp_akhir": datetime(2023,10,1,11,0,0),
    "suhu": 38.5,
    "berat_badan": 5.0
  },
  {
    "id_kunjungan": "KJN002",
    "no_identitas_klien": "987654321",
    "nama_hewan": "Anjing",
    "no_front_desk": "FD124",
    "no_perawat_hewan": "PW2",
    "no_dokter_hewan": "123",
    "kode_vaksin": None,
    "tipe_kunjungan": "Pemeriksaan Umum",
    "timetamp_awal": datetime(2023,10,2,9,30,0),
    "timetamp_akhir": None,
    "suhu": 39.0,
    "berat_badan": 12.3
  },
    ]

vaksin = [
    {
        "kode_vaksin": "VAK123",
        "nama_vaksin": "Vaksin Rabies",
        "harga": 150000,
        "stok": 10,
    },
    {
        "kode_vaksin": "VAK456",
        "nama_vaksin": "Vaksin Rabies 2",
        "harga": 150000,
        "stok": 0,
    },
    
]

clients =[ 
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
]

pets = [ {
    "nama" : "el wiwi",
    "no_identitas_klien" : "2306206282",
    "tanggal_lahir" : datetime(2020, 1, 1),
    "id_jenis" : "1"
},
{
    "nama" : "el wowo",
    "no_identitas_klien" : "2306206282",
    "tanggal_lahir" : datetime(2020, 1, 1),
    "id_jenis" : "2"
},
{
    "nama" : "el wawa",
    "no_identitas_klien" : "2306206281",
    "tanggal_lahir" : datetime(2020, 1, 1),
    "id_jenis" : "1"
},
{
    "nama" : "el wuwa",
    "no_identitas_klien" : "2306206282",
    "tanggal_lahir" : datetime(2020, 1, 1),
    "id_jenis" : "2"
}
]

jenis_hewan = [
    {
        "id" : "1",
        "nama_jenis" : "kucing"
    },
    {
        "id" : "2",
        "nama_jenis" : "anjing"
    }
]

# CRUD VAKSINASI DOKTER 
def show_vaksinasi(request):
    logged_user = request.session.get('logged_user', None)
    result = []

    if not logged_user or logged_user.get('role') != 'dokter':
        messages.error(request, "Anda harus login atau memiliki role dokter untuk akses vaksinasi.")
        return redirect('putih:login')
    else:
        sql = f'''
        SELECT
            k.id_kunjungan,
            k.timestamp_awal,
            v.kode,
            v.nama
        FROM 
            kunjungan k
        LEFT JOIN
            vaksin v ON k.kode_vaksin = v.kode
        WHERE
            no_dokter_hewan = '{logged_user.get('no_dokter_hewan')}'
        AND
            k.timestamp_akhir IS NULL
        AND
            k.kode_vaksin IS NOT NULL
        '''
        result = query(sql)

    context = {
        'logged_user': logged_user,
        'vaksin_data' : result,
    }
    return render(request, 'show_vaksinasi.html', context)
   
def create_vaksinasi(request):  
    logged_user = request.session.get('logged_user', None)
    kunjungan = []
    vaksin = []

    if not logged_user or logged_user.get('role') != 'dokter': 
        messages.error(request, "Anda harus login atau memiliki role dokter untuk akses vaksinasi.")
        return redirect('putih:login')
    else:
        if request.method == 'POST':
            selected_kunjungan = request.POST.get('selected_kunjungan')
            selected_vaksin = request.POST.get('selected_vaksin')

            print(selected_vaksin)

            sql = f'''
            UPDATE
                KUNJUNGAN
            SET
                kode_vaksin = '{selected_vaksin}'
            WHERE
                id_kunjungan = '{selected_kunjungan}';
            '''
            result = query(sql)
            if isinstance(result, dict) and result.get("status") == "error":
                messages.error(request, result.get('data'))
                return redirect('merah:create_vaksinasi')
                
            messages.success(request, "Vaksinasi berhasil ditambahkan")
            return redirect('merah:show_vaksinasi')

        logged_user = request.session.get('logged_user', None)
        
        kunjungan = f'''
        SELECT
            id_kunjungan
        FROM 
            kunjungan
        WHERE
            no_dokter_hewan = '{logged_user.get('no_dokter_hewan')}'
        AND
            timestamp_akhir IS NULL
        AND 
            kode_vaksin IS NULL
        '''

        vaksin = f'''
        SELECT
            kode,
            nama,
            stok
        FROM
            vaksin
        ORDER BY 
            kode ASC;
        '''

        kunjungan = query(kunjungan)
        vaksin  = query(vaksin)
    
    context = {
        'logged_user': logged_user,
        'kunjungan': kunjungan,
        'vaksin': vaksin,
    }

    return render(request, 'create_vaksinasi.html', context)

def update_vaksinasi(request, id_kunjungan):
    logged_user = request.session.get('logged_user', None)

    if not logged_user or logged_user.get('role') != 'dokter':
        messages.error(request, "Anda harus login atau memiliki role dokter untuk akses vaksinasi.")
        return redirect('putih:login')
    else:
        sql_get_kunjungan = f"""
            SELECT id_kunjungan, kode_vaksin, no_dokter_hewan 
            FROM KUNJUNGAN 
            WHERE id_kunjungan = '{id_kunjungan}';
        """

        kunjungan_result = query(sql_get_kunjungan)

        if not kunjungan_result or not isinstance(kunjungan_result, list) or len(kunjungan_result) == 0:
            messages.error(request, "Kunjungan tidak ditemukan.")
            return redirect('merah:show_vaksinasi')
        kunjungan_current = kunjungan_result

        if request.method == 'POST':
            selected_vaksin_baru = request.POST.get('selected_vaksin')

            if not selected_vaksin_baru:
                messages.error(request, "Silakan pilih vaksin baru.")
                all_vaksin = query("SELECT kode, nama, stok FROM VAKSIN ORDER BY nama;")
                context = {
                    'vaksin_options': all_vaksin if isinstance(all_vaksin, list) else [],
                    'current_kunjungan': kunjungan_current,
                    'logged_user': logged_user
                }
                return render(request, 'update_vaksinasi.html', context)

            if selected_vaksin_baru == kunjungan_current[0].get('kode_vaksin'):
                messages.info(request, f"Kunjungan sudah menggunakan vaksin tersebut. Tidak ada perubahan dilakukan.")
                return redirect('merah:show_vaksinasi')

            sql_update = f"""
                UPDATE KUNJUNGAN
                SET kode_vaksin = '{selected_vaksin_baru}'
                WHERE id_kunjungan = '{id_kunjungan}';
            """
            result = query(sql_update)

            if isinstance(result, dict) and result.get("status") == "error":
                messages.error(request, result.get("data") )
                all_vaksin_options_err = query("SELECT kode, nama, stok FROM VAKSIN WHERE stok > 0 ORDER BY nama;")
                context = {
                    'vaksin_options': all_vaksin_options_err if isinstance(all_vaksin_options_err, list) else [],
                    'current_kunjungan': kunjungan_current[0],
                    'logged_user': logged_user,
                    'selected_vaksin_id_on_error': selected_vaksin_baru 
                }
                return render(request, 'update_vaksinasi.html', context)
            
            messages.success(request, f"Vaksinasi untuk kunjungan {id_kunjungan} berhasil diperbarui.")
            return redirect('merah:show_vaksinasi')


    all_vaksin = query("SELECT kode, nama, stok FROM VAKSIN ORDER BY nama;")
    
    context = {
        'vaksin_options': all_vaksin if isinstance(all_vaksin, list) else [],
        'current_kunjungan': kunjungan_current[0],
        'logged_user': logged_user
    }
    return render(request, 'update_vaksinasi.html', context)

def delete_vaksinasi(request, id_kunjungan):
    logged_user = request.session.get('logged_user', None)
    if not logged_user or logged_user.get('role') != 'dokter':
        messages.error(request, "Anda harus login atau memiliki role dokter untuk akses vaksinasi.")
        return redirect('putih:login')
    
    sql = f"""
        UPDATE KUNJUNGAN 
        SET kode_vaksin = NULL 
        WHERE id_kunjungan = '{id_kunjungan}' AND kode_vaksin IS NOT NULL; 
    """
    result = query(sql) 

    if isinstance(result, dict) and result.get("status") == "error":
        messages.error(request, f"Gagal menghapus vaksinasi untuk kunjungan {id_kunjungan}: {result.get('data', 'Detail tidak tersedia')}")
    else:
        messages.success(request, f"Vaksinasi untuk kunjungan {id_kunjungan} berhasil dihapus.")
    return redirect('merah:show_vaksinasi')

# CRUD VAKSIN PERAWAT 
def is_vaksin_used(kode_vaksin):
    used_vaksin = {kunjungan_entry["kode_vaksin"] for kunjungan_entry in kunjungan if kunjungan_entry["kode_vaksin"]}
    return kode_vaksin in used_vaksin

def create_vaksin(request):
    if request.method == 'POST':
        kode_vaksin = uuid.uuid4()

        # Validasi nama_vaksin
        nama_vaksin = request.POST.get('nama_vaksin')
        if not nama_vaksin or len(nama_vaksin) > 50:
            messages.error(request, "Nama vaksin tidak valid. Nama vaksin harus ada dan tidak lebih dari 50 karakter.")
            return redirect('merah:create_vaksin')
        
        # Validasi harga
        harga = request.POST.get('harga')
        try:
            harga = int(harga)
            if harga <= 0:
                messages.error(request, "Harga vaksin tidak valid. Harga harus lebih besar dari 0.")
                return redirect('merah:create_vaksin')
        except ValueError:
            messages.error(request, "Harga vaksin harus berupa angka.")
            return redirect('merah:create_vaksin')
        
        # Validasi stok
        stok = request.POST.get('stok')
        try:
            stok = int(stok)
            if stok < 0:
                messages.error(request, "Stok vaksin tidak valid. Stok tidak boleh kurang dari 0.")
                return redirect('merah:create_vaksin')
        except ValueError:
            messages.error(request, "Stok vaksin harus berupa angka.")
            return redirect('merah:create_vaksin')

        vaksin.append({
            "kode_vaksin": kode_vaksin,
            "nama_vaksin": nama_vaksin,
            "harga": harga,
            "stok": stok,
        })
        
        messages.success(request, "Vaksin berhasil ditambahkan.")
        return redirect('merah:show_vaksin')
    
    return render(request, 'create_vaksin.html')

def show_vaksin(request):
    logged_user = request.session.get('logged_user', None)
    all_vaccines = []

    if logged_user:
        search_query = request.GET.get('search_query', '').strip()

        sql = f'''
        SELECT * from vaksin 
        WHERE  stok > 0 AND harga > 0
        '''

        if search_query:
            sql += f" AND nama ILIKE '%{search_query.replace('%', '%%').replace('_', '__')}%'"
        
        sql += " ORDER BY kode desc;"
        all_vaccines = query(sql)
    else:
        messages.error(request, "Anda harus login atau memiliki role perawat untuk melihat data vaksin.")
        return redirect('putih:login')

    context = {
        "vaccines": all_vaccines if isinstance(all_vaccines, list) else [],
        'logged_user': logged_user
    }
    return render(request, 'show_vaksin.html', context)
    
def update_vaksin(request, kode_vaksin):
    vaksin_to_update = next((v for v in vaksin if str(v["kode_vaksin"]) == str(kode_vaksin)), None)

    if not vaksin_to_update:
        messages.error(request, "Vaksin tidak ditemukan.")
        return redirect('merah:show_vaksin')

    if request.method == 'POST':
        nama_vaksin = request.POST.get('nama_vaksin')
        harga = request.POST.get('harga')

        if not nama_vaksin or len(nama_vaksin) > 50:
            messages.error(request, "Nama vaksin tidak valid.")
            return redirect('merah:update_vaksin', kode_vaksin=kode_vaksin)

        try:
            harga = int(harga)
            if harga <= 0:
                raise ValueError
        except ValueError:
            messages.error(request, "Harga vaksin tidak valid.")
            return redirect('merah:update_vaksin', kode_vaksin=kode_vaksin)

        vaksin_to_update["nama_vaksin"] = nama_vaksin
        vaksin_to_update["harga"] = harga
        messages.success(request, "Vaksin berhasil diperbarui.")
        return redirect('merah:show_vaksin')

    return render(request, 'update_vaksin.html', {'vaksin': vaksin_to_update})

def update_stok_vaksin(request, kode_vaksin):
    vaksin_to_update = next((v for v in vaksin if str(v["kode_vaksin"]) == str(kode_vaksin)), None)

    if not vaksin_to_update:
        messages.error(request, "Vaksin tidak ditemukan.")
        return redirect('merah:show_vaksin')

    if request.method == 'POST':
        stok = request.POST.get('stok')

        stok = request.POST.get('stok')
        try:
            stok = int(stok)
            if stok < 0:
                messages.error(request, "Stok vaksin tidak valid. Stok tidak boleh kurang dari 0.")
                return redirect('merah:update_stok_vaksin')
        except ValueError:
            messages.error(request, "Stok vaksin harus berupa angka.")
            return redirect('merah:update_stok_vaksin')

        vaksin_to_update["stok"] = stok

        messages.success(request, "Stok vaksin berhasil diperbarui.")
        return redirect('merah:show_vaksin')

    return render(request, 'update_stok_vaksin.html', {'vaksin': vaksin_to_update})

def delete_vaksin(request, kode_vaksin):
    selected_vaksin = next((v for v in vaksin if v['kode_vaksin'] == kode_vaksin), None)
    
    if kode_vaksin:
        vaksin.remove(selected_vaksin)
        messages.success(request, f"Vaksin {selected_vaksin.get('nama_vaksin')} dengan ID {kode_vaksin} berhasil dihapus.")
    else:
        messages.error(request, "Vaksin tidak ditemukan.")

    return redirect('merah:show_vaksin')

# R VAKSIN FRONT DESK
def show_data_klien(request):
    logged_user = request.session.get('logged_user', None)
    if not logged_user or logged_user.get('role') != 'front_desk':
        messages.error(request, "Anda harus login atau memiliki role front desk untuk akses data klien.")
        return redirect('putih:login')
    
    search_query = request.GET.get('search_query', '').strip()

    sql_to_execute = """
        SELECT
            K.no_identitas,
            K.email,
            U.alamat, 
            U.nomor_telepon,
            I.nama_depan,
            I.nama_tengah,
            I.nama_belakang,
            P.nama_perusahaan,
            CASE
                WHEN P.no_identitas_klien IS NOT NULL THEN 'Perusahaan'
                ELSE 'Individu'
            END AS jenis,
            COALESCE(
                P.nama_perusahaan,
                TRIM(CONCAT_WS(' ', I.nama_depan, I.nama_tengah, I.nama_belakang))
            ) AS nama
        FROM
            KLIEN K
        LEFT JOIN
            "USER" U ON K.email = U.email  -- Join with USER table on email
        LEFT JOIN
            INDIVIDU I ON K.no_identitas = I.no_identitas_klien
        LEFT JOIN
            PERUSAHAAN P ON K.no_identitas = P.no_identitas_klien
    """


    if search_query:
        search_term = f"%{search_query.replace('%', '%%').replace('_', '__')}%"
        sql_to_execute += f"""
            WHERE (
                P.nama_perusahaan ILIKE '{search_term}' OR
                TRIM(CONCAT_WS(' ', I.nama_depan, I.nama_tengah, I.nama_belakang)) ILIKE '{search_term}'
            )
        """
    sql_to_execute += " ORDER BY nama;"
    clients = query(sql_to_execute)
    
    context = {
        "logged_user": logged_user,
        "clients": clients if clients else [],
        "search_query": search_query
    }
    return render(request, "show_data_klien.html", context)

def show_klien_detail(request, no_identitas):
    logged_user = request.session.get('logged_user', None)
    if not logged_user or logged_user.get('role') != 'front_desk':
        messages.error(request, "Anda harus login atau memiliki role front desk untuk akses data klien.")
        return redirect('putih:login')
    else:
        sql_client = """
            SELECT
                K.no_identitas,
                K.email,
                K.tanggal_registrasi,
                U.alamat,        
                U.nomor_telepon,
                I.nama_depan,
                I.nama_tengah,
                I.nama_belakang,
                P.nama_perusahaan,
                COALESCE(
                    P.nama_perusahaan,
                    TRIM(CONCAT_WS(' ', I.nama_depan, I.nama_tengah, I.nama_belakang))
                ) AS nama_lengkap,  -- Combined name for display
                CASE
                    WHEN P.no_identitas_klien IS NOT NULL THEN 'Perusahaan'
                    ELSE 'Individu'
                END AS jenis_klien
            FROM
                KLIEN K
            LEFT JOIN
                "USER" U ON K.email = U.email -- Join KLIEN with USER
            LEFT JOIN
                INDIVIDU I ON K.no_identitas = I.no_identitas_klien
            LEFT JOIN
                PERUSAHAAN P ON K.no_identitas = P.no_identitas_klien
            WHERE
                K.no_identitas = %s
        """

        sql_client = sql_client.replace("%s", f"'{str(no_identitas)}'")
        client_list = query(sql_client) 

        if not client_list:
            messages.error(request, "Data klien tidak ditemukan.")
            return redirect('putih:show_data_klien')

        client_info = client_list[0]
        sql_pets = """
            SELECT
                H.nama AS nama_hewan,
                JH.nama AS nama_jenis_hewan,
                H.tanggal_lahir
            FROM
                HEWAN H
            LEFT JOIN
                JENIS_HEWAN JH ON H.id_jenis = JH.id
            WHERE
                H.no_identitas_klien = %s
            ORDER BY
                H.nama;
        """

        sql_pets = sql_pets.replace("%s", f"'{str(no_identitas)}'")
        client_pets = query(sql_pets) 
        print(client_pets)

        context = {
            "logged_user": logged_user,
            "client": client_info,
            "pets": client_pets if client_pets else [],
        }
        return render(request, "show_klien_detail.html", context)
