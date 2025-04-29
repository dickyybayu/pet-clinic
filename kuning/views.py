from django.shortcuts import render

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
    role = request.GET.get("role", "Front-Desk Officer") 
    context = {
        'role': role,
        'jenis_hewan_list': DUMMY_JENIS_HEWAN,
    }
    return render(request, 'list_jenis_hewan.html', context)

def create_jenis_hewan(request):
    return render(request, 'create_jenis_hewan.html')

def update_jenis_hewan(request, id_jenis):
    context = {'id_jenis': id_jenis}
    return render(request, 'update_jenis_hewan.html', context)

def delete_jenis_hewan(request, id_jenis):
    context = {'id_jenis': id_jenis}
    return render(request, 'delete_jenis_hewan.html', context)

def list_hewan(request):
    role = request.GET.get('role', 'Klien')
    context = {
        'role': role,
        'hewan_list': DUMMY_HEWAN,
    }
    return render(request, 'list_hewan.html', context)

def create_hewan(request):
    role = request.GET.get('role', 'Klien')
    context = {
        'role': role,
        'daftar_klien': DUMMY_KLIEN,
        'daftar_jenis': DUMMY_JENIS_HEWAN,
    }
    return render(request, 'create_hewan.html', context)

def update_hewan(request, id_hewan):
    role = request.GET.get('role', 'Klien')
    selected_hewan = next((h for h in DUMMY_HEWAN if h['id'] == id_hewan), None)

    context = {
        'role': role,
        'hewan': selected_hewan,
        'daftar_klien': DUMMY_KLIEN,
        'selected_klien_id': 'klien1',
        'daftar_jenis': DUMMY_JENIS_HEWAN,
        'selected_jenis_id': 'HWN002',
    }
    return render(request, 'update_hewan.html', context)

def delete_hewan(request, id_hewan):
    role = request.GET.get('role', 'Klien')
    if role != 'Front-Desk Officer':
        return render(request, 'unauthorized.html')  

    selected_hewan = next((h for h in DUMMY_HEWAN if h['id'] == id_hewan), None)
    context = {
        'hewan': selected_hewan,
    }
    return render(request, 'delete_hewan.html', context)
