import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog
from datetime import datetime
import threading
import time
import os
from collections import Counter

HARJOITUSOHJEET_TIEDOSTO = "harjoitusohjeet.txt"
PAIVAKIRJA_TIEDOSTO = "urheilupaivakirja.txt"

class Urheilupaivakirja:
    def __init__(self, root):
        self.root = root
        self.root.title("Urheilupäiväkirja")

        # --- Päiväkirjamerkintä ---
        tk.Label(root, text="Päiväkirjamerkintä", font=('Helvetica', 14, 'bold')).pack()

        self.diary_text = scrolledtext.ScrolledText(root, width=50, height=8)
        self.diary_text.pack()

        tk.Button(root, text="Tallenna merkintä", command=self.tallenna_merkinta).pack(pady=5)
        tk.Button(root, text="Näytä vanhat merkinnät", command=self.nayta_merkinnat).pack(pady=5)

        # --- Harjoitusohjeet ---
        tk.Label(root, text="Harjoitusohjeet", font=('Helvetica', 14, 'bold')).pack(pady=(20, 5))

        self.ohjeet_text = scrolledtext.ScrolledText(root, width=50, height=6)
        self.ohjeet_text.pack()
        self.lataa_harjoitusohjeet()

        tk.Button(root, text="Tallenna ohjeet", command=self.tallenna_ohjeet).pack(pady=5)

        # --- Ajastin ---
        tk.Label(root, text="Ajastin (sekunteina):", font=('Helvetica', 12)).pack(pady=(20, 5))

        self.timer_entry = tk.Entry(root)
        self.timer_entry.pack()

        tk.Button(root, text="Käynnistä ajastin", command=self.kaynnista_ajastin).pack(pady=5)
        self.timer_display = tk.Label(root, text="", font=("Helvetica", 12))
        self.timer_display.pack()

        # --- Statistiikka ---
        tk.Button(root, text="Näytä statistiikka", command=self.nayta_statistiikka).pack(pady=(20, 5))

    def tallenna_merkinta(self):
        merkinta = self.diary_text.get("1.0", tk.END).strip()
        if merkinta:
            aika = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(PAIVAKIRJA_TIEDOSTO, "a", encoding='utf-8') as f:
                f.write(f"{aika}\n{merkinta}\n\n")
            self.diary_text.delete("1.0", tk.END)
            messagebox.showinfo("Tallennettu", "Merkintä tallennettu.")
        else:
            messagebox.showwarning("Virhe", "Et voi tallentaa tyhjää merkintää.")

    def nayta_merkinnat(self):
        if not os.path.exists(PAIVAKIRJA_TIEDOSTO):
            messagebox.showinfo("Ei merkintöjä", "Ei aiempia merkintöjä.")
            return

        with open(PAIVAKIRJA_TIEDOSTO, "r", encoding='utf-8') as f:
            sisalto = f.read()

        ikkuna = tk.Toplevel(self.root)
        ikkuna.title("Merkinnät")
        teksti = scrolledtext.ScrolledText(ikkuna, width=70, height=20)
        teksti.pack()
        teksti.insert(tk.END, sisalto)
        teksti.config(state='disabled')

    def lataa_harjoitusohjeet(self):
        if os.path.exists(HARJOITUSOHJEET_TIEDOSTO):
            with open(HARJOITUSOHJEET_TIEDOSTO, "r", encoding='utf-8') as f:
                sisalto = f.read()
        else:
            sisalto = "1. Tee 3 x 15 punnerrusta\n2. Tee 3 x 20 kyykkyä\n3. Juokse 5 km\n"
        self.ohjeet_text.delete("1.0", tk.END)
        self.ohjeet_text.insert(tk.END, sisalto)

    def tallenna_ohjeet(self):
        sisalto = self.ohjeet_text.get("1.0", tk.END).strip()
        with open(HARJOITUSOHJEET_TIEDOSTO, "w", encoding='utf-8') as f:
            f.write(sisalto)
        messagebox.showinfo("Tallennettu", "Harjoitusohjeet tallennettu.")

    def kaynnista_ajastin(self):
        try:
            sekunnit = int(self.timer_entry.get())
            threading.Thread(target=self.ajastin, args=(sekunnit,), daemon=True).start()
        except ValueError:
            messagebox.showerror("Virhe", "Syötä kelvollinen sekuntimäärä.")

    def ajastin(self, sekunnit):
        while sekunnit >= 0:
            mins, secs = divmod(sekunnit, 60)
            time_format = f"{mins:02d}:{secs:02d}"
            self.timer_display.config(text=time_format)
            time.sleep(1)
            sekunnit -= 1
        self.timer_display.config(text="Aika loppui!")
        messagebox.showinfo("Ajastin", "Ajastin päättyi.")

        def nayta_statistiikka(self):
            if not os.path.exists(PAIVAKIRJA_TIEDOSTO):
                messagebox.showinfo("Ei dataa", "Ei merkintöjä statistiikkaa varten.")
                return

        with open(PAIVAKIRJA_TIEDOSTO, "r", encoding='utf-8') as f:
            rivit = f.readlines()

        paivamaarat = [rivi.split()[0] for rivi in rivit if self.on_pvm_rivi(rivi)]
        laskuri = Counter(paivamaarat)

        if not laskuri:
            messagebox.showinfo("Ei dataa", "Ei merkintöjä tilastoihin.")
            return

        stats_window = tk.Toplevel(self.root)
        stats_window.title("Tilastot - Merkintöjen määrä")

        tk.Label(stats_window, text="Päivämäärä\tMerkintöjä", font=('Helvetica', 12, 'bold')).pack()

        for pvm, maara in sorted(laskuri.items()):
            tk.Label(stats_window, text=f"{pvm}\t{maara}").pack(anchor='w')


    def on_pvm_rivi(self, rivi):
        try:
            datetime.strptime(rivi.strip(), "%Y-%m-%d %H:%M:%S")
            return True
        except:
            return False

if __name__ == "__main__":
    root = tk.Tk()
    app = Urheilupaivakirja(root)
    root.mainloop()
