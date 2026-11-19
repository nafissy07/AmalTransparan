# 🤝 AmalTransparan

**Transparansi donasi, membangun kepercayaan.**

## Tentang proyek

Sering kali orang ragu berdonasi karena tidak tahu ke mana uangnya pergi. Setelah donasi diberikan, donatur jarang mendapat kabar apakah dana benar-benar sampai kepada yang membutuhkan. AmalTransparan dibuat untuk menjawab masalah itu.

AmalTransparan adalah aplikasi web pencatat donasi yang memanfaatkan teknologi blockchain. Setiap langkah perjalanan sebuah donasi, mulai dari dicatat, dikelola, disalurkan, sampai diverifikasi, disimpan di smart contract. Data di blockchain tidak bisa diubah diam-diam, sehingga siapa pun dapat memeriksa riwayat donasi kapan saja tanpa harus percaya begitu saja kepada pengelola.

Proyek ini dikembangkan sebagai tugas mata kuliah Blockchain. Aplikasinya berjalan di jaringan lokal Hardhat, jadi cocok untuk pembelajaran dan demonstrasi, bukan untuk menampung dana sungguhan.

## Bagaimana cara kerjanya

Sebuah donasi melewati empat tahap.

Pertama, **donatur mencatat donasi**. Ia mengisi ID kampanye, namanya, dan nominal donasi, lalu mengonfirmasi transaksi lewat MetaMask. Pada tahap ini smart contract menyimpan data donasi dan menerbitkan NFT sebagai bukti pencatatan.

Kedua, **pengelola mengelola donasi**. Pengelola menuliskan tujuan penggunaan dana, misalnya pembelian sembako untuk korban bencana, sehingga arah penggunaan dana tercatat secara terbuka.

Ketiga, **pengelola menyalurkan bantuan**. Pengelola mencatat siapa penerima bantuan dan berapa jumlahnya. Jumlah yang disalurkan tidak boleh melebihi saldo kampanye.

Keempat, **pengawas memverifikasi**. Pengawas adalah pihak terpisah dari pengelola. Ia memeriksa dan memverifikasi donasi yang sudah disalurkan, sehingga ada pihak independen yang ikut menjaga kejujuran proses.

Status setiap donasi dapat dilihat kapan saja, dari "Menunggu diproses" sampai "Terverifikasi".

## Siapa saja yang terlibat

Aplikasi mengenali tiga peran berdasarkan alamat wallet yang terhubung.

**Pengelola** adalah akun yang melakukan deploy smart contract. Pengelola berhak mengelola donasi, menyalurkan bantuan, dan mendaftarkan pengawas.

**Pengawas** adalah alamat yang didaftarkan oleh pengelola. Tugasnya hanya satu, yaitu memverifikasi donasi yang sudah disalurkan.

**Donatur atau pengguna umum** adalah siapa saja selain keduanya. Mereka dapat mencatat donasi dan melihat seluruh data yang ada, karena semua informasi bersifat terbuka.

## Apa yang bisa dilakukan di aplikasi

Aplikasi terdiri dari beberapa halaman yang dipilih lewat menu di bagian atas.

**Beranda** memberi gambaran cepat tentang kondisi platform: total donasi yang tercatat, jumlah kampanye, dan jumlah donasi yang sudah terverifikasi. Halaman ini juga menjelaskan perjalanan sebuah donasi, menampilkan grafik dana per kampanye, dan daftar aktivitas terbaru.

**Kampanye** adalah tempat untuk memantau setiap kampanye. Setiap kampanye tampil sebagai kartu yang berisi total dana, jumlah donasi dan donatur, serta bar yang menunjukkan berapa donasi yang masih menunggu, sedang dikelola, sudah disalurkan, atau sudah terverifikasi. Kampanye dapat dicari berdasarkan nama, disaring menurut tahapnya, dan diurutkan berdasarkan dana terbesar, yang terbaru, atau progres tertinggi. Dari kartu, pengguna dapat membuka halaman detail yang memuat saldo kampanye, posisi dana di tiap tahap, grafik perkembangan dana, daftar seluruh donasi yang dapat diunduh sebagai CSV, peringkat donatur, serta linimasa aktivitas lengkap dengan nomor blok dan hash transaksi. Dari halaman detail, pengguna juga bisa langsung berdonasi ke kampanye tersebut.

**Donasi, Kelola, Salurkan, dan Verifikasi** adalah empat halaman transaksi yang sesuai dengan tahapan di atas. Setiap halaman memeriksa lebih dulu apakah wallet sudah terhubung, apakah jaringannya benar, dan apakah akun yang dipakai memang berhak melakukan aksi tersebut.

**Pengawas** dipakai pengelola untuk mendaftarkan alamat wallet pengawas.

**Riwayat** menampilkan semua catatan donasi dalam satu tabel. Pengguna dapat mencari berdasarkan kampanye, nama donatur, alamat wallet, atau tujuan penggunaan, menyaring berdasarkan status, dan mengunduh hasilnya.

**Detail Donasi** menunjukkan data lengkap satu donasi, termasuk tahapan yang sudah dilalui, waktu pencatatan, nomor blok, dan hash transaksinya, sehingga setiap donasi bisa dilacak sampai ke blockchain.

**Wallet** dipakai untuk menghubungkan MetaMask. Setelah terhubung, halaman ini menampilkan alamat, saldo ETH, jaringan yang dipakai, dan peran akun beserta hak aksesnya.

**Info** menampilkan keterangan jaringan, jumlah blok, dan alamat smart contract yang digunakan.

## Teknologi yang dipakai

Antarmuka dibuat dengan **Streamlit** sehingga seluruh aplikasi ditulis dalam Python. Jaringan blockchain lokal dan proses deploy memakai **Hardhat**, sedangkan logika donasi ditulis sebagai smart contract **Solidity**. Aplikasi membaca data kontrak lewat **web3.py**, dan transaksi ditandatangani pengguna melalui **MetaMask**. Jembatan antara Streamlit dan MetaMask di browser memakai pustaka **streamlit-js-eval**.

## Penjelasan kode

Seluruh antarmuka ada dalam satu file, `app.py`, dan dibaca dari atas ke bawah. Streamlit menjalankan ulang file ini setiap kali pengguna menekan tombol atau mengganti menu, jadi urutan penulisannya penting. Bagian ini menjelaskan isi file tersebut supaya mudah dipelajari dan dikembangkan.

### Susunan `app.py`

File ini terbagi menjadi beberapa blok berurutan:

1. **Konfigurasi halaman dan CSS.** `st.set_page_config` mengatur judul tab, lalu satu blok CSS besar mengatur seluruh tampilan. Warna, radius sudut, dan warna status disimpan sebagai variabel di `:root` (misalnya `--brand` dan `--s0` sampai `--s3`) supaya mengganti tema cukup mengubah variabel itu.
2. **Fungsi bantu tampilan.** Fungsi kecil yang dipakai berulang di semua halaman, seperti `rupiah()` untuk format `Rp 1.500.000`, `waktu_fmt()` untuk tanggal, `pendek()` untuk menyingkat alamat wallet, `chip_status()` untuk label status berwarna, dan `bar_tahapan()` untuk bar progres bertumpuk.
3. **Bar merek dan navigasi.** Menu dibuat dari satu `st.radio` horizontal dengan key `menu_fitur`, lalu dipercantik lewat CSS menjadi tab.
4. **Integrasi MetaMask.** Menghubungkan wallet dan menyimpan hasilnya di `st.session_state`.
5. **Koneksi kontrak dan pembacaan data.** Mengambil semua donasi dari blockchain menjadi satu tabel `data_donasi`.
6. **Halaman-halaman.** Rangkaian `if / elif menu_pilihan == ...`, satu cabang untuk setiap menu.
7. **Footer.**

### Menghubungkan MetaMask dari Streamlit

Streamlit berjalan di server (Python), sedangkan MetaMask hidup di browser. Karena itu aplikasi memakai `streamlit_js_eval` untuk menjalankan JavaScript di browser dan mengambil hasilnya kembali ke Python. Pola dasarnya:

```python
javascript = """
(async () => {
    const provider = window.parent.ethereum || window.ethereum;
    const accounts = await provider.request({ method: "eth_requestAccounts" });
    ...
    return JSON.stringify({ account: accounts[0], chainId: ..., balanceEth: ... });
})()
"""

hasil = streamlit_js_eval(js_expressions=javascript, want_output=True, key="AMALTRANSPARAN_METAMASK")
```

Hasilnya berupa teks JSON yang diurai lalu disimpan di `st.session_state.wallet_data`, sehingga semua halaman bisa memakainya. Agar JavaScript hanya berjalan saat tombol ditekan, kode memakai penghitung `wallet_request_id`. Penghitung itu naik setiap tombol Hubungkan MetaMask diklik, dan JavaScript baru dikirim ketika nilainya lebih dari nol.

### Alur satu transaksi

Semua halaman transaksi (Donasi, Kelola, Salurkan, Verifikasi, Pengawas) memakai pola yang sama:

1. **Validasi** isian form, kondisi wallet, jaringan (harus 31337), dan hak akses akun.
2. **Menyiapkan calldata.** Python menyusun data pemanggilan fungsi kontrak, misalnya:

   ```python
   calldata = kontrak.functions.createDonation(
       campaign_id, nama_donatur, int(nominal_donasi), metadata_uri
   )._encode_transaction_data()
   ```

3. **Mengirim lewat MetaMask.** Calldata dimasukkan ke JavaScript yang memanggil `eth_sendTransaction`. Pengguna melihat jendela konfirmasi MetaMask dan menandatangani di sana.
4. **Menunggu konfirmasi.** Hash transaksi yang dikembalikan dipakai oleh `w3.eth.wait_for_transaction_receipt(...)`.
5. **Menampilkan hasil.** Bila `receipt.status == 1`, transaksi berhasil dan halaman menampilkan hash serta nomor blok. Beberapa halaman lalu memanggil `st.rerun()` agar data langsung ikut diperbarui.

Aplikasi tidak pernah menyimpan atau meminta private key. Penandatanganan seluruhnya terjadi di MetaMask.

### Membaca data dari blockchain

Daftar donasi dibangun dari event `DonationCreated` milik kontrak:

1. `event_donasi.get_logs(from_block=0, to_block="latest")` mengambil semua event, lalu ID donasi dikumpulkan dari `log["args"]["donationId"]`.
2. Untuk setiap ID, `kontrak.functions.getDonation(id).call()` membaca data lengkapnya.
3. Hasilnya dikumpulkan menjadi `pandas.DataFrame` bernama `data_donasi`, dengan kolom `ID`, `Kampanye`, `Donatur`, `Alamat Donatur`, `Jumlah`, `Tujuan`, `Status`, `Timestamp`, `Block`, dan `Tx Hash`.

Nomor blok dan hash transaksi diambil dari log event, bukan dari fungsi `getDonation`. Koneksi ke kontrak dibungkus `@st.cache_resource` supaya tidak dibuat ulang setiap halaman dimuat. Tombol **Segarkan Data** di halaman Info menghapus cache itu.

### Pengecekan hak akses

Hak akses dicek dengan membandingkan alamat wallet yang terhubung dengan alamat di kontrak, dalam huruf kecil agar tidak terpengaruh perbedaan huruf besar dan kecil:

```python
wallet_kelola["account"].lower() != alamat_pengelola.lower()
```

Alamat pengelola dibaca dari `kontrak.functions.pengelola().call()` dan alamat pengawas dari `kontrak.functions.pengawas().call()`. Pengecekan di aplikasi ini hanya untuk memberi pesan yang jelas kepada pengguna. Penjaga sebenarnya tetap smart contract, yang akan menolak transaksi dari akun yang tidak berhak.

### Pengolahan data kampanye

Halaman Kampanye mengelompokkan `data_donasi` berdasarkan nama kampanye dengan `groupby("Kampanye")`. Untuk setiap kampanye dihitung dana masuk, jumlah donasi, jumlah donatur unik (dari alamat wallet), jumlah donasi di tiap status, progres penyaluran, dan saldo dari `campaignBalance`. Tahap kampanye ditentukan sederhana: semua donasi terverifikasi berarti selesai, ada yang sudah disalurkan berarti sedang berjalan, selain itu berarti menunggu.

Perpindahan antara daftar dan detail kampanye memakai `st.session_state.kampanye_aktif`. Tombol kartu memanggil fungsi callback:

- `buka_kampanye(nama)` mengisi kampanye aktif sehingga halaman detail tampil.
- `tutup_kampanye()` mengosongkannya sehingga kembali ke daftar.
- `donasi_ke_kampanye(nama)` mengisi `prefill_kampanye` lalu memindahkan menu ke Donasi, sehingga ID kampanye di form sudah terisi.

Callback dipakai, bukan `if st.button(...)`, karena callback berjalan sebelum halaman digambar ulang. Dengan begitu perubahan menu dan kampanye langsung terlihat pada tampilan berikutnya.

### Tampilan dan keamanan teks

Elemen HTML kustom (kartu kampanye, chip status, hero, linimasa) dibuat lewat fungsi `h()`, yang menggabungkan HTML menjadi satu baris supaya tidak dibaca sebagai blok kode oleh markdown. Nama donatur dan nama kampanye berasal dari input pengguna, jadi selalu dilewatkan ke `html.escape()` sebelum dimasukkan ke HTML. Tanpa itu, seseorang bisa menyisipkan kode HTML lewat nama donatur.

### Menambah menu atau fitur baru

Untuk menambahkan satu halaman baru:

1. Tambahkan konstanta menu, misalnya `M_LAPORAN = "Laporan"`.
2. Masukkan konstanta itu ke daftar pilihan `st.radio` dengan urutan yang diinginkan.
3. Tambahkan cabang `elif menu_pilihan == M_LAPORAN:` di bagian halaman, sebelum blok `except`.
4. Bila halaman itu mengirim transaksi, tambahkan juga ke `MENU_TRANSAKSI` agar bar status wallet ikut tampil.

Untuk fitur yang butuh data baru dari kontrak, tambahkan fungsi di smart contract, perbarui ABI yang dipakai `blockchain_connector.py`, lalu panggil lewat `kontrak.functions.namaFungsi(...)`.

### Hal yang perlu diperhatikan

- Kolom alamat di form **Pengawas** memiliki alamat bawaan. Ganti dengan alamat akun pengawas milikmu sendiri.
- File `blockchain_connector.py` diharapkan mengembalikan dua nilai, objek `w3` dan objek `kontrak`. Alamat kontrak di dalamnya harus diperbarui setiap kali kontrak di-deploy ulang.
- Kode memakai `use_container_width` dan `st.column_config.ProgressColumn`, yang membutuhkan Streamlit versi yang cukup baru.

## Cara menjalankan

Sebelum mulai, siapkan Python 3.10 atau lebih baru, Node.js 18 atau lebih baru, dan browser Chrome dengan ekstensi MetaMask.

Pasang dependensi Python dan Node terlebih dahulu:

```bash
pip install streamlit pandas web3 streamlit-js-eval
npm install
```

Lalu jalankan tiga hal secara berurutan, masing-masing di terminal sendiri.

Jalankan jaringan blockchain lokal dan biarkan terminal ini tetap terbuka:

```bash
npx hardhat node
```

Deploy smart contract ke jaringan tersebut. Akun yang dipakai saat deploy otomatis menjadi pengelola. Catat alamat kontrak yang muncul dan pastikan `blockchain_connector.py` memakai alamat itu. Sesuaikan nama skrip dengan yang ada di proyekmu:

```bash
npx hardhat run scripts/deploy.js --network localhost
```

Terakhir, jalankan aplikasinya, yang akan terbuka di `http://localhost:8501`:

```bash
streamlit run app.py
```

## Menyiapkan MetaMask

Tambahkan jaringan baru di MetaMask secara manual dengan nama **Hardhat Local**, RPC URL `http://127.0.0.1:8545`, Chain ID `31337`, dan simbol mata uang `ETH`.

Setelah itu impor beberapa akun uji coba dari daftar yang dicetak oleh `npx hardhat node`, dengan memakai private key-nya. Pakai akun yang melakukan deploy sebagai pengelola, satu akun lain sebagai pengawas, dan akun lainnya sebagai donatur. Terakhir, buka menu **Wallet** di aplikasi dan klik **Hubungkan MetaMask**.

Private key bawaan Hardhat bersifat publik, jadi gunakan hanya di jaringan lokal dan jangan pernah mengirim dana asli ke akun tersebut.

## Contoh alur penggunaan

Mulailah sebagai pengelola dengan mendaftarkan alamat pengawas lewat menu **Pengawas**. Lalu, sebagai donatur, buka menu **Donasi** dan catat satu donasi untuk kampanye tertentu. Kembali sebagai pengelola, buka menu **Kelola** untuk menetapkan tujuan penggunaan dana, kemudian menu **Salurkan** untuk mencatat penyaluran kepada penerima. Berpindah ke akun pengawas, buka menu **Verifikasi** untuk memverifikasi penyaluran tersebut. Sepanjang proses, menu **Kampanye** dan **Detail Donasi** akan memperlihatkan perubahan status secara langsung.

## Batasan saat ini

Nominal donasi dicatat sebagai data di smart contract. Kontrak belum memindahkan ETH atau uang sungguhan, jadi angka tersebut bukan bukti transfer.

Kontrak juga belum menyimpan target dana untuk tiap kampanye. Karena itu progres kampanye dihitung dari seberapa banyak donasi yang sudah mencapai tahap penyaluran, bukan dari persentase terhadap target.

Aplikasi hanya dirancang untuk jaringan Hardhat Local dengan Chain ID 31337. Karena node lokal tidak menyimpan data setelah dimatikan, kontrak perlu di-deploy ulang setiap kali node dimulai dari awal.

## Jika ada masalah

Bila muncul pesan bahwa aplikasi tidak dapat terhubung ke smart contract, periksa apakah `npx hardhat node` masih berjalan dan apakah alamat kontrak di `blockchain_connector.py` sama dengan hasil deploy terbaru. Bila MetaMask tidak terdeteksi, buka aplikasi lewat Chrome dengan ekstensi MetaMask aktif. Bila aplikasi meminta pindah jaringan, ganti jaringan MetaMask ke Hardhat Local. Bila transaksi gagal dengan pesan nonce setelah node dimulai ulang, buka pengaturan lanjutan MetaMask dan hapus data aktivitas tab.

## Lisensi

Proyek ini dibuat untuk keperluan pembelajaran. Tambahkan lisensi sesuai kebutuhan.