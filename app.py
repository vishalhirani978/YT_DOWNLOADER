import customtkinter as ctk
from pytubefix import YouTube
from tkinter import filedialog
import threading

# ---------------------- Setup ----------------------
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")  # base theme, we will override colors

root = ctk.CTk()
root.title("YouTube Downloader")
root.geometry("550x400")
root.resizable(False, False)

# ---------------------- Variables ----------------------
url_var = ctk.StringVar()
path_var = ctk.StringVar()
option_var = ctk.StringVar(value="Video")
progress_var = ctk.DoubleVar(value=0)

# ---------------------- Functions ----------------------
def browse_folder():
    folder = filedialog.askdirectory()
    if folder:
        path_var.set(folder)

def start_download():
    # Run download in separate thread to keep UI responsive
    threading.Thread(target=download, daemon=True).start()

def download():
    url = url_var.get()
    path = path_var.get()
    choice = option_var.get()

    if not url or not path:
        status_label.configure(text="❌ Please enter URL and folder!", text_color="#FF3B3F")
        return

    try:
        yt = YouTube(url)
        status_label.configure(text=f"⏳ Downloading: {yt.title}", text_color="#FFFFFF")

        if choice == "Video":
            stream = yt.streams.get_highest_resolution()
        else:
            stream = yt.streams.filter(only_audio=True).first()

        # Update progress bar manually (basic)
        progress_bar.set(0)
        stream.download(path)
        progress_bar.set(100)

        status_label.configure(text="✅ Download Complete!", text_color="#00FF7F")

    except Exception as e:
        status_label.configure(text=f"❌ Error: {str(e)}", text_color="#FF3B3F")

# ---------------------- UI ----------------------
ctk.CTkLabel(root, text="YouTube URL:", text_color="#FF3B3F", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(20,5))
url_entry = ctk.CTkEntry(root, textvariable=url_var, width=450, height=35, fg_color="#1C1C1C", text_color="#FFFFFF", border_color="#FF3B3F", corner_radius=8)
url_entry.pack(pady=5)

ctk.CTkLabel(root, text="Download Folder:", text_color="#FF3B3F", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(15,5))
folder_frame = ctk.CTkFrame(root, fg_color="#1C1C1C", corner_radius=10)
folder_frame.pack(pady=5, padx=10, fill="x")
ctk.CTkEntry(folder_frame, textvariable=path_var, width=350, height=35, fg_color="#1C1C1C", text_color="#FFFFFF", border_color="#FF3B3F", corner_radius=8).pack(side="left", padx=10, pady=5)
ctk.CTkButton(folder_frame, text="Browse", width=80, height=35, fg_color="#FF3B3F", hover_color="#FF6666", command=browse_folder).pack(side="left", padx=10)

ctk.CTkLabel(root, text="Download Type:", text_color="#FF3B3F", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(15,5))
option_frame = ctk.CTkFrame(root, fg_color="#1C1C1C", corner_radius=10)
option_frame.pack(pady=5)
ctk.CTkRadioButton(option_frame, text="Video", variable=option_var, value="Video", text_color="#FF3B3F").pack(side="left", padx=20)
ctk.CTkRadioButton(option_frame, text="Audio", variable=option_var, value="Audio", text_color="#FF3B3F").pack(side="left", padx=20)

ctk.CTkButton(root, text="Download", width=120, height=40, fg_color="#FF3B3F", hover_color="#FF6666", command=start_download).pack(pady=20)

progress_bar = ctk.CTkProgressBar(root, width=450, variable=progress_var)
progress_bar.set(0)
progress_bar.pack(pady=10)

status_label = ctk.CTkLabel(root, text="", text_color="#FFFFFF", font=ctk.CTkFont(size=14))
status_label.pack(pady=5)

root.mainloop()