from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from utils.query import query
import uuid
import json

def list_kunjungan(request):
    logged_user = request.session.get("logged_user", {})
    role = logged_user.get("role")
    no_identitas_klien = logged_user.get("no_identitas")

    if role == "klien_individu" or role == "klien_perusahaan":
        query_str = f"""
            SELECT k.id_kunjungan, k.no_identitas_klien, h.nama AS nama_hewan, k.tipe_kunjungan,
                   k.timestamp_awal, k.timestamp_akhir, k.suhu, k.berat_badan, k.catatan
            FROM KUNJUNGAN k
            JOIN HEWAN h ON k.nama_hewan = h.nama AND k.no_identitas_klien = h.no_identitas_klien
            WHERE k.no_identitas_klien = '{no_identitas_klien}'
            ORDER BY k.timestamp_awal DESC
        """
    else:
        query_str = """
            SELECT k.id_kunjungan, k.no_identitas_klien, h.nama AS nama_hewan, k.tipe_kunjungan,
                   k.timestamp_awal, k.timestamp_akhir, k.suhu, k.berat_badan, k.catatan
            FROM KUNJUNGAN k
            JOIN HEWAN h ON k.nama_hewan = h.nama AND k.no_identitas_klien = h.no_identitas_klien
            ORDER BY k.timestamp_awal DESC
        """

    kunjungan = query(query_str)

    context = {
        "kunjungan": kunjungan,
        "is_front_desk": role == "front_desk",
        "is_klien": role.startswith("klien") if role else False,
        "is_dokter": role == "dokter"
    }

    return render(request, "list_kunjungan.html", context)


def api_hewan_by_klien(request, no_identitas_klien):
    results = query(f"""
        SELECT nama FROM HEWAN WHERE no_identitas_klien = '{no_identitas_klien}'
    """)
    return JsonResponse(results, safe=False)

def create_kunjungan(request):
    logged_user = request.session.get("logged_user")
    if not logged_user or logged_user.get("role") != "front_desk":
        return redirect("hijau:list_kunjungan")

    if request.method == "POST":
        id_kunjungan = str(uuid.uuid4())
        nama_hewan = request.POST.get("nama_hewan")
        no_identitas_klien = request.POST.get("no_identitas_klien")
        no_perawat_hewan = request.POST.get("no_perawat_hewan")
        no_dokter_hewan = request.POST.get("no_dokter_hewan")
        tipe_kunjungan = request.POST.get("tipe_kunjungan")
        timestamp_awal = request.POST.get("timestamp_awal")
        timestamp_akhir = request.POST.get("timestamp_akhir") or None

        query(f"""
            INSERT INTO KUNJUNGAN (
                id_kunjungan, nama_hewan, no_identitas_klien, no_front_desk,
                no_perawat_hewan, no_dokter_hewan, tipe_kunjungan,
                timestamp_awal, timestamp_akhir
            ) VALUES (
                '{id_kunjungan}', '{nama_hewan}', '{no_identitas_klien}', '{logged_user.get("no_pegawai")}',
                '{no_perawat_hewan}', '{no_dokter_hewan}', '{tipe_kunjungan}',
                '{timestamp_awal}', {f"'{timestamp_akhir}'" if timestamp_akhir else "NULL"}
            )
        """)
        return redirect("hijau:list_kunjungan")

    # Ambil daftar klien dengan nama gabungan dari INDIVIDU / PERUSAHAAN
    daftar_klien = query("""
        SELECT 
            k.no_identitas,
            CASE
                WHEN i.nama_depan IS NOT NULL THEN 
                    TRIM(CONCAT(i.nama_depan, ' ', COALESCE(i.nama_tengah, ''), ' ', i.nama_belakang))
                WHEN p.nama_perusahaan IS NOT NULL THEN 
                    p.nama_perusahaan
                ELSE NULL
            END AS nama
        FROM KLIEN k
        LEFT JOIN INDIVIDU i ON k.no_identitas = i.no_identitas_klien
        LEFT JOIN PERUSAHAAN p ON k.no_identitas = p.no_identitas_klien
        WHERE i.nama_depan IS NOT NULL OR p.nama_perusahaan IS NOT NULL
    """)

    daftar_dokter = query("SELECT d.no_dokter_hewan, p.email_user as email FROM DOKTER_HEWAN d JOIN PEGAWAI p ON d.no_dokter_hewan = p.no_pegawai")
    daftar_perawat = query("SELECT p.no_perawat_hewan, pe.email_user as email FROM PERAWAT_HEWAN p JOIN PEGAWAI pe ON p.no_perawat_hewan = pe.no_pegawai")

    print(daftar_dokter)
    print(daftar_perawat)
    return render(request, "create_kunjungan.html", {
        "daftar_klien": daftar_klien,
        "daftar_dokter": daftar_dokter,
        "daftar_perawat": daftar_perawat,
    })

def update_kunjungan(request, id_kunjungan):
    logged_user = request.session.get("logged_user")
    if not logged_user or logged_user.get("role") != "front_desk":
        return redirect("hijau:list_kunjungan")

    if request.method == "POST":
        nama_hewan = request.POST.get("nama_hewan")
        no_identitas_klien = request.POST.get("no_identitas_klien")
        no_perawat_hewan = request.POST.get("no_perawat_hewan")
        no_dokter_hewan = request.POST.get("no_dokter_hewan")
        tipe_kunjungan = request.POST.get("tipe_kunjungan")
        timestamp_awal = request.POST.get("timestamp_awal")
        timestamp_akhir = request.POST.get("timestamp_akhir") or None

        query(f"""
            UPDATE KUNJUNGAN
            SET nama_hewan = '{nama_hewan}',
                no_identitas_klien = '{no_identitas_klien}',
                no_perawat_hewan = '{no_perawat_hewan}',
                no_dokter_hewan = '{no_dokter_hewan}',
                tipe_kunjungan = '{tipe_kunjungan}',
                timestamp_awal = '{timestamp_awal}',
                timestamp_akhir = {f"'{timestamp_akhir}'" if timestamp_akhir else "NULL"}
            WHERE id_kunjungan = '{id_kunjungan}'
        """)

        return redirect("hijau:list_kunjungan")

    # --- GET request: tampilkan form dengan data awal ---
    data = query(f"""
        SELECT id_kunjungan, nama_hewan, no_identitas_klien, no_dokter_hewan,
               no_perawat_hewan, tipe_kunjungan, timestamp_awal, timestamp_akhir
        FROM KUNJUNGAN
        WHERE id_kunjungan = '{id_kunjungan}'
    """)[0]

    # daftar hewan yang dimiliki klien saat ini (agar dropdown tidak kosong saat halaman pertama dibuka)
    daftar_hewan = query(f"""
        SELECT nama FROM HEWAN WHERE no_identitas_pemilik = '{data['no_identitas_klien']}'
    """)

    daftar_klien = query("""
        SELECT 
            k.no_identitas,
            CASE
                WHEN i.nama_depan IS NOT NULL THEN 
                    TRIM(CONCAT(i.nama_depan, ' ', COALESCE(i.nama_tengah, ''), ' ', i.nama_belakang))
                WHEN p.nama_perusahaan IS NOT NULL THEN 
                    p.nama_perusahaan
                ELSE NULL
            END AS nama
        FROM KLIEN k
        LEFT JOIN INDIVIDU i ON k.no_identitas = i.no_identitas_klien
        LEFT JOIN PERUSAHAAN p ON k.no_identitas = p.no_identitas_klien
        WHERE i.nama_depan IS NOT NULL OR p.nama_perusahaan IS NOT NULL
    """)

    daftar_dokter = query("""SELECT d.no_dokter_hewan, p.email_user as email FROM DOKTER_HEWAN d JOIN PEGAWAI p ON d.no_dokter_hewan = p.no_pegawai""")

    daftar_perawat = query("""SELECT p.no_perawat_hewan, pe.email_user as email FROM PERAWAT_HEWAN p JOIN PEGAWAI pe ON p.no_perawat_hewan = pe.no_pegawai""")

    context = {
        "data": data,
        "daftar_klien": daftar_klien,
        "daftar_dokter": daftar_dokter,
        "daftar_perawat": daftar_perawat,
        "daftar_hewan": daftar_hewan,
    }
    print(daftar_klien)

    return render(request, "update_kunjungan.html", context)


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
    logged_user = request.session.get("logged_user", {})
    role = logged_user.get("role")
    email_user = logged_user.get("email")

    query_str = """
        SELECT 
            kkp.id_kunjungan,
            kkp.no_identitas_klien,
            kkp.nama_hewan,
            pr.email_user AS email_perawat,
            dk.email_user AS email_dokter,
            fd.email_user AS email_frontdesk,
            p.kode_perawatan,
            p.nama_perawatan

        FROM KUNJUNGAN_KEPERAWATAN kkp
        JOIN PERAWAT_HEWAN prh ON kkp.no_perawat_hewan = prh.no_perawat_hewan
        JOIN TENAGA_MEDIS tmpr ON prh.no_perawat_hewan = tmpr.no_tenaga_medis
        JOIN PEGAWAI pr ON tmpr.no_tenaga_medis = pr.no_pegawai

        JOIN DOKTER_HEWAN dkh ON kkp.no_dokter_hewan = dkh.no_dokter_hewan
        JOIN TENAGA_MEDIS tmdk ON dkh.no_dokter_hewan = tmdk.no_tenaga_medis
        JOIN PEGAWAI dk ON tmdk.no_tenaga_medis = dk.no_pegawai

        JOIN FRONT_DESK fdo ON kkp.no_front_desk = fdo.no_front_desk
        JOIN PEGAWAI fd ON fdo.no_front_desk = fd.no_pegawai

        JOIN PERAWATAN p ON kkp.kode_perawatan = p.kode_perawatan
    """

    if role and role.startswith("klien"):
        no_identitas_klien = logged_user.get("no_identitas")
        query_str += f" WHERE kkp.no_identitas_klien = '{no_identitas_klien}'"

    result = query(query_str)

    # Format kolom
    for r in result:
        r["email_dokter"] = f"Dr. {r['email_dokter'].split('@')[0].capitalize()}"
        r["email_perawat"] = r["email_perawat"].split('@')[0].capitalize()
        r["email_frontdesk"] = r["email_frontdesk"].split('@')[0].capitalize()
        r["jenis_perawatan"] = f"{r['kode_perawatan']} - {r['nama_perawatan']}"

        print(r["email_perawat"])
    
    # print perawat hewan
    

    return render(request, "list_treatment.html", {
        "treatment": result,
        "is_dokter": role == "dokter"
    })

def create_treatment(request):
    logged_user = request.session.get("logged_user")
    if not logged_user or logged_user.get("role") != "dokter":
        messages.error(request, "Hanya dokter hewan yang dapat menambahkan treatment.")
        return redirect("hijau:list_perawatan")

    if request.method == "POST":
        id_kunjungan = request.POST.get("id_kunjungan")
        kode_perawatan = request.POST.get("kode_perawatan")

        # Dapatkan data kunjungan
        kunjungan = query(f"""
            SELECT * FROM KUNJUNGAN WHERE id_kunjungan = '{id_kunjungan}'
        """)
        if not kunjungan:
            messages.error(request, "Kunjungan tidak ditemukan.")
            return redirect("hijau:create_treatment")

        k = kunjungan[0]
        # Simpan ke tabel KUNJUNGAN_KEPERAWATAN
        query(f"""
            INSERT INTO KUNJUNGAN_KEPERAWATAN (
                id_kunjungan, nama_hewan, no_identitas_klien,
                no_front_desk, no_perawat_hewan, no_dokter_hewan,
                kode_perawatan
            ) VALUES (
                '{k["id_kunjungan"]}', '{k["nama_hewan"]}', '{k["no_identitas_klien"]}',
                '{k["no_front_desk"]}', '{k["no_perawat_hewan"]}', '{k["no_dokter_hewan"]}',
                '{kode_perawatan}'
            )
        """)
        messages.success(request, "Treatment berhasil ditambahkan.")
        return redirect("hijau:list_perawatan")

    # Ambil semua kunjungan (opsional: bisa dibatasi hanya yang belum punya perawatan)
    daftar_kunjungan = query("""
        SELECT id_kunjungan, nama_hewan, no_identitas_klien FROM KUNJUNGAN
    """)

    daftar_perawatan = query("""
        SELECT kode_perawatan, nama_perawatan FROM PERAWATAN
    """)

    return render(request, "create_treatment.html", {
        "daftar_kunjungan": daftar_kunjungan,
        "daftar_perawatan": daftar_perawatan,
    })


def delete_treatment(request, id_kunjungan, kode_perawatan):
    logged_user = request.session.get("logged_user")
    if not logged_user or logged_user.get("role") != "dokter":
        messages.error(request, "Hanya dokter yang dapat menghapus perawatan.")
        return redirect("hijau:list_perawatan")

    query(f"""
        DELETE FROM KUNJUNGAN_KEPERAWATAN
        WHERE id_kunjungan = '{id_kunjungan}' AND kode_perawatan = '{kode_perawatan}'
    """)
    messages.success(request, "Perawatan berhasil dihapus.")
    return redirect("hijau:list_perawatan")

def update_treatment(request, id_kunjungan, kode_perawatan):
    logged_user = request.session.get("logged_user")
    if not logged_user or logged_user.get("role") != "dokter":
        messages.error(request, "Akses ditolak.")
        return redirect("hijau:list_perawatan")

    if request.method == "POST":
        kode_perawatan_baru = request.POST.get("kode_perawatan")

        # Update kode_perawatan
        query(f"""
            UPDATE KUNJUNGAN_KEPERAWATAN
            SET kode_perawatan = '{kode_perawatan_baru}'
            WHERE id_kunjungan = '{id_kunjungan}' AND kode_perawatan = '{kode_perawatan}'
        """)
        messages.success(request, "Perawatan berhasil diperbarui.")
        return redirect("hijau:list_perawatan")

    # Load data perawatan & list untuk dropdown
    data = query(f"""
        SELECT * FROM KUNJUNGAN_KEPERAWATAN
        WHERE id_kunjungan = '{id_kunjungan}' AND kode_perawatan = '{kode_perawatan}'
    """)[0]
    daftar_perawatan = query("SELECT kode_perawatan, nama_perawatan FROM PERAWATAN")

    return render(request, "update_treatment.html", {
        "data": data,
        "daftar_perawatan": daftar_perawatan,
    })


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
