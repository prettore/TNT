'''
Module that holds useful functions that are independent from the different classes like experiments or communication
scenarios.
'''

try:
    import seaborn as sns
    from collections import Counter
    import matplotlib.pyplot as plt
    import numpy as np
    import iteround as it
except:
    raise


def get_numeric_sequence(sequence):
    """
    Map kbps data rates to state numbers.
    :param sequence: sequence of states
    :return: list of state numbers
    """
    numbers = []
    counter = 0
    for state in sequence:
        if state == '0.0 kbps':
            numbers.append(0.0)
        elif state == '0.6 kbps':
            numbers.append(0.6)
        elif state == '1.2 kbps':
            numbers.append(1.2)
        elif state == '2.4 kbps':
            numbers.append(2.4)
        elif state == '4.8 kbps':
            numbers.append(4.8)
        elif state == '9.6 kbps':
            numbers.append(9.6)
        counter = counter + 1
    return numbers


def get_int_sequence(sequence):
    """
    Map kbps data rates to state numbers.
    :param sequence: sequence of states
    :return: list of state numbers
    """
    numbers = []
    counter = 0
    for state in sequence:
        if state == '0.0 kbps':
            numbers.append(0)
        elif state == '0.6 kbps':
            numbers.append(1)
        elif state == '1.2 kbps':
            numbers.append(2)
        elif state == '2.4 kbps':
            numbers.append(3)
        elif state == '4.8 kbps':
            numbers.append(4)
        elif state == '9.6 kbps':
            numbers.append(5)
        counter = counter + 1
    return numbers


def get_distribution_hist(sequence):
    """
    Calculate distribution of states in current sequence
    :param: sequence: sequence of states
    :return: list of probabilities
    """
    # create dict holding all the states and the number of occurencies
    cnt = Counter()
    for state in sequence:
        cnt[state] += 1

    # length of the sequence
    n = len(sequence)

    dist = []
    # create dist hist for the sequence
    for state in cnt:
        dist.append(cnt[state] / n)
    return dist


def plot_distribution_hist(sequence):
    """
    Plot distribution of states as histogram
    :param sequence: sequence of states
    """
    # Density Plot and Histogram of all arrival delays
    sns.histplot(sequence, kde=True, binwidth=3)
    plt.show()


def saferound_pdistr(A, n=6, precision=4):
    """
    Round probability distributions by keeping the sum of the entries to 1
    :param A: matrix holding 2D probability distributions
    :param n: dimension of the matrix
    :param precision: round precision
    :return: rounded probability distribution matrix
    """
    for i in range(n):
        A[i] = it.saferound(A[i], precision)
        A[i] = [abs(j) for j in A[i]]
    return A
