# Panduan Instalasi dan Menjalankan InkluMap

## 1. Persiapan

Pastikan Python, Node.js, npm, PostgreSQL, dan Git tersedia.

Periksa:

```powershell
python --version
node --version
npm --version
git --version
```

## 2. Membuat Virtual Environment

Dari root proyek:

```powershell
python -m venv .venv

Set-ExecutionPolicy `
    -Scope Process `
    -ExecutionPolicy RemoteSigned

& .\.venv\Scripts\Activate.ps1
```

## 3. Memasang Dependency Backend

```powershell
python -m pip install `
    --upgrade pip

python -m pip install `
    -r .\backend\requirements.txt
```

## 4. Menyiapkan PostgreSQL

Salin konfigurasi:

```powershell
Copy-Item `
    .\backend\.env.example `
    .\backend\.env
```

Isi `backend/.env` menggunakan kredensial PostgreSQL lokal. Buat database sesuai nama yang dicantumkan pada file tersebut.

Jalankan migrasi:

```powershell
Set-Location .\backend

alembic upgrade head
```

Impor data bila database masih kosong:

```powershell
python .\scripts\import_initial_data.py
python .\scripts\import_analytics_results.py
```

## 5. Menjalankan Backend

```powershell
uvicorn app.main:app --reload
```

Periksa:

```text
http://127.0.0.1:8000/health
http://127.0.0.1:8000/health/database
http://127.0.0.1:8000/docs
```

## 6. Menyiapkan Frontend

Buka terminal baru:

```powershell
Set-Location `
    C:\Users\HazelWinata\Desktop\InkluMap\frontend

Copy-Item `
    .\.env.example `
    .\.env.local `
    -Force

npm install
```

## 7. Menjalankan Frontend

```powershell
npm run dev
```

Buka:

```text
http://localhost:3000
```

## 8. Pemeriksaan Masalah Umum

### Port 3000 sudah digunakan

Pesan ini menunjukkan server Next.js lain sudah berjalan:

```text
Another next dev server is already running.
```

Gunakan server yang sudah aktif. Untuk menghentikannya, gunakan PID yang ditampilkan terminal:

```powershell
taskkill /PID <PID> /F
```

### Frontend tidak mendapatkan data

Pastikan:

- backend berjalan pada port 8000;
- PostgreSQL berjalan;
- `frontend/.env.local` mengarah ke backend;
- endpoint `/health/database` berstatus sehat.

### Database belum memiliki tabel

```powershell
Set-Location .\backend

alembic upgrade head
```

### Halaman analytics kosong

Pastikan data awal dan hasil analytics telah diimpor:

```powershell
python .\scripts\import_initial_data.py
python .\scripts\import_analytics_results.py
```

### PowerShell menolak aktivasi virtual environment

```powershell
Set-ExecutionPolicy `
    -Scope Process `
    -ExecutionPolicy RemoteSigned

& ..\.venv\Scripts\Activate.ps1
```

## 9. Validasi Akhir

Backend:

```powershell
Set-Location .\backend
python -m pytest -q
```

Frontend:

```powershell
Set-Location ..\frontend
npm run lint
npm run build
```

Repository:

```powershell
Set-Location ..
git diff --check
git status
```
