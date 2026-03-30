# EMISGTK ABSEN OTOMATIS

Skrip Python otomatisasi upload absensi untuk SIAP Online.

## Ringkasan

- Nama file utama: `main.py`
- Tujuan: upload data absensi harian ke endpoint SIAP Online (`/pegawai-absensi-uploader/upload` dan `/pegawai-absensi-uploader/save`), dengan skip untuk tanggal akhir pekan, hari libur nasional dari `libur.txt`, dan tanggal yang sudah terisi (placeholder `cek_absensi_terisi`).

## Persyaratan

- Python 3.8+
- Paket Python: `requests`
- File konfigurasi:
  - `cookies.json`: berisi cookie login SIAP Online (format JSON) hilangkan `_example` pada nama file saat digunakan
  - `libur.txt`: daftar tanggal libur nasional, format `YYYY-MM-DD` per baris , hilangkan `_example` pada nama file saat digunakan
  - file absensi Excel (misal `absensi-guru.xls`) yang diupload. Template Excel dapat diunduh di Absensi Simpatika Unduh Format Excel Lalu Sesuaikan Kehadiran

## Instalasi

1. Pastikan Python dan `pip` terpasang.
2. Install dependensi:

```bash
pip install requests
```

## Cara pakai

1. Jalankan skrip:

```bash
python main.py
```

2. Ikuti prompt:

- Sekolah ID (contoh: `20278273`)
- Nama file absensi (contoh: `absensi-guru.xls`)
- Tanggal mulai (`YYYY-MM-DD`)
- Tanggal akhir (`YYYY-MM-DD`)
- Weekend yang di-skip (misal `5,6` untuk Sabtu-Minggu)

3. Skrip akan:
- Cek eksistensi file upload
- Validasi rentang tanggal
- Tampilkan pesan jika tanggal akhir > hari ini (otomatis disesuaikan)
- Lewati hari akhir pekan dan libur nasional
- Simpan data absensi ke endpoint

## Format `libur.txt`

Contoh:

```
2026-01-01
2026-02-18
2026-03-11
```

## File `cookies.json`

Contoh sederhana:

```json
{
  "PHPSESSID": "sessionid123",
  "other_cookie": "value"
}
```

### Cara Mendapatkan Cookies

1. Login Emis Gtk / Simpatika / Siap Online
2. Buka Inspect Element (Klik Kanan -> Pilih Inspect)
3. Pilih Tab Network
4. Cari File Index di Kolom Name
5. Cari Cookie di Tab Header
6. Sesuaikan Cookies.json dengan Cookies yang didapatkan. Jangan Lupa Simpan.

- Pastikan URL upload/save sesuai URL resmi SIAP jika berubah. dapat di cek di Inspect Element Seperti saat Mendapatkan Cookies

## Catatan

- Saat ini skrip hanya menampilkan status HTTP dan tidak melakukan retry otomatis.
- Pastikan semua tanggal berada dalam satuan `YYYY-MM-DD`.

## Lisensi

Lisensi bebas gunakan (MIT/UNLICENSE) — sesuaikan sendiri jika perlu.
