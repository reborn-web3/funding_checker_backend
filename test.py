def rc4_keystream(key: bytes, n: int):
    """
    Генератор первых n байт ключевого потока RC4.
    """
    # --- KSA ---
    S = list(range(256))
    j = 0
    key_len = len(key)
    for i in range(256):
        j = (j + S[i] + key[i % key_len]) & 0xFF
        S[i], S[j] = S[j], S[i]

    # --- PRGA ---
    i = j = 0
    for _ in range(n):
        i = (i + 1) & 0xFF
        j = (j + S[i]) & 0xFF
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) & 0xFF]
        yield K


# Демонстрация
if __name__ == "__main__":
    key = b"supersecretkey"
    plaintext = b"Hello, RC4 world!"

    # генерируем столько же байт ключевого потока, сколько длина текста
    keystream = list(rc4_keystream(key, len(plaintext)))

    # шифруем
    ciphertext = bytes([p ^ k for p, k in zip(plaintext, keystream)])
    recovered = bytes([c ^ k for c, k in zip(ciphertext, keystream)])

    print("Plaintext:", plaintext)
    print("Keystream:", [hex(k) for k in keystream])
    print("Ciphertext (hex):", ciphertext.hex())
    print("Recovered:", recovered)
