import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageTk

# Import fungsi histogram dari tugas 1
from histogram_citra import HistogramApp as Histogram

class EnhancementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tugas 2 - Perbaikan Kualitas Citra")
        self.root.geometry("900x700")
        self.root.configure(bg="white")
        self.img = None
        self.img_path = None
        self.build_ui()

    def build_ui(self):
        tk.Label(self.root, text="Perbaikan Kualitas Citra",
                 font=("Arial", 16, "bold"),
                 bg="white", fg="black").pack(fill=tk.X, pady=10)

        # Frame tombol buka citra
        frame_top = tk.Frame(self.root, bg="white", pady=8)
        frame_top.pack(fill=tk.X)

        tk.Button(frame_top, text="Buka Citra", command=self.buka_citra,
                  bg="#e6e6e6", fg="black", padx=12, pady=4).pack(side=tk.LEFT, padx=10)

        self.label_file = tk.Label(frame_top, text="Belum ada citra dipilih",
                                   fg="black", bg="white")
        self.label_file.pack(side=tk.LEFT, padx=10)

        tk.Button(frame_top, text="Kembali", command=self.kembali,
                  bg="#e6e6e6", fg="black", padx=12, pady=4).pack(side=tk.RIGHT, padx=10)

        # Frame parameter + metode
        frame_mid = tk.Frame(self.root, bg="white")
        frame_mid.pack(fill=tk.X, padx=10, pady=5)

        # Pilih metode
        tk.Label(frame_mid, text="Metode:", bg="white",
             fg="black").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

        self.metode = tk.StringVar()
        self.metode.set("Image Brightening")
        metode_list = [
            "Image Brightening",
            "Citra Negatif",
            "Balikan Citra Negatif",
            "Transformasi Log",
            "Transformasi Pangkat",
            "Contrast Stretching",
        ]
        self.dropdown_metode = tk.OptionMenu(frame_mid, self.metode,
                                             *metode_list,
                                             command=self.update_param)
        self.dropdown_metode.config(bg="#e6e6e6", fg="black")
        self.dropdown_metode.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        # Frame parameter input
        self.frame_param = tk.LabelFrame(frame_mid, text="Parameter",
                                         bg="white", fg="black", padx=10, pady=5)
        self.frame_param.grid(row=1, column=0, columnspan=4,
                              padx=5, pady=5, sticky=tk.W)

        # Parameter labels dan entry
        self.param_labels = []
        self.param_entries = []
        self.param_vars = []

        for i in range(3):
            lbl = tk.Label(self.frame_param, text="", bg="white", fg="black", width=10)
            lbl.grid(row=0, column=i*2, padx=5)
            var = tk.StringVar()
            ent = tk.Entry(self.frame_param, textvariable=var, width=8,
                           bg="white", fg="black", insertbackground="black")
            ent.grid(row=0, column=i*2+1, padx=5)
            self.param_labels.append(lbl)
            self.param_entries.append(ent)
            self.param_vars.append(var)

        # Tombol proses
        tk.Button(frame_mid, text="▶ Proses", command=self.proses,
                  bg="#e6e6e6", fg="black", font=("Arial", 11, "bold"),
                  padx=15, pady=5).grid(row=2, column=0,
                                                         columnspan=2, pady=10)

        # Frame preview
        frame_preview = tk.Frame(self.root, bg="white")
        frame_preview.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        frame_in = tk.LabelFrame(frame_preview, text="Citra Input",
                                 bg="white", fg="black", padx=5, pady=5)
        frame_in.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        self.canvas_in = tk.Canvas(frame_in, bg="#f5f5f5")
        self.canvas_in.pack(fill=tk.BOTH, expand=True)

        frame_out = tk.LabelFrame(frame_preview, text="Citra Output",
                                  bg="white", fg="black", padx=5, pady=5)
        frame_out.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        self.canvas_out = tk.Canvas(frame_out, bg="#f5f5f5")
        self.canvas_out.pack(fill=tk.BOTH, expand=True)

        # Init parameter default
        self.update_param("Image Brightening")

    def update_param(self, metode):
        # Reset semua label
        for lbl in self.param_labels:
            lbl.config(text="")
        for ent in self.param_entries:
            ent.grid_remove()

        if metode == "Image Brightening":
            self.param_labels[0].config(text="Value (b):")
            self.param_entries[0].grid()
            self.param_vars[0].set("50")

        elif metode in ("Citra Negatif", "Balikan Citra Negatif"):
            self.param_labels[0].config(text="-")

        elif metode == "Transformasi Log":
            self.param_labels[0].config(text="c:")
            self.param_entries[0].grid()
            self.param_vars[0].set("1")

        elif metode == "Transformasi Pangkat":
            self.param_labels[0].config(text="c:")
            self.param_entries[0].grid()
            self.param_vars[0].set("1")
            self.param_labels[1].config(text="gamma (γ):")
            self.param_entries[1].grid()
            self.param_vars[1].set("1.5")

        elif metode == "Contrast Stretching":
            self.param_labels[0].config(text="()")

    def buka_citra(self):
        path = filedialog.askopenfilename(
            title="Pilih Citra",
            filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp *.tif *.tiff")]
        )
        if path:
            self.img_path = path
            self.img = cv2.imread(path)
            nama = path.split("/")[-1]
            self.label_file.config(text=nama, fg="black")
            self.tampilkan_canvas(self.canvas_in, self.img)

    def tampilkan_canvas(self, canvas, img):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(img_rgb)
        pil_img.thumbnail((350, 250))
        tk_img = ImageTk.PhotoImage(pil_img)
        canvas.image = tk_img
        canvas.update()
        canvas.create_image(
            canvas.winfo_width() // 2,
            canvas.winfo_height() // 2,
            anchor=tk.CENTER, image=tk_img
        )

    def hitung_histogram_manual(self, channel):
        hist = np.zeros(256, dtype=int)
        for pixel in channel.flatten():
            hist[pixel] += 1
        return hist

    def tampilkan_histogram_hasil(self, img_in, img_out, judul):
        # Konversi ke grayscale untuk histogram jika berwarna
        if len(img_in.shape) == 3:
            gray_in = cv2.cvtColor(img_in, cv2.COLOR_BGR2GRAY)
            gray_out = cv2.cvtColor(img_out, cv2.COLOR_BGR2GRAY)
        else:
            gray_in = img_in
            gray_out = img_out

        hist_in = self.hitung_histogram_manual(gray_in)
        hist_out = self.hitung_histogram_manual(gray_out)

        fig, axes = plt.subplots(2, 2, figsize=(12, 8))
        fig.suptitle(judul, fontsize=14)

        # Citra input
        if len(img_in.shape) == 3:
            axes[0,0].imshow(cv2.cvtColor(img_in, cv2.COLOR_BGR2RGB))
        else:
            axes[0,0].imshow(img_in, cmap='gray')
        axes[0,0].set_title("Citra Input")
        axes[0,0].axis('off')

        # Histogram input
        axes[0,1].bar(range(256), hist_in, color='gray', width=1)
        axes[0,1].set_title("Histogram Input")
        axes[0,1].set_xlabel("Nilai Piksel")
        axes[0,1].set_ylabel("Jumlah Piksel")
        axes[0,1].set_xlim([0, 255])
        axes[0,1].grid(True, alpha=0.3)

        # Citra output
        if len(img_out.shape) == 3:
            axes[1,0].imshow(cv2.cvtColor(img_out, cv2.COLOR_BGR2RGB))
        else:
            axes[1,0].imshow(img_out, cmap='gray')
        axes[1,0].set_title("Citra Output")
        axes[1,0].axis('off')

        # Histogram output
        axes[1,1].bar(range(256), hist_out, color='steelblue', width=1)
        axes[1,1].set_title("Histogram Output")
        axes[1,1].set_xlabel("Nilai Piksel")
        axes[1,1].set_ylabel("Jumlah Piksel")
        axes[1,1].set_xlim([0, 255])
        axes[1,1].grid(True, alpha=0.3)

        plt.tight_layout()
        plt.show()

    def proses(self):
        if self.img is None:
            messagebox.showwarning("Peringatan", "Pilih citra terlebih dahulu!")
            return

        metode = self.metode.get()
        img = self.img.copy()
        hasil = None

        try:
            if metode == "Image Brightening":
                b = int(self.param_vars[0].get())
                hasil = np.clip(img.astype(np.int32) + b, 0, 255).astype(np.uint8)
                self.tampilkan_histogram_hasil(img, hasil, f"Image Brightening (b={b})")

            elif metode == "Citra Negatif":
                hasil = 255 - img
                self.tampilkan_histogram_hasil(img, hasil, "Citra Negatif")

            elif metode == "Balikan Citra Negatif":
                hasil = 255 - img
                hasil = 255 - hasil  # balikan kembali
                self.tampilkan_histogram_hasil(img, hasil, "Balikan Citra Negatif")

            elif metode == "Transformasi Log":
                c = float(self.param_vars[0].get())
                img_float = img.astype(np.float32)
                hasil = c * np.log1p(img_float)
                hasil = np.clip(hasil / hasil.max() * 255, 0, 255).astype(np.uint8)
                self.tampilkan_histogram_hasil(img, hasil, f"Transformasi Log (c={c})")

            elif metode == "Transformasi Pangkat":
                c = float(self.param_vars[0].get())
                gamma = float(self.param_vars[1].get())
                img_norm = img.astype(np.float32) / 255.0
                hasil = c * np.power(img_norm, gamma)
                hasil = np.clip(hasil * 255, 0, 255).astype(np.uint8)
                self.tampilkan_histogram_hasil(img, hasil,
                                               f"Transformasi Pangkat (c={c}, γ={gamma})")

            elif metode == "Contrast Stretching":
                hasil = self.contrast_stretching(img)
                self.tampilkan_histogram_hasil(img, hasil, "Contrast Stretching")

        except ValueError:
            messagebox.showerror("Error", "Parameter tidak valid, masukkan angka yang benar!")
            return

        if hasil is not None:
            self.tampilkan_canvas(self.canvas_out, hasil)

    def contrast_stretching(self, img):
        if len(img.shape) == 3:
            channels = cv2.split(img)
            stretched = []
            for ch in channels:
                r_min = int(ch.min())
                r_max = int(ch.max())
                if r_max == r_min:
                    stretched.append(ch)
                else:
                    ch_str = ((ch.astype(np.float32) - r_min) /
                              (r_max - r_min) * 255).astype(np.uint8)
                    stretched.append(ch_str)
            return cv2.merge(stretched)
        else:
            r_min = int(img.min())
            r_max = int(img.max())
            if r_max == r_min:
                return img
            return ((img.astype(np.float32) - r_min) /
                    (r_max - r_min) * 255).astype(np.uint8)

    def kembali(self):
        self.root.destroy()
        import main
        main.buka_dashboard()


def buka_tugas2():
    root = tk.Tk()
    app = EnhancementApp(root)
    root.mainloop()


if __name__ == "__main__":
    buka_tugas2()