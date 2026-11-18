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
    layout="wide"
)

# ==========================================
# DESAIN CSS - AMALTRANSPARAN
# ==========================================

st.markdown("""
<style>
/* BACKGROUND APLIKASI */
.stApp {
    background-color: #F1F5F9 !important;
    color: #243447 !important;
}

.block-container {
    max-width: 1250px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* JUDUL */
h1, h2, h3, h4, h5, h6 {
    color: #163A5F !important;
    font-weight: 700 !important;
}

/* TEKS UMUM */
p, li, label {
    color: #243447;
}

/* TEKS MARKDOWN */
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li {
    color: #243447;
}

/* LABEL INPUT */
[data-testid="stWidgetLabel"] p {
    color: #1E3A5F !important;
    font-weight: 600 !important;
}

.stCaption,
[data-testid="stCaptionContainer"] {
    color: #526477 !important;
}

/* ===== JUDUL DAN DESKRIPSI BAGIAN ===== */
.section-heading {
    color: #163A5F;
    font-size: 1.5rem;
    font-weight: 700;
    margin-top: 0.5rem;
    margin-bottom: 0.5rem;
}

.section-description {
    color: #526477;
    font-size: 0.95rem;
    margin-bottom: 1rem;
}

/* ===== KARTU DASHBOARD ===== */
[data-testid="stMetric"] {
    background-color: #FFFFFF;
    padding: 22px;
    border-radius: 14px;
    border: 1px solid #CBD5E1;
    box-shadow: 0 4px 12px rgba(22, 58, 95, 0.06);
}

[data-testid="stMetricLabel"],
[data-testid="stMetricLabel"] * {
    color: #526477 !important;
    font-weight: 600 !important;
}

[data-testid="stMetricValue"],
[data-testid="stMetricValue"] * {
    color: #163A5F !important;
    font-weight: 700 !important;
}

/* ===== KARTU GRAFIK ===== */
[data-testid="stVegaLiteChart"] {
    background-color: #FFFFFF;
    padding: 18px;
    border-radius: 14px;
    border: 1px solid #CBD5E1;
}

/* ===== KOTAK INFORMASI ===== */
[data-testid="stAlert"] {
    border-radius: 10px;
}

/* ===== FORM INPUT ===== */
.stTextInput input,
.stNumberInput input,
.stTextArea textarea,
.stDateInput input {
    background-color: #FFFFFF !important;
    color: #243447 !important;
    border: 1px solid #A8B8CA !important;
    border-radius: 8px !important;
}

/* Placeholder */
.stTextInput input::placeholder,
.stTextArea textarea::placeholder {
    color: #64748B !important;
    opacity: 1 !important;
}

/* ===== DROPDOWN ===== */
[data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    border-color: #A8B8CA !important;
}

[data-baseweb="select"] * {
    color: #243447 !important;
}

/* ==========================================
   TOMBOL BIRU
   ========================================== */

.stButton > button,
.stFormSubmitButton > button,
.stDownloadButton > button {
    background-color: #2563EB !important;
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    border: 1px solid #2563EB !important;
    border-radius: 10px !important;
    padding: 10px 20px !important;
    font-weight: 700 !important;
    transition: all 0.2s ease;
}

/* Memastikan tulisan dan ikon tombol putih */
.stButton > button *,
.stFormSubmitButton > button *,
.stDownloadButton > button * {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
}

/* Efek ketika kursor diarahkan ke tombol */
.stButton > button:hover,
.stFormSubmitButton > button:hover,
.stDownloadButton > button:hover {
    background-color: #1D4ED8 !important;
    border-color: #1D4ED8 !important;
    color: #FFFFFF !important;
}

/* Tombol yang tidak aktif */
.stButton > button:disabled,
.stFormSubmitButton > button:disabled {
    background-color: #94A3B8 !important;
    border-color: #94A3B8 !important;
    color: #FFFFFF !important;
}

/* ===== TABEL RIWAYAT ===== */
[data-testid="stDataFrame"],
[data-testid="stTable"] {
    background-color: #FFFFFF;
    border: 1px solid #CBD5E1;
    border-radius: 12px;
}

/* ===== SIDEBAR ===== */
[data-testid="stSidebar"] {
    background-color: #E7EEF7;
}

/* ==========================================
   ALAMAT WALLET DAN SMART CONTRACT
   ========================================== */

[data-testid="stCode"],
.stCode {
    background-color: #EFF6FF !important;
    border: 1px solid #BFDBFE !important;
    border-radius: 10px !important;
    overflow-wrap: anywhere !important;
}

/* Teks alamat wallet dan kode */
[data-testid="stCode"] code,
[data-testid="stCode"] pre,
.stCode code,
.stCode pre {
    color: #1D4ED8 !important;
    -webkit-text-fill-color: #1D4ED8 !important;
    background-color: #EFF6FF !important;
    white-space: pre-wrap !important;
    overflow-wrap: anywhere !important;
    word-break: break-word !important;
}

/* ===== BAGIAN METAMASK ===== */
.metamask-section {
    background-color: #FFFFFF;
    padding: 22px;
    border-radius: 14px;
    border: 1px solid #CBD5E1;
    margin-bottom: 20px;
}

/* ===== LINK ===== */
a {
    color: #2563EB !important;
    font-weight: 600;
}

/* ===== GARIS PEMBATAS ===== */
hr {
    border-color: #CBD5E1 !important;
}

/* ===== FOOTER ===== */
.footer {
    color: #526477;
    text-align: center;
    padding: 20px 0;
    line-height: 1.8;
}

.footer b {
    color: #163A5F;
}

/* NAVIGASI DAN TAMPILAN MODERN */
.welcome-line { background: linear-gradient(120deg,#103f35,#168568); padding: 22px 26px; border-radius: 16px; margin: 8px 0 22px; color: #fff; }
.welcome-line span { color:#bce8d3; font-size:11px; font-weight:800; letter-spacing:2px; }
.welcome-line h2 { color:#fff !important; margin:8px 0 4px; font-size:25px; }
.welcome-line p { color:#e2f5ec !important; margin:0; }
.stTabs [data-baseweb="tab-list"] { gap:7px; background:#e5edf2; padding:8px; border-radius:14px; }
.stTabs [data-baseweb="tab"] { border-radius:10px; padding:10px 15px; background:#f8fafc; color:#29445b; font-weight:700; }
.stTabs [aria-selected="true"] { background:#16785e !important; color:white !important; }
.stTabs [data-baseweb="tab-highlight"] { background:transparent; }
.stTabs [data-baseweb="tab-border"] { background:transparent; }
[data-testid="stVerticalBlockBorderWrapper"] { border-radius:15px; border-color:#d8e3e8; }

</style>
""", unsafe_allow_html=True)

# ==========================================
# HERO SECTION
# ==========================================


st.html("""
<div style="
    background: linear-gradient(120deg, #145C48, #23866A);
    padding: 35px;
    border-radius: 18px;
    margin-bottom: 25px;
">
    <p style="
        color: #BCE8D3;
        font-size: 12px;
        font-weight: bold;
        letter-spacing: 2px;
    ">
        BLOCKCHAIN DONATION PLATFORM
    </p>

    <h1 style="
        color: white;
        font-size: 38px;
        margin-bottom: 10px;
    ">
        🤝 AmalTransparan
    </h1>

    <p style="
        color: white;
        font-size: 19px;
        font-weight: bold;
    ">
        Transparansi Donasi, Membangun Kepercayaan.
    </p>

    <p style="
        color: #E2F5EC;
        font-size: 15px;
    ">
        Platform transparansi donasi berbasis blockchain
        untuk memantau pencatatan bantuan dan penyaluran
        secara terbuka.
    </p>
</div>
""")


# ==========================================
# NAVIGASI HALAMAN
# ==========================================
st.markdown("""<div class="welcome-line"><span>PLATFORM DONASI DIGITAL</span><h2>Selamat datang di AmalTransparan 👋</h2><p>Pilih menu untuk mengelola dan memantau donasi berbasis blockchain.</p></div>""", unsafe_allow_html=True)

tab_wallet, tab_donasi, tab_kelola, tab_verifikasi, tab_dashboard, tab_riwayat, tab_blockchain = st.tabs([
    "🦊 Wallet", "💚 Donasi", "🛠️ Pengelolaan", "🔍 Verifikasi",
    "📊 Dashboard", "📋 Riwayat", "⛓️ Blockchain"
])


# ==========================================
with tab_wallet:
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
    
    
    # ==========================================
    with tab_donasi:
        # FORM DONASI - INTEGRASI SMART CONTRACT
        # ==========================================

        st.divider()

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



        st.success("Blockchain Hardhat berhasil terhubung!")

        alamat_pengelola = kontrak.functions.pengelola().call()
    
    
        # ==========================================
    with tab_kelola:
        # PENDAFTARAN ALAMAT PENGAWAS
        # ==========================================

        st.divider()
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
    with tab_kelola:
        # PENGELOLAAN DONASI
        # ==========================================

        st.divider()
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
        # FORM PENYALURAN DONASI
        # ==========================================

        st.divider()
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
    with tab_verifikasi:
        # FORM VERIFIKASI DONASI
        # ==========================================

        st.divider()
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
    with tab_dashboard:
        # RINGKASAN DASHBOARD
        # ==========================================

        st.divider()

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


        # ==========================================
    with tab_dashboard:
            # GRAFIK DONASI
            # ==========================================

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

                st.bar_chart(data_grafik)

            else:
                st.info(
                    "Belum ada donasi yang tercatat di smart contract."
                )


            # ==========================================
    with tab_riwayat:
        # RIWAYAT DONASI
        # ==========================================

        st.divider()

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

            tampilan = data_donasi.copy()

            status_map = {
                0: "Menunggu diproses",
                1: "Dikelola",
                2: "Disalurkan",
                3: "Terverifikasi"
            }

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
            
            
            st.divider()
            st.markdown("### 🔎 Detail Data Donasi")

            daftar_id = data_donasi["ID"].astype(int).tolist()

            id_terpilih = st.selectbox(
                "Pilih ID Donasi untuk melihat detail",
                options=daftar_id,
                key="detail_donasi_id"
            )

            if id_terpilih is not None:

                detail = kontrak.functions.getDonation(
                    int(id_terpilih)
                ).call()

                status_detail = {
                    0: "Menunggu diproses",
                    1: "Dikelola",
                    2: "Disalurkan",
                    3: "Terverifikasi"
                }

                st.markdown("#### 📋 Informasi Donasi")

                col1, col2 = st.columns(2)

                with col1:
                    st.write("**ID Donasi**")
                    st.info(str(detail[0]))

                    st.write("**ID Kampanye**")
                    st.info(detail[1])

                    st.write("**Nama Donatur**")
                    st.info(detail[2])

                    st.write("**Alamat Wallet Donatur**")
                    st.code(detail[3])

                with col2:
                    st.write("**Nominal Donasi**")
                    st.info(
                        "Rp " + f"{int(detail[4]):,}".replace(",", ".")
                    )

                    st.write("**Tujuan Penggunaan**")
                    st.info(detail[5] if detail[5] else "Belum ditentukan")

                    st.write("**Status Donasi**")
                    st.success(
                        status_detail.get(
                            int(detail[6]),
                            "Tidak diketahui"
                        )
                    )

                    st.write("**Waktu Pencatatan**")
                    st.info(
                        datetime.fromtimestamp(
                            int(detail[7])
                        ).strftime("%d-%m-%Y %H:%M:%S")
                        if int(detail[7]) > 0 else "-"
                    )


        else:

            st.info(
                "Riwayat donasi masih kosong. "
                "Data akan tampil setelah catatan donasi "
                "tersimpan pada smart contract."
            )


        # ==========================================
    with tab_blockchain:
        # INFORMASI BLOCKCHAIN
        # ==========================================

        st.divider()

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
