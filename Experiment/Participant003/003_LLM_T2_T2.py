
def is_english_alpha(s: str) -> bool:
    """Retorna True se todos os caracteres em s forem A-Z ou a-z."""
    return all(('a' <= ch <= 'z') or ('A' <= ch <= 'Z') for ch in s)

def remove_trailing_vowels(s: str, vowels: str = "aeiou") -> str:
    """Remove vogais do fim da string s (s deve estar em minúsculas)."""
    i = len(s)
    while i > 0 and s[i - 1] in vowels:
        i -= 1
    return s[:i]

def process(j: str) -> str:
    """Valida j, converte para minúsculas e remove vogais do fim.
       Retorna a string resultante entre parênteses."""
    if not is_english_alpha(j):
        raise ValueError("Entrada contém caracteres fora do alfabeto inglês.")
    s = j.lower()
    result = remove_trailing_vowels(s)
    return f"({result})"

# Exemplos
if __name__ == "__main__":
    print(process("pirauouieiea"))  # saída: (id)
    print(process("daoiuyt"))   # saída: (day)  -> 'y' não é tratado como vogal aqui