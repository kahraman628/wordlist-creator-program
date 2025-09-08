import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import itertools
import string
import time

class WordlistGeneratorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Wordlist Generator (Educational)")
        self.geometry("500x500")
        self.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):
        # Options
        frame_opts = ttk.LabelFrame(self, text="Options")
        frame_opts.pack(fill="x", padx=10, pady=10)

        self.var_lower = tk.BooleanVar(value=True)
        self.var_upper = tk.BooleanVar(value=False)
        self.var_digits = tk.BooleanVar(value=True)
        self.var_symbols = tk.BooleanVar(value=False)

        ttk.Checkbutton(frame_opts, text="Lowercase (a-z)", variable=self.var_lower).pack(anchor="w", padx=8, pady=2)
        ttk.Checkbutton(frame_opts, text="Uppercase (A-Z)", variable=self.var_upper).pack(anchor="w", padx=8, pady=2)
        ttk.Checkbutton(frame_opts, text="Digits (0-9)", variable=self.var_digits).pack(anchor="w", padx=8, pady=2)
        ttk.Checkbutton(frame_opts, text="Symbols (!@#$)", variable=self.var_symbols).pack(anchor="w", padx=8, pady=2)

        # Length
        frame_len = ttk.LabelFrame(self, text="Length")
        frame_len.pack(fill="x", padx=10, pady=10)

        ttk.Label(frame_len, text="Min length:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.min_len = tk.Spinbox(frame_len, from_=1, to=10, width=5)
        self.min_len.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_len, text="Max length:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.max_len = tk.Spinbox(frame_len, from_=1, to=10, width=5)
        self.max_len.grid(row=1, column=1, padx=5, pady=5)

        # Progress bar
        self.progress = ttk.Progressbar(self, orient="horizontal", length=400, mode="determinate")
        self.progress.pack(pady=10)

        # Generate button
        ttk.Button(self, text="Generate Wordlist", command=self.generate_wordlist).pack(pady=10)

        # Status
        self.status = ttk.Label(self, text="Status: waiting...", foreground="gray")
        self.status.pack(pady=5)

    def generate_wordlist(self):
        chars = ""
        if self.var_lower.get():
            chars += string.ascii_lowercase
        if self.var_upper.get():
            chars += string.ascii_uppercase
        if self.var_digits.get():
            chars += string.digits
        if self.var_symbols.get():
            chars += "!@#$%^&*"

        if not chars:
            messagebox.showerror("Error", "Please select at least one character set.")
            return

        min_len = int(self.min_len.get())
        max_len = int(self.max_len.get())

        if min_len > max_len:
            messagebox.showerror("Error", "Min length cannot be greater than max length.")
            return

        # Calculate total combinations and estimated size
        total_combos = sum(len(chars)**i for i in range(min_len, max_len+1))
        avg_len = (min_len + max_len) / 2
        estimated_size = (total_combos * (avg_len + 1))  # bytes
        est_mb = estimated_size / (1024*1024)

        confirm = messagebox.askyesno(
            "Confirm",
            f"Total combinations: {total_combos:,}\n"
            f"Estimated file size: {est_mb:.2f} MB\n\n"
            "Do you want to continue?"
        )
        if not confirm:
            self.status.config(text="❌ Cancelled by user", foreground="red")
            return

        save_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")]
        )
        if not save_path:
            return

        # Start timing
        start_time = time.time()
        self.progress["maximum"] = total_combos
        count = 0

        with open(save_path, "w", encoding="utf-8") as f:
            for length in range(min_len, max_len+1):
                for combo in itertools.product(chars, repeat=length):
                    f.write("".join(combo) + "\n")
                    count += 1
                    if count % 1000 == 0:  # update progress every 1000 steps
                        self.progress["value"] = count
                        self.update_idletasks()

        elapsed = time.time() - start_time
        self.status.config(
            text=f"✅ Done: {count:,} combinations ({est_mb:.2f} MB) in {elapsed:.2f} sec.\nSaved to {save_path}",
            foreground="green"
        )
        messagebox.showinfo("Finished", f"Wordlist generated!\n{count:,} entries\nEstimated size: {est_mb:.2f} MB\nTime: {elapsed:.2f} sec")

if __name__ == "__main__":
    app = WordlistGeneratorApp()
    app.mainloop()
