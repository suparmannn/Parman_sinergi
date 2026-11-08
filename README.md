# Website Sinergi (sinergic.co.id)

Situs statis, mobile-first. Tidak ada dependency selain Python 3.

## Build dan preview

1. Jalankan `python3 build.py`. Hasilnya ada di `dist/`.
2. Jalankan `python3 -m http.server 8000 -d dist`.
3. Buka http://localhost:8000.

Jangan buka file di `dist/` langsung dengan `file://`. Link memakai path absolut (`/kontak/`), jadi perlu server.

## Struktur

| Path | Isi |
|---|---|
| `build.py` | Layout, data produk dan lowongan, template semua halaman |
| `static/` | `styles.css` dan `assets/`, disalin apa adanya ke `dist/` |
| `content/posts.json` | 51 berita dari situs WordPress lama |
| `content/clients.json` | Daftar klien `[nama, kota]` |
| `dist/` | Hasil build. Jangan edit manual |

## Ubah konten

- Produk, lowongan, visi-misi, angka statistik: edit `build.py`.
- Klien baru: tambah `[nama, kota]` di `content/clients.json`. Kalau kotanya baru, tambahkan juga di `ISLANDS` di `build.py`. Build gagal kalau kota belum terdaftar.
- Berita baru: tambah objek di `content/posts.json` dengan format yang sama.
- Screenshot aplikasi di bingkai laptop, tablet, atau ponsel: simpan sebagai `static/assets/ui/<slug>.png` atau `.jpg`, lalu build ulang. Contoh: `static/assets/ui/m-collection.png`. Tanpa file itu, layar memakai ilustrasi `static/assets/ui/<slug>.svg`. Jenis bingkai per produk ada di `DEVICE` di `build.py`. Rasio layar: laptop 16:10, tablet 4:3, ponsel 9:16. Gambar yang rasionya beda dipotong, bagian atas tetap terlihat.
- Logo klien: file di `static/assets/klien/`, daftar dan nama BPR di `CLIENT_LOGOS` di `build.py`.

## Sebelum go-live

- Gambar berita masih diambil dari `https://sinergic.co.id/wp-content/uploads/`. Salin folder itu ke hosting baru sebelum WordPress dimatikan.
- Form kontak membuka aplikasi email pengunjung. Untuk kirim langsung, pasang endpoint form di hosting.
- Redirect `berita-klien/*` memakai meta refresh. Ganti dengan aturan 301 di server.

## Deploy (Railway)

Railway membaca `Dockerfile`. Tahap 1 menjalankan `build.py`. Tahap 2 menyajikan `dist/` dengan Caddy (`Caddyfile`).

- Set variabel `PORT=8080` di service Railway.
- `Caddyfile` mengirim header `noindex` supaya domain preview tidak masuk Google. Hapus header itu saat situs pindah ke sinergic.co.id.
