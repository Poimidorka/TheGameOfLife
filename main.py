class Cell(object):
    x: int
    y: int

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def is_neighbour(self, other):
        return abs(self.x - other.x) <= 1 and abs(self.y - other.y) <= 1

    def copy(self):
        return Cell(self.x, self.y)

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))


def neighbour_list(x, y):
    neighbours = list()
    for i in range(x - 1, x + 2):
        for j in range(y - 1, y + 2):
            if i == x and j == y:
                continue
            neighbours.append(Cell(i, j))
    return neighbours


class Pole(object):
    __alive: set
    __c1: Cell
    __c2: Cell
    __epoch: int

    def __init__(self, alive, c1, c2):
        self.__epoch = 0
        self.__alive = alive
        self.__c1 = c1
        self.__c2 = c2

    def __count_neighbours(self, x, y):
        counter = 0
        neighbours = neighbour_list(x, y)
        for elem in neighbours:
            counter += (elem in self.__alive)
        return counter

    def next_epoch(self):
        epoch = self.__epoch + 1
        new_set = set()
        for el in self.__alive:
            if 2 <= self.__count_neighbours(el.x, el.y) <= 3:
                new_set.add(el)
            for neighbour in neighbour_list(el.x, el.y):
                if self.__count_neighbours(neighbour.x, neighbour.y) == 3 and neighbour not in self.__alive:
                    new_set.add(neighbour)
        self.__init__(new_set, self.__c1, self.__c2)
        self.__epoch = epoch

    def display(self):
        print("Epoch #", end="")
        print(self.__epoch)
        for i in range(min(self.__c1.x, self.__c2.x), max(self.__c1.x, self.__c2.x) + 1):
            for j in range(min(self.__c1.y, self.__c2.y), max(self.__c1.y, self.__c2.y) + 1):
                symbol = "."
                if Cell(i, j) in self.__alive:
                    symbol = "#"
                print(symbol, end="")
            print()
        print()


def read_str():
    try:
        s = input()
        return s
    except EOFError:
        print("Error of reading")
        exit(0)


def read_int():
    try:
        n = int(read_str())
        return n
    except ValueError:
        print("Error of reading")
        exit(0)


class Game:
    __eras: int
    __pole: Pole

    def __init__(self):
        print("Enter the number of living cells")
        n = int(input())
        print("Enter the coordinates of cells (2 integers in ", end="")
        print(n, "rows)")
        alive = set()
        for i in range(n):
            x, y = map(int, input().split())
            alive.add(Cell(x, y))
        c1 = Cell()
        c2 = Cell()
        print("Enter the coordinates of two opposite corners of the rectangle (2 integers in 2 rows)")
        c1.x, c1.y = map(int, input().split())
        c2.x, c2.y = map(int, input().split())
        self.__pole = Pole(alive, c1, c2)
        self.__pole.display()
        print("Enter the number of eras you want to see")
        self.__eras = int(input())

    def play(self):
        for era in range(self.__eras):
            self.__pole.next_epoch()
            self.__pole.display()


def main():
    print("This is The Game of Life")
    game = Game()
    game.play()


if __name__ == '__main__':
    main()
