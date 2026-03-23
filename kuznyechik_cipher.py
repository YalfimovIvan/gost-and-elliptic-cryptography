import os

PI = [
    252, 238, 221, 17, 207, 110, 49, 22, 251, 196, 250, 218, 35, 197, 4, 77,
    233, 119, 240, 219, 147, 46, 153, 186, 23, 54, 241, 187, 20, 205, 95, 193,
    249, 24, 101, 90, 226, 92, 239, 33, 129, 28, 60, 66, 139, 1, 142, 79,
    5, 132, 2, 174, 227, 106, 143, 160, 6, 11, 237, 152, 127, 212, 211, 31,
    235, 52, 44, 81, 234, 200, 72, 171, 242, 42, 104, 162, 253, 58, 206, 204,
    181, 112, 14, 86, 8, 12, 118, 18, 191, 114, 19, 71, 156, 183, 93, 135,
    21, 161, 150, 41, 16, 123, 154, 199, 243, 145, 120, 111, 157, 158, 178,
    177, 50, 117, 25, 61, 255, 53, 138, 126, 109, 84, 198, 128, 195, 189, 13,
    87, 223, 245, 36, 169, 62, 168, 67, 201, 215, 121, 214, 246, 124, 34, 185,
    3, 224, 15, 236, 222, 122, 148, 176, 188, 220, 232, 40, 80, 78, 51, 10,
    74, 167, 151, 96, 115, 30, 0, 98, 68, 26, 184, 56, 130, 100, 159,
    38, 65, 173, 69, 70, 146, 39, 94, 85, 47, 140, 163, 165, 125, 105, 213,
    149, 59, 7, 88, 179, 64, 134, 172, 29, 247, 48, 55, 107, 228, 136, 217,
    231, 137, 225, 27, 131, 73, 76, 63, 248, 254, 141, 83, 170, 144, 202, 216,
    133, 97, 32, 113, 103, 164, 45, 43, 9, 91, 203, 155, 37, 208, 190, 229,
    108, 82, 89, 166, 116, 210, 230, 244, 180, 192, 209, 102, 175, 194, 57,
    75, 99, 182,
]

PI_INV = [0] * 256
for i in range(256):
    PI_INV[PI[i]] = i

L_COEFFS = [148, 32, 133, 16, 194, 192, 1, 251, 1, 192, 194, 16, 133, 32, 148, 1]   #коэф линейного преобраз

BLOCK_SIZE = 16
KEY_SIZE = 32

_GF_RED = 0xC3 #константа неприводимый многочлен в поле галуа


def xor_bytes(a: bytes, b: bytes) -> bytes:         #побайтовый XOR двух байтовых строк
    return bytes([x ^ y for (x, y) in zip(a, b)])           #создаем bytes из списка результатов x XOR y, zip склеивает в пары




def gf_mul(a: int, b: int) -> int: #умножение в поле Галуа x^8+x^7+x^6+x+1.
     
    res = 0
    aa = a & 0xFF       #оставляем только младшие 8 бит числа a и b
    bb = b & 0xFF
    
    for _ in range(8):      #цикл по 8 битам множителя b
        if bb & 1:      # если младший бит bb равен 1
            res ^= aa                              # добавляем aa к результату (в GF(2) сложение = XOR)
        hi = aa & 0x80      #проверка старшего бита
        aa = (aa << 1) & 0xFF           #сдвигаем аа влево и оставляем 8 бит
        if hi:      #если переполнение старшего бита
            aa ^= _GF_RED
        bb >>= 1        #переход к след биту множителя
    return res




def l_func(state16: bytes) -> int:      #принимает 16байтный блок и возвращает 1 байт
    x = 0
    for c, b in zip(L_COEFFS, state16):
        x ^= gf_mul(c, b)       #умножение в поле Галуа и потом прибавляем к сумме через XOR
    return x    #на выходе 1 байт


def R(state16: bytes) -> bytes:         #линейное преобразование регистра, на вход 16 байт
    lb = l_func(state16)
    return bytes([lb]) + state16[:15]   #все байты вправо, последний отбрасывается


def R_inv(state16: bytes) -> bytes:     #обратное R преобразование
    seq = state16[1:] + state16[:1]     #первый байт в конец
    lb = l_func(seq)            #вычисл недостающий байт
    return state16[1:] + bytes([lb])        #сдвиг влево и добавл в конец


def L(state16: bytes) -> bytes:     #L преобразование для 16-байтного блока
    s = state16         #копируем в s
    for _ in range(16):     #16 итераций, на каждой R преобразование
        s = R(s)
    return s        #итоговое s на выходе 


def L_inv(state16: bytes) -> bytes:     #обратное L для 16байтного блока
    s = state16
    for _ in range(16):
        s = R_inv(s)        #для каждой итерации обратное R
    return s


def S(state16: bytes) -> bytes:    #нелинейное преобразование S-подстановка, замена байта по таблице
    return bytes([PI[b] for b in state16])      #для каждого байта b берем значение из таб. подстановки и собираем результат 


def S_inv(state16: bytes) -> bytes:         #обратная азмена для восстановления исходных байтов
    return bytes([PI_INV[b] for b in state16])


def LSX(k: bytes, a: bytes) -> bytes:           #раундовая операция, три преобразования
    return L(S(xor_bytes(a, k)))        #k раундовый ключ, а - текущ блок состояния 16 байт


def F(k: bytes, a1: bytes, a0: bytes):      #смешивает 2 блока, использует одну из констант c
    return xor_bytes(LSX(k, a1), a0), a1            #после  применений новая пара ключей


def gen_round_keys(master_key: bytes):      #ключ на вход
    if len(master_key) != KEY_SIZE:
        raise ValueError("Ключ должен быть 32 байта (256 бит).")        #проверка ключа на размер 32 байта

    k1 = master_key[:BLOCK_SIZE]        #разделение ключа на 2 
    k2 = master_key[BLOCK_SIZE:]
    C = []
    for i in range(1, 33):      #генерация констант в 16байтное представление
        C.append(L(i.to_bytes(BLOCK_SIZE, "big")))

    keys = [k1, k2]     #инициализация списка ключей
    a1, a0 = k1, k2             #рабочая пара блоков, над которой дальше будут применяться преобразования F

    for i in range(1, 5):       #цикл генерации ключей 4 серии
        for j in range(1, 9):           #в каждой серии 8 F преобразований
            c = C[8 * (i - 1) + (j - 1)]        #выбор константы
            a1, a0 = F(c, a1, a0)                   #применение F
        keys.append(a1)
        keys.append(a0)                 #новая пара ключей на выходе

    if len(keys) != 10:
        raise RuntimeError("Ошибка генерации итерационных ключей")          #проверка на 10 ключей
    return keys         #на выходе список ключей



class Kuznyechik:
    def __init__(self, master_key: bytes):      #генерация ключей и сохранение в классе
        self.rk = gen_round_keys(master_key)

    def encrypt_block(self, block16: bytes) -> bytes:       #шифрование 1 блока 128 бит
        if len(block16) != BLOCK_SIZE:
            raise ValueError("Блок должен быть 16 байт")
        x = block16
        for i in range(9):
            x = LSX(self.rk[i], x)
        return xor_bytes(x, self.rk[9])

    def decrypt_block(self, block16: bytes) -> bytes:       #расшифрование 1 блока 128 бит
        if len(block16) != BLOCK_SIZE:
            raise ValueError("Блок должен быть 16 байт.")
        x = xor_bytes(block16, self.rk[9])
        for i in range(8, -1, -1):
            x = xor_bytes(S_inv(L_inv(x)), self.rk[i])
        return x


def pad_proc2(data: bytes) -> bytes:                #добавление паддинга
    pad_len = BLOCK_SIZE - (len(data) % BLOCK_SIZE)         #вычисл сколько нужно добавить
    return data + bytes([0x80]) + (b"\x00" * (pad_len - 1))             #добавление


def unpad_proc2(data: bytes) -> bytes:          #удаление дополнения
    if len(data) == 0 or (len(data) % BLOCK_SIZE) != 0:
        raise ValueError("Некорректная длина данных для снятия дополнения")
    i = len(data) - 1       #начало с конца
    while i >= 0 and data[i] == 0x00:       #завершающие пропуск
        i -= 1
    if i < 0 or data[i] != 0x80:        #проверка наличия маркера дополнения
        raise ValueError("Некорректное дополнение, маркер 0x80 не найден")
    return data[:i]


def ecb_encrypt(cipher: Kuznyechik, plaintext: bytes) -> bytes:     #режим простой замены
    pt = pad_proc2(plaintext)       #добавление паддинга
    out = bytearray()       #изменяеммый массив байтов
    for i in range(0, len(pt), BLOCK_SIZE):             #шифрование поблочно
        out.extend(cipher.encrypt_block(pt[i:i + BLOCK_SIZE]))      #добавление байтов в bytearray
    return bytes(out) #обратно в bytes


def ecb_decrypt(cipher: Kuznyechik, ciphertext: bytes) -> bytes:        #расшифрование простой замены
    if (len(ciphertext) % BLOCK_SIZE) != 0:
        raise ValueError("ECB: длина шифртекста должна быть кратна 16 байтам.")
    out = bytearray()
    for i in range(0, len(ciphertext), BLOCK_SIZE):     #проход по шифртексту блоками по 16 байт
        out.extend(cipher.decrypt_block(ciphertext[i:i + BLOCK_SIZE]))
    return unpad_proc2(bytes(out))      # удаление паддинга и возврат исходного текста


def inc_be(counter_bytes: bytes) -> bytes:      #увеличение счетчика на 1, счетчик как массив байтов
    x = int.from_bytes(counter_bytes, "big")        #интерпретируем массив байтов как целое число
    x = (x + 1) % (1 << (8 * len(counter_bytes)))       #увелич на 1 и берем по модулю
    return x.to_bytes(len(counter_bytes), "big")        #число в массив байтов той же длины


def ctr_crypt(cipher: Kuznyechik, data: bytes, iv8: bytes) -> bytes:            #шифрование расшифр в режиме счетчика

    if len(iv8) != 8:           #проверка синхропосылки на 8 байт
        raise ValueError("CTR ошибка, IV должен быть 8 байт (64 бита).")
    ctr = iv8 + (b"\x00" * 8)  #формируем начальный счетчик нулями
    out = bytearray()       #изменяемый буфер для результата
    for i in range(0, len(data), BLOCK_SIZE):       #по 16 байт
        block = data[i:i + BLOCK_SIZE]          #извлекаем текущий
        gamma = cipher.encrypt_block(ctr)       #шифруем текущее значение счетчика
        out.extend(bytes([block[j] ^ gamma[j] for j in range(len(block))]))         #ксорим блок с гаммой
        ctr = inc_be(ctr)       #увелич счетчик на 1
    return bytes(out)


def ofb_crypt(cipher: Kuznyechik, data: bytes, iv: bytes, z: int) -> bytes:     #гаммирование с обратной связью по выходу

    if z < 1:           #проверка на длину регистра обратной связи
        raise ValueError("OFB ошибка, параметр z должен быть >= 1.")
    if len(iv) != (BLOCK_SIZE * z):                                     #проверка синхропосылки
        raise ValueError("OFB: длина IV должна быть 16*z байт (m=n*z).")

    Rreg = iv           #иниц регистр значением синхропосылки
    out = bytearray()

    for i in range(0, len(data), BLOCK_SIZE):       #блоки по 16 байт
        block = data[i:i + BLOCK_SIZE]          #текущий блок
        Y = cipher.encrypt_block(Rreg[:BLOCK_SIZE])  #шифрование старшего блока регистра
        out.extend(bytes([block[j] ^ Y[j] for j in range(len(block))]))     #ксорим блок данных с гаммой
        if z == 1:
            Rreg = Y
        else:
            Rreg = Rreg[BLOCK_SIZE:] + Y  #если регистр несколько блоков, сдвигаем и добавляем новую гамму в конец

    return bytes(out)


def cbc_encrypt(cipher: Kuznyechik, plaintext: bytes, iv: bytes, z: int) -> bytes:    #шифрование простая замена с зацеплением 
    if z < 1:
        raise ValueError("CBC ошибка параметр z должен быть >= 1.")  #проверка на длину регистра обратной связи 
    if len(iv) != (BLOCK_SIZE * z):
        raise ValueError("CBC: длина IV должна быть 16*z байт (m=n*z).")        #проверка синхропосылки, что длина 16*z байт

    pt = pad_proc2(plaintext)       #добавл паддинг
    Rreg = iv   #регистр обратной связи
    out = bytearray()       #буфер для результата

    for i in range(0, len(pt), BLOCK_SIZE):     #блоки по 16 байт
        P = pt[i:i + BLOCK_SIZE]        #открытый текст
        msb = Rreg[:BLOCK_SIZE]             #старший блок регистра
        C = cipher.encrypt_block(xor_bytes(P, msb))     #ксорим и шифруем
        out.extend(C)       #на выходе добавляем блок шифртекста
        if z == 1:
            Rreg = C        #новый регистр = текущий шифртекст
        else:
            Rreg = Rreg[BLOCK_SIZE:] + C    #сдвигаем и добавл новый блок С

    return bytes(out)


def cbc_decrypt(cipher: Kuznyechik, ciphertext: bytes, iv: bytes, z: int) -> bytes: #расшифрование простая замена с зацеплением
    if z < 1:
        raise ValueError("CBC: параметр z должен быть >= 1.")      #проверяем параметр регистра
    if len(iv) != (BLOCK_SIZE * z):
        raise ValueError("CBC: длина IV должна быть 16*z байт (m=n*z).")    # проверяем длину синхропосылки
    if (len(ciphertext) % BLOCK_SIZE) != 0:
        raise ValueError("CBC: длина шифртекста должна быть кратна 16 байтам.")  #длина шифртекста должна быть кратна размеру блока

    Rreg = iv
    out = bytearray()

    for i in range(0, len(ciphertext), BLOCK_SIZE): #шифртекст блоками 16 байт
        C = ciphertext[i:i + BLOCK_SIZE]    #текущий блок
        msb = Rreg[:BLOCK_SIZE]     #старший блок регистра
        P = xor_bytes(cipher.decrypt_block(C), msb) #расшифровываем C и XOR с предыдущим блоком
        out.extend(P)       #добавл расшифрованный блок
        if z == 1:
            Rreg = C
        else:
            Rreg = Rreg[BLOCK_SIZE:] + C

    return unpad_proc2(bytes(out))  #удаляем паддинг и выводим 


def cfb_crypt(cipher: Kuznyechik, data: bytes, iv: bytes, z: int, s_bytes: int, decrypt: bool) -> bytes:
    if z < 1:       #гаммирование с обратной связью по шифртексту
        raise ValueError("CFB ошибка, параметр z должен быть >= 1.")
    if len(iv) != (BLOCK_SIZE * z):                                 #синхропосылка 16*z байт
        raise ValueError("CFB ошибка, длина IV должна быть 16*z байт (m=n*z).")
    if not (1 <= s_bytes <= BLOCK_SIZE):                                        #размер сегмента от 1 до 16 байт
        raise ValueError("CFB ошибка, s должно быть от 1 до 16 байт (кратно 8 бит).")

    Rreg = iv       #регистр обратной связи значением синхропосылки
    out = bytearray()

    idx = 0     #текущая позиция в потоке
    while idx < len(data):      #обработка сегментами по s байт
        seg = data[idx: idx + s_bytes]      #текущий сегмент

        O = cipher.encrypt_block(Rreg[:BLOCK_SIZE])   #шифруем старший 16байтный блок регистра
        gamma = O[:len(seg)]                          # Ts / Tr

        if decrypt:
            Pseg = bytes([seg[i] ^ gamma[i] for i in range(len(seg))])  #ксорим гамму и Pi
            out.extend(Pseg)            #добавляем расшифрованный сегмент в результат
            Cseg = seg  #в регистр при расшифровании должен идти исходный шифртекстовый сегмент
        else:
            Cseg = bytes([seg[i] ^ gamma[i] for i in range(len(seg))])
            out.extend(Cseg)        #ксорим и добавляем шифротекстовый сегмент в результат

        if z == 1 and len(seg) == BLOCK_SIZE: #частный случай, если регистр 1 блок и сегмент полный
            Rreg = Cseg     #новый регистр просто текущий блок шифртекста
        else:
            Rreg = Rreg[len(seg):] + Cseg       #в общем случае сдивгаем влево на s и дописываем в конец

        idx += s_bytes

    return bytes(out)



def clean_hex(s: str) -> str:       #очистка строки до 16ричных символов  
    s = s.strip().lower()   #удал пробелы и в лоу регистр
    if s.startswith("0x"):
        s = s[2:]   #удаляем первые 2 символа, префикс
    allowed = "0123456789abcdef"
    return "".join([ch for ch in s if ch in allowed])   #объяединяем в строку


def parse_hex_bytes(s: str, expected_len: int) -> bytes:    #преобраз из 16рич в массив байтов заданной длины
    hs = clean_hex(s)
    if len(hs) != expected_len * 2:     
        raise ValueError("Ожидалось %d байт (%d hex-символов)." % (expected_len, expected_len * 2))
    return bytes.fromhex(hs)    #преобраз 16рич в bytes


def b2hex(b: bytes) -> str: #байтовый массив в 16рич строку
    return b.hex()


def choose(prompt: str, options):       #выбор номера
    while True:
        print(prompt)
        for i in range(len(options)):
            print("  %d) %s" % (i + 1, options[i]))
        ans = input("Введите номер: ").strip()
        if ans.isdigit():
            n = int(ans)
            if 1 <= n <= len(options):
                return n
        print("Некорректный ввод.\n")


def ask_existing_file(prompt: str) -> str:      #запрос пути к сущ. файлу
    while True:
        p = input(prompt).strip().strip('"').strip("'") #убираем пробелы и кавычки
        p = os.path.expanduser(p)       #замена на домашнюю директорию
        if os.path.isfile(p):       #проверка на сущ-е
            return p
        print("неа, файл не найден.\n")


def ask_out_file(default_path: str) -> str:     #путь выходного файла
    s = input("Путь выходного файла (Enter = %s): " % default_path).strip().strip('"').strip("'")   #ввод без пробелов и кавычек
    if s == "":
        return default_path
    return os.path.expanduser(s)    


def confirm_overwrite(path: str) -> bool:       #перезапись файла
    if not os.path.exists(path):
        return True
    ans = input("Файл уже существует. Перезаписать? (y/N): ").strip().lower()
    return ans == "y"


def ask_key() -> bytes:
    while True:
        s = input("Ключ 256 бит в 16ричной системе (32 байта = 64 hex-символа): ").strip()       #ввод ключа
        try:
            return parse_hex_bytes(s, KEY_SIZE)     #на выходе массив из 32 байтов 
        except Exception as e:
            print("Ошибка ключа: %s\n" % e)


def ask_z() -> int:     #запрос памаметра z и вывод как целое число
    while True:
        s = input("Параметр z (целое >= 1, Enter = 1): ").strip()
        if s == "":
            return 1
        if s.isdigit() and int(s) >= 1: #проверка что число и >=1
            return int(s)
        print("Некорректный z.\n")


def ask_s_bytes() -> int:       #запрос параметра s в байтах
    while True:
        s = input("Параметр s в байтах (1..16, Enter = 16): ").strip()
        if s == "":
            return 16
        if s.isdigit():     #проверка на число
            v = int(s)      #строка в целое число
            if 1 <= v <= 16:        #диапазон
                return v
        print("Некорректный s.\n")


def ask_iv_hex(iv_len: int) -> bytes:       #запрос синхропосылки
    while True:
        s = input("IV в hex (%d байт = %d hex-символов): " % (iv_len, iv_len * 2)).strip()      #убираем пробелы по краям
        try:
            return parse_hex_bytes(s, iv_len)       #перевод в байты
        except Exception as e:
            print("Ошибка IV: %s\n" % e)


def choose_iv_encrypt(mode: int, z: int) -> bytes:      #выбор синхропосылки для режимов

    if mode == 4:  #если каунтер, длина 8 байт
        iv_len = 8
    else:       
        iv_len = BLOCK_SIZE * z     #для CBC CFB OFB режимов

    gost_iv_long = bytes.fromhex("1234567890abcef0a1b2c3d4e5f0011223344556677889901213141516171819")
    gost_iv_ctr = bytes.fromhex("1234567890abcef0")

    while True:
        print("IV:")
        print(" 1) Сгенерировать")
        print(" 2) Контрольный пример из ГОСТ")
        print(" 3) Ввести вручную (hex)")
        c = input("Введите номер: ").strip()

        if c == "1":
            iv = os.urandom(iv_len)         #генерация синхропосылки
            print("IV (hex): %s" % b2hex(iv))
            return iv

        if c == "2":
            if mode == 4:
                iv = gost_iv_ctr
                print("IV из ГОСТ (hex): %s" % b2hex(iv))
                return iv
            if iv_len == 32:  #z=2 для n=128
                iv = gost_iv_long
                print("IV из ГОСТ (hex): %s" % b2hex(iv))
                return iv
            print(
                "Контрольный IV из ГОСТ имеет другую длину, нужно 32 байта при z=2).\n"
                "Выбери генерацию или ручной ввод.\n"
            )
            continue

        if c == "3":
            iv = ask_iv_hex(iv_len)
            print("IV (hex): %s" % b2hex(iv))
            return iv

        print("Некорректный ввод.\n")


def split_iv_and_payload(data: bytes, iv_len: int):     #разделение синхропосылки и текста в файле
    if len(data) < iv_len:
        raise ValueError("Файл слишком короткий, не хватает данных для IV (%d байт)." % iv_len)
    return data[:iv_len], data[iv_len:] #на выходе отдельно синхропосылка и данные




def main():
    print("Кузнечик (ГОСТ Р 34.12-2015) + режимы (ГОСТ Р 34.13-2015)\n")

    action = choose("Выберите действие:", ["Зашифровать файл", "Расшифровать файл"])

    mode = choose(
        "Выберите режим:",
        [
            "ECB — простая замена",
            "CBC — простая замена с зацеплением (m=n*z)",
            "CFB — гаммирование с обратной связью по шифртексту (m=n*z)",
            "CTR — гаммирование (счётчик)",
            "OFB — гаммирование с обратной связью по выходу (m=n*z)",
        ]
    )

    in_path = ask_existing_file("Путь к входному файлу: ")

    out_default = in_path + (".enc" if action == 1 else ".dec")
    out_path = ask_out_file(out_default)

    if os.path.abspath(in_path) == os.path.abspath(out_path):
        print("Ошибка, выходной файл должен отличаться от входного.")
        return
    if not confirm_overwrite(out_path):
        print("Отменено.")
        return

    key = ask_key()
    cipher = Kuznyechik(key)

    z = 1
    s_bytes = 16
    if mode in (2, 3, 5):  #CBC, CFB, OFB
        z = ask_z()
    if mode == 3:          #CFB
        s_bytes = ask_s_bytes()

    try:
        with open(in_path, "rb") as f:
            file_data = f.read()

        if action == 1:
            if mode == 1:  #ECB
                out_bytes = ecb_encrypt(cipher, file_data)
                print("ECB: IV не используется.")

            elif mode == 2:  #CBC
                iv = choose_iv_encrypt(mode=2, z=z)
                ct = cbc_encrypt(cipher, file_data, iv, z)
                out_bytes = iv + ct

            elif mode == 3:  #CFB
                iv = choose_iv_encrypt(mode=3, z=z)
                ct = cfb_crypt(cipher, file_data, iv, z, s_bytes=s_bytes, decrypt=False)
                out_bytes = iv + ct

            elif mode == 4:  #CTR
                iv = choose_iv_encrypt(mode=4, z=1)
                ct = ctr_crypt(cipher, file_data, iv)
                out_bytes = iv + ct

            elif mode == 5:  #OFB
                iv = choose_iv_encrypt(mode=5, z=z)
                ct = ofb_crypt(cipher, file_data, iv, z)
                out_bytes = iv + ct

            else:
                raise ValueError("Неизвестный режим.")

        else:
            if mode == 1:  #ECB
                out_bytes = ecb_decrypt(cipher, file_data)
                print("ECB: IV не используется.")

            elif mode == 2:  #CBC
                iv_len = BLOCK_SIZE * z
                iv, ct = split_iv_and_payload(file_data, iv_len)
                print("CBC: извлечён IV (hex): %s" % b2hex(iv))
                out_bytes = cbc_decrypt(cipher, ct, iv, z)

            elif mode == 3:  #CFB
                iv_len = BLOCK_SIZE * z
                iv, ct = split_iv_and_payload(file_data, iv_len)
                print("CFB: извлечён IV (hex): %s" % b2hex(iv))
                out_bytes = cfb_crypt(cipher, ct, iv, z, s_bytes=s_bytes, decrypt=True)

            elif mode == 4:  #CTR
                iv, ct = split_iv_and_payload(file_data, 8)
                print("CTR: извлечён IV (hex): %s" % b2hex(iv))
                out_bytes = ctr_crypt(cipher, ct, iv)

            elif mode == 5:  #OFB
                iv_len = BLOCK_SIZE * z
                iv, ct = split_iv_and_payload(file_data, iv_len)
                print("OFB: извлечён IV (hex): %s" % b2hex(iv))
                out_bytes = ofb_crypt(cipher, ct, iv, z)

            else:
                raise ValueError("Неизвестный режим.")

        with open(out_path, "wb") as f:
            f.write(out_bytes)

        print("Готово, результат сохранён в: %s" % out_path)

    except Exception as e:
        print("Ошибка: %s" % e)


if __name__ == "__main__":
    main()
