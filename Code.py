import pwinput

users = {
    "admin": {"password": "admin123", "role": "admin"},
    "budi": {"password": "user123", "role": "user"},
}
JENIS_SERVIS = {
    1: {"nama": "Ganti Oli Mesin", "jarak_km": 3000, "jarak_bulan": 3},
    2: {"nama": "Servis Rem", "jarak_km": 10000, "jarak_bulan": 12},
    3: {"nama": "Ganti Ban", "jarak_km": 30000, "jarak_bulan": 24},
    4: {"nama": "Servis Berkala", "jarak_km": 10000, "jarak_bulan": 6},
    5: {"nama": "Ganti Aki", "jarak_km": 20000, "jarak_bulan": 24},
    6: {"nama": "Lainnya (isi manual)", "jarak_km": None, "jarak_bulan": None},
}

riwayat_servis = {}


def buat_id_baru():
    if len(riwayat_servis) == 0:
        return 1
    id_terbesar = 0
    for id_servis in riwayat_servis:
        if id_servis > id_terbesar:
            id_terbesar = id_servis
    return id_terbesar + 1


def tambah_bulan(tgl, bulan):
    """tgl berupa tuple (hari, bulan, tahun). Return tuple baru."""
    total = tgl[1] - 1 + bulan
    tahun = tgl[2] + total // 12
    bulan_baru = total % 12 + 1
    hari = tgl[0]
    if hari > 28:
        hari = 28  # dibatasi 28 agar tanggal selalu valid di semua bulan
    return (hari, bulan_baru, tahun)


def hitung_jadwal(data):
    """Hitung KM & tanggal servis berikutnya dari jarak jenis servis."""
    if data["jarak_km"] is None or data["jarak_bulan"] is None:
        data["km_berikutnya"] = None
        data["tanggal_berikutnya"] = None
    else:
        data["km_berikutnya"] = data["km"] + data["jarak_km"]
        data["tanggal_berikutnya"] = tambah_bulan(data["tanggal"], data["jarak_bulan"])


def buat_record(kendaraan, jenis, km, tanggal, dicatat_oleh):
    data = {
        "kendaraan": kendaraan,
        "jenis": jenis["nama"],
        "jarak_km": jenis["jarak_km"],
        "jarak_bulan": jenis["jarak_bulan"],
        "km": km,
        "tanggal": tanggal,
        "dicatat_oleh": dicatat_oleh,
    }
    hitung_jadwal(data)
    return data


def isi_data_awal():
    id1 = buat_id_baru()
    riwayat_servis[id1] = buat_record("Kawasaki ZX25R - KU 47 HA", JENIS_SERVIS[1],
                                      12000, (12, 1, 2026), "admin")
    id2 = buat_id_baru()
    riwayat_servis[id2] = buat_record("Porsche 911 GT3 - KU 67 HA", JENIS_SERVIS[2],
                                      45000, (20, 2, 2026), "admin")


def format_tanggal(tgl):
    """tgl berupa tuple (hari, bulan, tahun) -> teks DD-MM-YYYY."""
    hari = str(tgl[0])
    bulan = str(tgl[1])
    if tgl[0] < 10:
        hari = "0" + hari
    if tgl[1] < 10:
        bulan = "0" + bulan
    return hari + "-" + bulan + "-" + str(tgl[2])


def format_km(angka):
    return f"{angka:,}".replace(",", ".") + " KM"


def daftar_kendaraan():
    return sorted(set(d["kendaraan"] for d in riwayat_servis.values()))


def km_terakhir(kendaraan):
    km_tertinggi = 0
    for data in riwayat_servis.values():
        if data["kendaraan"] == kendaraan and data["km"] > km_tertinggi:
            km_tertinggi = data["km"]
    return km_tertinggi


# =====================================================
# FUNCTION VALIDASI INPUT
# =====================================================
def ke_angka(teks):
    """Ubah teks jadi angka bulat. Return None kalau bukan angka."""
    try:
        return int(teks)
    except ValueError:
        return None


def input_teks(label, boleh_kosong=False):
    """Minta teks. Jika boleh_kosong=True, Enter kosong mengembalikan None."""
    while True:
        nilai = input(label).strip()
        if nilai == "":
            if boleh_kosong:
                return None
            print("Input tidak boleh kosong!")
        else:
            return nilai


def input_password(label):
    while True:
        nilai = pwinput.pwinput(label)
        if nilai == "":
            print("Password tidak boleh kosong!")
        else:
            return nilai


def input_km(label, batas_bawah=1, boleh_kosong=False):
    """Return int. Tidak boleh huruf, 0/negatif, atau kurang dari 'batas_bawah'."""
    if batas_bawah < 1:
        batas_bawah = 1
    while True:
        nilai = input(label).strip()
        if nilai == "" and boleh_kosong:
            return None
        angka = ke_angka(nilai)
        if nilai == "":
            print("Kilometer tidak boleh kosong!")
        elif angka is None:
            print("Kilometer harus berupa angka bulat positif!")
        elif angka < batas_bawah:
            print("Kilometer tidak boleh kurang dari", format_km(batas_bawah) + "!")
        else:
            return angka


def cek_tanggal(teks):
    """Cek format DD-MM-YYYY & apakah tanggalnya benar-benar ada. Return tuple (hari, bulan, tahun) atau None."""
    if len(teks) != 10 or teks[2] != "-" or teks[5] != "-":
        return None
    hari = ke_angka(teks[0:2])
    bulan = ke_angka(teks[3:5])
    tahun = ke_angka(teks[6:10])
    if hari is None or bulan is None or tahun is None:
        return None
    if tahun < 2000 or tahun > 2100 or bulan < 1 or bulan > 12 or hari < 1:
        return None
    jumlah_hari = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if tahun % 4 == 0 and (tahun % 100 != 0 or tahun % 400 == 0):
        jumlah_hari[1] = 29  # tahun kabisat
    if hari > jumlah_hari[bulan - 1]:
        return None
    return (hari, bulan, tahun)


def input_tanggal(label, boleh_kosong=False):
    """Return tuple (hari, bulan, tahun). Tidak boleh kosong / format salah / tanggal tidak ada."""
    while True:
        nilai = input(label).strip()
        if nilai == "":
            if boleh_kosong:
                return None
            print("Tanggal tidak boleh kosong!")
        else:
            tgl = cek_tanggal(nilai)
            if tgl is None:
                print("Format/tanggal tidak valid! Gunakan DD-MM-YYYY (contoh 25-03-2026).")
            else:
                return tgl


def pilih_kendaraan():
    """Pilih dari daftar kendaraan yang sudah ada, atau 0 untuk kendaraan baru."""
    while True:
        daftar = daftar_kendaraan()
        print("\nPilih kendaraan:")
        nomor = 1
        for nama in daftar:
            print(nomor, ".", nama)
            nomor = nomor + 1
        print("0 . Kendaraan baru")
        pilihan = input("Pilihan: ").strip()
        angka = ke_angka(pilihan)
        if pilihan == "0":
            return input_teks("Nama/Plat Kendaraan baru : ")
        elif angka is not None and 1 <= angka <= len(daftar):
            return daftar[angka - 1]
        else:
            print("Pilihan tidak valid!")


def pilih_jenis(boleh_kosong=False):
    """Return dict jenis servis (nama + jarak servis) atau None jika dikosongkan."""
    while True:
        print("\nPilih jenis servis:")
        for no, info in JENIS_SERVIS.items():
            print(no, ".", info["nama"])
        pilihan = input("Pilihan: ").strip()
        if pilihan == "" and boleh_kosong:
            return None
        angka = ke_angka(pilihan)
        if angka in JENIS_SERVIS:
            jenis = dict(JENIS_SERVIS[angka])
            if angka == 6:
                jenis["nama"] = input_teks("Nama jenis servis : ")
            return jenis
        print("Pilihan tidak valid!")

def register():
    print("\n--- REGISTER AKUN BARU (ROLE: USER) ---")
    username = input_teks("Username baru : ")
    if " " in username or len(username) < 3:
        print("Username minimal 3 karakter dan tanpa spasi!")
        return
    if username in users:
        print("Username sudah dipakai!")
        return
    password = input_password("Password baru : ")
    if len(password) < 6:
        print("Password minimal 6 karakter!")
        return
    users[username] = {"password": password, "role": "user"}
    print("Registrasi berhasil! Silakan login.")


def login():
    """Return (username, role) jika berhasil, None jika gagal 3x."""
    print("\n--- LOGIN ---")
    percobaan = 0
    while percobaan < 3:
        username = input_teks("Username : ")
        password = input_password("Password : ")
        if username in users and users[username]["password"] == password:
            print("\nLogin berhasil! Selamat datang,", username,
                  "(" + users[username]["role"] + ")")
            return username, users[username]["role"]
        percobaan += 1
        print("Username/password salah! Sisa percobaan:", 3 - percobaan)
    print("Login gagal 3 kali. Kembali ke menu awal.")
    return None

def tampil_riwayat():
    print("\n--- DAFTAR RIWAYAT SERVIS ---")
    if len(riwayat_servis) == 0:
        print("Belum ada data servis yang tersimpan.")
        return
    for id_servis in sorted(riwayat_servis.keys()):
        data = riwayat_servis[id_servis]
        print("ID", id_servis)
        print("   Kendaraan   :", data["kendaraan"])
        print("   Jenis Servis:", data["jenis"])
        print("   Kilometer   :", format_km(data["km"]))
        print("   Tanggal     :", format_tanggal(data["tanggal"]))
        if data["km_berikutnya"] is not None:
            print("   Servis Lagi :", format_km(data["km_berikutnya"]), "atau",
                  format_tanggal(data["tanggal_berikutnya"]))
        print("   Dicatat oleh:", data["dicatat_oleh"])
        print("-----------------------------------")


def tambah_servis(username):
    print("\n--- TAMBAH CATATAN SERVIS ---")
    kendaraan = pilih_kendaraan()
    jenis = pilih_jenis()
    terakhir = km_terakhir(kendaraan)
    if terakhir > 0:
        print("\n(KM terakhir", kendaraan, ":", format_km(terakhir) + ")")
    km = input_km("Kilometer Kendaraan  : ", terakhir)
    tanggal = input_tanggal("Tanggal DD-MM-YYYY    : ")

    id_baru = buat_id_baru()
    riwayat_servis[id_baru] = buat_record(kendaraan, jenis, km, tanggal, username)
    print("\nData servis berhasil ditambahkan dengan ID", id_baru)
    data = riwayat_servis[id_baru]
    if data["km_berikutnya"] is not None:
        print("Servis berikutnya dijadwalkan otomatis:", format_km(data["km_berikutnya"]),
              "atau", format_tanggal(data["tanggal_berikutnya"]))


def pilih_id(aksi):
    if len(riwayat_servis) == 0:
        print("\nTidak ada data untuk di" + aksi + ".")
        return None
    tampil_riwayat()
    pilihan = input("Masukkan ID catatan yang mau di" + aksi + ": ").strip()
    id_servis = ke_angka(pilihan)
    if id_servis is None:
        print("ID harus berupa angka!")
        return None
    if id_servis not in riwayat_servis:
        print("ID tidak ditemukan!")
        return None
    return id_servis


def ubah_servis():
    print("\n--- UBAH CATATAN SERVIS ---")
    id_servis = pilih_id("ubah")
    if id_servis is None:
        return
    data = riwayat_servis[id_servis]
    print("\n(Kosongkan lalu Enter jika tidak ingin mengubah bagian tersebut)")
    kendaraan = input_teks("Nama/Plat Baru [" + data["kendaraan"] + "] : ", True)
    jenis = pilih_jenis(True)
    km = input_km("Kilometer Baru [" + str(data["km"]) + "] : ", 1, True)
    tanggal = input_tanggal("Tanggal Baru [" + format_tanggal(data["tanggal"]) + "] : ", True)

    if kendaraan is not None:
        data["kendaraan"] = kendaraan
    if jenis is not None:
        data["jenis"] = jenis["nama"]
        data["jarak_km"] = jenis["jarak_km"]
        data["jarak_bulan"] = jenis["jarak_bulan"]
    if km is not None:
        data["km"] = km
    if tanggal is not None:
        data["tanggal"] = tanggal
    hitung_jadwal(data) 
    print("\nData servis berhasil diperbarui!")


def hapus_servis():
    print("\n--- HAPUS CATATAN SERVIS ---")
    id_servis = pilih_id("hapus")
    if id_servis is None:
        return
    yakin = input("Yakin hapus ID " + str(id_servis) + "? (y/n): ").strip().lower()
    if yakin == "y":
        del riwayat_servis[id_servis]
        print("\nData servis berhasil dihapus!")
    elif yakin == "n":
        print("\nPenghapusan dibatalkan.")
    else:
        print("\nInput tidak valid, penghapusan dibatalkan.")

def menu_admin(username):
    while True:
        print("\n=========================================")
        print("   MENU ADMIN -", username)
        print("=========================================")
        print("1. Tampilkan Seluruh Riwayat Servis")
        print("2. Tambah Catatan Servis Baru")
        print("3. Ubah Catatan Servis")
        print("4. Hapus Catatan Servis")
        print("5. Logout")
        pilihan = input("Pilih menu (1-5): ").strip()

        if pilihan == "1":
            tampil_riwayat()
        elif pilihan == "2":
            tambah_servis(username)
        elif pilihan == "3":
            ubah_servis()
        elif pilihan == "4":
            hapus_servis()
        elif pilihan == "5":
            print("\nAnda telah logout.")
            break
        else:
            print("\nPilihan menu tidak valid! Masukkan angka 1 sampai 5.")


def menu_user(username):
    while True:
        print("\n=========================================")
        print("   MENU USER -", username)
        print("=========================================")
        print("1. Tampilkan Seluruh Riwayat Servis")
        print("2. Tambah Catatan Servis Baru")
        print("3. Logout")
        pilihan = input("Pilih menu (1-3): ").strip()

        if pilihan == "1":
            tampil_riwayat()
        elif pilihan == "2":
            tambah_servis(username)
        elif pilihan == "3":
            print("\nAnda telah logout.")
            break
        else:
            print("\nPilihan menu tidak valid! Masukkan angka 1 sampai 3.")

def main():
    isi_data_awal()
    while True:
        print("\n=========================================")
        print("   JURNAL SERVIS KENDARAAN PRIBADI       ")
        print("=========================================")
        print("1. Login")
        print("2. Register")
        print("3. Keluar")
        pilihan = input("Pilih menu (1-3): ").strip()

        if pilihan == "1":
            hasil = login()
            if hasil is not None:
                username, role = hasil
                if role == "admin":
                    menu_admin(username)
                elif role == "user":
                    menu_user(username)
        elif pilihan == "2":
            register()
        elif pilihan == "3":
            print("\nTerima kasih telah menggunakan sistem Jurnal Servis Kendaraan!")
            break
        else:
            print("\nPilihan menu tidak valid! Masukkan angka 1 sampai 3.")


main()
