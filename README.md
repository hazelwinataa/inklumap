# InkluMap

InkluMap adalah sistem pendukung keputusan untuk memetakan kebutuhan akomodasi pembelajaran di sekolah inklusif. Sistem menggabungkan pengelolaan data siswa, asesmen kebutuhan fungsional, analisis kelompok berbasis data mining, rekomendasi akomodasi, pemeringkatan kebutuhan sumber daya, dan laporan yang dapat dicetak sebagai PDF.

## Tujuan

InkluMap membantu sekolah:

- memantau kelengkapan asesmen siswa;
- mengelompokkan siswa berdasarkan kemiripan kebutuhan fungsional;
- melihat kebutuhan dominan dan rekomendasi akomodasi;
- mengidentifikasi siswa dengan prioritas tinggi, hambatan akses kritis, atau kebutuhan validasi guru;
- menyusun urutan prioritas sumber daya berdasarkan data;
- menghasilkan laporan ringkas untuk rapat dan dokumentasi.

InkluMap tidak menggantikan keputusan profesional guru, tenaga pendamping, atau pihak sekolah. Rekomendasi sistem harus digunakan sebagai bahan pertimbangan dan divalidasi sesuai kondisi siswa.

## Fitur Utama

- Data siswa dan status kelengkapan asesmen.
- Detail siswa dan riwayat asesmen.
- Formulir asesmen yang dapat disimpan sebagai draf dan diperbarui.
- Pemetaan lima kelompok kebutuhan.
- Filter berdasarkan kelompok, prioritas, kebutuhan, dan penanda perhatian.
- Rekomendasi kelompok dan tindak lanjut individual.
- Pemeringkatan prioritas sumber daya sekolah.
- Laporan analytics yang dapat dicetak atau disimpan sebagai PDF.
- Tampilan responsif untuk desktop, tablet, dan perangkat seluler.

## Teknologi

### Frontend

- Next.js 16
- React 19
- TypeScript
- Tailwind CSS
- Lucide React

### Backend

- FastAPI
- SQLAlchemy
- Pydantic
- Alembic
- PostgreSQL
- Pytest

### Analytics

- Hierarchical Agglomerative Clustering
- Gower Distance
- Average Linkage
- DBSCAN untuk penanda kasus unik
- Scikit-learn, Pandas, NumPy, dan SciPy

## Struktur Proyek

```text
InkluMap/
├── analytics/                  # Eksperimen clustering dan aturan prioritas
├── backend/
│   ├── alembic/               # Migrasi database
│   ├── app/
│   │   ├── models/            # Model SQLAlchemy
│   │   ├── routers/           # Endpoint FastAPI
│   │   └── schemas/           # Schema Pydantic
│   ├── scripts/               # Import data dan hasil analytics
│   └── tests/                 # Pengujian backend
├── data/
│   ├── raw/                   # Data sumber
│   └── processed/             # Data hasil preprocessing
├── docs/                      # Dokumentasi final proyek
├── frontend/
│   └── src/
│       ├── app/               # Route Next.js
│       ├── components/        # Komponen antarmuka
│       ├── lib/               # Integrasi API
│       └── types/             # Tipe TypeScript
├── reports/                   # Grafik analytics dan hasil pengujian
└── scripts/                   # Pemeriksaan final proyek
```

## Persiapan Lingkungan

Perangkat yang diperlukan:

- Python 3.11
- Node.js dan npm
- PostgreSQL
- Git

Seluruh perintah berikut ditulis untuk Windows PowerShell.

## Instalasi Backend

Dari root proyek:

```powershell
python -m venv .venv

Set-ExecutionPolicy `
    -Scope Process `
    -ExecutionPolicy RemoteSigned

& .\.venv\Scripts\Activate.ps1

python -m pip install `
    --upgrade pip

python -m pip install `
    -r .\backend\requirements.txt
```

Salin konfigurasi backend:

```powershell
Copy-Item `
    .\backend\.env.example `
    .\backend\.env
```

Buka `backend/.env`, lalu isi konfigurasi PostgreSQL sesuai lingkungan lokal. Jangan commit file `.env`.

Buat database PostgreSQL sesuai konfigurasi tersebut, kemudian jalankan migrasi:

```powershell
Set-Location .\backend

alembic upgrade head
```

Impor data awal dan hasil analytics bila database masih kosong:

```powershell
python .\scripts\import_initial_data.py
python .\scripts\import_analytics_results.py
```

Jalankan backend:

```powershell
uvicorn app.main:app --reload
```

Backend lokal tersedia di:

```text
http://127.0.0.1:8000
```

Dokumentasi API interaktif:

```text
http://127.0.0.1:8000/docs
```

Pemeriksaan kesehatan:

```text
http://127.0.0.1:8000/health
http://127.0.0.1:8000/health/database
```

## Instalasi Frontend

Buka terminal PowerShell baru dari root proyek:

```powershell
Set-Location .\frontend

Copy-Item `
    .\.env.example `
    .\.env.local `
    -Force

npm install
npm run dev
```

Frontend lokal tersedia di:

```text
http://localhost:3000
```

Jika port 3000 sudah digunakan oleh proses Next.js InkluMap yang aktif, gunakan server tersebut dan jangan menjalankan `npm run dev` kedua kali.

## Route Frontend

| Halaman | Route |
|---|---|
| Ringkasan dan data siswa | `/` |
| Data siswa | `/students` |
| Detail siswa | `/students/[studentId]` |
| Formulir asesmen | `/students/[studentId]/assessment` |
| Kelompok kebutuhan | `/clusters` |
| Rekomendasi akomodasi | `/recommendations` |
| Prioritas anggaran | `/budget-priorities` |
| Laporan analytics | `/reports` |

## Endpoint Utama

| Fungsi | Endpoint |
|---|---|
| Ringkasan data siswa | `GET /api/students/summary` |
| Daftar siswa | `GET /api/students` |
| Detail siswa | `GET /api/students/{student_id}` |
| Membuat asesmen | `POST /api/assessments` |
| Membaca asesmen | `GET /api/assessments/{assessment_id}` |
| Mengganti asesmen | `PUT /api/assessments/{assessment_id}` |
| Memperbarui asesmen | `PATCH /api/assessments/{assessment_id}` |
| Ringkasan analytics | `GET /api/analytics/summary` |
| Profil kelompok | `GET /api/analytics/clusters` |
| Daftar hasil analytics siswa | `GET /api/analytics/students` |
| Detail analytics siswa | `GET /api/analytics/students/{student_id}` |
| Prioritas sumber daya | `GET /api/analytics/budget-priorities` |

## Metodologi Analytics

Model aktif menggunakan Hierarchical Agglomerative Clustering dengan Gower Distance dan Average Linkage. Gower Distance digunakan karena fitur kebutuhan siswa dapat terdiri dari tipe data yang berbeda. Model aktif menghasilkan lima kelompok kebutuhan dengan silhouette score sekitar `0.6757`.

DBSCAN digunakan sebagai analisis pendukung untuk menandai kasus unik. Penanda ini tidak otomatis menentukan keputusan akhir dan tetap memerlukan pemeriksaan manusia.

Pemeringkatan prioritas sumber daya menggunakan rumus:

```text
3 × jumlah prioritas tinggi
+ 2 × jumlah prioritas sedang
+ 1 × jumlah prioritas rendah
+ 2 × jumlah hambatan akses kritis
+ 1 × jumlah yang memerlukan validasi guru
```

Skor tersebut digunakan untuk mengurutkan kebutuhan sumber daya. Skor bukan estimasi harga dan bukan nominal rupiah.

## Pengujian

Jalankan seluruh backend test:

```powershell
Set-Location .\backend

python -m pytest -q
```

Baseline proyek saat dokumentasi dibuat:

```text
46 passed
```

Jalankan pemeriksaan frontend:

```powershell
Set-Location ..\frontend

npm run lint
npm run build
```

Pemeriksaan otomatis gabungan tersedia melalui:

```powershell
Set-Location ..

powershell `
    -ExecutionPolicy Bypass `
    -File .\scripts\final_check.ps1
```

## Mencetak Laporan

1. Buka `/reports`.
2. Klik **Cetak / Simpan PDF**.
3. Pilih **Save as PDF**.
4. Gunakan layout portrait.
5. Aktifkan background graphics agar progress bar dan penanda warna tetap terlihat.

Sidebar, header dashboard, dan tombol cetak disembunyikan pada mode cetak.

## Keamanan dan Privasi

- Jangan commit `backend/.env` atau `frontend/.env.local`.
- Gunakan data demonstrasi atau data pseudonim untuk publikasi dan presentasi.
- Hindari menampilkan nama lengkap, diagnosis, alamat, nomor telepon, atau informasi sensitif siswa.
- Jangan membagikan kredensial PostgreSQL melalui screenshot, video, atau repository.
- Periksa riwayat Git sebelum membuat repository publik.
- Batasi CORS dan kredensial database sesuai lingkungan deployment.

## Batasan

- Rekomendasi merupakan dukungan keputusan, bukan diagnosis.
- Pemeringkatan anggaran tidak menghitung harga alat atau biaya pengadaan.
- Kualitas hasil bergantung pada kelengkapan dan konsistensi asesmen.
- Model aktif dibangun dari data yang tersedia pada versi eksperimen saat ini.
- Ekspor PDF dilakukan melalui dialog cetak browser, bukan generator PDF di server.
- Perubahan data asesmen tidak otomatis melatih ulang model analytics.

## Dokumentasi Tambahan

- `docs/INSTALLATION.md`
- `docs/SCREENSHOT_CHECKLIST.md`
- `docs/DEMO_SCRIPT.md`
- `docs/FINAL_CHECKLIST.md`
- `docs/DEPLOYMENT_CHECKLIST.md`

## Status Pengembangan

Prototype utama telah mencakup alur data siswa, asesmen, analytics, rekomendasi, prioritas sumber daya, dan laporan. Tahap berikutnya untuk penggunaan produksi adalah autentikasi, otorisasi berbasis peran, audit log, pengamanan deployment, pencadangan database, dan pipeline retraining yang terkontrol.
