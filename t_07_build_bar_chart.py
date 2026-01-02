"""
Модуль для побудови графіка порівняння методу Монте-Карло з теорією.
"""
import matplotlib.pyplot as plt

def build_bar_chart(sums, mc_probs, theo_probs, filename = None):
    """
    Побудова графіка для порівняння методу Монте-Карло з теорією
    """
    plt.figure(figsize=(12, 7))  # Збільшимо розмір для кращої читабельності
    bars_mc = plt.bar([x - 0.2 for x in sums], mc_probs, width=0.4,
        label='Монте-Карло', color='skyblue', align='center')
    bars_theo = plt.bar([x + 0.2 for x in sums], theo_probs, width=0.4,
        label='Теорія', color='orange', align='center', alpha=0.7)

    # Додавання значень над барами
    for bar_element in bars_mc:
        yval = bar_element.get_height()
        plt.text(bar_element.get_x() + bar_element.get_width()/2, yval + 0.1,
            f'{yval:.4f}%', ha='center', va='bottom', fontsize=9, rotation=90)

    for bar_element in bars_theo:
        yval = bar_element.get_height()
        plt.text(bar_element.get_x() + bar_element.get_width()/2, yval + 0.1,
            f'{yval:.4f}%', ha='center', va='bottom', fontsize=9, rotation=90)

    # Set y-limit slightly higher to accommodate labels
    max_prob = max(mc_probs + theo_probs)
    plt.ylim(0, max_prob * 1.2)

    # Додавання легенди
    plt.xlabel('Сума на кубиках')
    plt.ylabel('Ймовірність (%)')
    plt.title('Порівняння методу Монте-Карло з теорією')
    plt.xticks(sums)
    plt.legend()
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    if filename:
        plt.savefig(filename)
    else:
        plt.show()
