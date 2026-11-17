import os
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon


def get_unique_colors(num_colors):
    """Генерирует список уникальных цветов для каждой траектории."""
    colors = set()
    while len(colors) < num_colors:
        color = (random.random(), random.random(), random.random())
        colors.add(color)
    return list(colors)


def draw_shape_boundary(shape_choice, ax, shape_params, color='red', linewidth=2):
    """
    Отрисовывает гладкую аналитическую границу фигуры поверх пиксельной маски.
    Использует математически точные геометрические примитивы.
    """
    if shape_choice == '1':
        # Квадрат: рисуем прямоугольник по координатам маски
        L = shape_params['L']
        x0, y0 = 0.5, 0.5
        x1, y1 = L + 0.5, L + 0.5
        rect = Polygon(
            [[x0, y0], [x1, y0], [x1, y1], [x0, y1]],
            closed=True, fill=False,
            edgecolor=color, linewidth=linewidth
        )
        ax.add_patch(rect)

    elif shape_choice == '2':
        # Круг: рисуем окружность
        R = shape_params['R']
        cx = shape_params['cx']
        cy = shape_params['cy']
        circle = Circle((cx, cy), R + 0.5, fill=False,
                        edgecolor=color, linewidth=linewidth)
        ax.add_patch(circle)

    elif shape_choice == '3':
        # Треугольник: рисуем треугольник по вершинам
        s = shape_params['s']
        h = shape_params['h']
        cx = shape_params['cx']
        cy = shape_params['cy']

        top   = (cx,                cy - h / 2 - 0.5)
        bot_l = (cx - s / 2 - 0.5, cy + h / 2 + 0.5)
        bot_r = (cx + s / 2 + 0.5, cy + h / 2 + 0.5)

        triangle = Polygon(
            [top, bot_l, bot_r],
            closed=True, fill=False,
            edgecolor=color, linewidth=linewidth
        )
        ax.add_patch(triangle)


def build_field(area, shape_choice):
    """
    Создает логическое поле (маску) заданной формы и площади.
    Возвращает маску, размер сетки N, фактическую площадь и параметры фигуры.
    """
    shape_params = {}

    if shape_choice == '1':  # Правильный квадрат
        L = max(1, round(np.sqrt(area)))
        N = L
        core_mask = np.ones((N, N), dtype=bool)
        shape_params['L'] = L
        # Добавляем координаты центра для 2-го и 3-го режимов блуждания
        shape_params['cx'] = (N + 2) // 2
        shape_params['cy'] = (N + 2) // 2

    elif shape_choice == '2':  # Правильный круг
        R = max(1, round(np.sqrt(area / np.pi)))
        N = 2 * R + 1
        cx, cy = R, R  # центр в координатах core_mask

        # Векторизованное создание маски круга
        y_idx, x_idx = np.ogrid[:N, :N]
        core_mask = ((x_idx - cx) ** 2 + (y_idx - cy) ** 2) <= R ** 2

        shape_params['R'] = R
        # Сразу сохраняем координаты центра с учётом будущего padding = 1
        shape_params['cx'] = cx + 1
        shape_params['cy'] = cy + 1

    elif shape_choice == '3':  # Правильный треугольник
        s = max(1, round(np.sqrt(4 * area / np.sqrt(3))))
        h = max(1, round(np.sqrt(3) / 2 * s))
        N = max(s, h)
        cx, cy = N // 2, N // 2
        core_mask = np.zeros((N, N), dtype=bool)

        for y in range(N):
            for x in range(N):
                dx = x - cx
                dy = y - cy
                if -h / 2 <= dy <= h / 2:
                    half_w = ((dy + h / 2) / h) * (s / 2)
                    if -half_w <= dx <= half_w:
                        core_mask[y, x] = True

        shape_params['s'] = s
        shape_params['h'] = h
        # Сразу сохраняем координаты центра с учётом будущего padding = 1
        shape_params['cx'] = cx + 1
        shape_params['cy'] = cy + 1
    else:
        return None, 0, 0, {}

    # Добавляем padding = 1 со всех сторон
    N_final = N + 2
    valid_mask = np.zeros((N_final, N_final), dtype=bool)
    valid_mask[1:-1, 1:-1] = core_mask

    actual_area = int(np.sum(valid_mask))
    return valid_mask, N_final, actual_area, shape_params


def find_start(valid_mask, N, shape_choice, shape_params):
    """
    Возвращает начальную точку:
    - Для треугольника — геометрический центроид (1/3 высоты от основания).
    - Для остальных фигур — геометрический центр сетки.
    Если целевая клетка невалидна — ищет ближайшую валидную.
    """
    if shape_choice == '3':
        cx = shape_params['cx']
        cy = shape_params['cy']
        h  = shape_params['h']
        target_x = int(round(cx))
        target_y = int(round(cy + h / 6))
    else:
        target_x = N // 2
        target_y = N // 2

    if 0 <= target_x < N and 0 <= target_y < N and valid_mask[target_y, target_x]:
        return target_x, target_y

    # Ищем ближайшую валидную клетку по спирали
    for r in range(1, N):
        for dy in range(-r, r + 1):
            for dx in range(-r, r + 1):
                nx, ny = target_x + dx, target_y + dy
                if 0 <= nx < N and 0 <= ny < N and valid_mask[ny, nx]:
                    return nx, ny

    return target_x, target_y  # fallback


def run_simulation():
    print("--- Настройка симуляции ---")
    try:
        area = int(input("Введите площадь будущего поля: "))

        print("\nВыберите форму будущего поля:")
        print("1 - Квадрат")
        print("2 - Круг")
        print("3 - Правильный треугольник")
        shape_choice = input("Введите номер формы (1, 2 или 3): ").strip()

        print("\nВыберите окрестность для дрейфа:")
        print("1 - Окрестность Мура (8 направлений)")
        print("2 - Окрестность Неймана (4 направления)")
        neighborhood_choice = input("Введите номер окрестности (1 или 2): ").strip()

        print("\nВыберите режим блуждания:")
        print("1 - Шаг равновероятен в любую сторону после любого хода")
        print("2 - Вероятность шагнуть дальше от центра падает на заданный процент")
        print("3 - Вероятность шагнуть дальше от центра повышается на заданный процент")
        mode_choice = input("Введите номер режима (1, 2 или 3): ").strip()

        # Запрос процента для режимов 2 и 3
        prob_change_percent = 1.0  # Значение по умолчанию
        if mode_choice in ('2', '3'):
            while True:
                try:
                    prob_change_percent = float(input("Введите процент изменения вероятности (например, 1 для 1% или 2.5 для 2.5%): "))
                    if prob_change_percent < 0:
                        print("Ошибка: процент не может быть отрицательным. Попробуйте снова.")
                        continue
                    break
                except ValueError:
                    print("Ошибка: введите корректное число (например, 1 или 2.5).")

        max_steps = int(input("\nВведите максимальное количество шагов (итераций): "))
        num_trajectories = int(input("Введите количество запускаемых траекторий: "))

        if area <= 0 or max_steps <= 0 or num_trajectories <= 0:
            print("Все значения должны быть положительными целыми числами.")
            return
    except ValueError:
        print("Ошибка: Введите корректные целые числа.")
        return

    # Выбор окрестности
    if neighborhood_choice == '1':
        offsets = [(-1, -1), (-1, 0), (-1, 1),
                   (0, -1),           (0, 1),
                   (1, -1),  (1, 0),  (1, 1)]
        neighborhood_name = "Мура"
    else:
        offsets = [(-1, 0), (0, -1), (0, 1), (1, 0)]
        neighborhood_name = "Неймана"

    # Строим поле
    valid_mask, N, actual_area, shape_params = build_field(area, shape_choice)
    if valid_mask is None:
        print("Ошибка выбора формы.")
        return

    print(f"\nПоле создано. Размер сетки: {N}x{N}. Фактическая площадь: {actual_area} клеток.")
    print(f"Используется окрестность: {neighborhood_name}")
    
    mode_str = 'Равновероятный'
    if mode_choice == '2':
        mode_str = f'Вероятность удаления падает на {prob_change_percent}% за клетку'
    elif mode_choice == '3':
        mode_str = f'Вероятность удаления растет на {prob_change_percent}% за клетку'
    print(f"Режим блуждания: {mode_str}")

    # Начальная точка
    start_x, start_y = find_start(valid_mask, N, shape_choice, shape_params)
    print(f"Начальная точка: ({start_x}, {start_y})")

    # Папка для сохранения
    save_dir = os.path.join(os.getcwd(), "simulation_results")
    os.makedirs(save_dir, exist_ok=True)

    # Инициализация данных
    heatmap = np.zeros((N, N))
    all_trajectories = []
    death_steps = []
    death_count = 0

    colors = get_unique_colors(num_trajectories)
    plt.ioff()

    print(f"\nНачало симуляции {num_trajectories} траекторий...")

    # Координаты центра для 2-го и 3-го режимов
    cx = shape_params.get('cx', N // 2)
    cy = shape_params.get('cy', N // 2)
    
    # Перевод процента в дробный коэффициент (например, 1% -> 0.01)
    prob_factor = prob_change_percent / 100.0

    for t in range(num_trajectories):
        x, y = start_x, start_y

        path_x = [x]
        path_y = [y]
        heatmap[y, x] += 1

        steps_survived = 0
        died = False

        for step in range(max_steps):
            if mode_choice in ('2', '3'):
                # Режимы 2 и 3: Вероятность шага зависит от расстояния до центра
                # Используем расстояние Чебышёва (покоординатное), как "клетки расстояния"
                dist = max(abs(x - cx), abs(y - cy))
                
                weights = []
                for dx, dy in offsets:
                    nx, ny = x + dx, y + dy
                    new_dist = max(abs(nx - cx), abs(ny - cy))
                    
                    if new_dist > dist:
                        if mode_choice == '2':
                            # Шаг удаляет от центра: вероятность падает на заданный процент
                            w = max(0.0, 1.0 - prob_factor * dist)
                        else:
                            # Шаг удаляет от центра: вероятность растет на заданный процент
                            w = 1.0 + prob_factor * dist
                    else:
                        # Шаг приближает или сохраняет расстояние: базовая вероятность
                        w = 1.0
                    weights.append(w)
                
                # В режиме 2 при больших процентах сумма весов может стать 0. 
                if sum(weights) == 0:
                    dx, dy = random.choice(offsets)
                else:
                    dx, dy = random.choices(offsets, weights=weights, k=1)[0]
            else:
                # Режим 1: Равновероятный шаг
                dx, dy = random.choice(offsets)

            nx, ny = x + dx, y + dy

            # Гибель: выход за сетку ИЛИ за границу фигуры
            if nx < 0 or nx >= N or ny < 0 or ny >= N or not valid_mask[ny, nx]:
                died = True
                death_count += 1
                death_steps.append(steps_survived + 1)
                path_x.append(nx)
                path_y.append(ny)
                break
            else:
                x, y = nx, ny
                path_x.append(x)
                path_y.append(y)
                heatmap[y, x] += 1
                steps_survived += 1

        all_trajectories.append((path_x, path_y))

        # --- Индивидуальная траектория ---
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.imshow(valid_mask, cmap='gray', alpha=0.15,
                  origin='upper', interpolation='nearest')
        draw_shape_boundary(shape_choice, ax, shape_params,
                            color='red', linewidth=2)

        ax.plot(path_x, path_y, color=colors[t],
                marker='.', linestyle='-', markersize=3, linewidth=1)

        ax.set_xlim(-2, N + 1)
        ax.set_ylim(N + 1, -2)
        ax.set_aspect('equal')
        ax.grid(True, linestyle=':', alpha=0.6)
        ax.set_title(f"Траектория {t + 1} ({'Погибла' if died else 'Выжила'})")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        fig.savefig(os.path.join(save_dir, f"trajectory_{t + 1}.png"), dpi=100)
        plt.close(fig)

    print("Симуляция завершена. Сохранение общих графиков...")

    # --- Все траектории вместе ---
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.imshow(valid_mask, cmap='gray', alpha=0.15,
              origin='upper', interpolation='nearest')
    draw_shape_boundary(shape_choice, ax, shape_params,
                        color='red', linewidth=2.5)

    for i, (px, py) in enumerate(all_trajectories):
        ax.plot(px, py, color=colors[i], alpha=0.6, linewidth=1)

    ax.set_xlim(-2, N + 1)
    ax.set_ylim(N + 1, -2)
    ax.set_aspect('equal')
    ax.set_title(f"Все траектории ({num_trajectories} шт.)")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    fig.savefig(os.path.join(save_dir, "all_trajectories.png"), dpi=150)
    plt.close(fig)

    # --- Тепловая карта ---
    fig, ax = plt.subplots(figsize=(8, 8))
    im = ax.imshow(heatmap, cmap='hot',
                   interpolation='nearest', origin='upper')
    plt.colorbar(im, ax=ax, label='Количество посещений клетки')
    draw_shape_boundary(shape_choice, ax, shape_params,
                        color='red', linewidth=2)
    ax.set_aspect('equal')
    ax.set_title("Тепловая карта посещений")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    fig.savefig(os.path.join(save_dir, "heatmap.png"), dpi=150)
    plt.close(fig)

    # --- Статистика ---
    print("\n--- Результаты симуляции ---")

    if death_count > 0:
        avg_steps  = np.mean(death_steps)
        prob_death = death_count / num_trajectories

        print(f"1. Среднее количество шагов до гибели: {avg_steps:.2f}")
        print(f"2. Вероятность выйти за границу (гибель): {prob_death * 100:.2f}% "
              f"({death_count} из {num_trajectories} траекторий погибло)")
    else:
        print("Ни одна клетка не погибла за указанное количество итераций.")

    print(f"\nВсе изображения сохранены в папку: {save_dir}")


if __name__ == "__main__":
    run_simulation()