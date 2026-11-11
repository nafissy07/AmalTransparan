
import json
from pathlib import Path
from web3 import Web3

# Folder utama proyek
BASE_DIR = Path(__file__).resolve().parent

# Alamat jaringan Hardhat lokal
RPC_URL = "http://127.0.0.1:8545"

# Lokasi file deployment dan ABI
DEPLOYMENT_PATH = BASE_DIR / "deployment.json"

ABI_PATH = (
    BASE_DIR
    / "artifacts"
    / "contracts"
    / "AmalTransparan.sol"
    / "AmalTransparan.json"
)


def hubungkan_blockchain():
    """Menghubungkan Python ke blockchain Hardhat."""

    # Periksa file deployment
    if not DEPLOYMENT_PATH.exists():
        raise FileNotFoundError(
            f"File deployment tidak ditemukan: {DEPLOYMENT_PATH}"
        )

    # Baca alamat kontrak dari deployment.json
    with open(DEPLOYMENT_PATH, "r", encoding="utf-8") as file:
        deployment = json.load(file)

    contract_address = Web3.to_checksum_address(
        deployment["address"]
    )

    expected_chain_id = int(deployment["chainId"])

    # Periksa file ABI
    if not ABI_PATH.exists():
        raise FileNotFoundError(
            f"File ABI tidak ditemukan: {ABI_PATH}"
        )

    with open(ABI_PATH, "r", encoding="utf-8") as file:
        data_artifact = json.load(file)

    # Hubungkan ke Hardhat
    w3 = Web3(Web3.HTTPProvider(RPC_URL))

    if not w3.is_connected():
        raise ConnectionError(
            "Blockchain tidak terhubung. Pastikan Hardhat Node berjalan."
        )

    # Pastikan jaringan sesuai
    if w3.eth.chain_id != expected_chain_id:
        raise ValueError(
            f"Chain ID tidak sesuai. "
            f"Seharusnya {expected_chain_id}, "
            f"tetapi terhubung ke {w3.eth.chain_id}."
        )

    # Pastikan smart contract tersedia
    if len(w3.eth.get_code(contract_address)) == 0:
        raise ValueError(
            "Smart contract tidak ditemukan pada alamat deployment."
        )

    # Buat objek kontrak
    kontrak = w3.eth.contract(
        address=contract_address,
        abi=data_artifact["abi"]
    )

    return w3, kontrak


def ambil_donasi(donation_id):
    """Mengambil satu data donasi berdasarkan ID."""

    w3, kontrak = hubungkan_blockchain()

    data = kontrak.functions.getDonation(int(donation_id)).call()

    return {
        "id": data[0],
        "campaign_id": data[1],
        "nama_donatur": data[2],
        "alamat_donatur": data[3],
        "jumlah": data[4],
        "tujuan": data[5],
        "status": data[6],
        "timestamp": data[7],
    }


if __name__ == "__main__":
    try:
        w3, kontrak = hubungkan_blockchain()

        print("Koneksi blockchain berhasil!")
        print("Chain ID:", w3.eth.chain_id)
        print("Alamat kontrak:", kontrak.address)
        print("Alamat pengelola:", kontrak.functions.pengelola().call())

    except Exception as error:
        print("Terjadi kesalahan:", error)
