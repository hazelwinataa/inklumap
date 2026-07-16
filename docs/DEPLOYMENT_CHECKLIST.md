# Checklist Persiapan Deployment InkluMap

Dokumen ini adalah panduan persiapan. Prototype saat ini telah diuji secara lokal dan belum boleh dianggap siap produksi sebelum seluruh kontrol keamanan diterapkan.

## Backend

- [ ] Gunakan PostgreSQL terkelola atau server PostgreSQL yang memiliki backup.
- [ ] Simpan kredensial database sebagai environment variable.
- [ ] Jalankan `alembic upgrade head` pada lingkungan deployment.
- [ ] Gunakan process manager atau layanan container untuk menjalankan Uvicorn.
- [ ] Jangan gunakan mode `--reload` di produksi.
- [ ] Tambahkan health check `/health` dan `/health/database`.
- [ ] Batasi CORS hanya ke domain frontend resmi.
- [ ] Aktifkan HTTPS.
- [ ] Tambahkan autentikasi.
- [ ] Tambahkan otorisasi berbasis peran.
- [ ] Tambahkan audit log untuk perubahan asesmen.
- [ ] Batasi akses Swagger UI pada lingkungan produksi bila diperlukan.
- [ ] Konfigurasikan backup dan pemulihan database.
- [ ] Terapkan retensi log yang aman.

## Frontend

- [ ] Atur `NEXT_PUBLIC_API_URL` ke URL backend HTTPS.
- [ ] Jalankan `npm run build`.
- [ ] Jalankan aplikasi menggunakan mode produksi.
- [ ] Pastikan domain frontend sudah dimasukkan ke daftar CORS backend.
- [ ] Periksa semua route setelah deployment.
- [ ] Periksa mode cetak laporan.
- [ ] Periksa responsif pada perangkat seluler.
- [ ] Pastikan source map dan log tidak mengekspos informasi sensitif.

## Data dan Privasi

- [ ] Gunakan prinsip data minimum.
- [ ] Enkripsi koneksi database.
- [ ] Jangan gunakan data siswa nyata pada lingkungan demo publik.
- [ ] Batasi akses berdasarkan peran pengguna.
- [ ] Tetapkan kebijakan backup, retensi, dan penghapusan data.
- [ ] Catat persetujuan dan dasar penggunaan data sesuai kebijakan sekolah.
- [ ] Lakukan penilaian keamanan sebelum penggunaan nyata.

## Analytics

- [ ] Simpan versi model aktif.
- [ ] Simpan tanggal dan sumber data pelatihan.
- [ ] Validasi hasil setelah perubahan data.
- [ ] Dokumentasikan aturan prioritas.
- [ ] Pisahkan proses retraining dari aplikasi produksi.
- [ ] Jangan mengganti model aktif tanpa evaluasi.
- [ ] Sediakan mekanisme rollback model.
- [ ] Pantau perubahan distribusi data dan kualitas cluster.

## Uji Setelah Deployment

- [ ] Health check backend berhasil.
- [ ] Koneksi database berhasil.
- [ ] Data siswa dapat dimuat.
- [ ] Asesmen dapat disimpan.
- [ ] Halaman analytics dapat dimuat.
- [ ] Prioritas anggaran dapat dimuat.
- [ ] Laporan dapat dicetak.
- [ ] Tidak ada mixed-content HTTP/HTTPS.
- [ ] Tidak ada error CORS.
- [ ] Log aplikasi tidak memuat password atau data siswa sensitif.
