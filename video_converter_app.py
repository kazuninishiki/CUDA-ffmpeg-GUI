import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import subprocess
import threading
import os

def run_ffmpeg():
    global ffmpeg_process
    source = source_entry.get()
    destination = dest_entry.get()
    crf_value = crf_slider.get()
    ffmpeg_cmd = f"ffmpeg -y "

    if minterpolate_var.get():
        ffmpeg_cmd += '-vf "minterpolate=fps=60:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1" '
    if hwaccel_cuda_var.get():
        ffmpeg_cmd += "-hwaccel cuda "
    if hwaccel_output_format_var.get():
        ffmpeg_cmd += "-hwaccel_output_format cuda "
    
    ffmpeg_cmd += f" -i \"{source}\" -c:a copy "

    if codec_var.get() == 1:
        ffmpeg_cmd += " -c:v h264_nvenc "
    else:
        ffmpeg_cmd += " -c:v hevc_nvenc "

    ffmpeg_cmd += f' -crf {crf_value} "{destination}"'
    
    cmd_display.delete(1.0, tk.END)
    cmd_display.insert(tk.END, ffmpeg_cmd)

    ffmpeg_process = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, shell=True)
    for line in ffmpeg_process.stdout:
        output_text.insert(tk.END, line)
        output_text.see(tk.END)
        window.update()
    done_button.config(state=tk.NORMAL)

def select_source():
    path = filedialog.askopenfilename()
    source_entry.delete(0, tk.END)
    source_entry.insert(0, path)
    dest_entry.delete(0, tk.END)
    dest_entry.insert(0, os.path.splitext(path)[0])

def select_destination():
    path = filedialog.asksaveasfilename(defaultextension=".mp4")
    dest_entry.delete(0, tk.END)
    dest_entry.insert(0, path)

def ffmpeg_thread():
    threading.Thread(target=run_ffmpeg, daemon=True).start()

def stop_ffmpeg():
    global ffmpeg_process
    if ffmpeg_process is not None:
        ffmpeg_process.terminate()

window = tk.Tk()
window.title("FFmpeg GUI")

source_entry = tk.Entry(window, width=50)
source_entry.grid(row=0, column=1, padx=10, pady=10)
tk.Button(window, text="Browse", command=select_source).grid(row=0, column=2)

dest_entry = tk.Entry(window, width=50)
dest_entry.grid(row=1, column=1, padx=10, pady=10)
tk.Button(window, text="Browse", command=select_destination).grid(row=1, column=2)

tk.Button(window, text="Submit", command=ffmpeg_thread).grid(row=2, column=1, padx=10, pady=10)
done_button = tk.Button(window, text="Done", state=tk.DISABLED)
done_button.grid(row=2, column=2, padx=10, pady=10)

output_text = scrolledtext.ScrolledText(window, width=132, height=20, font=('Consolas', 10))
output_text.grid(row=3, column=0, columnspan=3, padx=10, pady=10)

minterpolate_var = tk.BooleanVar()
tk.Checkbutton(window, text="minterpolate", variable=minterpolate_var).grid(row=4, column=0)
hwaccel_cuda_var = tk.BooleanVar()
tk.Checkbutton(window, text="hwaccel cuda", variable=hwaccel_cuda_var).grid(row=4, column=1)
hwaccel_cuda_var.set(1)
hwaccel_output_format_var = tk.BooleanVar()
tk.Checkbutton(window, text="hwaccel_output_format cuda", variable=hwaccel_output_format_var).grid(row=4, column=2)
hwaccel_output_format_var.set(1)

codec_var = tk.IntVar(value=2)
tk.Radiobutton(window, text="h264_nvenc", variable=codec_var, value=1).grid(row=5, column=1)
tk.Radiobutton(window, text="h265_nvenc", variable=codec_var, value=2).grid(row=5, column=2)

crf_slider = tk.Scale(window, from_=16, to=24, orient=tk.HORIZONTAL)
crf_slider.set(16)
crf_slider.grid(row=6, column=1, padx=10, pady=10)

cmd_display = scrolledtext.ScrolledText(window, width=132, height=3, font=('Consolas', 10))
cmd_display.grid(row=7, column=0, columnspan=3, padx=10, pady=10)

tk.Button(window, text="STOP", command=stop_ffmpeg).grid(row=8, column=1, padx=10, pady=10)

window.mainloop()
