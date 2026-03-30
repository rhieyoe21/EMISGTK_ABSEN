import requests
import json
import os
from datetime import datetime, timedelta

# ==========================================
# FUNGSI BANTUAN
# ==========================================

def load_cookies(filepath='cookies.json'):
    """Membaca cookie dari file JSON eksternal."""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"[-] File {filepath} tidak ditemukan. Buat file cookies.json terlebih dahulu.")
        exit(1)

def load_holidays(filepath='libur.txt'):
    """Membaca daftar hari libur dari file teks."""
    holidays = []
    try:
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    holidays.append(line)
        return holidays
    except FileNotFoundError:
        print(f"[!] File {filepath} tidak ditemukan. Lanjut tanpa data hari libur eksternal.")
        return []

def cek_absensi_terisi(tanggal, sekolah_id, cookies, headers):
    """
    Fungsi dummy: Anda perlu menyesuaikan ini dengan endpoint asli SIAP Online
    untuk mengecek apakah absensi tanggal tersebut sudah diisi atau belum.
    """
    return False 

# ==========================================
# KONFIGURASI HEADER DASAR
# ==========================================

HEADERS_BASE = {
    'accept-language': 'id',
    'origin': 'https://sim.siap-online.com',
    'sec-ch-ua': '"Not:A-Brand";v="99", "Microsoft Edge";v="145", "Chromium";v="145"',
    'sec-ch-ua-platform': '"Windows"',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36 Edg/145.0.0.0',
    'x-requested-with': 'XMLHttpRequest',
}

# ==========================================
# PROGRAM UTAMA
# ==========================================

def main():
    print("=== AUTOMATISASI UPLOAD ABSENSI SIAP ONLINE ===")
    
    # 1. Input dari User
    sekolah_id = input("[?] Masukkan Sekolah ID (contoh: 20278273): ").strip()
    
    # INPUT BARU: Nama file diinput manual
    nama_file = input("[?] Masukkan Nama File Absensi (contoh: absensi-guru.xls): ").strip()
    
    tgl_mulai_str = input("[?] Masukkan Tanggal Mulai (YYYY-MM-DD): ").strip()
    tgl_akhir_str = input("[?] Masukkan Tanggal Akhir (YYYY-MM-DD): ").strip()
    
    print("\nPengaturan Hari Libur Akhir Pekan (Weekend):")
    print("0=Senin, 1=Selasa, 2=Rabu, 3=Kamis, 4=Jumat, 5=Sabtu, 6=Minggu")
    weekend_input = input("[?] Masukkan angka hari libur (pisahkan dengan koma, misal '5,6' untuk Sabtu & Minggu): ").strip()
    
    # Parsing input akhir pekan
    weekend_days = [int(x.strip()) for x in weekend_input.split(',')] if weekend_input else []

    # 2. Validasi File (Cek di awal, sebelum looping)
    if not os.path.exists(nama_file):
        print(f"\n[-] ERROR: File '{nama_file}' tidak ditemukan di folder tempat skrip berjalan.")
        print("Pastikan nama file dan ekstensinya sudah benar (misal: ada .xls di belakangnya).")
        return

    # 3. Parsing dan Validasi Tanggal
    try:
        tgl_mulai = datetime.strptime(tgl_mulai_str, "%Y-%m-%d").date()
        tgl_akhir = datetime.strptime(tgl_akhir_str, "%Y-%m-%d").date()
    except ValueError:
        print("\n[-] ERROR: Format tanggal salah. Pastikan menggunakan format YYYY-MM-DD.")
        return

    # Ambil tanggal hari ini
    hari_ini = datetime.now().date()
    
    # Logika batas tanggal akhir maksimal adalah hari ini
    if tgl_akhir > hari_ini:
        print(f"\n[*] INFO: Tanggal akhir yang diinput melebihi hari ini.")
        print(f"[*] Otomatis mengubah batas tanggal akhir menjadi hari ini: {hari_ini}")
        tgl_akhir = hari_ini

    if tgl_mulai > tgl_akhir:
        print("\n[-] ERROR: Tanggal mulai tidak boleh lebih besar dari tanggal akhir.")
        return

    # 4. Load Data Eksternal
    cookies = load_cookies()
    holidays = load_holidays()

    # 5. Looping Tanggal
    current_date = tgl_mulai
    while current_date <= tgl_akhir:
        tgl_str = current_date.strftime("%Y-%m-%d")
        print(f"\n---> Memproses tanggal: {tgl_str} <---")

        # Cek apakah akhir pekan
        if current_date.weekday() in weekend_days:
            print(f"[-] Dilewati: {tgl_str} adalah hari libur akhir pekan.")
            current_date += timedelta(days=1)
            continue

        # Cek apakah hari libur nasional (dari libur.txt)
        if tgl_str in holidays:
            print(f"[-] Dilewati: {tgl_str} terdaftar sebagai hari libur di libur.txt.")
            current_date += timedelta(days=1)
            continue

        # Cek apakah data sudah terisi (Fungsi ini butuh disesuaikan dengan endpoint SIAP)
        if cek_absensi_terisi(tgl_str, sekolah_id, cookies, HEADERS_BASE):
            print(f"[-] Dilewati: {tgl_str} sudah terisi di sistem.")
            current_date += timedelta(days=1)
            continue

        # ==========================================
        # PROSES 1: UPLOAD FILE (Menggunakan file yang sama)
        # ==========================================
        print(f"[+] Mengunggah file '{nama_file}' untuk tanggal {tgl_str}...")
        upload_url = f'https://sim.siap-online.com/{sekolah_id}/pegawai-absensi-uploader/upload'
        
        # Header untuk upload
        upload_headers = HEADERS_BASE.copy()
        upload_headers['referer'] = f'https://sim.siap-online.com/{sekolah_id}'

        try:
            with open(nama_file, 'rb') as f:
                # Menggunakan nama_file yang diinput secara manual
                files = {
                    'name': (None, nama_file),
                    'k_jenis_pegawai': (None, '1'),
                    'tgl_absensi': (None, tgl_str),
                    'file': (nama_file, f, 'application/vnd.ms-excel'),
                }
                
                upload_res = requests.post(upload_url, cookies=cookies, headers=upload_headers, files=files)
                
                if upload_res.status_code != 200:
                    print(f"[!] Gagal upload {tgl_str}. Status code: {upload_res.status_code}")
                    current_date += timedelta(days=1)
                    continue
                else:
                    print("  [v] Upload berhasil.")
        except Exception as e:
            print(f"[!] Error saat proses upload: {e}")
            current_date += timedelta(days=1)
            continue

        # ==========================================
        # PROSES 2: SAVE DATA
        # ==========================================
        print(f"[+] Menyimpan data absensi ke sistem...")
        save_url = f'https://sim.siap-online.com/{sekolah_id}/pegawai-absensi-uploader/save'
        
        save_headers = HEADERS_BASE.copy()
        save_headers['content-type'] = 'application/x-www-form-urlencoded; charset=UTF-8'
        save_headers['accept'] = 'application/json, text/javascript, */*; q=0.01'
        save_headers['referer'] = f'https://sim.siap-online.com/{sekolah_id}'

        save_data = {
            'sekolah_id': sekolah_id,
            'k_jenis_pegawai': '1',
            'tgl_absensi': tgl_str,
        }

        try:
            save_res = requests.post(save_url, cookies=cookies, headers=save_headers, data=save_data)
            
            if save_res.status_code == 200:
                print(f"  [v] Data absensi tanggal {tgl_str} selesai disimpan!")
            else:
                print(f"  [!] Gagal menyimpan data {tgl_str}. Status code: {save_res.status_code}")
        except Exception as e:
            print(f"[!] Error saat proses simpan: {e}")

        # Lanjut ke hari berikutnya
        current_date += timedelta(days=1)

    print("\n=== PROSES SELESAI ===")

if __name__ == "__main__":
    main()