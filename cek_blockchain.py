import json
from pathlib import Path
from web3 import Web3

# ==========================================
# KONFIGURASI BLOCKCHAIN
# ==========================================

RPC_URL = "http://127.0.0.1:8545"

ALAMAT_KONTRAK = Web3.to_checksum_address(
    "0x5FbDB2315678afecb367f032d93F642f64180aa3"
)

ABI_PATH = (
    Path(__file__).parent
    / "artifacts"
    / "contracts"
    / "AmalTransparan.sol"
    / "AmalTransparan.json"
)


# ==========================================
# MEMBACA ABI LENGKAP
# ==========================================

def baca_abi():
    if not ABI_PATH.exists():
        raise FileNotFoundError(
            f"File ABI tidak ditemukan: {ABI_PATH}\n"
            "Pastikan smart contract sudah dikompilasi."
        )

    with open(ABI_PATH, "r", encoding="utf-8") as file:
        artifact = json.load(file)

    return artifact["abi"]


# ==========================================
# MENGHUBUNGKAN BLOCKCHAIN
# ==========================================

def hubungkan_blockchain():
    w3 = Web3(Web3.HTTPProvider(RPC_URL))

    if not w3.is_connected():
        raise ConnectionError(
            "Blockchain tidak terhubung.\n"
            "Pastikan Hardhat Node sedang berjalan."
        )

    abi = baca_abi()

    kode_kontrak = w3.eth.get_code(ALAMAT_KONTRAK)

    if len(kode_kontrak) == 0:
        raise ValueError(
            "Smart contract tidak ditemukan pada alamat tersebut.\n"
            "Periksa alamat kontrak dan jaringan Hardhat."
        )

    kontrak = w3.eth.contract(
        address=ALAMAT_KONTRAK,
        abi=abi
    )

    return w3, kontrak


# ==========================================
# TES KONEKSI DAN INFORMASI KONTRAK
# ==========================================

def tes_koneksi():
    print("=== TES KONEKSI AMALTRANSPARAN ===")

    w3, kontrak = hubungkan_blockchain()

    print("Status koneksi: BERHASIL")
    print("Chain ID:", w3.eth.chain_id)
    print("Jumlah blok:", w3.eth.block_number)
    print("Alamat kontrak:", ALAMAT_KONTRAK)

    akun = w3.eth.accounts[0]

    saldo = w3.from_wei(
        w3.eth.get_balance(akun),
        "ether"
    )

    print("Akun Hardhat:", akun)
    print("Saldo akun:", saldo, "ETH")

    alamat_pengelola = kontrak.functions.pengelola().call()

    print("Alamat pengelola:", alamat_pengelola)

    return w3, kontrak


# ==========================================
# MEMBUAT DONASI UJI
# ==========================================

def buat_donasi_uji(w3, kontrak):
    print("\n=== TES MEMBUAT DONASI ===")

    # Akun pertama bawaan Hardhat untuk pengujian lokal.
    akun = w3.eth.accounts[0]

    campaign_id = "BANTUAN001"
    nama_donatur = "Donatur Uji"
    jumlah_donasi = 500000
    metadata_uri = ""

    try:
        # Membuat transaksi untuk mencatat donasi.
        transaksi = kontrak.functions.createDonation(
            campaign_id,
            nama_donatur,
            jumlah_donasi,
            metadata_uri
        ).transact({
            "from": akun
        })

        # Menunggu transaksi selesai diproses.
        hasil = w3.eth.wait_for_transaction_receipt(
            transaksi
        )

        print("Hash transaksi:", hasil.transactionHash.hex())
        print("Status transaksi:", hasil.status)

        if hasil.status == 1:
            print("Donasi berhasil dicatat di blockchain!")

            # Membaca event untuk mengetahui ID donasi.
            try:
                event_donasi = kontrak.events.DonationCreated()
                daftar_event = event_donasi.process_receipt(hasil)

                if daftar_event:
                    donation_id = daftar_event[0]["args"]["donationId"]

                    print("ID donasi:", donation_id)

                    # Membaca kembali data donasi dari kontrak.
                    data = kontrak.functions.getDonation(
                        donation_id
                    ).call()

                    print("\n=== DATA DONASI TERCATAT ===")
                    print("ID:", data[0])
                    print("Kampanye:", data[1])
                    print("Nama donatur:", data[2])
                    print("Alamat donatur:", data[3])
                    print("Jumlah:", data[4])
                    print("Tujuan:", data[5])
                    print("Status:", data[6])
                    print("Timestamp:", data[7])

            except Exception as error_event:
                print(
                    "Transaksi berhasil, tetapi detail event "
                    "belum dapat dibaca:",
                    error_event
                )

        else:
            print("Transaksi gagal dicatat.")

    except Exception as error:
        print("Gagal mencatat donasi:", error)


# ==========================================
# PROGRAM UTAMA
# ==========================================

if __name__ == "__main__":
    try:
        w3, kontrak = tes_koneksi()

        # Menjalankan donasi uji satu kali setiap program
        # dijalankan. Jalankan lagi hanya jika memang ingin
        # membuat transaksi uji tambahan.
        jawaban = input(
            "\nApakah ingin mencatat donasi uji sebesar "
            "500000? (y/n): "
        ).strip().lower()

        if jawaban == "y":
            buat_donasi_uji(w3, kontrak)
        else:
            print("Pengujian donasi dilewati.")

    except Exception as error:
        print("\nTerjadi kesalahan:")
        print(error)