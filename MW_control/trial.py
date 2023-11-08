import tkinter as tk
import SMR20_control


class RSMR20GUI:
    def __init__(self, smr20):
        self.smr20 = smr20
        self.root = tk.Tk()
        self.root.title("RSMR20 GUI")

        # Frequency
        self.label_frequency = tk.Label(self.root, text="Frequency")
        self.entry_frequency = tk.Entry(self.root)

        # Power
        self.label_power = tk.Label(self.root, text="Power")
        self.entry_power = tk.Entry(self.root)

        # Sweep parameters
        self.label_start_frequency = tk.Label(self.root, text="Start frequency")
        self.entry_start_frequency = tk.Entry(self.root)
        self.label_stop_frequency = tk.Label(self.root, text="Stop frequency")
        self.entry_stop_frequency = tk.Entry(self.root)
        self.label_step_size = tk.Label(self.root, text="Step size")
        self.entry_step_size = tk.Entry(self.root)
        self.label_dwell_time = tk.Label(self.root, text="Dwell time")
        self.entry_dwell_time = tk.Entry(self.root)

        # Buttons
        self.button_set = tk.Button(self.root, text="Set", command=self.set_parameters)
        self.button_start_sweep = tk.Button(self.root, text="Start sweep", command=self.start_sweep)

        # On/Off buttons
        self.button_on = tk.Button(self.root, text="On", command=self.smr20.on)
        self.button_off = tk.Button(self.root, text="Off", command=self.smr20.off)

        # Layout
        self.label_frequency.grid(row=0, column=0)
        self.entry_frequency.grid(row=0, column=1)
        self.label_power.grid(row=1, column=0)
        self.entry_power.grid(row=1, column=1)
        self.label_start_frequency.grid(row=2, column=0)
        self.entry_start_frequency.grid(row=2, column=1)
        self.label_stop_frequency.grid(row=3, column=0)
        self.entry_stop_frequency.grid(row=3, column=1)
        self.label_step_size.grid(row=4, column=0)
        self.entry_step_size.grid(row=4, column=1)
        self.label_dwell_time.grid(row=5, column=0)
        self.entry_dwell_time.grid(row=5, column=1)
        self.button_set.grid(row=6, column=0)
        self.button_start_sweep.grid(row=6, column=1)
        self.button_on.grid(row=7, column=0)
        self.button_off.grid(row=7, column=1)

        self.root.mainloop()

    def set_parameters(self):
        frequency = int(self.entry_frequency.get())
        power = int(self.entry_power.get())
        start_frequency = int(self.entry_start_frequency.get())
        stop_frequency = int(self.entry_stop_frequency.get())
        step_size = int(self.entry_step_size.get())
        dwell_time = int(self.entry_dwell_time.get())

        self.smr20.set_frequency(frequency)
        self.smr20.set_power(power)
        self.smr20.set_sweep_parameters(start_frequency, stop_frequency, step_size, dwell_time)

    def start_sweep(self):
        self.smr20.start_sweep()


if __name__ == "__main__":
    smr20 = SMR20_control.RSMR20("GPIB0::3::INSTR")
    gui = RSMR20GUI(smr20)