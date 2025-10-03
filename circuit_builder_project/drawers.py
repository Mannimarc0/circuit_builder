import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, Circle, Arc
import numpy as np


def draw_resistor(ax, x_mid, y_mid, angle, label, value):
    """Рисование резистора"""
    width, height = 1.0, 0.4

    rect = FancyBboxPatch((x_mid - width / 2, y_mid - height / 2), width, height,
                          boxstyle="round,pad=0.02",
                          edgecolor='black', facecolor='white', linewidth=2.5)

    t = patches.transforms.Affine2D().rotate_around(x_mid, y_mid, angle) + ax.transData
    rect.set_transform(t)
    ax.add_patch(rect)
    text_offset = 0.6
    offset_x = -np.sin(angle) * text_offset
    offset_y = np.cos(angle) * text_offset

    ax.text(x_mid + offset_x, y_mid + offset_y, label, ha='center', va='bottom',
            fontsize=10, weight='bold')
    if value is not None:
        ax.text(x_mid - offset_x, y_mid - offset_y, f'{value}Ω', ha='center', va='top',
                fontsize=9, color='blue')


def draw_inductor(ax, x_mid, y_mid, angle, label, value):
    """Рисование катушки индуктивности (спираль)"""
    n_loops = 4
    loop_width = 0.25
    total_width = n_loops * loop_width

    cos_a, sin_a = np.cos(angle), np.sin(angle)

    for i in range(n_loops):
        local_x = -total_width / 2 + i * loop_width + loop_width / 2
        center_x = x_mid + local_x * cos_a
        center_y = y_mid + local_x * sin_a

        arc = Arc((center_x, center_y), loop_width, 0.4,
                  angle=np.degrees(angle), theta1=0, theta2=180,
                  edgecolor='black', linewidth=2.5)
        ax.add_patch(arc)

    text_offset = 0.6
    offset_x = -np.sin(angle) * text_offset
    offset_y = np.cos(angle) * text_offset

    ax.text(x_mid + offset_x, y_mid + offset_y, label, ha='center', va='bottom',
            fontsize=10, weight='bold')
    if value is not None:
        ax.text(x_mid - offset_x, y_mid - offset_y, f'{value}H', ha='center', va='top',
                fontsize=9, color='blue')


def draw_capacitor(ax, x_mid, y_mid, angle, label, value):
    """Рисование конденсатора"""
    gap = 0.2
    height = 0.6

    cos_a, sin_a = np.cos(angle), np.sin(angle)

    # Первая пластина
    p1_x1 = x_mid - gap / 2 * cos_a - height / 2 * sin_a
    p1_y1 = y_mid - gap / 2 * sin_a + height / 2 * cos_a
    p1_x2 = x_mid - gap / 2 * cos_a + height / 2 * sin_a
    p1_y2 = y_mid - gap / 2 * sin_a - height / 2 * cos_a

    # Вторая пластина
    p2_x1 = x_mid + gap / 2 * cos_a - height / 2 * sin_a
    p2_y1 = y_mid + gap / 2 * sin_a + height / 2 * cos_a
    p2_x2 = x_mid + gap / 2 * cos_a + height / 2 * sin_a
    p2_y2 = y_mid + gap / 2 * sin_a - height / 2 * cos_a

    ax.plot([p1_x1, p1_x2], [p1_y1, p1_y2], 'k-', linewidth=3)
    ax.plot([p2_x1, p2_x2], [p2_y1, p2_y2], 'k-', linewidth=3)

    text_offset = 0.6
    offset_x = -np.sin(angle) * text_offset
    offset_y = np.cos(angle) * text_offset

    ax.text(x_mid + offset_x, y_mid + offset_y, label, ha='center', va='bottom',
            fontsize=10, weight='bold')
    if value is not None:
        ax.text(x_mid - offset_x, y_mid - offset_y, f'{value}F', ha='center', va='top',
                fontsize=9, color='blue')


def draw_voltage_source(ax, x_mid, y_mid, angle, label, value):
    """Рисование источника напряжения"""
    radius = 0.5
    circle = Circle((x_mid, y_mid), radius, edgecolor='black',
                    facecolor='white', linewidth=2.5, zorder=5)
    ax.add_patch(circle)

    sign_size = 0.18
    ax.plot([x_mid - sign_size, x_mid + sign_size], [y_mid, y_mid],
            'k-', linewidth=2.5)
    ax.plot([x_mid, x_mid], [y_mid - sign_size, y_mid + sign_size],
            'k-', linewidth=2.5)

    text_offset = 0.8
    offset_x = -np.sin(angle) * text_offset
    offset_y = np.cos(angle) * text_offset

    ax.text(x_mid + offset_x, y_mid + offset_y, label, ha='center', va='bottom',
            fontsize=10, weight='bold')
    if value is not None:
        ax.text(x_mid - offset_x, y_mid - offset_y, f'{value}V', ha='center', va='top',
                fontsize=9, color='blue')


def draw_current_source(ax, x_mid, y_mid, angle, label, value):
    """Рисование источника тока"""
    radius = 0.5
    circle = Circle((x_mid, y_mid), radius, edgecolor='black',
                    facecolor='white', linewidth=2.5, zorder=5)
    ax.add_patch(circle)

    arrow_len = 0.28
    cos_a, sin_a = np.cos(angle), np.sin(angle)

    ax.annotate('',
                xy=(x_mid + arrow_len * cos_a, y_mid + arrow_len * sin_a),
                xytext=(x_mid - arrow_len * cos_a, y_mid - arrow_len * sin_a),
                arrowprops=dict(arrowstyle='->', lw=2.5, color='black'))

    text_offset = 0.8
    offset_x = -np.sin(angle) * text_offset
    offset_y = np.cos(angle) * text_offset

    ax.text(x_mid + offset_x, y_mid + offset_y, label, ha='center', va='bottom',
            fontsize=10, weight='bold')
    if value is not None:
        ax.text(x_mid - offset_x, y_mid - offset_y, f'{value}A', ha='center', va='top',
                fontsize=9, color='blue')