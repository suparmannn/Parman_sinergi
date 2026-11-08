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
    'shield': '<path d="M12 22s8-3.5 8-10V5l-8-3-8 3v7c0 6.5 8 10 8 10Z"/><path d="m8.5 12 2.5 2.5 4.5-5"/>',
    'tel': '<path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2Z"/>',
}


def icon(name, cls='icon'):
    return '<svg class="%s" viewBox="0 0 24 24" aria-hidden="true">%s</svg>' % (cls, ICONS[name])


# Products. "card" is the short text for cards; "summary" is the full lead; "body" is trusted HTML.
# "short" is the name on small tiles. "photo" is an AI illustration (Gemini) for the product page header,
# not a photo of Sinergi staff or clients.
PRODUCTS = [
    dict(slug='coreplus', name='ARB+', logo='logo-arb.png', photo='ilustrasi-arb.jpg',
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
    dict(slug='aplikasi-pelaporan-tks', name='Pelaporan TKS, Manajemen Risiko & Tata Kelola', short='Pelaporan TKS',
         logo='produk-tks.png',
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
    dict(slug='m-approval', name='M-Approval', logo='produk-m-approval.png', photo='ilustrasi-m-approval.jpg',
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
    dict(slug='m-collection', name='M-Collection', logo='produk-m-collection.png', photo='ilustrasi-m-collection.jpg',
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
    dict(slug='sms-notification', name='Notifikasi SMS / WhatsApp', short='Notifikasi SMS/WA', logo='produk-sms-notification.png',
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
PRODUCT = {p['slug']: p for p in PRODUCTS}

# Device frame per product: phones for the Android apps and notifications, laptop or tablet for web products.
DEVICE = {'coreplus': 'laptop', 'aplikasi-pelaporan-tks': 'tablet', 'e-kyc': 'tablet', 'virtual-account': 'tablet',
          'm-collection': 'phone', 'm-approval': 'phone', 'sms-notification': 'phone'}


def device(p):
    """CSS device frame for a product. Put a real screenshot at static/assets/ui/<slug>.png (or .jpg) and the
    build shows it in the frame. Until then the screen shows the product logo on a placeholder."""
    kind = DEVICE[p['slug']]
    shot = next((f for f in ('%s.png' % p['slug'], '%s.jpg' % p['slug']) if (ROOT / 'static/assets/ui' / f).exists()), None)
    screen = ('<img src="/assets/ui/%s" alt="">' % shot if shot else
              '<span class="screen-ph"><img src="/assets/%s" alt=""><i></i><i></i><i></i></span>' % p['logo'])
    base = '<span class="device__base"></span>' if kind == 'laptop' else ''
    return '<span class="device device--%s" aria-hidden="true"><span class="device__screen">%s</span>%s</span>' % (kind, screen, base)


def product_cards(products, wide_first=True):
    """Colored product cards, each with its device frame. Tones cycle navy, light, blue."""
    out = []
    for n, p in enumerate(products):
        out.append('<a href="/produk-layanan/%s/" class="pc pc--%s%s"><span class="pc__visual">%s</span>'
                   '<span class="pc__body"><span class="pc__logo"><img src="/assets/%s" alt="" loading="lazy"></span>'
                   '<h3>%s</h3><span class="pc__text">%s</span><span class="pc__more">Pelajari</span></span></a>' % (
                       p['slug'], ('navy', 'sky', 'blue')[n % 3], ' pc--wide' if wide_first and n == 0 else '', device(p),
                       p['logo'], e('ARB+ Core Banking System' if p is FLAGSHIP else p['name']), e(p['card'])))
    return '<div class="cards">%s</div>' % ''.join(out)


# Client logos from the old site's "Mitra Kami" carousel, in their original colors.
CLIENT_LOGOS = [
    ('Picture1.jpg', 'BPR Bhakti Daya Ekonomi'), ('Picture2.jpg', 'BPR Bringin Dana Sejahtera'),
    ('Picture3.jpg', 'BPR LSE Manggala'), ('Picture4.png', 'BPR Hayura Artalola'),
    ('Picture6.png', 'BPR Akasia Mas'), ('Picture7.png', 'BPR Sukabumi'),
    ('Picture8.png', 'BPR Pancaputra Ganda Grup'), ('Picture10.jpg', 'BPR Karya Perdana Sejahtera'),
    ('Picture11.png', 'BPR Rifi Maligi'), ('Picture12.png', 'BPR Sulawesi Mandiri'),
    ('Picture14.png', 'BPR Sentral Investasi Prima'), ('Picture15.png', 'BPR Kepri Bintan'),
    ('Picture17.jpg', 'BPR Danamas Simpan Pinjam'), ('Picture18.png', 'BPR Karya Guna Mandiri'),
    ('Picture19.png', 'BPR Mitra Lestari'), ('Picture21.png', 'BPR Marcorindo Perdana'),
    ('Picture22.png', 'BPR Lima Padma Mandiri'), ('Picture23.png', 'BPR Lokadana Sentosa'),
    ('Picture24.jpg', 'BPR Tri Gunung Selatan'), ('Picture28.png', 'BPR Danatama Indonesia'),
    ('Picture29.png', 'BPR Citra Dumoga'), ('Picture30.png', 'BPR Rudo Indobank'),
    ('Picture31.png', 'BPR klien Sinergi'), ('Picture32.jpg', 'BAS Bank'),
    ('Picture33.png', 'BPR Batanghari'), ('Picture35.png', 'BPR Harapan Bunda Batam'),
    ('Picture36.png', 'BPR Dana Selaras Sentosa'), ('Picture38.png', 'BPR Dana Nagoya'),
    ('Picture39.png', 'BPR Primadana Abadi'), ('Picture40.png', 'BPR Pancur Banua Khatulistiwa'),
    ('Picture41.png', 'BPR Lebak Sejahtera'), ('Picture42.png', 'BPR Artha Prima Persada'),
    ('Picture43.png', 'BPR Dana Utama'), ('Picture44.png', 'BPR Bina Dana Swadaya'),
]


def logo_marquee():
    """Client logos scroll in a loop. The second copy only closes the loop, so screen readers skip it."""
    first = ''.join('<li><img src="/assets/klien/%s" alt="%s"></li>' % (f, e(a)) for f, a in CLIENT_LOGOS)
    copy = ''.join('<li><img src="/assets/klien/%s" alt=""></li>' % f for f, _ in CLIENT_LOGOS)
    return ('<div class="marquee"><ul class="marquee__track">%s</ul>'
            '<ul class="marquee__track" aria-hidden="true">%s</ul></div>' % (first, copy))


def story(p, big=False):
    return ('<a href="/%s/" class="story%s"><img src="%s" alt="" loading="lazy"><span class="story__body">'
            '<span class="tag">%s</span><h3>%s</h3><time datetime="%s">%s</time></span></a>') % (
        p['path'], ' story--big' if big else '', e(p['image']), e(p['category']), e(p['title']), p['date'],
        tanggal(p['date']))

# Mission text is verbatim from the company. Only the short titles are new.
MISSIONS = [
    ('Selalu berkembang', 'Terus berkembang untuk memenuhi seluruh kebutuhan client.'),
    ('Dukungan optimal, biaya ekonomis', 'Memberikan dukungan Core Banking System yang optimal dengan biaya yang ekonomis.'),
    ('Tumbuh bersama', 'Menjalin Sinergi untuk kemajuan bersama.'),
]
VISION = 'Menjadi Penyedia Solusi Core Banking System yang handal dan terpercaya.'

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


SITE_JS = '''<script>
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
  // Scroll reveal: blocks rise in the first time they enter the screen. Keep this list in sync with styles.css.
  const reveal = '.tile, .pc, .story, .doc, .news__item, .sec__head, .page-hero__inner, .contact__item, .missions li';
  const io = new IntersectionObserver(list => list.forEach(en => {
    if (!en.isIntersecting) return;
    en.target.classList.add('in');
    io.unobserve(en.target);
  }), { rootMargin: '0px 0px -8% 0px' });
  document.querySelectorAll(reveal).forEach(el => {
    const sibs = [...el.parentElement.children].filter(c => c.matches(reveal));
    el.style.setProperty('--i', Math.min(sibs.indexOf(el), 6));
    io.observe(el);
  });
</script>'''

FOOTER = '''
<footer class="footer">
  <div class="container">
    <div class="footer__tile">
      <div class="footer__grid">
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
            <a href="https://wa.me/%s" class="btn btn--light btn--sm">Chat WhatsApp</a>
            <a href="/kontak/" class="btn btn--outline-light btn--sm">Kirim Pesan</a>
          </div>
        </div>
      </div>
      <p class="footer__copy">© 2026 PT Sinergi Prakarsa Utama</p>
    </div>
  </div>
</footer>''' % (''.join('<li><a href="/produk-layanan/%s/">%s</a></li>' % (p['slug'], e(p.get('short', p['name'])))
                        for p in PRODUCTS), WA)

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
  <meta name="theme-color" content="#003d6f">
  <link rel="icon" type="image/png" href="/assets/favicon.png">
  <link rel="apple-touch-icon" href="/assets/favicon.png">
  <script>document.documentElement.classList.add('js');</script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/styles.css">
</head>
<body>
  <a class="skip" href="#konten">Lewati ke konten</a>
  <header class="header">
    <div class="container header__bar">
      <a href="/" class="header__logo"><img src="/assets/logo-white.png" alt="Sinergi" width="432" height="168"></a>
      <nav id="nav" class="nav" aria-label="Menu utama">
        {nav}
        <a href="/kontak/" class="btn btn--primary nav__cta">Hubungi Kami</a>
      </nav>
      <button class="menu-btn" type="button" aria-expanded="false" aria-controls="nav" aria-label="Buka menu"><span></span><span></span><span></span></button>
    </div>
  </header>
  <main id="konten">
{body}
  </main>
{footer}
  <a href="https://wa.me/{wa}" class="chat-float" aria-label="Chat WhatsApp dengan Sinergi">{chat_icon}<span>Chat WA</span></a>
{site_js}
{js}
</body>
</html>
'''.format(title=e(full_title), desc=e(desc), site=SITE, path=path, og_image=e(og_image), nav=nav_html(section),
           body=body, footer=FOOTER, site_js=SITE_JS, js=js, wa=WA,
           chat_icon='<svg viewBox="0 0 24 24" aria-hidden="true">%s</svg>' % ICONS['chat'])
    write(path, doc, in_sitemap)


def page_hero(crumb, h1, lead='', extra='', aside=''):
    """Light page header: breadcrumb, title, lead. crumb is trusted HTML for the trail after "Beranda".
    aside is an optional picture tile beside the text on desktop."""
    return '''
<section class="page-hero">
  <div class="container page-hero__grid%s">
    <div class="page-hero__inner">
      <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Beranda</a><span aria-hidden="true">/</span>%s</nav>
      <h1>%s</h1>
      %s%s
    </div>%s
  </div>
</section>''' % (' page-hero__grid--split' if aside else '', crumb, h1,
                 '<p class="lede">%s</p>' % lead if lead else '', extra, aside)


def stat_tiles(items, cls):
    """Number tiles: (label, number, caption). The first tile is solid blue."""
    return '<div class="%s">%s</div>' % (cls, ''.join(
        '<div class="tile tile--stat%s"><span class="tile__label">%s</span><div><div class="num">%s</div><p>%s</p></div></div>' % (
            ' tile--blue' if n == 0 else '', e(label), e(num), e(txt)) for n, (label, num, txt) in enumerate(items)))


PARTNERS = '''<ul class="partners">
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

TEAM_PHOTO = ('<img src="/assets/foto-tim-hut-17.jpg" srcset="/assets/foto-tim-hut-17-800.jpg 800w, /assets/foto-tim-hut-17.jpg 1600w" '
              'sizes="%s" alt="Keluarga besar Sinergi pada perayaan HUT ke-17" width="1600" height="1069"%s>')


def post_card(p):
    # shortcut: post images load from the old WordPress uploads, copy wp-content/uploads before the old site goes down.
    return ('<a href="/%s/" class="news__item"><img src="%s" alt="" loading="lazy"><span class="tag">%s</span>'
            '<h3>%s</h3><time datetime="%s">%s</time></a>') % (
        p['path'], e(p['image']), e(p['category']), e(p['title']), p['date'], tanggal(p['date']))


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


def build_home():
    missions = ''.join('<li><b>0%d</b><div><h3>%s</h3><p>%s</p></div></li>' % (n, e(t), e(x))
                       for n, (t, x) in enumerate(MISSIONS, 1))
    docs = ''.join('<a href="/%s/" class="doc"><img src="%s" alt="%s" loading="lazy"><span>%s</span></a>' % (
        p['path'], e(p['image']), e(p['title']), e(p['title'])) for p in POSTS[3:9])
    body = '''
<section class="hero">
  <div class="container hero__grid">
    <div class="hero__text">
      <span class="tag-pill">ARB+ Core Banking System</span>
      <h1>Core Banking System <span class="hl">terdepan</span> untuk BPR di Indonesia</h1>
      <p class="lede">Berbasis web, sesuai POJK, dan berjalan di cloud dengan data center Tier 3.</p>
      <div class="cta"><a href="/produk-layanan/" class="btn btn--light">Lihat Produk</a><a href="/kontak/" class="btn btn--outline-light">Hubungi Kami</a></div>
      <ul class="trust"><li><strong>105</strong><span>BPR klien</span></li><li><strong>17</strong><span>tahun</span></li><li><strong>8,1%%</strong><span>pangsa pasar</span></li></ul>
    </div>
    <div class="hero__art">
      <div class="arch"><img src="/assets/ilustrasi-m-collection.jpg" alt="" width="1024" height="1024" fetchpriority="high"></div>
      <div class="float"><span class="float__icon">%(shield)s</span><span><b>Diakui &amp; direkomendasikan</b>oleh OJK</span></div>
    </div>
  </div>
</section>

<section class="logos">
  <div class="container"><p class="logos__title">Dipercaya <a href="/klien-kami/">105 BPR</a> di seluruh Indonesia</p></div>
  %(marquee)s
</section>

<section class="section">
  <div class="container">
    <div class="sec__head"><div><h2>Solusi untuk setiap kebutuhan BPR</h2><p>Dari kantor sampai lapangan, semua terhubung dengan ARB+.</p></div><a href="/produk-layanan/" class="link">Semua produk</a></div>
    %(cards)s
  </div>
</section>

<section class="section section--ice vision">
  <div class="container">
    <p class="kicker">Visi kami</p>
    <p class="vision__quote">Menjadi Penyedia Solusi Core Banking System yang <span class="hl">handal dan terpercaya</span>.</p>
    <ol class="missions">%(missions)s</ol>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="sec__head"><div><h2>Kabar &amp; dokumentasi</h2><p>Kegiatan Sinergi bersama tim dan BPR klien.</p></div><a href="/berita-acara/" class="link">Semua berita</a></div>
    <div class="stories">%(feature)s<div class="stories__side">%(side)s</div></div>
    <div class="docs">%(docs)s</div>
  </div>
</section>

<section class="section section--ice section--tight">
  <div class="container">
    <p class="logos__title">Terhubung dengan</p>
    %(partners)s
  </div>
</section>

<section class="cta-band">
  <div class="container cta-band__inner">
    <h2>Butuh dukungan optimal untuk Core Banking System?</h2>
    <p>Bicara dengan tim kami tentang solusi Core Banking System web-based yang andal dan efisien.</p>
    <div class="cta"><a href="/kontak/" class="btn btn--light">Hubungi Kami</a><a href="https://wa.me/%(wa)s" class="btn btn--outline-light">Chat WhatsApp</a></div>
  </div>
</section>''' % dict(shield=icon('shield', 'ico'), marquee=logo_marquee(), cards=product_cards(PRODUCTS),
                     missions=missions, feature=story(POSTS[0], big=True),
                     side=''.join(story(p) for p in POSTS[1:3]), docs=docs, partners=PARTNERS, wa=WA)
    page('', 'Sinergi — Core Banking System untuk BPR di Indonesia',
         'PT Sinergi Prakarsa Utama menyediakan Core Banking System ARB+ berbasis web dan cloud untuk BPR. Dipakai 105 BPR di seluruh Indonesia sejak 2009.',
         body)


def build_products():
    body = page_hero('Produk &amp; Layanan', 'Solusi untuk setiap kebutuhan BPR',
                     'Satu Core Banking System dan enam produk pendukung untuk operasional BPR.') + '''
<section class="section section--first section--last">
  <div class="container">%s</div>
</section>''' % product_cards(PRODUCTS).replace('class="cards"', 'class="cards cards--all"', 1)
    page('produk-layanan/', 'Produk & Layanan',
         'Core Banking System ARB+ dan produk pendukung untuk BPR: Pelaporan TKS, e-KYC, M-Approval, Virtual Account, M-Collection, dan notifikasi SMS/WhatsApp.',
         body, section='produk-layanan/')

    for p in PRODUCTS:
        title = 'ARB+ Core Banking System' if p is FLAGSHIP else p['name']
        actions = ('<div class="cta"><a href="/kontak/" class="btn btn--light">Hubungi Kami</a>'
                   '<a href="https://wa.me/%s" class="btn btn--outline-light">Tanya via WhatsApp</a></div>' % WA)
        h1 = '<span class="page-hero__brand"><img src="/assets/%s" alt=""></span>%s' % (p['logo'], e(title))
        aside = '<div class="page-hero__visual page-hero__visual--%s">%s</div>' % (DEVICE[p['slug']], device(p))
        details = '''
<section class="section section--first">
  <div class="container"><div class="tile prose prose--wide">%s</div></div>
</section>''' % p['body'] if p['body'] else ''
        body = page_hero('<a href="/produk-layanan/">Produk &amp; Layanan</a>', h1, e(p['summary']), actions, aside) + details + '''
<section class="section section--last">
  <div class="container">
    <div class="sec__head"><h2>Produk lainnya</h2><a href="/produk-layanan/" class="link">Semua produk</a></div>
    %s
  </div>
</section>''' % product_cards([o for o in PRODUCTS if o is not p], wide_first=False)
        page('produk-layanan/%s/' % p['slug'], title, p['summary'], body, section='produk-layanan/')


def build_about():
    missions = ''.join('<li><b>0%d</b><div><h3>%s</h3><p>%s</p></div></li>' % (n, e(t), e(x))
                       for n, (t, x) in enumerate(MISSIONS, 1))
    body = page_hero('Tentang Kami', 'Kemitraan strategis untuk sukses bersama',
                     'Sinergi adalah perusahaan teknologi informasi yang menyediakan aplikasi untuk industri keuangan, terutama Core Banking System untuk BPR konvensional.') + '''
<section class="section section--first">
  <div class="container about-bento">
    <figure class="tile tile--photo">%(photo)s<figcaption>Keluarga besar Sinergi, HUT ke-17, September 2026</figcaption></figure>
    %(stats)s
  </div>
</section>

<section class="section">
  <div class="container about">
    <div class="tile prose">
      <h2>PT Sinergi Prakarsa Utama</h2>
      <p>Sinergi termasuk satu dari tiga vendor aplikasi perbankan BPR konvensional dengan pengguna terbanyak di Indonesia. Sinergi diakui dan direkomendasikan oleh OJK.</p>
      <p>Tim kami terdiri dari tenaga profesional berpengalaman di bidang teknologi informasi dan perbankan, dengan rata-rata pengalaman di atas 10 tahun. Kami memberikan solusi teknologi yang andal, efektif, dan efisien untuk semua mitra.</p>
      <h3>Legalitas</h3>
      <p>Sinergi berdiri pada 14 Agustus 2009 berdasarkan Akta Nomor 14 dari Notaris Elizabeth Arlita Suryoko, SH, di Tangerang. Pendirian disahkan oleh Keputusan Menteri Hukum dan HAM RI Nomor AHU-39511.AH.01.01 Tahun 2009, tanggal 14 Agustus 2009.</p>
    </div>
    <div class="vm-col" id="visi-misi">
      <div class="tile tile--navy">
        <span class="tile__label">Visi</span>
        <p class="vm__quote vm__quote--sm">%(vision)s</p>
      </div>
      <div class="tile">
        <span class="tile__label">Misi</span>
        <ol class="missions">%(missions)s</ol>
      </div>
    </div>
  </div>
</section>

<section class="section" id="struktur">
  <div class="container">
    <div class="tile org">
      <h2>Struktur organisasi</h2>
      <a href="/assets/struktur-organisasi.png"><img src="/assets/struktur-organisasi.png" alt="Bagan struktur organisasi PT Sinergi Prakarsa Utama" width="1920" height="1080" loading="lazy"></a>
      <p class="muted">Per Desember 2024. Ketuk gambar untuk melihat ukuran penuh.</p>
    </div>
  </div>
</section>

<section class="section section--last" id="mitra">
  <div class="container">
    <div class="tile">
      <h2 class="tile__title">Mitra &amp; integrasi</h2>
      %(partners)s
    </div>
  </div>
</section>''' % dict(photo=TEAM_PHOTO % ('(min-width: 1024px) 60vw, 100vw', ''),
                     stats=stat_tiles([('Pengalaman', '17', 'tahun, sejak 2009'),
                                       ('Klien', '105', 'BPR di seluruh Indonesia'),
                                       ('Pangsa pasar', '8,1%', 'dari 1.291 BPR')], 'stack'),
                     vision=e(VISION), missions=missions,
                     partners=PARTNERS.replace('class="partners"', 'class="partners partners--row"'))
    page('tentang-kami/', 'Tentang Kami',
         'Profil PT Sinergi Prakarsa Utama: penyedia Core Banking System untuk BPR sejak 2009. Visi, misi, dan legalitas perusahaan.',
         body, section='tentang-kami/')


def build_clients():
    groups = []
    for island, rows in BY_ISLAND.items():
        items = ''.join('<li class="client"><strong>%s</strong><span>%s</span></li>' % (e(n), e(c))
                        for n, c in sorted(rows))
        groups.append('<section class="tile client-group"><h2>%s <b>%d</b></h2><ul class="client-list">%s</ul></section>' % (
            e(island), len(rows), items))
    body = page_hero('Klien Kami', 'Pilihan utama BPR di seluruh Indonesia', 'Data klien Sinergi per Juni 2026.') + '''
<section class="section section--first section--last">
  <div class="container">
    %s
    <div class="tile"><h2 class="tile__title">Sebagian BPR klien kami</h2><ul class="wall">%s</ul></div>
    <div class="tile clients-map"><img src="/assets/peta-indonesia.png" alt="Peta sebaran klien Sinergi di Indonesia" width="1620" height="616" loading="lazy"></div>
    <div class="search">
      <label for="cari">Cari BPR atau kota</label>
      <input id="cari" type="search" placeholder="Contoh: Palembang" autocomplete="off">
    </div>
    <p class="empty" hidden>Tidak ada klien yang cocok.</p>
    <div class="client-groups">%s</div>
  </div>
</section>''' % (stat_tiles([('BPR konvensional', '1.291', 'di Indonesia per Mei 2026 (OJK)'),
                             ('Klien Sinergi', '105', 'BPR per Juni 2026'),
                             ('Pangsa pasar', '8,1%', 'dari seluruh BPR konvensional')], 'stats'),
       ''.join('<li><img src="/assets/klien/%s" alt="%s" loading="lazy"></li>' % (f, e(a)) for f, a in CLIENT_LOGOS),
       ''.join(groups))
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
<section class="section section--first section--last">
  <div class="container">
    <nav class="chips" aria-label="Kategori berita">%s</nav>
    %s
    <div class="news">%s</div>
  </div>
</section>''' % (nav, story(posts[0], big=True) if posts else '', ''.join(post_card(p) for p in posts[1:]))
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
<article class="section section--first article">
  <div class="container narrow">
    <a href="/berita-acara/" class="back">← Berita &amp; Acara</a>
    <p class="tag">{cat}</p>
    <h1>{title}</h1>
    <time datetime="{date}" class="muted">{when}</time>
    {cover}
    <div class="tile prose">{content}</div>
  </div>
</article>
<section class="section section--last">
  <div class="container">
    <div class="sec__head"><h2>Berita lainnya</h2><a href="/berita-acara/" class="link">Semua berita</a></div>
    <div class="news-grid">{related}</div>
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
    cards = ''.join('''<a href="/karier/{slug}/" class="tile job"><span class="tile__label">Lowongan</span><h2>{title}</h2><p class="muted">{place}</p><span class="link">Lihat detail</span></a>'''.format(
        slug=j['slug'], title=e(j['title']), place=e(j['place'])) for j in JOBS)
    body = page_hero('Karier', 'Bergabung bersama PT Sinergi Prakarsa Utama',
                     'Kembangkan karier Anda bersama tim penyedia Core Banking System untuk BPR di seluruh Indonesia.') + '''
<section class="section section--first section--last">
  <div class="container"><div class="jobs">%s</div></div>
</section>''' % cards
    page('karier/', 'Karier', 'Lowongan kerja di PT Sinergi Prakarsa Utama.', body, section='karier/')

    for j in JOBS:
        subject = 'Nama - %s' % j['title']
        body = page_hero('<a href="/karier/">Karier</a>', e(j['title']), e(j['place'])) + '''
<section class="section section--first section--last">
  <div class="container narrow">
    <div class="tile prose">
      <h2>Deskripsi pekerjaan</h2>
      <ul>{tasks}</ul>
      <h2>Kualifikasi</h2>
      <ul>{reqs}</ul>
    </div>
    <div class="tile tile--blue apply">
      <h2>Cara melamar</h2>
      <p>Kirim CV ke <a href="mailto:hrdept@sinergic.co.id">hrdept@sinergic.co.id</a> dengan subjek <strong>"Nama - Posisi"</strong>.</p>
      <a href="mailto:hrdept@sinergic.co.id?subject={subject}" class="btn btn--light">Kirim CV</a>
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
<section class="section section--first section--last">
  <div class="container contact">
    <div class="contact__list">
      <a href="https://wa.me/{wa}" class="contact__item">{i_chat}<div><h2>WhatsApp</h2><p>Chat dengan tim kami</p></div></a>
      <div class="contact__item">{i_tel}<div><h2>Telepon</h2><p><a href="tel:+622180821315">021-8082-1315</a><br><a href="tel:+622180821316">021-8082-1316</a></p></div></div>
      <a href="mailto:cs@sinergic.co.id" class="contact__item">{i_mail}<div><h2>Email</h2><p>cs@sinergic.co.id</p></div></a>
      <a href="https://maps.google.com/?q=Ruko+The+Prominence+Blok+38H+No+10+Alam+Sutera+Tangerang" class="contact__item">{i_pin}<div><h2>Kantor Pusat</h2><p>Ruko The Prominence Blok 38-H No. 10, Jl. Jalur Sutera Boulevard, Alam Sutera, Kota Tangerang, Banten 15143</p><span class="link">Buka di Google Maps</span></div></a>
      <a href="https://maps.google.com/?q=Ruko+Klampis+21+Blok+AA+No+2+Surabaya" class="contact__item">{i_pin}<div><h2>Kantor Cabang</h2><p>Ruko Klampis 21 Blok AA No. 2, Jl. Arief Rahman Hakim, Surabaya 60117</p><span class="link">Buka di Google Maps</span></div></a>
    </div>
    <form class="tile form" id="form-kontak">
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
                     '<div class="cta"><a href="/" class="btn btn--light">Ke Beranda</a><a href="/berita-acara/" class="btn btn--outline-light">Lihat Berita</a></div>')
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
