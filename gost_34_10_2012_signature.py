import os 
import random 


PI = [  #таблица подстановки S-преобразования Стрибога
    252, 238, 221, 17, 207, 110, 49, 22, 251, 196, 250, 218, 35, 197, 4, 77,
    233, 119, 240, 219, 147, 46, 153, 186, 23, 54, 241, 187, 20, 205, 95, 193,
    249, 24, 101, 90, 226, 92, 239, 33, 129, 28, 60, 66, 139, 1, 142, 79, 5, 132,
    2, 174, 227, 106, 143, 160, 6, 11, 237, 152, 127, 212, 211, 31, 235, 52, 44,
    81, 234, 200, 72, 171, 242, 42, 104, 162, 253, 58, 206, 204, 181, 112, 14, 86,
    8, 12, 118, 18, 191, 114, 19, 71, 156, 183, 93, 135, 21, 161, 150, 41, 16, 123,
    154, 199, 243, 145, 120, 111, 157, 158, 178, 177, 50, 117, 25, 61, 255, 53, 138,
    126, 109, 84, 198, 128, 195, 189, 13, 87, 223, 245, 36, 169, 62, 168, 67, 201,
    215, 121, 214, 246, 124, 34, 185, 3, 224, 15, 236, 222, 122, 148, 176, 188, 220,
    232, 40, 80, 78, 51, 10, 74, 167, 151, 96, 115, 30, 0, 98, 68, 26, 184, 56, 130,
    100, 159, 38, 65, 173, 69, 70, 146, 39, 94, 85, 47, 140, 163, 165, 125, 105, 213,
    149, 59, 7, 88, 179, 64, 134, 172, 29, 247, 48, 55, 107, 228, 136, 217, 231, 137,
    225, 27, 131, 73, 76, 63, 248, 254, 141, 83, 170, 144, 202, 216, 133, 97, 32,
    113, 103, 164, 45, 43, 9, 91, 203, 155, 37, 208, 190, 229, 108, 82, 89, 166, 116,
    210, 230, 244, 180, 192, 209, 102, 175, 194, 57, 75, 99, 182,
]

TAU = [  #таблица перестановки байтов для P-преобразования
    0, 8, 16, 24, 32, 40, 48, 56, 1, 9, 17, 25, 33, 41, 49, 57,
    2, 10, 18, 26, 34, 42, 50, 58, 3, 11, 19, 27, 35, 43, 51, 59,
    4, 12, 20, 28, 36, 44, 52, 60, 5, 13, 21, 29, 37, 45, 53, 61,
    6, 14, 22, 30, 38, 46, 54, 62, 7, 15, 23, 31, 39, 47, 55, 63,
]
#таблица 64 констант для линейного L-преобразования
A = [int(x, 16) for x in """ 
8e20faa72ba0b470 47107ddd9b505a38 ad08b0e0c3282d1c d8045870ef14980e
6c022c38f90a4c07 3601161cf205268d 1b8e0b0e798c13c8 83478b07b2468764
a011d380818e8f40 5086e740ce47c920 2843fd2067adea10 14aff010bdd87508
0ad97808d06cb404 05e23c0468365a02 8c711e02341b2d01 46b60f011a83988e
90dab52a387ae76f 486dd4151c3dfdb9 24b86a840e90f0d2 125c354207487869
092e94218d243cba 8a174a9ec8121e5d 4585254f64090fa0 accc9ca9328a8950
9d4df05d5f661451 c0a878a0a1330aa6 60543c50de970553 302a1e286fc58ca7
18150f14b9ec46dd 0c84890ad27623e0 0642ca05693b9f70 0321658cba93c138
86275df09ce8aaa8 439da0784e745554 afc0503c273aa42a d960281e9d1d5215
e230140fc0802984 71180a8960409a42 b60c05ca30204d21 5b068c651810a89e
456c34887a3805b9 ac361a443d1c8cd2 561b0d22900e4669 2b838811480723ba
9bcf4486248d9f5d c3e9224312c8c1a0 effa11af0964ee50 f97d86d98a327728
e4fa2054a80b329c 727d102a548b194e 39b008152acb8227 9258048415eb419d
492c024284fbaec0 aa16012142f35760 550b8e9e21f7a530 a48b474f9ef5dc18
70a6a56e2440598e 3853dc371220a247 1ca76e95091051ad 0edd37c48a08a6d8
07e095624504536c 8d70c431ac02a736 c83862965601dd1b 641c314b2b8ee083
""".split()]
#12 раундовых констант для преобразования ключа в функции E
C = [bytes.fromhex(x) for x in """
b1085bda1ecadae9ebcb2f81c0657c1f2f6a76432e45d016714eb88d7585c4fc4b7ce09192676901a2422a08a460d31505767436cc744d23dd806559f2a64507
6fa3b58aa99d2f1a4fe39d460f70b5d7f3feea720a232b9861d55e0f16b501319ab5176b12d699585cb561c2db0aa7ca55dda21bd7cbcd56e679047021b19bb7
f574dcac2bce2fc70a39fc286a3d843506f15e5f529c1f8bf2ea7514b1297b7bd3e20fe490359eb1c1c93a376062db09c2b6f443867adb31991e96f50aba0ab2
ef1fdfb3e81566d2f948e1a05d71e4dd488e857e335c3c7d9d721cad685e353fa9d72c82ed03d675d8b71333935203be3453eaa193e837f1220cbebc84e3d12e
4bea6bacad4747999a3f410c6ca923637f151c1f1686104a359e35d7800fffbdbfcd1747253af5a3dfff00b723271a167a56a27ea9ea63f5601758fd7c6cfe57
ae4faeae1d3ad3d96fa4c33b7a3039c02d66c4f95142a46c187f9ab49af08ec6cffaa6b71c9ab7b40af21f66c2bec6b6bf71c57236904f35fa68407a46647d6e
f4c70e16eeaac5ec51ac86febf240954399ec6c7e6bf87c9d3473e33197a93c90992abc52d822c3706476983284a05043517454ca23c4af38886564d3a14d493
9b1f5b424d93c9a703e7aa020c6e41414eb7f8719c36de1e89b4443b4ddbc49af4892bcb929b069069d18d2bd1a5c42f36acc2355951a8d9a47f0dd4bf02e71e
378f5a541631229b944c9ad8ec165fde3a7d3a1b258942243cd955b7e00d0984800a440bdbb2ceb17b2b8a9aa6079c540e38dc92cb1f2a607261445183235adb
abbedea680056f52382ae548b2e4f3f38941e71cff8a78db1fffe18a1b3361039fe76702af69334b7a1e6c303b7652f43698fad1153bb6c374b4c7fb98459ced
7bcd9ed0efc889fb3002c6cd635afe94d8fa6bbbebab076120018021148466798a1d71efea48b9caefbacd1d7d476e98dea2594ac06fd85d6bcaa4cd81f32d1b
378ee767f11631bad21380b00449b17acda43c32bcdf1d77f82012d430219f9b5d80ef9d1891cc86e71da4aa88e12852faf417d5d9b21b9948bc924af11bd720
""".split()]


def xor512(a, b):  #побитовое XOR двух 512-битных последовательностей
    return bytes(x ^ y for x, y in zip(a, b))  #ксорит попарно байты a и b и собирает результат


def add_mod_2_512(a, b):  # Сложение двух чисел по модулю 2^512
    return ((a + b) % (1 << 512)).to_bytes(64, "big")  #складываем, берем остаток и переводим в 64 байта


def transform_s(data):  #S-преобразование Стрибога
    return bytes(PI[b] for b in data)  #заменяет каждый байт по таблице PI


def transform_p(data):  #P-преобразование Стрибога
    return bytes(data[TAU[i]] for i in range(64))  #переставляет байты по индексам из TAU


def transform_l(data):  #L-преобразование Стрибога
    result = bytearray(64)              #создает массив результата на 64 байта
    for block_index in range(8):                #обрабатывает 8 блоков по 8 байт
        t = 0               #накопитель результата для одного 64-битного блока
        for byte_index in range(8):                     #проходит по байтам текущего блока
            current = data[block_index * 8 + byte_index]     #берет очередной байт текущего блока
            for bit_index in range(8):                              #проходит по всем битам байта
                if current & (1 << (7 - bit_index)):                        #проверяет, установлен ли очередной бит
                    t ^= A[byte_index * 8 + bit_index]  #если бит равен 1, ксорит t с нужной константой из A
        result[block_index * 8:(block_index + 1) * 8] = t.to_bytes(8, "big")  #записывает результат 8-байтового блока
    return bytes(result)     #возвращает итог как неизменяемую байтовую строку


def transform_lps(data): 
    return transform_l(transform_p(transform_s(data)))  #LPS


def encryption_e(key, message):  #внутреннее преобразование E в хэш-функции
    state = message                     #начальное состояние равно входному сообщению
    round_key = key                                 #начальный раундовый ключ
    for i in range(12):        #выполняет 12 раундов
        state = transform_lps(xor512(state, round_key))  #ксор состояния с ключом и применение LPS
        round_key = transform_lps(xor512(round_key, C[i]))          #обновление раундового ключа через константу C[i]
    return xor512(state, round_key)             #финальный ксор состояния с последним раундовым ключом


def compression_g(n_value, h_value, message_block):  #функция сжатия g_N
    key = transform_lps(xor512(h_value, n_value))      #формирует ключ из h и N
    return xor512(xor512(encryption_e(key, message_block), h_value), message_block)        


def gost3411_2012_hash(message, digest_size_bits):  #основная функция хэширования 
    if digest_size_bits not in (256, 512):              #проверка на допустимую длину хэша
        raise ValueError("Допустимы только длины хэш-кода 256 или 512 бит.")  # Ошибка при неверной длине

    h = bytes([1]) * 64 if digest_size_bits == 256 else bytes(64)  #начальное значение h из единиц для 256 бит и из нулей для 512 бит
    n_value = bytes(64)                 #счетчик длины обработанных данных N
    sigma = bytes(64)                           #контрольная сумма обработанных блоков 
    remaining = message                     #копия исходного сообщения для поэтапной обработки

    while len(remaining) >= 64:             #пока есть полные 64-байтовые блоки
        block = remaining[-64:]                     #берем последний полный блок
        remaining = remaining[:-64]                     #удаляем этот блок из оставшейся части
        h = compression_g(n_value, h, block)                #обновляем внутреннее сост h
        n_value = add_mod_2_512(int.from_bytes(n_value, "big"), 512)        #увеличивает N на 512 бит
        sigma = add_mod_2_512(int.from_bytes(sigma, "big"), int.from_bytes(block, "big"))           #добавляет блок к сумме

    final_block = b"\x00" * (63 - len(remaining)) + b"\x01" + remaining             #формирует последний блок с дополнением
    h = compression_g(n_value, h, final_block)                      #обрабатывает последний блок
    n_value = add_mod_2_512(int.from_bytes(n_value, "big"), len(remaining) * 8)             #прибавляет длину остатка в битах
    sigma = add_mod_2_512(int.from_bytes(sigma, "big"), int.from_bytes(final_block, "big"))         #добавляет последний блок к сумме

    zero = bytes(64)            #64 байта нулей для заключительных преобразований
    h = compression_g(zero, h, n_value)         #сжимает с учетом итогового N
    h = compression_g(zero, h, sigma)                   #сжимает с учетом итоговой суммы

    if digest_size_bits == 256:  #если 256-битный хэш
        return h[:32]  #возвращает первые 32 байта
    return h  #иначе полный 512-битный хэш



class CurveParams:  # Класс параметров эллиптической кривой
    def __init__(self, p, a, b, q, px, py, name="", source=""): 
        self.p = p  #модуль поля
        self.a = a  # a 
        self.b = b  #  b 
        self.q = q  #порядок подгруппы
        self.px = px  #X-координата базовой точки
        self.py = py  #Y-координата базовой точки
        self.name = name  #имя набора параметров
        self.source = source  #источник параметров

    @property
    def l_bits(self):               #свойство длины q в битах
        return 256 if self.q.bit_length() <= 256 else 512  #возвращает 256 или 512 в зависимости от размера q

    @property
    def l_bytes(self):      #свойство длины q в байтах
        return self.l_bits // 8     #переводит длину из бит в байты

    @property
    def hash_size_bits(self):       #свойство длины используемого хэша
        return self.l_bits              #длина хэша по длине q


class Point:  #класс точки кривой
    def __init__(self, x=None, y=None, inf=False): 
        self.x = x              #X-координата точки
        self.y = y              #Y-координата точки
        self.inf = inf          #Флаг бесконечно удаленной точки

    @staticmethod
    def infinity(): 
        return Point(None, None, True)  #на выходе бесконечно удал точка


class PrivateKey:  #класс закрытого ключа
    def __init__(self, curve, d): 
        self.curve = curve  #параметры кривой
        self.d = d  #секретное  d


class PublicKey:  #класс открытого ключа
    def __init__(self, curve, qx, qy): 
        self.curve = curve  #параметры кривой
        self.qx = qx  #X-координата открытого ключа
        self.qy = qy  #Y-координата открытого ключа


class Signature:  #класс электронной подписи
    def __init__(self, r, s): 
        self.r = r  #первая компонента подписи
        self.s = s  #вторая компонента подписи

    def to_bytes(self, l_bytes):  #метод перевода подписи в байты
        return self.r.to_bytes(l_bytes, "big") + self.s.to_bytes(l_bytes, "big")  # конкатенация r и s


INF = Point.infinity()  #бесконечно удаленная точка

BUILTIN_CURVE = CurveParams(  #встроенные параметры кривой из примера ГОСТ
    p=int("8000000000000000000000000000000000000000000000000000000000000431", 16),  #модуль p
    a=7,  #Коэффициент a
    b=int("5FBFF498AA938CE739B8E022FBAFEF40563F6E6A3472FC2A514C0CE9DAE23B7E", 16),  #коэффициент b
    q=int("8000000000000000000000000000000150FE8A1892976154C59CFC193ACCF5B3", 16),  #порядок подгруппы q
    px=2,  #X-координата базовой точки
    py=int("08E2A8A0E65147D4BD6316030E16D19C85C97F0A9CA267122B96ABBCEA7E8FC8", 16),  #Y-координата базовой точки
    name="appendix_a_example_1",  #имя набора параметров
    source="GOST R 34.10-2012, Приложение А, пример 1",  #источник параметров
)

SYS_RNG = random.SystemRandom()  #генератор случайных чисел


def int_to_hex(value):  #переводит число в hex-строку без 0x
    return format(value, "x")


def parse_int(value):  # Преобразует строку или число в int
    if isinstance(value, int):  #если значение уже число
        return value  
    cleaned = value.strip().lower()  #пробелы и к нижнему регистру
    if cleaned.startswith("0x"):  # Если число записано с префиксом 0x
        return int(cleaned, 16)  #парсит как hex
    if cleaned and all(ch in "0123456789abcdef" for ch in cleaned):  #если строка состоит только из hex-символов
        return int(cleaned, 16)  #парсит как hex
    return int(cleaned, 10)  #иначе парсит как десятичное число


def mod_inv(a, m):  #вычисляет обратный элемент a mod m
    a %= m  # Приводит a mod m
    if a == 0:  
        raise ZeroDivisionError("Обратный элемент не существует.") 

    old_r, r = m, a  #переменные для расширенного алгоритма Евклида
    old_s, s = 1, 0  #вспомогательные коэффициенты
    old_t, t = 0, 1  

    while r != 0:  #пока остаток не 0
        quotient = old_r // r  #частное от деления
        old_r, r = r, old_r - quotient * r  #обновляет остатки
        old_s, s = s, old_s - quotient * s  #обновляет коэффициенты
        old_t, t = t, old_t - quotient * t 

    if old_r != 1:  #если gcd(a, m) не равен 1
        raise ValueError("Обратный элемент не существует.") 
    return old_t % m  # на выходе обратный элемент по модулю m


def is_on_curve(curve, point):  #проверка принадлежность точки эллиптической кривой
    if point.inf:  #бесконечно удал точка корректна
        return True 
    left = (point.y * point.y) % curve.p  #вычисляет лев часть
    right = (point.x * point.x * point.x + curve.a * point.x + curve.b) % curve.p  #вычисляет правую часть x^3 + ax + b mod p
    return left == right  #сравн лев и прав части


def negate_point(curve, point):  #противоположн точка
    if point.inf:  #если точка бесконечно удаленная
        return point  #возвращает ее же
    return Point(point.x, (-point.y) % curve.p)  #меняет знак y по модулю p


def point_add(curve, p1, p2):  #сложение двух точек кривой
    if p1.inf:  #если первая точка бесконечно удаленная
        return p2  #результат равен второй точке
    if p2.inf:  #если вторая точка бесконечно удаленная
        return p1  #результат равен первой точке

    p = curve.p  #сохраняет модуль поля

    if p1.x == p2.x and (p1.y + p2.y) % p == 0:  #если точки противоположны
        return INF  #их сумма равна бесконеч удал

    if p1.x == p2.x and p1.y == p2.y:  #если выполняется удвоение точки
        if p1.y % p == 0:  #   если y равно 0
            return INF              #бескон
        lam = ((3 * p1.x * p1.x + curve.a) * mod_inv(2 * p1.y, p)) % p 
    else:                   #если складываются разные точки
        lam = ((p2.y - p1.y) * mod_inv(p2.x - p1.x, p)) % p  

    x3 = (lam * lam - p1.x - p2.x) % p  #вычисляет x-координату новой точки
    y3 = (lam * (p1.x - x3) - p1.y) % p  #вычисляет y-координату новой точки
    return Point(x3, y3)  #сумма точек


def scalar_mul(curve, k, point):  #умножение точки на число k
    if k == 0 or point.inf:  #если множитель 0 или точка бесконечна
        return INF  #бесконеч удал
    if k < 0:  # Если k отрицательное
        return scalar_mul(curve, -k, negate_point(curve, point))  #меняет знак точки и берет положительное k

    result = INF  #нач результат
    addend = point  #текущее слагаемое
    n = k  #рабочая копия множителя
    while n > 0:  #пока не обработаны все биты k
        if n & 1:  #если младший бит равен 1
            result = point_add(curve, result, addend)  #прибавляет текущее слагаемое к результату
        addend = point_add(curve, addend, addend)  #удваивает текущее слагаемое
        n >>= 1  #сдвигает множитель вправо
    return result  #возвращает k * point


def validate_curve(curve):  #проверяет корректность параметров кривой
    discriminant = (4 * pow(curve.a, 3, curve.p) + 27 * pow(curve.b, 2, curve.p)) % curve.p  #дискриминант
    if discriminant == 0:  
        raise ValueError("Некорректная кривая, дискриминант равен нулю по модулю p.")  # Кривая вырождена

    if not (curve.p > 3 and curve.q > 0):  # Проверяет допустимость p и q
        raise ValueError("Некорректные параметры поля или порядка q.") 

    base = Point(curve.px, curve.py)  #создает базовую точку
    if not is_on_curve(curve, base):  #проверяет принадлежность базовой точки кривой
        raise ValueError("Некорректная кривая, базовая точка не принадлежит кривой.") 

    if not scalar_mul(curve, curve.q, base).inf:  #проверяет, что qP = O
        raise ValueError("Некорректная кривая, qP не равно бесконечно удаленной точке.") 


def validate_public_key(public_key):                #проверяет корректность открытого ключа
    validate_curve(public_key.curve)                    #сначала проверяет саму кривую
    point = Point(public_key.qx, public_key.qy)             #создает точку открытого ключа
    if not is_on_curve(public_key.curve, point):                #проверяет, принадлежит ли ключ кривой
        raise ValueError("Открытый ключ не принадлежит эллиптической кривой.")  
    if not scalar_mul(public_key.curve, public_key.curve.q, point).inf:  #проверяет, лежит ли ключ в подгруппе порядка q
        raise ValueError("Открытый ключ не лежит в подгруппе порядка q.")  


def public_from_private(private_key):  #строит открытый ключ из закрытого
    q_point = scalar_mul(       #вычисляет Q = dP
        private_key.curve,              #параметры кривой
        private_key.d,                          #закрытый ключ d
        Point(private_key.curve.px, private_key.curve.py)           #базовая точка P
    )
    return PublicKey(private_key.curve, q_point.x, q_point.y)  #на выходе открытый ключ с координатами Q


def generate_keypair(curve):  #генерирует пару ключей
    validate_curve(curve)  #проверяет корректность параметров кривой
    d = SYS_RNG.randrange(1, curve.q)  #случайно выбирает d из диапазона 1 <= d < q
    private_key = PrivateKey(curve, d)  #создает объект закрытого ключа
    public_key = public_from_private(private_key)  #строит открытый ключ
    return private_key, public_key  #возвращает пару ключей


def digest_to_e(curve, digest):         #преобразует хэш в значение e
    expected = curve.hash_size_bits // 8    #ожидаемая длину хэша в байтах
    if len(digest) != expected:                 #проверяет длину хэша
        raise ValueError("Неверная длина хэша для выбранной кривой.") 
    alpha = int.from_bytes(digest, "big")   #хэш из байтов в число
    e = alpha % curve.q  #e как остаток от деления на q
    return 1 if e == 0 else e  #если e получилось 0, возвращает 1


def normalize_e(curve, e):  #нормализует значение e по модулю q
    e = e % curve.q  # e по модулю q
    return 1 if e == 0 else e  #если e получилось нулем, заменяет на 1


def sign_with_e_and_k(private_key, e, k):  #формирует подпись по известным e и k
    curve = private_key.curve                       #                извлекает параметры кривой
    if not (0 < private_key.d < curve.q):               #проверяет корректность d
        raise ValueError("Закрытый ключ должен удовлетворять 0 < d < q.") 
    if not (0 < k < curve.q):  # Проверяет корректность k
        raise ValueError("Параметр k должен удовлетворять 0 < k < q.")  

    e = normalize_e(curve, e)  #нормализует e
    base = Point(curve.px, curve.py)  #создает базовую точку P
    c_point = scalar_mul(curve, k, base)  #вычисляет C = kP

    if c_point.inf:  #если получилась бесконечно удаленная точка
        raise ValueError("Получена бесконечно удаленная точка, выберите другой k.") 

    r = c_point.x % curve.q  # Считает r = x_C mod q
    if r == 0:  # Если r = 0
        raise ValueError("Получено r = 0, выберите другой k.") 

    s = (r * private_key.d + k * e) % curve.q  # Считает s = (rd + ke) mod q
    if s == 0:  # Если s = 0
        raise ValueError("Получено s = 0, выберите другой k.") 

    return Signature(r, s)  #на выходе готовая подпись


def sign_digest(private_key, digest):  #формирует подпись по хэшу
    curve = private_key.curve  # извлекает параметры кривой
    e = digest_to_e(curve, digest)  #вычисляет e из хэша

    while True:             #цикл подбора корректного k
        k = SYS_RNG.randrange(1, curve.q)  #случайно  k
        try:  
            signature = sign_with_e_and_k(private_key, e, k)  #считает подпись
            return signature, e, k  #возвращает подпись и использованные e, k
        except ValueError:  #если k дал r=0 или s=0
            continue                #пробует новое значение k



def verify_digest(public_key, signature, digest):               #проверка подписи по хэшу файла
    validate_public_key(public_key)                      #проверяет корректность открытого ключа
    curve = public_key.curve 
    r = signature.r  
    s = signature.s  

    if not (0 < r < curve.q and 0 < s < curve.q):  #проверяет допустимость r и s
        return False  #если r или s вне диапазона, подпись неверна

    e = digest_to_e(curve, digest)  #вычисляет e из хэша
    v = mod_inv(e, curve.q)  #считает v = e^(-1) mod q
    z1 = (s * v) % curve.q  #считает z1 = s * v mod q
    z2 = (-r * v) % curve.q  #считает z2 = -r * v mod q

    base = Point(curve.px, curve.py)  #создает базовую точку P
    q_point = Point(public_key.qx, public_key.qy)  #создает точку открытого ключа Q
    c_point = point_add(curve, scalar_mul(curve, z1, base), scalar_mul(curve, z2, q_point))  #считает C = z1P + z2Q

    if c_point.inf:  #если получилась бесконеч удал
        return False  #подпись неверна

    r_check = c_point.x % curve.q  #считает проверочное значение r
    return r_check == r  #тру если совпало


def verify_with_e(public_key, signature, e_value):  #проверяет подпись по заранее известному e
    validate_public_key(public_key)         #проверяет корректность открытого ключа
    curve = public_key.curve  
    r = signature.r  
    s = signature.s 

    if not (0 < r < curve.q and 0 < s < curve.q):  #проверяет допустимость r и s
        return False                        #если знач вне диапазона, подпись неверна

    e = normalize_e(curve, e_value)  #нормализует переданное e
    v = mod_inv(e, curve.q)  
    z1 = (s * v) % curve.q  
    z2 = (-r * v) % curve.q  

    base = Point(curve.px, curve.py)  #создает базовую точку P
    q_point = Point(public_key.qx, public_key.qy)  #создает точку открытого ключа Q
    c_point = point_add(curve, scalar_mul(curve, z1, base), scalar_mul(curve, z2, q_point))  #считает C = z1P + z2Q

    if c_point.inf:  
        return False 

    r_check = c_point.x % curve.q  #считает проверочное r
    return r_check == r             #сравнивает проверочное r с исходным



def write_txt_map(path, data):  #аписывает словарь в тхт-файл в формате ключ=значение
    lines = [] 
    for key, value in data.items():  
        lines.append(str(key) + "=" + str(value))  #формирует строку key=value
    with open(path, "w", encoding="utf-8") as f:  #открывает файл на запись
        f.write("\n".join(lines) + "\n")  #записывает все строки через перевод строки


def read_txt_map(path):  #читает TXT-файл формата key=value в словарь
    result = {}  #словарь результата
    with open(path, "r", encoding="utf-8") as f:  #открывает файл на чтение
        lines = f.read().splitlines()  #считывает все строки без символов перевода строки

    line_number = 0  #счетчик номера строки
    for raw_line in lines:  #проходит по всем строкам файла
        line_number += 1            #увеличивает номер строки
        line = raw_line.strip()                 #убирает пробелы по краям
        if not line or line.startswith("#"):  #         пропускает пустые строки и комментарии
            continue                  
        if "=" not in line: 
            raise ValueError("Некорректная строка {} в файле {}: отсутствует '='.".format(line_number, path)) 
        key, value = line.split("=", 1)  
        key = key.strip()               #убирает пробелы 
        value = value.strip()               #убирает пробелы вокруг значения
        if not key:  
            raise ValueError("Некорректная строка {} в файле {}: пустое имя поля.".format(line_number, path)) 
        result[key] = value 
    return result 


def curve_to_txt_map(curve):  #преобразует параметры кривой в словарь для сохранения
    return {
        "type": "curve_params", 
        "name": curve.name,  
        "source": curve.source,  
        "p": int_to_hex(curve.p),  
        "a": int_to_hex(curve.a),  
        "b": int_to_hex(curve.b), 
        "q": int_to_hex(curve.q), 
        "px": int_to_hex(curve.px), 
        "py": int_to_hex(curve.py), 
    }


def curve_from_txt_map(data): 
    return CurveParams(
        p=parse_int(data["p"]),  
        a=parse_int(data["a"]),  
        b=parse_int(data["b"]),
        q=parse_int(data["q"]), 
        px=parse_int(data["px"]), 
        py=parse_int(data["py"]), 
        name=data.get("name", ""),  
        source=data.get("source", ""),  
    )


def save_curve_params(path, curve):             #сохраняет параметры кривой в файл
    write_txt_map(path, curve_to_txt_map(curve))  #преобразует кривую в словарь и записывает в файл


def load_curve_params(path):  #загружает параметры кривой из файла
    return curve_from_txt_map(read_txt_map(path))  #читает словарь из файла и строит объект CurveParams


def save_private_key(path, private_key):                #сохраняет закрытый ключ в файл
    data = curve_to_txt_map(private_key.curve)  #берет словарь параметров кривой
    data.update({
        "type": "private_key",  
        "algorithm": "GOST R 34.10-2012",  
        "d": int_to_hex(private_key.d),  
    })
    write_txt_map(path, data) 


def save_public_key(path, public_key):  #сохраняет открытый ключ в файл
    data = curve_to_txt_map(public_key.curve)  #берет словарь параметров кривой
    data.update({
        "type": "public_key",  
        "algorithm": "GOST R 34.10-2012",  
        "qx": int_to_hex(public_key.qx),  
        "qy": int_to_hex(public_key.qy), 
    })
    write_txt_map(path, data)  


def save_signature(path, signature, curve, digest, file_path, e_value=None, k_value=None, mode_name="standard"):  #сохраняет подпись в файл
    data = {
        "type": "signature",  
        "algorithm": "GOST R 34.10-2012",  
        "signature_encoding": "r||s",  
        "mode": mode_name,  
        "l_bits": str(curve.l_bits),  
        "hash_algorithm": "GOST R 34.11-2012 ({} bits)".format(curve.hash_size_bits),  
        "signed_file": str(file_path), 
        "digest_hex": digest.hex() if digest is not None else "", 
        "r": int_to_hex(signature.r),  # Компонента r
        "s": int_to_hex(signature.s),  # Компонента s
        "signature_hex": signature.to_bytes(curve.l_bytes).hex(),  # Подпись как r||s
    }
    if e_value is not None:  #если есть значение e
        data["e"] = int_to_hex(e_value)  #сохраняет e
    if k_value is not None:  #если есть значение k
        data["k"] = int_to_hex(k_value)  #сохраняет k
    write_txt_map(path, data) 


def load_private_key(path):  #загружает закрытый ключ из файла
    data = read_txt_map(path)  #читает словарь из файла
    if data.get("type") != "private_key":  # Проверяет тип файла
        raise ValueError("Указанный TXT-файл не является файлом закрытого ключа.")  
    curve = curve_from_txt_map(data)  
    return PrivateKey(curve, parse_int(data["d"]))  #возвращает объект закрытого ключа


def load_public_key(path):  #загружает открытый ключ из файла
    data = read_txt_map(path)  #читает словарь из файла
    if data.get("type") != "public_key":            #проверяет тип файла
        raise ValueError("Указанный TXT-файл не является файлом открытого ключа.")  
    curve = curve_from_txt_map(data)  # Восстанавливает параметры кривой
    return PublicKey(curve, parse_int(data["qx"]), parse_int(data["qy"])) 


def load_signature(path):  # Загружает только r и s из файла подписи
    data = read_txt_map(path)  # Читает словарь из файла
    if data.get("type") != "signature":  # Проверяет тип файла
        raise ValueError("Указанный TXT-файл не является файлом подписи.") 
    return Signature(parse_int(data["r"]), parse_int(data["s"]))  # Возвращает объект подписи


def load_signature_full(path):  # Загружает все данные из файла подписи
    data = read_txt_map(path) 
    if data.get("type") != "signature": 
        raise ValueError("Указанный TXT-файл не является файлом подписи.") 
    return data  # Возвращает полный словарь данных подписи


def prompt_nonempty(message):  # Запрашивает у пользователя непустую строку
    while True:  
        value = input(message).strip() 
        if value: 
            return value 
        print("Пустой ввод недопустим.") 


def prompt_yes_no(message):  # Запрашивает ответ да/нет
    while True:  # Цикл до корректного ввода
        value = input(message).strip().lower()  #читает строку и приводит к нижнему регистру
        if value in ("1", "да", "д", "y", "yes"): 
            return True  
        if value in ("0", "нет", "н", "n", "no"): 
            return False  
        print("Введите 1/0, да/нет.")  


def prompt_hex_or_dec_int(message):  #запрашивает число в hex или dec формате
    value = prompt_nonempty(message)  #сначала получает непустую строку
    return parse_int(value)  #преобразует строку в число


def prompt_menu_choice(): 
    print() 
    print("Выберите действие:") 
    print("1 - Сгенерировать ключевую пару")  
    print("2 - Сформировать электронную подпись файла")  
    print("3 - Проверить электронную подпись файла") 
    print("4 - Режим примера ГОСТ (ручной ввод d, e, k)")  
    print("0 - Выход")  
    return input("Ваш выбор: ").strip() 


def prompt_mode_choice():  
    print() 
    print("Выберите режим формирования подписи:")  
    print("1 - Обычный режим ГОСТ (хэш файла, случайный k)") 
    print("2 - Режим точного воспроизведения примера ГОСТ") 
    return input("Ваш выбор [1/2]: ").strip() or "1"  


def select_curve_for_generation():  # Выбирает параметры кривой для генерации ключей
    print()  
    print("Параметры эллиптической кривой:")  
    print("1 - Встроенные параметры из ГОСТ Р 34.10-2012")  
    print("2 - Загрузить параметры кривой из TXT-файла")  
    choice = input("Ваш выбор [1/2]: ").strip() or "1"  

    if choice == "1":  
        return BUILTIN_CURVE  #возвращает встроенную кривую
    if choice == "2": 
        curve_path = prompt_nonempty("Введите путь к TXT-файлу с параметрами кривой: ")  
        curve = load_curve_params(curve_path) 
        validate_curve(curve) 
        return curve 

    raise ValueError("Некорректный выбор параметров кривой.")  


def read_file_bytes(path):  #читает файл как набор байтов
    with open(path, "rb") as f:  #открывает файл в бинарном режиме
        return f.read()  #возвращает все байты файла


def hash_file_for_curve(file_path, curve):  #хэширует файл с учетом размера q кривой
    data = read_file_bytes(file_path)  #читает байты файла
    return gost3411_2012_hash(data, curve.hash_size_bits)  #вычисляет хэш нужной длины


def print_curve_params(curve):  
    print() 
    print("Параметры кривой ГОСТ:")  
    print("name =", curve.name)  
    print("source =", curve.source)  
    print("p  =", int_to_hex(curve.p))  
    print("a  =", int_to_hex(curve.a))  
    print("b  =", int_to_hex(curve.b)) 
    print("q  =", int_to_hex(curve.q))
    print("px =", int_to_hex(curve.px))  
    print("py =", int_to_hex(curve.py))  
    print("Размер q =", curve.l_bits, "бит")  


def action_generate_keys():  #выполняет сценарий генерации ключевой пары
    curve = select_curve_for_generation() 
    private_path = prompt_nonempty("Введите путь для сохранения закрытого ключа: ") 
    public_path = prompt_nonempty("Введите путь для сохранения открытого ключа: ") 

    private_key, public_key = generate_keypair(curve) 
    save_private_key(private_path, private_key)  #сохраняет закрытый ключ
    save_public_key(public_path, public_key)  #сохраняет открытый ключ

    print() 
    print("Ключевая пара успешно сгенерирована.")  
    print("Закрытый ключ сохранен:", os.path.abspath(private_path)) 
    print("Открытый ключ сохранен:", os.path.abspath(public_path)) 
    print("Размер параметра q:", curve.l_bits, "бит")  
    print("Для подписи будет использоваться хэш ГОСТ Р 34.11-2012 на", curve.hash_size_bits, "бит")  


def action_sign_file_standard():  #выполняет стандартное формирование подписи файла
    file_path = prompt_nonempty("Введите путь к подписываемому файлу: ")  
    private_key_path = prompt_nonempty("Введите путь к TXT-файлу закрытого ключа: ")  
    signature_path = prompt_nonempty("Введите путь для сохранения TXT-файла подписи: ") 

    private_key = load_private_key(private_key_path)  #загружает закрытый ключ
    validate_curve(private_key.curve)  #проверяет корректность параметров кривой

    digest = hash_file_for_curve(file_path, private_key.curve)  #вычисляет хэш файла
    signature, e_value, k_value = sign_digest(private_key, digest)  #формирует подпись и получает e, k

    save_signature(  #сохраняет подпись в файл
        signature_path,  
        signature,  
        private_key.curve,  
        digest, 
        file_path, 
        e_value=e_value, 
        k_value=k_value,  
        mode_name="standard"  
    )

    derived_public_key = public_from_private(private_key)  #вычисляет открытый ключ из закрытого
    public_key_path = os.path.splitext(signature_path)[0] + "_public_key.txt"  #формирует путь для открытого ключа
    save_public_key(public_key_path, derived_public_key)            #сохраняет открытый ключ

    print()  # Пустая строка
    print("Электронная подпись успешно сформирована.")  
    print("Хэш файла:", digest.hex()) 
    print("e =", int_to_hex(e_value))  
    print("k =", int_to_hex(k_value))  
    print("r =", int_to_hex(signature.r))  
    print("s =", int_to_hex(signature.s))  
    print("Файл подписи сохранен:", os.path.abspath(signature_path))  
    print("Открытый ключ сохранен:", os.path.abspath(public_key_path))  


def action_sign_file_gost_example():  #выполняет формирование подписи в режиме примера ГОСТ
    print("Режим точного воспроизведения примера ГОСТ.")  

    curve = BUILTIN_CURVE       # Использует встроенные параметры кривой
    validate_curve(curve)           # Проверяет корректность встроенной кривой
    print_curve_params(curve)           # Печатает параметры кривой

    use_file = prompt_yes_no("Использовать реальный файл для расчета хэша? [1=да, 0=нет]: ")  

    digest = None  #заготовка для хэша
    file_path = ""  #заготовка для имени файла

    if use_file:  #если использовать реальный файл
        file_path = prompt_nonempty("Введите путь к файлу: ")  
        digest = hash_file_for_curve(file_path, curve)  
        print("Вычисленный хэш файла:", digest.hex())  
        calculated_e = digest_to_e(curve, digest)  
        print("e, полученное из хэша:", int_to_hex(calculated_e))  
    else:  # 
        print("Хэш файла не вычисляется. e вводится вручную из примера ГОСТ.")  

    d_value = prompt_hex_or_dec_int("Введите d из примера ГОСТ (hex или dec): ")  
    e_value = prompt_hex_or_dec_int("Введите e из примера ГОСТ (hex или dec): ")  
    k_value = prompt_hex_or_dec_int("Введите k из примера ГОСТ (hex или dec): ")  

    private_key = PrivateKey(curve, d_value)  #создает закрытый ключ из введенного d
    public_key = public_from_private(private_key)  #вычисляет соответствующий открытый ключ
    signature = sign_with_e_and_k(private_key, e_value, k_value)  #формирует подпись по заданным d, e, k

    signature_path = prompt_nonempty("Введите путь для сохранения TXT-файла подписи: ") 
    public_key_path = os.path.splitext(signature_path)[0] + "_public_key.txt"  #формирует путь для открытого ключа

    if digest is None:  #если хэш не вычислялся
        digest_for_file = b""  #использует пустую байтовую строку
    else: 
        digest_for_file = digest  #сохраняет реальный хэш

    save_signature(  
        signature_path,  
        signature,  #подпись
        curve, 
        digest_for_file,  
        file_path if file_path else "manual_gost_example", 
        e_value=e_value,  #значение e
        k_value=k_value,  #значение k
        mode_name="gost_example"  
    )
    save_public_key(public_key_path, public_key) 

    print() 
    print("Подпись в режиме примера ГОСТ сформирована.") 
    print("d  =", int_to_hex(d_value)) 
    print("e  =", int_to_hex(normalize_e(curve, e_value))) 
    print("k  =", int_to_hex(k_value)) 
    print("Qx =", int_to_hex(public_key.qx)) 
    print("Qy =", int_to_hex(public_key.qy))  
    print("r  =", int_to_hex(signature.r))  
    print("s  =", int_to_hex(signature.s))  
    print("Файл подписи сохранен:", os.path.abspath(signature_path))  
    print("Открытый ключ сохранен:", os.path.abspath(public_key_path)) 


def action_sign_file(): 
    mode = prompt_mode_choice()  
    if mode == "1": 
        action_sign_file_standard() 
    elif mode == "2": 
        action_sign_file_gost_example()  
    else: 
        raise ValueError("Некорректный выбор режима подписи.") 


def action_verify_file():  #выполняет проверку электронной подписи
    signature_path = prompt_nonempty("Введите путь к TXT-файлу подписи: ")  #запрашивает путь к подписи
    public_key_path = prompt_nonempty("Введите путь к TXT-файлу открытого ключа: ")  #запрашивает путь к открытому ключу

    signature_data = load_signature_full(signature_path)  #загружает все данные подписи
    public_key = load_public_key(public_key_path)  #загружает открытый ключ
    signature = Signature(parse_int(signature_data["r"]), parse_int(signature_data["s"]))  #создает объект подписи из r и s

    mode_name = signature_data.get("mode", "standard")  #определяет режим создания подписи
    signed_file = signature_data.get("signed_file", "")  #получает имя подписанного файла

    print() 
    print("Режим подписи:", mode_name) 

    if mode_name == "gost_example" and signed_file == "manual_gost_example":  #если это подпись режима ГОСТ без реального файла
        if "e" not in signature_data:  #проверяет, есть ли e в файле подписи
            raise ValueError("В файле подписи отсутствует значение e для проверки примера ГОСТ.")  

        e_value = parse_int(signature_data["e"]) 
        is_valid = verify_with_e(public_key, signature, e_value)  

        print("Используется контрольное значение e из примера ГОСТ:")  
        print("e =", int_to_hex(e_value))  

        if is_valid:  
            print("Результат проверки: подпись корректна.") 
        else: 
            print("Результат проверки: подпись некорректна.")
        return  

    file_path = prompt_nonempty("Введите путь к проверяемому файлу: ")  
    digest = hash_file_for_curve(file_path, public_key.curve)  #вычисляет хэш этого файла
    is_valid = verify_digest(public_key, signature, digest)  #проверяет подпись по хэшу файла

    print("Хэш файла:", digest.hex())  
    if is_valid: 
        print("Результат проверки: подпись корректна.")  
    else:  
        print("Результат проверки: подпись некорректна.")  


def print_header():  
    print("Программная реализация электронной цифровой подписи ГОСТ Р 34.10-2012") 


def main():
    print_header()
    while True:
        try:
            choice = prompt_menu_choice()
            if choice == "1":
                action_generate_keys()
            elif choice == "2":
                action_sign_file()
            elif choice == "3":
                action_verify_file()
            elif choice == "4":
                action_sign_file_gost_example()
            elif choice == "0":
                print("Работа завершена.")
                break
            else:
                print("Некорректный выбор. Повторите ввод.")
        except FileNotFoundError as exc:
            print("Ошибка: файл не найден:", exc)
        except Exception as exc:
            print("Ошибка:", exc)


if __name__ == "__main__":
    main()