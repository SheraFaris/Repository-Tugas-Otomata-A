"""
PDA Simulator for the provided PDA diagram.

Language accepted:
    L = { s^(2n) | n >= 0 }

Meaning:
    The PDA accepts strings with an even number of 's'.

Why?
    1. In the first phase, the PDA reads 's' and PUSHes 's' to the stack.
    2. Using an epsilon transition, it moves to the second phase.
    3. In the second phase, it reads 's' and POPs one 's' from the stack.
    4. It accepts only when the input is finished and only the bottom symbol Δ remains.

Examples accepted:
    ε
    ss
    ssss
    ssssss

Examples rejected:
    s
    sss
    sssss
    a
"""

import tkinter as tk
from tkinter import ttk


BOTTOM = "Δ"


class PDASimulator:
    def __init__(self):
        self.alphabet = {"s"}

    def simulate(self, input_string: str):
        """
        Simulates the PDA by choosing the middle of the string as the epsilon move.
        This matches the PDA's nondeterministic behavior for L = { s^(2n) }.

        Returns:
            accepted: bool
            trace: list[dict]
            reason: str
        """
        # Program membersihkan input 
        text = input_string.strip().lower()
        """ 
            ε
            epsilon
            lambda
            λ
            ==> Dianggap kosong
        """
        if text in {"ε", "epsilon", "lambda", "λ"}:
            text = ""

        for ch in text:
            if ch not in self.alphabet:
                return False, [], "Rejected: simbol input hanya boleh 's'."
        # Program mengecek panjang string
        if len(text) % 2 != 0:
            return False, self._make_failed_trace(text), (
                "Rejected: jumlah simbol 's' ganjil, sehingga jumlah PUSH dan POP tidak seimbang."
            )

        half = len(text) // 2
        stack = [BOTTOM]
        trace = []
        step = 1

        # Phase 1: READ s, PUSH s
        for i in range(half):
            stack_before = self._stack_text(stack)
            stack.append("s")
            trace.append({
                "Step": step,
                "State": "q_push",
                "Remaining Input": text[i:],
                "Read": "s",
                "Stack Before": stack_before,
                "Action": "READ s, PUSH s",
                "Stack After": self._stack_text(stack),
            })
            step += 1

        # Epsilon transition from first READ to second READ
        trace.append({
            "Step": step,
            "State": "q_push → q_pop",
            "Remaining Input": text[half:],
            "Read": "ε",
            "Stack Before": self._stack_text(stack),
            "Action": "ε-transition, pindah ke fase POP",
            "Stack After": self._stack_text(stack),
        })
        step += 1

        # Phase 2: READ s, POP s
        for i in range(half, len(text)):
            stack_before = self._stack_text(stack)

            if len(stack) <= 1 or stack[-1] != "s":
                trace.append({
                    "Step": step,
                    "State": "q_pop",
                    "Remaining Input": text[i:],
                    "Read": "s",
                    "Stack Before": stack_before,
                    "Action": "GAGAL: top stack bukan s",
                    "Stack After": self._stack_text(stack),
                })
                return False, trace, "Rejected: simbol 's' tidak dapat di-POP dari stack."

            stack.pop()
            trace.append({
                "Step": step,
                "State": "q_pop",
                "Remaining Input": text[i:],
                "Read": "s",
                "Stack Before": stack_before,
                "Action": "READ s, POP s",
                "Stack After": self._stack_text(stack),
            })
            step += 1

        # Pop bottom marker Δ and accept
        if stack == [BOTTOM]:
            stack_before = self._stack_text(stack)
            stack.pop()
            trace.append({
                "Step": step,
                "State": "q_pop → q_accept",
                "Remaining Input": "ε",
                "Read": "Δ",
                "Stack Before": stack_before,
                "Action": "POP Δ, ACCEPT",
                "Stack After": "ε",
            })
            return True, trace, "Accepted: jumlah PUSH dan POP seimbang. String memiliki jumlah 's' genap."

        return False, trace, "Rejected: input habis tetapi stack belum kembali ke Δ."

    def _make_failed_trace(self, text):
        """
        Gives a simple trace for odd-length strings.
        The PDA cannot split an odd number of s into two equal parts.
        """
        trace = []
        stack = [BOTTOM]
        step = 1
        middle = len(text) // 2

        for i in range(middle + 1):
            stack_before = self._stack_text(stack)
            stack.append("s")
            trace.append({
                "Step": step,
                "State": "q_push",
                "Remaining Input": text[i:],
                "Read": "s",
                "Stack Before": stack_before,
                "Action": "READ s, PUSH s",
                "Stack After": self._stack_text(stack),
            })
            step += 1

        trace.append({
            "Step": step,
            "State": "q_pop",
            "Remaining Input": text[middle + 1:],
            "Read": "ε",
            "Stack Before": self._stack_text(stack),
            "Action": "GAGAL: sisa input tidak cukup untuk mengosongkan stack",
            "Stack After": self._stack_text(stack),
        })
        return trace

    def _stack_text(self, stack):
        if not stack:
            return "ε"
        return "".join(stack)

# Class PDAApp membuat tampilan program
class PDAApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDA Simulator - Even Number of s")
        self.root.geometry("980x600")
        self.root.resizable(True, True)

        self.simulator = PDASimulator()

        title = tk.Label(root, text="PDA Simulator", font=("Arial", 22, "bold"))
        title.pack(pady=(15, 0))

        subtitle = tk.Label(
            root,
            text="Bahasa: L = { s^(2n) | n ≥ 0 }  → menerima jumlah huruf 's' yang genap",
            font=("Arial", 12)
        )
        subtitle.pack(pady=(0, 15))

        input_frame = tk.Frame(root)
        input_frame.pack(pady=5)

        tk.Label(input_frame, text="Input string:", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)

        self.entry = tk.Entry(input_frame, width=40, font=("Arial", 12))
        self.entry.pack(side=tk.LEFT, padx=5)
        self.entry.bind("<Return>", lambda event: self.run_simulation())

        run_button = tk.Button(
            input_frame,
            text="Run PDA",
            font=("Arial", 11, "bold"),
            command=self.run_simulation
        )
        run_button.pack(side=tk.LEFT, padx=5)

        clear_button = tk.Button(
            input_frame,
            text="Clear",
            font=("Arial", 11),
            command=self.clear_all
        )
        clear_button.pack(side=tk.LEFT, padx=5)

        example_frame = tk.Frame(root)
        example_frame.pack(pady=(5, 10))

        tk.Label(
            example_frame,
            text="Contoh accepted: ε, ss, ssss, ssssss     |     Contoh rejected: s, sss, sssss",
            font=("Arial", 10)
        ).pack()

        self.result_label = tk.Label(root, text="Result: -", font=("Arial", 16, "bold"))
        self.result_label.pack(pady=5)

        self.reason_label = tk.Label(root, text="", font=("Arial", 11), wraplength=900)
        self.reason_label.pack(pady=5)

        table_frame = tk.Frame(root)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        columns = (
            "Step",
            "State",
            "Remaining Input",
            "Read",
            "Stack Before",
            "Action",
            "Stack After",
        )

        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")

        widths = {
            "Step": 55,
            "State": 125,
            "Remaining Input": 140,
            "Read": 70,
            "Stack Before": 125,
            "Action": 300,
            "Stack After": 125,
        }

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=widths[col], anchor=tk.CENTER)

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def run_simulation(self):
        # mengambil input pengguna:
        input_string = self.entry.get()

        # menjalankan simulator PDA
        accepted, trace, reason = self.simulator.simulate(input_string)

        for item in self.tree.get_children():
            self.tree.delete(item)

        for row in trace:
            self.tree.insert(
                "",
                tk.END,
                values=(
                    row["Step"],
                    row["State"],
                    row["Remaining Input"],
                    row["Read"],
                    row["Stack Before"],
                    row["Action"],
                    row["Stack After"],
                )
            )

        if accepted:
            self.result_label.config(text="Result: ACCEPTED", fg="green")
        else:
            self.result_label.config(text="Result: REJECTED", fg="red")

        self.reason_label.config(text=reason)

    def clear_all(self):
        self.entry.delete(0, tk.END)
        self.result_label.config(text="Result: -", fg="black")
        self.reason_label.config(text="")
        for item in self.tree.get_children():
            self.tree.delete(item)

# Bagian ini menjalankan GUI Tkinter
if __name__ == "__main__":
    root = tk.Tk()
    app = PDAApp(root)
    root.mainloop()
