import streamlit as st
import pandas as pd
import json
from datetime import datetime
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
# DESAIN CSS - AMALTRANSPARAN (HIJAU TUA & PUTIH)
# ==========================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

/* FONT */
.stApp, .stApp p, .stApp label, .stApp li, .stApp h1, .stApp h2,
.stApp h3, .stApp h4, .stApp h5, .stApp h6, .stApp button,
.stApp input, .stApp textarea {
    font-family: 'Plus Jakarta Sans', 'Segoe UI', sans-serif;
}

/* BACKGROUND: PUTIH - HIJAU TUA DENGAN GARIS HITAM */
.stApp {
    background-color: #F6FAF8 !important;
    background-image:
        linear-gradient(rgba(0, 0, 0, 0.065) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0, 0, 0, 0.065) 1px, transparent 1px),
        radial-gradient(circle at 10% 6%, rgba(6, 78, 59, 0.22), transparent 38%),
        radial-gradient(circle at 92% 94%, rgba(4, 120, 87, 0.20), transparent 42%),
        linear-gradient(160deg, #FFFFFF 0%, #EEF6F2 100%) !important;
    background-size: 44px 44px, 44px 44px, 100% 100%, 100% 100%, 100% 100% !important;
    background-attachment: fixed !important;
    color: #1F3A30 !important;
}

[data-testid="stHeader"] {
    background: transparent !important;
}

/* FEED ALA INSTAGRAM (KOLOM TENGAH) */
.block-container {
    max-width: 780px !important;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}

/* JUDUL */
h1, h2, h3, h4, h5, h6 {
    color: #064E3B !important;
    font-weight: 800 !important;
}

/* JUDUL BAGIAN (CHIP PUTIH) */
h2 {
    font-size: 1.2rem !important;
    background-color: #FFFFFF;
    border: 1px solid #CFE5DA;
    border-left: 6px solid #065F46;
    border-radius: 999px;
    padding: 8px 18px !important;
    width: fit-content;
    box-shadow: 0 2px 8px rgba(6, 78, 59, 0.08);
    margin-top: 0.4rem;
}

/* TEKS UMUM */
p, li, label {
    color: #1F3A30;
}

[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li {
    color: #1F3A30;
}

/* LABEL INPUT */
[data-testid="stWidgetLabel"] p {
    color: #064E3B !important;
    font-weight: 600 !important;
}

.stCaption,
[data-testid="stCaptionContainer"] {
    color: #4B6358 !important;
}

/* ===== JUDUL DAN DESKRIPSI BAGIAN ===== */
.section-heading {
    display: inline-block;
    color: #064E3B;
    background-color: #FFFFFF;
    border: 1px solid #CFE5DA;
    border-left: 6px solid #065F46;
    border-radius: 999px;
    padding: 8px 18px;
    font-size: 1.2rem;
    font-weight: 800;
    margin-top: 0.5rem;
    margin-bottom: 0.5rem;
    box-shadow: 0 2px 8px rgba(6, 78, 59, 0.08);
}

.section-description {
    color: #4B6358;
    font-size: 0.92rem;
    margin-bottom: 1rem;
}

/* ===== KARTU PROFIL (HERO) ===== */
.profile-card {
    position: relative;
    overflow: hidden;
    background:
        radial-gradient(circle at 88% 12%, rgba(255, 255, 255, 0.16), transparent 42%),
        radial-gradient(circle at 5% 100%, rgba(110, 231, 183, 0.18), transparent 40%),
        linear-gradient(135deg, #032B20 0%, #064E3B 55%, #047857 100%);
    border-radius: 28px;
    padding: 28px;
    margin-bottom: 20px;
    box-shadow: 0 20px 44px rgba(3, 43, 32, 0.35);
}

.profile-top {
    display: flex;
    align-items: center;
    gap: 22px;
}

.avatar-ring {
    width: 96px;
    height: 96px;
    flex-shrink: 0;
    border-radius: 50%;
    padding: 4px;
    background: conic-gradient(
        from 210deg,
        #ECFDF5, #6EE7B7, #FFFFFF, #6EE7B7, #ECFDF5
    );
}

.avatar-inner {
    width: 100%;
    height: 100%;
    border-radius: 50%;
    background-color: #FFFFFF;
    border: 3px solid #064E3B;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 40px;
}

.profile-kicker {
    color: #6EE7B7;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2px;
}

.profile-name {
    color: #FFFFFF;
    font-size: 30px;
    font-weight: 800;
    margin: 2px 0;
    line-height: 1.2;
}

.profile-tagline {
    color: #ECFDF5;
    font-size: 15px;
    font-weight: 700;
}

.profile-desc {
    color: rgba(236, 253, 245, 0.82);
    font-size: 13.5px;
    line-height: 1.7;
    margin-top: 18px;
}

.profile-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 16px;
}

.profile-tag {
    color: #ECFDF5;
    background-color: rgba(255, 255, 255, 0.12);
    border: 1px solid rgba(255, 255, 255, 0.22);
    border-radius: 999px;
    padding: 5px 12px;
    font-size: 11.5px;
    font-weight: 600;
}

/* ===== MENU FITUR (GESER SAMPING, GAYA INSTAGRAM) ===== */
.menu-title {
    color: #064E3B;
    font-size: 13px;
    font-weight: 800;
    letter-spacing: 1px;
    margin: 6px 0 0 4px;
}

.menu-hint {
    color: #4B6358;
    font-size: 12px;
    margin: 0 0 2px 4px;
}

div[data-testid="stRadio"] div[role="radiogroup"] {
    display: flex !important;
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    overflow-x: auto;
    gap: 10px !important;
    padding: 8px 4px 16px 4px;
    scrollbar-width: thin;
    scrollbar-color: #065F46 transparent;
}

div[data-testid="stRadio"] label[data-baseweb="radio"] {
    flex: 0 0 auto;
    margin: 0 !important;
    padding: 11px 20px !important;
    background-color: #FFFFFF;
    border: 1.5px solid #CFE5DA;
    border-radius: 999px;
    box-shadow: 0 4px 12px rgba(6, 78, 59, 0.08);
    cursor: pointer;
    transition: all 0.2s ease;
}

/* Sembunyikan bulatan radio bawaan */
div[data-testid="stRadio"] label[data-baseweb="radio"] > div:first-child {
    display: none !important;
}

div[data-testid="stRadio"] label[data-baseweb="radio"] p {
    margin: 0 !important;
    color: #064E3B !important;
    font-size: 0.9rem !important;
    font-weight: 700 !important;
    white-space: nowrap;
}

div[data-testid="stRadio"] label[data-baseweb="radio"]:hover {
    transform: translateY(-2px);
    border-color: #065F46;
    box-shadow: 0 8px 18px rgba(6, 78, 59, 0.16);
}

/* Menu yang sedang dipilih */
div[data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked) {
    background: linear-gradient(135deg, #032B20, #065F46) !important;
    border-color: #032B20 !important;
    box-shadow: 0 10px 22px rgba(3, 43, 32, 0.38);
}

div[data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked) p,
div[data-testid="stRadio"] label[data-baseweb="radio"]:has(input:checked) * {
    color: #FFFFFF !important;
}

/* ===== KARTU DASHBOARD ===== */
[data-testid="stMetric"] {
    background-color: #FFFFFF;
    padding: 20px;
    border-radius: 18px;
    border: 1px solid #CFE5DA;
    border-left: 6px solid #065F46;
    box-shadow: 0 6px 16px rgba(6, 78, 59, 0.09);
    transition: all 0.2s ease;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-3px);
    box-shadow: 0 12px 26px rgba(6, 78, 59, 0.16);
}

[data-testid="stMetricLabel"],
[data-testid="stMetricLabel"] * {
    color: #4B6358 !important;
    font-weight: 600 !important;
}

[data-testid="stMetricValue"],
[data-testid="stMetricValue"] * {
    color: #064E3B !important;
    font-weight: 800 !important;
}

/* ===== KARTU GRAFIK ===== */
[data-testid="stVegaLiteChart"] {
    background-color: #FFFFFF;
    padding: 18px;
    border-radius: 18px;
    border: 1px solid #CFE5DA;
    box-shadow: 0 6px 16px rgba(6, 78, 59, 0.09);
}

/* ===== KARTU POSTINGAN (CONTAINER BERBORDER) ===== */
[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: #FFFFFF;
    border: 1px solid #CFE5DA !important;
    border-radius: 20px !important;
    box-shadow: 0 8px 24px rgba(6, 78, 59, 0.09);
}

[data-testid="stForm"] {
    border: none !important;
    padding: 0 !important;
}

/* ===== KOTAK INFORMASI ===== */
[data-testid="stAlert"] {
    border-radius: 14px;
}

/* ===== FORM INPUT ===== */
.stTextInput input,
.stNumberInput input,
.stTextArea textarea,
.stDateInput input {
    background-color: #F7FBF9 !important;
    color: #1F3A30 !important;
    border: 1px solid #BFD8CB !important;
    border-radius: 12px !important;
}

.stTextInput input:focus,
.stNumberInput input:focus,
.stTextArea textarea:focus {
    border-color: #065F46 !important;
    box-shadow: 0 0 0 3px rgba(6, 95, 70, 0.20) !important;
}

/* Placeholder */
.stTextInput input::placeholder,
.stTextArea textarea::placeholder {
    color: #6B8277 !important;
    opacity: 1 !important;
}

/* ===== DROPDOWN ===== */
[data-baseweb="select"] > div {
    background-color: #F7FBF9 !important;
    border-color: #BFD8CB !important;
    border-radius: 12px !important;
}

[data-baseweb="select"] * {
    color: #1F3A30 !important;
}

/* ==========================================
   TOMBOL HIJAU TUA
   ========================================== */

.stButton > button,
.stFormSubmitButton > button,
.stDownloadButton > button {
    background: linear-gradient(135deg, #064E3B, #047857) !important;
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 10px 20px !important;
    font-weight: 700 !important;
    box-shadow: 0 6px 14px rgba(6, 78, 59, 0.30);
    transition: all 0.2s ease;
}

.stButton > button *,
.stFormSubmitButton > button *,
.stDownloadButton > button * {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover,
.stDownloadButton > button:hover {
    background: linear-gradient(135deg, #032B20, #065F46) !important;
    transform: translateY(-2px);
    box-shadow: 0 10px 20px rgba(6, 78, 59, 0.38);
    color: #FFFFFF !important;
}

.stButton > button:disabled,
.stFormSubmitButton > button:disabled {
    background: #9CB2A5 !important;
    box-shadow: none;
    color: #FFFFFF !important;
}

/* ===== TABEL RIWAYAT ===== */
[data-testid="stDataFrame"],
[data-testid="stTable"] {
    background-color: #FFFFFF;
    border: 1px solid #CFE5DA;
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 6px 16px rgba(6, 78, 59, 0.09);
}

/* ===== SIDEBAR ===== */
[data-testid="stSidebar"] {
    background-color: #E7F2EC;
}

/* ==========================================
   ALAMAT WALLET DAN SMART CONTRACT
   ========================================== */

[data-testid="stCode"],
.stCode {
    background-color: #ECF6F0 !important;
    border: 1px solid #BFDCCB !important;
    border-radius: 12px !important;
    overflow-wrap: anywhere !important;
}

[data-testid="stCode"] code,
[data-testid="stCode"] pre,
.stCode code,
.stCode pre {
    color: #064E3B !important;
    -webkit-text-fill-color: #064E3B !important;
    background-color: #ECF6F0 !important;
    white-space: pre-wrap !important;
    overflow-wrap: anywhere !important;
    word-break: break-word !important;
}

/* ===== BAGIAN METAMASK ===== */
.metamask-section {
    background-color: #FFFFFF;
    padding: 22px;
    border-radius: 18px;
    border: 1px solid #CFE5DA;
    margin-bottom: 20px;
}

/* ===== LINK ===== */
a {
    color: #047857 !important;
    font-weight: 600;
}

/* ===== GARIS PEMBATAS ===== */
hr {
    border-color: rgba(6, 78, 59, 0.18) !important;
    margin: 1.6rem 0 !important;
}

/* ===== FOOTER ===== */
.footer {
    color: #4B6358;
    text-align: center;
    padding: 20px;
    line-height: 1.8;
    background-color: #FFFFFF;
    border: 1px solid #CFE5DA;
    border-radius: 20px;
}

.footer b {
    color: #064E3B;
}

/* ===== TAMPILAN PONSEL ===== */
@media (max-width: 640px) {
    .profile-top {
        flex-direction: column;
        text-align: center;
    }

    .profile-tags {
        justify-content: center;
    }
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# HERO SECTION (KARTU PROFIL)
# ==========================================


st.html("""
<div class="profile-card">
<div class="profile-top">
<div class="avatar-ring"><div class="avatar-inner">🤝</div></div>
<div>
<div class="profile-kicker">BLOCKCHAIN DONATION PLATFORM</div>
<div class="profile-name">AmalTransparan</div>
<div class="profile-tagline">Transparansi Donasi, Membangun Kepercayaan.</div>
</div>
</div>
<div class="profile-desc">
Platform transparansi donasi berbasis blockchain
untuk memantau pencatatan bantuan dan penyaluran
secara terbuka.
</div>
<div class="profile-tags">
<span class="profile-tag">⛓️ Hardhat Local</span>
<span class="profile-tag">🔐 Smart Contract</span>
<span class="profile-tag">🖼️ NFT Bukti Donasi</span>
</div>
</div>
""")


# ==========================================
# MENU FITUR (GESER KE SAMPING)
# ==========================================

M_BERANDA = "🏠 Beranda"
M_DONASI = "💚 Donasi"
M_KELOLA = "📝 Kelola"
M_SALURKAN = "📦 Salurkan"
M_VERIFIKASI = "🔍 Verifikasi"
M_PENGAWAS = "🛡️ Pengawas"
M_RIWAYAT = "📋 Riwayat"
M_INFO = "🔗 Info"

st.markdown(
    '<div class="menu-title">PILIH FITUR</div>'
    '<div class="menu-hint">Geser ke samping, lalu pilih fitur yang ingin dibuka.</div>',
    unsafe_allow_html=True
)

menu_pilihan = st.radio(
    "Menu Fitur",
    [
        M_BERANDA,
        M_DONASI,
        M_KELOLA,
        M_SALURKAN,
        M_VERIFIKASI,
        M_PENGAWAS,
        M_RIWAYAT,
        M_INFO,
    ],
    horizontal=True,
    label_visibility="collapsed",
    key="menu_fitur"
)


# ==========================================
# INTEGRASI METAMASK
# ==========================================

st.markdown(
    '<div class="section-heading">🦊 Hubungkan MetaMask</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-description">'
    'Hubungkan wallet untuk melihat alamat akun dan saldo ETH.'
    '</div>',
    unsafe_allow_html=True
)

if "wallet_request_id" not in st.session_state:
    st.session_state.wallet_request_id = 0

if "wallet_data" not in st.session_state:
    st.session_state.wallet_data = None

if st.button("🦊 Hubungkan MetaMask", type="primary"):
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


st.divider()

# ==========================================
# KONEKSI SMART CONTRACT
# ==========================================

@st.cache_resource
def koneksi_kontrak():
    return hubungkan_blockchain()


try:

    w3, kontrak = koneksi_kontrak()

    st.success("Blockchain Hardhat berhasil terhubung!")

    alamat_pengelola = kontrak.functions.pengelola().call()

    # ==========================================
    # MEMBACA DATA DONASI DARI SMART CONTRACT
    # ==========================================

    seluruh_id = []

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
                "Timestamp": int(data[7])
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

        st.markdown(
            '<div class="section-heading">📈 Ringkasan Donasi</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="section-description">'
            'Ikhtisar catatan donasi yang tersimpan pada blockchain.'
            '</div>',
            unsafe_allow_html=True
        )

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

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "💰 Total Donasi Tercatat",
                f"Rp {total_donasi:,}".replace(",", ".")
            )

        with col2:
            st.metric(
                "📢 Jumlah Kampanye",
                jumlah_kampanye
            )

        with col3:
            st.metric(
                "🔍 Donasi Terverifikasi",
                jumlah_terverifikasi
            )

        st.caption(
            "Catatan: nominal merupakan data yang tersimpan "
            "dalam smart contract, bukan bukti transfer uang."
        )

        st.divider()

        st.markdown(
            '<div class="section-heading">📊 Statistik Donasi</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="section-description">'
            'Visualisasi nominal donasi berdasarkan kampanye.'
            '</div>',
            unsafe_allow_html=True
        )

        if not data_donasi.empty:

            data_grafik = (
                data_donasi.groupby("Kampanye")["Jumlah"]
                .sum()
                .to_frame()
            )

            st.bar_chart(data_grafik, color="#065F46")

        else:
            st.info(
                "Belum ada donasi yang tercatat di smart contract."
            )


    # ==========================================
    # MENU: FORM DONASI - INTEGRASI SMART CONTRACT
    # ==========================================

    elif menu_pilihan == M_DONASI:

        st.markdown("## 💚 Form Donasi")
        st.caption(
            "Catat donasi dan buat NFT sebagai bukti pencatatan "
            "donasi pada blockchain."
        )

        with st.container(border=True):
            with st.form("form_donasi_blockchain"):

                campaign_id = st.text_input(
                    "ID Kampanye",
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

        st.markdown("## 📝 Pengelolaan Donasi")
        st.caption(
            "Pengelola dapat menentukan tujuan penggunaan dana "
            "dan mengubah status donasi menjadi dikelola."
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

        st.markdown("## 📦 Penyaluran Donasi")
        st.caption(
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

        st.markdown("## 🔍 Verifikasi Donasi")
        st.caption(
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

        st.markdown("## 🛡️ Pendaftaran Pengawas")

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

        st.markdown(
            '<div class="section-heading">📋 Riwayat Donasi</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="section-description">'
            'Daftar catatan donasi yang tersimpan pada blockchain.'
            '</div>',
            unsafe_allow_html=True
        )

        if not data_donasi.empty:

            # Salin data asli agar filter tidak mengubah data blockchain.
            tampilan_asli = data_donasi.copy()

            st.markdown("### 🔎 Cari Data Donasi")
            st.caption(
                "Cari berdasarkan ID kampanye, ID donasi, nama donatur, "
                "alamat wallet, atau tujuan penggunaan."
            )

            kolom_cari, kolom_status = st.columns([2, 1])

            with kolom_cari:
                kata_kunci = st.text_input(
                    "Kata kunci pencarian",
                    placeholder="Contoh: BANTUAN-001, Donatur, atau ID 1",
                    key="cari_riwayat_donasi"
                )

            with kolom_status:
                pilihan_status = st.selectbox(
                    "Filter status",
                    [
                        "Semua Status",
                        "Menunggu diproses",
                        "Dikelola",
                        "Disalurkan",
                        "Terverifikasi"
                    ],
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

            status_map = {
                0: "Menunggu diproses",
                1: "Dikelola",
                2: "Disalurkan",
                3: "Terverifikasi"
            }

            if pilihan_status != "Semua Status":
                kode_status = {
                    nama: kode for kode, nama in status_map.items()
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
                    status_map
                ).fillna("Tidak diketahui")

                tampilan["Jumlah"] = tampilan["Jumlah"].apply(
                    lambda jumlah: (
                        "Rp " + f"{jumlah:,}".replace(",", ".")
                    )
                )

                tampilan["Waktu"] = tampilan["Timestamp"].apply(
                    lambda ts: datetime.fromtimestamp(ts).strftime(
                        "%d-%m-%Y %H:%M:%S"
                    ) if ts > 0 else "-"
                )

                st.dataframe(
                    tampilan[
                        [
                            "ID",
                            "Kampanye",
                            "Donatur",
                            "Alamat Donatur",
                            "Jumlah",
                            "Tujuan",
                            "Status",
                            "Waktu"
                        ]
                    ],
                    use_container_width=True,
                    hide_index=True
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
    # MENU: INFORMASI BLOCKCHAIN
    # ==========================================

    elif menu_pilihan == M_INFO:

        st.markdown(
            '<div class="section-heading">🔗 Informasi Blockchain</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="section-description">'
            'Informasi jaringan dan smart contract yang digunakan.'
            '</div>',
            unsafe_allow_html=True
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

st.markdown("""
<div class="footer">
    <b>AmalTransparan</b><br>
    Transparansi untuk setiap donasi.<br>
    Platform Donasi Berbasis Blockchain
</div>
""", unsafe_allow_html=True)