import tkinter.filedialog as tkfd
import tkinter as tk
import csv
import binascii


def bin_to_csv(bin_file, csv_file):
    with open(bin_file, "rb") as f_bin:
        with open(csv_file, "w", newline="") as f_csv:
            writer = csv.writer(f_csv, delimiter=",")
            for line in f_bin:
                data = binascii.b2a_hex(line).decode("utf-8")
                # Split the hexadecimal string into a list of strings
                data_list = data.split(" ")
                # Add a header row to the CSV file
                if not writer.newlines:
                    writer.writerow(["Data"])
                writer.writerow(data_list)


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    bin_file = tkfd.askopenfilename()
    csv_file = "data/csv_file.csv"

    bin_to_csv(bin_file, csv_file)