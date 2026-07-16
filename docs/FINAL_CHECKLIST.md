# Checklist Final InkluMap

## Kode

- [ ] Seluruh perubahan penting sudah di-commit.
- [ ] `git status` menunjukkan working tree clean.
- [ ] Tidak ada file konteks sementara.
- [ ] Tidak ada file `.env` yang masuk Git.
- [ ] Tidak ada password di source code atau dokumentasi.
- [ ] Tidak ada data pribadi siswa pada repository publik.

## Backend

- [ ] PostgreSQL berjalan.
- [ ] Alembic berada pada revisi terbaru.
- [ ] `/health` berhasil.
- [ ] `/health/database` berhasil.
- [ ] Swagger UI dapat dibuka.
- [ ] Seluruh test backend berhasil.
- [ ] Endpoint budget priority menghasilkan respons 200.

## Frontend

- [ ] ESLint tanpa error dan warning.
- [ ] Production build berhasil.
- [ ] Seluruh route terdaftar saat build.
- [ ] Sidebar desktop berfungsi.
- [ ] Sidebar mobile berfungsi.
- [ ] Tidak ada horizontal overflow yang tidak disengaja.
- [ ] Error state dan empty state terlihat benar.
- [ ] Tombol kembali dan link detail siswa bekerja.

## Alur Utama

- [ ] Data siswa dapat dilihat.
- [ ] Detail siswa dapat dibuka.
- [ ] Asesmen dapat dibuat.
- [ ] Asesmen dapat diperbarui.
- [ ] Notifikasi penyimpanan muncul.
- [ ] Halaman kelompok dapat difilter.
- [ ] Halaman rekomendasi dapat difilter.
- [ ] Halaman prioritas dapat diurutkan berdasarkan urgency.
- [ ] Halaman laporan dapat dicetak sebagai PDF.

## Dokumentasi

- [ ] README sesuai implementasi aktual.
- [ ] `backend/.env.example` tersedia.
- [ ] `frontend/.env.example` tersedia.
- [ ] Panduan instalasi tersedia.
- [ ] Skenario demo tersedia.
- [ ] Screenshot seluruh halaman tersedia.
- [ ] Keterbatasan model dijelaskan.
- [ ] Rumus prioritas dijelaskan.
- [ ] Pernyataan “bukan nominal biaya” terlihat.

## Presentasi

- [ ] Demo selesai dalam 6–8 menit.
- [ ] Data demonstrasi sudah disiapkan.
- [ ] Tab browser sudah dibuka.
- [ ] Screenshot cadangan tersedia.
- [ ] PDF laporan cadangan tersedia.
- [ ] Notifikasi sistem dimatikan.
- [ ] Informasi sensitif tidak terlihat.
- [ ] Narasi membedakan rekomendasi sistem dan keputusan guru.

## Arsip

- [ ] Folder `node_modules` tidak dimasukkan ke ZIP.
- [ ] Folder `.next` tidak dimasukkan ke ZIP.
- [ ] Folder `.venv` tidak dimasukkan ke ZIP.
- [ ] Folder `.git` hanya dimasukkan jika memang diminta.
- [ ] File `.env` tidak dimasukkan ke ZIP publik.
- [ ] Nama ZIP jelas dan konsisten.
- [ ] ZIP berhasil diekstrak pada folder uji.
