import heapq
import math
from collections import Counter
from dataclasses import dataclass
from typing import Dict, Optional, Tuple, List


VOWELS = set("AEIOUaeiou")


def first_two_vowels(name: str) -> str:
    """Return the first two vowels found in `name` (keeps vowel letters as uppercase)."""
    found: List[str] = []
    for ch in name:
        if ch in VOWELS:
            found.append(ch.upper())
            if len(found) == 2:
                break
    if len(found) < 2:
        raise ValueError(
            "Your name must contain at least TWO vowels (A, E, I, O, U). "
            "Example: 'TEO' has vowels 'E' and 'O'."
        )
    return "".join(found)


@dataclass
class Node:
    freq: int
    symbol: Optional[str] = None
    left: Optional["Node"] = None
    right: Optional["Node"] = None


def build_huffman_tree(freq_map: Dict[str, int]) -> Node:
    """
    Build a Huffman tree using a min-heap.
    Tie-breaking is made stable by using an increasing counter.
    """
    heap: List[Tuple[int, int, Node]] = []
    uid = 0

    for sym, f in freq_map.items():
        heapq.heappush(heap, (f, uid, Node(freq=f, symbol=sym)))
        uid += 1

    
    if len(heap) == 1:
        f, _, only = heap[0]
        dummy = Node(freq=0, symbol=None)
        return Node(freq=f, left=only, right=dummy)

    while len(heap) > 1:
        f1, _, n1 = heapq.heappop(heap)
        f2, _, n2 = heapq.heappop(heap)
        merged = Node(freq=f1 + f2, left=n1, right=n2)
        heapq.heappush(heap, (merged.freq, uid, merged))
        uid += 1

    return heap[0][2]


def build_codes(root: Node) -> Dict[str, str]:
    """Traverse Huffman tree to produce {symbol: code}."""
    codes: Dict[str, str] = {}

    def dfs(node: Node, path: str) -> None:
        if node.symbol is not None:
            
            codes[node.symbol] = path if path else "0"
            return
        if node.left is not None:
            dfs(node.left, path + "0")
        if node.right is not None:
            dfs(node.right, path + "1")

    dfs(root, "")
    return codes


def entropy_from_counts(counts: Dict[str, int]) -> float:
    """Shannon entropy H(S) in bits/symbol."""
    total = sum(counts.values())
    H = 0.0
    for c in counts.values():
        p = c / total
        H += p * math.log2(1 / p)
    return H


def average_code_length(counts: Dict[str, int], codes: Dict[str, str]) -> float:
    """Average codeword length L̄ = Σ p_i * l_i."""
    total = sum(counts.values())
    L = 0.0
    for sym, c in counts.items():
        p = c / total
        L += p * len(codes[sym])
    return L


def encode_text(text: str, codes: Dict[str, str]) -> str:
    """Encode full text to a bitstring using the Huffman code table."""
    return "".join(codes[ch] for ch in text)


def print_table(counts: Dict[str, int], codes: Dict[str, str]) -> None:
    """Pretty print encoding table."""
    total = sum(counts.values())

    
    rows = []
    for sym, c in counts.items():
        p = c / total
        rows.append((p, sym, c, codes[sym], len(codes[sym])))
    rows.sort(key=lambda x: (-x[0], x[1]))

    print("\nENCODING TABLE (Huffman)")
    print("-" * 60)
    print(f"{'Symbol':^8} | {'Count':^7} | {'Prob':^10} | {'Code':^15} | {'Len':^5}")
    print("-" * 60)
    for p, sym, c, code, ln in rows:
        print(f"{sym!s:^8} | {c:^7} | {p:^10.4f} | {code:^15} | {ln:^5}")
    print("-" * 60)


def main() -> None:
    # Group members' names and IDs
    print("=== TIT3131 Part B: Huffman Encoding Program ===")
    print("Group Members: Abdulrahman Abdullah Bawadi (ID: 1201301970), Omar Albassam (ID: 1191202421)")
    print("")

    base_text = "AERIOUS"
    print(f"Base text: {base_text}")
    
    # Continue the rest of your program...
    name = input("Enter ONE group member's name (used to find first 2 vowels): ").strip()
    
    # Existing code continues here...
    two_vowels = first_two_vowels(name)
    final_text = base_text + two_vowels  # "append behind the text"
    print(f"\nBase text: {base_text}")
    print(f"First two vowels from name: {two_vowels}")
    print(f"Final text used for Huffman: {final_text}")
    
    counts = dict(Counter(final_text))
    root = build_huffman_tree(counts)
    codes = build_codes(root)

    print_table(counts, codes)

    encoded = encode_text(final_text, codes)
    total_bits = len(encoded)

    H = entropy_from_counts(counts)
    Lbar = average_code_length(counts, codes)
    efficiency = (H / Lbar) * 100 if Lbar > 0 else 0.0

    print("\nCALCULATIONS")
    print("-" * 60)
    print(f"Total symbols (N)           = {sum(counts.values())}")
    print(f"Entropy, H(S) (bits/symbol) = {H:.6f}")
    print(f"Avg code length, L̄          = {Lbar:.6f} bits/symbol")
    print(f"Efficiency, η = H/L̄         = {efficiency:.2f}%")
    print(f"Encoded bitstring length     = {total_bits} bits")
    print(f"Encoded output               = {encoded}")
    print("-" * 60)

    encoded_base = encode_text(base_text, codes)
    print("\n(Verification) Encoding 'AERIOUS' using SAME table:")
    print(f"Encoded 'AERIOUS' = {encoded_base}  ({len(encoded_base)} bits)")

if __name__ == "__main__": main()
