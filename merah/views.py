from django.shortcuts import redirect, render
from django.urls import reverse
from putih.views import get_logged_user
from datetime import datetime
from django.contrib import messages

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