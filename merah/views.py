from django.shortcuts import render
from putih.views import get_logged_user
from datetime import datetime

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
    "kode_vaksin": "VAK456",
    "tipe_kunjungan": "Pemeriksaan Umum",
    "timetamp_awal": datetime(2023,10,2,9,30,0),
    "timetamp_akhir": None,
    "suhu": 39.0,
    "berat_badan": 12.3
  },
  {
    "id_kunjungan": "KJN003",
    "no_identitas_klien": "112233445",
    "nama_hewan": "Kelinci",
    "no_front_desk": "FD125",
    "no_perawat_hewan": "PW3",
    "no_dokter_hewan": "DH3",
    "kode_vaksin": None,
    "tipe_kunjungan": "Sterilisasi",
    "timetamp_awal": "2023-10-03 14:00:00",
    "timetamp_akhir": "2023-10-03 15:30:00",
    "suhu": 38.0,
    "berat_badan": 2.5
  }
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
        "stok": 10,
    },
    
]

def show_vaksinasi(request):
    logged_pengguna = get_logged_user()
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