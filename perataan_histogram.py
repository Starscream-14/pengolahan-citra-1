import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageTk


class EqualizationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tugas 3 - Histogram Equalization")
        self.root.geometry("900x650")
        self.root.configure(bg="white")
        self.img = None
        self.build_ui()

    def build_ui(self):
        tk.Label(self.root, text="Histogram Equalization",
                 font=("Arial", 16, "bold"),
                 bg="white", fg="black").pack(fill=tk.X, pady=10)

        frame_top = tk.Frame(self.root, bg="white", pady=8)
        frame_top.pack(fill=tk.X)

        tk.Button(frame_top, text="Buka Citra", command=self.buka_citra,
                  bg="#e6e6e6", fg="black", padx=12, pady=4).pack(side=tk.LEFT, padx=10)

        tk.Button(frame_top, text="Proses Equalization", command=self.proses,
                  bg="#e6e6e6", fg="black", padx=12, pady=4).pack(side=tk.LEFT, padx=10)

        tk.Button(frame_top, text="Kembali", command=self.kembali,
                  bg="#e6e6e6", fg="black", padx=12, pady=4).pack(side=tk.RIGHT, padx=10)

        self.label_file = tk.Label(frame_top, text="Belum ada citra dipilih",
                                   fg="black", bg="white")
        self.label_file.pack(side=tk.LEFT, padx=10)

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

    def buka_citra(self):
        path = filedialog.askopenfilename(
            title="Pilih Citra",
            filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp *.tif *.tiff")]
        )
        if path:
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

    def equalize_channel(self, channel):
        # Hitung histogram manual
        hist = self.hitung_histogram_manual(channel)
        total_piksel = channel.size

        # Hitung CDF (Cumulative Distribution Function)
        cdf = np.zeros(256, dtype=np.float64)
        cdf[0] = hist[0]
        for i in range(1, 256):
            cdf[i] = cdf[i-1] + hist[i]

        # Normalisasi CDF
        cdf_min = cdf[cdf > 0].min()
        cdf_norm = np.round(
            (cdf - cdf_min) / (total_piksel - cdf_min) * 255
        ).astype(np.uint8)

        # Map piksel menggunakan CDF
        hasil = cdf_norm[channel]
        return hasil

    def proses(self):
        if self.img is None:
            messagebox.showwarning("Peringatan", "Pilih citra terlebih dahulu!")
            return

        img = self.img.copy()

        # Cek grayscale atau berwarna
        if len(img.shape) == 2:
            hasil = self.equalize_channel(img)
        else:
            b, g, r = cv2.split(img)
            # Cek apakah grayscale disimpan sebagai BGR
            if np.array_equal(b, g) and np.array_equal(g, r):
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                hasil_gray = self.equalize_channel(gray)
                hasil = cv2.cvtColor(hasil_gray, cv2.COLOR_GRAY2BGR)
            else:
                # Equalize per channel RGB
                eq_r = self.equalize_channel(r)
                eq_g = self.equalize_channel(g)
                eq_b = self.equalize_channel(b)
                hasil = cv2.merge([eq_b, eq_g, eq_r])

        self.tampilkan_canvas(self.canvas_out, hasil)
        self.tampilkan_histogram_hasil(img, hasil)

    def tampilkan_histogram_hasil(self, img_in, img_out):
        if len(img_in.shape) == 3:
            gray_in = cv2.cvtColor(img_in, cv2.COLOR_BGR2GRAY)
            gray_out = cv2.cvtColor(img_out, cv2.COLOR_BGR2GRAY)
        else:
            gray_in = img_in
            gray_out = img_out

        hist_in = self.hitung_histogram_manual(gray_in)
        hist_out = self.hitung_histogram_manual(gray_out)

        fig, axes = plt.subplots(2, 2, figsize=(12, 8))
        fig.suptitle("Histogram Equalization", fontsize=14)

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
        axes[1,0].set_title("Citra Output (Equalized)")
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

    def kembali(self):
        self.root.destroy()
        import main
        main.buka_dashboard()


def buka_tugas3():
    root = tk.Tk()
    app = EqualizationApp(root)
    root.mainloop()


if __name__ == "__main__":
    buka_tugas3()