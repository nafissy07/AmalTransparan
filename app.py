import streamlit as st
import pandas as pd
import json
from datetime import datetime
from html import escape
from blockchain_connector import hubungkan_blockchain
from streamlit_js_eval import streamlit_js_eval

# ==========================================
# KONFIGURASI HALAMAN
# ==========================================

st.set_page_config(
    page_title="AmalTransparan",
    page_icon="🤝",
    layout="centered"
)

# ==========================================
# DESAIN CSS - AMALTRANSPARAN
# Palet: hijau hutan (identitas), mint (latar lembut),
# putih (permukaan), aksen status: amber, biru, teal, hijau.
# ==========================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

:root {
    --ink: #0F2A22;
    --brand: #0B6B4F;
    --brand-dark: #084C39;
    --forest: #06372B;
    --mint: #E6F5ED;
    --paper: #F5F8F6;
    --surface: #FFFFFF;
    --line: #E1EAE5;
    --line-strong: #C9D9D0;
    --muted: #5B7066;
    --s0: #D99A1E;
    --s1: #2F6FB5;
    --s2: #0E8A94;
    --s3: #0B6B4F;
    --r-sm: 10px;
    --r-md: 14px;
    --r-lg: 20px;
}

/* ===== DASAR ===== */
.stApp, .stApp p, .stApp label, .stApp li, .stApp h1, .stApp h2,
.stApp h3, .stApp h4, .stApp h5, .stApp h6, .stApp button,
.stApp input, .stApp textarea {
    font-family: 'Plus Jakarta Sans', 'Segoe UI', sans-serif;
}

.stApp {
    background:
        radial-gradient(900px 380px at 50% -120px, rgba(11, 107, 79, 0.10), transparent 70%),
        var(--paper) !important;
    color: var(--ink) !important;
}

[data-testid="stHeader"] { background: transparent !important; }

.block-container {
    max-width: 1040px !important;
    padding-top: 1.2rem;
    padding-bottom: 3rem;
}

h1, h2, h3, h4, h5, h6 {
    color: var(--ink) !important;
    font-weight: 800 !important;
    letter-spacing: -0.01em;
}

p, li, label,
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li {
    color: var(--ink);
}

[data-testid="stWidgetLabel"] p {
    color: var(--ink) !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
}

.stCaption, [data-testid="stCaptionContainer"] {
    color: var(--muted) !important;
}

a { color: var(--brand) !important; font-weight: 600; }

hr {
    border-color: var(--line) !important;
    margin: 1.6rem 0 !important;
}

/* ===== BAR MEREK (ATAS) ===== */
.brandbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 14px;
    flex-wrap: wrap;
    padding: 4px 2px 14px 2px;
}

.brand-left { display: flex; align-items: center; gap: 12px; }

.brand-logo {
    width: 44px;
    height: 44px;
    border-radius: 13px;
    background: linear-gradient(145deg, var(--forest), var(--brand));
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    box-shadow: 0 6px 16px rgba(6, 55, 43, 0.28);
}

.brand-name {
    font-size: 20px;
    font-weight: 800;
    color: var(--ink);
    line-height: 1.1;
}

.brand-sub {
    font-size: 12.5px;
    color: var(--muted);
    margin-top: 2px;
}

.brand-right { display: flex; gap: 8px; flex-wrap: wrap; }

.pill {
    font-size: 12px;
    font-weight: 600;
    color: var(--brand-dark);
    background: var(--mint);
    border: 1px solid #CFE8DA;
    border-radius: 999px;
    padding: 5px 11px;
}

/* ===== NAVIGASI (TAB GESER) ===== */
div[data-testid="stRadio"] div[role="radiogroup"] {
    display: flex !important;
    flex-wrap: nowrap !important;
    gap: 4px !important;
    overflow-x: auto !important;
    padding: 5px !important;
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: var(--r-md);
    scrollbar-width: none;
}

div[data-testid="stRadio"] div[role="radiogroup"]::-webkit-scrollbar { display: none; }

div[data-testid="stRadio"] div[role="radiogroup"] > label {
    flex: 0 0 auto !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    margin: 0 !important;
    padding: 8px 15px !important;
    min-height: 38px !important;
    background: transparent !important;
    border: none !important;
    border-radius: 10px !important;
    cursor: pointer;
    transition: background 0.15s ease;
}

div[data-testid="stRadio"] div[role="radiogroup"] input[type="radio"] {
    display: none !important;
}

div[data-testid="stRadio"] div[role="radiogroup"] > label > div:first-child:not([data-testid="stMarkdownContainer"]) {
    display: none !important;
}

div[data-testid="stRadio"] div[role="radiogroup"] > label p {
    color: var(--muted) !important;
    font-size: 13.5px !important;
    font-weight: 600 !important;
    margin: 0 !important;
    white-space: nowrap !important;
}

div[data-testid="stRadio"] div[role="radiogroup"] > label:hover {
    background: var(--mint) !important;
}

div[data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked) {
    background: var(--brand) !important;
}

div[data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked) p {
    color: #FFFFFF !important;
}

/* ===== JUDUL HALAMAN ===== */
.page-title {
    font-size: 26px;
    font-weight: 800;
    color: var(--ink);
    margin: 22px 0 4px 0;
    letter-spacing: -0.02em;
}

.page-desc {
    color: var(--muted);
    font-size: 14.5px;
    margin-bottom: 18px;
    max-width: 62ch;
    line-height: 1.55;
}

.block-title {
    font-size: 16px;
    font-weight: 800;
    color: var(--ink);
    margin: 26px 0 10px 0;
}

/* ===== HERO BERANDA ===== */
.hero {
    background:
        radial-gradient(circle at 92% 8%, rgba(110, 231, 183, 0.22), transparent 40%),
        linear-gradient(135deg, var(--forest) 0%, #0A5A43 100%);
    border-radius: 24px;
    padding: 34px 34px 28px 34px;
    margin: 8px 0 20px 0;
    box-shadow: 0 18px 40px rgba(6, 55, 43, 0.25);
}

.hero-title {
    color: #FFFFFF;
    font-size: 31px;
    font-weight: 800;
    line-height: 1.2;
    letter-spacing: -0.02em;
    max-width: 20ch;
}

.hero-text {
    color: rgba(236, 253, 245, 0.85);
    font-size: 14.5px;
    line-height: 1.65;
    margin-top: 12px;
    max-width: 56ch;
}

.hero-stats {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 12px;
    margin-top: 26px;
}

.hero-stat {
    background: rgba(255, 255, 255, 0.09);
    border: 1px solid rgba(255, 255, 255, 0.16);
    border-radius: var(--r-md);
    padding: 14px 16px;
}

.hero-stat b {
    display: block;
    color: #FFFFFF;
    font-size: 21px;
    font-weight: 800;
}

.hero-stat span {
    color: rgba(236, 253, 245, 0.75);
    font-size: 12.5px;
}

/* ===== ALUR DONASI ===== */
.flow {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 12px;
}

.flow-card {
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: var(--r-md);
    padding: 16px;
}

.flow-no {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 13px;
    font-weight: 800;
    color: #FFFFFF;
    margin-bottom: 10px;
}

.flow-no.s0 { background: var(--s0); }
.flow-no.s1 { background: var(--s1); }
.flow-no.s2 { background: var(--s2); }
.flow-no.s3 { background: var(--s3); }

.flow-name { font-weight: 800; font-size: 14.5px; color: var(--ink); }
.flow-who { font-size: 12px; font-weight: 600; color: var(--brand); margin: 2px 0 6px 0; }
.flow-desc { font-size: 12.5px; color: var(--muted); line-height: 1.5; }

/* ===== CHIP STATUS ===== */
.chip {
    display: inline-block;
    font-size: 11.5px;
    font-weight: 700;
    border-radius: 999px;
    padding: 3px 10px;
    white-space: nowrap;
}

.chip.c0, .chip.wait { color: #8A5A00; background: #FDF1D6; }
.chip.c1 { color: #1F4F86; background: #E3EDF8; }
.chip.c2, .chip.run { color: #0A646C; background: #DDF3F4; }
.chip.c3, .chip.done { color: #084C39; background: #DDF3E7; }

/* ===== BAR TAHAPAN (STACKED) ===== */
.stagebar {
    display: flex;
    height: 9px;
    border-radius: 999px;
    overflow: hidden;
    background: #E8EFEB;
    margin: 12px 0 8px 0;
}

.seg.s0 { background: var(--s0); }
.seg.s1 { background: var(--s1); }
.seg.s2 { background: var(--s2); }
.seg.s3 { background: var(--s3); }

.legend { display: flex; flex-wrap: wrap; gap: 4px 14px; }

.lg { font-size: 12px; color: var(--muted); font-weight: 600; }

.dot {
    display: inline-block;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    margin-right: 5px;
}

.dot.s0 { background: var(--s0); }
.dot.s1 { background: var(--s1); }
.dot.s2 { background: var(--s2); }
.dot.s3 { background: var(--s3); }

/* ===== KARTU KAMPANYE ===== */
.camp-head {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 10px;
}

.camp-title {
    font-size: 16px;
    font-weight: 800;
    color: var(--ink);
    overflow-wrap: anywhere;
}

.camp-amount {
    font-size: 24px;
    font-weight: 800;
    color: var(--brand-dark);
    margin-top: 10px;
    letter-spacing: -0.02em;
}

.camp-sub { font-size: 12.5px; color: var(--muted); margin-top: 2px; }

.camp-foot {
    display: flex;
    justify-content: space-between;
    gap: 10px;
    font-size: 12.5px;
    color: var(--muted);
    margin-top: 10px;
    padding-top: 10px;
    border-top: 1px dashed var(--line-strong);
}

.camp-foot b { color: var(--ink); }

/* ===== TAHAPAN DETAIL KAMPANYE ===== */
.pipe {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 10px;
    margin: 6px 0 4px 0;
}

.pipe-card {
    background: var(--surface);
    border: 1px solid var(--line);
    border-top: 4px solid var(--line-strong);
    border-radius: var(--r-md);
    padding: 12px 14px;
}

.pipe-card.s0 { border-top-color: var(--s0); }
.pipe-card.s1 { border-top-color: var(--s1); }
.pipe-card.s2 { border-top-color: var(--s2); }
.pipe-card.s3 { border-top-color: var(--s3); }

.pipe-name { font-size: 12px; font-weight: 700; color: var(--muted); }
.pipe-count { font-size: 22px; font-weight: 800; color: var(--ink); margin-top: 2px; }
.pipe-nom { font-size: 12px; color: var(--muted); }

/* ===== FEED AKTIVITAS ===== */
.feed-item {
    display: flex;
    gap: 12px;
    padding: 12px 0;
    border-bottom: 1px solid var(--line);
}

.feed-item:last-child { border-bottom: none; }

.feed-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
    margin-top: 6px;
    flex-shrink: 0;
    background: var(--line-strong);
}

.feed-dot.s0 { background: var(--s0); }
.feed-dot.s1 { background: var(--s1); }
.feed-dot.s2 { background: var(--s2); }
.feed-dot.s3 { background: var(--s3); }

.feed-body { font-size: 14px; color: var(--ink); line-height: 1.5; }
.feed-meta { font-size: 12px; color: var(--muted); margin-top: 3px; }

/* ===== BAR STATUS WALLET ===== */
.wallet-bar {
    display: flex;
    align-items: center;
    gap: 10px;
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: var(--r-md);
    padding: 11px 14px;
    font-size: 13px;
    color: var(--ink);
    min-height: 44px;
    margin-top: 12px;
}

.wdot {
    width: 9px;
    height: 9px;
    border-radius: 50%;
    background: #B7C7BE;
    flex-shrink: 0;
}

.wdot.on { background: #16A34A; box-shadow: 0 0 0 4px rgba(22, 163, 74, 0.18); }
.wdot.warn { background: #D9A400; }

/* ===== KARTU METRIK ===== */
[data-testid="stMetric"] {
    background: var(--surface);
    padding: 16px 18px;
    border-radius: var(--r-md);
    border: 1px solid var(--line);
}

[data-testid="stMetricLabel"], [data-testid="stMetricLabel"] * {
    color: var(--muted) !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
}

[data-testid="stMetricValue"], [data-testid="stMetricValue"] * {
    color: var(--ink) !important;
    font-weight: 800 !important;
}

/* ===== KARTU / CONTAINER BERBORDER ===== */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: var(--surface);
    border: 1px solid var(--line) !important;
    border-radius: var(--r-lg) !important;
    box-shadow: 0 1px 2px rgba(15, 42, 34, 0.04);
}

[data-testid="stForm"] { border: none !important; padding: 0 !important; }

[data-testid="stVegaLiteChart"] {
    background: var(--surface);
    padding: 16px;
    border-radius: var(--r-md);
    border: 1px solid var(--line);
}

[data-testid="stAlert"] { border-radius: var(--r-md); }

/* ===== FORM INPUT ===== */
.stTextInput input, .stNumberInput input, .stTextArea textarea, .stDateInput input {
    background: #FFFFFF !important;
    color: var(--ink) !important;
    border: 1px solid var(--line-strong) !important;
    border-radius: var(--r-sm) !important;
}

.stTextInput input:focus, .stNumberInput input:focus, .stTextArea textarea:focus {
    border-color: var(--brand) !important;
    box-shadow: 0 0 0 3px rgba(11, 107, 79, 0.18) !important;
}

.stTextInput input::placeholder, .stTextArea textarea::placeholder {
    color: #84998E !important;
    opacity: 1 !important;
}

[data-baseweb="select"] > div {
    background: #FFFFFF !important;
    border-color: var(--line-strong) !important;
    border-radius: var(--r-sm) !important;
}

[data-baseweb="select"] * { color: var(--ink) !important; }

/* ===== TOMBOL ===== */
.stButton > button, .stDownloadButton > button {
    background: #FFFFFF !important;
    color: var(--brand-dark) !important;
    border: 1px solid var(--line-strong) !important;
    border-radius: var(--r-sm) !important;
    padding: 8px 18px !important;
    font-weight: 700 !important;
    box-shadow: none !important;
    transition: all 0.15s ease;
}

.stButton > button:hover, .stDownloadButton > button:hover {
    border-color: var(--brand) !important;
    background: var(--mint) !important;
}

.stFormSubmitButton > button,
.stButton > button[kind="primary"],
.stButton > button[data-testid="stBaseButton-primary"] {
    background: var(--brand) !important;
    color: #FFFFFF !important;
    border: 1px solid var(--brand) !important;
    border-radius: var(--r-sm) !important;
    padding: 10px 20px !important;
    font-weight: 700 !important;
    box-shadow: 0 6px 14px rgba(11, 107, 79, 0.22) !important;
}

.stFormSubmitButton > button:hover,
.stButton > button[kind="primary"]:hover,
.stButton > button[data-testid="stBaseButton-primary"]:hover {
    background: var(--brand-dark) !important;
    border-color: var(--brand-dark) !important;
}

.stButton > button *, .stDownloadButton > button *, .stFormSubmitButton > button * {
    color: inherit !important;
    -webkit-text-fill-color: inherit !important;
}

.stButton > button:disabled, .stFormSubmitButton > button:disabled {
    background: #B9C9BF !important;
    border-color: #B9C9BF !important;
    box-shadow: none !important;
    color: #FFFFFF !important;
}

/* ===== TAB (DETAIL KAMPANYE) ===== */
[data-baseweb="tab-list"] { gap: 6px; border-bottom: 1px solid var(--line); }

[data-baseweb="tab"] {
    font-weight: 700 !important;
    color: var(--muted) !important;
    padding: 8px 14px !important;
}

[data-baseweb="tab"][aria-selected="true"] { color: var(--brand) !important; }
[data-baseweb="tab-highlight"] { background-color: var(--brand) !important; }

/* ===== TABEL ===== */
[data-testid="stDataFrame"], [data-testid="stTable"] {
    background: var(--surface);
    border: 1px solid var(--line);
    border-radius: var(--r-md);
    overflow: hidden;
}

/* ===== SIDEBAR ===== */
[data-testid="stSidebar"] { background-color: #E7F2EC; }

/* ===== ALAMAT WALLET / KODE ===== */
[data-testid="stCode"], .stCode {
    background: #EEF6F1 !important;
    border: 1px solid #D3E5DB !important;
    border-radius: var(--r-sm) !important;
    overflow-wrap: anywhere !important;
}

[data-testid="stCode"] code, [data-testid="stCode"] pre, .stCode code, .stCode pre {
    color: var(--brand-dark) !important;
    -webkit-text-fill-color: var(--brand-dark) !important;
    background: #EEF6F1 !important;
    white-space: pre-wrap !important;
    overflow-wrap: anywhere !important;
    word-break: break-word !important;
}

/* ===== PROGRESS ===== */
[data-testid="stProgress"] div[role="progressbar"] > div {
    background-color: var(--brand) !important;
}

/* ===== STEPPER DETAIL DONASI ===== */
.stepper { display: flex; margin: 10px 0 20px 0; }

.step {
    flex: 1;
    text-align: center;
    position: relative;
    font-size: 12px;
    font-weight: 700;
    color: #7A8F84;
}

.step::before {
    content: "";
    position: absolute;
    top: 17px;
    left: -50%;
    width: 100%;
    height: 3px;
    background: #DCE8E1;
    z-index: 0;
}

.step:first-child::before { display: none; }

.step .bulat {
    position: relative;
    z-index: 1;
    width: 36px;
    height: 36px;
    margin: 0 auto 6px auto;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    background: #E6EFEA;
    color: #7A8F84;
    font-weight: 800;
}

.step.done { color: var(--ink); }
.step.done::before { background: var(--brand); }
.step.done .bulat { background: var(--brand); color: #FFFFFF; }
.step.now .bulat { box-shadow: 0 0 0 5px rgba(11, 107, 79, 0.18); }

/* ===== FOOTER ===== */
.footer {
    color: var(--muted);
    text-align: center;
    padding: 18px;
    line-height: 1.7;
    font-size: 13px;
}

.footer b { color: var(--ink); }

/* ===== PONSEL ===== */
@media (max-width: 760px) {
    .hero { padding: 24px 20px; }
    .hero-title { font-size: 24px; }
    .hero-stats { grid-template-columns: 1fr; }
    .flow, .pipe { grid-template-columns: repeat(2, minmax(0, 1fr)); }
    .page-title { font-size: 22px; }
}
</style>
""", unsafe_allow_html=True)


# ==========================================
# FUNGSI BANTU TAMPILAN
# ==========================================

NAMA_STATUS = {
    0: "Menunggu diproses",
    1: "Dikelola",
    2: "Disalurkan",
    3: "Terverifikasi"
}


def h(teks):
    """Render HTML satu baris agar tidak dibaca sebagai blok kode markdown."""
    st.markdown(
        "".join(baris.strip() for baris in teks.strip().splitlines()),
        unsafe_allow_html=True
    )


def judul(teks, deskripsi=""):
    h(
        f'<div class="page-title">{teks}</div>'
        + (f'<div class="page-desc">{deskripsi}</div>' if deskripsi else "")
    )


def judul_blok(teks):
    h(f'<div class="block-title">{teks}</div>')


def rupiah(n):
    return "Rp " + f"{int(n):,}".replace(",", ".")


def waktu_fmt(ts):
    ts = int(ts)
    return (
        datetime.fromtimestamp(ts).strftime("%d %b %Y, %H:%M")
        if ts > 0 else "-"
    )


def pendek(teks, awal=6, akhir=4):
    teks = str(teks)
    return teks if len(teks) <= awal + akhir + 1 else teks[:awal] + "…" + teks[-akhir:]


def chip_status(kode):
    kode = int(kode)
    return f'<span class="chip c{kode}">{NAMA_STATUS.get(kode, "-")}</span>'


def bar_tahapan(hitung):
    """Bar bertumpuk: porsi donasi per tahap + legenda."""
    total = sum(hitung) or 1
    segmen = "".join(
        f'<span class="seg s{i}" style="width:{c / total * 100:.1f}%"></span>'
        for i, c in enumerate(hitung) if c
    )
    legenda = "".join(
        f'<span class="lg"><i class="dot s{i}"></i>{c} {NAMA_STATUS[i].lower()}</span>'
        for i, c in enumerate(hitung) if c
    )
    return (
        f'<div class="stagebar">{segmen}</div>'
        f'<div class="legend">{legenda}</div>'
    )


# ----- Callback navigasi kampanye -----

M_BERANDA = "Beranda"
M_KAMPANYE = "Kampanye"
M_DONASI = "Donasi"
M_KELOLA = "Kelola"
M_SALURKAN = "Salurkan"
M_VERIFIKASI = "Verifikasi"
M_PENGAWAS = "Pengawas"
M_RIWAYAT = "Riwayat"
M_DETAIL = "Detail Donasi"
M_WALLET = "Wallet"
M_INFO = "Info"


def buka_kampanye(nama):
    st.session_state.kampanye_aktif = nama


def tutup_kampanye():
    st.session_state.kampanye_aktif = None


def donasi_ke_kampanye(nama):
    st.session_state.prefill_kampanye = nama
    st.session_state.menu_fitur = M_DONASI


if "kampanye_aktif" not in st.session_state:
    st.session_state.kampanye_aktif = None


# ==========================================
# BAR MEREK + NAVIGASI
# ==========================================

h("""
<div class="brandbar">
<div class="brand-left">
<div class="brand-logo">🤝</div>
<div>
<div class="brand-name">AmalTransparan</div>
<div class="brand-sub">Transparansi donasi, membangun kepercayaan</div>
</div>
</div>
<div class="brand-right">
<span class="pill">Hardhat Local</span>
<span class="pill">Smart Contract</span>
<span class="pill">NFT Bukti Donasi</span>
</div>
</div>
""")

menu_pilihan = st.radio(
    "Menu Fitur",
    [
        M_BERANDA,
        M_KAMPANYE,
        M_DONASI,
        M_KELOLA,
        M_SALURKAN,
        M_VERIFIKASI,
        M_PENGAWAS,
        M_RIWAYAT,
        M_DETAIL,
        M_WALLET,
        M_INFO,
    ],
    horizontal=True,
    label_visibility="collapsed",
    key="menu_fitur"
)


# ==========================================
# INTEGRASI METAMASK
# ==========================================
# Koneksi wallet selalu diproses di semua halaman (tanpa tampilan),
# tetapi tampilannya hanya muncul di halaman yang memerlukannya:
# - Halaman transaksi  : bar ringkas
# - Halaman Wallet     : kartu lengkap (alamat, saldo, jaringan)
# - Halaman baca saja  : tidak ditampilkan

MENU_TRANSAKSI = (M_DONASI, M_KELOLA, M_SALURKAN, M_VERIFIKASI, M_PENGAWAS)

wallet_penuh = menu_pilihan == M_WALLET
wallet_ringkas = menu_pilihan in MENU_TRANSAKSI

if "wallet_request_id" not in st.session_state:
    st.session_state.wallet_request_id = 0

if "wallet_data" not in st.session_state:
    st.session_state.wallet_data = None

wallet_sekarang = st.session_state.wallet_data
sudah_terhubung = bool(wallet_sekarang) and "account" in wallet_sekarang
label_tombol_wallet = (
    "🔄 Perbarui Wallet" if sudah_terhubung else "🦊 Hubungkan MetaMask"
)

klik_wallet = False

if wallet_penuh:

    judul(
        "Wallet",
        "Hubungkan wallet untuk melihat alamat akun, saldo ETH, dan peran akun."
    )

    klik_wallet = st.button(
        label_tombol_wallet,
        type="primary",
        key="tombol_wallet_penuh"
    )

elif wallet_ringkas:

    # Halaman transaksi hanya menampilkan status wallet.
    # Tombol koneksi hanya tersedia di halaman Wallet.
    kolom_status_wallet = st.container()

if klik_wallet:
    st.session_state.wallet_request_id += 1

if st.session_state.wallet_request_id > 0:

    request_id = st.session_state.wallet_request_id

    javascript = f"""
    (async () => {{
        const provider =
            window.parent.ethereum || window.ethereum;

        if (!provider) {{
            return JSON.stringify({{
                error: "MetaMask tidak ditemukan. Buka aplikasi melalui Chrome."
            }});
        }}

        try {{
            const accounts = await provider.request({{
                method: "eth_requestAccounts"
            }});

            if (!accounts || accounts.length === 0) {{
                return JSON.stringify({{
                    error: "Belum ada akun MetaMask yang terhubung."
                }});
            }}

            const account = accounts[0];

            const chainId = await provider.request({{
                method: "eth_chainId"
            }});

            const balanceHex = await provider.request({{
                method: "eth_getBalance",
                params: [account, "latest"]
            }});

            const balanceWei = BigInt(balanceHex);
            const balanceEth =
                Number(balanceWei) / 1000000000000000000;

            return JSON.stringify({{
                account: account,
                chainId: parseInt(chainId, 16),
                balanceEth: balanceEth.toFixed(6)
            }});

        }} catch (error) {{
            return JSON.stringify({{
                error: error.message
            }});
        }}
    }})()
    // request_id: {request_id}
    """

else:
    javascript = "null"

hasil_wallet = streamlit_js_eval(
    js_expressions=javascript,
    want_output=True,
    key="AMALTRANSPARAN_METAMASK"
)

if hasil_wallet and hasil_wallet != "null":

    try:
        if isinstance(hasil_wallet, str):
            data_wallet = json.loads(hasil_wallet)
        else:
            data_wallet = hasil_wallet

        if isinstance(data_wallet, dict):
            st.session_state.wallet_data = data_wallet

    except Exception:
        st.warning("Hasil koneksi MetaMask belum dapat dibaca.")

wallet = st.session_state.wallet_data

# ----- Tampilan ringkas (halaman transaksi) -----
if wallet_ringkas:

    with kolom_status_wallet:

        if wallet and "account" in wallet:

            alamat_pendek = wallet["account"][:6] + "…" + wallet["account"][-4:]

            if wallet.get("chainId") == 31337:
                h(
                    '<div class="wallet-bar"><span class="wdot on"></span>'
                    f'<b>{alamat_pendek}</b>'
                    f'<span>{float(wallet["balanceEth"]):.4f} ETH</span></div>'
                )
            else:
                h(
                    '<div class="wallet-bar"><span class="wdot warn"></span>'
                    '<span>Pilih jaringan Hardhat Local di MetaMask</span></div>'
                )

        else:
            h(
                '<div class="wallet-bar"><span class="wdot"></span>'
                '<span>Wallet belum terhubung. Buka menu Wallet untuk menghubungkan MetaMask.</span></div>'
            )

    if wallet and "error" in wallet:
        st.warning(wallet["error"])

# ----- Tampilan lengkap (halaman Wallet) -----
elif wallet_penuh:

    if wallet:

        if "error" in wallet:

            st.error("Koneksi MetaMask gagal.")
            st.warning(wallet["error"])

        else:

            st.success("MetaMask berhasil terhubung!")

            alamat_wallet = wallet["account"]
            chain_id_wallet = wallet["chainId"]
            saldo_wallet = wallet["balanceEth"]

            col_wallet1, col_wallet2 = st.columns(2)

            with col_wallet1:
                st.metric(
                    "💳 Saldo ETH Wallet",
                    f"{saldo_wallet} ETH"
                )

            with col_wallet2:
                st.metric(
                    "🌐 Chain ID Wallet",
                    chain_id_wallet
                )

            st.write("**Alamat Wallet:**")
            st.code(alamat_wallet)

            if chain_id_wallet == 31337:
                st.success("Jaringan sesuai: Hardhat Local.")
            else:
                st.warning(
                    "Pilih jaringan Hardhat Local pada MetaMask."
                )

    else:
        st.info(
            "Belum ada wallet yang terhubung. "
            "Klik tombol Hubungkan MetaMask untuk memulai."
        )


# ==========================================
# KONEKSI SMART CONTRACT
# ==========================================

@st.cache_resource
def koneksi_kontrak():
    return hubungkan_blockchain()


try:

    w3, kontrak = koneksi_kontrak()

    if menu_pilihan == M_INFO:
        st.success("Blockchain Hardhat berhasil terhubung!")

    alamat_pengelola = kontrak.functions.pengelola().call()

    # ==========================================
    # MEMBACA DATA DONASI DARI SMART CONTRACT
    # ==========================================

    seluruh_id = []
    log_donasi = []

    event_donasi = kontrak.events.DonationCreated()

    try:
        log_donasi = event_donasi.get_logs(
            from_block=0,
            to_block="latest"
        )

        seluruh_id = sorted({
            int(log["args"]["donationId"])
            for log in log_donasi
        })

    except Exception as error:
        st.warning(
            "Riwayat event belum dapat dibaca: " + str(error)
        )

    daftar_donasi = []

    # Peta ID donasi -> log event (untuk nomor blok dan hash transaksi)
    info_log = {}
    try:
        for lg in log_donasi:
            info_log[int(lg["args"]["donationId"])] = lg
    except Exception:
        pass

    for donation_id in seluruh_id:

        try:

            data = kontrak.functions.getDonation(
                donation_id
            ).call()

            daftar_donasi.append({
                "ID": data[0],
                "Kampanye": data[1],
                "Donatur": data[2],
                "Alamat Donatur": data[3],
                "Jumlah": int(data[4]),
                "Tujuan": data[5],
                "Status": data[6],
                "Timestamp": int(data[7]),
                "Block": (
                    int(info_log[int(data[0])]["blockNumber"])
                    if int(data[0]) in info_log else 0
                ),
                "Tx Hash": (
                    w3.to_hex(info_log[int(data[0])]["transactionHash"])
                    if int(data[0]) in info_log else "-"
                )
            })

        except Exception as error:
            st.warning(
                f"Donasi ID {donation_id} gagal dibaca: {error}"
            )

    data_donasi = pd.DataFrame(daftar_donasi)


    # ==========================================
    # MENU: BERANDA (RINGKASAN + STATISTIK)
    # ==========================================

    if menu_pilihan == M_BERANDA:

        if not data_donasi.empty:

            total_donasi = int(data_donasi["Jumlah"].sum())

            jumlah_kampanye = data_donasi["Kampanye"].nunique()

            jumlah_terverifikasi = int(
                (data_donasi["Status"] == 3).sum()
            )

        else:

            total_donasi = 0
            jumlah_kampanye = 0
            jumlah_terverifikasi = 0

        h(f"""
        <div class="hero">
        <div class="hero-title">Setiap donasi tercatat. Setiap penyaluran terlihat.</div>
        <div class="hero-text">
        Catatan donasi disimpan di smart contract, sehingga siapa pun
        dapat menelusuri dari mana dana masuk, ke mana dana disalurkan,
        dan siapa yang memverifikasinya.
        </div>
        <div class="hero-stats">
        <div class="hero-stat"><b>{rupiah(total_donasi)}</b><span>Total donasi tercatat</span></div>
        <div class="hero-stat"><b>{jumlah_kampanye}</b><span>Kampanye berjalan</span></div>
        <div class="hero-stat"><b>{jumlah_terverifikasi}</b><span>Donasi terverifikasi</span></div>
        </div>
        </div>
        """)

        st.caption(
            "Nominal merupakan data yang tersimpan dalam smart contract, "
            "bukan bukti transfer uang."
        )

        judul_blok("Perjalanan satu donasi")

        h("""
        <div class="flow">
        <div class="flow-card"><div class="flow-no s0">1</div>
        <div class="flow-name">Dicatat</div><div class="flow-who">Donatur</div>
        <div class="flow-desc">Donasi tersimpan di blockchain dan NFT bukti diterbitkan.</div></div>
        <div class="flow-card"><div class="flow-no s1">2</div>
        <div class="flow-name">Dikelola</div><div class="flow-who">Pengelola</div>
        <div class="flow-desc">Pengelola menetapkan tujuan penggunaan dana.</div></div>
        <div class="flow-card"><div class="flow-no s2">3</div>
        <div class="flow-name">Disalurkan</div><div class="flow-who">Pengelola</div>
        <div class="flow-desc">Bantuan dicatat sampai ke penerima yang dituju.</div></div>
        <div class="flow-card"><div class="flow-no s3">4</div>
        <div class="flow-name">Terverifikasi</div><div class="flow-who">Pengawas</div>
        <div class="flow-desc">Pengawas independen memastikan penyaluran sesuai.</div></div>
        </div>
        """)

        if not data_donasi.empty:

            kiri, kanan = st.columns([3, 2], gap="large")

            with kiri:
                judul_blok("Dana per kampanye")

                data_grafik = (
                    data_donasi.groupby("Kampanye")["Jumlah"]
                    .sum()
                    .to_frame()
                )

                st.bar_chart(data_grafik, color="#0B6B4F")

            with kanan:
                judul_blok("Aktivitas terbaru")

                terbaru = data_donasi.sort_values("ID", ascending=False).head(5)
                isi_feed = ""

                for _, r in terbaru.iterrows():
                    isi_feed += (
                        f'<div class="feed-item"><div class="feed-dot s{int(r["Status"])}"></div>'
                        f'<div class="feed-body"><b>{escape(str(r["Donatur"]))}</b> '
                        f'mencatat {rupiah(r["Jumlah"])}'
                        f'<div class="feed-meta">{escape(str(r["Kampanye"]))} · '
                        f'{waktu_fmt(r["Timestamp"])}</div></div></div>'
                    )

                h(f'<div>{isi_feed}</div>')

        else:
            st.info(
                "Belum ada donasi yang tercatat di smart contract. "
                "Buka menu Donasi untuk mencatat donasi pertama."
            )


    # ==========================================
    # MENU: FORM DONASI - INTEGRASI SMART CONTRACT
    # ==========================================

    elif menu_pilihan == M_DONASI:

        judul(
            "Catat Donasi",
            "Donasi dicatat di blockchain dan NFT diterbitkan sebagai "
            "bukti pencatatan."
        )

        with st.container(border=True):
            with st.form("form_donasi_blockchain"):

                campaign_id = st.text_input(
                    "ID Kampanye",
                    value=st.session_state.get("prefill_kampanye", ""),
                    placeholder="Contoh: BANTUAN-001"
                )

                nama_donatur = st.text_input(
                    "Nama Donatur",
                    placeholder="Masukkan nama donatur"
                )

                nominal_donasi = st.number_input(
                    "Nominal Donasi (Rp)",
                    min_value=1000,
                    step=1000,
                    value=10000
                )

                metadata_uri = st.text_input(
                    "Metadata URI (Opsional)",
                    placeholder="https://..."
                )

                submit_donasi = st.form_submit_button(
                    "💚 Catat Donasi ke Blockchain",
                    use_container_width=True
                )

        st.info(
            "Nominal donasi dicatat sebagai data pada smart contract. "
            "Kode kontrak saat ini belum melakukan transfer ETH."
        )


        if submit_donasi:

            wallet = st.session_state.get("wallet_data")

            if not campaign_id.strip():
                st.error("ID kampanye wajib diisi.")

            elif not nama_donatur.strip():
                st.error("Nama donatur wajib diisi.")

            elif not wallet or "account" not in wallet:
                st.error("Hubungkan MetaMask terlebih dahulu.")

            elif wallet.get("chainId") != 31337:
                st.error("Pilih jaringan Hardhat Local di MetaMask.")

            else:
                try:
                    alamat_wallet = w3.to_checksum_address(
                        wallet["account"]
                    )

                    # Siapkan data transaksi dari smart contract
                    calldata = kontrak.functions.createDonation(
                        campaign_id.strip(),
                        nama_donatur.strip(),
                        int(nominal_donasi),
                        metadata_uri.strip()
                    )._encode_transaction_data()

                    # Kirim transaksi melalui MetaMask
                    javascript_transaksi = f"""
                    (async () => {{
                        const provider =
                            window.parent.ethereum || window.ethereum;

                        if (!provider) {{
                            return JSON.stringify({{
                                error: "MetaMask tidak ditemukan."
                            }});
                        }}

                        try {{
                            const accounts = await provider.request({{
                                method: "eth_requestAccounts"
                            }});

                            if (
                                accounts[0].toLowerCase() !==
                                "{alamat_wallet}".toLowerCase()
                            ) {{
                                return JSON.stringify({{
                                    error: "Akun MetaMask berubah. Hubungkan ulang wallet."
                                }});
                            }}

                            const txHash = await provider.request({{
                                method: "eth_sendTransaction",
                                params: [{{
                                    from: "{alamat_wallet}",
                                    to: "{kontrak.address}",
                                    data: "{calldata}"
                                }}]
                            }});

                            return JSON.stringify({{
                                txHash: txHash
                            }});

                        }} catch (error) {{
                            return JSON.stringify({{
                                error: error.message
                            }});
                        }}
                    }})()
                    """

                    st.info(
                        "Silakan konfirmasi transaksi pada MetaMask."
                    )

                    hasil_transaksi = streamlit_js_eval(
                        js_expressions=javascript_transaksi,
                        want_output=True,
                        key="DONASI_METAMASK_TX"
                    )

                    if hasil_transaksi and hasil_transaksi != "null":

                        if isinstance(hasil_transaksi, str):
                            hasil = json.loads(hasil_transaksi)
                        else:
                            hasil = hasil_transaksi

                        if "error" in hasil:
                            st.error(hasil["error"])

                        elif "txHash" in hasil:
                            with st.spinner(
                                "Menunggu transaksi dikonfirmasi blockchain..."
                            ):
                                receipt = w3.eth.wait_for_transaction_receipt(
                                    hasil["txHash"]
                                )

                            if receipt.status == 1:
                                st.success(
                                    "Donasi berhasil dicatat ke blockchain!"
                                )
                                st.write("**Transaction Hash:**")
                                st.code(receipt.transactionHash.hex())
                                st.write(
                                    "**Block Number:**",
                                    receipt.blockNumber
                                )
                                st.write("**Alamat Donatur:**")
                                st.code(alamat_wallet)
                                st.info(
                                    "NFT donasi berhasil dibuat oleh smart contract."
                                )
                            else:
                                st.error("Transaksi gagal.")

                except Exception as error:
                    st.error("Transaksi donasi gagal.")
                    st.code(str(error))


    # ==========================================
    # MENU: PENGELOLAAN DONASI
    # ==========================================

    elif menu_pilihan == M_KELOLA:

        judul(
            "Kelola Donasi",
            "Pengelola menentukan tujuan penggunaan dana dan mengubah "
            "status donasi menjadi dikelola."
        )

        if not data_donasi.empty:

            with st.container(border=True):
                with st.form("form_pengelolaan_donasi"):

                    pilihan_donasi = st.selectbox(
                        "Pilih ID Donasi",
                        options=data_donasi["ID"].astype(int).tolist()
                    )

                    tujuan_penggunaan = st.text_area(
                        "Tujuan Penggunaan Dana",
                        placeholder="Contoh: Pembelian sembako untuk korban bencana"
                    )

                    submit_kelola = st.form_submit_button(
                        "📝 Kelola Donasi melalui MetaMask",
                        use_container_width=True
                    )

            if submit_kelola:

                wallet_kelola = st.session_state.get("wallet_data")

                if not tujuan_penggunaan.strip():
                    st.error("Tujuan penggunaan dana wajib diisi.")

                elif not wallet_kelola or "account" not in wallet_kelola:
                    st.error("Hubungkan MetaMask terlebih dahulu.")

                elif wallet_kelola.get("chainId") != 31337:
                    st.error("Pilih jaringan Hardhat Local.")

                elif wallet_kelola["account"].lower() != alamat_pengelola.lower():
                    st.error(
                        "Akun MetaMask bukan akun pengelola. "
                        "Gunakan akun yang melakukan deploy smart contract."
                    )

                else:
                    try:
                        alamat_wallet_kelola = w3.to_checksum_address(
                            wallet_kelola["account"]
                        )

                        calldata_kelola = (
                            kontrak.functions.manageDonation(
                                int(pilihan_donasi),
                                tujuan_penggunaan.strip()
                            )._encode_transaction_data()
                        )

                        javascript_kelola = f"""
                        (async () => {{
                            const provider =
                                window.parent.ethereum || window.ethereum;

                            if (!provider) {{
                                return JSON.stringify({{
                                    error: "MetaMask tidak ditemukan."
                                }});
                            }}

                            try {{
                                const accounts = await provider.request({{
                                    method: "eth_requestAccounts"
                                }});

                                if (
                                    accounts[0].toLowerCase() !==
                                    "{alamat_wallet_kelola}".toLowerCase()
                                ) {{
                                    return JSON.stringify({{
                                        error: "Akun MetaMask tidak sesuai."
                                    }});
                                }}

                                const txHash = await provider.request({{
                                    method: "eth_sendTransaction",
                                    params: [{{
                                        from: "{alamat_wallet_kelola}",
                                        to: "{kontrak.address}",
                                        data: "{calldata_kelola}"
                                    }}]
                                }});

                                return JSON.stringify({{
                                    txHash: txHash
                                }});

                            }} catch (error) {{
                                return JSON.stringify({{
                                    error: error.message
                                }});
                            }}
                        }})()
                        """

                        st.info(
                            "Silakan konfirmasi pengelolaan donasi di MetaMask."
                        )

                        hasil_kelola = streamlit_js_eval(
                            js_expressions=javascript_kelola,
                            want_output=True,
                            key="PENGELOLAAN_DONASI_METAMASK"
                        )

                        if hasil_kelola and hasil_kelola != "null":

                            if isinstance(hasil_kelola, str):
                                hasil = json.loads(hasil_kelola)
                            else:
                                hasil = hasil_kelola

                            if "error" in hasil:
                                st.error(hasil["error"])

                            elif "txHash" in hasil:

                                with st.spinner(
                                    "Menunggu transaksi blockchain..."
                                ):
                                    receipt_kelola = (
                                        w3.eth.wait_for_transaction_receipt(
                                            hasil["txHash"]
                                        )
                                    )

                                if receipt_kelola.status == 1:
                                    st.success(
                                        "Donasi berhasil dikelola!"
                                    )
                                    st.write("**Transaction Hash:**")
                                    st.code(
                                        receipt_kelola.transactionHash.hex()
                                    )
                                    st.rerun()

                                else:
                                    st.error("Transaksi pengelolaan gagal.")

                    except Exception as error:
                        st.error("Gagal mengelola donasi.")
                        st.code(str(error))

        else:
            st.info("Belum ada donasi yang dapat dikelola.")


    # ==========================================
    # MENU: FORM PENYALURAN DONASI
    # ==========================================

    elif menu_pilihan == M_SALURKAN:

        judul(
            "Salurkan Donasi",
            "Catat penyaluran bantuan kepada penerima melalui blockchain."
        )

        kampanye_tersedia = []

        if not data_donasi.empty:
            donasi_dikelola = data_donasi[
                data_donasi["Status"] == 1
            ]

            for campaign in donasi_dikelola["Kampanye"].unique():
                saldo = kontrak.functions.campaignBalance(
                    campaign
                ).call()

                if saldo > 0:
                    kampanye_tersedia.append(campaign)

        if kampanye_tersedia:

            with st.container(border=True):
                with st.form("form_penyaluran_donasi"):

                    kampanye_pilih = st.selectbox(
                        "Pilih Kampanye",
                        options=kampanye_tersedia
                    )

                    saldo_kampanye = kontrak.functions.campaignBalance(
                        kampanye_pilih
                    ).call()

                    st.info(
                        "Saldo kampanye: Rp "
                        + f"{saldo_kampanye:,}".replace(",", ".")
                    )

                    nama_penerima = st.text_input(
                        "Nama Penerima Bantuan",
                        placeholder="Masukkan nama penerima"
                    )

                    jumlah_penyaluran = st.number_input(
                        "Jumlah Bantuan (Rp)",
                        min_value=1,
                        max_value=int(saldo_kampanye),
                        step=1000,
                        value=min(10000, int(saldo_kampanye))
                    )

                    submit_penyaluran = st.form_submit_button(
                        "📦 Salurkan Donasi melalui MetaMask",
                        use_container_width=True
                    )

            if submit_penyaluran:

                wallet_penyaluran = st.session_state.get(
                    "wallet_data"
                )

                if not nama_penerima.strip():
                    st.error("Nama penerima wajib diisi.")

                elif not wallet_penyaluran:
                    st.error("Hubungkan MetaMask terlebih dahulu.")

                elif wallet_penyaluran.get("chainId") != 31337:
                    st.error("Pilih jaringan Hardhat Local.")

                elif wallet_penyaluran.get("account", "").lower() != (
                    alamat_pengelola.lower()
                ):
                    st.error(
                        "Gunakan akun MetaMask milik pengelola."
                    )

                else:
                    try:
                        calldata_penyaluran = (
                            kontrak.functions.distributeDonation(
                                kampanye_pilih,
                                nama_penerima.strip(),
                                int(jumlah_penyaluran)
                            )._encode_transaction_data()
                        )

                        javascript_penyaluran = f"""
                        (async () => {{
                            const provider =
                                window.parent.ethereum || window.ethereum;

                            if (!provider) {{
                                return JSON.stringify({{
                                    error: "MetaMask tidak ditemukan."
                                }});
                            }}

                            try {{
                                const accounts = await provider.request({{
                                    method: "eth_requestAccounts"
                                }});

                                const txHash = await provider.request({{
                                    method: "eth_sendTransaction",
                                    params: [{{
                                        from: accounts[0],
                                        to: "{kontrak.address}",
                                        data: "{calldata_penyaluran}"
                                    }}]
                                }});

                                return JSON.stringify({{
                                    hash: txHash
                                }});

                            }} catch (error) {{
                                return JSON.stringify({{
                                    error: error.message
                                }});
                            }}
                        }})()
                        """

                        hasil_penyaluran = streamlit_js_eval(
                            js_expressions=javascript_penyaluran,
                            want_output=True,
                            key="PENYALURAN_DONASI_METAMASK"
                        )

                        if hasil_penyaluran:
                            if isinstance(hasil_penyaluran, str):
                                hasil_data = json.loads(
                                    hasil_penyaluran
                                )
                            else:
                                hasil_data = hasil_penyaluran

                            if hasil_data.get("error"):
                                st.error(hasil_data["error"])

                            elif hasil_data.get("hash"):

                                with st.spinner(
                                    "Menunggu transaksi blockchain..."
                                ):
                                    hash_transaksi = hasil_data["hash"]

                                    receipt = (
                                        w3.eth.wait_for_transaction_receipt(
                                            hash_transaksi
                                        )
                                    )

                                if receipt.status == 1:
                                    st.success(
                                        "Penyaluran donasi berhasil dicatat!"
                                    )

                                    st.write("Transaction Hash:")
                                    st.code(hash_transaksi)

                                    st.write(
                                        "Block Number:",
                                        receipt.blockNumber
                                    )

                                    st.rerun()

                    except Exception as error:
                        st.error("Penyaluran donasi gagal.")
                        st.code(str(error))

        else:
            st.info(
                "Belum ada kampanye dengan donasi berstatus "
                "Dikelola dan saldo yang tersedia."
            )


    # ==========================================
    # MENU: FORM VERIFIKASI DONASI
    # ==========================================

    elif menu_pilihan == M_VERIFIKASI:

        judul(
            "Verifikasi Donasi",
            "Pengawas memverifikasi donasi yang telah disalurkan "
            "melalui smart contract."
        )

        alamat_pengawas = kontrak.functions.pengawas().call()

        st.write("Alamat Pengawas Terdaftar:")
        st.code(alamat_pengawas)

        kampanye_verifikasi = []

        if not data_donasi.empty:
            donasi_disalurkan = data_donasi[
                data_donasi["Status"] == 2
            ]

            kampanye_verifikasi = (
                donasi_disalurkan["Kampanye"].unique().tolist()
            )

        if kampanye_verifikasi:

            with st.container(border=True):
                with st.form("form_verifikasi_donasi"):

                    pilihan_kampanye_verifikasi = st.selectbox(
                        "Pilih Kampanye untuk Diverifikasi",
                        options=kampanye_verifikasi
                    )

                    submit_verifikasi = st.form_submit_button(
                        "🔍 Verifikasi Donasi melalui MetaMask",
                        use_container_width=True
                    )

            if submit_verifikasi:

                wallet_verifikasi = st.session_state.get("wallet_data")

                if not wallet_verifikasi or "account" not in wallet_verifikasi:
                    st.error("Hubungkan MetaMask terlebih dahulu.")

                elif wallet_verifikasi.get("chainId") != 31337:
                    st.error("Pilih jaringan Hardhat Local.")

                elif wallet_verifikasi["account"].lower() != alamat_pengawas.lower():
                    st.error(
                        "Akun MetaMask bukan akun pengawas terdaftar."
                    )

                else:
                    try:
                        calldata_verifikasi = (
                            kontrak.functions.verifyDonation(
                                pilihan_kampanye_verifikasi
                            )._encode_transaction_data()
                        )

                        alamat_wallet_verifikasi = w3.to_checksum_address(
                            wallet_verifikasi["account"]
                        )

                        javascript_verifikasi = f"""
                        (async () => {{
                            const provider =
                                window.parent.ethereum || window.ethereum;

                            try {{
                                const accounts = await provider.request({{
                                    method: "eth_requestAccounts"
                                }});

                                if (
                                    accounts[0].toLowerCase() !==
                                    "{alamat_wallet_verifikasi}".toLowerCase()
                                ) {{
                                    return JSON.stringify({{
                                        error: "Akun MetaMask tidak sesuai."
                                    }});
                                }}

                                const txHash = await provider.request({{
                                    method: "eth_sendTransaction",
                                    params: [{{
                                        from: accounts[0],
                                        to: "{kontrak.address}",
                                        data: "{calldata_verifikasi}"
                                    }}]
                                }});

                                return JSON.stringify({{hash: txHash}});

                            }} catch (error) {{
                                return JSON.stringify({{
                                    error: error.message
                                }});
                            }}
                        }})()
                        """

                        st.info(
                            "Silakan konfirmasi verifikasi di MetaMask."
                        )

                        hasil_verifikasi = streamlit_js_eval(
                            js_expressions=javascript_verifikasi,
                            want_output=True,
                            key="VERIFIKASI_DONASI_METAMASK"
                        )

                        if hasil_verifikasi and hasil_verifikasi != "null":

                            if isinstance(hasil_verifikasi, str):
                                hasil_data = json.loads(hasil_verifikasi)
                            else:
                                hasil_data = hasil_verifikasi

                            if hasil_data.get("error"):
                                st.error(hasil_data["error"])

                            elif hasil_data.get("hash"):

                                with st.spinner(
                                    "Menunggu transaksi blockchain..."
                                ):
                                    receipt_verifikasi = (
                                        w3.eth.wait_for_transaction_receipt(
                                            hasil_data["hash"]
                                        )
                                    )

                                if receipt_verifikasi.status == 1:
                                    st.success(
                                        "Transaksi verifikasi berhasil dicatat!"
                                    )
                                    st.write("Transaction Hash:")
                                    st.code(hasil_data["hash"])
                                    st.rerun()

                                else:
                                    st.error("Transaksi verifikasi gagal.")

                    except Exception as error:
                        st.error("Gagal memverifikasi donasi.")
                        st.code(str(error))

        else:
            st.info(
                "Belum ada donasi berstatus Disalurkan "
                "yang dapat diverifikasi."
            )


    # ==========================================
    # MENU: PENDAFTARAN ALAMAT PENGAWAS
    # ==========================================

    elif menu_pilihan == M_PENGAWAS:

        judul(
            "Pendaftaran Pengawas",
            "Hanya pengelola yang dapat mendaftarkan alamat pengawas."
        )

        alamat_pengawas_terdaftar = kontrak.functions.pengawas().call()

        st.write("Alamat pengawas saat ini:")
        st.code(
            alamat_pengawas_terdaftar
            if alamat_pengawas_terdaftar != "0x0000000000000000000000000000000000000000"
            else "Belum ada pengawas terdaftar"
        )

        with st.container(border=True):
            with st.form("form_daftar_pengawas"):
                alamat_pengawas_baru = st.text_input(
                    "Alamat Wallet Pengawas",
                    value="0x5eaFb8348d346e70C36154D9b80fc0228273E799"
                )

                submit_pengawas = st.form_submit_button(
                    "🛡️ Daftarkan Pengawas",
                    use_container_width=True
                )

        if submit_pengawas:
            wallet_pengelola = st.session_state.get("wallet_data")

            if not wallet_pengelola or "account" not in wallet_pengelola:
                st.error("Hubungkan MetaMask terlebih dahulu.")

            elif wallet_pengelola.get("chainId") != 31337:
                st.error("Pilih jaringan Hardhat Local.")

            elif wallet_pengelola["account"].lower() != alamat_pengelola.lower():
                st.error("Gunakan akun MetaMask milik pengelola.")

            else:
                try:
                    alamat_valid = w3.to_checksum_address(
                        alamat_pengawas_baru.strip()
                    )

                    calldata_pengawas = (
                        kontrak.functions.setPengawas(
                            alamat_valid
                        )._encode_transaction_data()
                    )

                    javascript_pengawas = f"""
                    (async () => {{
                        const provider =
                            window.parent.ethereum || window.ethereum;

                        try {{
                            const accounts = await provider.request({{
                                method: "eth_requestAccounts"
                            }});

                            if (
                                accounts[0].toLowerCase() !==
                                "{alamat_pengelola}".toLowerCase()
                            ) {{
                                return JSON.stringify({{
                                    error: "Akun MetaMask bukan akun pengelola."
                                }});
                            }}

                            const txHash = await provider.request({{
                                method: "eth_sendTransaction",
                                params: [{{
                                    from: accounts[0],
                                    to: "{kontrak.address}",
                                    data: "{calldata_pengawas}"
                                }}]
                            }});

                            return JSON.stringify({{hash: txHash}});

                        }} catch (error) {{
                            return JSON.stringify({{
                                error: error.message
                            }});
                        }}
                    }})()
                    """

                    st.info("Konfirmasi pendaftaran di MetaMask.")

                    hasil_pengawas = streamlit_js_eval(
                        js_expressions=javascript_pengawas,
                        want_output=True,
                        key="PENDAFTARAN_PENGAWAS_METAMASK"
                    )

                    if hasil_pengawas and hasil_pengawas != "null":
                        if isinstance(hasil_pengawas, str):
                            hasil_data = json.loads(hasil_pengawas)
                        else:
                            hasil_data = hasil_pengawas

                        if hasil_data.get("error"):
                            st.error(hasil_data["error"])

                        elif hasil_data.get("hash"):
                            receipt = w3.eth.wait_for_transaction_receipt(
                                hasil_data["hash"]
                            )

                            if receipt.status == 1:
                                st.success("Pengawas berhasil didaftarkan!")
                                st.code(hasil_data["hash"])
                                st.rerun()
                            else:
                                st.error("Transaksi pendaftaran gagal.")

                except Exception as error:
                    st.error("Gagal mendaftarkan pengawas.")
                    st.code(str(error))


    # ==========================================
    # MENU: RIWAYAT DONASI
    # ==========================================

    elif menu_pilihan == M_RIWAYAT:

        judul(
            "Riwayat Donasi",
            "Daftar catatan donasi yang tersimpan pada blockchain."
        )

        if not data_donasi.empty:

            # Salin data asli agar filter tidak mengubah data blockchain.
            tampilan_asli = data_donasi.copy()

            kolom_cari, kolom_status = st.columns([2, 1])

            with kolom_cari:
                kata_kunci = st.text_input(
                    "Cari donasi",
                    placeholder="ID kampanye, ID donasi, nama donatur, wallet, atau tujuan",
                    key="cari_riwayat_donasi"
                )

            with kolom_status:
                pilihan_status = st.selectbox(
                    "Filter status",
                    ["Semua Status"] + list(NAMA_STATUS.values()),
                    key="filter_status_riwayat"
                )

            hasil_filter = tampilan_asli.copy()

            # Pencarian lintas kolom: ID, kampanye, donatur, wallet, tujuan.
            if kata_kunci.strip():
                kata = kata_kunci.strip().lower()
                kolom_teks = (
                    hasil_filter["ID"].astype(str).str.lower().str.contains(kata, na=False)
                    | hasil_filter["Kampanye"].astype(str).str.lower().str.contains(kata, na=False)
                    | hasil_filter["Donatur"].astype(str).str.lower().str.contains(kata, na=False)
                    | hasil_filter["Alamat Donatur"].astype(str).str.lower().str.contains(kata, na=False)
                    | hasil_filter["Tujuan"].astype(str).str.lower().str.contains(kata, na=False)
                )
                hasil_filter = hasil_filter[kolom_teks]

            if pilihan_status != "Semua Status":
                kode_status = {
                    nama: kode for kode, nama in NAMA_STATUS.items()
                }[pilihan_status]
                hasil_filter = hasil_filter[
                    hasil_filter["Status"] == kode_status
                ]

            st.caption(
                f"Menampilkan {len(hasil_filter)} dari "
                f"{len(tampilan_asli)} catatan donasi."
            )

            if not hasil_filter.empty:
                tampilan = hasil_filter.copy()

                tampilan["Status"] = tampilan["Status"].map(
                    NAMA_STATUS
                ).fillna("Tidak diketahui")

                tampilan["Jumlah"] = tampilan["Jumlah"].apply(rupiah)

                tampilan["Waktu"] = tampilan["Timestamp"].apply(waktu_fmt)

                kolom_riwayat = [
                    "ID", "Kampanye", "Donatur", "Alamat Donatur",
                    "Jumlah", "Tujuan", "Status", "Waktu"
                ]

                st.dataframe(
                    tampilan[kolom_riwayat],
                    use_container_width=True,
                    hide_index=True
                )

                st.download_button(
                    "⬇️ Unduh hasil (CSV)",
                    data=tampilan[kolom_riwayat].to_csv(index=False).encode("utf-8"),
                    file_name="riwayat_donasi.csv",
                    mime="text/csv"
                )
            else:
                st.warning(
                    "Data donasi tidak ditemukan. Coba kata kunci "
                    "atau filter status yang berbeda."
                )

        else:

            st.info(
                "Riwayat donasi masih kosong. "
                "Data akan tampil setelah catatan donasi "
                "tersimpan pada smart contract."
            )


    # ==========================================
    # MENU: KAMPANYE (DAFTAR + DETAIL TRANSPARANSI)
    # ==========================================

    elif menu_pilihan == M_KAMPANYE:

        if data_donasi.empty:

            judul(
                "Kampanye",
                "Pantau dana masuk dan progres penyaluran setiap kampanye."
            )

            st.info(
                "Belum ada kampanye. Kampanye muncul otomatis setelah "
                "donasi pertama dicatat."
            )

            st.button(
                "💚 Catat donasi pertama",
                type="primary",
                on_click=donasi_ke_kampanye,
                args=("",)
            )

        else:

            data_k = data_donasi.copy()
            data_k["ID"] = data_k["ID"].astype(int)
            data_k["Status"] = data_k["Status"].astype(int)

            # ----- Ringkasan per kampanye -----
            daftar_k = []

            for nama_k, grup_k in data_k.groupby("Kampanye"):

                try:
                    saldo_k = int(
                        kontrak.functions.campaignBalance(nama_k).call()
                    )
                except Exception:
                    saldo_k = None

                hitung_k = [
                    int((grup_k["Status"] == s).sum()) for s in range(4)
                ]
                jumlah_k = len(grup_k)
                tersalur_k = int((grup_k["Status"] >= 2).sum())

                if hitung_k[3] == jumlah_k:
                    tahap_k = "done"
                elif tersalur_k > 0:
                    tahap_k = "run"
                else:
                    tahap_k = "wait"

                daftar_k.append({
                    "Kampanye": nama_k,
                    "Dana Masuk": int(grup_k["Jumlah"].sum()),
                    "Jumlah Donasi": jumlah_k,
                    "Donatur": int(grup_k["Alamat Donatur"].nunique()),
                    "Hitung": hitung_k,
                    "Disalurkan": tersalur_k,
                    "Terverifikasi": hitung_k[3],
                    "Progres": tersalur_k / jumlah_k,
                    "Terbaru": int(grup_k["ID"].max()),
                    "Tahap": tahap_k,
                    "Saldo": saldo_k
                })

            label_tahap = {
                "wait": "Menunggu penyaluran",
                "run": "Sedang disalurkan",
                "done": "Selesai terverifikasi"
            }

            # =========================================
            # TAMPILAN DETAIL SATU KAMPANYE
            # =========================================

            aktif = st.session_state.kampanye_aktif
            ringkas = next(
                (k for k in daftar_k if k["Kampanye"] == aktif), None
            )

            if aktif is not None and ringkas is None:
                st.session_state.kampanye_aktif = None
                aktif = None

            if ringkas is not None:

                grup_detail = data_k[
                    data_k["Kampanye"] == aktif
                ].sort_values("ID")

                st.button(
                    "← Semua kampanye",
                    on_click=tutup_kampanye,
                    key="kembali_kampanye"
                )

                h(
                    f'<div class="page-title">{escape(str(aktif))}</div>'
                    f'<div class="page-desc"><span class="chip {ringkas["Tahap"]}">'
                    f'{label_tahap[ringkas["Tahap"]]}</span> &nbsp; '
                    f'{ringkas["Jumlah Donasi"]} donasi dari '
                    f'{ringkas["Donatur"]} donatur</div>'
                )

                d1, d2, d3, d4 = st.columns(4)

                with d1:
                    st.metric("💰 Dana Masuk", rupiah(ringkas["Dana Masuk"]))

                with d2:
                    st.metric(
                        "🏦 Saldo Kontrak",
                        rupiah(ringkas["Saldo"])
                        if ringkas["Saldo"] is not None else "-"
                    )

                with d3:
                    st.metric(
                        "📦 Disalurkan",
                        f'{ringkas["Disalurkan"]}/{ringkas["Jumlah Donasi"]}'
                    )

                with d4:
                    st.metric(
                        "✅ Terverifikasi",
                        f'{ringkas["Terverifikasi"]}/{ringkas["Jumlah Donasi"]}'
                    )

                judul_blok("Posisi dana saat ini")

                kartu_tahap = ""
                for s in range(4):
                    nom_s = int(
                        grup_detail.loc[
                            grup_detail["Status"] == s, "Jumlah"
                        ].sum()
                    )
                    kartu_tahap += (
                        f'<div class="pipe-card s{s}">'
                        f'<div class="pipe-name">{NAMA_STATUS[s]}</div>'
                        f'<div class="pipe-count">{ringkas["Hitung"][s]}</div>'
                        f'<div class="pipe-nom">{rupiah(nom_s)}</div></div>'
                    )

                h(f'<div class="pipe">{kartu_tahap}</div>')

                st.button(
                    "💚 Donasi ke kampanye ini",
                    type="primary",
                    on_click=donasi_ke_kampanye,
                    args=(aktif,),
                    key="donasi_dari_detail"
                )

                tab_ringkasan, tab_donasi, tab_donatur, tab_aktivitas = st.tabs(
                    ["Perkembangan", "Semua donasi", "Donatur", "Aktivitas"]
                )

                # ----- Tab: perkembangan dana -----
                with tab_ringkasan:

                    grafik_k = grup_detail.copy()
                    grafik_k["Dana Terkumpul"] = grafik_k["Jumlah"].cumsum()
                    grafik_k["Donasi ke-"] = range(1, len(grafik_k) + 1)

                    st.line_chart(
                        grafik_k.set_index("Donasi ke-")[["Dana Terkumpul"]],
                        color="#0B6B4F"
                    )
                    st.caption(
                        "Dana terkumpul bertambah setiap donasi baru "
                        "dicatat, diurutkan menurut ID donasi."
                    )

                    st.write("**Pengelola dana (wallet pengelola kontrak):**")
                    st.code(alamat_pengelola)

                    tujuan_unik = [
                        t for t in grup_detail["Tujuan"].astype(str).unique()
                        if t.strip()
                    ]

                    if tujuan_unik:
                        st.write("**Tujuan penggunaan dana:**")
                        for t in tujuan_unik:
                            st.write("•", t)
                    else:
                        st.caption(
                            "Pengelola belum menetapkan tujuan penggunaan dana."
                        )

                # ----- Tab: semua donasi -----
                with tab_donasi:

                    tabel_k = grup_detail.copy()
                    tabel_k["Status"] = tabel_k["Status"].map(NAMA_STATUS)
                    tabel_k["Jumlah"] = tabel_k["Jumlah"].apply(rupiah)
                    tabel_k["Waktu"] = tabel_k["Timestamp"].apply(waktu_fmt)

                    kolom_tabel = [
                        "ID", "Donatur", "Alamat Donatur",
                        "Jumlah", "Status", "Waktu"
                    ]

                    st.dataframe(
                        tabel_k[kolom_tabel],
                        use_container_width=True,
                        hide_index=True
                    )

                    st.download_button(
                        "⬇️ Unduh data kampanye (CSV)",
                        data=tabel_k[kolom_tabel].to_csv(index=False).encode("utf-8"),
                        file_name=f"kampanye_{aktif}.csv",
                        mime="text/csv"
                    )

                # ----- Tab: donatur teratas -----
                with tab_donatur:

                    donatur_k = (
                        grup_detail.groupby("Alamat Donatur")
                        .agg(
                            Nama=("Donatur", "last"),
                            Donasi=("ID", "count"),
                            Total=("Jumlah", "sum")
                        )
                        .reset_index()
                        .sort_values("Total", ascending=False)
                    )

                    total_semua = donatur_k["Total"].sum() or 1
                    donatur_k["Kontribusi"] = donatur_k["Total"] / total_semua * 100
                    donatur_k["Nominal"] = donatur_k["Total"].apply(rupiah)

                    st.dataframe(
                        donatur_k[
                            ["Nama", "Alamat Donatur", "Donasi", "Nominal", "Kontribusi"]
                        ],
                        use_container_width=True,
                        hide_index=True,
                        column_config={
                            "Kontribusi": st.column_config.ProgressColumn(
                                "Kontribusi",
                                format="%.0f%%",
                                min_value=0,
                                max_value=100
                            )
                        }
                    )

                # ----- Tab: aktivitas -----
                with tab_aktivitas:

                    isi_aktivitas = ""

                    for _, r in grup_detail.sort_values(
                        "ID", ascending=False
                    ).iterrows():
                        tx = str(r.get("Tx Hash", "-"))
                        isi_aktivitas += (
                            f'<div class="feed-item"><div class="feed-dot s{int(r["Status"])}"></div>'
                            f'<div class="feed-body"><b>{escape(str(r["Donatur"]))}</b> '
                            f'mencatat donasi {rupiah(r["Jumlah"])} {chip_status(r["Status"])}'
                            f'<div class="feed-meta">#{int(r["ID"])} · {waktu_fmt(r["Timestamp"])} · '
                            f'Blok {int(r.get("Block", 0))} · Tx {pendek(tx, 8, 6)}</div>'
                            f'</div></div>'
                        )

                    h(f'<div>{isi_aktivitas}</div>')

            # =========================================
            # TAMPILAN DAFTAR KAMPANYE
            # =========================================

            else:

                total_dana_k = sum(k["Dana Masuk"] for k in daftar_k)
                total_salur_k = sum(k["Disalurkan"] for k in daftar_k)
                total_donasi_k = sum(k["Jumlah Donasi"] for k in daftar_k)

                judul(
                    "Kampanye",
                    "Pantau dana masuk dan progres penyaluran setiap "
                    "kampanye. Pilih satu kampanye untuk melihat "
                    "rinciannya."
                )

                m1, m2, m3 = st.columns(3)

                with m1:
                    st.metric("📢 Kampanye", len(daftar_k))

                with m2:
                    st.metric("💰 Total Dana Masuk", rupiah(total_dana_k))

                with m3:
                    st.metric(
                        "📦 Donasi Tersalurkan",
                        f"{total_salur_k}/{total_donasi_k}"
                    )

                st.write("")

                kc1, kc2, kc3 = st.columns([2, 1, 1])

                with kc1:
                    kata_kampanye = st.text_input(
                        "Cari kampanye",
                        placeholder="Contoh: BANTUAN-001",
                        key="cari_kampanye"
                    )

                with kc2:
                    filter_tahap = st.selectbox(
                        "Tahap",
                        ["Semua", "Menunggu penyaluran", "Sedang disalurkan", "Selesai terverifikasi"],
                        key="filter_tahap_kampanye"
                    )

                with kc3:
                    urutan = st.selectbox(
                        "Urutkan",
                        ["Dana terbesar", "Terbaru", "Progres tertinggi", "Nama A–Z"],
                        key="urutan_kampanye"
                    )

                tampil_k = [
                    k for k in daftar_k
                    if kata_kampanye.strip().lower() in str(k["Kampanye"]).lower()
                ]

                if filter_tahap != "Semua":
                    tampil_k = [
                        k for k in tampil_k
                        if label_tahap[k["Tahap"]] == filter_tahap
                    ]

                if urutan == "Dana terbesar":
                    tampil_k.sort(key=lambda k: k["Dana Masuk"], reverse=True)
                elif urutan == "Terbaru":
                    tampil_k.sort(key=lambda k: k["Terbaru"], reverse=True)
                elif urutan == "Progres tertinggi":
                    tampil_k.sort(key=lambda k: k["Progres"], reverse=True)
                else:
                    tampil_k.sort(key=lambda k: str(k["Kampanye"]).lower())

                st.caption(
                    f"Menampilkan {len(tampil_k)} dari {len(daftar_k)} kampanye. "
                    "Kontrak belum menyimpan target dana, sehingga progres "
                    "dihitung dari tahap penyaluran donasi."
                )

                if not tampil_k:
                    st.warning(
                        "Kampanye tidak ditemukan. Ubah kata kunci atau filter tahap."
                    )

                # Grid 2 kolom
                for i in range(0, len(tampil_k), 2):

                    kolom_kartu = st.columns(2, gap="medium")

                    for kolom, k in zip(kolom_kartu, tampil_k[i:i + 2]):

                        with kolom:

                            with st.container(border=True):

                                saldo_teks = (
                                    rupiah(k["Saldo"])
                                    if k["Saldo"] is not None else "tidak tersedia"
                                )

                                h(
                                    f'<div class="camp-head">'
                                    f'<div class="camp-title">{escape(str(k["Kampanye"]))}</div>'
                                    f'<span class="chip {k["Tahap"]}">{label_tahap[k["Tahap"]]}</span></div>'
                                    f'<div class="camp-amount">{rupiah(k["Dana Masuk"])}</div>'
                                    f'<div class="camp-sub">dana tercatat dari '
                                    f'{k["Jumlah Donasi"]} donasi · {k["Donatur"]} donatur</div>'
                                    f'{bar_tahapan(k["Hitung"])}'
                                    f'<div class="camp-foot"><span>Saldo kontrak '
                                    f'<b>{saldo_teks}</b></span>'
                                    f'<span><b>{k["Terverifikasi"]}</b> terverifikasi</span></div>'
                                )

                                st.button(
                                    "Lihat rincian",
                                    key=f"buka_{k['Kampanye']}",
                                    on_click=buka_kampanye,
                                    args=(k["Kampanye"],),
                                    use_container_width=True
                                )


    # ==========================================
    # MENU: DETAIL DONASI (BERDASARKAN ID)
    # ==========================================

    elif menu_pilihan == M_DETAIL:

        judul(
            "Detail Donasi",
            "Lihat data lengkap satu donasi berdasarkan ID."
        )

        if data_donasi.empty:

            st.info(
                "Belum ada donasi yang dapat ditampilkan. "
                "Catat donasi terlebih dahulu."
            )

        else:

            data_d = data_donasi.copy()
            data_d["ID"] = data_d["ID"].astype(int)

            baris_donasi = {
                int(baris["ID"]): baris
                for _, baris in data_d.iterrows()
            }

            id_dipilih = st.selectbox(
                "Pilih ID Donasi",
                options=sorted(baris_donasi.keys(), reverse=True),
                format_func=lambda i: (
                    f"#{i} · {baris_donasi[i]['Donatur']} "
                    f"· {baris_donasi[i]['Kampanye']}"
                ),
                key="pilih_detail_donasi"
            )

            d = baris_donasi[id_dipilih]
            status_d = int(d["Status"])

            # Tahapan status donasi
            tahap = ["Dicatat", "Dikelola", "Disalurkan", "Terverifikasi"]
            html_tahap = '<div class="stepper">'

            for i, nama_tahap in enumerate(tahap):
                kelas = "step"
                if i <= status_d:
                    kelas += " done"
                if i == status_d:
                    kelas += " now"
                isi = "✓" if i <= status_d else str(i + 1)
                html_tahap += (
                    f'<div class="{kelas}"><div class="bulat">{isi}</div>'
                    f'{nama_tahap}</div>'
                )

            html_tahap += "</div>"

            h(html_tahap)

            with st.container(border=True):

                st.markdown(f"#### Donasi #{id_dipilih}")

                m1, m2 = st.columns(2)

                with m1:
                    st.metric("💰 Nominal Tercatat", rupiah(d["Jumlah"]))

                with m2:
                    st.metric(
                        "📌 Status",
                        NAMA_STATUS.get(status_d, "Tidak diketahui")
                    )

                st.write("**Kampanye:**", d["Kampanye"])
                st.write("**Nama Donatur:**", d["Donatur"])
                st.write("**Waktu Pencatatan:**", waktu_fmt(d["Timestamp"]))

                st.write(
                    "**Tujuan Penggunaan Dana:**",
                    d["Tujuan"] if d["Tujuan"] else "Belum ditentukan oleh pengelola"
                )

                st.write("**Alamat Wallet Donatur:**")
                st.code(str(d["Alamat Donatur"]))

                st.write("**Nomor Blok Pencatatan:**", d.get("Block", "-"))
                st.write("**Hash Transaksi Pencatatan:**")
                st.code(str(d.get("Tx Hash", "-")))

            st.caption(
                "Hash dan nomor blok berasal dari transaksi pencatatan donasi."
            )


    # ==========================================
    # MENU: WALLET (PERAN AKUN)
    # ==========================================

    elif menu_pilihan == M_WALLET:

        wallet_peran = st.session_state.get("wallet_data")

        if wallet_peran and "account" in wallet_peran:

            akun_peran = wallet_peran["account"].lower()

            if akun_peran == alamat_pengelola.lower():
                nama_peran = "Pengelola"
                hak_akses = "Kelola donasi, salurkan donasi, dan daftarkan pengawas."
            elif akun_peran == kontrak.functions.pengawas().call().lower():
                nama_peran = "Pengawas"
                hak_akses = "Verifikasi donasi yang telah disalurkan."
            else:
                nama_peran = "Donatur / pengguna umum"
                hak_akses = "Mencatat donasi dan melihat seluruh data secara terbuka."

            judul_blok("Peran akun")
            st.success(f"**{nama_peran}**")
            st.caption(f"Hak akses: {hak_akses}")

        st.caption(
            "Status transaksi (menunggu konfirmasi, berhasil, atau gagal) "
            "ditampilkan di halaman tempat transaksi dikirim."
        )


    # ==========================================
    # MENU: INFORMASI BLOCKCHAIN
    # ==========================================

    elif menu_pilihan == M_INFO:

        judul(
            "Informasi Blockchain",
            "Informasi jaringan dan smart contract yang digunakan."
        )

        col4, col5 = st.columns(2)

        with col4:
            st.info(
                f"**Jaringan:** Hardhat Local\n\n"
                f"**Chain ID:** {w3.eth.chain_id}\n\n"
                f"**Jumlah Blok:** {w3.eth.block_number}"
            )

        with col5:
            st.info(
                f"**Alamat Smart Contract:**\n\n"
                f"{kontrak.address}"
            )

        st.write("**Alamat Pengelola:**")
        st.code(alamat_pengelola)

        if st.button("🔄 Segarkan Data"):

            st.cache_resource.clear()
            st.rerun()


except Exception as error:

    st.error("Tidak dapat terhubung ke smart contract.")

    st.code(str(error))

    st.info(
        "Pastikan Hardhat Node sedang berjalan dan alamat "
        "smart contract sesuai dengan jaringan yang aktif."
    )


# ==========================================
# FOOTER
# ==========================================

st.divider()

h("""
<div class="footer">
<b>AmalTransparan</b><br>
Transparansi untuk setiap donasi · Platform donasi berbasis blockchain
</div>
""")