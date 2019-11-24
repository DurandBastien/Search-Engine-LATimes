import heapq


class PQNode:

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.freq = 0

    def access(self):
        self.freq += 1

    def __lt__(self, other):
        return self.value < other.value

    def __str__(self):
        return str("{} : {}".format(self.key, self.value))

    def __eq__(self, other):
        return self.key == other.key and self.value == other.value



