import os
import csv
from tkinter import Tk, filedialog, simpledialog


def choose_folder_dialog():
    root = Tk()
    root.withdraw()

    # Open dialog to choose folder
    folder_path = filedialog.askdirectory()

    return folder_path


def sum_rows(input_file_path, num_rows):
    # Read the input CSV file
    with open(input_file_path, 'r') as input_file:
        reader = csv.reader(input_file)
        rows = list(reader)

    # Calculate the sum for each column
    sums = []
    for i in range(len(rows[1])):
        column_sum = sum(float(rows[j][i]) for j in range(1, num_rows + 1))
        sums.append(column_sum)

    return sums


def process_folder(input_folder_path, num_rows_to_sum):
    # Get a list of all CSV files in the input folder
    csv_files = [file for file in os.listdir(input_folder_path) if file.endswith('.csv')]

    # Sort the CSV files alphabetically
    csv_files.sort(key=lambda x: int(os.path.splitext(x)[0].split()[1]))

    for csv_file in csv_files:
        # Create the input and output file paths
        input_file_path = os.path.join(input_folder_path, csv_file)
        output_file_path = os.path.join(input_folder_path, 'summed.csv')

        # Sum the chosen number of rows in the file
        sums = sum_rows(input_file_path, num_rows_to_sum)

        # Write the summed data to the output file
        with open(output_file_path, 'a', newline='') as output_file:
            writer = csv.writer(output_file)
            writer.writerow(sums)  # Write the sums as a new row

        print(f'Processed file {csv_file} and appended summed data to summed.csv')


# Example usage
input_folder_path = choose_folder_dialog()
print("Input folder path:", input_folder_path)
num_rows_to_sum = 50

process_folder(input_folder_path, num_rows_to_sum)
