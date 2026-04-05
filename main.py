import tkinter as tk
from tkinter import ttk

class Dashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Pengolahan Citra Digital")
        self.root.geometry("800x500")
        self.root.configure(bg="white")
        self.root.resizable(False, False)
        
        self.build_ui()
    
    def build_ui(self):

        tk.Label(self.root, text="Pengolahan Citra Digital",
                 font=("Arial", 20, "bold"),
                 bg="white", fg="black").pack(pady=30)
        
        tk.Label(self.root, text="Pilih menu dari dropdown di bawah",
                 font=("Arial", 10),
                 bg="white", fg="black").pack()
        
        frame_menu = tk.Frame(self.root, bg="white")
        frame_menu.pack(pady=20)
        
        tk.Label(frame_menu, text="Menu:", bg="white",
             fg="black", font=("Arial", 12)).grid(row=0, column=0, padx=10)
        
        self.pilihan = tk.StringVar()
        self.pilihan.set("--- Pilih Tugas ---")
        
        menu_list = [
            "Tugas 1 - Histogram Citra",
            "Tugas 2 - Perbaikan Kualitas Citra",
            "Tugas 3 - Perataan Histogram",
            "Tugas 4 - Spesifikasi Histogram",
        ]
        
        self.dropdown = ttk.Combobox(frame_menu, textvariable=self.pilihan,
                                     values=menu_list, width=35,
                                     state="readonly", font=("Arial", 11))
        self.dropdown.grid(row=0, column=1, padx=10)
        
        tk.Button(self.root, text="▶ Buka", command=self.buka_tugas,
                  bg="#e6e6e6", fg="black", font=("Arial", 12, "bold"),
                  padx=20, pady=8).pack(pady=10)
        
        self.label_status = tk.Label(self.root, text="",
                                     bg="white", fg="black")
        self.label_status.pack()
    
    def buka_tugas(self):
        pilihan = self.pilihan.get()
        
        if pilihan == "-- Pilih Tugas --":
            self.label_status.config(text="Pilih tugas terlebih dahulu!", fg="red")
            return
        
        self.root.destroy()
        
        if "Tugas 1" in pilihan:
            import histogram_citra
            histogram_citra.buka_tugas1()
        elif "Tugas 2" in pilihan:
            import perbaikan_citra
            perbaikan_citra.buka_tugas2()
        elif "Tugas 3" in pilihan:
            import perataan_histogram
            perataan_histogram.buka_tugas3()
        elif "Tugas 4" in pilihan:
            import spesifikasi_histogram
            spesifikasi_histogram.buka_tugas4()

def buka_dashboard():
    root = tk.Tk()
    app = Dashboard(root)
    root.mainloop()

if __name__ == "__main__":
    buka_dashboard()