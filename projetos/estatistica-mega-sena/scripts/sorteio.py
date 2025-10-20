import random

def rando(it, r):
    pool = tuple(it)
    n = len(pool)
    indices = sorted(random.sample(range(n), r))
    return tuple(pool[i] for i in indices)


if __init__ == "__main__":
    print(rando())
