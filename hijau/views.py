from django.shortcuts import render, redirect
from django.db import connection
from django.http import JsonResponse
import uuid
import json

# READ - Semua user bisa lihat data kunjungan
def list_kunjungan(request):
    context = {}
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id_kunjungan, nama_hewan, no_identitas_klien, tipe_kunjungan, timestamp_awal, timestamp_akhir
            FROM PETCLINIC.KUNJUNGAN
            ORDER BY timestamp_awal DESC
        """)
        context['kunjungan'] = cursor.fetchall()

        # Ambil email user dari sesi
        session_id = request.session.get('sessionId')
        if session_id:
            cursor.execute("""
                SELECT email FROM PETCLINIC."USER"
                WHERE email IN (
                    SELECT email_user FROM PETCLINIC.PEGAWAI
                    WHERE no_pegawai IN (
                        SELECT no_front_desk FROM PETCLINIC.FRONT_DESK
                    )
                ) AND email = (
                    SELECT email FROM PETCLINIC."USER"
                    WHERE email = %s
                )
            """, [session_id])
            is_front_desk = cursor.fetchone()
            context['is_front_desk'] = bool(is_front_desk)
        else:
            context['is_front_desk'] = False

    return render(request, "list_kunjungan.html", context)

# CUD - Front-Desk Officer dapat membuat, mengupdate, dan delete kunjungan
def create_kunjungan(request):
    if request.method == "POST":
        data = json.loads(request.body)
        id_kunjungan = uuid.uuid4()
        nama_hewan = data.get('nama_hewan')
        no_identitas_klien = data.get('no_identitas_klien')
        no_front_desk = data.get('no_front_desk')
        tipe_kunjungan = data.get('tipe_kunjungan')
        timestamp_awal = data.get('timestamp_awal')

        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO PETCLINIC.KUNJUNGAN
                (id_kunjungan, nama_hewan, no_identitas_klien, no_front_desk, tipe_kunjungan, timestamp_awal)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, [id_kunjungan, nama_hewan, no_identitas_klien, no_front_desk, tipe_kunjungan, timestamp_awal])
        
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'invalid method'})

def update_kunjungan(request, id_kunjungan):
    if request.method == "POST":
        data = json.loads(request.body)
        timestamp_akhir = data.get('timestamp_akhir')

        with connection.cursor() as cursor:
            cursor.execute("""
                UPDATE PETCLINIC.KUNJUNGAN
                SET timestamp_akhir = %s
                WHERE id_kunjungan = %s
            """, [timestamp_akhir, id_kunjungan])
        
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'invalid method'})

def delete_kunjungan(request, id_kunjungan):
    if request.method == "POST":
        with connection.cursor() as cursor:
            cursor.execute("""
                DELETE FROM PETCLINIC.KUNJUNGAN
                WHERE id_kunjungan = %s
            """, [id_kunjungan])
        return JsonResponse({'status': 'deleted'})
    return JsonResponse({'status': 'invalid method'})

# CRUD - Perawatan Hewan (untuk semua role)
def list_perawatan(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT * FROM PETCLINIC.PERAWATAN
        """)
        perawatan = cursor.fetchall()
    return render(request, 'list_perawatan.html', {'perawatan': perawatan})

# R Rekam Medis - semua role bisa lihat
def list_rekam_medis(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT * FROM PETCLINIC.KUNJUNGAN_KEPERAWATAN
        """)
        data = cursor.fetchall()
    return render(request, "list_rekam_medis.html", {'data': data})

# CU Rekam Medis - hanya dokter hewan
def create_or_update_rekam_medis(request):
    if request.method == "POST":
        data = json.loads(request.body)
        id_kunjungan = data.get('id_kunjungan')
        nama_hewan = data.get('nama_hewan')
        no_identitas_klien = data.get('no_identitas_klien')
        no_front_desk = data.get('no_front_desk')
        no_perawat_hewan = data.get('no_perawat_hewan')
        no_dokter_hewan = data.get('no_dokter_hewan')
        kode_perawatan = data.get('kode_perawatan')
        catatan = data.get('catatan')

        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO PETCLINIC.KUNJUNGAN_KEPERAWATAN (
                    id_kunjungan, nama_hewan, no_identitas_klien,
                    no_front_desk, no_perawat_hewan, no_dokter_hewan,
                    kode_perawatan, catatan
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id_kunjungan, nama_hewan, no_identitas_klien,
                             no_front_desk, no_perawat_hewan, no_dokter_hewan, kode_perawatan)
                DO UPDATE SET catatan = EXCLUDED.catatan
            """, [
                id_kunjungan, nama_hewan, no_identitas_klien,
                no_front_desk, no_perawat_hewan, no_dokter_hewan,
                kode_perawatan, catatan
            ])
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'invalid method'})
