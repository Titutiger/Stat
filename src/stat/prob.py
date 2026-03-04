# src/stat/prob.py

import math
from typing import List


class Prob:
    """
    A collection of core probability functions and distributions.
    """

    # =========================
    # Internal Utilities
    # =========================

    @staticmethod
    def _validate_prob(p: float) -> None:
        """Ensures a given probability is strictly between 0.0 and 1.0"""
        if not (0.0 <= p <= 1.0):
            raise ValueError(f"Probability must be between 0.0 and 1.0. Received: {p}")

    # =========================
    # Combinatorics
    # =========================

    @staticmethod
    def combinations(n: int, r: int) -> int:
        """
        Calculates nCr: The number of ways to choose 'r' items from 'n' items without replacement and where order DOES NOT matter.
        """
        if r > n or n < 0 or r < 0:
            raise ValueError("Invalid values for n and r. Ensure 0 <= r <= n.")
        return math.comb(n, r)

    comb = combinations
    ncr = combinations

    @staticmethod
    def permutations(n: int, r: int) -> int:
        """
        Calculates nPr: The number of ways to choose 'r' items from 'n' items without replacement and where order DOES matter.
        """
        if r > n or n < 0 or r < 0:
            raise ValueError("Invalid values for n and r. Ensure 0 <= r <= n.")
        return math.perm(n, r)

    perm = permutations
    npr = permutations

    # =========================
    # Probability Theorems
    # =========================

    @staticmethod
    def bayes(p_a: float, p_b_given_a: float, p_b: float) -> float:
        """
        Calculates Bayes' Theorem: P(A|B) = [P(B|A) * P(A)] / P(B)
        """
        Prob._validate_prob(p_a)
        Prob._validate_prob(p_b_given_a)
        Prob._validate_prob(p_b)

        if p_b == 0:
            raise ZeroDivisionError("The probability of event B (p_b) cannot be exactly 0.")

        return (p_b_given_a * p_a) / p_b

    @staticmethod
    def expected_value(values: List[float], probabilities: List[float]) -> float:
        """
        Calculates the Expected Value E[X] of a discrete random variable.
        """
        if len(values) != len(probabilities):
            raise ValueError("The number of values must match the number of probabilities.")

        for p in probabilities:
            Prob._validate_prob(p)

        # Using math.isclose to avoid floating point precision errors like 0.9999999999999999 != 1.0
        if not math.isclose(sum(probabilities), 1.0, rel_tol=1e-5):
            raise ValueError(f"Probabilities must sum to 1.0. Current sum: {sum(probabilities)}")

        return sum(v * p for v, p in zip(values, probabilities))

    # =========================
    # Distributions
    # =========================

    @staticmethod
    def binomial_pmf(n: int, k: int, p: float) -> float:
        """
        Probability Mass Function for the Binomial Distribution.
        Calculates the exact probability of getting 'k' successes in 'n' independent trials.
        """
        Prob._validate_prob(p)
        if k > n or n < 0 or k < 0:
            raise ValueError("Invalid values for n and k. Ensure 0 <= k <= n.")

        # Formula: nCr * (p^k) * (1-p)^(n-k)
        combinations = Prob.combinations(n, k)
        return combinations * (p ** k) * ((1 - p) ** (n - k))





if __name__ == '__main__':
    print(Prob.comb(5, 2))