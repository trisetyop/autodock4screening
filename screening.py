#!/usr/bin/env python3
import os
import glob

# Mendapatkan daftar semua file berformat SDF di direktori tertentu
sdf_files = glob.glob('*.sdf')





def get_grid_center_from_fld(fld_file):
    with open(fld_file, 'r') as file:
        # Loop through each line in the file
        for line in file:
            # Check for the line starting with "#CENTER"
            if line.startswith("#CENTER"):
                # Extracting the x, y, z coordinates from the "center" line
                center_coords = [float(coord) for coord in line.split()[1:]]
                # Convert the coordinates to a string with commas and quotes
                center_string = ','.join(map(str, center_coords))
                return center_string

    # If no center information is found
    return None

# Example usage
fld_file_path = 'rec.maps.fld'
grid_center = get_grid_center_from_fld(fld_file_path)




# Loop melalui setiap file SDF
for sdf_file in sdf_files:
    # Mendapatkan nama file tanpa ekstensi
    file_name = os.path.splitext(sdf_file)[0]
    os.system(f'obabel {sdf_file} -O {sdf_file}.pdbqt --gen3D -p 7.4 --partialcharge gasteiger --addtotrot')
    os.system(f'./prepare_gpf4.py -l {sdf_file}.pdbqt -r rec.pdbqt -p gridcenter={grid_center}')
    os.system(f'./prepare_dpf4.py -l {sdf_file}.pdbqt -r rec.pdbqt')
    os.system(f'./autogrid4 -p rec.gpf')
    # Get the directory of the script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Use the script directory to create a relative path
    ffile_path = os.path.join(script_dir, 'rec.maps.fld')
    lfile_path = os.path.join(script_dir, f'{sdf_file}.pdbqt')
    sdf = sdf_file.replace(".sdf", "")





    # Baca file
    with open(f'{sdf}_rec.dpf', "r") as file:
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
    with open(f'{sdf}_rec.dpf', "w") as file:
        file.writelines(lines)




    dfile_path = os.path.join(script_dir, f'{sdf}_rec.dpf')
    # Use the relative paths in your system command
    #os.system(f'./autodock_gpu_128wi --ffile {ffile_path} --lfile {lfile_path} --nrun 100')
    #os.system(f'./adgpu_analysis -C 1 {sdf_file}.xml')
    os.system(f'./autodock4 -p {dfile_path}')