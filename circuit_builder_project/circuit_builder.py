import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Circle
import numpy as np
import re

from .drawers import (draw_resistor, draw_inductor, draw_capacitor,
                      draw_voltage_source, draw_current_source)


class CircuitBuilder:
    def __init__(self):
        self.elements = []
        self.node_positions = {}

    def add_element(self, id_num, node1, node2, el_type, value):
        """Добавление элемента: id, узел1, узел2, тип, значение"""
        self.elements.append({
            'id': id_num,
            'node1': node1,
            'node2': node2,
            'type': el_type,
            'value': value
        })

    def parse_element_type(self, type_str):
        """Распознавание типа элемента из строки"""
        type_str = type_str.strip().upper()

        # Источник напряжения
        if 'ИН' in type_str or 'U' in type_str.upper() or type_str.startswith('U'):
            return 'U'
        # Источник тока
        elif 'ИТ' in type_str or 'I' in type_str.upper() or type_str.startswith('I'):
            return 'I'
        # Резистор
        elif 'R' in type_str:
            return 'R'
        # Катушка индуктивности
        elif 'L' in type_str:
            return 'L'
        # Конденсатор
        elif 'C' in type_str:
            return 'C'
        else:
            # По умолчанию - резистор
            return 'R'

    def parse_from_input(self, input_str):
        """
        Парсинг ввода в различных форматах
        Примеры:
        "114 - ИН и = 2"
        "212 - R2 = 2"
        "324 - L3 = 2"
        "534-R5=2" (без пробелов)
        "643- ИТ і6 = 2"
        """
        # Очищаем строку
        input_str = input_str.strip()

        # Удаляем точку с запятой в конце, если есть
        if input_str.endswith(';'):
            input_str = input_str[:-1]

        # Разбиваем по '-'
        parts = input_str.split('-', 1)
        if len(parts) != 2:
            print(f"Ошибка парсинга: {input_str}")
            return False

        # Первая часть - тройка чисел
        triple = parts[0].strip()
        if len(triple) < 3:
            print(f"Ошибка: неверный формат тройки {triple}")
            return False

        try:
            id_num = int(triple[0])
            node1 = int(triple[1])
            node2 = int(triple[2])
        except:
            print(f"Ошибка: не удалось распознать номера {triple}")
            return False

        # Вторая часть - тип и значение
        type_value = parts[1].strip()

        # Разбиваем по '='
        if '=' in type_value:
            type_part, value_part = type_value.split('=', 1)

            # Определяем тип элемента
            el_type = self.parse_element_type(type_part)

            # Извлекаем значение
            try:
                value = float(value_part.strip())
            except:
                print(f"Предупреждение: не удалось распознать значение {value_part}, используется 0")
                value = 0.0
        else:
            # Если нет знака '=', то просто тип без значения
            el_type = self.parse_element_type(type_value)
            value = None  # Значение не указано

        self.add_element(id_num, node1, node2, el_type, value)
        return True

    def parse_circuit_string(self, circuit_str):
        """Парсинг строки с описанием всей цепи"""
        # Обновленный парсер с опциональным '-' для поддержки форматов вроде "134 i" или "324 - r"
        pattern = r'(\d{3})\s*(?:-)?\s*([^=;]+?)\s*(?:=\s*([^;]+?))?(?=;|\s*$|\s*\d{3})'
        matches = re.findall(pattern, circuit_str)

        success_count = 0
        for match in matches:
            triple = match[0]
            type_str = match[1].strip()
            value_str = match[2].strip() if match[2] else None

            try:
                id_num = int(triple[0])
                node1 = int(triple[1])
                node2 = int(triple[2])
                el_type = self.parse_element_type(type_str)
                value = float(value_str) if value_str else None
                self.add_element(id_num, node1, node2, el_type, value)
                success_count += 1
            except Exception as e:
                print(f"Ошибка парсинга элемента {match}: {e}")

        print(f"\nРаспознано элементов: {success_count} из {len(matches)}")
        return success_count > 0

    def calculate_node_positions(self):
        """Вычисление позиций узлов для строго прямоугольной схемы"""
        if not self.elements:
            return

        # Находим все уникальные узлы
        all_nodes = set()
        for el in self.elements:
            all_nodes.add(el['node1'])
            all_nodes.add(el['node2'])

        max_node = max(all_nodes)

        # Размещаем узлы: верхний ряд слева направо, нижний узел - земля
        node_spacing_x = 6.0
        node_spacing_y = 6.0

        # Определяем, какой узел является "землей" (нижним)
        ground_node = max_node

        # Верхние узлы располагаются слева направо
        upper_nodes = sorted([n for n in all_nodes if n != ground_node])

        # Позиционируем верхние узлы
        for i, node in enumerate(upper_nodes):
            self.node_positions[node] = (i * node_spacing_x, node_spacing_y)

        # Нижний узел (земля) располагается внизу по центру
        if len(upper_nodes) > 0:
            ground_x = (len(upper_nodes) - 1) * node_spacing_x / 2
        else:
            ground_x = 0

        self.node_positions[ground_node] = (ground_x, 0)

    def group_parallel_elements(self):
        """Группировка параллельных элементов (с общими двумя узлами)"""
        edge_groups = {}

        for el in self.elements:
            # Создаем ключ для пары узлов (нормализуем порядок)
            key = tuple(sorted([el['node1'], el['node2']]))

            if key not in edge_groups:
                edge_groups[key] = []
            edge_groups[key].append(el)

        return edge_groups

    def draw_circuit(self):
        """Построение схемы цепи"""
        if not self.elements:
            print("Нет элементов для отрисовки!")
            return

        self.calculate_node_positions()
        edge_groups = self.group_parallel_elements()

        fig, ax = plt.subplots(figsize=(16, 10))
        ax.set_aspect('equal')

        # Рисуем соединения
        for key, group in edge_groups.items():
            n1, n2 = key  # Уже отсортированы
            pos1 = self.node_positions[n1]
            pos2 = self.node_positions[n2]

            dx = pos2[0] - pos1[0]
            dy = pos2[1] - pos1[1]

            num_parallel = len(group)

            # Определяем, является ли это перемычкой (spanning) на горизонтальной линии
            spanning = False
            offset_base = 0.0
            if abs(dy) < 0.1 and abs(n2 - n1) > 1:  # Горизонтальное соединение через узлы
                spanning = True
                offset_base = 2.0  # Сдвиг вверх для перемычек

            for idx, element in enumerate(group):
                # Смещение для параллельных элементов с учетом базы для перемычек
                offset = offset_base + (idx - (num_parallel - 1) / 2) * 2

                # Определяем путь соединения
                if abs(dx) > 0.1 and abs(dy) > 0.1:
                    # Диагональное соединение - используем прямоугольный путь
                    intermediate_x = pos1[0] + offset
                    intermediate_y = pos2[1]

                    # Вертикальная линия с элементом на ней
                    vert_mid_y = (pos1[1] + intermediate_y) / 2
                    mid_x = intermediate_x
                    mid_y = vert_mid_y

                    element_offset = 0.7

                    # Горизонтальная линия от узла к вертикальной
                    ax.plot([pos1[0], intermediate_x], [pos1[1], pos1[1]],
                            'k-', linewidth=2.5, zorder=1)

                    # Вертикальная линия с элементом
                    ax.plot([intermediate_x, intermediate_x], [pos1[1], vert_mid_y - element_offset],
                            'k-', linewidth=2.5, zorder=1)
                    ax.plot([intermediate_x, intermediate_x], [vert_mid_y + element_offset, intermediate_y],
                            'k-', linewidth=2.5, zorder=1)

                    # Горизонтальная линия от вертикальной к узлу 2
                    ax.plot([intermediate_x, pos2[0]], [intermediate_y, pos2[1]],
                            'k-', linewidth=2.5, zorder=1)

                    angle = -np.pi / 2  # Вертикально вниз

                else:
                    # Прямое соединение (горизонтальное или вертикальное)
                    length = np.sqrt(dx ** 2 + dy ** 2)
                    if length == 0:
                        continue

                    ux, uy = dx / length, dy / length
                    perpx, perpy = -uy, ux

                    x1 = pos1[0] + perpx * offset
                    y1 = pos1[1] + perpy * offset
                    x2 = pos2[0] + perpx * offset
                    y2 = pos2[1] + perpy * offset

                    mid_x = (x1 + x2) / 2
                    mid_y = (y1 + y2) / 2

                    element_offset = 0.7

                    ax.plot([x1, mid_x - ux * element_offset], [y1, mid_y - uy * element_offset],
                            'k-', linewidth=2.5, zorder=1)
                    ax.plot([mid_x + ux * element_offset, x2], [mid_y + uy * element_offset, y2],
                            'k-', linewidth=2.5, zorder=1)

                    angle = np.arctan2(dy, dx)

                    # Добавляем соединительные линии от узлов к сдвинутой ветви, если есть смещение
                    if abs(offset) > 0.01:
                        ax.plot([pos1[0], x1], [pos1[1], y1], 'k-', linewidth=2.5, zorder=1)
                        ax.plot([pos2[0], x2], [pos2[1], y2], 'k-', linewidth=2.5, zorder=1)

                # Метка элемента
                label = f"{element['type']}{element['id']}"
                value = element['value']

                # Рисуем элемент (используем функции из drawers.py)
                if element['type'] == 'R':
                    draw_resistor(ax, mid_x, mid_y, angle, label, value)
                elif element['type'] == 'L':
                    draw_inductor(ax, mid_x, mid_y, angle, label, value)
                elif element['type'] == 'C':
                    draw_capacitor(ax, mid_x, mid_y, angle, label, value)
                elif element['type'] == 'U':
                    draw_voltage_source(ax, mid_x, mid_y, angle, label, value)
                elif element['type'] == 'I':
                    draw_current_source(ax, mid_x, mid_y, angle, label, value)

        # Рисуем узлы
        for node, pos in self.node_positions.items():
            circle = Circle(pos, 0.18, color='black', zorder=10)
            ax.add_patch(circle)

            # Номер узла в красном кружке
            node_label_circle = Circle((pos[0] - 0.6, pos[1] + 0.6), 0.3,
                                       color='white', edgecolor='red',
                                       linewidth=2.5, zorder=11)
            ax.add_patch(node_label_circle)
            ax.text(pos[0] - 0.6, pos[1] + 0.6, f'{node}', ha='center', va='center',
                    fontsize=11, weight='bold', color='red', zorder=12)

        ax.autoscale()
        ax.margins(0.25)
        ax.axis('off')
        ax.set_title('Схема электрической цепи', fontsize=16, weight='bold', pad=20)
        plt.tight_layout()
        plt.show()