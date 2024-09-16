#!/usr/bin/env python3
import os
import csv
from rdkit import Chem
from rdkit.Chem import Lipinski
from rdkit.Chem import Descriptors
from rdkit.Chem import Lipinski

def calculate_lipinski_parameters(mol, filename):
    params = {}
    params['FileName'] = filename
    params['MolecularWeight'] = Chem.Descriptors.MolWt(mol)
    params['LogP'] = Chem.Descriptors.MolLogP(mol)
    params['NumHDonors'] = Lipinski.NumHDonors(mol)
    params['NumHAcceptors'] = Lipinski.NumHAcceptors(mol)
    params['MolarRefractivity'] = Chem.Descriptors.MolMR(mol)
    return params

def check_lipinski_rules(params):
    violations = []
    if params['MolecularWeight'] > 500:
        violations.append("Molecular weight exceeds 500 Dalton.")
    if params['LogP'] > 5:
        violations.append("LogP exceeds 5 (high lipophilicity).")
    if params['NumHDonors'] >= 5:
        violations.append("Number of hydrogen bond donors exceeds 5.")
    if params['NumHAcceptors'] >= 10:
        violations.append("Number of hydrogen bond acceptors exceeds 10.")
    if params['MolarRefractivity'] < 40 or params['MolarRefractivity'] > 130:
        violations.append("Molar refractivity is not between 40-130.")
    
    if len(violations) <= 1:
        return True, violations
    else:
        return False, violations

def process_sdf_files_in_current_directory():
    cwd = os.getcwd()
    sdf_files = [f for f in os.listdir(cwd) if f.endswith('.sdf')]
    with open('lipinski_results.csv', 'w', newline='') as csvfile:
        fieldnames = ['FileName', 'MolecularWeight', 'LogP', 'NumHDonors', 'NumHAcceptors', 'MolarRefractivity', 'PassedLipinski', 'RuleViolations']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for sdf_file in sdf_files:
            suppl = Chem.SDMolSupplier(os.path.join(cwd, sdf_file))
            for mol in suppl:
                if mol:
                    params = calculate_lipinski_parameters(mol, sdf_file)
                    passed, violations = check_lipinski_rules(params)
                    params['PassedLipinski'] = passed
                    params['RuleViolations'] = '; '.join(violations)
                    writer.writerow(params)

# Memproses file SDF di direktori saat ini
process_sdf_files_in_current_directory()



import pandas as pd

# Baca file affinities.csv
affinities_df = pd.read_csv("affinities.csv")

# Baca file lipinski_result.csv
lipinski_df = pd.read_csv("lipinski_results.csv")

# Gabungkan kedua dataframe berdasarkan kolom "Compound" atau "FileName"
merged_df = pd.merge(affinities_df, lipinski_df, left_on="Compound", right_on="FileName")

# Simpan hasil gabungan ke dalam file CSV
merged_df.to_csv("merged_data.csv", index=False)

# Buka file CSV yang telah disimpan
import os
os.system("start merged_data.csv")

