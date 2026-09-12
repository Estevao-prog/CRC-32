import zlib

def crc32_bitwise_didatico(dados: bytes, polinomio: int = 0x04C11DB7, mostrar_passos: bool = True) -> int:
    # Calcula o CRC realizando a divisão polinomial bit a bit.   # Converte os bytes em uma lista de bits
    bits = []
    for byte in dados:
        for i in range(7, -1, -1):
            bits.append((byte >> i) & 1)

    # anexa 32 bits zero ao final (equivale a multiplicar por x^32)
    bits += [0] * 32

    registrador = 0
    grau = 32  # grau do polinômio gerador (CRC-32 -> 32 bits)

    for i, bit in enumerate(bits):
        # Desloca o registrador e insere o próximo bit (bit menos significativo)
        bit_saida = (registrador >> (grau - 1)) & 1
        registrador = ((registrador << 1) | bit) & 0xFFFFFFFF

        # Se o bit que saiu for 1, faz XOR com o polinômio gerador
        if bit_saida ^ ((registrador >> grau) & 1):
            registrador ^= polinomio

        if mostrar_passos:
            print(f"bit {i:3d}: entrada={bit}  registrador={registrador:032b}")

    return registrador & 0xFFFFFFFF

# Versão padrão do CRC32.
def crc32_padrao(dados: bytes) -> int:
    """
    Implementação bit a bit do CRC-32.
    """
    POLINOMIO = 0xEDB88320  # forma refletida de 0x04C11DB7
    crc = 0xFFFFFFFF

    for byte in dados:
        crc ^= byte
        for _ in range(8):
            if crc & 1:
                crc = (crc >> 1) ^ POLINOMIO
            else:
                crc >>= 1

    return crc ^ 0xFFFFFFFF


# Demonstração da Implementação
if __name__ == "__main__":
    mensagem = b"Fala meu mano, tudo bom? Bora estudar CRC32!"

    print(f"Mensagem: {mensagem}")
    print("-" * 60)

    crc_didatico = crc32_bitwise_didatico(mensagem)
    print(f"CRC32 (versão didática, sem reflexão): {crc_didatico:#010x}")

    crc_manual = crc32_padrao(mensagem)
    print(f"CRC32 (implementação manual padrão):   {crc_manual:#010x}")

    crc_zlib = zlib.crc32(mensagem) & 0xFFFFFFFF
    print(f"CRC32 (zlib, referência oficial):      {crc_zlib:#010x}")

    print("-" * 60)
    if crc_manual == crc_zlib:
        print("A implementação manual bate com o resultado do zlib!")
    else:
        print("Diferença encontrada — revise a implementação.")