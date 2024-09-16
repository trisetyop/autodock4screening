#!/usr/bin/env python3

import sys
import os
import logging
import tkinter as tk
from tkinter import simpledialog
import subprocess
import urllib.request
import re
from rdkit import Chem
import pubchempy as pcp
import string
import csv
import shutil
from tkinter import filedialog





# Fungsi untuk mendapatkan argumen dari dialog box
def get_arguments():
    root = tk.Tk()
    root.withdraw()

    rec = simpledialog.askstring("Input", "Masukkan nama reseptor:")
    lig = simpledialog.askstring("Input", "Masukkan nama ligand:")
    chain = simpledialog.askstring("Input", "Masukkan nama chain:")

    return rec, lig, chain

# Dapatkan argumen dari dialog box
rec, lig, chain = get_arguments()





url = f'http://files.rcsb.org/download/{rec}.pdb'
filename = f'{rec}.pdb'

try:
    urllib.request.urlretrieve(url, filename)
    print(f"File {filename} berhasil diunduh.")
except Exception as e:
    print(f"Terjadi kesalahan saat mengunduh file: {e}")





input_filename = f'{rec}.pdb'
output_filename = f'{rec}_{chain}.pdb'

try:
    with open(input_filename, 'r') as input_file, open(output_filename, 'w') as output_file:
        for line in input_file:
            if re.match(r'^ATOM', line) and line[21] == chain or re.match(r'^HETATM', line) and line[21] == chain:
                output_file.write(line)

    print(f"File {output_filename} berhasil dibuat.")
except Exception as e:
    print(f"Terjadi kesalahan saat memproses file: {e}")





input_filename = f'{rec}_{chain}.pdb'
output_filename = 'rec.pdb'

try:
    with open(input_filename, 'r') as input_file, open(output_filename, 'w') as output_file:
        for line in input_file:
            if 'ATOM' in line:
                output_file.write(line)

    print(f"File {output_filename} berhasil dibuat.")
except Exception as e:
    print(f"Terjadi kesalahan saat memproses file: {e}")



os.system(f'./prepare_receptor4.py -r rec.pdb')

# Gunakan grep dengan regular expression untuk mencari baris yang sesuai dengan pola
input_filename = f'{rec}_{chain}.pdb'
output_filename = 'lig.pdb'

try:
    with open(input_filename, 'r') as input_file, open(output_filename, 'w') as output_file:
        for line in input_file:
            if f'{lig} {chain}' in line:
                output_file.write(line)

    print(f"File {output_filename} berhasil dibuat.")
except Exception as e:
    print(f"Terjadi kesalahan saat memproses file: {e}")







os.system(f'./prepare_ligand4.py -l lig.pdb')
os.system(f'./prepare_dpf4.py -l lig.pdbqt -r rec.pdbqt')
os.system(f'./prepare_gpf4.py -l lig.pdbqt -r rec.pdbqt -y')
os.system(f'./prepare_dpf4.py -l lig.pdbqt -r rec.pdbqt')

os.system(f'./autogrid4 -p rec.gpf')



# Get the directory of the script
script_dir = os.path.dirname(os.path.abspath(__file__))






# Baca file
with open("lig_rec.dpf", "r") as file:
    lines = file.readlines()

# Hapus baris yang diinginkan
lines = [line for line in lines if "tran0 random" not in line and
         "quaternion0 random" not in line and
         "dihe0 random" not in line and
         "torsdof 3" not in line and
         "rmstol 2.0" not in line and
         "extnrg 1000.0" not in line and
         "e0max 0.0 10000" not in line and
         "ga_pop_size 150" not in line and
         "ga_num_evals 2500000" not in line and
         "ga_num_generations 27000" not in line and
         "ga_elitism 1" not in line and
         "ga_mutation_rate 0.02" not in line and
         "ga_crossover_rate 0.8" not in line and
         "ga_window_size 10" not in line and
         "ga_cauchy_alpha 0.0" not in line and
         "ga_cauchy_beta 1.0" not in line and
         "set_ga" not in line and
         "sw_max_its 300" not in line and
         "sw_max_succ 4" not in line and
         "sw_max_fail 4" not in line and
         "sw_rho 1.0" not in line and
         "sw_lb_rho 0.01" not in line and
         "ls_search_freq 0.06" not in line and
         "set_psw1" not in line and
         "unbound_model extended" not in line and
         "ga_run 10" not in line and
         "analysis" not in line]

# Tambahkan baris baru
new_lines = [
    "## INITIAL SEARCH STATE SECTION\n",
    "set_ga # set the above parameters for GA or LGA\n",
    "## LOCAL SEARCH PARAMETERS SECTION\n",
    "sw_max_its 300 # iterations of Solis & Wets local search\n",
    "sw_max_succ 4 # consecutive successes before changing rho\n",
    "sw_max_fail 4 # consecutive failures before changing rho\n",
    "sw_rho 1.0 # size of local search space to sample\n",
    "sw_lb_rho 0.01 # lower bound on rho\n",
    "ls_search_freq 0.06 # probability of performing local search on individual\n",
    "set_psw1 # set the above pseudo Solis & Wets parameters\n",
    "## PERFORM SEARCH SECTION\n",
    "ga_run 100 # do this many hybrid GA-LS runs\n",
    "## ANALYSIS SECTION\n",
    "rmstol 2 # cluster_tolerance/A\n",
    "analysis # perform a ranked cluster analysis\n"
]

# Gabungkan baris-baris baru dengan baris-baris yang tersisa
lines += new_lines

# Tulis kembali file
with open("lig_rec.dpf", "w") as file:
    file.writelines(lines)







# Use the script directory to create a relative path
ffile_path = os.path.join(script_dir, 'rec.maps.fld')
lfile_path = os.path.join(script_dir, 'lig.pdbqt')
dfile_path = os.path.join(script_dir, 'lig_rec.dpf')
# Use the relative paths in your system command
os.system(f'./autodock4 -p {dfile_path}')
