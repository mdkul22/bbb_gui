from random import uniform, randint


def randgen():
    sensID = ['a', 'b', 'c', 'd']
    y = randint(0, 3)
    x = round(uniform(15, 20), 2)
    x = sensID[y] + str(x)
    return x

if __name__ == "__main__":
    randgen()
