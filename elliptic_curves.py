import random
import math
from typing import List, Tuple, Optional, Dict
from datetime import datetime

class EllipticCurve:    
    def __init__(self, a: int, b: int, p: int):

        self.a = a % p
        self.b = b % p      #инициализация параметров кривой
        self.p = p
        self.O = (None, None)  #бесконечно удаленная точка
        
        if p <= 3:
            raise ValueError(f"p = {p} должен быть > 3")
        
        if not self.test_ferma(p, 20):
            raise ValueError(f"p = {p} не является простым (по тесту Ферма)")                   #проверка простоты p тестом Ферма
    
        a3 = self._mod_pow(a, 3, p)
        b2 = self._mod_pow(b, 2, p)                     #проверка условия на дискриминант -4a^3 - 27b^2 != 0 (mod p)
        disc = (-4 * a3 - 27 * b2) % p
        if disc == 0:
            raise ValueError(f"Дискриминант равен 0 по модулю {p}, кривая сингулярна и поэтому не подходит")
        
        self._all_points_cache = None               #кэш для повторных точек и порядка
        self._group_order = None
 
        
    def test_ferma(self, n: int, t: int) -> bool:
        if n <= 1:              # 1 и меньше не простые
            return False
        if n <= 3:              # 2 и 3 простые
            return True
        if n % 2 == 0:           #четн больше 2 составн
            return False
        
        for _ in range(t):              #повтор t раз 
            a = random.randint(2, n - 1)        #рандомное а
            r = self._mod_pow(a, n - 1, n)
            if r != 1:      #если не равно 1 то составное
                return False
        return True
  
    
    def _mod_pow(self, a: int, k: int, n: int) -> int:        #быстрое возведение в степень по модулю
        if k == 0:
            return 1 % n            #любое число в степени 0 равно 1 по мод n
        
        k_bits = []                         #бинарное k
        temp_k = k
        while temp_k > 0:
            k_bits.append(temp_k & 1)       #выдел младший бит 
            temp_k >>= 1                            #сдвиг вправо
        
        b = 1
        
        A = a % n           #a по модулю n 
        
        if k_bits[0] == 1:                  #если =1 то *а
            b = a % n
        
        for i in range(1, len(k_bits)):  #остальные биты
            A = (A * A) % n                         #квадрат предыдущ знач
            
            if k_bits[i] == 1:
                b = (A * b) % n     #умнож результат на текущий квадрат
        
        return b            #на выходе а^k mod n
    
    def _extended_gcd(self, a: int, b: int) -> Tuple[int, int, int]:
        if a < b:
            a, b = b, a     #меняем местами
        
        x2, x1 = 1, 0       #инициализация
        y2, y1 = 0, 1
        
        while b > 0:
            q = a // b
            r = a - q * b       #остаток от дел
            x = x2 - q * x1         #обновл коэфф
            y = y2 - q * y1
            
            a, b = b, r         #след итерация
            x2, x1 = x1, x                      #сдвиг коэффициентов
            y2, y1 = y1, y
        
        return a, x2, y2
    
    def _mod_inv(self, a: int) -> int:              #обратный элемент по мод p
        a_mod = a % self.p          #а по мод р
        if a_mod == 0:
            raise ValueError(f"Обратного элемента не существует для 0 mod {self.p}")
        
        d, x, y = self._extended_gcd(self.p, a_mod)         #на вход алгоритм евклида
        
        if d != 1:                          #если НОД(p, a) != 1, обратного не сущ
            raise ValueError(f"Обратного элемента не существует для a={a} mod p={self.p}")
        return y % self.p
  
    
    def _is_quadratic_residue(self, a: int) -> bool:            #проверка на кваадратичный вычет по mod p, есть ли корень
        if a % self.p == 0:
            return True                                     #критерий Эйлера: a^((p-1)/2) ≡ 1 (mod p) для квадратичного вычета
        return self._mod_pow(a, (self.p - 1) // 2, self.p) == 1         #квадратичный вычет это числ, имеющее квадратный корень по модулю p
 
    
    def _sqrt_mod(self, a: int) -> Optional[int]:       #извлечение квадратного корня по модулю простого p
        a_mod = a % self.p
        if a_mod == 0:          #если корень равен 0
            return 0
        
        if not self._is_quadratic_residue(a_mod):               #проверка, является ли a квадратичным вычетом
            return None
        if self.p % 4 == 3:
            return self._mod_pow(a_mod, (self.p + 1) // 4, self.p)
        
        for y in range(1, self.p):
            if (y * y) % self.p == a_mod:       #перебор в общем случае
                return y       
        return None
 
 
    
    def is_on_curve(self, point: Tuple[int, int]) -> bool:          #проверка на принадлежность точки кривой
        if point == self.O:     #бесконеч удал всегда на кривой
            return True
        
        x, y = point        #координаты точки
        left = (y * y) % self.p     #левая часть уравн
        right = (x*x*x + self.a*x + self.b) % self.p        #правая
        return left == right
    
    def add_points(self, P: Tuple[int, int], Q: Tuple[int, int]) -> Tuple[int, int]:            #операция сложение
        if P == self.O:
            return Q                #случай 1. P = O
        
        if Q == self.O:                     #случай 2. Q = O
            return P
        
        x1, y1 = P
        x2, y2 = Q
        
        if x1 == x2 and (y1 + y2) % self.p == 0:                #случай 3. P и Q - взаимно обратные (P = -Q)
            return self.O           #бесконеч удал
        
        if P == Q and (y1 % self.p) == 0:
            return self.O
        
        if P == Q:                              #касательная, когда P=Q, 
            numerator = (3 * x1 * x1 + self.a) % self.p    
            denominator = (2 * y1) % self.p                
        else:
            numerator = (y2 - y1) % self.p          #числитель при P!=Q, когда секущая
            denominator = (x2 - x1) % self.p         #знаменатель. наклон прямой через 2 точки
        
        s = (numerator * self._mod_inv(denominator)) % self.p       #деление = умнож на обратный
        
        x3 = (s * s - x1 - x2) % self.p             #коорд результата 
        y3 = (s * (x1 - x3) - y1) % self.p
        
        return (x3, y3)
    
    
    
    
    def multiply_point(self, k: int, P: Tuple[int, int]) -> Tuple[int, int]:   #умножение kP
        if k == 0 or P == self.O:
            return self.O
        
        if k < 0:
            k = -k              #отрицательные k, св-во -P=(x; -y)
            P = (P[0], (-P[1]) % self.p)
        
        result = self.O         # Алгоритм удвоения-сложения аналог алгоритму возв в степ)
        temp = P
        
        while k > 0:
            if k & 1:           #младший бит
                result = self.add_points(result, temp)
            temp = self.add_points(temp, temp)      #удваивается
            k >>= 1             #сдвиг вправо
        
        return result
    
    def naive_count_points(self) -> Tuple[List[Tuple[int, int]], int]:          #наивный перебор для малых p
        points = [self.O]
        
        for x in range(self.p):                 #перебор всех x
            rhs = (x*x*x + self.a*x + self.b) % self.p          #правая часть уравн
            
            y_sq = self._sqrt_mod(rhs)                  #проверка, является ли правая часть уравн квадратичным вычетом
            
            if y_sq is not None:
                points.append((x, y_sq))                        #нашли точку (x, y)
                
                if y_sq != 0:                   
                    points.append((x, (-y_sq) % self.p))                            #если y != 0 добавляем вторую точку (x, -y)
        
        return points, len(points)
   
   
   
    
    def baby_step_giant_step(self, P: Tuple[int, int]) -> int:
        if P == self.O:     #бесконеч удал имеет порядок 1
            return 1
                                                                #на вход эллиптич кривая и точка на кривой рандомная

        Q = self.multiply_point(self.p + 1, P)              #шаг 1. Q ← (p+1)P

        m = int(math.isqrt(int(math.isqrt(self.p)))) + 1            #m - размер малых шагов         # Шаг 2. Выбираем целое m > √[4]{p}
        
        baby_steps = {}         
        current = self.O         #начало с 0
        
        for j in range(m + 1):
            baby_steps[current] = j     #сохраняем точку 
            if j < m:       #если не последняя итерация
                current = self.add_points(current, P)       #вычисляем (j+1)P = jP + P
        
        two_m_P = self.multiply_point(2 * m, P)             # 2mP для больших шагов
        
        found = False       #флаг успешного поиска
        k_found = 0
        l_found = 0
                                                        # Шаг 3. точки Q + k(2mP) для k = -m..m
        for k in range(-m, m + 1):
            if k == 0:
                k_point = self.O
            elif k > 0:
                k_point = self.multiply_point(k, two_m_P)
            else:  
                k_abs = -k          #к абсолют
                k_point = self.multiply_point(k_abs, two_m_P)       #умнож на модуль и бер обратную
                if k_point != self.O:       # Берем обратную точку
                    k_point = (k_point[0], (-k_point[1]) % self.p)
            
            current_point = self.add_points(Q, k_point)                 #вычисляем Q + k(2mP)
            
            if current_point in baby_steps:                         #проверяем совпадение с jP
                j = baby_steps[current_point]
                l_found = -j
                k_found = k
                found = True
                break
            
            if current_point != self.O:                         #проверяем совпадение с -jP
                neg_point = (current_point[0], (-current_point[1]) % self.p)
                if neg_point in baby_steps:
                    j = baby_steps[neg_point]
                    l_found = j
                    k_found = k
                    found = True
                    break
        
        if not found:
            return 0        #не найдено = ошибка
        
        M = self.p + 1 + 2 * m * k_found + l_found              #M = p+1 + 2mk ± j делит порядок точки P
        
        factors = self._factorize(M)
        unique_factors = []             #факторизация для простых делителей
        seen = set()
        for f in factors:
            if f not in seen:
                unique_factors.append(f)        #добавление только уникальных
                seen.add(f)                 #память что уже было
        
        current_M = M
        for p_i in unique_factors:                  # Шаг 6. уточнене порядка, удаляя лишние множители
            while current_M % p_i == 0:
                test_point = self.multiply_point(current_M // p_i, P)                       #вычисляем (M/p_i)P
                if test_point == self.O:
                    current_M //= p_i       #если результат = 0, то порядок меньше в iраз
                else:
                    break
        
        return current_M                    #возвращаем порядок точки P
 
 
 
 
 
 
    
    def _factorize(self, n: int) -> List[int]:      #факторизация для простых множителей
        if n <= 1:
            return []
        
        factors = []
        temp = n
        
        while temp % 2 == 0:
            factors.append(2)
            temp //= 2                          #проверяем делимость на 2, потом на нечет 3, 5, 7 и тд
        
        d = 3
        while d * d <= temp:
            while temp % d == 0:
                factors.append(d)
                temp //= d
            d += 2
        
        if temp > 1:
            factors.append(temp)        #если остаток >1 то это ласт простой множитель
        
        return factors
 
    
    def calculate_group_order(self, force_recalculate: bool = False) -> int:            #вычисление порядка группы точек эллиптической кривой      
        if self._group_order is not None and not force_recalculate:
            return self._group_order
        
        if self.p < 1000:
            _, order = self.naive_count_points()                    #для малых p наивный алгоритм
            self._group_order = order
            return order
        
        
        sqrt_p = int(math.isqrt(self.p))                    #интервал Хассе
        lower_bound = self.p + 1 - 2 * sqrt_p
        upper_bound = self.p + 1 + 2 * sqrt_p
        
        orders = []
        points = []
        
        max_attempts = min(20, self.p // 100 + 1)           #повторяем для случайных точек
        
        for attempt in range(max_attempts):
            P = self.get_random_point()                         #генерируем случайную точку
            if P is None:
                continue
            
            try:
                order_P = self.baby_step_giant_step(P)                          #вычисляем порядок точки алгоритмом больших и малых шагов
                if order_P > 0 and lower_bound <= order_P <= upper_bound:
                    orders.append(order_P)          #проверка точки на интервал Хассе
                    points.append(P)
                    
                    if self.multiply_point(order_P, P) != self.O:
                        factors = self._factorize(order_P)          #факторизуем найденный порядок, проверка
                        for factor in factors:
                            test_order = order_P // factor      #проверка деления порядка на делитель
                            if test_order > 0 and self.multiply_point(test_order, P) == self.O:         #если равен 0, обновляем порядок
                                order_P = test_order
                                orders[-1] = order_P    
                                break
            except Exception:
                continue
        
        if not orders:                                  # Если все-таки не удалось вычислить, то берем оценку по теореме Хассе
            self._group_order = self.p + 1
            return self._group_order
        
        lcm_order = 1                   # Ищем НОК порядков точек по т. Лагранжа
        for order in orders:
            lcm_order = lcm_order * order // math.gcd(lcm_order, order)     #для каждого найденного порядка
        
        possible_orders = []        #ищем N в интервале Хассе, которое делится на НОК
        
        for N in range(lower_bound, upper_bound + 1):                   #проверяем делители lcm_order в интервале Хассе
            if N % lcm_order == 0:                                             #проверяем, что N - порядок группы
                valid = True
                for P in points:
                    if self.multiply_point(N, P) != self.O:
                        valid = False
                        break
                
                if valid:
                    possible_orders.append(N)
        
        if possible_orders:
            self._group_order = min(possible_orders)            #берем наименьший порядок
        else:
            self._group_order = self.p + 1      #иначе наиточнейшая оценка хассе
        
        return self._group_order
 
 
 
    
    def get_random_point(self, attempts: int = 100) -> Optional[Tuple[int, int]]:           #генерация случайной точки на эллиптической кривой
        for _ in range(attempts):
            x = random.randint(0, self.p - 1)               #случайная x
            rhs = (x*x*x + self.a*x + self.b) % self.p          #под нее правую часть 
            
            y = self._sqrt_mod(rhs)
            if y is not None:           #если корень существует, то rhs - квадратичный вычет, точка найдена
                return (x, y)
        
        return None
   
    
    def get_all_points(self) -> List[Tuple[int, int]]:              #получение всех точек эллиптической кривой (или первых точек для больших p)

        if self._all_points_cache is not None:
            return self._all_points_cache           #проверка кеша
        
        if self.p < 10000:                      #для малых p используем наивный алгоритм
            points, _ = self.naive_count_points()
            self._all_points_cache = points
        else:
            points = [self.O]
            x = 0
            
            while len(points) < 101 and x < self.p:
                rhs = (x*x*x + self.a*x + self.b) % self.p          #вычисляем правую часть уравнения на принадлежнсть кривой
                y = self._sqrt_mod(rhs)
                
                if y is not None:
                    points.append((x, y))           #если корень сущ., дабавл точку в лист
                    if y != 0:
                        points.append((x, (-y) % self.p))       #если y!0, то add симметрич точку
                
                x += 1          #и идем дальше
            
            self._all_points_cache = points         #найденные сохраняем в кеш
        
        return self._all_points_cache

    
    def generate_first_n_points(self, n: int = 50) -> List[Tuple[int, int]]:            #генерация первых n точек эллиптической кривой в порядке возрастания x)
        points = [self.O]
        x = 0
        
        while len(points) < n + 1 and x < self.p:
            rhs = (x*x*x + self.a*x + self.b) % self.p          #вычисл правую часть уравн для каждого икса
            y = self._sqrt_mod(rhs)
            
            if y is not None:
                points.append((x, y))
                if y != 0 and len(points) < n + 1:          #если есть квадратич вычет, то добавляем точку
                    points.append((x, (-y) % self.p))
            
            x += 1
        
        return points[:n + 1]
    
    def get_hasse_interval(self) -> Tuple[int, int]:            #вычисление интервала Хассе для порядка группы эллиптической кривой       
        sqrt_p = int(math.isqrt(self.p))        #целая часть квадратного корня
        return (self.p + 1 - 2 * sqrt_p, self.p + 1 + 2 * sqrt_p)           #кортеж верхней и нижней границ
 
    
    
    
    
    
    def _find_subgroups_of_order(self, q: int) -> List[List[Tuple[int, int]]]:  #поиск подгрупп заданного простого порядка q
        
        order = self.calculate_group_order()        #на вход порядок группы
        
        if order % q != 0:                  #если q не делит порядок группы
            return []
        
        subgroups = []
        

        if q == 2:          #особый случай для порядка 2, точка симметрична сама себе
            for x in range(self.p):
                if (x*x*x + self.a*x + self.b) % self.p == 0:
                    P = (x, 0)      #кандидат
                    if self.is_on_curve(P):                                             #проверяем, что порядок действительно 2
                        if self.multiply_point(2, P) == self.O:
                            subgroup = [self.O, P]                                                          #если нашли точку порядка 2, строим подгруппу
                            if not any(all(p in s for p in subgroup) for s in subgroups):
                                subgroups.append(subgroup)                                                          #проверяем, что не нашли уже эту же подгруппу
            return subgroups
        
        attempts = 0        #счетчик попыток
        max_attempts = min(1000, self.p)            #макс число попыток
        
        while attempts < max_attempts:
            attempts += 1               #попытки найти образующую
            
            P = self.get_random_point()                         #ьерем рандомную точку
            if P is None or P == self.O:
                continue            #если неудалось, пропускаем попытку
            
            candidate = self.multiply_point(order // q, P)                      #вычисляем точку порядка q: (order/q)*P
            
            if candidate == self.O:     #если 0 -- не подходит
                continue
            
            if self.multiply_point(q, candidate) != self.O:                             #проверяем, что кандидат действительно имеет порядок q
                continue
            
            subgroup = []                       #построение подгруппу
            current = self.O
            for _ in range(q):
                subgroup.append(current)
                current = self.add_points(current, candidate)
            
            is_new = True       #проверка что это новая подгруппа 
            for existing_subgroup in subgroups:
                if len(existing_subgroup) == len(subgroup):                         #если все точки подгруппы совпадают с существующей
                    all_points_match = True      
                    for p1, p2 in zip(existing_subgroup, subgroup):     #сравнение точек попарно
                        if p1 != p2:
                            all_points_match = False    #разные подгруппы
                            break
                    if all_points_match:
                        is_new = False      #уже найденная подгруппа, стопаем
                        break
            
            if is_new:
                subgroups.append(subgroup)                          #для циклической группы достаточно одной подгруппы
                break
        
        return subgroups
    
    def find_prime_order_subgroups(self) -> Dict[int, List[List[Tuple[int, int]]]]:             #Главная функция поиска всех подгрупп простого порядка на эллиптической кривой

        print("  Вычисление порядка группы")
        order = self.calculate_group_order()
        print(f"  Порядок группы: {order}")
        
        factors = self._factorize(order)                #факторизуем порядок
        
        prime_factors = []
        seen = set()                    #уникальные простые делители
        for f in factors:           #прохоим по всем множителям
            if f not in seen:
                prime_factors.append(f)
                seen.add(f)         #кешируем увиденное
        
        print(f"  Простые делители порядка: {prime_factors}")
        
        result = {}         #словарь для результатов 
        
        for q in prime_factors:
            if q == 1:          #единица тривиальна, пропускаем
                continue
            
            print(f"  Поиск подгрупп порядка {q}")
            subgroups = self._find_subgroups_of_order(q)
            
            unique_subgroups = []                       #удаляем дубликаты подгрупп
            seen_sets = []
            
            for subgroup in subgroups:

                point_set = set()                           #создаем множество точек кроме бесконечно удаленной
                for point in subgroup:
                    if point != self.O:
                        point_set.add(point)
                
                sorted_points = tuple(sorted(point_set))        #Преобразуем множество в отсортированный кортеж для однозначного сравнения
                
                if sorted_points not in seen_sets:      #проверяем встречали или нет
                    seen_sets.append(sorted_points)
                    unique_subgroups.append(subgroup)           #добавляем уникальную подгруппу 
            
            if unique_subgroups:        #если нашли хотя бы одну подгруппу 
                result[q] = unique_subgroups
                print(f"  Найдено {len(unique_subgroups)} подгрупп порядка {q}")
            else:
                print(f"  Подгрупп порядка {q} не найдено")
        
        return result           #на выходе словарь всех найденных подгрупп простого порядка


def display_points(points: List[Tuple[int, int]], max_display: int = 50) -> None:
    if not points:
        print("Точек не найдено")           #проверка на пустой список точек
        return
    
    print(f"Всего точек: {len(points)}")
    
    if len(points) > max_display:
        print(f"Отображаются первые {max_display} точек:")      
        points_to_display = points[:max_display]
    else:
        points_to_display = points
    
    for i, point in enumerate(points_to_display):       #отображение каждой точки с нумерацией
        if point == (None, None):
            print(f"  {i+1}. O (бесконечно удаленная точка)")       #бесконечно удаленная
        else:
            print(f"  {i+1}. ({point[0]}, {point[1]})")     #обычная точка


def display_subgroups(subgroups_dict: Dict[int, List[List[Tuple[int, int]]]]) -> None:
    if not subgroups_dict:
        print("Подгрупп не найдено")
        return
    
    total_subgroups = sum(len(subs) for subs in subgroups_dict.values())        #сумма длин всех поисков подгрупп
    print(f"Всего найдено {total_subgroups} подгрупп:")
    
    for order, subgroups in subgroups_dict.items():         #проходим по всем порядкам подгрупп в словаре
        print(f"\n{'='*60}")
        print(f"Порядок {order}: {len(subgroups)} подгрупп")
        print(f"{'='*60}")
        
        for i, subgroup in enumerate(subgroups, 1):         #проходим по каждой подгруппе данного порядка
            print(f"\nПодгруппа {i} (порядок {order}):")
            
            if order <= 10:     #маленькие подгруппы
                print(f"  Точки подгруппы ({len(subgroup)}):")
                for j, point in enumerate(subgroup):
                    if point == (None, None):
                        print(f"    {j+1}. O")
                    else:
                        print(f"    {j+1}. ({point[0]}, {point[1]})")
            else:
                if subgroup and len(subgroup) > 1:
                    generator = None                #большие подгруппы
                    for point in subgroup:
                        if point != (None, None):       #пропускаем точку 0
                            generator = point           #нашли образующую
                            break
                    
                    if generator:
                        print(f"  Образующая точка: ({generator[0]}, {generator[1]})")
                        
                        print(f"  Первые 10 точек из {len(subgroup)}:")
                        points_str = []
                        for j in range(1, min(11, len(subgroup))):             #определяем начальный индекс. зависит от того, с чего начинается подгруппа
                            point = subgroup[j] if subgroup[0] == (None, None) else subgroup[j-1]           #если с 0, берем subgroup[j-1]
                            if point == (None, None):       #точка 0
                                points_str.append("O")
                            else:
                                points_str.append(f"({point[0]},{point[1]})")
                        
                        print("    " + ", ".join(points_str))       #вывод точки в строку
                        
                        if len(subgroup) > 11:
                            print(f" и еще {len(subgroup) - 11} точек")         #если точек больше 10, то показываем сколько осталось


def main():
    print("=" * 60)
    print("ИНСТРУМЕНТ ДЛЯ ИССЛЕДОВАНИЯ ЭЛЛИПТИЧЕСКИХ КРИВЫХ")
    print("=" * 60)
    
    try:
        p = int(input("Введите простое число p (p > 3): "))
        a = int(input("Введите коэффициент a: "))
        b = int(input("Введите коэффициент b: "))
        
        print("\n" + "=" * 40)              #создание кривой
        print("Создание эллиптической кривой")
        
        curve = EllipticCurve(a, b, p)
        print(f"Кривая: y^2 = x^3 + {a}x + {b} (mod {p})")
        
        disc = (-4 * pow(a, 3, p) - 27 * pow(b, 2, p)) % p
        print(f"Дискриминант: {disc} != 0 mod {p} ")

        while True:
            print("\n" + "=" * 40)
            print("МЕНЮ:")
            print("1. Построить группу точек и вычислить порядок")
            print("2. Вычислить кратную точку")
            print("3. Найти подгруппы простого порядка")
            print("4. Проверить теорему Хассе")
            print("5. Выход")
            print("=" * 40)
            
            choice = input("Выберите опцию (1-5): ").strip()
            
            if choice == "1":
                print("\n- Построение группы точек и вычисление порядка -")
                
                start_time = datetime.now()
                if p < 1000:
                    print("полный перебор (p<1000)")
                    points, order = curve.naive_count_points()
                else:
                    print("алгоритм больших и малых шагов (p>1000)")
                    order = curve.calculate_group_order(force_recalculate=True)
                    points = curve.generate_first_n_points(50)
                
                elapsed = (datetime.now() - start_time).total_seconds()
                
                print(f"Порядок группы |E| = {order}")
                print(f"Время вычисления: {elapsed:.2f} сек")
                
                if points:              #отображение точек
                    display_points(points, min(50, len(points)))
                else:
                    print("Точек не найдено")
    
                hasse_lower, hasse_upper = curve.get_hasse_interval()                       #проверка теоремы Хассе
                print(f"\nТеорема Хассе: | |E| - (p+1) | ≤ 2√p")
                print(f"Интервал Хассе: [{hasse_lower}, {hasse_upper}]")
                print(f"|E| - (p+1) = {order - (p+1)}")
                print(f"2√p ≈ {2 * math.sqrt(p):.2f}")
                
                if hasse_lower <= order <= hasse_upper:
                    print(" Теорема Хассе выполняется")
                else:
                    print(" Теорема Хассе не выполняется")
            
            elif choice == "2":
                print("\n- Вычисление кратной точки -")
                try:
                    x = int(input("Введите x-координату точки P: "))
                    y = int(input("Введите y-координату точки P: "))
                    k = int(input("Введите кратность k: "))
                    
                    P = (x, y)
                    
                    if not curve.is_on_curve(P):            #проверка точки
                        print("Точка не лежит на кривой")
                        left = (y * y) % curve.p
                        right = (x*x*x + curve.a*x + curve.b) % curve.p
                        print(f"Проверка: y² = {left}, x³+ax+b = {right}")
                        continue
                    
                    print(f"\nВычисление {k}P")
                    start_time = datetime.now()
                    kP = curve.multiply_point(k, P)
                    elapsed = (datetime.now() - start_time).total_seconds()
                    
                    if kP == curve.O:
                        print(f"Результат: {k}P = O (бесконечно удаленная точка)")
                    else:
                        print(f"Результат: {k}P = ({kP[0]}, {kP[1]})")
                        
                        # Проверка результата
                        if curve.is_on_curve(kP):
                            print("Результат лежит на кривой")
                        else:
                            print("Ошибка, результат не лежит на кривой")
                    
                    
                    # Дополнительно: показать несколько первых кратных
                    if 0 < k <= 20:
                        print(f"\nПошаговое вычисление:")
                        for i in range(1, min(k, 10) + 1):
                            iP = curve.multiply_point(i, P)
                            if iP == curve.O:
                                print(f"{i}P = O")
                            else:
                                print(f"{i}P = ({iP[0]}, {iP[1]})")
                
                except ValueError as e:
                    print(f"Ошибка ввода: {e}")
                except Exception as e:
                    print(f"Ошибка при вычислении: {e}")
            
            elif choice == "3":
                print("\n- Поиск подгрупп простого порядка -")
                
                start_time = datetime.now()
                subgroups_dict = curve.find_prime_order_subgroups()
                elapsed = (datetime.now() - start_time).total_seconds()
                
                display_subgroups(subgroups_dict)
            
            elif choice == "4":
                print("\n- Проверка теоремы Хассе -")
                order = curve.calculate_group_order()
                hasse_lower, hasse_upper = curve.get_hasse_interval()
                
                print(f"p = {p}")
                print(f"√p ≈ {math.sqrt(p):.2f}")
                print(f"2√p ≈ {2 * math.sqrt(p):.2f}")
                print(f"p + 1 = {p + 1}")
                print(f"Интервал Хассе: [{hasse_lower}, {hasse_upper}]")
                print(f"Порядок группы |E| = {order}")
                print(f"| |E| - (p+1) | = |{order} - {p+1}| = {abs(order - (p+1))}")
                
                deviation = abs(order - (p + 1))
                bound = 2 * math.sqrt(p)
                
                print(f"\nПроверка: {deviation:.2f} ≤ {bound:.2f}")
                
                if deviation <= bound + 1e-10:
                    print("Теорема Хассе выполняется")
                else:
                    print("Теорема Хассе НЕ выполняется")
            
            elif choice == "5":
                print("Выход из программы.")
                break
            
            else:
                print("Неверный выбор. Попробуйте снова.")
    
    except ValueError as e:
        print(f"Ошибка: {e}")
    except KeyboardInterrupt:
        print("\nпрограмма прервана пользователем.")
    except Exception as e:
        print(f"неожиданная ошибка: {e}")


if __name__ == "__main__":
    main()