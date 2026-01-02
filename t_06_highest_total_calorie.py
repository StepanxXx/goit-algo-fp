"""
Module for solving the highest calorie selection problem using
Greedy Algorithm and Dynamic Programming (Unbounded Knapsack).
"""
from collections import defaultdict


def greedy_algorithm(products_dict: dict[str, dict[str, int]], budget: int) -> dict[str, int]:
    """
    Selects items greedily to maximize calories without exceeding the budget.
    """
    list_items = sorted(
        [item for item in products_dict.items()],
        key=lambda x: x[1]['calories'] / x[1]['cost'],
        reverse=True
    )
    result = {}
    for item in list_items:
        if budget < item[1]['cost']:
            continue
        product_count = budget // item[1]['cost']
        result[item[0]] = product_count
        budget -= item[1]['cost'] * product_count
        if budget == 0:
            break
    return result

def dynamic_programming(products_dict: dict[str, dict[str, int]], budget: int) -> dict[str, int]:
    """
    Calculates the optimal set of items to maximize calories for a given budget
    using the Unbounded Knapsack dynamic programming algorithm.
    """
    # Підготовка даних: перетворюємо словник у список for зручності
    products = []
    for name, data in products_dict.items():
        products.append({
            'name': name,
            'cost': data['cost'],
            'calories': data['calories']
        })

    # dp[i] буде зберігати максимальну калорійність для бюджету i
    dp = [0] * (budget + 1)
    # item_tracker[i] буде зберігати індекс товару, який ми додали, щоб отримати dp[i]
    item_tracker = [-1] * (budget + 1)

    # Заповнюємо таблицю DP
    for i in range(1, budget + 1):
        for idx, product in enumerate(products):
            if product['cost'] <= i:
                # Якщо ми додамо цей продукт, яка буде загальна калорійність?
                # current_calories = калорії від решти бюджету + калорії цього продукту
                if dp[i - product['cost']] + product['calories'] > dp[i]:
                    dp[i] = dp[i - product['cost']] + product['calories']
                    item_tracker[i] = idx

    # Відновлення результату (які товари ми взяли)
    result = defaultdict(int)
    current_budget = budget

    # Поки ми не дійдемо до бюджету 0 або не знайдемо, що нічого не було додано
    while current_budget > 0 and item_tracker[current_budget] != -1:
        product_idx = item_tracker[current_budget]
        product = products[product_idx]
        result[product['name']] += 1
        current_budget -= product['cost']

    return dict(result)



if __name__ == "__main__":
    items = {
        "pizza": {"cost": 50, "calories": 300},
        "hamburger": {"cost": 40, "calories": 250},
        "hot-dog": {"cost": 30, "calories": 200},
        "pepsi": {"cost": 10, "calories": 100},
        "cola": {"cost": 15, "calories": 220},
        "potato": {"cost": 25, "calories": 350}
    }

    AMOUNT = 2450

    greedy_result = greedy_algorithm(items, AMOUNT)
    dp_result = dynamic_programming(items, AMOUNT)

    print(f"greedy_algorithm {AMOUNT} budget:", greedy_result, "=",
        sum(
            [items[product]['calories'] * count
            for product, count in greedy_result.items()]
        ), "calories")

    print(f"dynamic_programming {AMOUNT} budget:", dp_result, "=",
        sum(
            [items[product]['calories'] * count
            for product, count in dp_result.items()]
        ), "calories")
