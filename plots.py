import os
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon


# ============================================================
# Вспомогательные функции (скопированы из оригинала без изменений)
# ============================================================

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
    """
    if shape_choice == '1':
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
        R  = shape_params['R']
        cx = shape_params['cx']
        cy = shape_params['cy']
        circle = Circle((cx, cy), R + 0.5, fill=False,
                        edgecolor=color, linewidth=linewidth)
        ax.add_patch(circle)

    elif shape_choice == '3':
        s  = shape_params['s']
        h  = shape_params['h']
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
    """
    shape_params = {}

    if shape_choice == '1':
        L = max(1, round(np.sqrt(area)))
        N = L
        core_mask = np.ones((N, N), dtype=bool)
        shape_params['L'] = L
        shape_params['cx'] = (N + 2) // 2
        shape_params['cy'] = (N + 2) // 2

    elif shape_choice == '2':
        R  = max(1, round(np.sqrt(area / np.pi)))
        N  = 2 * R + 1
        cx, cy = R, R

        y_idx, x_idx = np.ogrid[:N, :N]
        core_mask = ((x_idx - cx) ** 2 + (y_idx - cy) ** 2) <= R ** 2

        shape_params['R']  = R
        shape_params['cx'] = cx + 1
        shape_params['cy'] = cy + 1

    elif shape_choice == '3':
        s  = max(1, round(np.sqrt(4 * area / np.sqrt(3))))
        h  = max(1, round(np.sqrt(3) / 2 * s))
        N  = max(s, h)
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

        shape_params['s']  = s
        shape_params['h']  = h
        shape_params['cx'] = cx + 1
        shape_params['cy'] = cy + 1
    else:
        return None, 0, 0, {}

    N_final = N + 2
    valid_mask = np.zeros((N_final, N_final), dtype=bool)
    valid_mask[1:-1, 1:-1] = core_mask

    actual_area = int(np.sum(valid_mask))
    return valid_mask, N_final, actual_area, shape_params


def find_start(valid_mask, N, shape_choice, shape_params):
    """
    Возвращает начальную точку (центр фигуры или ближайшую валидную клетку).
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

    for r in range(1, N):
        for dy in range(-r, r + 1):
            for dx in range(-r, r + 1):
                nx, ny = target_x + dx, target_y + dy
                if 0 <= nx < N and 0 <= ny < N and valid_mask[ny, nx]:
                    return nx, ny

    return target_x, target_y


# ============================================================
# Основная функция одного прогона симуляции (без рисования траекторий)
# Возвращает: (среднее шагов до гибели | None, процент погибших)
# ============================================================

def run_one_simulation(valid_mask, N, shape_params, shape_choice,
                       offsets, start_x, start_y,
                       mode_choice, prob_change_percent,
                       max_steps, num_trajectories):
    """
    Прогоняет num_trajectories траекторий с заданным процентом изменения
    вероятности и возвращает статистику.

    Returns
    -------
    avg_steps  : float | None  — среднее шагов до гибели (None если никто не погиб)
    death_pct  : float         — доля погибших траекторий (0..100)
    """
    cx = shape_params.get('cx', N // 2)
    cy = shape_params.get('cy', N // 2)
    prob_factor = prob_change_percent / 100.0

    death_count = 0
    death_steps = []

    for _ in range(num_trajectories):
        x, y = start_x, start_y
        steps_survived = 0

        for step in range(max_steps):
            if mode_choice in ('2', '3'):
                dist = max(abs(x - cx), abs(y - cy))

                weights = []
                for dx, dy in offsets:
                    nx, ny = x + dx, y + dy
                    new_dist = max(abs(nx - cx), abs(ny - cy))

                    if new_dist > dist:
                        if mode_choice == '2':
                            # Шаг удаляет — вероятность ПАДАЕТ
                            w = max(0.0, 1.0 - prob_factor * dist)
                        else:
                            # Шаг удаляет — вероятность РАСТЁТ
                            w = 1.0 + prob_factor * dist
                    else:
                        w = 1.0
                    weights.append(w)

                if sum(weights) == 0:
                    dx, dy = random.choice(offsets)
                else:
                    dx, dy = random.choices(offsets, weights=weights, k=1)[0]
            else:
                dx, dy = random.choice(offsets)

            nx, ny = x + dx, y + dy

            if nx < 0 or nx >= N or ny < 0 or ny >= N or not valid_mask[ny, nx]:
                death_count += 1
                death_steps.append(steps_survived + 1)
                break
            else:
                x, y = nx, ny
                steps_survived += 1

    avg_steps = np.mean(death_steps) if death_steps else None
    death_pct = death_count / num_trajectories * 100.0
    return avg_steps, death_pct


# ============================================================
# Главная функция: ввод, перебор процентов, графики
# ============================================================

def run_sweep_simulation():
    print("--- Настройка симуляции (перебор процентов) ---")

    try:
        area = int(input("Введите площадь будущего поля: "))

        print("\nВыберите форму будущего поля:")
        print("1 - Правильный квадрат")
        print("2 - Правильный круг")
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

        # Запрос диапазона и шага только для режимов 2 и 3
        if mode_choice in ('2', '3'):
            print("\n--- Настройка диапазона перебора процентов ---")

            while True:
                try:
                    pct_min = float(input("Введите начальный процент (например, 1 или 0.5): "))
                    if pct_min < 0:
                        print("Ошибка: начальный процент не может быть отрицательным.")
                        continue
                    break
                except ValueError:
                    print("Ошибка: введите корректное число.")

            while True:
                try:
                    pct_max = float(input("Введите конечный процент (например, 10 или 5.0): "))
                    if pct_max < pct_min:
                        print(f"Ошибка: конечный процент должен быть ≥ начального ({pct_min}).")
                        continue
                    break
                except ValueError:
                    print("Ошибка: введите корректное число.")

            while True:
                try:
                    pct_step = float(input("Введите шаг перебора процентов (например, 1 или 0.5): "))
                    if pct_step <= 0:
                        print("Ошибка: шаг должен быть положительным числом.")
                        continue
                    break
                except ValueError:
                    print("Ошибка: введите корректное число.")

        max_steps        = int(input("\nВведите максимальное количество шагов (итераций): "))
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

    # Строим поле один раз — оно одинаково для всех прогонов
    valid_mask, N, actual_area, shape_params = build_field(area, shape_choice)
    if valid_mask is None:
        print("Ошибка выбора формы.")
        return

    print(f"\nПоле создано. Размер сетки: {N}x{N}. Фактическая площадь: {actual_area} клеток.")
    print(f"Используется окрестность: {neighborhood_name}")

    # Начальная точка
    start_x, start_y = find_start(valid_mask, N, shape_choice, shape_params)
    print(f"Начальная точка: ({start_x}, {start_y})")

    # Папка для сохранения
    save_dir = os.path.join(os.getcwd(), "sweep_results")
    os.makedirs(save_dir, exist_ok=True)

    # --------------------------------------------------------
    # Режим 1: один прогон (процент не нужен)
    # --------------------------------------------------------
    if mode_choice == '1':
        print("\nРежим 1 (равновероятный) — процент не используется, запускаем один прогон...")

        avg_steps, death_pct = run_one_simulation(
            valid_mask, N, shape_params, shape_choice,
            offsets, start_x, start_y,
            mode_choice, 0.0,
            max_steps, num_trajectories
        )

        print("\n--- Результаты ---")
        if avg_steps is not None:
            print(f"Среднее шагов до гибели : {avg_steps:.2f}")
        else:
            print("Ни одна траектория не погибла.")
        print(f"Процент погибших        : {death_pct:.2f}%")
        return

    # --------------------------------------------------------
    # Режимы 2 и 3: перебор процентов с заданным шагом
    # --------------------------------------------------------

    # Формируем список процентов через np.arange для точности с float
    percents = []
    pct = pct_min
    while pct <= pct_max + 1e-9:   # небольшой допуск на погрешность float
        percents.append(round(pct, 10))
        pct += pct_step

    if not percents:
        print("Ошибка: диапазон процентов пуст. Проверьте введённые значения.")
        return

    avg_steps_list = []
    death_pct_list = []

    mode_name = "падает" if mode_choice == '2' else "растёт"
    print(f"\nРежим {mode_choice}: вероятность удаления {mode_name}.")
    print(f"Перебираем проценты от {pct_min} до {pct_max} с шагом {pct_step}...\n")

    for pct in percents:
        print(f"  Процент = {pct}% ... ", end="", flush=True)

        avg_s, d_pct = run_one_simulation(
            valid_mask, N, shape_params, shape_choice,
            offsets, start_x, start_y,
            mode_choice, pct,
            max_steps, num_trajectories
        )

        avg_steps_list.append(avg_s)
        death_pct_list.append(d_pct)

        avg_str = f"{avg_s:.2f}" if avg_s is not None else "N/A"
        print(f"среднее шагов до гибели = {avg_str}, погибло = {d_pct:.1f}%")

    # Заменяем None на NaN, чтобы matplotlib корректно рисовал разрывы
    avg_steps_plot = [
        s if s is not None else float('nan')
        for s in avg_steps_list
    ]

    # --------------------------------------------------------
    # График 1: Среднее число шагов до гибели vs процент
    # --------------------------------------------------------
    fig1, ax1 = plt.subplots(figsize=(9, 5))
    ax1.plot(percents, avg_steps_plot,
             marker='o', linewidth=2, color='steelblue', label='Среднее шагов')
    ax1.set_xlabel("Процент изменения вероятности (%)", fontsize=12)
    ax1.set_ylabel("Среднее число шагов до гибели", fontsize=12)
    ax1.set_title(
        f"Среднее число шагов до гибели\n"
        f"(режим {mode_choice}, окр. {neighborhood_name}, "
        f"траекторий={num_trajectories}, шагов≤{max_steps})",
        fontsize=11
    )
    ax1.set_xticks(percents)
    ax1.tick_params(axis='x', rotation=45)
    ax1.grid(True, linestyle='--', alpha=0.6)
    ax1.legend()
    fig1.tight_layout()
    path1 = os.path.join(save_dir, "avg_steps_vs_percent.png")
    fig1.savefig(path1, dpi=150)
    plt.close(fig1)
    print(f"\nГрафик сохранён: {path1}")

    # --------------------------------------------------------
    # График 2: Процент погибших vs процент
    # --------------------------------------------------------
    fig2, ax2 = plt.subplots(figsize=(9, 5))
    ax2.plot(percents, death_pct_list,
             marker='s', linewidth=2, color='tomato', label='% погибших')
    ax2.set_xlabel("Процент изменения вероятности (%)", fontsize=12)
    ax2.set_ylabel("Доля погибших траекторий (%)", fontsize=12)
    ax2.set_title(
        f"Процент погибших траекторий\n"
        f"(режим {mode_choice}, окр. {neighborhood_name}, "
        f"траекторий={num_trajectories}, шагов≤{max_steps})",
        fontsize=11
    )
    ax2.set_xticks(percents)
    ax2.tick_params(axis='x', rotation=45)
    ax2.set_ylim(0, 105)
    ax2.grid(True, linestyle='--', alpha=0.6)
    ax2.legend()
    fig2.tight_layout()
    path2 = os.path.join(save_dir, "death_pct_vs_percent.png")
    fig2.savefig(path2, dpi=150)
    plt.close(fig2)
    print(f"График сохранён: {path2}")

    # --------------------------------------------------------
    # График 3: Оба показателя на одном полотне (двойная ось Y)
    # --------------------------------------------------------
    fig3, ax3 = plt.subplots(figsize=(10, 5))

    color_steps = 'steelblue'
    color_death = 'tomato'

    ax3.plot(percents, avg_steps_plot,
             marker='o', linewidth=2, color=color_steps, label='Среднее шагов')
    ax3.set_xlabel("Процент изменения вероятности (%)", fontsize=12)
    ax3.set_ylabel("Среднее число шагов до гибели", fontsize=12, color=color_steps)
    ax3.tick_params(axis='y', labelcolor=color_steps)
    ax3.tick_params(axis='x', rotation=45)
    ax3.set_xticks(percents)
    ax3.grid(True, linestyle='--', alpha=0.4)

    ax4 = ax3.twinx()   # вторая ось Y
    ax4.plot(percents, death_pct_list,
             marker='s', linewidth=2, color=color_death, label='% погибших')
    ax4.set_ylabel("Доля погибших траекторий (%)", fontsize=12, color=color_death)
    ax4.tick_params(axis='y', labelcolor=color_death)
    ax4.set_ylim(0, 105)

    # Объединяем легенды обеих осей
    lines1, labels1 = ax3.get_legend_handles_labels()
    lines2, labels2 = ax4.get_legend_handles_labels()
    ax3.legend(lines1 + lines2, labels1 + labels2, loc='center right')

    ax3.set_title(
        f"Среднее шагов до гибели и % погибших\n"
        f"(режим {mode_choice}, окр. {neighborhood_name}, "
        f"траекторий={num_trajectories}, шагов≤{max_steps})",
        fontsize=11
    )
    fig3.tight_layout()
    path3 = os.path.join(save_dir, "combined_vs_percent.png")
    fig3.savefig(path3, dpi=150)
    plt.close(fig3)
    print(f"График сохранён: {path3}")

    print(f"\nВсе результаты сохранены в папку: {save_dir}")


# ============================================================
if __name__ == "__main__":
# %%
    run_sweep_simulation()
