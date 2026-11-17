# Лабораторная работа №3
## 🎲 Стохастическое моделирование случайного блуждания

<div align="justify">
Данная компьютерная модель представляет собой симуляцию стохастического (случайного) блуждания частицы на дискретной двумерной сетке с поглощающей границей. Модель предназначена для исследования влияния геометрии области, топологии окрестности и управляемого дрейфа на статистические характеристики процесса: среднее время жизни траектории и вероятность поглощения границей.
    
Процесс описывается как цепь Маркова с дискретным временем. Частица стартует из центральной области фигуры заданной формы (квадрат, круг или правильный треугольник) и совершает шаги в одну из соседних клеток согласно заданному закону распределения вероятностей. Блуждание прекращается при выходе частицы за пределы области («гибель» траектории) или достижении предельного числа шагов. Реализованы три режима блуждания: равновероятный, с дрейфом к центру и с дрейфом от центра.
</div>

### ⌨ Инструкция по запуску
<div align="justify">
Модель написана на языке программирования Python и может быть запущена в большинстве интерактивных IDE. Программа работает в интерактивном режиме и запрашивает параметры через консоль: площадь поля, форму области, тип окрестности (Мура/Неймана), режим блуждания, процент изменения вероятности (для режимов с дрейфом), максимальное количество шагов и число траекторий.
Проект состоит из двух скриптов:
    <ul>
        <li><code>main.py</code> — основная симуляция с визуализацией отдельных траекторий, ансамбля путей и тепловой карты посещений.</li>
        <li><code>plots.py</code> — параметрический анализ: автоматический перебор коэффициента дрейфа с построением графиков зависимостей среднего времени жизни и доли погибших траекторий от процента изменения вероятности.</li>
    </ul>
</div>

### 📃 Структура данных

**Входные параметры:**
*   Площадь поля;
*   Форма области (квадрат, круг, треугольник);
*   Тип окрестности (Мура / Неймана);
*   Режим блуждания (равновероятный / дрейф к центру / дрейф от центра);
*   Процент изменения вероятности (коэффициент дрейфа);
*   Максимальное количество шагов (`max_steps`);
*   Количество запускаемых траекторий.

**Выходные параметры:**
*   Числовые: среднее количество шагов до гибели, вероятность выхода за границу (%), размер итоговой сетки, фактическая площадь фигуры;
*   Графические: индивидуальные траектории (`.png`), совокупность всех траекторий, тепловая карта плотности посещений, графики параметрического анализа (`avg_steps_vs_percent.png`, `death_pct_vs_percent.png`, `combined_vs_percent.png`).

### 🗂 Структура репозитория
*   `README.md` — текущий файл;
*   `main.py` — основной скрипт симуляции и визуализации;
*   `plots.py` — скрипт параметрического анализа и построения графиков;
*   `simulation_results/` — папка с результатами основной симуляции (траектории, тепловые карты);
*   `sweep_results/` — папка с результатами параметрического анализа (графики зависимостей).


### 📊 Результаты эксперимента

Ниже представлены результаты моделирования для различных конфигураций поля и режимов блуждания. 
В каждом блоке: **слева** — тепловая карта плотности посещений, **справа** — ансамбль траекторий.

💡 Для просмотра изображений дождитесь полной загрузки страницы. При медленном интернет-соединении загрузка большого количества рисунков может занять некоторое время.

### 📊 Результаты эксперимента

Ниже представлены результаты моделирования для различных конфигураций поля и режимов блуждания. 
В каждом блоке: **сверху** — тепловая карта плотности посещений, **снизу** — ансамбль траекторий.

<h3>Случай 1. Влияние формы поля</h3>
<table style="border-collapse: collapse; width: 100%; margin-bottom: 20px;">
 <!-- Окрестность Мура -->
 <tr>
  <td width="33%" align="center" valign="top" style="padding: 10px; vertical-align: top;">
   <b>Рисунок 1. Квадрат (Мура)</b><br>
   <sub>Тепловая карта</sub><br>
   <img src="simulation_results/1квадр (2).png" style="width: 100%; max-width: 400px; display: block; margin: 5px auto;"><br>
   <sub>Ансамбль траекторий</sub><br>
   <img src="simulation_results/1квадр.png" style="width: 100%; max-width: 400px; display: block; margin: 5px auto;">
  </td>
  <td width="33%" align="center" valign="top" style="padding: 10px; vertical-align: top;">
   <b>Рисунок 2. Круг (Мура)</b><br>
   <sub>Тепловая карта</sub><br>
   <img src="simulation_results/1круг (2).png" style="width: 100%; max-width: 400px; display: block; margin: 5px auto;"><br>
   <sub>Ансамбль траекторий</sub><br>
   <img src="simulation_results/1круг.png" style="width: 100%; max-width: 400px; display: block; margin: 5px auto;">
  </td>
  <td width="33%" align="center" valign="top" style="padding: 10px; vertical-align: top;">
   <b>Рисунок 3. Треугольник (Мура)</b><br>
   <sub>Тепловая карта</sub><br>
   <img src="simulation_results/1треуг (2).png" style="width: 100%; max-width: 400px; display: block; margin: 5px auto;"><br>
   <sub>Ансамбль траекторий</sub><br>
   <img src="simulation_results/1треуг.png" style="width: 100%; max-width: 400px; display: block; margin: 5px auto;">
  </td>
 </tr>
 <!-- Окрестность Неймана -->
 <tr>
  <td width="33%" align="center" valign="top" style="padding: 10px; vertical-align: top;">
   <b>Рисунок 4. Квадрат (Неймана)</b><br>
   <sub>Тепловая карта</sub><br>
   <img src="simulation_results/2квадр (2).png" style="width: 100%; max-width: 400px; display: block; margin: 5px auto;"><br>
   <sub>Ансамбль траекторий</sub><br>
   <img src="simulation_results/2квадр.png" style="width: 100%; max-width: 400px; display: block; margin: 5px auto;">
  </td>
  <td width="33%" align="center" valign="top" style="padding: 10px; vertical-align: top;">
   <b>Рисунок 5. Круг (Неймана)</b><br>
   <sub>Тепловая карта</sub><br>
   <img src="simulation_results/2круг (2).png" style="width: 100%; max-width: 400px; display: block; margin: 5px auto;"><br>
   <sub>Ансамбль траекторий</sub><br>
   <img src="simulation_results/2круг.png" style="width: 100%; max-width: 400px; display: block; margin: 5px auto;">
  </td>
  <td width="33%" align="center" valign="top" style="padding: 10px; vertical-align: top;">
   <b>Рисунок 6. Треуг. (Неймана)</b><br>
   <sub>Тепловая карта</sub><br>
   <img src="simulation_results/2треуг (2).png" style="width: 100%; max-width: 400px; display: block; margin: 5px auto;"><br>
   <sub>Ансамбль траекторий</sub><br>
   <img src="simulation_results/2треуг.png" style="width: 100%; max-width: 400px; display: block; margin: 5px auto;">
  </td>
 </tr>
</table>

<hr>

<h3>Случай 2. Влияние максимального количества шагов (max_steps)</h3>
<table style="border-collapse: collapse; width: 100%; margin-bottom: 20px;">
 <!-- Окрестность Мура -->
 <tr>
  <td width="33%" align="center" valign="top" style="padding: 10px; vertical-align: top;">
   <b>Рисунок 7. max_steps = 100 (Мура)</b><br>
   <sub>Тепловая карта</sub><br>
   <img src="simulation_results/3_100(2).png" style="width: 100%; max-width: 400px; display: block; margin: 5px auto;"><br>
   <sub>Ансамбль траекторий</sub><br>
   <img src="simulation_results/3_100.png" style="width: 100%; max-width: 400px; display: block; margin: 5px auto;">
  </td>
  <td width="33%" align="center" valign="top" style="padding: 10px; vertical-align: top;">
   <b>Рисунок 8. max_steps = 200 (Мура)</b><br>
   <sub>Тепловая карта</sub><br>
   <img src="simulation_results/3_200(2).png" style="width: 100%; max-width: 400px; display: block; margin: 5px auto;"><br>
   <sub>Ансамбль траекторий</sub><br>
   <img src="simulation_results/3_200.png" style="width: 100%; max-width: 400px; display: block; margin: 5px auto;">
  </td>
  <td width="33%" align="center" valign="top" style="padding: 10px; vertical-align: top;">
   <b>Рисунок 9. max_steps = 300 (Мура)</b><br>
   <sub>Тепловая карта</sub><br>
   <img src="simulation_results/3_300(2).png" style="width: 100%; max-width: 400px; display: block; margin: 5px auto;"><br>
   <sub>Ансамбль траекторий</sub><br>
   <img src="simulation_results/3_300.png" style="width: 100%; max-width: 400px; display: block; margin: 5px auto;">
  </td>
 </tr>
 <!-- Окрестность Неймана -->
 <tr>
  <td width="33%" align="center" valign="top" style="padding: 10px; vertical-align: top;">
   <b>Рисунок 10. max_steps = 100 (Неймана)</b><br>
   <sub>Тепловая карта</sub><br>
   <img src="simulation_results/4_100(2).png" style="width: 100%; max-width: 400px; display: block; margin: 5px auto;"><br>
   <sub>Ансамбль траекторий</sub><br>
   <img src="simulation_results/4_100.png" style="width: 100%; max-width: 400px; display: block; margin: 5px auto;">
  </td>
  <td width="33%" align="center" valign="top" style="padding: 10px; vertical-align: top;">
   <b>Рисунок 11. max_steps = 200 (Неймана)</b><br>
   <sub>Тепловая карта</sub><br>
   <img src="simulation_results/4_200(2).png" style="width: 100%; max-width: 400px; display: block; margin: 5px auto;"><br>
   <sub>Ансамбль траекторий</sub><br>
   <img src="simulation_results/4_200.png" style="width: 100%; max-width: 400px; display: block; margin: 5px auto;">
  </td>
  <td width="33%" align="center" valign="top" style="padding: 10px; vertical-align: top;">
   <b>Рисунок 12. max_steps = 300 (Неймана)</b><br>
   <sub>Тепловая карта</sub><br>
   <img src="simulation_results/4_300(2).png" style="width: 100%; max-width: 400px; display: block; margin: 5px auto;"><br>
   <sub>Ансамбль траекторий</sub><br>
   <img src="simulation_results/4_300.png" style="width: 100%; max-width: 400px; display: block; margin: 5px auto;">
  </td>
 </tr>
</table>

<hr>

<h3>Случай 3. Дрейф к центру (уменьшение вероятности удаления)</h3>
<table style="border-collapse: collapse; width: 100%; margin-bottom: 20px;">
 <!-- Окрестность Мура -->
 <tr>
  <td width="33%" align="center" valign="top" style="padding: 10px; vertical-align: top;">
   <b>Рисунок 13. Дрейф 1% (Мура)</b><br>
   <sub>Тепловая карта</sub><br>
   <img src="simulation_results/5_1(2).png" style="width: 100%; max-width: 400px; display: block; margin: 5px auto;"><br>
   <sub>Ансамбль траекторий</sub><br>
   <img src="simulation_results/5_1.png" style="width: 100%; max-width: 400px; display: block; margin: 5px auto;">
  </td>
  <td width="33%" align="center" valign="top" style="padding: 10px; vertical-align: top;">
   <b>Рисунок 14. Дрейф 2% (Мура)</b><br>
   <sub>Тепловая карта</sub><br>
   <img src="simulation_results/5_2(2).png" style="width: 100%; max-width: 400px; display: block; margin: 5px auto;"><br>
   <sub>Ансамбль траекторий</sub><br>
   <img src="simulation_results/5_2.png" style="width: 100%; max-width: 400px; display: block; margin: 5px auto;">
  </td>
  <td width="33%" align="center" valign="top" style="padding: 10px; vertical-align: top;">
   <b>Рисунок 15. Дрейф 5% (Мура)</b><br>
   <sub>Тепловая карта</sub><br>
   <img src="simulation_results/5_5(2).png" style="width: 100%; max-width: 400px; display: block; margin: 5px auto;"><br>
   <sub>Ансамбль траекторий</sub><br>
   <img src="simulation_results/5_5.png" style="width: 100%; max-width: 400px; display: block; margin: 5px auto;">
  </td>
 </tr>
 <!-- Окрестность Неймана -->
 <tr>
  <td width="33%" align="center" valign="top" style="padding: 10px; vertical-align: top;">
   <b>Рисунок 16. Дрейф 1% (Неймана)</b><br>
   <sub>Тепловая карта</sub><br>
   <img src="simulation_results/6_1(2).png" style="width: 100%; max-width: 400px; display: block; margin: 5px auto;"><br>
   <sub>Ансамбль траекторий</sub><br>
   <img src="simulation_results/6_1.png" style="width: 100%; max-width: 400px; display: block; margin: 5px auto;">
  </td>
  <td width="33%" align="center" valign="top" style="padding: 10px; vertical-align: top;">
   <b>Рисунок 17. Дрейф 2% (Неймана)</b><br>
   <sub>Тепловая карта</sub><br>
   <img src="simulation_results/6_2(2).png" style="width: 100%; max-width: 400px; display: block; margin: 5px auto;"><br>
   <sub>Ансамбль траекторий</sub><br>
   <img src="simulation_results/6_2.png" style="width: 100%; max-width: 400px; display: block; margin: 5px auto;">
  </td>
  <td width="33%" align="center" valign="top" style="padding: 10px; vertical-align: top;">
   <b>Рисунок 18. Дрейф 5% (Неймана)</b><br>
   <sub>Тепловая карта</sub><br>
   <img src="simulation_results/6_5(2).png" style="width: 100%; max-width: 400px; display: block; margin: 5px auto;"><br>
   <sub>Ансамбль траекторий</sub><br>
   <img src="simulation_results/6_5.png" style="width: 100%; max-width: 400px; display: block; margin: 5px auto;">
  </td>
 </tr>
</table>

<hr>

<h3>Случай 4. Дрейф от центра (увеличение вероятности удаления)</h3>
<table style="border-collapse: collapse; width: 100%; margin-bottom: 20px;">
 <!-- Окрестность Мура -->
 <tr>
  <td width="33%" align="center" valign="top" style="padding: 10px; vertical-align: top;">
   <b>Рисунок 19. Дрейф 1% (Мура)</b><br>
   <sub>Тепловая карта</sub><br>
   <img src="simulation_results/7_1(2).png" style="width: 100%; max-width: 400px; display: block; margin: 5px auto;"><br>
   <sub>Ансамбль траекторий</sub><br>
   <img src="simulation_results/7_1.png" style="width: 100%; max-width: 400px; display: block; margin: 5px auto;">
  </td>
  <td width="33%" align="center" valign="top" style="padding: 10px; vertical-align: top;">
   <b>Рисунок 20. Дрейф 2% (Мура)</b><br>
   <sub>Тепловая карта</sub><br>
   <img src="simulation_results/7_2(2).png" style="width: 100%; max-width: 400px; display: block; margin: 5px auto;"><br>
   <sub>Ансамбль траекторий</sub><br>
   <img src="simulation_results/7_2.png" style="width: 100%; max-width: 400px; display: block; margin: 5px auto;">
  </td>
  <td width="33%" align="center" valign="top" style="padding: 10px; vertical-align: top;">
   <b>Рисунок 21. Дрейф 5% (Мура)</b><br>
   <sub>Тепловая карта</sub><br>
   <img src="simulation_results/7_5(2).png" style="width: 100%; max-width: 400px; display: block; margin: 5px auto;"><br>
   <sub>Ансамбль траекторий</sub><br>
   <img src="simulation_results/7_5.png" style="width: 100%; max-width: 400px; display: block; margin: 5px auto;">
  </td>
 </tr>
 <!-- Окрестность Неймана -->
 <tr>
  <td width="33%" align="center" valign="top" style="padding: 10px; vertical-align: top;">
   <b>Рисунок 22. Дрейф 1% (Неймана)</b><br>
   <sub>Тепловая карта</sub><br>
   <img src="simulation_results/8_1(2).png" style="width: 100%; max-width: 400px; display: block; margin: 5px auto;"><br>
   <sub>Ансамбль траекторий</sub><br>
   <img src="simulation_results/8_1.png" style="width: 100%; max-width: 400px; display: block; margin: 5px auto;">
  </td>
  <td width="33%" align="center" valign="top" style="padding: 10px; vertical-align: top;">
   <b>Рисунок 23. Дрейф 2% (Неймана)</b><br>
   <sub>Тепловая карта</sub><br>
   <img src="simulation_results/8_2(2).png" style="width: 100%; max-width: 400px; display: block; margin: 5px auto;"><br>
   <sub>Ансамбль траекторий</sub><br>
   <img src="simulation_results/8_2.png" style="width: 100%; max-width: 400px; display: block; margin: 5px auto;">
  </td>
  <td width="33%" align="center" valign="top" style="padding: 10px; vertical-align: top;">
   <b>Рисунок 24. Дрейф 5% (Неймана)</b><br>
   <sub>Тепловая карта</sub><br>
   <img src="simulation_results/8_5(2).png" style="width: 100%; max-width: 400px; display: block; margin: 5px auto;"><br>
   <sub>Ансамбль траекторий</sub><br>
   <img src="simulation_results/8_5.png" style="width: 100%; max-width: 400px; display: block; margin: 5px auto;">
  </td>
 </tr>
</table>

