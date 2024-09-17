**Proyek: Protein-Ligand Docking Automation**

Proyek ini bertujuan untuk melakukan docking otomatis antara protein dan ligan menggunakan AutoDock. Skrip Python ini mengambil input protein dan ligan, mengunduh dan memproses file PDB, dan kemudian menjalankan docking. Hasilnya mencakup data afinitas dan evaluasi Lipinski untuk setiap ligan.

Struktur Proyek

preparatiopn.py:

Mengambil input reseptor, ligan, dan chain.
Mengunduh file PDB dari PDB server.
Memproses file PDB dan menyiapkan file input untuk AutoDock.
Menjalankan AutoDock untuk mendapatkan afinitas.

screening.py:

Mengonversi file SDF menjadi format PDBQT.
Menggunakan Open Babel untuk menambahkan muatan parsial dan mengoptimalkan geometri.
Menyiapkan file untuk grid map dan docking.
Melakukan docking otomatis menggunakan AutoDock GPU.

affinity.py:

Mengekstrak nilai afinitas dari file .dlg hasil docking.
Menyimpan data afinitas ke dalam file CSV.

lipinski.py:

Mengevaluasi ligan berdasarkan aturan Lipinski.
Menghitung parameter seperti berat molekul, logP, jumlah donor dan akseptor ikatan hidrogen, dan molar refractivity.
Menyimpan hasil evaluasi ke dalam file CSV.
Merged Data:

Menggabungkan data afinitas dan evaluasi Lipinski ke dalam satu file CSV bernama merged_data.csv.

Persyaratan
Python 3.x
RDKit
PubChemPy
Open Babel
AutoDock

Cara Penggunaan

siapkan file sdf yang akan di docking.

Jalankan preparatiopn.py untuk memulai proses docking. masukan kode pdb reseptor, kode ligand dan kode chain.

Jalankan screening.py akan mengonversi dan mempersiapkan file untuk docking.

Jalankan affinity.py akan mengekstrak nilai afinitas dan menyimpannya dalam file CSV.

Jalankan lipinski.py akan mengevaluasi ligan berdasarkan aturan Lipinski dan menyimpannya dalam file CSV.

Hasil gabungan akan disimpan dalam merged_data.csv.

Catatan
Pastikan koneksi internet aktif saat menjalankan preparatiopn.py untuk mengunduh file PDB.
Hasil akhir akan disimpan dalam format CSV yang dapat dianalisis lebih lanjut.
