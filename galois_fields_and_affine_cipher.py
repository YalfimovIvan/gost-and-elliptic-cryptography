import random

def print_polynomial(coeffs):  #Преобразует список коэффициентов в многочлен от старшего к младшему
    terms = [] 
    for i in range(len(coeffs)-1, -1, -1):                  #проход по индексам коэфов в обр порядке
        coeff = coeffs[i]
        if coeff != 0:
            if i == 0:
                terms.append(f"{coeff}")            #добавляем коэф как строку
            elif i == 1:
                terms.append(f"{coeff}x" if coeff != 1 else "x")            #x вместо 1x
            else:
                term = f"{coeff}x^{i}" if coeff != 1 else f"x^{i}"
                terms.append(term)
    return " + ".join(terms) if terms else "0"      #склеиваем через +




def generate_galois_field(p, n):       #генерирует все элементы поля Галуа
    elements = []
    for i in range(p**n):                   #перебор всех чисел от 0 до p^n-1
        coeffs = []
        num = i
        for _ in range(n):                      #для каждой из n позиций от мл ст к ст
            
            coeffs.append(num % p)              #коэф при текущей степени как остаток от дел на р
            
            num //= p                           #переход к след степени
        elements.append(coeffs)
    return elements



def has_roots(poly, p):             #проверка на неприводимость, есть ли у многочлена корни в поле F_p
    
    n = len(poly) - 1                                   #на вход степень многочлена - 1
    for x in range(p):              #перебор всех возм знач x в поле
        
        value = 0       #значение многоч в точке х
        for i, coeff in enumerate(poly):            
            value = (value + coeff * pow(x, i, p)) % p      #вычисл x^p modp, затем * x^i, после добавляем к value и берем по modp
        if value == 0:      #если 0, значит х корень
            return True
    return False



def poly_mod(a, b, p):                  #проверка на неприводимость, деление многочленов с остатком в поле, возвращает остаток, буквально как деление в столбик
    a = a[:]
    b = b[:]            #копии списков
    
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    while len(b) > 1 and b[-1] == 0:
        b.pop()
    
    deg_a = len(a) - 1      #ст делимого
    deg_b = len(b) - 1          #ст делителя
    
    if deg_a < deg_b:
        return a
    
    lead_coeff = b[deg_b]       #старший коэф делителя
    if lead_coeff != 1:
        inv_lead = pow(lead_coeff, p-2, p)      #находим обратный к старш коэф в поле
        b = [(coeff * inv_lead) % p for coeff in b]
        a = [(coeff * inv_lead) % p for coeff in a]         #умножаем все коэфы на обратный, чтобы ст коэф стал =1
    
    for i in range(deg_a - deg_b, -1, -1):      #цикл деления от самой высокой степени в частном до 0
        if a[i + deg_b] != 0:
            factor = a[i + deg_b]       #текущий коэф
            for j in range(deg_b + 1):
                a[i + j] = (a[i + j] - factor * b[j]) % p   #вычитаем из делимого и удаляем ведущие нули из остатка
    
    while len(a) > 1 and a[-1] == 0:
        a.pop()         #удаляем ласт нулевой коэф
    
    return a        #на выходе остаток от деления 


def is_irreducible_naive(poly, p):        #проверка неприводимости перебором для небольших n
    n = len(poly) - 1                                   #степень многочлена на вход
    
    if has_roots(poly, p):                              #если корень, то точно приводим
        return False
    
    for k in range(1, n // 2 + 1):      #полный перебор всех возм делителей
                    #к - степень делителя потенц
        for i in range(p ** (k + 1)):           #перебор всех возм многочленов
            divisor = []
            num = i
            for _ in range(k + 1):          #генерир к+1 коэф 
                divisor.append(num % p)     #коэф как цифра в p-системе
                num //= p               #переход к след цифре
            
            if divisor[-1] == 0:            #пропускаем делители со ст коэф 0
                continue
            
            if len(divisor) < 2:                #пропуск делит дл <2, т.е. константы
                continue
            
            remainder = poly_mod(poly, divisor, p)          #деление исходного на потенциальный делитель
            if len(remainder) == 1 and remainder[0] == 0:       #если нашли делитель - приводим
                return False
    
    return True



def is_irreducible(poly, p):        #проверка на неприводимость основа
    n = len(poly) - 1
    
    if n <= 8:
        return is_irreducible_naive(poly, p)
    else:
        if has_roots(poly, p):
            return False        #для степени >8 проверка неполная, опора только на корни
        else:
            return True







def input_polynomial(p, n):             #ввод неприводимого многочлена    
    print(f"\nВведите коэффициенты неприводимого многочлена степени {n} над F_{p}")
    print(f"Пример для степени 2: [1, 1, 1] соответствует x² + x + 1")
    
    while True:
        try:
            coeffs = list(map(int, input("Введите коэффициенты: ").split()))
            
            if len(coeffs) != n + 1:
                print(f"Неа, многочлен должен иметь {n+1} коэффициентов (степень {n})")
                continue
                
            if coeffs[0] != 1:
                print("Неа, старший коэффициент должен быть равен 1")
                continue
                
            if any(c < 0 or c >= p for c in coeffs):
                print(f"Неа, все коэффициенты должны быть в диапазоне [0, {p-1}]")
                continue
            coeffs = coeffs[::-1]               #преобразуем к внутреннему формату от младшего к старшему
            
            if not is_irreducible(coeffs, p):
                print("Ошибка, многочлен приводим над F_p")         #проверка на неприводимость после ввода
                continue
                
            return coeffs
            
        except ValueError:
            print("Ошибка, введите целые числа, разделенные пробелами")

def generate_irreducible_polynomial(p, n):                           #генерирует случайный неприводимый многочлен степени n над Fp
    known_irreducible = {
        (2, 2): [1, 1, 1],
        (2, 3): [1, 1, 0, 1],
        (2, 4): [1, 1, 0, 0, 1],
        (2, 5): [1, 0, 1, 0, 0, 1],
        (2, 6): [1, 1, 0, 0, 0, 0, 1],
        (2, 7): [1, 1, 0, 0, 0, 0, 0, 1],
        (2, 8): [1, 1, 0, 0, 0, 1, 1, 0, 1],
        (3, 2): [1, 1, 2],
        (3, 3): [1, 2, 0, 1],
    }
    
    if (p, n) in known_irreducible:
        poly = known_irreducible[(p, n)]
        print(f"Сгенерирован многочлен: {print_polynomial(poly)}")
        return poly
    else:
        max_attempts = 1000     #макс число попыток
        for attempt in range(max_attempts):
            poly = [1]          #старший коэф всегда 1
            for _ in range(n - 1):           #генерация коэффициентов <n
                poly.append(random.randint(0, p - 1))
            poly.append(random.randint(1, p - 1))           #свободный член
            
            if is_irreducible(poly, p):
                print(f"Сгенерирован многочлен: {print_polynomial(poly)}")          #проверка на неприводимость после генерации
                print(f"(Потребовалось попыток: {attempt + 1})")
                return poly
        
        print("Не удалось найти неприводимый многочлен за 1000 попыток")
        return None

def display_field_info(p, n, field_order, multiplicative_group_order, irreducible_poly=None):       #Отображает информацию о поле
    print(f"\n{'='*50}")
    print(f"Поле Галуа: F_{p}^{n} = F_{field_order}")
    print(f"{'='*50}")
    print(f"Порядок поля: {field_order}")
    print(f"Порядок мультипликативной группы: {multiplicative_group_order}")
    print(f"Количество элементов: {field_order}")
    if irreducible_poly:
        print(f"Неприводимый многочлен: {print_polynomial(irreducible_poly)}")

def display_elements(elements):        #отображает элементы поля

    print(f"\n{'='*50}")
    print("Элементы поля (от старшей степени к младшей):")
    print(f"{'='*50}")
    for i, elem in enumerate(elements):
        poly_str = print_polynomial(elem)           #форматирование
        print(f"{i:2d}: {poly_str}")

def input_field_element(p, n):          #ввод элемента поля Галуа
    print(f"\nВведите коэффициенты элемента поля (многочлен степени < {n})")
    print(f"Пример для n=3: [1, 0, 1] соответствует x² + 1")
    
    while True:
        try:
            coeffs = list(map(int, input("Введите коэффициенты: ").split()))
            
            if len(coeffs) > n:
                print(f"Ошибка, многочлен должен иметь не более {n} коэффициентов")
                continue
                
            if any(c < 0 or c >= p for c in coeffs):
                print(f"Ошибка, все коэффициенты должны быть в диапазоне [0, {p-1}]")
                continue
            while len(coeffs) < n:          #дополняем нулями до длины n (в конце, для младших степеней)
                coeffs.append(0)
        
            coeffs = coeffs[::-1]
            return coeffs                           #преобразуем к внутреннему формату от младшего к старшему
            
        except ValueError:
            print("Ошибка, введите целые числа, разделенные пробелами")


def add_polynomials(a, b, p):       #сложение двух многочленов в поле Галуа
    n = max(len(a), len(b))                     #макс степень
    result = [0] * n            #массив для результата
    for i in range(n):                      #проход по всем позициям от мл к ст
        a_val = a[i] if i < len(a) else 0       
        b_val = b[i] if i < len(b) else 0
        result[i] = (a_val + b_val) % p     #складываем и берем по mod p
    return result

def subtract_polynomials(a, b, p):          #вычитание многочленов в поле для Евкл
    n = max(len(a), len(b))
    result = [0] * n
    for i in range(n):
        a_val = a[i] if i < len(a) else 0       #то же самое
        b_val = b[i] if i < len(b) else 0
        result[i] = (a_val - b_val) % p
    return result

def multiply_polynomials_simple(a, b, p):       #умножение двух многочленов без приведения для алг. Евклида
    result = [0] * (len(a) + len(b) - 1)
    for i in range(len(a)):          #проходим по всем коэффициентам первого многочлена (a)
        for j in range(len(b)):
            result[i + j] = (result[i + j] + a[i] * b[j]) % p   #умножаем коэффициент a[i] (при x^i) на коэффициент b[j] (при x^j)
    return result                                               #добавл к сущ и берем по mod p

def multiply_polynomials(a, b, p, irreducible_poly):            #умножение двух многочленов в поле Галуа

    n = len(a)
    product = multiply_polynomials_simple(a, b, p)                  #умножаем многочлены обычным способом
    remainder = poly_mod(product, irreducible_poly, p)                          # Приводим по модулю неприводимого многочлена
    
    while len(remainder) < n:                                           #дополняем результат до длины n
        remainder.append(0)
    
    return remainder[:n]



def poly_division(a, b, p):         #деление многочленов с возвратом частного и остатка
    a = a[:]                    #копии
    b = b[:]
    while len(a) > 1 and a[-1] == 0:
        a.pop()
    while len(b) > 1 and b[-1] == 0:
        b.pop()
    deg_a = len(a) - 1      #степень делимого
    deg_b = len(b) - 1      #степень делителя
    
    if deg_b == -1:
        raise ValueError("деление на нулевой многочлен")
    
    if deg_a < deg_b:
        return [0], a  #частное = 0, остаток = a
    lead_coeff = b[deg_b]
    inv_lead = pow(lead_coeff, p-2, p) if lead_coeff != 0 else 0            #обратный к старшему коэффициенту b
    
    q = [0] * (deg_a - deg_b + 1)       #инициализируем частное нулями
    
    for i in range(deg_a - deg_b, -1, -1):      #деление от старших степеней к младшим
        if a[i + deg_b] != 0:               #нужно ли обнулять текущий коэффициент в делимом
            factor = (a[i + deg_b] * inv_lead) % p #(текущий коэффициент делимого) * (обратный к старшему коэффициенту делителя)
            q[i] = factor       
            
            for j in range(deg_b + 1):                          #Вычитаем из делимого factor * b(x), сдвинутое на i позиций
                                                                #j - индекс в делителе b (от 0 до deg_b)
                a[i + j] = (a[i + j] - factor * b[j]) % p
    
    # Удаляем ведущие нули из остатка
    while len(a) > 1 and a[-1] == 0:    #пока длина >1 b старший коэф =0
        a.pop()                     #удаляем послед элемент
    
    while len(q) > 1 and q[-1] == 0:
        q.pop()                             #удаляем ведущие нули из частного
    
    return q, a



def extended_euclidean(a, b, p):            #расширенный алгоритм Евклида
    x0, x1 = [1], [0]  #коэффициенты для a          #инициализация
    y0, y1 = [0], [1]  #коэффициенты для b
    while len(b) > 1 or b[0] != 0:                  #нормализуем многочлены удаляем ведущие нули

        q, r = poly_division(a, b, p)               #вычисляем частное и остаток от деления a на b
        
        q_x1 = multiply_polynomials_simple(q, x1, p)        #обновляем коэффициенты                        
        q_y1 = multiply_polynomials_simple(q, y1, p)
                                                                    #цикл продолжается, пока b не станет нулевым многочленом
        x_next = subtract_polynomials(x0, q_x1, p)
        y_next = subtract_polynomials(y0, q_y1, p)              #новые коэффициенты
        
        a, b = b, r                 #обновляем переменные
        x0, x1 = x1, x_next
        y0, y1 = y1, y_next         #сдвигаем коэффициенты
    
    if len(a) > 0 and a[-1] != 0:                   #нормализуем НОД (делаем старший коэффициент равным 1)
        inv_lead = pow(a[-1], p-2, p)                                   #находим обратный к старшему коэффициенту НОД
        a = [(coeff * inv_lead) % p for coeff in a]
        x0 = [(coeff * inv_lead) % p for coeff in x0]            #умножаем НОД и коэффициенты на обратный элемент
        y0 = [(coeff * inv_lead) % p for coeff in y0]
    
    return a, x0, y0



def polynomial_inverse_euclidean(a, p, n, irreducible_poly):            #обратный многочлен с помощью расширенного алгоритма Евклида
    if all(coeff == 0 for coeff in a):
        return None                             #у нуля нет обратного
    
    gcd, u, v = extended_euclidean(a, irreducible_poly, p)          #используем расширенный алгоритм Евклида
    
    if len(gcd) != 1 or gcd[0] != 1:                #проверка что НОД равен 1
        return None 
    
    u = [coeff % p for coeff in u]          #приводим u по модулю p
    if len(u) > n:                          #приводим к длине n (отбрасываем старшие степени)
        u = poly_mod(u, irreducible_poly, p)                                #берем остаток от деления на неприводимый многочлен
    
    # Дополняем нулями до длины n
    while len(u) < n:
        u.append(0)
    
    return u                #возвращаем обратный элемент

def polynomial_operations(p, n, irreducible_poly, elements):
    print(f"\n{'='*50}")
    print("ОПЕРАЦИИ С МНОГОЧЛЕНАМИ В ПОЛЕ ГАЛУА")
    print(f"{'='*50}")
    
    print("\nПервый многочлен:")
    poly1 = input_field_element(p, n)
    print(f"Первый многочлен: {print_polynomial(poly1)}")
    
    print("\nВторой многочлен:")
    poly2 = input_field_element(p, n)
    print(f"Второй многочлен: {print_polynomial(poly2)}")
    
    print("\nВыберите операцию:")
    print("1. Сложение")
    print("2. Умножение")
    print("3. Нахождение обратного элемента (для первого многочлена)")
    
    choice = input("Введите операцию (1, 2 или 3): ")
    
    if choice == "1":
        result = add_polynomials(poly1, poly2, p)
        print(f"\nРезультат сложения: {print_polynomial(result)}")
    elif choice == "2":
        result = multiply_polynomials(poly1, poly2, p, irreducible_poly)
        print(f"\nРезультат умножения: {print_polynomial(result)}")
    elif choice == "3":
        if all(coeff == 0 for coeff in poly1):              #проверка на нулевой элемент
            print("Нулевой элемент не имеет обратного")
        else:
            inverse = polynomial_inverse_euclidean(poly1, p, n, irreducible_poly)
            if inverse:
                check = multiply_polynomials(poly1, inverse, p, irreducible_poly)                       #проверяем, что действительно получили обратный
                is_correct = (check == [1] + [0] * (n - 1))
                
                print(f"\nОбратный элемент к {print_polynomial(poly1)}:")
                print(f"Обратный: {print_polynomial(inverse)}")
                print(f"Проверка: {print_polynomial(poly1)} * {print_polynomial(inverse)} = {print_polynomial(check)}")
                if is_correct:
                    print("Проверка пройдена")
                else:
                    print("Внимание, проверка не пройдена!")
            else:
                print("Не удалось найти обратный элемент")
    else:
        print("Неверный выбор операции")



def euler_phi(n):       #функция Эйлера

    result = n
    p = 2           #перебираем все возможные едлители начиная с 2
    while p * p <= n:       #делители квадратного корня из n
        if n % p == 0:
            while n % p == 0:           #делим n на p пока делится
                n //= p
            result -= result // p        #обновляем
        p += 1
    if n > 1:                   #оставшийся просто делитель
        result -= result // n
    return result


def factorize(n):               #разложение числа на простые множители для проверки образуюих элементов
    factors = []
    d = 2           #начинаем с наим простого делителя 2
    while d * d <= n:       #проверяем делители до квадратного корня из n
                        #если n делится на d без остатка, значит d - простой делитель
        if n % d == 0:      
            factors.append(d)       #добавляем d в список простых делителей
            while n % d == 0:               #делим пока делится чтобы убрать все степени d
                n //= d
        d += 1                  #переходим к след делителю
    if n > 1:   
        factors.append(n)       #добавляем в список
    return factors



def power_polynomial(poly, exponent, p, irreducible_poly):          #быстрое возведение многочлена в степень в поле Галуа для проверки образующих
    n = len(poly)
    result = [1] + [0] * (n - 1)  #инициализируем результат как единичный элемент поля

    base = poly.copy()          #создаем копию основания для возведения в степень
    
    while exponent > 0:
        if exponent % 2 == 1:               #если текущий бит экспоненты = 1
            result = multiply_polynomials(result, base, p, irreducible_poly)                #умножаем результат на текущее основание
        base = multiply_polynomials(base, base, p, irreducible_poly)            #основание в квадрат
        exponent //= 2          #сдвиг вправо
    
    return result


def is_primitive_element(element, p, n, irreducible_poly):      #проверяет, является ли элемент образующим мультипликативной группы
    m = p ** n - 1          #порядок мультипликативной группы
    
    if element == [1] + [0] * (n - 1):          #проверяем, что элемент не единичный
        return False
    
    prime_factors = factorize(m)                #находим простые делители m
                                                    #проверяем необходимое и достаточное условие для образующего элемента
                                                    #элемент g является образующим когда g^(m/q) ≠ 1 для каждого простого делителя q числа m
    for q in prime_factors:
        exponent = m // q           #вычисл степень
        power_result = power_polynomial(element, exponent, p, irreducible_poly)
        
        if power_result == [1] + [0] * (n - 1):         #если результат равен 1, то элемент не образующий
            return False
    
    return True



def find_primitive_elements(p, n, irreducible_poly, elements):              #находит все образующие элементы поля
    primitive_elements = []                 #список для хранения найденных образующих элем
    total = len(elements)       #общ кол-во элем в поле
    
    for i, element in enumerate(elements):              #проходим по всем элементам поля
                                                            #i - индекс элемента, element - сам элемент (список коэффициентов)
        if i == 0:                          #нулевой элемент [0, 0, ..., 0] никогда не может быть образующим
            continue
        
        if total > 100 and i % 50 == 0:
            print(f"  Проверено {i}/{total} элементов")                      #прогресс для больших полей
        
        if is_primitive_element(element, p, n, irreducible_poly):               #проверка является ли образующим
            primitive_elements.append(element)      #если да, то добавл в лист
    
    return primitive_elements       #ретюрн всех образ элеменентов




def build_log_table(primitive, p, n, irreducible_poly):             #строит таблицу для разложения элементов по степеням образующего)
    m = p ** n - 1                  #порядок мультипликативной группы
    log_table = {}
    antilog_table = {}          
    
    current_power = [1] + [0] * (n - 1)      #α^0 = 1
    
    for exp in range(m):                    #вычисляем все степени образующего элемента
        element_tuple = tuple(current_power)            #сохраняем текущую степень в таблице, в картеж
        log_table[element_tuple] = exp
        antilog_table[exp] = element_tuple
        
                        #умножаем текущий элемент на образующий, чтобы получить следующую степень
        if exp < m - 1:  #не вычисляем α^m, так как оно равно α^0
            current_power = multiply_polynomials(current_power, primitive, p, irreducible_poly)
    element_tuple = tuple([1] + [0] * (n - 1))          #добавляем α^m = 1
    log_table[element_tuple] = 0            #α^m соответствует логарифму 0
    antilog_table[m] = element_tuple            #степень m соответствует элементу 1
    
    return log_table, antilog_table


def display_primitive_info(p, n, irreducible_poly, elements):
    m = p ** n - 1
    expected_count = euler_phi(m)
    
    print(f"\n{'='*60}")
    print("ОБРАЗУЮЩИЕ ЭЛЕМЕНТЫ МУЛЬТИПЛИКАТИВНОЙ ГРУППЫ")
    print(f"{'='*60}")
    print(f"Порядок мультипликативной группы: {m}")
    print(f"Разложение на простые множители: {m} = {' * '.join(map(str, factorize(m)))}")
    print(f"Ожидаемое количество образующих (φ({m}) = {expected_count})")
    
    primitive_elements = find_primitive_elements(p, n, irreducible_poly, elements)
    
    print(f"Найдено образующих элементов: {len(primitive_elements)}")
    
    if len(primitive_elements) != expected_count:
        print(f"ВНИМАНИЕ: Найдено {len(primitive_elements)} образующих, но ожидалось {expected_count}!")    
    if primitive_elements:
        if len(primitive_elements) > 20:                    #выбор, показывать ли все образующие
            print(f"\nНайдено {len(primitive_elements)} образующих элементов.")
            show_all = input("Показать все? (да/нет): ").strip().lower()
            if show_all in ['да', 'д', 'yes', 'y']:
                print(f"\nВсе образующие элементы:")
                for i, elem in enumerate(primitive_elements):
                    num = element_to_number(elem, p, n)
                    print(f"{i+1:3d}: {print_polynomial(elem)}")
        else:
            print(f"\nВсе образующие элементы:")
            for i, elem in enumerate(primitive_elements):
                num = element_to_number(elem, p, n)
                print(f"{i+1:3d}: {print_polynomial(elem)}")
        
        print(f"\nВыбери образующий элемент (1-{len(primitive_elements)}):")
        print("Или введи 0 для использования первого образующего")
        try:
            choice = int(input("Ваш выбор: ")) - 1
            if choice < 0 or choice >= len(primitive_elements):
                print("Используется первый образующий элемент.")
                choice = 0
        except ValueError:
            print("Неверный ввод. Используется первый образующий элемент.")
            choice = 0
        
        primitive = primitive_elements[choice]
        primitive_num = element_to_number(primitive, p, n)
        print(f"\nВыбран образующий элемент: a = {print_polynomial(primitive)} (число: {primitive_num})")
        
        print(f"\nПроверка, что a действительно образующий:")
        check_passed = True                             #проверка, что элемент действительно образующий
        for q in factorize(m):
            exponent = m // q
            power_result = power_polynomial(primitive, exponent, p, irreducible_poly)
            power_num = element_to_number(power_result, p, n)
            is_one = (power_result == [1] + [0] * (n - 1))
            print(f"  a^{m}/{q} = a^{exponent} = {print_polynomial(power_result)} (число: {power_num}) {'= 1' if is_one else '!= 1'}")
            if is_one:
                check_passed = False
        
        if check_passed:
            print("  Элемент является образующим")
        else:
            print("  Элемент НЕ является образующим")
    
        log_table, antilog_table = build_log_table(primitive, p, n, irreducible_poly)
        print(f"\nТаблица степеней образующего элемента a:")
        print("Степень   | Элемент поля |                Число")
        print("-" * 50)
        
        for exp in range(0, min(11, m + 1)):
            elem_list = list(antilog_table.get(exp % m, [1] + [0] * (n - 1)))                   #показываем первые 10 и последние 5 степеней
            num = element_to_number(elem_list, p, n)
            print(f"a^{exp:<6} | {print_polynomial(elem_list):30} | {num:3d}")
        
        if m > 10:
            print("...")
            for exp in range(m - 4, m + 1):
                elem_list = list(antilog_table.get(exp % m, [1] + [0] * (n - 1)))
                num = element_to_number(elem_list, p, n)
                print(f"a^{exp:<6} | {print_polynomial(elem_list):30} | {num:3d}")
        
        while True:
            print(f"\n{'='*60}")
            print("Разложение элемента по степеням образующего")
            print(f"{'='*60}")
            
            print("Введите элемент поля для разложения:")
            element = input_field_element(p, n)
            
            if all(coeff == 0 for coeff in element):                    #проверка на нулевой элемент
                print("Это нулевой элемент. Он не имеет разложения по степеням образующего.")
            else:
                if element == [1] + [0] * (n - 1):
                    print(f"Элемент {print_polynomial(element)} = a^0")     #если единичный
                else:
                    element_tuple = tuple(element)
                    if element_tuple in log_table:
                        exp = log_table[element_tuple]
                        print(f"Элемент {print_polynomial(element)} = a^{exp}")
                        
                        check = power_polynomial(primitive, exp, p, irreducible_poly)
                        if check == element:
                            print(f"  Проверка: a^{exp} = {print_polynomial(check)}")
                        else:
                            print(f"  Ошибка: a^{exp} = {print_polynomial(check)}")
                    else:
                        print("Ошибка, элемент не найден среди элементов поля")
            print("\nХотите ли вы разложить еще один элемент? (да/нет)")
            choice = input("Ваш выбор: ").strip().lower()
            if choice not in ['да', 'д', 'yes', 'y']:
                break
        
        return primitive, log_table
    else:
        print("Не найдено образующих элементов!")
        return None, None

def find_closest_field_size(alphabet_size):                 #находит ближайшее сверху поле Галуа 2^n
    n = 1
    while (2 ** n) < alphabet_size:
        n += 1
    return 2, n, 2 ** n





def create_extended_alphabet(unique_chars, field_size):         #cоздает расширенный алфавит для поля заданного размера

    base_chars = sorted(list(unique_chars))         #сортируем уникальные символы для упорядочивания
    
    if field_size <= len(base_chars):           #если поле меньше или равно количеству уникальных символов в
        return base_chars[:field_size]          
    alphabet = base_chars[:]                #добавляем дополнительные символы
    extra_chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"          #символы для дополнения
    
    i = 0
    while len(alphabet) < field_size:
        if i < len(extra_chars):                #добавляем дополнительные символы, пока не достигнем нужного размера
            char = extra_chars[i]
            if char not in alphabet:                #убедимся, что символ не повторяется
                alphabet.append(char)
        else:                                       
            char = f"#{len(alphabet)}"          #если закончились символы, добавляем номер
            alphabet.append(char)
        i += 1
    
    return alphabet

def text_to_numbers(text, alphabet):            #преобразует текст в числовую последовательность по алфавиту
    numbers = []
    for char in text:               #проходим по каждому символу открытого текста
        if char in alphabet:
            numbers.append(alphabet.index(char))
        else:
            numbers.append(0)                           # если символ не найден, заменяем на первый символ алфавита
    return numbers

def numbers_to_text(numbers, alphabet):         #преобразует числовую последовательность обратно в текст
    text_chars = []
    for num in numbers:
        if 0 <= num < len(alphabet):
            text_chars.append(alphabet[num])
        else:
            text_chars.append('?')
    return ''.join(text_chars)

def numbers_to_binary_blocks(numbers, n):     #преобразует числа в двоичные блоки длины n
    binary_blocks = []
    for num in numbers:                                 #проход по всем числам в списке
        binary = bin(num)[2:].zfill(n)           #добавляем нули вначало
        binary_blocks.append(binary)                                     #добавляем полученную двоичную строку в список
    return binary_blocks

def binary_blocks_to_numbers(binary_blocks, n):     #преобразует двоичные блоки обратно в числа
    numbers = []
    for block in binary_blocks:
        if len(block) == n:
            numbers.append(int(block, 2))
    return numbers

def number_to_element(num, p, n):                       #преобразует число в элемент поля (многочлен)
    element = []        #пустой лист для коэффициентов
    temp = num              #временая переменная
    for _ in range(n):                  #повтор n раз для каждой степени
        element.append(temp % p)                #коэфф при текущей (младшей) степени
        temp //= p      #целочисл деление на p
    return element              #на выходе список коэффициентов 

def element_to_number(element, p, n):    #преобразует элемент поля в число
    
    num = 0                 #поначалу результат 0
    for i, coeff in enumerate(element):         #возвращает пары индекс значение
        num += coeff * (p ** i)
    return num          #на выходе полученное число 




def affine_encrypt_text_polynomials(plaintext, alpha_poly, beta_poly, p, n, irreducible_poly, alphabet):            #ШИФРОВАНИЕ
    print(f"Открытый текст: '{plaintext}'")
    
    numbers = text_to_numbers(plaintext, alphabet)           #преобразуем текст в числовую последовательность
    print(f"Числовая последовательность: {numbers}")
    
    binary_blocks = numbers_to_binary_blocks(numbers, n)        #преобразуем числа в двоичные блоки
    print(f"Двоичные блоки (n={n}): {binary_blocks}")
    
    field_numbers = []                                          #преобразуем двоичные блоки в числа (для поля Галуа)
    for binary in binary_blocks:
        field_num = int(binary, 2)
        field_numbers.append(field_num)
    
    print(f"Числа в поле (0-{2**n-1}): {field_numbers}")
    
    element_polynomials = []                                    #преобразуем числа в элементы поля (многочлены)
    for num in field_numbers:
        element_poly = number_to_element(num, p, n)
        element_polynomials.append(element_poly)
        
    encrypted_polynomials = []                                                          #применяем формулу шифрования к каждому многочлену
    
    for i, x_poly in enumerate(element_polynomials):            #enumerate возвращает пары индекс значение для списка

        product = multiply_polynomials(alpha_poly, x_poly, p, irreducible_poly)                 #умножение: α * x_i
        
        y_poly = add_polynomials(product, beta_poly, p)                                             #сложение: α * x_i + β
        encrypted_polynomials.append(y_poly)
        
        x_num = element_to_number(x_poly, p, n)
        y_num = element_to_number(y_poly, p, n)
    
    encrypted_numbers = [element_to_number(poly, p, n) for poly in encrypted_polynomials]           #преобразуем зашифрованные многочлены в числа
    
    encrypted_binary_blocks = []                                                        #преобразуем числа обратно в двоичные блоки
    for num in encrypted_numbers:
        binary = bin(num)[2:].zfill(n)      #заполняем блоки нулями вначале
        encrypted_binary_blocks.append(binary)
        
    encrypted_alphabet_numbers = []  #преобразуем двоичные блоки в числа для алфавита
    for binary in encrypted_binary_blocks:
        num = int(binary, 2)
        encrypted_alphabet_numbers.append(num)      #двоичные блоки в индексы алфавита
    
    shifrtext = numbers_to_text(encrypted_alphabet_numbers, alphabet)        #преобразуем индексы в буквы 
        
    return shifrtext, encrypted_numbers, encrypted_binary_blocks








def affine_decrypt_text_polynomials(shifrtext, alpha_poly, beta_poly, p, n, irreducible_poly, alphabet):        #РАСШИФРОВАНИЕ
    print(f"Шифртекст: '{shifrtext}'")
    
    alphabet_numbers = text_to_numbers(shifrtext, alphabet)                                         #преобразуем шифртекст в числовую последовательность по алфавиту
    print(f"Числовая последовательность (из алфавита): {alphabet_numbers}")
    
    binary_blocks = []                                                      #преобразуем числа в двоичные блоки
    for num in alphabet_numbers:
        binary = bin(num)[2:].zfill(n)
        binary_blocks.append(binary)
    
    print(f"Двоичные блоки (n={n}): {binary_blocks}")
    
                                                                        #преобразуем двоичные блоки в числа для поля
    field_numbers = []
    for binary in binary_blocks:
        field_num = int(binary, 2)
        field_numbers.append(field_num)
    
    print(f"Числа в поле (0-{2**n-1}): {field_numbers}")
    
    element_polynomials = []                                                #преобразуем числа в многочлены
    for num in field_numbers:
        element_poly = number_to_element(num, p, n)
        element_polynomials.append(element_poly)
    
    print(f"\nПоиск обратного элемента к а с помощью расширенного алгоритма Евклида")           #находим обратный элемент к α с помощью расширенного алгоритма Евклида
    alpha_inv_poly = polynomial_inverse_euclidean(alpha_poly, p, n, irreducible_poly)
    
    if alpha_inv_poly is None:
        print("Ошибка: не удалось найти обратный элемент к а")
        return None
    
    alpha_num = element_to_number(alpha_poly, p, n)
    alpha_inv_num = element_to_number(alpha_inv_poly, p, n)
    
    print(f"a = {print_polynomial(alpha_poly)}")
    print(f"a⁻¹ = {print_polynomial(alpha_inv_poly)}")

    check_product = multiply_polynomials(alpha_poly, alpha_inv_poly, p, irreducible_poly)           #проверяем, что а * а⁻¹ = 1
    check_num = element_to_number(check_product, p, n)
    print(f"Проверка: a * a⁻¹ = {print_polynomial(check_product)}")
    
    decrypted_polynomials = []                                              #применяем формулу расшифрования к каждому многочлену
    
    for i, y_poly in enumerate(element_polynomials):        
        y_minus_beta = subtract_polynomials(y_poly, beta_poly, p)                   #вычитание: y_i - b
        
        x_poly = multiply_polynomials(y_minus_beta, alpha_inv_poly, p, irreducible_poly)                    #умножение: (y_i - b) * а⁻¹
        decrypted_polynomials.append(x_poly)    
        
        y_num = element_to_number(y_poly, p, n)
        x_num = element_to_number(x_poly, p, n)
    
    decrypted_numbers = [element_to_number(poly, p, n) for poly in decrypted_polynomials]               #преобразуем расшифрованные многочлены в числа
    
    decrypted_binary_blocks = []                                                                    #преобразуем числа обратно в двоичные блоки
    for num in decrypted_numbers:
        binary = bin(num)[2:].zfill(n)
        decrypted_binary_blocks.append(binary)
    
    decrypted_alphabet_numbers = []                                                                        #преобразуем двоичные блоки в числа для алфавита
    for binary in decrypted_binary_blocks:
        num = int(binary, 2)
        decrypted_alphabet_numbers.append(num)
    
    opentext = numbers_to_text(decrypted_alphabet_numbers, alphabet)                                               #преобразуем числа в текст
    
    original_alphabet = "абвгдежзийклмнопрстуфхцчшщъыьэюя"                                                              #убираем лишние символы, если они есть
    clean_text = ""                                                          #находим индекс первого символа, который не в оригинальном алфавите
    for char in opentext:                                      #проходим по расшифр тексту. и оставляем только символы из русского алфавита
        if char.lower() in original_alphabet:
            clean_text += char
        else:
            break    
    return clean_text



def affine_cipher_interface():
    print(f"\n{'='*60}")
    print("АФФИННЫЙ ШИФР НАД ПОЛЕМ ГАЛУА")
    print(f"{'='*60}")
    
    while True:
        print("\nВыберите действие:")
        print("1. Зашифрование текста")
        print("2. Расшифрование шифртекста")
        print("0. Вернуться в главное меню")
        
        choice = input("Ваш выбор: ").strip()
        
        if choice == "0":
            return
        
        elif choice == "1":
            print(f"\n{'='*60}")
            print("ЗАШИФРОВАНИЕ ТЕКСТА")
            print(f"{'='*60}")
            opentext = input("Введите текст на русском языке (без ё): ").strip()        #ввод открытого текста
            if not opentext:
                print("Текст не может быть пустым")
                continue
        
            unique_chars = set(opentext.lower())                           #определяем уникальные символы
            russian_chars = "абвгдежзийклмнопрстуфхцчшщъыьэюя"
            unique_chars = {char for char in unique_chars if char in russian_chars}                 #убираем символы, которых нет в русском алфавите
            alphabet_size = len(unique_chars)
            
            print(f"\nУникальных символов в тексте: {alphabet_size}")
            print(f"Уникальные символы: {''.join(sorted(unique_chars))}")
            
            p, n, field_size = find_closest_field_size(alphabet_size)                                           #выбираем поле Галуа
            print(f"\nВыбрано поле: F_{p}^{n} = F_{field_size}")
            print(f"Размер поля: {field_size} элементов")
            print(f"Степень расширения: n = {n}")
            
            alphabet = create_extended_alphabet(unique_chars, field_size)                       #создаем алфавит
            print(f"\nСоздан алфавит из {len(alphabet)} символов:")
            for i, char in enumerate(alphabet):
                print(f"{i:2d}: '{char}'", end="  ")
                if (i + 1) % 8 == 0:
                    print()
            
            print(f"\nГенерация неприводимого многочлена степени {n} над F_{p}...")                         #генерируем неприводимый многочлен
            irreducible_poly = generate_irreducible_polynomial(p, n)
            if not irreducible_poly:
                print("Не удалось сгенерировать неприводимый многочлен")
                continue
            
            print(f"\n{'='*50}")
            print(f"ВСЕ ЭЛЕМЕНТЫ ПОЛЯ F_{p}^{n}:")                                          #выводим все элементы поля
            print(f"{'='*50}")
            elements = generate_galois_field(p, n)
            for i, elem in enumerate(elements):
                poly_str = print_polynomial(elem)
                num = element_to_number(elem, p, n)
                print(f"{i:2d}         {poly_str}")
            

            print(f"\nВвод ключа k = (a, b):")
            print(f"a ∈ F_{field_size}^* (ненулевой элемент), b ∈ F_{field_size}")
            print(f"a и b задаются как многочлены степени < {n}")
            
            print(f"\nВведите a (ненулевой многочлен):")
            alpha_poly = input_field_element(p, n)
            
            while all(coeff == 0 for coeff in alpha_poly):                              #проверка, что а не нулевой
                print("Ошибка: a не должен быть нулевым многочленом")
                alpha_poly = input_field_element(p, n)
            
            print(f"\nВведите b (любой многочлен):")
            beta_poly = input_field_element(p, n)
            
            alpha_num = element_to_number(alpha_poly, p, n)                     #вывод введенных ключей
            beta_num = element_to_number(beta_poly, p, n)
            print(f"\nКлючи:")
            print(f"a = {print_polynomial(alpha_poly)} (число: {alpha_num})")
            print(f"b = {print_polynomial(beta_poly)} (число: {beta_num})")
            
            result = affine_encrypt_text_polynomials(                                               #шифрование
                opentext, alpha_poly, beta_poly, p, n, irreducible_poly, alphabet
            )
            
            if result:
                ciphertext, encrypted_numbers, encrypted_binary_blocks = result
                print(f"\n{'='*60}")
                print("РЕЗУЛЬТАТ ШИФРОВАНИЯ:")
                print(f"{'='*60}")
                print(f"Открытый текст: '{opentext}'")
                print(f"Поле: F_{p}^{n}")
                print(f"Неприводимый многочлен: {print_polynomial(irreducible_poly)}")
                print(f"Алфавит: {''.join(alphabet)}")
                print(f"Ключ a (многочлен): {print_polynomial(alpha_poly)}")
                print(f"Ключ b (многочлен): {print_polynomial(beta_poly)}")
                print(f"Шифртекст: '{ciphertext}'")
                print(f"Зашифрованные двоичные блоки: {encrypted_binary_blocks}")
                print(f"{'='*60}")
        
        elif choice == "2":
            print(f"\n{'='*60}")
            print("РАСШИФРОВАНИЕ ТЕКСТА")
            print(f"{'='*60}")
            
            ciphertext = input("Введите шифртекст: ").strip()
            if not ciphertext:
                print("Шифртекст не может быть пустым")
                continue
            
            print("\nДля расшифрования необходимо знать параметры поля:")                               #определение поля Галуа
            try:
                p = int(input("Введите p (основание поля, обычно 2): ").strip())
                n = int(input("Введите n (степень расширения): ").strip())
                field_size = p ** n
                
                if p != 2:
                    print("Для аффинного шифра рекомендуется использовать p = 2")
                    continue
                
            except ValueError:
                print("Ошибка: введите целые числа")
                continue
            
            print(f"\nВведите алфавит из {field_size} символов:")                       #ввод алфавита
            alphabet_input = input("Алфавит: ").strip()
            
            if len(alphabet_input) != field_size:
                print(f"Ошибка: алфавит должен содержать ровно {field_size} символов")
                continue
            
            alphabet = list(alphabet_input)
            
            print(f"\nВведите неприводимый многочлен степени {n} над F_{p}")                                #ввод неприводимого многочлена
            print(f"Пример для степени 2: [1, 0, 1] соответствует x² + 1")
            
            try:
                coeffs = list(map(int, input("Введите коэффициенты: ").split()))
                
                if len(coeffs) != n + 1:
                    print(f"Ошибка: многочлен должен иметь {n+1} коэффициентов")
                    continue
                    
                if coeffs[0] != 1:
                    print("Ошибка: старший коэффициент должен быть равен 1")
                    continue
                    
                if any(c < 0 or c >= p for c in coeffs):
                    print(f"Ошибка: все коэффициенты должны быть в диапазоне [0, {p-1}]")
                    continue
                
                irreducible_poly = coeffs[::-1]                                                     #преобразуем к внутреннему формату от младшего к старшему
                    
            except ValueError:
                print("Ошибка: введите целые числа, разделенные пробелами")
                continue
            
            print(f"\nВвод ключа k = (a, b):")                                           #ввод ключа как многочленов
            print(f"a ∈ F_{field_size}^* (ненулевой элемент), b ∈ F_{field_size}")
            print(f"a и b задаются как многочлены степени < {n}")
            
            print(f"\nВведите a (ненулевой многочлен):")
            alpha_poly = input_field_element(p, n)
            
            while all(coeff == 0 for coeff in alpha_poly):                              #проверяем, что a не нулевой
                print("Ошибка: a не должен быть нулевым многочленом")
                alpha_poly = input_field_element(p, n)
            
            print(f"\nВведите b (любой многочлен):")
            beta_poly = input_field_element(p, n)
            
            print(f"\nПоиск обратного элемента")                            #находим обратный элемент к а с помощью расширенного алгоритма Евклида
            alpha_inv_poly = polynomial_inverse_euclidean(alpha_poly, p, n, irreducible_poly)
            
            if alpha_inv_poly is None:
                print("Ошибка: не удалось найти обратный элемент к a")
                continue
            
            alpha_num = element_to_number(alpha_poly, p, n)
            beta_num = element_to_number(beta_poly, p, n)
            alpha_inv_num = element_to_number(alpha_inv_poly, p, n)
            
            print(f"\nКлючи:")
            print(f"a = {print_polynomial(alpha_poly)}")
            print(f"b = {print_polynomial(beta_poly)}")
            print(f"a⁻¹ = {print_polynomial(alpha_inv_poly)}")
            
            check_product = multiply_polynomials(alpha_poly, alpha_inv_poly, p, irreducible_poly)                                   #проверяем, что a * a⁻¹ = 1
            check_num = element_to_number(check_product, p, n)
            print(f"Проверка: a * a⁻¹ = {print_polynomial(check_product)}")
            
            opentext = affine_decrypt_text_polynomials(
                ciphertext, alpha_poly, beta_poly, p, n, irreducible_poly, alphabet                             #расшифрование
            )
            
            if opentext:
                print(f"\n{'='*60}")
                print("РЕЗУЛЬТАТ РАСШИФРОВАНИЯ:")
                print(f"{'='*60}")
                print(f"Шифртекст: '{ciphertext}'")
                print(f"Поле: F_{p}^{n}")
                print(f"Неприводимый многочлен: {print_polynomial(irreducible_poly)}")
                print(f"Алфавит: {''.join(alphabet)}")
                print(f"Ключ a (многочлен): {print_polynomial(alpha_poly)}")
                print(f"Ключ b (многочлен): {print_polynomial(beta_poly)}")
                print(f"Обратный элемент a⁻¹: {print_polynomial(alpha_inv_poly)}")              #(число: {alpha_inv_num})
                print(f"Расшифрованный текст: '{opentext}'")
                print(f"{'='*60}")
        
        else:
            print("Неверный выбор. Попробуйте снова.")






def main():
    while True:
        print("\nГЛАВНОЕ МЕНЮ:")
        print("1. Инструмент для исследования поля Галуа")
        print("2. Аффинный шифр с полем Галуа")
        print("0. Выход")
        
        main_choice = input("Выберите действие: ").strip()
        
        if main_choice == "0":
            print("Выход из программы.")
            break
        
        elif main_choice == "1":
            print("\nИНСТРУМЕНТ ДЛЯ ИССЛЕДОВАНИЯ ПОЛЯ ГАЛУА")
            p = int(input("Введите p (простое число): "))
            n = int(input("Введите n (степень расширения): "))
            
            field_order = p ** n
            multiplicative_group_order = field_order - 1
            
            print(f"\nВыберите способ задания неприводимого многочлена степени {n} над F_{p}:")
            print("1. Задать неприводимый многочлен самостоятельно")
            print("2. Сгенерировать неприводимый многочлен")
            
            choice_poly = input("Выберите действие (1 или 2): ")
            
            irreducible_poly = None
            if choice_poly == "1":
                irreducible_poly = input_polynomial(p, n)
            elif choice_poly == "2":
                irreducible_poly = generate_irreducible_polynomial(p, n)
            else:
                print("Неверный выбор, используется генерация по умолчанию")
                irreducible_poly = generate_irreducible_polynomial(p, n)
            
            if irreducible_poly is None:
                print("Не удалось получить неприводимый многочлен. Возврат в главное меню.")
                continue
            
            elements = generate_galois_field(p, n)
            
            display_field_info(p, n, field_order, multiplicative_group_order, irreducible_poly)
            
            while True:
                print("\nДоступные действия:")
                print("1. Показать элементы поля")
                print("2. Показать неприводимый многочлен")
                print("3. Операции с многочленами")
                print("4. Найти образующие элементы и разложить элемент по степени образующего")
                
                choice = input("Выберите действие: ")
                
                if choice == "1":
                    display_elements(elements)
                elif choice == "2":
                    if irreducible_poly:
                        print(f"\nНеприводимый многочлен: {print_polynomial(irreducible_poly)}")
                    else:
                        print("Неприводимый многочлен не задан")
                elif choice == "3":
                    polynomial_operations(p, n, irreducible_poly, elements)
                elif choice == "4":
                    display_primitive_info(p, n, irreducible_poly, elements)
                elif choice == "0":
                    break
                else:
                    print("Неверный выбор. Попробуйте снова.")
        
        elif main_choice == "2":                            #аффинный шифр над полем галуа
            affine_cipher_interface()
        
        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main()