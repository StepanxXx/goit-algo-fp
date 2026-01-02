"""
Моделювання кидання двох кубиків методом Монте-Карло.
"""
import random
from t_07_build_bar_chart import build_bar_chart

def monte_carlo_dice_simulation(num_simulations=100000):
    """
    Симуляція кидання двох кубиків методом Монте-Карло.

    Args:
        num_simulations: кількість симуляцій (за замовчуванням 100000)

    Returns:
        tuple: діапазон сум, ймовірності МК, теоретичні ймовірності
    """
    # Ініціалізація лічильника для сум від 2 до 12
    counts = {s: 0 for s in range(2, 13)}

    # Процес симуляції
    for _ in range(num_simulations):
        die1 = random.randint(1, 6)
        die2 = random.randint(1, 6)
        total_sum = die1 + die2
        counts[total_sum] += 1

    # Теоретичні ймовірності (кількість сприятливих подій / 36)
    # Сума: кількість комбінацій
    combinations = {
        2: 1, 3: 2, 4: 3, 5: 4, 6: 5,
        7: 6,
        8: 5, 9: 4, 10: 3, 11: 2, 12: 1
    }

    print(
        f"{'Сума':<5} | {'К-сть випадінь':<15} | "
        f"{'Монте-Карло (%)':<15} | {'Теорія (%)':<13} | {'Різниця (%)':<12}"
    )
    print("-" * 70)

    results_mc = []
    results_theo = []
    sum_range = range(2, 13)

    for s in sum_range:
        # Експериментальна ймовірність
        prob_mc = (counts[s] / num_simulations) * 100
        results_mc.append(prob_mc)

        # Теоретична ймовірність
        prob_theo = (combinations[s] / 36) * 100
        results_theo.append(prob_theo)

        diff = abs(prob_mc - prob_theo)

        theoretical = f"{prob_theo:<.2f} ({combinations[s]}/36)"
        print(
            f"{s:<5} | {counts[s]:<15} | {prob_mc:<15.2f} | "
            f"{theoretical:<13} | {diff:<12.3f}"
        )

    return sum_range, results_mc, results_theo

# Запуск симуляції (наприклад, 1 мільйон кидків)
sum_values, mc_probs, theo_probs = monte_carlo_dice_simulation(1_000_000)

# --- Побудова графіка (опціонально) ---
build_bar_chart(sum_values, mc_probs, theo_probs)
