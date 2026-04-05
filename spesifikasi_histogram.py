import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageTk


class HistogramSpecificationApp:
	def __init__(self, root):
		self.root = root
		self.root.title("Tugas 4 - Histogram Specification")
		self.root.geometry("980x700")
		self.root.configure(bg="white")

		self.img_input = None
		self.img_ref = None
		self.img_hasil = None

		self.build_ui()

	def build_ui(self):
		tk.Label(self.root, text="Histogram Specification (Matching)",
				 font=("Arial", 16, "bold"),
				 bg="white", fg="black").pack(fill=tk.X, pady=10)

		frame_top = tk.Frame(self.root, bg="white", pady=8)
		frame_top.pack(fill=tk.X)

		tk.Button(frame_top, text="Buka Citra Input", command=self.buka_citra_input,
				  bg="#e6e6e6", fg="black", padx=12, pady=4).pack(side=tk.LEFT, padx=8)

		tk.Button(frame_top, text="Buka Citra Referensi", command=self.buka_citra_referensi,
				  bg="#e6e6e6", fg="black", padx=12, pady=4).pack(side=tk.LEFT, padx=8)

		tk.Button(frame_top, text="Proses Matching", command=self.proses,
				  bg="#e6e6e6", fg="black", padx=12, pady=4).pack(side=tk.LEFT, padx=8)

		tk.Button(frame_top, text="Tampilkan 6 Output", command=self.tampilkan_hasil,
				  bg="#e6e6e6", fg="black", padx=12, pady=4).pack(side=tk.LEFT, padx=8)

		tk.Button(frame_top, text="Kembali", command=self.kembali,
				  bg="#e6e6e6", fg="black", padx=12, pady=4).pack(side=tk.RIGHT, padx=8)

		self.label_info = tk.Label(frame_top, text="Pilih citra input dan citra referensi",
								   fg="black", bg="white")
		self.label_info.pack(side=tk.LEFT, padx=10)

		frame_preview = tk.Frame(self.root, bg="white")
		frame_preview.pack(fill=tk.BOTH, expand=True, padx=10, pady=8)

		frame_in = tk.LabelFrame(frame_preview, text="Citra Input",
								 bg="white", fg="black", padx=5, pady=5)
		frame_in.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
		self.canvas_in = tk.Canvas(frame_in, bg="#f5f5f5")
		self.canvas_in.pack(fill=tk.BOTH, expand=True)

		frame_ref = tk.LabelFrame(frame_preview, text="Citra Referensi",
							  bg="white", fg="black", padx=5, pady=5)
		frame_ref.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
		self.canvas_ref = tk.Canvas(frame_ref, bg="#f5f5f5")
		self.canvas_ref.pack(fill=tk.BOTH, expand=True)

		frame_out = tk.LabelFrame(frame_preview, text="Citra Hasil",
							  bg="white", fg="black", padx=5, pady=5)
		frame_out.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
		self.canvas_out = tk.Canvas(frame_out, bg="#f5f5f5")
		self.canvas_out.pack(fill=tk.BOTH, expand=True)

	def buka_citra_input(self):
		path = filedialog.askopenfilename(
			title="Pilih Citra Input",
			filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp *.tif *.tiff")]
		)
		if path:
			self.img_input = cv2.imread(path, cv2.IMREAD_COLOR)
			self.tampilkan_canvas(self.canvas_in, self.img_input)
			self.perbarui_label_status()

	def buka_citra_referensi(self):
		path = filedialog.askopenfilename(
			title="Pilih Citra Referensi",
			filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp *.tif *.tiff")]
		)
		if path:
			self.img_ref = cv2.imread(path, cv2.IMREAD_COLOR)
			self.tampilkan_canvas(self.canvas_ref, self.img_ref)
			self.perbarui_label_status()

	def tampilkan_canvas(self, canvas, img_bgr):
		img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
		pil_img = Image.fromarray(img_rgb)
		pil_img.thumbnail((300, 250))
		tk_img = ImageTk.PhotoImage(pil_img)
		canvas.image = tk_img
		canvas.update()
		canvas.create_image(
			canvas.winfo_width() // 2,
			canvas.winfo_height() // 2,
			anchor=tk.CENTER,
			image=tk_img
		)

	def hitung_histogram_manual(self, channel):
		hist = np.zeros(256, dtype=np.int64)
		for pixel in channel.flatten():
			hist[pixel] += 1
		return hist

	def hitung_cdf(self, channel):
		hist = self.hitung_histogram_manual(channel)
		cdf = np.cumsum(hist).astype(np.float64)
		cdf /= cdf[-1]
		return cdf

	def buat_lookup_matching(self, cdf_src, cdf_ref):
		lookup = np.zeros(256, dtype=np.uint8)
		j = 0
		for i in range(256):
			while j < 255 and cdf_ref[j] < cdf_src[i]:
				j += 1
			lookup[i] = j
		return lookup

	def match_channel(self, src_channel, ref_channel):
		cdf_src = self.hitung_cdf(src_channel)
		cdf_ref = self.hitung_cdf(ref_channel)
		lookup = self.buat_lookup_matching(cdf_src, cdf_ref)
		return lookup[src_channel]

	def proses(self):
		if self.img_input is None or self.img_ref is None:
			messagebox.showwarning("Peringatan", "Pilih citra input dan citra referensi terlebih dahulu!")
			return

		if self.img_input.shape[:2] != self.img_ref.shape[:2]:
			messagebox.showerror("Error", "Ukuran citra input dan referensi harus sama!")
			return

		in_b, in_g, in_r = cv2.split(self.img_input)
		ref_b, ref_g, ref_r = cv2.split(self.img_ref)

		# Jika ketiga channel identik, perlakukan sebagai grayscale.
		if np.array_equal(in_b, in_g) and np.array_equal(in_g, in_r) and \
		   np.array_equal(ref_b, ref_g) and np.array_equal(ref_g, ref_r):
			out_gray = self.match_channel(in_b, ref_b)
			self.img_hasil = cv2.cvtColor(out_gray, cv2.COLOR_GRAY2BGR)
		else:
			out_b = self.match_channel(in_b, ref_b)
			out_g = self.match_channel(in_g, ref_g)
			out_r = self.match_channel(in_r, ref_r)
			self.img_hasil = cv2.merge([out_b, out_g, out_r])

		self.tampilkan_canvas(self.canvas_out, self.img_hasil)
		messagebox.showinfo("Sukses", "Histogram specification selesai diproses.")

	def plot_histogram(self, ax, img_bgr, judul):
		b, g, r = cv2.split(img_bgr)
		if np.array_equal(b, g) and np.array_equal(g, r):
			hist = self.hitung_histogram_manual(b)
			ax.bar(range(256), hist, color="gray", width=1)
			ax.set_ylabel("Jumlah Piksel")
		else:
			hist_r = self.hitung_histogram_manual(r)
			hist_g = self.hitung_histogram_manual(g)
			hist_b = self.hitung_histogram_manual(b)
			ax.plot(hist_r, color="red", label="R", linewidth=1.2)
			ax.plot(hist_g, color="green", label="G", linewidth=1.2)
			ax.plot(hist_b, color="blue", label="B", linewidth=1.2)
			ax.legend(loc="upper right", fontsize=8)
			ax.set_ylabel("Jumlah Piksel")

		ax.set_title(judul)
		ax.set_xlabel("Nilai Intensitas (0-255)")
		ax.set_xlim([0, 255])
		ax.grid(True, alpha=0.3)

	def tampilkan_hasil(self):
		if self.img_input is None or self.img_ref is None:
			messagebox.showwarning("Peringatan", "Pilih citra input dan citra referensi terlebih dahulu!")
			return

		if self.img_hasil is None:
			messagebox.showwarning("Peringatan", "Jalankan proses matching terlebih dahulu!")
			return

		fig, axes = plt.subplots(3, 2, figsize=(12, 12))
		fig.suptitle("Tugas 4 - Histogram Specification", fontsize=14)

		axes[0, 0].imshow(cv2.cvtColor(self.img_input, cv2.COLOR_BGR2RGB))
		axes[0, 0].set_title("1. Citra Input")
		axes[0, 0].axis("off")

		self.plot_histogram(axes[0, 1], self.img_input, "2. Histogram Citra Input")

		axes[1, 0].imshow(cv2.cvtColor(self.img_ref, cv2.COLOR_BGR2RGB))
		axes[1, 0].set_title("3. Citra Referensi")
		axes[1, 0].axis("off")

		self.plot_histogram(axes[1, 1], self.img_ref, "4. Histogram Citra Referensi")

		axes[2, 0].imshow(cv2.cvtColor(self.img_hasil, cv2.COLOR_BGR2RGB))
		axes[2, 0].set_title("5. Citra Hasil Histogram Specification")
		axes[2, 0].axis("off")

		self.plot_histogram(axes[2, 1], self.img_hasil,
							"6. Histogram Citra Hasil Histogram Specification")

		plt.tight_layout()
		plt.show()

	def perbarui_label_status(self):
		input_ok = self.img_input is not None
		ref_ok = self.img_ref is not None

		if input_ok and ref_ok:
			self.label_info.config(text="Input dan referensi sudah dipilih.", fg="black")
		elif input_ok:
			self.label_info.config(text="Citra input dipilih. Pilih citra referensi.", fg="black")
		elif ref_ok:
			self.label_info.config(text="Citra referensi dipilih. Pilih citra input.", fg="black")
		else:
			self.label_info.config(text="Pilih citra input dan citra referensi", fg="black")

	def kembali(self):
		self.root.destroy()
		import main

		main.buka_dashboard()


def buka_tugas4():
	root = tk.Tk()
	app = HistogramSpecificationApp(root)
	root.mainloop()


if __name__ == "__main__":
	buka_tugas4()
