import os
import csv
from tkinter import Tk, filedialog, simpledialog


def choose_folder_dialog():
    root = Tk()
    root.withdraw()

    # Open dialog to choose folder
    folder_path = filedialog.askdirectory()

    return folder_path


def choose_group_size_dialog():
    root = Tk()
    root.withdraw()

    # Open dialog to choose group size
    group_size = simpledialog.askinteger("Group Size", "Enter the size of the CSV file group:")
    return group_size


def process_csv_files(input_folder, output_folder, group_size):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Get a list of all the CSV files in the input folder
    csv_files = [file for file in os.listdir(input_folder) if file.endswith('.csv')]

    # Sort the CSV files alphabetically
    csv_files.sort(key=lambda x: int(os.path.splitext(x)[0]))

    # Process the CSV files in groups of the specified size
    for i in range(0, len(csv_files), group_size):
        # Create a list to store the data from the group of files
        data = []

        # Create a list to store the file names
        file_names = []

        # Iterate over the files in the current group
        for j in range(i, min(i + group_size, len(csv_files))):
            # Open the CSV file
            csv_file_path = os.path.join(input_folder, csv_files[j])
            with open(csv_file_path, 'r') as file:
                reader = csv.reader(file)
                rows = list(reader)  # Read all rows
                k = 0

                # Process each row starting from the 16th row
                for row in rows[15:]:
                    averaged_row = []
                    for cell in row:
                        try:
                            averaged_cell = float(cell)
                        except ValueError:
                            averaged_cell = cell
                        averaged_row.append(averaged_cell)
                    if j-i == 0:
                        data.append(averaged_row)
                    else:
                        data[k].append(averaged_row[1])
                        k = k+1

            # Store the file name
            file_names.append(csv_files[j])

        # Average the data points
        data = [[sublist[0], sum(sublist[1:]) / len(sublist[1:])] for sublist in data]

        # Create the output file name
        output_file_name = f'average {csv_files[i].split(".")[0]} - {csv_files[min(i + group_size - 1, len(csv_files) - 1)].split(".")[0]}.csv'
        output_file_path = os.path.join(output_folder, output_file_name)

        # Save the averaged data to a new CSV file
        with open(output_file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            # Write the file names as the first line
            writer.writerow(file_names)
            writer.writerows(data)

        print(f'Processed files {csv_files[i]} to {csv_files[min(i + group_size - 1, len(csv_files) - 1)]} and saved averaged data to {output_file_name}')


# Example usage
input_folder = choose_folder_dialog()
print("Input folder path:", input_folder)

output_folder = choose_folder_dialog()
print("Output folder path:", output_folder)

group_size = choose_group_size_dialog()
process_csv_files(input_folder, output_folder, group_size)
