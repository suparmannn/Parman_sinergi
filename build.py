#!/usr/bin/env python3
"""Build the static Sinergi site into dist/.

Run:     python3 build.py
Preview: python3 -m http.server 8000 -d dist   (then open http://localhost:8000)
"""
import html
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).parent
DIST = ROOT / 'dist'
SITE = 'https://sinergic.co.id'
WA = '6285175249728'
e = html.escape

POSTS = json.loads((ROOT / 'content/posts.json').read_text(encoding='utf-8'))
CLIENTS = json.loads((ROOT / 'content/clients.json').read_text(encoding='utf-8'))

MONTHS = 'Januari Februari Maret April Mei Juni Juli Agustus September Oktober November Desember'.split()


def tanggal(iso):
    y, m, d = iso.split('-')
    return '%d %s %s' % (int(d), MONTHS[int(m) - 1], y)


ICONS = {
    'chat': '<path d="M21 12a8 8 0 0 1-11.6 7.1L3 21l1.9-6.4A8 8 0 1 1 21 12Z"/>',
    'pin': '<path d="M12 22s-7-6.3-7-12a7 7 0 0 1 14 0c0 5.7-7 12-7 12Z"/><circle cx="12" cy="10" r="2.5"/>',
    'mail': '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m2 6 10 7 10-7"/>',
    'tel': '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2Z"/>',
    'db': '<ellipse cx="12" cy="5" rx="8" ry="3"/><path d="M4 5v14c0 1.7 3.6 3 8 3s8-1.3 8-3V5M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3"/>',
    'learn': '<path d="M22 9 12 4 2 9l10 5 10-5Z"/><path d="M6 11v5c3 2.5 9 2.5 12 0v-5"/>',
    'support': '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="3.5"/><path d="m5.6 5.6 3.9 3.9M14.5 14.5l3.9 3.9M18.4 5.6l-3.9 3.9M9.5 14.5l-3.9 3.9"/>',
    'cloud': '<path d="M17.5 19a4.5 4.5 0 1 0-1.4-8.8A6 6 0 0 0 4.5 12.5 3.5 3.5 0 0 0 6 19Z"/>',
    'growth': '<path d="m3 17 6-6 4 4 8-8"/><path d="M14 7h7v7"/>',
    'shield': '<path d="M12 22s8-3.5 8-10V5l-8-3-8 3v7c0 6.5 8 10 8 10Z"/><path d="m8.5 12 2.5 2.5 4.5-5"/>',
    'check': '<circle cx="12" cy="12" r="9"/><path d="m8 12 3 3 5-6"/>',
    'printer': '<path d="M6 9V3h12v6"/><rect x="3" y="9" width="18" height="8" rx="2"/><path d="M6 14h12v7H6z"/>',
    'wallet': '<rect x="2" y="6" width="20" height="14" rx="2"/><path d="M2 10h20M16 15h2"/>',
    'users': '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20c.8-3.5 3.4-5.5 6.5-5.5s5.7 2 6.5 5.5"/><circle cx="17" cy="9" r="2.5"/><path d="M16.5 14.6c2.4.3 4.2 2.1 4.9 5.4"/>',
}


def icon(name, cls='icon'):
    return '<svg class="%s" viewBox="0 0 24 24" aria-hidden="true">%s</svg>' % (cls, ICONS[name])


# Products. "card" is the short text for cards; "summary" is the full lead; "body" is trusted HTML.
PRODUCTS = [
    dict(slug='coreplus', name='ARB+', logo='logo-arb.png',
         card='Core Banking System BPR berbasis web, sesuai POJK, dan berjalan di cloud.',
         summary='Core Banking System BPR berbasis web yang mudah dipakai, sudah sesuai POJK, dan memiliki fitur lengkap untuk operasional BPR. Berjalan di cloud dengan standar internasional.',
         body='''
<h2>Infrastruktur cloud</h2>
<p>ARB+ berjalan di colocation server pada 3 gedung data center Tier 3 di Indonesia.</p>
<p>Infrastrukturnya high availability. Setiap update data di server Data Center (DC) otomatis tersalin ke server DRC. Bila server DC bermasalah, server DRC langsung mengambil alih secara real time.</p>
<h2>Fitur utama</h2>
<div class="features">
  <div><h3>Data nasabah (Single CIF)</h3><p>Satu data nasabah dengan portofolio semua rekening: tabungan, deposito, dan pinjaman. Terpusat untuk semua kantor. Mendukung APU-PPT dan kolektibilitas pinjaman dengan konsep one obligor.</p></div>
  <div><h3>Pajak dan spesimen</h3><p>Pembebanan pajak bunga tabungan dan deposito per CIF sesuai ketentuan pajak. Maksimal 4 spesimen tanda tangan per nasabah.</p></div>
  <div><h3>Tabungan dan deposito</h3><p>Modul Tabungan untuk produk tabungan umum dan tabungan berjangka. Modul Deposito.</p></div>
  <div><h3>Pinjaman</h3><p>Cetak Perjanjian Kredit, dokumen pencairan, dan Surat Peringatan langsung dari sistem. Termasuk submodul interface laporan SLIK.</p></div>
  <div><h3>Teller</h3><p>Modul Teller untuk semua transaksi harian di kantor BPR.</p></div>
  <div><h3>General Ledger</h3><p>Sistem General Ledger dengan submodul Aktiva Tetap. Pilihan metode straight line atau double declining.</p></div>
  <div><h3>Pelaporan</h3><p>Dukungan laporan bulanan APOLO, laporan OBOX, dan laporan Tingkat Kesehatan Bank.</p></div>
</div>'''),
    dict(slug='aplikasi-pelaporan-tks', name='Pelaporan TKS, Manajemen Risiko & Tata Kelola', logo='produk-tks.png',
         card='Laporan dan monitoring tingkat kesehatan BPR, bulanan dan semesteran, dengan cepat dan akurat.',
         summary='Aplikasi berbasis web untuk pelaporan dan monitoring tingkat kesehatan BPR, semesteran dan bulanan, dengan cepat dan akurat. Mencakup rasio keuangan, profil risiko, dan tata kelola BPR.',
         body=''),
    dict(slug='e-kyc', name='e-KYC', logo='produk-e-kyc.png',
         card='Verifikasi data dan foto selfie calon nasabah ke Dukcapil melalui VIDA. Mencegah pemalsuan identitas.',
         summary='Verifikasi data demografi dan foto selfie calon nasabah BPR dengan data kependudukan Dukcapil, melalui VIDA. Memastikan data nasabah cocok dan mengurangi pemalsuan identitas.',
         body='''
<h2>Bekerja sama dengan VIDA</h2>
<p>VIDA adalah penyedia layanan tanda tangan digital dan verifikasi e-KYC yang berizin dari Kominfo dan OJK. VIDA bekerja sama dengan sumber data resmi, seperti Dukcapil Kemendagri dan operator telekomunikasi.</p>
<h2>Kenapa lebih efektif</h2>
<ul>
  <li>Memverifikasi foto selfie calon nasabah, bukan hanya data demografi.</li>
  <li>Liveness detection memastikan objek adalah orang hidup, bukan foto ulang, rekaman video, atau topeng.</li>
  <li>Mencegah pemalsuan e-KTP oleh calon nasabah atau debitur.</li>
  <li>Terhubung lewat API antara CBS ARB/ARB+ dan sistem VIDA.</li>
</ul>'''),
    dict(slug='m-approval', name='M-Approval', logo='produk-m-approval.png',
         card='Aplikasi Android untuk Direksi dan Pejabat BPR. Setujui transaksi CBS dari luar kantor.',
         summary='Aplikasi Android untuk Direksi dan Pejabat BPR. Mereka tetap bisa menyetujui transaksi dan pemeliharaan data CBS dari luar kantor BPR.',
         body=''),
    dict(slug='virtual-account', name='Virtual Account', logo='produk-virtual-account.png',
         card='Nasabah setor ke tabungan atau pinjaman secara real time lewat ATM, m-banking, Alfamart, atau Indomaret.',
         summary='Nasabah bisa membayar atau menyetor ke rekening tabungan dan pinjaman di BPR secara online dan real time. Lewat ATM, m-banking, e-banking, atau gerai Alfamart dan Indomaret.',
         body='''
<h2>Integrasi</h2>
<p>Sinergi mendukung integrasi Virtual Account bank umum dan convenience store seperti Alfamart dan Indomaret. Integrasi bisa langsung ke bank umum (BCA, BNI, PermataBank) atau lewat payment gateway Faspay.</p>
<h2>Manfaat</h2>
<p>Transfer masuk VA berjalan host-to-host. Setiap transfer atau pembayaran nasabah langsung dibukukan secara real time ke rekening tabungan atau pinjaman di CBS ARB/ARB+. Operasional BPR jadi lebih efisien.</p>'''),
    dict(slug='m-collection', name='M-Collection', logo='produk-m-collection.png',
         card='Aplikasi Android untuk petugas kolektor. Terima setoran tunai di lapangan, langsung tercatat di CBS.',
         summary='Aplikasi Android untuk petugas marketing dan kolektor BPR. Petugas menerima setoran tunai ke rekening tabungan atau pinjaman di luar kantor, terhubung online dan real time ke CBS.',
         body='''
<p>Petugas menerima setoran tabungan dan angsuran pinjaman di lokasi nasabah. Karena terhubung real time ke Core Banking System, risiko penyalahgunaan oleh petugas jadi lebih kecil.</p>
<h2>Keamanan</h2>
<ul>
  <li>Tim Sinergi mendaftarkan pengguna dengan persetujuan Pejabat Sinergi, berdasarkan surat permintaan tertulis yang ditandatangani Pejabat BPR.</li>
  <li>Setiap perangkat terdaftar dengan Device ID, termasuk handphone dan printer bluetooth portable.</li>
  <li>Koneksi dari perangkat Android ke Web Mobile Collection Server dan ke CBS ARB/ARB+ terenkripsi.</li>
  <li>Setiap setoran tunai punya struk yang bisa dicetak ulang.</li>
  <li>Setoran baru efektif setelah Pejabat Operasional kantor BPR menyetujuinya di sistem ARB/ARB+.</li>
</ul>
<h2>Fleksibel</h2>
<ul>
  <li>BPR menentukan sendiri pengadaan perangkat Android (handphone atau tablet) dan printer bluetooth portable.</li>
  <li>Jaringan komunikasi menyesuaikan kondisi jaringan terbaik di wilayah BPR.</li>
</ul>'''),
    dict(slug='sms-notification', name='Notifikasi SMS / WhatsApp', logo='produk-sms-notification.png',
         card='Notifikasi transaksi otomatis ke nasabah, terhubung langsung dengan data CBS.',
         summary='Notifikasi otomatis ke nasabah BPR lewat SMS atau WhatsApp, terhubung dengan data dan transaksi nasabah di CBS.',
         body='''
<h2>SMS Notifikasi</h2>
<ul>
  <li>Pengirim SMS atas nama BPR (SMS masking, maksimal 11 karakter).</li>
  <li>1 SMS maksimal 160 karakter. Pesan 200 karakter terkirim sebagai 2 SMS.</li>
  <li>Mendukung 5 operator: Telkomsel, Indosat, Smartfren, XL, dan Three.</li>
</ul>
<h3>Jenis SMS</h3>
<dl>
  <dt>Harian</dt><dd>Ucapan ulang tahun, pengingat angsuran jatuh tempo (beberapa hari sebelumnya, sesuai parameter), dan tunggakan angsuran.</dd>
  <dt>Real time</dt><dd>Transfer masuk VA, setoran Mobile Collection, setoran tunai, penarikan tunai, break deposito, dan transfer keluar via PermataBank.</dd>
  <dt>Blast / promosi</dt><dd>BPR menyiapkan file Excel berisi nomor HP, nama nasabah, dan pesan. Bisa juga dikirim ke operator atau kondisi tertentu.</dd>
</dl>
<h2>WhatsApp Notifikasi</h2>
<ul>
  <li>Pesan memakai sender ID atas nama BPR, misalnya BANKSINERGI.</li>
  <li>Terhubung dengan data CBS ARB/ARB+.</li>
  <li>3 kategori pesan: Marketing, Authentication, dan Utility.</li>
</ul>'''),
]
FLAGSHIP, SUPPORT = PRODUCTS[0], PRODUCTS[1:]

JOBS = [
    dict(slug='implementor-staff', title='Implementor Staff', place='Tangerang (Alam Sutera)',
         tasks=['Menyiapkan implementasi: pengolahan data, migrasi data, dan lainnya.',
                'Menjalankan implementasi, termasuk pelatihan langsung ke klien.',
                'Menangani masalah klien dari awal sampai akhir masa garansi.'],
         reqs=['D3/S1 Akuntansi.',
               'Mampu mengajar dan berkomunikasi dengan baik.',
               'Menguasai pengolahan data Ms. Excel (VLOOKUP, Pivot Table).',
               'Memahami akuntansi. Akuntansi perbankan menjadi nilai plus.',
               'Bersedia ditugaskan ke luar kota.',
               'Pengalaman kerja di bidang IT atau perbankan menjadi nilai plus.',
               'Memahami peraturan perbankan menjadi nilai plus.',
               'Domisili Tangerang dan sekitarnya, atau bersedia pindah ke Tangerang (Alam Sutera).']),
]

# Each client city belongs to exactly one island group. A new city in clients.json fails the build here.
ISLANDS = {
    'Sumatera': 'Medan|Pekanbaru|Batam|Tanjung Pinang|Jambi|Palembang|Lampung',
    'Jawa': 'Jakarta|Bogor|Depok|Tangerang|Bekasi|Bandung|Sukabumi|Cianjur|Lebak|Yogyakarta|Solo|Semarang|Surabaya',
    'Kalimantan': 'Pontianak|Balikpapan',
    'Sulawesi': 'Manado|Minahasa|Gorontalo|Makasar|Gowa|Kendari|Kolaka|Kolaka Utara|Konawe|Konawe Selatan|Konawe Utara|Wakatobi|Bombana|Buton|Buton Utara|Baubau|Muna',
    'Bali & Nusa Tenggara': 'Bali|Lombok Barat',
    'Maluku': 'Ternate',
}
ISLAND_OF = {c: i for i, cs in ISLANDS.items() for c in cs.split('|')}
BY_ISLAND = {i: [] for i in ISLANDS}
for _name, _city in CLIENTS:
    BY_ISLAND[ISLAND_OF[_city]].append((_name, _city))
assert sum(map(len, BY_ISLAND.values())) == len(CLIENTS)

CATEGORIES = [('implementasi', 'Implementasi'), ('acara-umum', 'Acara Umum'),
              ('acara-internal', 'Acara Internal'), ('press', 'Press')]

# Old URLs that duplicate a post. A static host cannot send 301s, so these pages redirect with meta refresh.
# shortcut: meta refresh redirects, switch to server 301 rules when the host is known.
REDIRECTS = {
    'berita-klien/selamat-bergabung-pt-bpr-%s' % s: t for s, t in [
        ('millenia', 'implementasi-core-banking-system-arb-pt-bpr-millenia'),
        ('semesta-megadana', 'implementasi-core-banking-system-arb-pt-bpr-semesta-megadana'),
        ('adji-caka', 'implementasi-core-banking-system-arb-pt-bpr-adji-caka'),
        ('putra-batam', 'implementasi-core-banking-system-arb-pt-bpr-putra-batam'),
        ('artatama-sejahtera', 'implementasi-core-banking-system-arb-pt-bpr-artatama-sejahtera'),
        ('brata-bhakti-sejahtera', 'selamat-bergabung-pt-bpr-brata-bhakti-sejahtera'),
        ('musi-arta-lestari', 'selamat-bergabung-pt-bpr-musi-arta-lestari'),
    ]
}

PRODUCT = {p['slug']: p for p in PRODUCTS}

# Top-level menu. Items with children get a dropdown on desktop and an accordion on phones.
NAV = [
    ('produk-layanan/', 'Produk & Layanan',
     [('produk-layanan/', 'Semua produk')] +
     [('produk-layanan/%s/' % p['slug'], 'ARB+ Core Banking System' if p is FLAGSHIP else p['name']) for p in PRODUCTS]),
    ('tentang-kami/', 'Tentang Kami',
     [('tentang-kami/', 'Profil perusahaan'), ('tentang-kami/#visi-misi', 'Visi & misi'),
      ('tentang-kami/#struktur', 'Struktur organisasi'), ('tentang-kami/#mitra', 'Mitra kami')]),
    ('berita-acara/', 'Berita & Acara',
     [('berita-acara/', 'Semua berita')] + [('category/%s/' % s, n) for s, n in CATEGORIES]),
    ('klien-kami/', 'Klien Kami', []),
    ('karier/', 'Karier', []),
]


def nav_html(section):
    out = []
    for href, label, children in NAV:
        link = '<a href="/%s" class="nav__link"%s>%s</a>' % (
            href, ' aria-current="page"' if href == section else '', e(label))
        if not children:
            out.append(link)
            continue
        out.append('<div class="nav__item">%s<button class="nav__toggle" type="button" aria-expanded="false" '
                   'aria-label="Submenu %s"></button><div class="nav__menu">%s</div></div>' % (
                       link, e(label), ''.join('<a href="/%s">%s</a>' % (h, e(t)) for h, t in children)))
    return ''.join(out)


MENU_JS = '''<script>
  const btn = document.querySelector('.menu-btn');
  btn.addEventListener('click', () => {
    const open = btn.getAttribute('aria-expanded') !== 'true';
    btn.setAttribute('aria-expanded', open);
    document.body.classList.toggle('nav-open', open);
  });
  // Submenu toggles. Opening one submenu closes the others.
  document.querySelectorAll('.nav__toggle').forEach(t => t.addEventListener('click', () => {
    const item = t.parentElement;
    const open = !item.classList.contains('open');
    document.querySelectorAll('.nav__item.open').forEach(o => {
      o.classList.remove('open');
      o.querySelector('.nav__toggle').setAttribute('aria-expanded', false);
    });
    item.classList.toggle('open', open);
    t.setAttribute('aria-expanded', open);
  }));
</script>'''

FOOTER = '''
<footer class="footer">
  <div class="container footer__grid">
    <div class="footer__about">
      <img src="/assets/logo-white.png" alt="Sinergi" width="432" height="168" class="footer__logo" loading="lazy">
      <p>PT Sinergi Prakarsa Utama. Penyedia Core Banking System untuk BPR sejak 2009.</p>
      <p class="footer__social"><a href="https://www.instagram.com/sinergic.co.id">Instagram</a><a href="https://www.facebook.com/profile.php?id=61551558174894">Facebook</a></p>
    </div>
    <div class="footer__office">
      <h2>Kantor</h2>
      <address><strong>Kantor Pusat</strong>Ruko The Prominence Blok 38-H No. 10, Jl. Jalur Sutera Boulevard, Alam Sutera, Panunggangan Timur, Pinang, Kota Tangerang, Banten 15143</address>
      <address><strong>Kantor Cabang</strong>Ruko Klampis 21 Blok AA No. 2, Jl. Arief Rahman Hakim, Surabaya 60117</address>
    </div>
    <div>
      <h2>Perusahaan</h2>
      <ul class="footer__list">
        <li><a href="/tentang-kami/">Tentang Kami</a></li>
        <li><a href="/klien-kami/">Klien Kami</a></li>
        <li><a href="/berita-acara/">Berita &amp; Acara</a></li>
        <li><a href="/karier/">Karier</a></li>
        <li><a href="/kontak/">Kontak</a></li>
      </ul>
    </div>
    <div>
      <h2>Produk</h2>
      <ul class="footer__list">%s</ul>
    </div>
    <div class="footer__contact">
      <h2>Hubungi Kami</h2>
      <ul class="footer__list">
        <li><a href="tel:+622180821315">021-8082-1315</a></li>
        <li><a href="tel:+622180821316">021-8082-1316</a></li>
        <li><a href="mailto:cs@sinergic.co.id">cs@sinergic.co.id</a></li>
      </ul>
      <div class="footer__actions">
        <a href="https://wa.me/%s" class="btn btn--accent btn--sm">Chat WhatsApp</a>
        <a href="/kontak/" class="btn btn--outline-light btn--sm">Kirim Pesan</a>
      </div>
    </div>
  </div>
  <div class="footer__bar"><div class="container">© 2026 PT Sinergi Prakarsa Utama</div></div>
</footer>''' % (''.join('<li><a href="/produk-layanan/%s/">%s</a></li>' % (p['slug'], e(p['name'])) for p in PRODUCTS), WA)

SITEMAP = []


def write(path, doc, in_sitemap=True):
    """Write dist/<path>index.html, or dist/<path> when path is a file name."""
    f = DIST / path if path.endswith('.html') else DIST / path / 'index.html'
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(doc, encoding='utf-8')
    if in_sitemap:
        SITEMAP.append(path)


def page(path, title, desc, body, section='', image='', js='', in_sitemap=True):
    full_title = title if not path else '%s | Sinergi' % title
    og_image = image or SITE + '/assets/logo.png'
    doc = '''<!doctype html>
<html lang="id">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{site}/{path}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="Sinergi Prakarsa Utama">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:image" content="{og_image}">
  <meta name="theme-color" content="#003c71">
  <link rel="icon" type="image/png" href="/assets/favicon.png">
  <link rel="apple-touch-icon" href="/assets/favicon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/styles.css">
</head>
<body>
  <a class="skip" href="#konten">Lewati ke konten</a>
  <header class="header">
    <div class="container header__bar">
      <a href="/" class="header__logo"><img src="/assets/logo.png" alt="Sinergi" width="432" height="168"></a>
      <button class="menu-btn" aria-expanded="false" aria-controls="nav" aria-label="Buka menu"><span></span><span></span><span></span></button>
      <nav id="nav" class="nav" aria-label="Menu utama">
        {nav}
        <a href="/kontak/" class="btn btn--primary nav__cta">Hubungi Kami</a>
      </nav>
    </div>
  </header>
  <main id="konten">
{body}
  </main>
{footer}
  <a href="https://wa.me/{wa}" class="chat-float" aria-label="Chat WhatsApp dengan Sinergi">{chat_icon}<span>Chat WA</span></a>
{menu_js}
{js}
</body>
</html>
'''.format(title=e(full_title), desc=e(desc), site=SITE, path=path, og_image=e(og_image), nav=nav_html(section),
           body=body, footer=FOOTER, menu_js=MENU_JS, js=js, wa=WA,
           chat_icon='<svg viewBox="0 0 24 24" aria-hidden="true">%s</svg>' % ICONS['chat'])
    write(path, doc, in_sitemap)


def page_hero(crumb, h1, lead='', extra=''):
    """Dark page header. crumb is trusted HTML for the breadcrumb after "Beranda" (it may hold a parent link)."""
    return '''
<section class="page-hero">
  <div class="container">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Beranda</a><span aria-hidden="true">/</span>%s</nav>
    <h1>%s</h1>
    %s%s
  </div>
</section>''' % (crumb, h1, '<p class="lead">%s</p>' % lead if lead else '', extra)


def stats(items):
    return '<ul class="stats" aria-label="Sinergi dalam angka">%s</ul>' % ''.join(
        '<li><strong>%s</strong><span>%s</span></li>' % x for x in items)


STATS = [('17', 'tahun pengalaman, sejak 2009'), ('105', 'BPR klien di seluruh Indonesia'),
         ('8,1%', 'pangsa pasar dari 1.291 BPR')]


def product_card(p, level='h3'):
    return '<a href="/produk-layanan/%s/" class="card">%s<%s>%s</%s><p>%s</p></a>' % (
        p['slug'], '<span class="card__logo"><img src="/assets/%s" alt="" loading="lazy"></span>' % p['logo'], level, e(p['name']), level, e(p['card']))


def product_cards(items, level='h3'):
    return '<div class="cards">%s</div>' % ''.join(product_card(p, level) for p in items)


FLAGSHIP_CARD = '''
<a href="/produk-layanan/coreplus/" class="flagship">
  <img src="/assets/logo-arb.png" alt="ARB+" width="1400" height="617" class="flagship__logo">
  <div>
    <h3>ARB+ Core Banking System</h3>
    <p>%s</p>
    <ul class="checks">
      <li>3 data center Tier 3 dengan DRC otomatis</li>
      <li>Tabungan, deposito, pinjaman, teller, dan GL</li>
      <li>Laporan APOLO, OBOX, SLIK, dan tingkat kesehatan bank</li>
    </ul>
    <span class="link">Pelajari ARB+ →</span>
  </div>
</a>''' % e(FLAGSHIP['summary'])

PARTNERS = '''
<ul class="partners">
  <li><img src="/assets/partner-bca.png" alt="BCA" loading="lazy"></li>
  <li><img src="/assets/partner-bni.png" alt="BNI" loading="lazy"></li>
  <li><img src="/assets/partner-permata.png" alt="PermataBank" loading="lazy"></li>
  <li><img src="/assets/partner-vida.png" alt="VIDA" loading="lazy"></li>
  <li><img src="/assets/partner-espay.png" alt="Espay" loading="lazy"></li>
  <li><img src="/assets/partner-faspay.png" alt="Faspay" loading="lazy"></li>
  <li><img src="/assets/partner-wowrack.png" alt="Wowrack" loading="lazy"></li>
  <li><img src="/assets/partner-aptana.png" alt="Aptana" loading="lazy"></li>
  <li><img src="/assets/partner-rackh.png" alt="RACKH" loading="lazy"></li>
</ul>'''


def post_card(p):
    # shortcut: post images load from the old WordPress uploads, copy wp-content/uploads before the old site goes down.
    return '''<a href="/{path}/" class="news__item"><img src="{img}" alt="" loading="lazy"><span class="tag">{cat}</span><h3>{title}</h3><time datetime="{date}">{when}</time></a>'''.format(
        path=p['path'], img=e(p['image']), cat=e(p['category']), title=e(p['title']), date=p['date'],
        when=tanggal(p['date']))


def text(v):
    return e(v).replace('\n', '<br>')


def render_blocks(blocks, title):
    """Turn scraped blocks into HTML. Runs of list items become <ul>; runs of images become a gallery."""
    out, i, n_img = [], 0, 0
    while i < len(blocks):
        kind = blocks[i][0]
        if kind in ('img', 'li'):
            j = i
            while j < len(blocks) and blocks[j][0] == kind:
                j += 1
            if kind == 'li':
                out.append('<ul>%s</ul>' % ''.join('<li>%s</li>' % text(v) for _, v in blocks[i:j]))
            else:
                items = []
                for _, url in blocks[i:j]:
                    n_img += 1
                    items.append('<a href="%s"><img src="%s" alt="%s, foto %d" loading="lazy"></a>' % (
                        e(url), e(url), e(title), n_img))
                out.append('<div class="gallery">%s</div>' % ''.join(items))
            i = j
            continue
        v = blocks[i][1]
        if v.strip() != title.strip():
            tag = {'h2': 'h2', 'h3': 'h2', 'h4': 'h3'}.get(kind, 'p')
            out.append('<%s>%s</%s>' % (tag, text(v), tag))
        i += 1
    return '\n'.join(out)


MOCKUP_LAPTOP = '''<div class="mockup" aria-hidden="true">
  <div class="mockup__bar"><span></span><span></span><span></span><em>ARB+ Core Banking System</em></div>
  <div class="mockup__body">
    <div class="mockup__side"><i class="on"></i><i></i><i></i><i></i><i></i></div>
    <div class="mockup__main">
      <div class="mockup__tiles"><b></b><b></b><b></b></div>
      <svg class="mockup__chart" viewBox="0 0 300 90" preserveAspectRatio="none">
        <path d="M0 70 L40 62 L80 66 L120 48 L160 52 L200 34 L240 38 L300 16 L300 90 L0 90 Z" fill="rgba(0,167,157,.14)"/>
        <path d="M0 70 L40 62 L80 66 L120 48 L160 52 L200 34 L240 38 L300 16" fill="none" stroke="#00a79d" stroke-width="2.5"/>
      </svg>
      <div class="mockup__rows"><i></i><i></i><i></i></div>
    </div>
  </div>
</div>'''

# "Layanan Kami" cards: (icon, title, text, link, link label). The facts come from the old site:
# the implementor job description, the ARB+ infrastructure text, and the training posts.
SERVICES = [
    ('db', 'Implementasi & migrasi data', 'Tim kami menyiapkan dan memigrasikan data BPR ke ARB+.',
     'category/implementasi/', 'Lihat implementasi'),
    ('learn', 'Pelatihan pengguna', 'Pelatihan langsung untuk staf BPR, plus workshop regulasi.',
     'category/acara-umum/', 'Lihat kegiatan'),
    ('support', 'Pendampingan', 'Kami menangani kendala klien dari awal sampai akhir masa garansi.',
     'kontak/', 'Hubungi kami'),
    ('cloud', 'Cloud & DRC', 'ARB+ berjalan di 3 data center Tier 3 dengan DRC otomatis.',
     'produk-layanan/coreplus/', 'Pelajari ARB+'),
]

# Mission text is verbatim from the company. Only the short titles are new.
MISSIONS = [
    ('growth', 'Selalu berkembang', 'Terus berkembang untuk memenuhi seluruh kebutuhan client.'),
    ('shield', 'Dukungan optimal, biaya ekonomis',
     'Memberikan dukungan Core Banking System yang optimal dengan biaya yang ekonomis.'),
    ('users', 'Tumbuh bersama', 'Menjalin Sinergi untuk kemajuan bersama.'),
]

HOME_JS = '''<script>
  // Hero slider: next slide every 6 s. Hover, focus, touch, and reduced motion stop it.
  // shortcut: no pause button (owner's choice), so WCAG 2.2.2 is not fully met. Add one if an accessibility audit asks for it.
  (() => {
    const hero = document.querySelector('.hero');
    const track = hero.querySelector('.hero__track');
    const slides = [...track.children];
    const dots = [...hero.querySelectorAll('.hero__dots button')];
    const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
    let i = 0, timer = 0, paused = reduce, hold = false;
    const go = n => {
      i = (n + slides.length) % slides.length;
      track.scrollTo({ left: i * track.clientWidth, behavior: reduce ? 'auto' : 'smooth' });
    };
    const start = () => {
      clearInterval(timer);
      if (!paused && !hold) timer = setInterval(() => go(i + 1), 6000);
    };
    // Keep the dots in sync with swipes as well as with button clicks.
    const io = new IntersectionObserver(list => list.forEach(en => {
      if (!en.isIntersecting) return;
      i = slides.indexOf(en.target);
      dots.forEach((d, k) => d.setAttribute('aria-current', k === i));
    }), { root: track, threshold: 0.6 });
    slides.forEach(s => io.observe(s));
    dots.forEach((d, k) => d.addEventListener('click', () => { go(k); start(); }));
    hero.querySelector('.hero__arrow--prev').addEventListener('click', () => { go(i - 1); start(); });
    hero.querySelector('.hero__arrow--next').addEventListener('click', () => { go(i + 1); start(); });
    const holdOn = () => { hold = true; start(); };
    const holdOff = () => { hold = false; start(); };
    hero.addEventListener('mouseenter', holdOn);
    hero.addEventListener('mouseleave', holdOff);
    hero.addEventListener('focusin', holdOn);
    hero.addEventListener('focusout', holdOff);
    track.addEventListener('touchstart', () => { paused = true; start(); }, { passive: true });
    start();
  })();

  // Carousel arrows (desktop). Phones swipe.
  document.querySelectorAll('.rail-wrap').forEach(w => {
    const rail = w.querySelector('.rail');
    w.querySelectorAll('.rail-btn').forEach(b => b.addEventListener('click', () => {
      const dir = b.classList.contains('rail-btn--prev') ? -1 : 1;
      rail.scrollBy({ left: dir * rail.clientWidth * 0.9, behavior: 'smooth' });
    }));
  });

  // News tabs
  const tabs = [...document.querySelectorAll('[role=tab]')];
  tabs.forEach(t => t.addEventListener('click', () => tabs.forEach(o => {
    const on = o === t;
    o.setAttribute('aria-selected', on);
    document.getElementById(o.getAttribute('aria-controls')).hidden = !on;
  })));
</script>'''


def hero_slider():
    """Banner slider: the company vision, ARB+, and the newest client-facing news post."""
    news = next(p for p in POSTS if p['category'] in ('Implementasi', 'Acara Umum'))
    team = ('<img src="/assets/foto-tim-hut-17.jpg" srcset="/assets/foto-tim-hut-17-800.jpg 800w, '
            '/assets/foto-tim-hut-17.jpg 1600w" sizes="100vw" alt="" class="slide__bg" fetchpriority="high">')
    slides = [
        # The first slide is the largest paint on load, so its photo loads early and phones get the 800px file.
        ('slide--photo', team, '''
      <div class="slide__text">
        <p class="slide__kicker">Visi kami</p>
        <h1>Menjadi Penyedia Solusi Core Banking System yang handal dan terpercaya</h1>
        <p>Sejak 2009, kami mendampingi BPR di seluruh Indonesia.</p>
        <div class="slide__actions"><a href="/tentang-kami/" class="btn btn--light">Tentang Kami</a></div>
      </div>'''),
        ('slide--product', '', '''
      <div class="slide__text">
        <p class="slide__kicker">ARB+ Core Banking System</p>
        <h2>Core Banking System terdepan untuk BPR di Indonesia</h2>
        <p>ARB+ berbasis web, sesuai POJK, dan berjalan di cloud dengan data center Tier 3.</p>
        <div class="slide__actions">
          <a href="/kontak/" class="btn btn--light">Jadwalkan Demo</a>
          <a href="/produk-layanan/" class="btn btn--outline-light">Lihat Produk</a>
        </div>
      </div>
      <div class="slide__visual">%s</div>''' % MOCKUP_LAPTOP),
        ('slide--photo slide--news', '<img src="%s" alt="" class="slide__bg" loading="lazy">' % e(news['image']), '''
      <div class="slide__text">
        <p class="slide__kicker">Berita terbaru · %s</p>
        <h2>%s</h2>
        <p>%s</p>
        <div class="slide__actions"><a href="/%s/" class="btn btn--light">Baca Selengkapnya</a></div>
      </div>''' % (e(news['category']), e(news['title']), tanggal(news['date']), news['path'])),
    ]
    out = []
    for n, (cls, img, inner) in enumerate(slides, 1):
        out.append('<div class="slide %s" role="group" aria-roledescription="slide" aria-label="%d dari %d">'
                   '%s<div class="container slide__grid">%s\n    </div></div>' % (cls, n, len(slides), img, inner))
    dots = ''.join('<button type="button" aria-label="Slide %d"%s></button>' % (
        n, ' aria-current="true"' if n == 1 else '') for n in range(1, len(slides) + 1))
    return '''
<section class="hero" aria-roledescription="carousel" aria-label="Sorotan Sinergi">
  <div class="hero__track">%s</div>
  <button class="hero__arrow hero__arrow--prev" type="button" aria-label="Slide sebelumnya"></button>
  <button class="hero__arrow hero__arrow--next" type="button" aria-label="Slide berikutnya"></button>
  <div class="hero__controls">
    <div class="hero__dots">%s</div>
  </div>
</section>''' % (''.join(out), dots)


def pic(src, width, height, icons):
    """Product card picture: a round photo with two small icon badges on its edge. Decorative only."""
    return '<div class="pic" aria-hidden="true"><img src="/assets/%s" alt="" width="%d" height="%d" loading="lazy">%s</div>' % (
        src, width, height,
        ''.join('<span class="pic__icon pic__icon--%d">%s</span>' % (n, icon(ic, 'ico')) for n, ic in enumerate(icons, 1)))


def rail_carousel(cards, label):
    return '''<div class="rail-wrap">
      <button class="rail-btn rail-btn--prev" type="button" aria-label="Geser ke kiri"></button>
      <div class="rail rail--carousel" role="region" aria-label="%s" tabindex="0">%s</div>
      <button class="rail-btn rail-btn--next" type="button" aria-label="Geser ke kanan"></button>
    </div>''' % (e(label), cards)


def build_home():
    services = ''.join('''
      <a href="/%s" class="scard">
        <span class="scard__icon scard__icon--%d">%s</span>
        <h3>%s</h3>
        <p>%s</p>
        <span class="scard__more">%s →</span>
      </a>''' % (href, n, icon(ic, 'ico'), e(title), e(txt), e(more))
        for n, (ic, title, txt, href, more) in enumerate(SERVICES, 1))
    # The three card pictures are AI-generated illustrations (Gemini), not photos of Sinergi staff or clients.
    featured = [
        (FLAGSHIP, pic('ilustrasi-arb.jpg', 720, 538, ['cloud', 'shield'])),
        (PRODUCT['m-collection'], pic('ilustrasi-m-collection.jpg', 480, 480, ['wallet', 'printer'])),
        (PRODUCT['m-approval'], pic('ilustrasi-m-approval.jpg', 480, 480, ['check', 'shield'])),
    ]
    pcards = ''.join('''
      <a href="/produk-layanan/%s/" class="pcard">
        <div class="pcard__visual">%s</div>
        <div class="pcard__body">
          <h3><img src="/assets/%s" alt="%s" class="pcard__logo" loading="lazy"></h3>
          <p>%s</p>
          <span class="btn btn--ghost btn--sm">Selengkapnya</span>
        </div>
      </a>''' % (p['slug'], visual, p['logo'], e(p['name']), e(p['card'])) for p, visual in featured)
    missions = ''.join('''
        <div class="mcard"><span class="mcard__icon">%s</span><div><h3>%s</h3><p>%s</p></div></div>''' % (
        icon(ic, 'ico'), e(title), e(txt)) for ic, title, txt in MISSIONS)
    islands = ''.join('<li><span>%s</span><b>%d</b></li>' % (e(k), len(v)) for k, v in BY_ISLAND.items())
    dcards = ''.join('''
      <a href="/produk-layanan/%s/" class="dcard"><h3>%s</h3><p>%s</p><span class="dcard__more">Selengkapnya →</span></a>''' % (
        p['slug'], e(p['name']), e(p['card']))
        for p in (PRODUCT[s] for s in ('aplikasi-pelaporan-tks', 'e-kyc', 'virtual-account', 'sms-notification')))
    tab_sets = [('Semua', POSTS)] + [(n, [p for p in POSTS if p['category'] == n])
                                     for n in ('Acara Umum', 'Acara Internal', 'Press')]
    tabs = ''.join('<button type="button" role="tab" id="tab-%d" aria-controls="panel-%d" aria-selected="%s">%s</button>' % (
        n, n, 'true' if n == 0 else 'false', e(name)) for n, (name, _) in enumerate(tab_sets))
    panels = ''.join('<div class="rail rail--grid cols-4" role="tabpanel" id="panel-%d" aria-labelledby="tab-%d"%s>%s</div>' % (
        n, n, '' if n == 0 else ' hidden', ''.join(post_card(p) for p in posts[:4])) for n, (_, posts) in enumerate(tab_sets))

    body = hero_slider() + '''
<section class="section">
  <div class="container">
    <div class="sec-head">
      <h2>Layanan Kami</h2>
      <p>Dukungan lengkap, dari implementasi sampai operasional harian BPR.</p>
    </div>
    <div class="rail rail--grid cols-4">%(services)s
    </div>
  </div>
</section>

<section class="section section--tint" id="produk">
  <div class="container">
    <div class="sec-head">
      <h2>Solusi untuk setiap kebutuhan BPR</h2>
      <p>Dari kantor sampai lapangan, semua terhubung dengan ARB+.</p>
    </div>
    <div class="rail rail--grid cols-3">%(pcards)s
    </div>
  </div>
</section>

<section class="section showcase">
  <div class="container">
    <div class="sec-head sec-head--split">
      <div>
        <h2>Operasional BPR lebih mudah dengan ARB+</h2>
        <p>Satu sistem untuk data nasabah, transaksi, dan pelaporan.</p>
      </div>
      <a href="/produk-layanan/coreplus/" class="btn btn--primary">Pelajari ARB+</a>
    </div>
    <div class="showcase__grid">
      <div class="showcase__visual">
        %(mockup)s
      </div>
      <div class="showcase__list">
        <div class="fcard fcard--on"><h3>Berjalan di cloud</h3><p>3 data center Tier 3. Server DRC mengambil alih otomatis bila DC bermasalah.</p></div>
        <div class="fcard"><h3>Fitur operasional lengkap</h3><p>Data nasabah (Single CIF), tabungan, deposito, pinjaman, teller, dan General Ledger.</p></div>
        <div class="fcard"><h3>Siap untuk regulasi</h3><p>Laporan APOLO, OBOX, SLIK, dan tingkat kesehatan bank. <a href="/cbs-core-siap-untuk-penerapan-sak-ep/">Siap SAK EP</a>.</p></div>
      </div>
    </div>
  </div>
</section>

<section class="section section--flush-top">
  <div class="container">
    <div class="sec-head sec-head--split">
      <div>
        <h2>Implementasi terbaru</h2>
        <p>Kabar implementasi sistem Sinergi di BPR klien.</p>
      </div>
      <a href="/category/implementasi/" class="btn btn--primary">Lihat Semua</a>
    </div>
    %(impl)s
  </div>
</section>

<section class="band band--navy">
  <div class="container">
    <div class="sec-head sec-head--light">
      <p class="sec-head__kicker">Visi kami</p>
      <h2>Menjadi Penyedia Solusi Core Banking System yang handal dan terpercaya</h2>
      <p>Tiga misi yang kami jalankan untuk BPR di seluruh Indonesia.</p>
    </div>
    <div class="mission">
      <div class="mission__list">%(missions)s
        <a href="/tentang-kami/" class="btn btn--accent">Tentang Kami</a>
      </div>
      <figure class="mission__photo"><img src="/assets/foto-gathering-klien.jpg" alt="Pelatihan PDP dan Gathering Client Sinergi 2024" loading="lazy"></figure>
    </div>
  </div>
</section>

<section class="band band--mint">
  <div class="container">
    <div class="sec-head">
      <h2>Dipercaya BPR di seluruh Indonesia</h2>
      <p>Salah satu dari tiga vendor aplikasi BPR konvensional dengan pengguna terbanyak. Diakui dan direkomendasikan oleh OJK.</p>
    </div>
    <div class="reach">
      <div class="reach__text">
        <h3 class="caps">Dari Sumatera sampai Maluku</h3>
        <ul class="reach__stats">
          <li><strong>105</strong><span>BPR klien</span></li>
          <li><strong>8,1%%</strong><span>pangsa pasar</span></li>
          <li><strong>17</strong><span>tahun pengalaman</span></li>
        </ul>
        <a href="/klien-kami/" class="btn btn--ghost">Lihat Daftar Klien</a>
      </div>
      <div class="reach__card">
        <img src="/assets/peta-indonesia.png" alt="Peta sebaran klien Sinergi di Indonesia" width="1620" height="616" class="reach__map" loading="lazy">
        <ul class="reach__islands">%(islands)s</ul>
      </div>
    </div>
    <h2 class="row-title">Lengkapi dengan produk pendukung</h2>
    <div class="rail rail--grid cols-4">%(dcards)s
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="sec-head">
      <h2>Mitra &amp; integrasi</h2>
      <p>Terhubung dengan bank, payment gateway, e-KYC, dan penyedia infrastruktur.</p>
    </div>
    <div class="panel">%(partners)s</div>
  </div>
</section>

<section class="section section--flush-top">
  <div class="container">
    <div class="sec-head">
      <h2>Berita &amp; Acara</h2>
      <p>Ikuti kegiatan dan kabar terbaru dari Sinergi.</p>
    </div>
    <div class="tabs" role="tablist" aria-label="Kategori berita">%(tabs)s</div>
    <div class="news-box">%(panels)s</div>
    <p class="center"><a href="/berita-acara/" class="link">Lihat semua berita →</a></p>
  </div>
</section>''' % dict(services=services, pcards=pcards, mockup=MOCKUP_LAPTOP,
                     impl=rail_carousel(''.join(post_card(p) for p in POSTS if p['category'] == 'Implementasi'),
                                        'Implementasi terbaru'),
                     missions=missions, islands=islands, dcards=dcards, partners=PARTNERS, tabs=tabs, panels=panels)
    page('', 'Sinergi — Core Banking System untuk BPR di Indonesia',
         'PT Sinergi Prakarsa Utama menyediakan Core Banking System ARB+ berbasis web dan cloud untuk BPR. Dipakai 105 BPR di seluruh Indonesia sejak 2009.',
         body, js=HOME_JS)


def build_products():
    body = page_hero('Produk &amp; Layanan', 'Pilihan terbaik untuk perbankan di Indonesia',
                     'Satu Core Banking System dan enam produk pendukung untuk operasional BPR.') + '''
<section class="section section--first">
  <div class="container">
    {flagship}
    <h2 class="subhead">Produk pendukung</h2>
    {cards}
  </div>
</section>'''.format(flagship=FLAGSHIP_CARD, cards=product_cards(SUPPORT))
    page('produk-layanan/', 'Produk & Layanan',
         'Core Banking System ARB+ dan produk pendukung untuk BPR: Pelaporan TKS, e-KYC, M-Approval, Virtual Account, M-Collection, dan notifikasi SMS/WhatsApp.',
         body, section='produk-layanan/')

    for p in PRODUCTS:
        logo = '<img src="/assets/%s" alt="" class="product-logo">' % p['logo']
        actions = '''<div class="hero__actions"><a href="/kontak/" class="btn btn--primary">Minta Demo</a>
<a href="https://wa.me/%s" class="btn btn--ghost">Tanya via WhatsApp</a></div>''' % WA
        title = 'ARB+ Core Banking System' if p is FLAGSHIP else p['name']
        details = '''
<section class="section section--first">
  <div class="container prose">%s</div>
</section>''' % p['body'] if p['body'] else ''
        others = [o for o in PRODUCTS if o is not p]
        body = page_hero('<a href="/produk-layanan/">Produk &amp; Layanan</a>', logo + e(title), e(p['summary']), actions) + details + '''
<section class="section section--tint">
  <div class="container">
    <h2 class="subhead">Produk lainnya</h2>
    {cards}
  </div>
</section>'''.format(cards=product_cards(others))
        page('produk-layanan/%s/' % p['slug'], title, p['summary'], body, section='produk-layanan/')


def build_about():
    body = page_hero('Tentang Kami', 'Kemitraan strategis untuk sukses bersama',
                     'Sinergi adalah perusahaan teknologi informasi yang menyediakan aplikasi untuk industri keuangan, terutama Core Banking System untuk BPR konvensional.',
                     stats(STATS)) + '''
<section class="section">
  <div class="container">
    <figure class="about__photo">
      <img src="/assets/foto-tim-hut-17.jpg" alt="Keluarga besar Sinergi pada perayaan HUT ke-17" width="1600" height="1069" loading="lazy">
      <figcaption>Keluarga besar Sinergi pada perayaan HUT ke-17, September 2026.</figcaption>
    </figure>
  </div>
  <div class="container about">
    <div class="prose">
      <h2>PT Sinergi Prakarsa Utama</h2>
      <p>Sinergi termasuk satu dari tiga vendor aplikasi perbankan BPR konvensional dengan pengguna terbanyak di Indonesia. Sinergi diakui dan direkomendasikan oleh OJK.</p>
      <p>Tim kami terdiri dari tenaga profesional berpengalaman di bidang teknologi informasi dan perbankan, dengan rata-rata pengalaman di atas 10 tahun. Kami memberikan solusi teknologi yang andal, efektif, dan efisien untuk semua mitra.</p>
      <h3>Legalitas</h3>
      <p>Sinergi berdiri pada 14 Agustus 2009 berdasarkan Akta Nomor 14 dari Notaris Elizabeth Arlita Suryoko, SH, di Tangerang. Pendirian disahkan oleh Keputusan Menteri Hukum dan HAM RI Nomor AHU-39511.AH.01.01 Tahun 2009, tanggal 14 Agustus 2009.</p>
    </div>
    <div class="vm" id="visi-misi">
      <div class="vm__card vm__card--dark">
        <p class="eyebrow">Visi</p>
        <p class="vm__vision">Menjadi Penyedia Solusi Core Banking System yang handal dan terpercaya.</p>
      </div>
      <div class="vm__card">
        <p class="eyebrow">Misi</p>
        <ol class="vm__list">
          <li>Terus berkembang untuk memenuhi seluruh kebutuhan client.</li>
          <li>Memberikan dukungan Core Banking System yang optimal dengan biaya yang ekonomis.</li>
          <li>Menjalin Sinergi untuk kemajuan bersama.</li>
        </ol>
      </div>
    </div>
  </div>
  <div class="container org" id="struktur">
    <h2>Struktur organisasi</h2>
    <a href="/assets/struktur-organisasi.png"><img src="/assets/struktur-organisasi.png" alt="Bagan struktur organisasi PT Sinergi Prakarsa Utama" width="1920" height="1080" loading="lazy"></a>
    <p class="muted">Per Desember 2024. Ketuk gambar untuk melihat ukuran penuh.</p>
  </div>
</section>

<section class="section section--tint section--tight" id="mitra">
  <div class="container">
    <h2 class="subhead center">Mitra kami</h2>
    %s
  </div>
</section>''' % PARTNERS
    page('tentang-kami/', 'Tentang Kami',
         'Profil PT Sinergi Prakarsa Utama: penyedia Core Banking System untuk BPR sejak 2009. Visi, misi, dan legalitas perusahaan.',
         body, section='tentang-kami/')


def build_clients():
    groups = []
    for island, rows in BY_ISLAND.items():
        items = ''.join('<li class="client"><strong>%s</strong><span>%s</span></li>' % (e(n), e(c))
                        for n, c in sorted(rows))
        groups.append('<section class="client-group"><h2>%s <b>%d</b></h2><ul class="client-list">%s</ul></section>' % (
            e(island), len(rows), items))
    body = page_hero('Klien Kami', 'Pilihan utama BPR di seluruh Indonesia', '',
                     stats([('1.291', 'BPR konvensional di Indonesia per Mei 2026 (OJK)'),
                            ('105', 'BPR klien Sinergi per Juni 2026'),
                            ('8,1%', 'pangsa pasar Sinergi')])) + '''
<section class="section section--first">
  <div class="container">
    <img src="/assets/peta-indonesia.png" alt="Peta sebaran klien Sinergi di Indonesia" width="1620" height="616" class="clients-map" loading="lazy">
    <div class="search">
      <label for="cari">Cari BPR atau kota</label>
      <input id="cari" type="search" placeholder="Contoh: Palembang" autocomplete="off">
    </div>
    <p class="empty" hidden>Tidak ada klien yang cocok.</p>
    %s
  </div>
</section>''' % ''.join(groups)
    js = '''<script>
  const q = document.getElementById('cari');
  q.addEventListener('input', () => {
    const v = q.value.trim().toLowerCase();
    document.querySelectorAll('.client').forEach(li => { li.hidden = !li.textContent.toLowerCase().includes(v); });
    let any = false;
    document.querySelectorAll('.client-group').forEach(g => { g.hidden = !g.querySelector('.client:not([hidden])'); any = any || !g.hidden; });
    document.querySelector('.empty').hidden = any;
  });
</script>'''
    page('klien-kami/', 'Klien Kami',
         'Daftar BPR klien Sinergi di seluruh Indonesia, dikelompokkan per wilayah.',
         body, section='klien-kami/', js=js)


def build_news():
    def listing(path, active, posts, h1):
        chips = [('berita-acara/', 'Semua')] + [('category/%s/' % s, n) for s, n in CATEGORIES]
        nav = ''.join('<a href="/%s" class="chip"%s>%s</a>' % (
            href, ' aria-current="page"' if href == active else '', e(n)) for href, n in chips)
        body = page_hero('Berita &amp; Acara', e(h1)) + '''
<section class="section section--first">
  <div class="container">
    <nav class="chips" aria-label="Kategori berita">%s</nav>
    <div class="news">%s</div>
  </div>
</section>''' % (nav, ''.join(post_card(p) for p in posts))
        page(path, h1, 'Berita, acara, dan kabar implementasi Core Banking System dari Sinergi.', body,
             section='berita-acara/')

    listing('berita-acara/', 'berita-acara/', POSTS, 'Kabar terbaru dari Sinergi')
    for slug, name in CATEGORIES:
        listing('category/%s/' % slug, 'category/%s/' % slug,
                [p for p in POSTS if p['category'] == name], name)

    for p in POSTS:
        has_cover = not any(b[0] == 'img' and b[1] == p['image'] for b in p['blocks'])
        cover = '<img src="%s" alt="" class="article__cover">' % e(p['image']) if has_cover else ''
        related = [o for o in POSTS if o is not p][:3]
        first_text = next((b[1] for b in p['blocks'] if b[0] == 'p'), '')
        desc = (first_text[:155].rsplit(' ', 1)[0] + '…') if len(first_text) > 155 else (first_text or p['title'])
        body = '''
<article class="section section--article">
  <div class="container narrow">
    <a href="/berita-acara/" class="back">← Berita &amp; Acara</a>
    <p class="tag">{cat}</p>
    <h1>{title}</h1>
    <time datetime="{date}" class="muted">{when}</time>
    {cover}
    <div class="prose">{content}</div>
  </div>
</article>
<section class="section section--tint">
  <div class="container">
    <h2 class="subhead">Berita lainnya</h2>
    <div class="rail rail--grid cols-3">{related}</div>
  </div>
</section>'''.format(cat=e(p['category']), title=e(p['title']), date=p['date'], when=tanggal(p['date']),
                     cover=cover, content=render_blocks(p['blocks'], p['title']),
                     related=''.join(post_card(o) for o in related))
        page(p['path'] + '/', p['title'], desc, body, section='berita-acara/', image=p['image'])

    for old, new in REDIRECTS.items():
        write(old + '/', '''<!doctype html><html lang="id"><head><meta charset="utf-8"><title>Halaman dipindahkan</title>
<link rel="canonical" href="{site}/{new}/"><meta http-equiv="refresh" content="0; url=/{new}/"></head>
<body><p>Halaman ini pindah ke <a href="/{new}/">alamat baru</a>.</p></body></html>
'''.format(site=SITE, new=new), in_sitemap=False)


def build_careers():
    cards = ''.join('''<a href="/karier/{slug}/" class="card job"><h2>{title}</h2><p>{place}</p><span class="link">Lihat detail →</span></a>'''.format(
        slug=j['slug'], title=e(j['title']), place=e(j['place'])) for j in JOBS)
    body = page_hero('Karier', 'Bergabung bersama PT Sinergi Prakarsa Utama',
                     'Kembangkan karier Anda bersama tim penyedia Core Banking System untuk BPR di seluruh Indonesia.') + '''
<section class="section section--first">
  <div class="container"><div class="cards">%s</div></div>
</section>''' % cards
    page('karier/', 'Karier', 'Lowongan kerja di PT Sinergi Prakarsa Utama.', body, section='karier/')

    for j in JOBS:
        subject = 'Nama - %s' % j['title']
        body = page_hero('<a href="/karier/">Karier</a>', e(j['title']), e(j['place'])) + '''
<section class="section section--first">
  <div class="container narrow prose">
    <h2>Deskripsi pekerjaan</h2>
    <ul>{tasks}</ul>
    <h2>Kualifikasi</h2>
    <ul>{reqs}</ul>
    <div class="apply">
      <h2>Cara melamar</h2>
      <p>Kirim CV ke <a href="mailto:hrdept@sinergic.co.id">hrdept@sinergic.co.id</a> dengan subjek <strong>"Nama - Posisi"</strong>.</p>
      <a href="mailto:hrdept@sinergic.co.id?subject={subject}" class="btn btn--primary">Kirim CV</a>
    </div>
  </div>
</section>'''.format(tasks=''.join('<li>%s</li>' % e(t) for t in j['tasks']),
                     reqs=''.join('<li>%s</li>' % e(r) for r in j['reqs']),
                     subject=e(subject.replace(' ', '%20')))
        page('karier/%s/' % j['slug'], j['title'], 'Lowongan %s di PT Sinergi Prakarsa Utama, %s.' % (j['title'], j['place']),
             body, section='karier/')


def build_contact():
    body = page_hero('Kontak', 'Hubungi kami',
                     'Hubungi kami untuk solusi Core Banking System web-based yang andal dan efisien.') + '''
<section class="section section--first">
  <div class="container contact">
    <div class="contact__list">
      <a href="https://wa.me/{wa}" class="contact__item">{i_chat}<div><h2>WhatsApp</h2><p>Chat dengan tim kami</p></div></a>
      <div class="contact__item">{i_tel}<div><h2>Telepon</h2><p><a href="tel:+622180821315">021-8082-1315</a><br><a href="tel:+622180821316">021-8082-1316</a></p></div></div>
      <a href="mailto:cs@sinergic.co.id" class="contact__item">{i_mail}<div><h2>Email</h2><p>cs@sinergic.co.id</p></div></a>
      <a href="https://maps.google.com/?q=Ruko+The+Prominence+Blok+38H+No+10+Alam+Sutera+Tangerang" class="contact__item">{i_pin}<div><h2>Kantor Pusat</h2><p>Ruko The Prominence Blok 38-H No. 10, Jl. Jalur Sutera Boulevard, Alam Sutera, Kota Tangerang, Banten 15143</p><span class="link">Buka di Google Maps →</span></div></a>
      <a href="https://maps.google.com/?q=Ruko+Klampis+21+Blok+AA+No+2+Surabaya" class="contact__item">{i_pin}<div><h2>Kantor Cabang</h2><p>Ruko Klampis 21 Blok AA No. 2, Jl. Arief Rahman Hakim, Surabaya 60117</p><span class="link">Buka di Google Maps →</span></div></a>
    </div>
    <form class="form" id="form-kontak">
      <h2>Kirim pesan</h2>
      <label for="f-nama">Nama</label>
      <input id="f-nama" name="nama" autocomplete="name">
      <label for="f-email">Email <span aria-hidden="true">*</span></label>
      <input id="f-email" name="email" type="email" required autocomplete="email">
      <label for="f-telp">No. telepon <span aria-hidden="true">*</span></label>
      <input id="f-telp" name="telepon" type="tel" required autocomplete="tel" inputmode="tel">
      <label for="f-pesan">Pesan <span aria-hidden="true">*</span></label>
      <textarea id="f-pesan" name="pesan" rows="5" required></textarea>
      <button class="btn btn--primary" type="submit">Kirim</button>
      <p class="form__note">Tombol Kirim membuka aplikasi email Anda dengan pesan yang sudah terisi.</p>
    </form>
  </div>
</section>'''.format(wa=WA, i_chat=icon('chat'), i_tel=icon('tel'), i_mail=icon('mail'), i_pin=icon('pin'))
    # shortcut: the form opens the visitor's mail app (no backend), switch to a form endpoint when hosting is chosen.
    js = '''<script>
  document.getElementById('form-kontak').addEventListener('submit', ev => {
    ev.preventDefault();
    const d = new FormData(ev.target);
    const body = 'Nama: ' + d.get('nama') + '\\nEmail: ' + d.get('email') + '\\nTelepon: ' + d.get('telepon') + '\\n\\n' + d.get('pesan');
    location.href = 'mailto:cs@sinergic.co.id?subject=' + encodeURIComponent('Pesan dari website: ' + (d.get('nama') || d.get('email'))) + '&body=' + encodeURIComponent(body);
  });
</script>'''
    page('kontak/', 'Kontak', 'Alamat, telepon, email, dan WhatsApp PT Sinergi Prakarsa Utama di Tangerang dan Surabaya.',
         body, section='kontak/', js=js)


def build_404():
    body = page_hero('404', 'Halaman tidak ditemukan', 'Halaman yang Anda cari tidak ada atau sudah dipindahkan.',
                     '<div class="hero__actions"><a href="/" class="btn btn--primary">Ke Beranda</a><a href="/berita-acara/" class="btn btn--ghost">Lihat Berita</a></div>')
    page('404.html', 'Halaman tidak ditemukan', 'Halaman tidak ditemukan.', body, in_sitemap=False)


def build_sitemap():
    urls = ''.join('<url><loc>%s/%s</loc></url>' % (SITE, p) for p in SITEMAP)
    (DIST / 'sitemap.xml').write_text(
        '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">%s</urlset>\n' % urls,
        encoding='utf-8')
    (DIST / 'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: %s/sitemap.xml\n' % SITE, encoding='utf-8')


if __name__ == '__main__':
    shutil.rmtree(DIST, ignore_errors=True)
    shutil.copytree(ROOT / 'static', DIST)
    build_home()
    build_products()
    build_about()
    build_clients()
    build_news()
    build_careers()
    build_contact()
    build_404()
    build_sitemap()
    print('Built %d pages into %s' % (len(SITEMAP), DIST))
