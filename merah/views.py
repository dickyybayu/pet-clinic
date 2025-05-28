from django.shortcuts import redirect, render
from django.urls import reverse
from datetime import datetime
from django.contrib import messages
import uuid


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
#dummy data 
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

def show_vaksinasi(request):
    logged_pengguna = logged_doctor
    print(logged_pengguna)
    context = []
    for kunj in kunjungan:
        if kunj['kode_vaksin']:
            if kunj['no_dokter_hewan'] == logged_pengguna.get('doctor_id'):
                for vak in vaksin:
                    if vak['kode_vaksin'] == kunj['kode_vaksin']:
                        context.append({
                            "id_kunjungan": kunj['id_kunjungan'],
                            "timetamp_awal": kunj['timetamp_awal'],
                            "kode_vaksin": vak['kode_vaksin'],
                            "nama_vaksin": vak['nama_vaksin'],
                        })
    print(context)
    return render(request, 'show_vaksinasi.html', {'vaksin_data': context})

def create_vaksinasi(request):
    logged_pengguna = logged_doctor

    if request.method == 'POST':
        selected_kunjungan = request.POST.get('selected_kunjungan')
        selected_vaksin = request.POST.get('selected_vaksin')

        vaksin_terpilih = next((v for v in vaksin if v['kode_vaksin'] == selected_vaksin), None)
        if not vaksin_terpilih or vaksin_terpilih['stok'] <= 0:
            messages.error(request, "Vaksin tidak tersedia")
            return redirect('merah:create_vaksinasi')

        for kunj in kunjungan:
            if kunj['id_kunjungan'] == selected_kunjungan:
                kunj['kode_vaksin'] = selected_vaksin
                vaksin_terpilih['stok'] -= 1
                messages.success(request, "Vaksinasi berhasil ditambahkan")
                return redirect('merah:show_vaksinasi')

    vaksin_list = [v for v in vaksin]

    kunjungan_list = [
        {
            'id_kunjungan': k['id_kunjungan'],
            'nama_hewan': k['nama_hewan']
        }
        for k in kunjungan
        if k['no_dokter_hewan'] == logged_pengguna.get('doctor_id') and not k.get('kode_vaksin')
    ]

    context = {
        'vaksin': vaksin_list,
        'kunjungan': kunjungan_list,
    }
    return render(request, 'create_vaksinasi.html', context)

def update_vaksinasi(request, id_kunjungan):
    logged_pengguna = logged_doctor

    kunj = next(
        (k for k in kunjungan if k['id_kunjungan'] == id_kunjungan and k['no_dokter_hewan'] == logged_pengguna.get('doctor_id')),
        None
    )

    if not kunj:
        messages.error(request, "Kunjungan tidak ditemukan atau Anda tidak memiliki akses.")
        return redirect('merah:show_vaksinasi')

    if request.method == 'POST':
        selected_vaksin_id = request.POST.get('selected_vaksin')

        # Ambil objek vaksin yang dipilih
        vaksin_baru = next((v for v in vaksin if v['kode_vaksin'] == selected_vaksin_id), None)
        if not vaksin_baru:
            messages.error(request, "Vaksin yang dipilih tidak ditemukan.")
            return redirect(reverse('merah:update_vaksinasi', args=[id_kunjungan]))

        if vaksin_baru['stok'] <= 0:
            messages.error(request, "Vaksin yang dipilih sedang tidak tersedia (stok 0).")
            return redirect(reverse('merah:update_vaksinasi', args=[id_kunjungan]))

        vaksin_lama_kode = kunj.get('kode_vaksin')
        # Tambah stok vaksin lama jika ada
        if vaksin_lama_kode:
            vaksin_lama = next((v for v in vaksin if v['kode_vaksin'] == vaksin_lama_kode), None)
            if vaksin_lama:
                vaksin_lama['stok'] += 1

        # Update vaksinasi
        kunj['kode_vaksin'] = selected_vaksin_id
        vaksin_baru['stok'] -= 1

        messages.success(request, f"Vaksinasi kunjungan {id_kunjungan} berhasil diperbarui.")
        return redirect('merah:show_vaksinasi')

    context = {
        'vaksin': vaksin,
        'id_kunjungan': kunj.get('id_kunjungan'),
    }
    return render(request, 'update_vaksinasi.html', context)

def delete_vaksinasi(request, id_kunjungan):
    selected_kunjungan = next((k for k in kunjungan if k['id_kunjungan'] == id_kunjungan), None)
    
    if selected_kunjungan:
        selected_kunjungan['kode_vaksin'] = None
        messages.success(request, f"Vaksinasi dengan ID Kunjungan {id_kunjungan} berhasil dihapus.")
    else:
        messages.error(request, "Kunjungan tidak ditemukan.")

    return redirect('merah:show_vaksinasi')

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
    all_vaccines = []
    for vaccine in vaksin:
        vaccine['is_used'] = is_vaksin_used(vaccine['kode_vaksin'])
        all_vaccines.append(vaccine)

    return render(request, 'show_vaksin.html', {'vaccines': all_vaccines})
    
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

def show_data_klien(request):
    for client in clients:
        if "company_name" in client:
            client["jenis"] = "Perusahaan"
            client["nama"] = client["company_name"]
        else:
            client["jenis"] = "Individu"
            client["nama"] = f"{client['first_name']} {client['middle_name']} {client['last_name']}"

    return render(request, "show_data_klien.html", {"clients": clients})

def show_klien_detail(request, no_identitas):
    client = next((c for c in clients if c["no_identitas"] == no_identitas), None)
    client_info = {k: v for k, v in client.items() if k != "password"}
    if "company_name" in client:
        client["nama"] = client["company_name"]
    else:
        client["nama"] = f"{client['first_name']} {client['middle_name']} {client['last_name']}"

    client_pets = [pet for pet in pets if pet["no_identitas_klien"] == no_identitas]
    for pet in client_pets:
        jenis = next((j for j in jenis_hewan if j["id"] == pet["id_jenis"]), {"nama_jenis": "Tidak diketahui"})
        pet["nama_jenis"] = jenis["nama_jenis"]

    return render(request, "show_klien_detail.html", {
        "client": client_info,
        "pets": client_pets,
    })