import streamlit as st
import heapq
import matplotlib.pyplot as plt

# ==========================================
# KELAS LOGIKA ALGORITMA RVC (Tanpa UI)
# ==========================================
class SistemAnalisisPewarnaan:
    def __init__(self, jumlah_baris, jumlah_kolom):
        self.jumlah_baris = jumlah_baris
        self.jumlah_kolom = jumlah_kolom
        
        # Hitung jumlah warna (Rvc)
        self.jumlah_warna = jumlah_baris + jumlah_kolom - 3
        if self.jumlah_warna < 1:
            self.jumlah_warna = 1
            
        self.matriks_warna = [[0 for _ in range(self.jumlah_kolom)] for _ in range(self.jumlah_baris)]
        self.terapkan_rumus_piecewise()

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

    def ambil_nilai_warna(self, r, c):
        return self.matriks_warna[r][c]

    def hitung_jarak(self, r1, c1, r2, c2):
        return abs(r1 - r2) + abs(c1 - c2)
        
    def nama_simpul(self, r, c):
        return f"v({r},{c})"

    def identifikasi_lintasan_pelangi(self, r_awal, c_awal, r_tujuan, c_tujuan):
        antrean = []
        identitas_awal = self.nama_simpul(r_awal, c_awal)
        
        # Susunan Prioritas: (Skor Penalti Pola, belokan, panjang_rute, id_unik, r_skrg, c_skrg, arah_sblm, jejak, list_warna, list_simpul)
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
                            
                            # Mencegah langkah menjauhi target
                            if (arah == 0 and r_tujuan > r_skrg) or (arah == 1 and r_tujuan < r_skrg): tambahan_penalti += 20
                            if (arah == 2 and c_tujuan > c_skrg) or (arah == 3 and c_tujuan < c_skrg): tambahan_penalti += 20

                            # 1. Aturan Sama Kolom (Utamakan vertikal lurus)
                            if c_awal == c_tujuan and arah in [2, 3]: tambahan_penalti += 50
                            # 2. Aturan Sama Baris (Utamakan horizontal lurus)
                            elif r_awal == r_tujuan and arah in [0, 1]: tambahan_penalti += 50
                            # 3. Aturan Beda Baris dan Kolom (j < l)
                            elif c_awal < c_tujuan: 
                                if r_awal > r_tujuan and arah == 0 and c_skrg % 2 == 0: tambahan_penalti += 100
                                elif r_awal < r_tujuan and arah == 1 and c_skrg % 2 != 0: tambahan_penalti += 100
                            # 4. Melindungi Rute untuk kasus j > l 
                            elif c_awal > c_tujuan:
                                if r_awal > r_tujuan and arah == 0 and c_skrg % 2 == 0: tambahan_penalti += 100
                                elif r_awal < r_tujuan and arah == 1 and c_skrg % 2 != 0: tambahan_penalti += 100

                            koleksi_warna_baru = warna_terekam.copy()
                            koleksi_warna_baru.append(warna_simpul)
                            koleksi_simpul_baru = simpul_terekam.copy()
                            koleksi_simpul_baru.append(identitas_baru)
                            jejak_baru = jejak_koordinat.copy()
                            jejak_baru.append((r_baru, c_baru))
                            
                            belokan_baru = belokan if arah_skrg == -1 or arah_skrg == arah else belokan + 1
                            counter_id += 1
                            
                            heapq.heappush(antrean, (penalti + tambahan_penalti, belokan_baru, panjang + 1, counter_id, r_baru, c_baru, arah, jejak_baru, koleksi_warna_baru, koleksi_simpul_baru))
        return []

# ==========================================
# FUNGSI RENDER GRAF (MATPLOTLIB)
# ==========================================
def buat_gambar_graf(sistem, jalur_sorot=None):
    fig, ax = plt.subplots(figsize=(max(6, sistem.jumlah_kolom * 1.5), max(5, sistem.jumlah_baris * 1.5)))
    
    if not jalur_sorot: jalur_sorot = []
    
    def dalam_jalur_edge(r_a, c_a, r_b, c_b):
        for i in range(len(jalur_sorot) - 1):
            p1, p2 = jalur_sorot[i], jalur_sorot[i+1]
            if (p1 == (r_a, c_a) and p2 == (r_b, c_b)) or (p1 == (r_b, c_b) and p2 == (r_a, c_a)):
                return True
        return False

    # Gambar Edge (Garis)
    for r in range(sistem.jumlah_baris):
        for c in range(sistem.jumlah_kolom):
            if c < sistem.jumlah_kolom - 1:
                sorot = dalam_jalur_edge(r, c, r, c+1)
                ax.plot([c, c+1], [-r, -r], color="#E74C3C" if sorot else "#94A3B8", lw=4 if sorot else 1.5, zorder=1)
            if r < sistem.jumlah_baris - 1:
                sorot = dalam_jalur_edge(r, c, r+1, c)
                ax.plot([c, c], [-r, -(r+1)], color="#E74C3C" if sorot else "#94A3B8", lw=4 if sorot else 1.5, zorder=1)

    # Gambar Node (Simpul)
    for r in range(sistem.jumlah_baris):
        for c in range(sistem.jumlah_kolom):
            nilai_angka = sistem.ambil_nilai_warna(r, c)
            is_node_sorot = (r, c) in jalur_sorot
            
            bg_warna = "#FFD700" if is_node_sorot else "#FFFFFF"
            out_warna = "#C0392B" if is_node_sorot else "#1E293B"
            
            if jalur_sorot and jalur_sorot[0] == (r, c): bg_warna = "#2ECC71" # Hijau untuk Start
            elif jalur_sorot and jalur_sorot[-1] == (r, c): bg_warna = "#3498DB" # Biru untuk End
            
            ax.scatter(c, -r, s=800, color=bg_warna, edgecolors=out_warna, linewidths=2 if is_node_sorot else 1.5, zorder=2)
            ax.text(c, -r, str(nilai_angka) if nilai_angka != 0 else "", ha='center', va='center', fontsize=11, fontweight='bold', color="#1E293B", zorder=3)
            ax.text(c, -r - 0.25, f"v({r},{c})", ha='center', va='center', fontsize=9, color="#475569", zorder=3)

    ax.axis('off')
    return fig

# ==========================================
# ANTARMUKA WEB STREAMLIT
# ==========================================
st.set_page_config(page_title="Analisis RVC Graf", layout="wide")

st.markdown("""
<style>
    .stButton>button { width: 100%; font-weight: bold; }
    .log-box { font-family: monospace; background-color: #1E272E; color: #00D2D3; padding: 10px; border-radius: 5px; height: 400px; overflow-y: scroll; white-space: pre-wrap;}
</style>
""", unsafe_allow_html=True)

# Inisialisasi State
if 'sistem' not in st.session_state: st.session_state.sistem = None
if 'log_text' not in st.session_state: st.session_state.log_text = ""
if 'jalur' not in st.session_state: st.session_state.jalur = []

def catat_log(pesan, bersih=False):
    if bersih: st.session_state.log_text = pesan + "\n"
    else: st.session_state.log_text += pesan + "\n"

# Header
st.title("🌈 Analisis Lintasan Simpul Pelangi Graf Pn x Pm")
st.caption("Cek Syarat Lintasan Simpul Pelangi Berpola (Metode Piecewise)")
st.divider()

# Panel Kontrol Atas
col_n, col_m, col_btn = st.columns([1, 1, 2])
with col_n: input_n = st.number_input("Baris (n):", min_value=1, value=4, step=1)
with col_m: input_m = st.number_input("Kolom (m):", min_value=1, value=5, step=1)
with col_btn:
    st.write("")
    st.write("")
    if st.button("Proses Graf", type="primary"):
        if input_n > input_m:
            st.warning("Aturan Dilanggar: Nilai baris (n) tidak boleh lebih besar dari kolom (m)!")
        else:
            st.session_state.sistem = SistemAnalisisPewarnaan(input_n, input_m)
            st.session_state.jalur = []
            catat_log(f"=== INISIASI ANALISIS GRAF P{input_n} x P{input_m} (Rvc(G): {st.session_state.sistem.jumlah_warna} WARNA) ===", bersih=True)
            catat_log(">> Menggunakan Algoritma Pewarnaan Piecewise dan Pola Pencarian Fleksibel\n")

if st.session_state.sistem:
    st.markdown("---")
    col_kiri, col_kanan = st.columns([1.2, 1])
    
    with col_kiri:
        st.subheader("Visualisasi Graf")
        
        # Kontrol Cek Lintasan Spesifik
        c1, c2, c3, c4, c5 = st.columns([1, 1, 1, 1, 2])
        n_max, m_max = st.session_state.sistem.jumlah_baris - 1, st.session_state.sistem.jumlah_kolom - 1
        with c1: r1 = st.number_input("Awal (r)", min_value=0, max_value=n_max, value=0)
        with c2: c1_val = st.number_input("Awal (c)", min_value=0, max_value=m_max, value=0)
        with c3: r2 = st.number_input("Tujuan (r)", min_value=0, max_value=n_max, value=n_max)
        with c4: c2_val = st.number_input("Tujuan (c)", min_value=0, max_value=m_max, value=m_max)
        with c5:
            st.write("")
            st.write("")
            if st.button("Cek Lintasan", use_container_width=True):
                if r1 == r2 and c1_val == c2_val:
                    st.info("Titik awal dan tujuan berada di posisi yang sama.")
                else:
                    catat_log(f"\n=======================================================\n>> MEMPROSES PENCARIAN LINTASAN DARI v({r1},{c1_val}) ke v({r2},{c2_val})")
                    rute = st.session_state.sistem.identifikasi_lintasan_pelangi(r1, c1_val, r2, c2_val)
                    if not rute:
                        catat_log(" [!] PENCARIAN GAGAL: Tidak ditemukan jalur pelangi untuk simpul ini.")
                        st.error("Lintasan pelangi tidak ditemukan!")
                        st.session_state.jalur = []
                    else:
                        teks_jejak = " -> ".join([st.session_state.sistem.nama_simpul(r, c) for r, c in rute])
                        catat_log(f" [V] PENCARIAN SUKSES! Lintasan Terverifikasi:\n     {teks_jejak}")
                        st.session_state.jalur = rute
                        st.success("Jalur Ditemukan!")

        # Render Gambar
        fig = buat_gambar_graf(st.session_state.sistem, st.session_state.jalur)
        st.pyplot(fig)

    with col_kanan:
        st.subheader("Terminal Log")
        if st.button("Verifikasi Massal (Semua Titik)", type="secondary"):
            sistem = st.session_state.sistem
            catat_log("\n[PENGUJIAN MASSAL] Memeriksa Syarat RVC Seluruh Titik Graf...")
            status_validitas = True
            
            prog = st.progress(0)
            total = (sistem.jumlah_baris * sistem.jumlah_kolom) ** 2
            curr = 0
            
            for row1 in range(sistem.jumlah_baris):
                for col1 in range(sistem.jumlah_kolom):
                    for row2 in range(sistem.jumlah_baris):
                        for col2 in range(sistem.jumlah_kolom):
                            idx1 = (row1 * sistem.jumlah_kolom) + col1
                            idx2 = (row2 * sistem.jumlah_kolom) + col2
                            
                            if (idx1 < idx2) and (sistem.hitung_jarak(row1, col1, row2, col2) > 1):
                                rute = sistem.identifikasi_lintasan_pelangi(row1, col1, row2, col2)
                                if not rute:
                                    catat_log(f" [!] ANOMALI: Lintasan dari v({row1},{col1}) ke v({row2},{col2}) gagal.")
                                    status_validitas = False
                                    break
                            curr += 1
                            if curr % 50 == 0: prog.progress(min(curr / total, 1.0))
                            
                        if not status_validitas: break
                    if not status_validitas: break
                if not status_validitas: break
                
            prog.progress(1.0)
            catat_log("\n-------------------------------------------------------------")
            if status_validitas:
                catat_log("[KESIMPULAN AKHIR] KONFIGURASI PEWARNAAN VALID.")
                st.success("Verifikasi Berhasil! Seluruh titik memenuhi syarat.")
            else:
                catat_log("[KESIMPULAN AKHIR] KONFIGURASI PEWARNAAN GAGAL.")
                st.error("Verifikasi Gagal! Ada pasangan titik yang tidak terhubung.")
        
        # Tampilkan Log di div custom HTML agar bisa scroll
        st.markdown(f'<div class="log-box">{st.session_state.log_text}</div>', unsafe_allow_html=True)
else:
    st.info("Silakan tentukan ukuran graf (Baris & Kolom) lalu klik 'Proses Graf' di atas.")
