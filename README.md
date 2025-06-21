# 📰 Crawler & Scraper Artikel Bisnis.com

Proyek ini adalah **crawler dan scraper web otomatis** untuk mengambil artikel dari situs [bisnis.com](https://www.bisnis.com). Tujuan proyek ini adalah untuk:

- Mengambil artikel terbaru secara berkala (mode standar)
- Mengambil artikel lama berdasarkan rentang tanggal (mode backtrack)
- Menyimpan hasil ke file `.json` yang bisa diolah lebih lanjut

---

## Video

[![Video])](https://www.youtube.com/watch?v=BGt0YU2aaCw)

## ⚙️ Fungsi Dasar Crawler

Secara garis besar, proses yang dilakukan adalah:

1. **Crawl halaman indeks** bisnis.com berdasarkan tanggal dan pagination.
2. **Scrape link artikel** dari setiap halaman.
3. **Ambil konten artikel** secara detail (judul, isi, tanggal).
4. **Simpan dalam format JSON** agar bisa dianalisis, ditampilkan, atau diolah lebih lanjut.

Crawler ini hanya mengambil artiker not berbayar atau selain dari link (`https://premium.bisnis.com/...`)

## 🏗️ Struktur Folder

```text
bisnis/
├── run_standar.py     # Menjalankan scraping terbaru dengan interval tertentu
├── run_backtrack.py   # Menjalankan scraping berdasarkan tanggal mulai & akhir
├── crawler.py         # Fungsi untuk menjelajahi halaman indeks dan mendapatkan link
├── scraper.py         # Fungsi untuk mengambil konten artikel dari URL
├── utils.py           # Fungsi bantu seperti membersihkan teks, parsing tangga

### 🔄 Alur Eksekusi Crawler

#### 📆 Mode Backtrack

Digunakan untuk mengambil artikel dari rentang tanggal tertentu.

- `run_backtrack.py` menerima dua argumen wajib:
  - `--start`: Tanggal awal penarikan artikel (`YYYY-MM-DD`)
  - `--end`: Tanggal akhir penarikan artikel (`YYYY-MM-DD`)
- Terdapat validasi agar tanggal `end` **tidak boleh lebih kecil** dari `start`.
- Script akan memanggil fungsi `crawl_by_date(start_date, end_date)` yang berada di modul `bisnis.crawler`.
- Fungsi ini akan:
  1. Mengambil seluruh link artikel per tanggal menggunakan `fetch_article_links()`.
  2. Mengambil isi konten dari setiap link menggunakan `fetch_article_content()`.
  3. Menyimpan hasil dalam format `.json` menggunakan `save_to_json()`.
- Output file json akan disimpan di folder output/hasil_backtrack_startdate_enddate.json

#### 🔁 Mode Standar

Digunakan untuk mengambil artikel terbaru secara berkala berdasarkan interval waktu tertentu.

- `run_standar.py` menerima satu argumen opsional:
  - `--interval`: Waktu interval antar penarikan (dalam **detik**). Default: `300` detik.
- Argumen ini akan divalidasi agar tidak bernilai negatif atau nol.
- Script akan menjalankan fungsi `crawl_latest(interval_sec)` yang berada di modul `bisnis.crawler`.
- Fungsi ini akan berjalan terus-menerus dalam loop dan:
  1. Mengambil link artikel terbaru menggunakan `fetch_article_links()`.
  2. Mengambil isi konten dari setiap link menggunakan `fetch_article_content()`.
  3. Menyimpan hasil dalam format `.json` menggunakan `save_to_json()` pada setiap iterasi jika ada artikel baru.
- Output file json akan disimpan di folder output/hasil_standard.json

## 🚀 Cara Menjalankan

### Menggunakan Virtual Env (Opsional)

Linux / Macos

```

python -m venv venv

source venv/bin/activate

````

### Install dependensi

```bash
pip install -r requirements.txt
````

### Jalankan Script

#### Backtrack

```
python run_backtrack.py --start 2024-06-01 --end 2024-06-02
```

#### Standard

```
python run_standard.py --interval 600
```
