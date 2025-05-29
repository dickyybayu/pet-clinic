import uuid
from django.shortcuts import render, redirect
from django.http import HttpResponseBadRequest, HttpResponseForbidden, HttpResponseNotFound
from utils.query import query


DUMMY_JENIS_HEWAN = [
    {'id': 'HWN001', 'nama': 'Kucing', 'bisa_dihapus': True},
    {'id': 'HWN002', 'nama': 'Anjing', 'bisa_dihapus': True},
    {'id': 'HWN003', 'nama': 'Hamster', 'bisa_dihapus': False},
]

DUMMY_KLIEN = [
    {'id': 'klien1', 'nama': 'John Doe'},
    {'id': 'klien2', 'nama': 'PT Pecinta Kucing'},
]

DUMMY_HEWAN = [
    {
        'id': 'H001',
        'pemilik': 'John Doe',
        'jenis': 'Kucing',
        'nama': 'Snowy',
        'tanggal_lahir': '2020-02-09',
        'url_foto': 'https://example.com/kucing.jpg',
    },
    {
        'id': 'H002',
        'pemilik': 'PT Aku Sayang Hewan',
        'jenis': 'Anjing',
        'nama': 'Blacky',
        'tanggal_lahir': '2019-11-15',
        'url_foto': 'https://example.com/anjing.jpg',
    },
    {
        'id': 'H003',
        'pemilik': 'PT Pecinta Kucing',
        'jenis': 'Hamster',
        'nama': 'Hamseung',
        'tanggal_lahir': '2024-10-15',
        'url_foto': 'https://example.com/hamster.jpg',
    },
]

def list_jenis_hewan(request):
    logged_user = request.session.get('logged_user')
    if not logged_user:
        return redirect('login')

    if logged_user['role'] not in ['front_desk', 'dokter']:
        return HttpResponseForbidden("You don't have permission to access this page.")

    jenis_query = "SELECT id, nama FROM JENIS_HEWAN ORDER BY id ASC"
    jenis_data = query(jenis_query)

    jenis_hewan_list = []
    for row in jenis_data:
        id_jenis = row['id']
        nama = row['nama']

        count_query = f"SELECT COUNT(*) FROM HEWAN WHERE id_jenis = '{id_jenis}'"
        jumlah_hewan = query(count_query)[0]['count']

        jenis_hewan_list.append({
            'id': id_jenis,
            'nama': nama,
            'bisa_dihapus': jumlah_hewan == 0
        })

    context = {
        'role': logged_user['role'],
        'jenis_hewan_list': jenis_hewan_list
    }
    return render(request, 'list_jenis_hewan.html', context)

def create_jenis_hewan(request):
    logged_user = request.session.get('logged_user')
    if not logged_user or logged_user['role'] != 'front_desk':
        return HttpResponseForbidden("Akses hanya untuk Front-Desk Officer.")

    if request.method == 'POST':
        nama = request.POST.get('nama')

        if not nama or nama.strip() == "":
            return render(request, 'create_jenis_hewan.html', {
                'error': 'Nama tidak boleh kosong.'
            })

        new_id = str(uuid.uuid4())
        insert_query = f"""
            INSERT INTO JENIS_HEWAN (id, nama)
            VALUES ('{new_id}', '{nama}')
        """

        result = query(insert_query)

        if isinstance(result, dict) and result.get("status") == "error":
            return render(request, 'create_jenis_hewan.html', {
                'error': result["data"]
            })

        return redirect('kuning:jenis_list')

    return render(request, 'create_jenis_hewan.html')

def update_jenis_hewan(request, id_jenis):
    logged_user = request.session.get('logged_user')
    if not logged_user or logged_user['role'] != 'front_desk':
        return HttpResponseForbidden("Akses hanya untuk Front-Desk Officer.")

    select_query = f"SELECT * FROM JENIS_HEWAN WHERE id = '{id_jenis}'"
    jenis_result = query(select_query)

    if not jenis_result:
        return HttpResponseNotFound("Jenis hewan tidak ditemukan.")

    jenis = jenis_result[0]

    if request.method == 'POST':
        nama_baru = request.POST.get('nama')

        if not nama_baru or nama_baru.strip() == "":
            return render(request, 'update_jenis_hewan.html', {
                'error': 'Nama tidak boleh kosong.',
                'jenis': jenis
            })

        check_query = f"""
            SELECT COUNT(*) FROM JENIS_HEWAN
            WHERE LOWER(nama) = LOWER('{nama_baru}') AND id != '{id_jenis}'
        """
        count = query(check_query)[0]['count']
        if count > 0:
            return render(request, 'update_jenis_hewan.html', {
                'error': 'Nama tersebut sudah digunakan oleh jenis lain.',
                'jenis': jenis
            })

        update_query = f"""
            UPDATE JENIS_HEWAN SET nama = '{nama_baru}' WHERE id = '{id_jenis}'
        """
        query(update_query)
        return redirect('kuning:jenis_list')

    return render(request, 'update_jenis_hewan.html', {'jenis': jenis})

def delete_jenis_hewan(request, id_jenis):
    logged_user = request.session.get('logged_user')
    if not logged_user or logged_user['role'] != 'front_desk':
        return HttpResponseForbidden("Akses hanya untuk Front-Desk Officer.")

    check_query = f"""
        SELECT COUNT(*) FROM HEWAN WHERE id_jenis = '{id_jenis}'
    """
    count = query(check_query)[0]['count']

    if count > 0:
        return redirect('kuning:jenis_list')

    if request.method == 'POST':
        delete_query = f"""
            DELETE FROM JENIS_HEWAN WHERE id = '{id_jenis}'
        """
        query(delete_query)
        return redirect('kuning:jenis_list')

    return render(request, 'delete_jenis_hewan.html', {
        'id_jenis': id_jenis
    })

def list_hewan(request):
    logged_user = request.session.get('logged_user')
    if not logged_user:
        return redirect('login')

    role = logged_user['role']
    email = logged_user['email']

    klien_identitas = None
    if role in ['klien_individu', 'klien_perusahaan']:
        klien_result = query(f"SELECT no_identitas FROM KLIEN WHERE email = '{email}'")
        if not klien_result:
            return HttpResponseNotFound("Klien tidak ditemukan.")
        klien_identitas = klien_result[0]['no_identitas']

    sql = f"""
        SELECT
            h.nama AS nama_hewan,
            h.no_identitas_klien AS klien_id,
            jh.nama AS jenis_hewan,
            h.tanggal_lahir,
            h.url_foto,
            COALESCE(
                i.nama_depan || ' ' || COALESCE(i.nama_tengah || ' ', '') || i.nama_belakang,
                p.nama_perusahaan
            ) AS pemilik
        FROM HEWAN h
        JOIN JENIS_HEWAN jh ON h.id_jenis = jh.id
        JOIN KLIEN k ON h.no_identitas_klien = k.no_identitas
        LEFT JOIN INDIVIDU i ON i.no_identitas_klien = k.no_identitas
        LEFT JOIN PERUSAHAAN p ON p.no_identitas_klien = k.no_identitas
    """

    if role in ['klien_individu', 'klien_perusahaan']:
        sql += f" WHERE h.no_identitas_klien = '{klien_identitas}'"

    sql += " ORDER BY pemilik ASC, jh.nama ASC, h.nama ASC"

    hewan_list = query(sql)

    context = {
        'role': 'Front-Desk Officer' if role == 'front_desk' else 'Klien',
        'hewan_list': hewan_list,
    }
    return render(request, 'list_hewan.html', context)

def create_hewan(request):
    logged_user = request.session.get('logged_user')
    if not logged_user:
        return redirect('login')

    role = logged_user['role']
    email = logged_user['email']

    jenis_list = query("SELECT id, nama FROM JENIS_HEWAN ORDER BY nama ASC")

    if role in ['klien_individu', 'klien_perusahaan']:
        klien_result = query("SELECT no_identitas FROM KLIEN WHERE email = '%s'" % email)
        if not klien_result:
            return HttpResponseBadRequest("Klien tidak ditemukan.")
        no_identitas_klien = klien_result[0]['no_identitas']
        klien_list = query("""
            SELECT no_identitas, 
                   COALESCE(i.nama_depan || ' ' || COALESCE(i.nama_tengah || ' ', '') || i.nama_belakang, 
                            p.nama_perusahaan) AS nama_klien
            FROM KLIEN k
            LEFT JOIN INDIVIDU i ON i.no_identitas_klien = k.no_identitas
            LEFT JOIN PERUSAHAAN p ON p.no_identitas_klien = k.no_identitas
            WHERE k.no_identitas = '%s'
        """ % no_identitas_klien)
    else:
        klien_list = query("""
            SELECT k.no_identitas, 
                   COALESCE(i.nama_depan || ' ' || COALESCE(i.nama_tengah || ' ', '') || i.nama_belakang, 
                            p.nama_perusahaan) AS nama_klien
            FROM KLIEN k
            LEFT JOIN INDIVIDU i ON i.no_identitas_klien = k.no_identitas
            LEFT JOIN PERUSAHAAN p ON p.no_identitas_klien = k.no_identitas
            ORDER BY nama_klien ASC
        """)

    if request.method == 'POST':
        nama = request.POST.get('nama')
        tanggal_lahir = request.POST.get('tanggal_lahir')
        id_jenis = request.POST.get('id_jenis')
        url_foto = request.POST.get('url_foto')
        pemilik_id = request.POST.get('pemilik_id') if role not in ['klien_individu', 'klien_perusahaan'] else no_identitas_klien

        if not all([nama, tanggal_lahir, id_jenis, url_foto, pemilik_id]):
            return HttpResponseBadRequest("Semua field harus diisi.")

        cek_duplikat = query(f"""
            SELECT 1 FROM HEWAN 
            WHERE nama = '{nama}' AND no_identitas_klien = '{pemilik_id}'
        """)
        if cek_duplikat:
            return HttpResponseBadRequest("Nama hewan ini sudah digunakan oleh klien yang sama.")

        insert_query = f"""
            INSERT INTO HEWAN (nama, no_identitas_klien, tanggal_lahir, id_jenis, url_foto)
            VALUES ('{nama}', '{pemilik_id}', '{tanggal_lahir}', '{id_jenis}', '{url_foto}')
        """
        query(insert_query)

        return redirect('kuning:hewan_list')

    context = {
        'role': role,
        'daftar_klien': klien_list,
        'daftar_jenis': jenis_list,
    }
    return render(request, 'create_hewan.html', context)

def update_hewan(request, nama_hewan, no_identitas_klien):
    logged_user = request.session.get('logged_user')
    if not logged_user:
        return redirect('login')

    role = logged_user['role']
    email = logged_user['email']

    fetch_hewan_query = f"""
        SELECT * FROM HEWAN
        WHERE nama = '{nama_hewan}' AND no_identitas_klien = '{no_identitas_klien}'
    """
    result = query(fetch_hewan_query)
    if not result:
        return HttpResponseNotFound("Data hewan tidak ditemukan.")
    hewan = result[0]

    pemilik_result = query(f"""
        SELECT 
            COALESCE(i.nama_depan || ' ' || COALESCE(i.nama_tengah || ' ', '') || i.nama_belakang, 
                     p.nama_perusahaan) AS nama_klien
        FROM KLIEN k
        LEFT JOIN INDIVIDU i ON i.no_identitas_klien = k.no_identitas
        LEFT JOIN PERUSAHAAN p ON p.no_identitas_klien = k.no_identitas
        WHERE k.no_identitas = '{no_identitas_klien}'
    """)
    hewan['pemilik'] = pemilik_result[0]['nama_klien'] if pemilik_result else 'Tidak diketahui'

    jenis_list = query("SELECT id, nama FROM JENIS_HEWAN ORDER BY nama ASC")

    if role in ['klien_individu', 'klien_perusahaan']:
        klien_list = query(f"""
            SELECT k.no_identitas, 
                   COALESCE(i.nama_depan || ' ' || COALESCE(i.nama_tengah || ' ', '') || i.nama_belakang, 
                            p.nama_perusahaan) AS nama_klien
            FROM KLIEN k
            LEFT JOIN INDIVIDU i ON i.no_identitas_klien = k.no_identitas
            LEFT JOIN PERUSAHAAN p ON p.no_identitas_klien = k.no_identitas
            WHERE k.email = '{email}'
        """)
    else:
        klien_list = query("""
            SELECT k.no_identitas, 
                   COALESCE(i.nama_depan || ' ' || COALESCE(i.nama_tengah || ' ', '') || i.nama_belakang, 
                            p.nama_perusahaan) AS nama_klien
            FROM KLIEN k
            LEFT JOIN INDIVIDU i ON i.no_identitas_klien = k.no_identitas
            LEFT JOIN PERUSAHAAN p ON p.no_identitas_klien = k.no_identitas
            ORDER BY nama_klien ASC
        """)

    if request.method == 'POST':
        new_nama = request.POST.get('nama')
        tanggal_lahir = request.POST.get('tanggal_lahir')
        id_jenis = request.POST.get('id_jenis')
        url_foto = request.POST.get('url_foto')
        pemilik_id = request.POST.get('pemilik_id') if role not in ['klien_individu', 'klien_perusahaan'] else no_identitas_klien

        if not all([new_nama, tanggal_lahir, id_jenis, url_foto, pemilik_id]):
            return HttpResponseBadRequest("Semua field harus diisi.")

        if new_nama != nama_hewan or pemilik_id != no_identitas_klien:
            cek_duplikat = query(f"""
                SELECT 1 FROM HEWAN 
                WHERE nama = '{new_nama}' AND no_identitas_klien = '{pemilik_id}'
            """)
            if cek_duplikat:
                return HttpResponseBadRequest("Nama hewan ini sudah digunakan oleh klien yang sama.")

        update_query = f"""
            UPDATE HEWAN
            SET nama = '{new_nama}', 
                no_identitas_klien = '{pemilik_id}',
                tanggal_lahir = '{tanggal_lahir}',
                id_jenis = '{id_jenis}',
                url_foto = '{url_foto}'
            WHERE nama = '{nama_hewan}' AND no_identitas_klien = '{no_identitas_klien}'
        """
        query(update_query)

        return redirect('kuning:hewan_list')

    context = {
        'role': role,
        'hewan': hewan,
        'daftar_klien': klien_list,
        'daftar_jenis': jenis_list,
        'selected_klien_id': hewan['no_identitas_klien'],
        'selected_jenis_id': hewan['id_jenis'],
    }
    return render(request, 'update_hewan.html', context)

def delete_hewan(request, nama_hewan, no_identitas_klien):
    logged_user = request.session.get('logged_user')
    if not logged_user:
        return redirect('login')

    role = logged_user['role']

    if role != 'front_desk':
        return HttpResponseForbidden("Hanya Front-Desk Officer yang dapat menghapus hewan.")

    fetch_query = f"""
        SELECT h.*, 
               COALESCE(i.nama_depan || ' ' || COALESCE(i.nama_tengah || ' ', '') || i.nama_belakang, 
                        p.nama_perusahaan) AS pemilik
        FROM HEWAN h
        JOIN KLIEN k ON h.no_identitas_klien = k.no_identitas
        LEFT JOIN INDIVIDU i ON i.no_identitas_klien = k.no_identitas
        LEFT JOIN PERUSAHAAN p ON p.no_identitas_klien = k.no_identitas
        WHERE h.nama = '{nama_hewan}' AND h.no_identitas_klien = '{no_identitas_klien}'
    """
    result = query(fetch_query)
    if not result:
        return HttpResponseNotFound("Data hewan tidak ditemukan.")

    hewan = result[0]

    if request.method == 'POST':
        delete_query = f"""
            DELETE FROM HEWAN
            WHERE nama = '{nama_hewan}' AND no_identitas_klien = '{no_identitas_klien}'
        """
        result = query(delete_query)

        if isinstance(result, dict) and result.get("status") == "error":
            return render(request, 'delete_hewan.html', {
                'role': role,
                'hewan': hewan,
                'error': result["data"]  
            })

        return redirect('kuning:hewan_list')

    context = {
        'role': role,
        'hewan': hewan,
    }
    return render(request, 'delete_hewan.html', context)
