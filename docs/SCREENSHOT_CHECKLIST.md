# Checklist Screenshot InkluMap

Gunakan ukuran browser desktop yang konsisten. Hindari menampilkan password, isi `.env`, nama lengkap siswa, atau data pribadi.

## Screenshot Wajib

| No. | Nama file yang disarankan | Isi |
|---:|---|---|
| 01 | `01-data-siswa.png` | Halaman data siswa dan kartu ringkasan |
| 02 | `02-detail-siswa.png` | Identitas pseudonim, status asesmen, dan hasil analytics |
| 03 | `03-form-asesmen.png` | Formulir asesmen kebutuhan fungsional |
| 04 | `04-notifikasi-simpan.png` | Notifikasi asesmen berhasil disimpan |
| 05 | `05-kelompok-kebutuhan.png` | Ringkasan lima kelompok |
| 06 | `06-detail-kelompok.png` | Satu kelompok dipilih dan rekomendasi terlihat |
| 07 | `07-rekomendasi.png` | Ringkasan rekomendasi akomodasi |
| 08 | `08-filter-rekomendasi.png` | Filter prioritas atau akses kritis aktif |
| 09 | `09-prioritas-anggaran.png` | Ringkasan dan tiga prioritas utama |
| 10 | `10-urutan-urgensi.png` | Urutan berdasarkan urgency index |
| 11 | `11-laporan.png` | Halaman laporan analytics |
| 12 | `12-preview-pdf.png` | Preview cetak tanpa sidebar dan header |
| 13 | `13-mobile-sidebar.png` | Sidebar mobile terbuka |
| 14 | `14-responsive-page.png` | Salah satu halaman analytics pada ukuran mobile |
| 15 | `15-api-docs.png` | Swagger UI FastAPI |
| 16 | `16-backend-tests.png` | Terminal dengan hasil `46 passed` |
| 17 | `17-frontend-build.png` | Terminal dengan seluruh route berhasil dibangun |
| 18 | `18-git-clean.png` | `git status` dengan working tree clean |

## Aturan Pengambilan Screenshot

- Gunakan zoom browser 100%.
- Tutup bookmark bar jika mengganggu.
- Gunakan data pseudonim.
- Pastikan tidak ada tooltip atau dropdown yang menutupi informasi utama.
- Jangan memotong judul halaman.
- Jangan menampilkan panel developer tools kecuali screenshot responsif.
- Gunakan nama file berurutan agar mudah dimasukkan ke laporan.
- Untuk screenshot terminal, tampilkan perintah dan hasil penting saja.
- Periksa kembali agar `.env`, password, username database, dan alamat pribadi tidak terlihat.

## Screenshot Tambahan untuk Presentasi

- Filter pencarian siswa.
- Empty state setelah kombinasi filter tidak menemukan data.
- Halaman detail siswa dengan rekomendasi individual.
- Metodologi skor prioritas.
- Peringatan bahwa skor anggaran bukan nominal rupiah.
- Health check database.
