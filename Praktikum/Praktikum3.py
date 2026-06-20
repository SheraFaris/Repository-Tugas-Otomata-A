"""
PDA Simulator for language L = { w x reverse(w) | w in {a,b}* }

Based on the given PDA diagram:
1. Read symbols before 'x' and PUSH each a/b to stack.
2. After reading 'x', read symbols after 'x' and POP matching stack top.
3. ACCEPT only if input is finished and stack is empty.

Examples accepted:
x
axa
bxb
abxba
aabxbaa

Examples rejected:
abxabb
abx
xab
abc
"""

import tkinter as tk
from tkinter import ttk, messagebox


class PDASimulator:
    def __init__(self):
        self.valid_symbols = {"a", "b", "x"}

    def simulate(self, input_string: str):
        """
        Returns:
            accepted (bool)
            trace (list of dict)
            reason (str)
        """
        s = input_string.strip().lower()
        stack = []
        mode = "PUSH"       # before reading x
        seen_x = False
        trace = []

        if s == "":
            return False, [], "Input kosong. Minimal harus ada simbol 'x'."

        step = 1

        for index, symbol in enumerate(s):
            if symbol not in self.valid_symbols:
                return False, trace, f"Simbol tidak valid: '{symbol}'. Hanya boleh a, b, dan x."

            stack_before = "".join(stack) if stack else "ε"
            action = ""
            state = ""

            if mode == "PUSH":
                state = "q_push"

                if symbol in {"a", "b"}:
                    stack.append(symbol)
                    action = f"READ {symbol}, PUSH {symbol}"

                elif symbol == "x":
                    if seen_x:
                        return False, trace, "Input memiliki lebih dari satu simbol 'x'."
                    seen_x = True
                    mode = "POP"
                    action = "READ x, pindah ke mode POP"

            else:  # mode == "POP"
                state = "q_pop"

                if symbol == "x":
                    return False, trace, "Input memiliki lebih dari satu simbol 'x'."

                if not stack:
                    action = f"READ {symbol}, gagal karena stack kosong"
                    trace.append({
                        "Step": step,
                        "State": state,
                        "Input": symbol,
                        "Stack Before": stack_before,
                        "Action": action,
                        "Stack After": "ε",
                    })
                    return False, trace, "Rejected: bagian kanan lebih panjang dari bagian kiri."

                top = stack[-1]
                if top == symbol:
                    stack.pop()
                    action = f"READ {symbol}, POP {symbol}"
                else:
                    action = f"READ {symbol}, gagal karena top stack = {top}"
                    trace.append({
                        "Step": step,
                        "State": state,
                        "Input": symbol,
                        "Stack Before": stack_before,
                        "Action": action,
                        "Stack After": "".join(stack) if stack else "ε",
                    })
                    return False, trace, (
                        f"Rejected: simbol kanan '{symbol}' tidak cocok "
                        f"dengan top stack '{top}'."
                    )

            trace.append({
                "Step": step,
                "State": state,
                "Input": symbol,
                "Stack Before": stack_before,
                "Action": action,
                "Stack After": "".join(stack) if stack else "ε",
            })
            step += 1

        if not seen_x:
            return False, trace, "Rejected: input harus memiliki satu simbol tengah 'x'."

        # λ transition to ACCEPT when input is finished and stack is empty
        if len(stack) == 0:
            trace.append({
                "Step": step,
                "State": "q_accept",
                "Input": "λ",
                "Stack Before": "ε",
                "Action": "ACCEPT karena input habis dan stack kosong",
                "Stack After": "ε",
            })
            return True, trace, "Accepted: string sesuai pola w x reverse(w)."

        return False, trace, (
            "Rejected: input habis tetapi stack belum kosong. "
            "Bagian kiri lebih panjang dari bagian kanan."
        )


class PDAApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDA Simulator - w x reverse(w)")
        self.root.geometry("900x560")
        self.root.resizable(True, True)

        self.simulator = PDASimulator()

        title = tk.Label(
            root,
            text="PDA Simulator",
            font=("Arial", 22, "bold")
        )
        title.pack(pady=(15, 0))

        subtitle = tk.Label(
            root,
            text="Bahasa: L = { w x reverse(w) | w ∈ {a,b}* }",
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

        examples = tk.Label(
            root,
            text="Contoh accepted: x, axa, bxb, abxba, aabxbaa | Contoh rejected: abxabb, abx, xab",
            font=("Arial", 10)
        )
        examples.pack(pady=(5, 10))

        self.result_label = tk.Label(
            root,
            text="Result: -",
            font=("Arial", 16, "bold")
        )
        self.result_label.pack(pady=5)

        self.reason_label = tk.Label(
            root,
            text="",
            font=("Arial", 11),
            wraplength=800
        )
        self.reason_label.pack(pady=5)

        table_frame = tk.Frame(root)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

        columns = ("Step", "State", "Input", "Stack Before", "Action", "Stack After")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")

        widths = {
            "Step": 60,
            "State": 100,
            "Input": 80,
            "Stack Before": 120,
            "Action": 330,
            "Stack After": 120,
        }

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=widths[col], anchor=tk.CENTER)

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def run_simulation(self):
        input_string = self.entry.get()
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
                    row["Input"],
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


if __name__ == "__main__":
    root = tk.Tk()
    app = PDAApp(root)
    root.mainloop()
