import random
import tqdm


def simulate():
    return sum(random.random() for i in tqdm.tqdm(range(100_000_000)))


if __name__ == "__main__":
    print(simulate())
