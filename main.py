import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import socket
import threading
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ---------------- DNS LIST ----------------
DEFAULT_DNS_SERVERS = {
    'Google': '8.8.8.8',
    'Cloudflare': '1.1.1.1',
    'OpenDNS': '208.67.222.222',
    'Quad9': '9.9.9.9'
}

# ---------------- THEME ----------------
THEME = {
    'bg': '#1e1e1e',
    'card': '#2b2b2b',
    'fg': '#ffffff',
    'accent': '#00c853',
    'button': '#00897b'
}

# ---------------- LATENCY ----------------
def measure_latency(dns_ip, timeout=2):
    try:
        start = time.time()
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((dns_ip, 53))
        return round((time.time() - start) * 1000, 2)
    except:
        return None

# ---------------- APP ----------------
class DNSAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DNS Analyzer Tool")
        self.root.geometry("900x650")
        self.root.configure(bg=THEME['bg'])

        self.dns_servers = DEFAULT_DNS_SERVERS.copy()
        self.results = []

        self.setup_ui()

    # ---------- UI ----------
    def setup_ui(self):

        # HEADER
        header = tk.Frame(self.root, bg=THEME['bg'])
        header.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(header, text="DNS Analyzer Tool",
                 font=("Segoe UI", 22, "bold"),
                 bg=THEME['bg'], fg=THEME['accent']).pack(anchor="w")

        tk.Label(header, text="Optimize your internet performance",
                 font=("Segoe UI", 10),
                 bg=THEME['bg'], fg="gray").pack(anchor="w")

        # INPUT CARD
        input_card = tk.Frame(self.root, bg=THEME['card'], bd=0)
        input_card.pack(fill=tk.X, padx=20, pady=10)

        tk.Label(input_card, text="Add Custom DNS",
                 bg=THEME['card'], fg=THEME['fg'],
                 font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=10, pady=5)

        row = tk.Frame(input_card, bg=THEME['card'])
        row.pack(fill=tk.X, padx=10, pady=5)

        self.entry = tk.Entry(row, font=("Segoe UI", 10))
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)

        tk.Button(row, text="➕ Add", bg=THEME['button'], fg="white",
                  relief="flat", command=self.add_dns).pack(side=tk.RIGHT)

        # CONTROL CARD
        control_card = tk.Frame(self.root, bg=THEME['card'])
        control_card.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # BUTTON
        top_bar = tk.Frame(control_card, bg=THEME['card'])
        top_bar.pack(fill=tk.X, padx=10, pady=5)

        self.analyze_btn = tk.Button(top_bar, text="🚀 Analyze DNS",
                                     bg=THEME['button'], fg="white",
                                     relief="flat", padx=10,
                                     command=self.start_analysis)
        self.analyze_btn.pack(side=tk.LEFT)

        self.progress = ttk.Progressbar(top_bar)
        self.progress.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=10)

        # TABLE
        self.tree = ttk.Treeview(control_card,
                                columns=("IP", "Latency"),
                                show='headings', height=6)

        self.tree.heading("IP", text="DNS IP")
        self.tree.heading("Latency", text="Latency (ms)")

        self.tree.column("IP", anchor="center")
        self.tree.column("Latency", anchor="center")

        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # GRAPH
        self.figure = plt.Figure(figsize=(6, 3), dpi=100)
        self.ax = self.figure.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.figure, master=control_card)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # STATUS
        self.status = tk.Label(self.root, text="", bg=THEME['bg'], fg="lightgreen")
        self.status.pack(pady=5)

    # ---------- ADD DNS ----------
    def add_dns(self):
        ip = self.entry.get().strip()
        if ip:
            self.dns_servers[f"Custom-{ip}"] = ip
            self.entry.delete(0, tk.END)
            self.status.config(text=f"✅ Added {ip}")
        else:
            self.status.config(text="⚠️ Enter valid IP")

    # ---------- START ----------
    def start_analysis(self):
        self.analyze_btn.config(state="disabled")
        threading.Thread(target=self.analyze).start()

    # ---------- ANALYSIS ----------
    def analyze(self):
        self.tree.delete(*self.tree.get_children())
        self.results = []
        self.progress["maximum"] = len(self.dns_servers)

        best = None
        min_latency = float('inf')

        for i, (name, ip) in enumerate(self.dns_servers.items(), 1):
            latency = measure_latency(ip)

            if latency:
                self.results.append((name, ip, latency))
                if latency < min_latency:
                    min_latency = latency
                    best = (name, ip)
            else:
                self.results.append((name, ip, "Timeout"))

            self.progress["value"] = i
            self.root.update_idletasks()

        # Fill table
        for _, ip, latency in self.results:
            self.tree.insert('', tk.END, values=(ip, latency))

        self.draw_graph()

        if best:
            self.status.config(
                text=f"⚡ Fastest DNS: {best[0]} ({best[1]}) - {min_latency} ms"
            )

        self.analyze_btn.config(state="normal")

    # ---------- GRAPH ----------
    def draw_graph(self):
        self.ax.clear()

        names = [ip for _, ip, _ in self.results]
        values = [lat if isinstance(lat, float) else 0 for _, _, lat in self.results]

        self.ax.barh(names, values)
        self.ax.set_title("DNS Latency")
        self.ax.set_xlabel("ms")
        self.ax.grid(True, linestyle="--", alpha=0.3)
        self.figure.tight_layout() 
        self.canvas.draw()


# ---------------- RUN ----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = DNSAnalyzerApp(root)
    root.mainloop()