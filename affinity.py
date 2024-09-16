#!/usr/bin/env python3
import os
import csv

def extract_affinity(file_path):
    affinities = []
    with open(file_path, 'r') as file:
        for line in file:
            if line.strip().startswith("1 |"):
                affinity = line.split("|")[1].strip()
                affinities.append(affinity)
    return affinities


def process_files(directory):
    data = []
    for filename in os.listdir(directory):
        if filename.endswith(".dlg"):
            compound_name = os.path.splitext(filename)[0]
            file_path = os.path.join(directory, filename)
            affinities = extract_affinity(file_path)
            print(f"Processed {compound_name}: {affinities}")  # Debugging line
            data.extend([(compound_name, affinity) for affinity in affinities])
    return data

def write_to_csv(data, output_file):
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Compound', 'Affinity'])
        writer.writerows(data)
        print("Data written to CSV file.")  # Debugging line

def open_csv_file(csv_file):
    try:
        import subprocess
        subprocess.Popen(['xdg-open', csv_file])
    except FileNotFoundError:
        print("Failed to open CSV file. Please check your default application for CSV files.")

if __name__ == "__main__":
    directory_path = os.path.dirname(os.path.abspath(__file__))  # Ganti dengan path direktori yang sesuai
    output_csv = "affinities.csv"

    data = process_files(directory_path)
    write_to_csv(data, output_csv)
    print("CSV file has been created:", output_csv)

    open_csv_file(output_csv)

 