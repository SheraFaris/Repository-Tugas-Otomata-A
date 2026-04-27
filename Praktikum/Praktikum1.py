import re

# Reserve words
RESERVED = {
    "if", "else", "for", "while", "return", "int", "float",
    "double", "char", "void", "print", "def", "import"
}

# Simbol
SYMBOLS = {
    "+", "-", "*", "/", "=", "==", "!=", ">=", "<=",
    "(", ")", "{", "}", ";", ","
}

def analyze(code):
    reserved = []
    symbols = []
    variables = []
    math_expr = []

    # Deteksi kalimat matematika
    lines = code.split("\n")
    for line in lines:
        if any(op in line for op in "+-*/="):
            math_expr.append(line.strip())

    # Tokenisasi
    tokens = re.findall(r"[A-Za-z_]\w*|==|!=|>=|<=|[+\-*/=(){};,]", code)

    for token in tokens:
        if token in RESERVED:
            reserved.append(token)
        elif token in SYMBOLS:
            symbols.append(token)
        elif re.match(r"[A-Za-z_]\w*", token):
            variables.append(token)

    # Hapus duplikat
    reserved = list(set(reserved))
    symbols = list(set(symbols))
    variables = list(set(variables))
    math_expr = list(set(math_expr))

    # Output
    print("\n=== HASIL ANALISIS ===")
    print("Reserve Words:", reserved)
    print("Simbol:", symbols)
    print("Variabel:", variables)
    print("Kalimat Matematika:", math_expr)


# Input dari user
print("Masukkan kode (akhiri dengan ENTER kosong):")
lines = []
while True:
    line = input()
    if line == "":
        break
    lines.append(line)

code_input = "\n".join(lines)

analyze(code_input)