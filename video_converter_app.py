import tkinter as tk
from tkinter import filedialog
import subprocess
from threading import Thread

class VideoConverterApp:
    def __init__(self, master):
        self.master = master
        master.title("CUDA-ffmpeg-GUI")

        # Input Widgets
        self.source_label = tk.Label(master, text="Source:")
        self.source_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.E)

        self.source_entry = tk.Entry(master, width=50)
        self.source_entry.grid(row=0, column=1, padx=10, pady=10)

        self.source_button = tk.Button(master, text="Browse", command=self.browse_source)
        self.source_button.grid(row=0, column=2, padx=10, pady=10)

        self.source_duration_label = tk.Label(master, text="Source Duration:")
        self.source_duration_label.grid(row=0, column=3, padx=10, pady=10, sticky=tk.E)

        # Destination Widgets
        self.destination_label = tk.Label(master, text="Destination:")
        self.destination_label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.E)

        self.destination_entry = tk.Entry(master, width=50)
        self.destination_entry.grid(row=1, column=1, padx=10, pady=10)

        self.destination_button = tk.Button(master, text="Browse", command=self.browse_destination)
        self.destination_button.grid(row=1, column=2, padx=10, pady=10)

        self.destination_duration_label = tk.Label(master, text="Destination Duration:")
        self.destination_duration_label.grid(row=1, column=3, padx=10, pady=10, sticky=tk.E)

        # minterpolate Checkbox
        self.minterpolate_var = tk.IntVar()
        self.minterpolate_checkbox = tk.Checkbutton(master, text="motion interpolation (60fps)", variable=self.minterpolate_var)
        self.minterpolate_checkbox.grid(row=2, column=0, pady=10, sticky=tk.W)

        # CUDA Output Checkbox
        self.cuda_output_var = tk.IntVar(value=1)
        self.cuda_output_checkbox = tk.Checkbutton(master, text="cuda output", variable=self.cuda_output_var)
        self.cuda_output_checkbox.grid(row=2, column=1, pady=10, sticky=tk.W)

        # CUDA Hardware Acceleration Checkbox
        self.cuda_hw_accel_var = tk.IntVar(value=1)  # Checked by default
        self.cuda_hw_accel_checkbox = tk.Checkbutton(master, text="CUVID Accel", variable=self.cuda_hw_accel_var)
        self.cuda_hw_accel_checkbox.grid(row=2, column=3, pady=10, sticky=tk.W)

        # h264 or h265 output Checkbox
        self.h264or5_var = tk.IntVar(value=1)  # Checked by default
        self.h264or5_checkbox = tk.Checkbutton(master, text="h265 (empty=h264)", variable=self.h264or5_var)
        self.h264or5_checkbox.grid(row=2, column=2, pady=10, sticky=tk.W)

        # CRF Slider
        self.crf_label = tk.Label(master, text="CRF Value:")
        self.crf_label.grid(row=2, column=3, pady=10, padx=(10, 0), sticky=tk.E)

        self.crf_slider = tk.Scale(master, from_=16, to=24, orient=tk.HORIZONTAL, length=150, resolution=1, command=self.update_crf)
        self.crf_slider.set(18)
        self.crf_slider.grid(row=2, column=4, pady=10, sticky=tk.W)

        # Submit Button
        self.submit_button = tk.Button(master, text="Submit", command=self.convert_video)
        self.submit_button.grid(row=3, columnspan=5, pady=10)

        # Stop Button
        self.stop_button = tk.Button(master, text="STOP", command=self.stop_conversion)
        self.stop_button.grid(row=4, columnspan=5, pady=10)
        self.stop_button.grid_remove()

        # Command Text Widget
        self.command_text = tk.Text(master, height=2, width=132, font=("Consolas", 10))
        self.command_text.grid(row=5, columnspan=5, padx=10, pady=10, sticky="nsew")

        # Output Text Widget with Scrollbar
        self.output_text = tk.Text(master, height=10, width=132, font=("Consolas", 10))
        self.output_text.grid(row=6, columnspan=5, padx=10, pady=10, sticky="nsew")

        self.scrollbar = tk.Scrollbar(master, command=self.output_text.yview)
        self.scrollbar.grid(row=6, column=5, sticky='ns')
        self.output_text['yscrollcommand'] = self.scrollbar.set

        # Configure resizing behavior
        master.columnconfigure(1, weight=1)
        master.columnconfigure(2, weight=0)
        master.columnconfigure(3, weight=0)
        master.columnconfigure(4, weight=0)
        master.columnconfigure(5, weight=0)
        master.rowconfigure(6, weight=1)

        # Done Button (Initially hidden)
        self.done_button = tk.Button(master, text="Done", command=self.reset_form)
        self.done_button.grid(row=7, columnspan=5, pady=10)
        self.done_button.grid_remove()

        # Variable to store the subprocess object
        self.process = None

    def browse_source(self):
        source_file = filedialog.askopenfilename(filetypes=[("Source Video File", "*")])
        self.source_entry.delete(0, tk.END)
        self.source_entry.insert(0, source_file)
        self.update_source_duration()

    def browse_destination(self):
        destination_file = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("Output Video File", "*.mp4")])
        self.destination_entry.delete(0, tk.END)
        self.destination_entry.insert(0, destination_file)
        self.update_destination_duration()

    def update_source_duration(self):
        source = self.source_entry.get()
        if source:
            duration = self.get_video_duration(source)
            self.source_duration_label.config(text=f"Source Duration: {duration} Seconds")

    def update_destination_duration(self):
        destination = self.destination_entry.get()
        if destination:
            duration = self.get_video_duration(destination)
            self.destination_duration_label.config(text=f"Destination Duration: {duration} Seconds")

    def get_video_duration(self, file_path):
        try:
            result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', file_path], stdout=subprocess.PIPE, text=True)
            return round(float(result.stdout))
        except Exception as e:
            print(f"Error getting duration: {str(e)}")
            return "N/A"

    def convert_video(self):
        source = self.source_entry.get()
        destination = self.destination_entry.get()

        if not source or not destination:
            self.output_text.insert(tk.END, "Please select source and destination files.\n")
            return

        minterpolate_option = f' -vf "minterpolate=fps=60:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1" ' if self.minterpolate_var.get() else ""
        cuda_output_option = '-hwaccel_output_format cuda ' if self.cuda_output_var.get() else ""
        cuda_hw_accel_option = '-hwaccel cuda' if self.cuda_hw_accel_var.get() else ""
        crf_value = self.crf_slider.get()
        h264or5_option = f'hevc_nvenc ' if self.h264or5_var.get() else "h264_nvenc"

        cmd = f'ffmpeg -y {cuda_hw_accel_option} {cuda_output_option} -i "{source}" -c:a copy -c:v {h264or5_option} -crf {crf_value} {minterpolate_option} "{destination}"'

        # Display the command in the command_text widget
        self.command_text.delete(1.0, tk.END)
        self.command_text.insert(tk.END, f"Executing command: {cmd}\n\n")

        # Run command in a separate thread to avoid blocking the GUI
        thread = Thread(target=self.run_command, args=(cmd,))
        thread.start()

        # Show the Stop button
        self.stop_button.grid(row=4, columnspan=5, pady=10)
        # Hide the Submit button
        self.submit_button.grid_remove()

    def run_command(self, cmd):
        try:
            self.process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            while self.process.poll() is None:
                output = self.process.stdout.readline()
                self.output_text.insert(tk.END, output)
                self.output_text.yview(tk.END)
            # Capture the remaining output after the process completes
            remaining_output = self.process.communicate()[0]
            self.output_text.insert(tk.END, remaining_output)
        except Exception as e:
            self.output_text.insert(tk.END, f"Error: {str(e)}\n")
        finally:
            self.done_button.grid(row=7, columnspan=5, pady=10)
            self.update_source_duration()
            self.update_destination_duration()

    def stop_conversion(self):
        if self.process:
            try:
                # Terminate the ffmpeg process
                self.process.terminate()
                self.output_text.insert(tk.END, "Conversion stopped by user.\n")
            except Exception as e:
                self.output_text.insert(tk.END, f"Error stopping conversion: {str(e)}\n")

            # Hide the Stop button
            self.stop_button.grid_remove()
            # Show the Submit button
            self.submit_button.grid(row=3, columnspan=5, pady=10)

    def reset_form(self):
        self.source_entry.delete(0, tk.END)
        self.destination_entry.delete(0, tk.END)
        self.output_text.delete(1.0, tk.END)
        self.command_text.delete(1.0, tk.END)
        self.done_button.grid_remove()
        self.stop_button.grid_remove()
        self.submit_button.grid(row=3, columnspan=5, pady=10)
        self.source_duration_label.config(text="Source Duration:")
        self.destination_duration_label.config(text="Destination Duration:")

    def update_crf(self, value):
        self.crf_label.config(text=f"CRF:")

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoConverterApp(root)
    root.mainloop()
