# Skenario Demo InkluMap

Durasi yang disarankan: 6–8 menit.

## 1. Pembukaan — 30 detik

“Pada sekolah inklusif, kebutuhan siswa tidak selalu dapat ditangani dengan pendekatan yang sama. InkluMap membantu sekolah memetakan kebutuhan fungsional, menyusun rekomendasi akomodasi, dan menentukan urutan prioritas sumber daya berdasarkan data.”

Tampilkan halaman utama.

## 2. Data Siswa — 45 detik

Tunjukkan:

- jumlah siswa;
- status asesmen lengkap, belum lengkap, dan belum dimulai;
- pencarian siswa;
- tombol menuju detail siswa.

Narasi:

“Identitas siswa ditampilkan menggunakan kode dan inisial. Guru dapat memantau siapa yang sudah memiliki asesmen dan siapa yang masih perlu dilengkapi.”

## 3. Detail dan Asesmen — 1 menit

Buka satu siswa, lalu masuk ke formulir asesmen.

Tunjukkan:

- domain visual;
- pendengaran;
- komunikasi;
- pemahaman instruksi;
- perhatian;
- mobilitas;
- pendampingan;
- penyesuaian evaluasi;
- preferensi materi dan alat bantu;
- notifikasi penyimpanan.

Narasi:

“Asesmen berfokus pada kebutuhan fungsional, bukan label diagnosis. Data dapat disimpan sebagai draf dan diperbarui.”

Jangan mengubah data demonstrasi secara permanen saat presentasi. Gunakan siswa khusus demo atau batalkan perubahan setelah menunjukkan formulir.

## 4. Kelompok Kebutuhan — 1 menit

Buka `/clusters`.

Tunjukkan:

- lima kelompok;
- jumlah anggota;
- kebutuhan dominan;
- rekomendasi;
- filter kelompok dan prioritas;
- daftar anggota kelompok.

Narasi:

“Model aktif menggunakan Hierarchical Agglomerative Clustering dengan Gower Distance. Hasil saat ini membentuk lima kelompok dengan silhouette score sekitar 0.6757.”

Pilih satu kelompok agar detailnya terlihat.

## 5. Rekomendasi Akomodasi — 1 menit

Buka `/recommendations`.

Tunjukkan:

- rekomendasi per kelompok;
- jumlah siswa prioritas tinggi;
- akses kritis;
- hasil yang perlu validasi;
- filter;
- tombol detail siswa.

Narasi:

“Rekomendasi kelompok menjadi panduan umum. Keputusan individual tetap diperiksa melalui detail siswa dan validasi guru.”

## 6. Prioritas Anggaran — 1 menit

Buka `/budget-priorities`.

Tunjukkan:

- total poin;
- kelompok dengan poin terbesar;
- kelompok dengan urgency index tertinggi;
- metodologi;
- ranking;
- tindakan yang direkomendasikan.

Ubah pengurutan menjadi **Indeks urgensi**.

Narasi:

“Poin prioritas menunjukkan besarnya kebutuhan secara keseluruhan, sedangkan urgency index menunjukkan seberapa mendesak kebutuhan di dalam kelompok. Skor ini bukan nominal rupiah dan tidak menggantikan proses pengadaan.”

## 7. Laporan — 45 detik

Buka `/reports`.

Tunjukkan:

- ringkasan siswa;
- distribusi prioritas;
- profil kelompok;
- ranking sumber daya;
- tombol Cetak / Simpan PDF.

Buka print preview sebentar.

Narasi:

“Laporan dapat disimpan sebagai PDF untuk rapat sekolah dan dokumentasi. Elemen navigasi otomatis disembunyikan saat dicetak.”

## 8. Penutup — 30 detik

“InkluMap mengubah data asesmen menjadi informasi operasional yang lebih mudah digunakan sekolah. Sistem membantu menentukan siapa yang perlu ditindaklanjuti, akomodasi apa yang perlu disiapkan, dan kebutuhan mana yang perlu diprioritaskan. Hasil sistem tetap digunakan bersama pertimbangan guru dan kondisi nyata siswa.”

## Rencana Cadangan

Sebelum demo:

- nyalakan PostgreSQL;
- jalankan backend;
- jalankan frontend;
- buka seluruh route dalam tab terpisah;
- siapkan screenshot cadangan;
- simpan PDF laporan sebelumnya;
- pastikan browser tidak menawarkan update;
- matikan notifikasi sistem;
- jangan membuka file `.env`;
- periksa koneksi database melalui `/health/database`.
