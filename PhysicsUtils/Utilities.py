import random as rd

def get_random_colors(n):
    """This returns a list of n random hex colors."""
    color_list = []
    for _ in range(n):
        r = rd.randint(0, 5) * 0.2
        g = 1 - r
        color_list.append((r, g, rd.randint(0, 5) * 0.2, 1))
    return color_list