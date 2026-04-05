import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageTk

class HistogramApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tugas 1 - Histogram Citra")
        self.root.geometry("800x600")
        self.root.configure(bg="white")
        self.img = None
        self.img_path = None
        self.build_ui()
    
    def build_ui(self):
        tk.Label(self.root, text="Histogram Citra", font=("Arial", 16, "bold"),
                 bg="white", fg="black").pack(fill=tk.X, pady=10)
        
        frame_top = tk.Frame(self.root, pady=10, bg="white")
        frame_top.pack(fill=tk.X)
        
        tk.Button(frame_top, text="Buka Citra", command=self.buka_citra,
                  bg="#e6e6e6", fg="black", padx=15, pady=5).pack(side=tk.LEFT, padx=10)
        
        tk.Button(frame_top, text="Tampilkan Histogram", command=self.tampilkan_histogram,
                  bg="#e6e6e6", fg="black", padx=15, pady=5).pack(side=tk.LEFT, padx=10)

        tk.Button(frame_top, text="Kembali", command=self.kembali,
                  bg="#e6e6e6", fg="black", padx=15, pady=5).pack(side=tk.RIGHT, padx=10)
        
        self.label_file = tk.Label(frame_top, text="Belum ada citra dipilih",
                                   fg="black", bg="white")
        self.label_file.pack(side=tk.LEFT, padx=10)
        
        frame_img = tk.LabelFrame(self.root, text="Preview Citra",
                                  padx=5, pady=5, bg="white", fg="black")
        frame_img.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.canvas_img = tk.Canvas(frame_img, bg="#f5f5f5")
        self.canvas_img.pack(fill=tk.BOTH, expand=True)
    
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
            self.tampilkan_citra()
    
    def tampilkan_citra(self):
        img_rgb = cv2.cvtColor(self.img, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(img_rgb)
        pil_img.thumbnail((400, 300))
        self.tk_img = ImageTk.PhotoImage(pil_img)
        self.canvas_img.update()
        self.canvas_img.create_image(
            self.canvas_img.winfo_width() // 2,
            self.canvas_img.winfo_height() // 2,
            anchor=tk.CENTER, image=self.tk_img
        )
    
    def hitung_histogram_manual(self, channel):
        hist = np.zeros(256, dtype=int)
        flat = channel.flatten()
        for pixel in flat:
            hist[pixel] += 1
        return hist
    
    def tampilkan_histogram(self):
        if self.img is None:
            messagebox.showwarning("Peringatan", "Pilih citra terlebih dahulu!")
            return
        
        if len(self.img.shape) == 2:
            self.histogram_grayscale(self.img)
        else:
            b, g, r = cv2.split(self.img)
            if np.array_equal(b, g) and np.array_equal(g, r):
                gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
                self.histogram_grayscale(gray)
            else:
                self.histogram_berwarna(self.img)

    def kembali(self):
        self.root.destroy()
        import main
        main.buka_dashboard()
    
    def histogram_grayscale(self, img):
        hist = self.hitung_histogram_manual(img)
        
        fig, axes = plt.subplots(1, 2, figsize=(12, 4))
        fig.suptitle("Histogram Grayscale", fontsize=14)
        
        axes[0].imshow(img, cmap='gray')
        axes[0].set_title("Citra Grayscale")
        axes[0].axis('off')
        
        axes[1].bar(range(256), hist, color='gray', width=1)
        axes[1].set_title("Histogram (Manual)")
        axes[1].set_xlabel("Derajat Keabuan (0-255)")
        axes[1].set_ylabel("Jumlah Piksel")
        axes[1].set_xlim([0, 255])
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    def histogram_berwarna(self, img):
        b, g, r = cv2.split(img)
        
        hist_r = self.hitung_histogram_manual(r)
        hist_g = self.hitung_histogram_manual(g)
        hist_b = self.hitung_histogram_manual(b)
        
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        fig, axes = plt.subplots(2, 2, figsize=(12, 8))
        fig.suptitle("Histogram Citra Berwarna (RGB)", fontsize=14)
        
        axes[0,0].imshow(img_rgb)
        axes[0,0].set_title("Citra Asli")
        axes[0,0].axis('off')
        
        axes[0,1].bar(range(256), hist_r, color='red', width=1, alpha=0.7)
        axes[0,1].set_title("Channel Red")
        axes[0,1].set_xlabel("Nilai Piksel (0-255)")
        axes[0,1].set_ylabel("Jumlah Piksel")
        axes[0,1].set_xlim([0, 255])
        axes[0,1].grid(True, alpha=0.3)
        
        axes[1,0].bar(range(256), hist_g, color='green', width=1, alpha=0.7)
        axes[1,0].set_title("Channel Green")
        axes[1,0].set_xlabel("Nilai Piksel (0-255)")
        axes[1,0].set_ylabel("Jumlah Piksel")
        axes[1,0].set_xlim([0, 255])
        axes[1,0].grid(True, alpha=0.3)
        
        axes[1,1].bar(range(256), hist_b, color='blue', width=1, alpha=0.7)
        axes[1,1].set_title("Channel Blue")
        axes[1,1].set_xlabel("Nilai Piksel (0-255)")
        axes[1,1].set_ylabel("Jumlah Piksel")
        axes[1,1].set_xlim([0, 255])
        axes[1,1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()


def buka_tugas1():
    root = tk.Tk()
    app = HistogramApp(root)
    root.mainloop()


if __name__ == "__main__":
    buka_tugas1()