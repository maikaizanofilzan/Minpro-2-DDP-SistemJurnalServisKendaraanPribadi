Minpro-2-DDP-JurnalServisKendaraan
1. Deskripsi Singkat Program

Program terminal Python untuk mencatat riwayat servis kendaraan pribadi, lanjutan dari Mini Project 1. Memakai dictionary, function, validasi dengan conditional statement, dan library pwinput (password tampil ***).

| Role  | Hak akses |
|-------|-----------|
| Admin | CRUD lengkap |
| User  | Lihat dan tambah |

Jalankan: pip install pwinput lalu python jurnal_servis.py
Akun bawaan: admin / admin123 dan budi / user123. Akun baru lewat Register berperan sebagai User.

2. Flowchart

<img width="897" height="782" alt="Screenshot 2026-10-05 163509" src="https://github.com/user-attachments/assets/5d29199f-eb87-434b-8ade-131c7ad40fb1" />

Program dimulai dari menu awal (Login, Register, Keluar). Login dicocokkan dengan dictionary `users` dengan 3 kali kesempatan, lalu program mengecek role untuk membuka menu admin atau menu user. Tiap fitur (lihat, tambah, ubah, hapus) memvalidasi input dan kembali ke menu role sampai Logout. Halaman 2 dan 3 merinci validasi Tambah, Ubah, Hapus, Register, Login, dan Lihat.

3. Dokumentasi Program & Output

a. Menu Awal <img width="474" height="399" alt="Screenshot 2026-10-05 160356" src="https://github.com/user-attachments/assets/5adad61c-2263-49b9-a5f9-e065f53f655e" />
 Pilihan selain 1-3 ditolak.
 
b. Register <img width="414" height="858" alt="Screenshot 2026-10-05 160619" src="https://github.com/user-attachments/assets/549ff0c4-1848-4e0b-a77a-8bc34b7e0ae8" />
Username dan password dicek syaratnya.

c. Login <img width="421" height="590" alt="Screenshot 2026-10-05 160732" src="https://github.com/user-attachments/assets/dcd08186-aadf-4881-9c9f-78494de12320" />
Password salah menampilkan sisa percobaan.

d. Menu Admin  <img width="421" height="590" alt="Screenshot 2026-10-05 160732" src="https://github.com/user-attachments/assets/1e668b4b-bfb6-4875-8099-a7f5509b2ba9" />
Lima pilihan termasuk ubah dan hapus. 

e. Menu User <img width="438" height="482" alt="Screenshot 2026-10-05 161619" src="https://github.com/user-attachments/assets/6d25e0b4-98a7-456e-b8ef-66b6ab6ce6db" />
<img width="602" height="448" alt="Screenshot 2026-10-05 161759" src="https://github.com/user-attachments/assets/f9b9d3ab-8cb6-44e9-89e7-94459df2079d" />
Hanya lihat, tambah, logout. 

f. Lihat <img width="412" height="596" alt="Screenshot 2026-10-05 160754" src="https://github.com/user-attachments/assets/b3b46857-71d5-449a-8577-cf041f6e9173" />
Menampilkan semua catatan per ID.

g. Tambah <img width="604" height="759" alt="Screenshot 2026-10-05 161036" src="https://github.com/user-attachments/assets/f25060ed-e045-47c9-8a72-6d174b7e1dec" />
KM dan tanggal divalidasi.

h. Ubah <img width="683" height="346" alt="Screenshot 2026-10-05 161313" src="https://github.com/user-attachments/assets/b33ddb5e-a14e-4438-a174-d9b3e7cc2776" />
Pilih lewat ID, kosongkan bagian yang tidak diubah.

i. Hapus <img width="451" height="835" alt="Screenshot 2026-10-05 161411" src="https://github.com/user-attachments/assets/2a667777-8039-417a-883b-ff8fde57e43b" />
<img width="435" height="732" alt="Screenshot 2026-10-05 161520" src="https://github.com/user-attachments/assets/6391b598-ad0c-4117-9f15-89f8fcb3c597" />
Pilih lewat ID dengan konfirmasi y/n.
