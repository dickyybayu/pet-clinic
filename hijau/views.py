from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from utils.query import query
import uuid
import json

def list_kunjungan(request):
    print("DEBUG: logged_user =", request.session.get('logged_user'))
    context = {
        'kunjungan': query("""
            SELECT id_kunjungan, nama_hewan, no_identitas_klien, tipe_kunjungan, timestamp_awal, timestamp_akhir, suhu, berat_badan, catatan
            FROM KUNJUNGAN
            ORDER BY timestamp_awal DESC
        """),
        'is_front_desk': request.session.get('logged_user', {}).get('role') == 'front_desk'
    }
    return render(request, "list_kunjungan.html", context)

def create_kunjungan(request):
    logged_user = request.session.get("logged_user")
    if not logged_user or logged_user.get("role") != "front_desk":
        return redirect("putih:list_kunjungan")

    if request.method == "POST":
        id_kunjungan = str(uuid.uuid4())
        nama_hewan = request.POST.get("nama_hewan")
        no_identitas_klien = request.POST.get("no_identitas_klien")
        no_perawat_hewan = request.POST.get("no_perawat_hewan")
        no_dokter_hewan = request.POST.get("no_dokter_hewan")
        tipe_kunjungan = request.POST.get("tipe_kunjungan")
        timestamp_awal = request.POST.get("timestamp_awal")
        kode_vaksin = request.POST.get("kode_vaksin") or None
        suhu = request.POST.get("suhu") or None
        berat_badan = request.POST.get("berat_badan") or None
        catatan = request.POST.get("catatan") or None

        insert_result = query(f"""
            INSERT INTO KUNJUNGAN (
              id_kunjungan, nama_hewan, no_identitas_klien, no_front_desk,
              no_perawat_hewan, no_dokter_hewan, kode_vaksin,
              tipe_kunjungan, timestamp_awal, suhu, berat_badan
            )
            VALUES (
              '{id_kunjungan}', '{nama_hewan}', '{no_identitas_klien}', '{logged_user.get("no_pegawai")}',
              '{no_perawat_hewan}', '{no_dokter_hewan}', {f"'{kode_vaksin}'" if kode_vaksin else "NULL"},
              '{tipe_kunjungan}', '{timestamp_awal}', {int(suhu) if suhu else "NULL"}, {float(berat_badan) if berat_badan else "NULL"},
                '{catatan}'
            )
        """)
        return redirect("hijau:list_kunjungan")

    return render(request, "create_kunjungan.html")

def update_kunjungan(request, id_kunjungan):
    if request.method == "POST":
        data = json.loads(request.body)
        timestamp_akhir = data.get('timestamp_akhir')
        query(f"""
            UPDATE KUNJUNGAN
            SET timestamp_akhir = '{timestamp_akhir}'
            WHERE id_kunjungan = '{id_kunjungan}'
        """)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'invalid method'})

def delete_kunjungan(request, id_kunjungan):
    logged_user = request.session.get("logged_user")
    if not logged_user or logged_user.get("role") != "front_desk":
        return redirect("hijau:list_kunjungan")

    if request.method == "POST":
        query(f"DELETE FROM KUNJUNGAN WHERE id_kunjungan = '{id_kunjungan}'")
        messages.success(request, "Kunjungan berhasil dihapus.")
        return redirect("hijau:list_kunjungan")

    return render(request, "confirm_delete_kunjungan.html", {'id_kunjungan': id_kunjungan})

def list_perawatan(request):
    perawatan = query("SELECT * FROM PERAWATAN")
    return render(request, 'list_perawatan.html', {'perawatan': perawatan})

def show_rekam_medis(request, id_kunjungan):
    kunjungan = query(f"SELECT suhu, berat_badan, catatan FROM KUNJUNGAN WHERE id_kunjungan = '{id_kunjungan}'")
    if not kunjungan:
        return render(request, "404.html", status=404)

    data = kunjungan[0]
    is_available = data['suhu'] is not None and data['berat_badan'] is not None and data['catatan']

    return render(request, "rekam_medis_detail.html", {
        'id_kunjungan': id_kunjungan,
        'data': data,
        'is_available': is_available
    })

def create_rekam_medis(request, id_kunjungan):
    logged_user = request.session.get("logged_user")
    if not logged_user or logged_user.get("role") != "dokter":
        messages.error(request, "Akses ditolak. Hanya dokter hewan yang dapat mengisi rekam medis.")
        return redirect("hijau:list_kunjungan")
    
    if request.method == "POST":
        suhu = request.POST.get("suhu_tubuh")
        berat = request.POST.get("berat_badan")
        catatan = request.POST.get("catatan")

        if not all([suhu, berat, catatan]):
            messages.error(request, "Semua field wajib diisi.")
            return redirect('hijau:create_rekam_medis', id_kunjungan=id_kunjungan)

        query(f"""
            UPDATE KUNJUNGAN
            SET suhu = {int(suhu)},
                berat_badan = {float(berat)},
                catatan = '{catatan}'
            WHERE id_kunjungan = '{id_kunjungan}'
        """)
        return redirect('hijau:show_rekam_medis', id_kunjungan=id_kunjungan)

    return render(request, 'create_rekam_medis.html', {'id_kunjungan': id_kunjungan})

# def create_or_update_rekam_medis(request):
#     if request.method == "POST":
#         data = json.loads(request.body)
#         q = f"""
#             INSERT INTO KUNJUNGAN_KEPERAWATAN (
#                 id_kunjungan, nama_hewan, no_identitas_klien,
#                 no_front_desk, no_perawat_hewan, no_dokter_hewan,
#                 kode_perawatan, catatan
#             ) VALUES (
#                 '{data["id_kunjungan"]}', '{data["nama_hewan"]}', '{data["no_identitas_klien"]}',
#                 '{data["no_front_desk"]}', '{data["no_perawat_hewan"]}', '{data["no_dokter_hewan"]}',
#                 '{data["kode_perawatan"]}', '{data["catatan"]}'
#             )
#             ON CONFLICT (id_kunjungan, nama_hewan, no_identitas_klien,
#                          no_front_desk, no_perawat_hewan, no_dokter_hewan, kode_perawatan)
#             DO UPDATE SET catatan = EXCLUDED.catatan
#         """
#         query(q)
#         return JsonResponse({'status': 'success'})
#     return JsonResponse({'status': 'invalid method'})
