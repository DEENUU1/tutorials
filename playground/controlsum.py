# Utworzenie listy ramki
frames = [
    [0x6A, 0x10, 0xB4, 0x6D, 0xA1, 0x04, 0x00, 0x00],
    [0x10, 0x11, 0xB4, 0x04, 0xA1, 0x04, 0x00, 0x00],
    # ... pozostałe ramki omijane ze względu na ilość miejsca
]

sum_control = 0
for frame in frames[:len(frames) - 1]:
    sum_temp = 0
    for idx in range(1, len(frame)):
        sum_temp += frame[idx]

    sum_temp >>= 8  # Przesuniecie wyniku sumowania o 8 bitów
    sum_control += sum_temp + frame[0]

print("Suma kontrolna bajtu ZERO:", hex(sum_control))
