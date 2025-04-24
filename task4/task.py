import math
from collections import Counter

def compute_probabilities(data):
    total = sum(data.values())
    return {k: v / total for k, v in data.items()}


def compute_entropy(probabilities):
    return -sum(p * math.log2(p) for p in probabilities.values() if p > 0)


def build_matrix(data):
    count = Counter(data)
    return compute_probabilities(count)


def main():
    possible_rolls = [(i, j) for i in range(1, 7) for j in range(1, 7)]

    sum_values = [sum(roll) for roll in possible_rolls]
    P_A = build_matrix(sum_values)

    product_values = [roll[0] * roll[1] for roll in possible_rolls]
    P_B = build_matrix(product_values)

    joint_events = [(sum_val, prod_val) for sum_val, prod_val in zip(sum_values, product_values)]
    P_AB = build_matrix(joint_events)

    H_A = compute_entropy(P_A)
    H_B = compute_entropy(P_B)
    H_AB = compute_entropy(P_AB)

    Ha_B = H_AB - H_A  # H(B|A) = H(AB) - H(A)
    I_A_B = H_A + H_B - H_AB  # I(A, B) = H(A) + H(B) - H(AB)

    result = [H_AB, H_A, H_B, Ha_B, I_A_B]
    print(', '.join([f'{x:.2f}' for x in result]))


if __name__ == "__main__":
    main()
