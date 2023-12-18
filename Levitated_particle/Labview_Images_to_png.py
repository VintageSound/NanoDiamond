import matplotlib
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import scipy.io as sio


# Function to load settings
def load_settings(data_dir, exp_num):
    # Define the settings file name
    set_name = f'{data_dir}/data_{exp_num}/settings.txt'
    # Load the settings file
    settings = np.loadtxt(set_name, delimiter=' ', dtype=str, max_rows=4)
    # Print the settings
    print(settings)
    # Return the settings
    return settings


# Function to process data
def process_data(data_dir, exp_num, settings):
    # Extract parameters from settings
    pic_num = int(settings[3, 1])
    numbers = 4
    width = int(settings[0, 1])
    height = int(settings[1, 1])

    # Loop over all pictures
    for iii in range(pic_num):
        # Define file names
        name = f'{data_dir}/data_{exp_num}/data_{iii}'
        name_txt = name + '.txt'
        name_png = name + '.png'

        # Load data file
        file = np.loadtxt(name_txt, delimiter=';')
        # Initialize data array
        data = np.zeros([height, width, numbers])

        # Reshape data
        var = 0
        for i in range(height):
            for ii in range(width):
                data[i, ii] = file[var:var + 4]
                var += 4

        # Plot and save data
        plot_and_save(data, name_png)


# Function to plot and save data
def plot_and_save(data, name_png):
    # Create a new figure
    fig, ax = plt.subplots()
    # Display data
    image = ax.imshow(data[:, :, 0], vmin=0, vmax=50)
    # Save figure
    plt.savefig(name_png)
    # Close figure
    plt.close()
    print('done')


def today_date():
    # Get today's date
    today = datetime.today()

    # Format it as dd.mm.yy
    date_string = today.strftime("%d.%m.%y")
    return date_string


# Main function
def main():
    back = matplotlib.get_backend()
    print(back)
    # Define experiment number and data directory
    exp_num = str(1)
    data_dir = 'imaging/'+today_date()
    # Load settings
    settings = load_settings(data_dir, exp_num)
    # Process data
    process_data(data_dir, exp_num, settings)


# Run main function if script is run directly
if __name__ == "__main__":
    main()
