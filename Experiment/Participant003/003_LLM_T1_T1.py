from typing import List, Tuple, Dict

def word_weight_to_letter(words: List[str], weights: List[int]) -> Dict[str, Tuple[int,int,str]]:
    """
    Para cada palavra em `words`:
    - soma os pesos das letras (weights[0] = 'a', ..., weights[25] = 'z')
    - pega total % 26 (resultado 0..25)
    - converte para letra invertida: 0 -> 'z', 1 -> 'y', ..., 25 -> 'a'
    Retorna dicionário: palavra -> (soma_total, resto_mod26, letra_resultado)
    """
    if len(weights) != 26:
        raise ValueError("weights deve ter exatamente 26 elementos (um por letra a..z).")
    result = {}
    for w in words:
        if not all('a' <= ch <= 'z' for ch in w):
            raise ValueError(f"Palavra inválida (apenas letras minúsculas a-z são permitidas): {w!r}")
        total = sum(weights[ord(ch) - ord('a')] for ch in w)
        r = total % 26
        letter = chr(ord('z') - r)  # 0 -> 'z', 25 -> 'a'
        result[w] = (total, r, letter)
    return result

# Exemplo de uso
if __name__ == "__main__":
    words = ["abcd", "def", "xyz"]
    # exemplo de pesos (a=1, b=2, ..., z=26)
    words = ["a", "b", "c"]
    weights = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    # weights = [5, 3, 12, 14, 1, 2, 3, 2, 10, 6, 6, 9, 7, 8, 7, 10, 8, 9, 6, 9, 9, 8, 3, 7, 7, 2]
    # weights = list(range(1, 27))
    out = word_weight_to_letter(words, weights)
    for word, (total, r, letter) in out.items():
        print(f"{word}: total={total}, total%26={r}, letra='{letter}'")