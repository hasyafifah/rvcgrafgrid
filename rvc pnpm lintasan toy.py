import tkinter as tk
from tkinter import messagebox
import tkinter.font as tkfont
import heapq

class SistemAnalisisPewarnaan:
    def __init__(self, root):
        self.root = root
        self.root.title("Analisis Pewarnaan Bilangan Terhubung Pelangi (RVC) pada Graf Grid")
        self.root.geometry("1150x850")
        self.root.configure(bg="#F8F9FA")
        
        self.jumlah_baris = 0
        self.jumlah_kolom = 0
        self.jumlah_warna = 0
        self.matriks_warna = []
        
        self.palet_warna = ["#E2E8F0", "#EF4444"]
        
        self.inisialisasi_antarmuka()

    def inisialisasi_antarmuka(self):
        frame_header = tk.Frame(self.root, bg="#2C3E50", pady=15)
        frame_header.pack(side=tk.TOP, fill=tk.X)
        
        tk.Label(frame_header, text="ANALISIS LINTASAN SIMPUL PELANGI GRAF Pn x Pm", fg="#FFFFFF", bg="#2C3E50", font=("Segoe UI", 16, "bold")).pack()
        tk.Label(frame_header, text="Cek Syarat Lintasan Simpul Pelangi Berpola (Metode Piecewise)", fg="#BDC3C7", bg="#2C3E50", font=("Segoe UI", 10, "italic")).pack()
        
        frame_kontrol = tk.Frame(self.root, bg="#F8F9FA", pady=10)
        frame_kontrol.pack(fill=tk.X, padx=10)
        
        font_label = ("Segoe UI", 10, "bold")
        font_entry = ("Segoe UI", 11, "bold")
        btn_style = {"font": ("Segoe UI", 10, "bold"), "fg": "white", "relief": "flat", "cursor": "hand2", "padx": 15, "pady": 5}
        
        # Baris kontrol: Generate Graf
        frame_baris1 = tk.Frame(frame_kontrol, bg="#F8F9FA")
        frame_baris1.pack(side=tk.TOP, fill=tk.X, pady=(0, 5))
        
        tk.Label(frame_baris1, text="Baris (n):", bg="#F8F9FA", font=font_label).pack(side=tk.LEFT, padx=(0, 5))
        self.input_baris = tk.Entry(frame_baris1, width=5, font=font_entry, justify='center', relief="solid", bd=1)
        self.input_baris.pack(side=tk.LEFT, padx=(0, 20))
        
        tk.Label(frame_baris1, text="Kolom (m):", bg="#F8F9FA", font=font_label).pack(side=tk.LEFT, padx=(0, 5))
        self.input_kolom = tk.Entry(frame_baris1, width=5, font=font_entry, justify='center', relief="solid", bd=1)
        self.input_kolom.pack(side=tk.LEFT, padx=(0, 20))
        
        tk.Button(frame_baris1, text="Proses Graf", bg="#27AE60", command=self.jalankan_sistem_otomatis, **btn_style).pack(side=tk.LEFT)

        # Baris kontrol: Cek Lintasan
        frame_baris2 = tk.Frame(frame_kontrol, bg="#F8F9FA")
        frame_baris2.pack(side=tk.TOP, fill=tk.X, pady=(10, 0))

        tk.Label(frame_baris2, text="Cari Lintasan dari  v (", bg="#F8F9FA", font=font_label, fg="#2980B9").pack(side=tk.LEFT)
        self.input_r1 = tk.Entry(frame_baris2, width=3, font=font_entry, justify='center', relief="solid", bd=1)
        self.input_r1.pack(side=tk.LEFT)
        tk.Label(frame_baris2, text=",", bg="#F8F9FA", font=font_label, fg="#2980B9").pack(side=tk.LEFT)
        self.input_c1 = tk.Entry(frame_baris2, width=3, font=font_entry, justify='center', relief="solid", bd=1)
        self.input_c1.pack(side=tk.LEFT)
        
        tk.Label(frame_baris2, text=")  ke  v (", bg="#F8F9FA", font=font_label, fg="#2980B9").pack(side=tk.LEFT)
        self.input_r2 = tk.Entry(frame_baris2, width=3, font=font_entry, justify='center', relief="solid", bd=1)
        self.input_r2.pack(side=tk.LEFT)
        tk.Label(frame_baris2, text=",", bg="#F8F9FA", font=font_label, fg="#2980B9").pack(side=tk.LEFT)
        self.input_c2 = tk.Entry(frame_baris2, width=3, font=font_entry, justify='center', relief="solid", bd=1)
        self.input_c2.pack(side=tk.LEFT)
        tk.Label(frame_baris2, text=")", bg="#F8F9FA", font=font_label, fg="#2980B9").pack(side=tk.LEFT, padx=(0, 20))

        tk.Button(frame_baris2, text="Cek & Visualisasi Lintasan", bg="#3498DB", command=self.visualisasi_lintasan_spesifik, **btn_style).pack(side=tk.LEFT)

        frame_tengah = tk.Frame(self.root, bg="#F8F9FA")
        frame_tengah.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        panel_kiri = tk.Frame(frame_tengah, bg="#FFFFFF", relief="solid", bd=1)
        panel_kiri.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        tk.Label(panel_kiri, text="Visualisasi Graf", bg="#ECF0F1", font=font_label).pack(fill=tk.X, ipady=5)
        
        kontainer_scroll_kiri = tk.Frame(panel_kiri, bg="#F1F2F6")
        kontainer_scroll_kiri.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        scroll_y_kiri = tk.Scrollbar(kontainer_scroll_kiri, orient="vertical")
        scroll_x_kiri = tk.Scrollbar(kontainer_scroll_kiri, orient="horizontal")
        
        self.kanvas_graf = tk.Canvas(kontainer_scroll_kiri, bg="#FFFFFF", highlightthickness=0, yscrollcommand=scroll_y_kiri.set, xscrollcommand=scroll_x_kiri.set)
        scroll_y_kiri.config(command=self.kanvas_graf.yview)
        scroll_x_kiri.config(command=self.kanvas_graf.xview)
        
        scroll_y_kiri.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x_kiri.pack(side=tk.BOTTOM, fill=tk.X)
        self.kanvas_graf.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        panel_kanan = tk.Frame(frame_tengah, bg="#FFFFFF", relief="solid", bd=1)
        panel_kanan.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        tk.Label(panel_kanan, text="Terminal Log", bg="#ECF0F1", font=font_label).pack(fill=tk.X, ipady=5)
        
        self.teks_log = tk.Text(panel_kanan, font=("Consolas", 10), bg="#1E272E", fg="#00D2D3", relief="flat", padx=10, pady=10)
        self.teks_log.pack(fill=tk.BOTH, expand=True)

    def jalankan_sistem_otomatis(self):
        try:
            self.jumlah_baris = int(self.input_baris.get())
            self.jumlah_kolom = int(self.input_kolom.get())
        except ValueError:
            messagebox.showerror("Error", "Harap masukkan nilai n dan m pakai angka bulat!")
            return
            
        if self.jumlah_baris > self.jumlah_kolom:
            messagebox.showwarning("Aturan Dilanggar", "Nilai baris (n) tidak boleh lebih besar dari kolom (m)!")
            return
            
        n = self.jumlah_baris
        m = self.jumlah_kolom
        
        self.jumlah_warna = n + m - 3
        if self.jumlah_warna < 1:
            self.jumlah_warna = 1
        
        self.matriks_warna = [[0 for _ in range(self.jumlah_kolom)] for _ in range(self.jumlah_baris)]
        self.terapkan_rumus_piecewise()
        self.render_gambar_graf()
        self.eksekusi_verifikasi()

    def terapkan_rumus_piecewise(self):
        n = self.jumlah_baris
        m = self.jumlah_kolom
        rvc_g = self.jumlah_warna
        
        for i in range(n):
            for j in range(m):
                if (i == 0 and j == 0) or (i == 0 and j == m - 1) or \
                   (i == n - 1 and j == 0) or (i == n - 1 and j == m - 1):
                    self.matriks_warna[i][j] = m - 1
                elif i == 0 and 1 <= j <= m - 2:
                    self.matriks_warna[i][j] = j
                elif i == n - 1 and 1 <= j <= m - 2:
                    self.matriks_warna[i][j] = m - 1 - j
                elif j == m - 1 and 1 <= i <= n - 2:
                    self.matriks_warna[i][j] = m - 1 + i
                elif j == 0 and 1 <= i <= n - 2:
                    self.matriks_warna[i][j] = n + m - 2 - i
                elif 1 <= i <= n - 2 and 1 <= j <= m - 2:
                    v_j = rvc_g - 2 * (j // 2)
                    if j % 2 != 0: 
                        self.matriks_warna[i][j] = ((v_j + i - 2) % rvc_g) + 1
                    else:
                        self.matriks_warna[i][j] = ((v_j - i) % rvc_g) + 1

    def catat_log(self, pesan, bersih=False):
        if bersih:
            self.teks_log.delete(1.0, tk.END)
        self.teks_log.insert(tk.END, pesan + "\n")
        self.teks_log.see(tk.END)

    def ambil_nilai_warna(self, r, c):
        return self.matriks_warna[r][c]

    def render_gambar_graf(self, jalur_sorot=None):
        self.kanvas_graf.delete("all")
        if self.jumlah_baris == 0: return
        
        if jalur_sorot is None:
            jalur_sorot = []
            
        def dalam_jalur_edge(r_a, c_a, r_b, c_b):
            if not jalur_sorot: return False
            for i in range(len(jalur_sorot) - 1):
                p1, p2 = jalur_sorot[i], jalur_sorot[i+1]
                if (p1 == (r_a, c_a) and p2 == (r_b, c_b)) or (p1 == (r_b, c_b) and p2 == (r_a, c_a)):
                    return True
            return False

        offset_x = 50
        offset_y = 50
        spasi_titik = 45
        radius = 10

        for r in range(self.jumlah_baris):
            for c in range(self.jumlah_kolom):
                x1 = offset_x + (c * spasi_titik)
                y1 = offset_y + (r * spasi_titik)
                
                if c < self.jumlah_kolom - 1:
                    x2 = offset_x + ((c + 1) * spasi_titik)
                    di_sorot = dalam_jalur_edge(r, c, r, c+1)
                    warna_garis = "#E74C3C" if di_sorot else "#94A3B8"
                    tebal_garis = 5 if di_sorot else 3
                    self.kanvas_graf.create_line(x1, y1, x2, y1, fill=warna_garis, width=tebal_garis)
                
                if r < self.jumlah_baris - 1:
                    y2 = offset_y + ((r + 1) * spasi_titik)
                    di_sorot = dalam_jalur_edge(r, c, r+1, c)
                    warna_garis = "#E74C3C" if di_sorot else "#94A3B8"
                    tebal_garis = 5 if di_sorot else 3
                    self.kanvas_graf.create_line(x1, y1, x1, y2, fill=warna_garis, width=tebal_garis)

        for r in range(self.jumlah_baris):
            for c in range(self.jumlah_kolom):
                x = offset_x + (c * spasi_titik)
                y = offset_y + (r * spasi_titik)
                
                nilai_angka = self.ambil_nilai_warna(r, c)
                
                is_node_sorot = (r, c) in jalur_sorot
                bg_warna = "#FFD700" if is_node_sorot else "#FFFFFF"
                out_warna = "#C0392B" if is_node_sorot else "#1E293B"
                out_tebal = 3 if is_node_sorot else 2
                
                if jalur_sorot and jalur_sorot[0] == (r, c):
                    bg_warna = "#2ECC71"
                elif jalur_sorot and jalur_sorot[-1] == (r, c):
                    bg_warna = "#3498DB"

                self.kanvas_graf.create_oval(x - radius, y - radius, x + radius, y + radius, fill=bg_warna, outline=out_warna, width=out_tebal)
                self.kanvas_graf.create_text(x, y, text=str(nilai_angka) if nilai_angka != 0 else "", font=("Segoe UI", 10, "bold"), fill="#1E293B")
                
                self.kanvas_graf.create_text(x, y + radius + 12, text=f"v({r},{c})", font=("Consolas", 8), fill="#475569")
                
        self.kanvas_graf.configure(scrollregion=self.kanvas_graf.bbox("all"))
    
    def hitung_jarak(self, r1, c1, r2, c2):
        return abs(r1 - r2) + abs(c1 - c2)
        
    def nama_simpul(self, r, c):
        return f"v({r},{c})"

    def identifikasi_lintasan_pelangi(self, r_awal, c_awal, r_tujuan, c_tujuan):
        antrean = []
        identitas_awal = self.nama_simpul(r_awal, c_awal)
        
        # Susunan Prioritas: (Skor Penalti Pola, belokan, panjang_rute, id_unik, r_skrg, c_skrg, arah_sblm, jejak, list_warna, list_simpul)
        # Penalti Pola (indeks ke-0) menjadi prioritas utama untuk memaksa AI mencoba pola garis lurus/spesifik terlebih dahulu.
        counter_id = 0
        heapq.heappush(antrean, (0, 0, 0, counter_id, r_awal, c_awal, -1, [(r_awal, c_awal)], [], [identitas_awal]))
        
        vektor_r = [-1, 1, 0, 0] # 0: Atas, 1: Bawah, 2: Kiri, 3: Kanan
        vektor_c = [0, 0, -1, 1] 
        
        while antrean:
            penalti, belokan, panjang, _, r_skrg, c_skrg, arah_skrg, jejak_koordinat, warna_terekam, simpul_terekam = heapq.heappop(antrean)
            
            for arah in range(4):
                r_baru = r_skrg + vektor_r[arah]
                c_baru = c_skrg + vektor_c[arah]
                
                if 0 <= r_baru < self.jumlah_baris and 0 <= c_baru < self.jumlah_kolom:
                    identitas_baru = self.nama_simpul(r_baru, c_baru)
                    
                    if r_baru == r_tujuan and c_baru == c_tujuan:
                        jejak_koordinat_baru = jejak_koordinat.copy()
                        jejak_koordinat_baru.append((r_baru, c_baru))
                        return jejak_koordinat_baru 
                        
                    if identitas_baru not in simpul_terekam:
                        warna_simpul = self.ambil_nilai_warna(r_baru, c_baru)
                        
                        if warna_simpul > 0 and warna_simpul not in warna_terekam:
                            
                            # ===== PENERAPAN ATURAN POLA PERGERAKAN (PENALTI HEURISTIK) =====
                            tambahan_penalti = 0
                            
                            # Mencegah langkah menjauhi target (diutamakan langkah progresif)
                            if (arah == 0 and r_tujuan > r_skrg) or (arah == 1 and r_tujuan < r_skrg):
                                tambahan_penalti += 20
                            if (arah == 2 and c_tujuan > c_skrg) or (arah == 3 and c_tujuan < c_skrg):
                                tambahan_penalti += 20

                            # 1. Aturan Sama Kolom (Utamakan vertikal lurus)
                            if c_awal == c_tujuan:
                                if arah in [2, 3]: # Menghindari Kiri/Kanan
                                    tambahan_penalti += 50
                                    
                            # 2. Aturan Sama Baris (Utamakan horizontal lurus)
                            elif r_awal == r_tujuan:
                                if arah in [0, 1]: # Menghindari Atas/Bawah
                                    tambahan_penalti += 50
                                    
                            # 3. Aturan Beda Baris dan Kolom (Kasus Spesifik: j < l / Ke Arah Kanan)
                            elif c_awal < c_tujuan: 
                                if r_awal > r_tujuan: # i > k (Target ada di Atas-Kanan)
                                    # Aturan: Titik potong keatas di kolom GANJIL (c % 2 != 0)
                                    if arah == 0 and c_skrg % 2 == 0: 
                                        tambahan_penalti += 100 # Penalti besar jika belok atas di kolom genap
                                        
                                elif r_awal < r_tujuan: # i < k (Target ada di Bawah-Kanan)
                                    # Aturan: Titik potong kebawah di kolom GENAP (c % 2 == 0)
                                    if arah == 1 and c_skrg % 2 != 0:
                                        tambahan_penalti += 100 # Penalti besar jika belok bawah di kolom ganjil

                            # 4. Melindungi Rute untuk kasus j > l (Menyesuaikan dengan logika di atas)
                            elif c_awal > c_tujuan:
                                if r_awal > r_tujuan:
                                    if arah == 0 and c_skrg % 2 == 0: tambahan_penalti += 100
                                elif r_awal < r_tujuan:
                                    if arah == 1 and c_skrg % 2 != 0: tambahan_penalti += 100
                            # ================================================================

                            koleksi_warna_baru = warna_terekam.copy()
                            koleksi_warna_baru.append(warna_simpul)
                            
                            koleksi_simpul_baru = simpul_terekam.copy()
                            koleksi_simpul_baru.append(identitas_baru)
                            
                            jejak_baru = jejak_koordinat.copy()
                            jejak_baru.append((r_baru, c_baru))
                            
                            belokan_baru = belokan
                            if arah_skrg != -1 and arah_skrg != arah:
                                belokan_baru += 1
                                
                            penalti_baru = penalti + tambahan_penalti
                            panjang_baru = panjang + 1
                            counter_id += 1
                            
                            heapq.heappush(antrean, (penalti_baru, belokan_baru, panjang_baru, counter_id, r_baru, c_baru, arah, jejak_baru, koleksi_warna_baru, koleksi_simpul_baru))
        return [] 

    def visualisasi_lintasan_spesifik(self):
        if not self.matriks_warna or self.jumlah_baris == 0:
            messagebox.showwarning("Peringatan", "Harap buat graf dan klik 'Proses Graf' terlebih dahulu!")
            return

        try:
            r1 = int(self.input_r1.get())
            c1 = int(self.input_c1.get())
            r2 = int(self.input_r2.get())
            c2 = int(self.input_c2.get())
        except ValueError:
            messagebox.showerror("Kesalahan Input", "Harap masukkan koodinat simpul menggunakan angka bulat (integer)!")
            return

        if not (0 <= r1 < self.jumlah_baris and 0 <= c1 < self.jumlah_kolom and
                0 <= r2 < self.jumlah_baris and 0 <= c2 < self.jumlah_kolom):
            messagebox.showerror("Error Batas", f"Koordinat di luar jangkauan peta graf!\nMaksimal Baris: 0 s/d {self.jumlah_baris-1}\nMaksimal Kolom: 0 s/d {self.jumlah_kolom-1}")
            return

        if r1 == r2 and c1 == c2:
            messagebox.showinfo("Info", "Titik awal dan tujuan berada di posisi yang sama.")
            return

        jalur_pelangi = self.identifikasi_lintasan_pelangi(r1, c1, r2, c2)

        self.catat_log("\n=======================================================")
        self.catat_log(f">> MEMPROSES PENCARIAN LINTASAN DARI v({r1},{c1}) ke v({r2},{c2})")

        if not jalur_pelangi:
            self.catat_log(" [!] PENCARIAN GAGAL: Tidak ditemukan jalur pelangi untuk simpul ini.")
            messagebox.showerror("Gagal", f"Lintasan pelangi dari v({r1},{c1}) ke v({r2},{c2}) tidak ditemukan!")
        else:
            teks_jejak = " -> ".join([self.nama_simpul(r, c) for r, c in jalur_pelangi])
            self.catat_log(f" [V] PENCARIAN SUKSES! Lintasan Terverifikasi:\n     {teks_jejak}")
            
            self.render_gambar_graf(jalur_sorot=jalur_pelangi)

    def eksekusi_verifikasi(self):
        self.catat_log(f"=== INISIASI ANALISIS GRAF P{self.jumlah_baris} x P{self.jumlah_kolom} (Rvc(G): {self.jumlah_warna} WARNA) ===", bersih=True)
        self.catat_log(">> Menggunakan Algoritma Pewarnaan Piecewise dan Pola Pencarian Fleksibel\n")
        
        status_validitas = True
        
        for r in range(self.jumlah_baris):
            for c in range(self.jumlah_kolom):
                if self.ambil_nilai_warna(r, c) <= 0:
                    messagebox.showwarning("Inkompresibilitas Data", f"Peringatan: Simpul {self.nama_simpul(r,c)} tidak mendapat warna valid. Verifikasi dibatalkan.")
                    return

        self.catat_log("\n[PENGUJIAN MASSAL] Memeriksa Syarat RVC Seluruh Titik Graf...")
        
        for r1 in range(self.jumlah_baris):
            for c1 in range(self.jumlah_kolom):
                for r2 in range(self.jumlah_baris):
                    for c2 in range(self.jumlah_kolom):
                        indeks_1 = (r1 * self.jumlah_kolom) + c1
                        indeks_2 = (r2 * self.jumlah_kolom) + c2
                        
                        if (indeks_1 < indeks_2) and (self.hitung_jarak(r1, c1, r2, c2) > 1):
                            simpul_awal = self.nama_simpul(r1, c1)
                            simpul_akhir = self.nama_simpul(r2, c2)
                            
                            rute_pelangi = self.identifikasi_lintasan_pelangi(r1, c1, r2, c2)
                            
                            if not rute_pelangi:
                                self.catat_log(f" [!] ANOMALI: Lintasan pelangi antara {simpul_awal} dan {simpul_akhir} tidak ditemukan.")
                                status_validitas = False
                                break
                            else:
                                teks_jejak = " -> ".join([self.nama_simpul(r, c) for r, c in rute_pelangi])
                                self.catat_log(f" > Rute Terverifikasi ({simpul_awal} ke {simpul_akhir}): {teks_jejak}")
                                
                    if not status_validitas: break
                if not status_validitas: break
            if not status_validitas: break
        
        self.catat_log("\n-------------------------------------------------------------")
        if status_validitas:
            self.catat_log("[KESIMPULAN AKHIR] KONFIGURASI PEWARNAAN VALID.")
            messagebox.showinfo("Verifikasi Berhasil", "Analisis awal selesai! Seluruh titik memenuhi syarat pelangi.\n\nLintasan utama akan memprioritaskan pola gerakan khusus. Jika pola utama menabrak warna berulang, ia akan menemukan lintasan berliku yang memenuhi syarat pelangi.")
        else:
            self.catat_log("[KESIMPULAN AKHIR] KONFIGURASI PEWARNAAN GAGAL.")
            messagebox.showerror("Verifikasi Gagal", "Pewarnaan ini tidak valid (Gagal memenuhi syarat koneksi pelangi).")

if __name__ == "__main__":
    jendela_aplikasi = tk.Tk()
    program_riset = SistemAnalisisPewarnaan(jendela_aplikasi)
    jendela_aplikasi.mainloop()