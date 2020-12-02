import random


class ReadNumbers:
    def __init__(self, **kwargs):
        self._exercise = []
        self._shuffle = kwargs.get('shuffle', True)
        self.reset()

    def reset(self):
        self._exercise.clear()
        self._exercise.append(('Eins',  1))
        self._exercise.append(('Zwei',  2))
        self._exercise.append(('Drei',  3))
        self._exercise.append(('Vier',  4))
        self._exercise.append(('Fünf',  5))
        self._exercise.append(('Sechs',  6))
        self._exercise.append(('Sieben',  7))
        self._exercise.append(('Acht',  8))
        self._exercise.append(('Neun',  9))
        if self._shuffle:
            random.shuffle(self._exercise)

    @property
    def current(self):
        return self._exercise[0][0]

    def try_result(self, value):
        try:
            if value == f'{self._exercise[0][1]}':
                self._exercise.pop(0)
                return True
            return False
        finally:
            if not self._exercise:
                self.reset()


class SimpleMultiplication:
    def __init__(self, **kwargs):
        self._exercise = []
        self._shuffle = kwargs.get('shuffle', True)
        self.reset()

    def reset(self):
        self._exercise.clear()
        for x in range(1, 10):
            for y in range(1, 11):
                self._exercise.append((f'{x} * {y}',  x * y))
        if self._shuffle:
            random.shuffle(self._exercise)

    @property
    def current(self):
        return self._exercise[0][0]

    def try_result(self, value):
        try:
            if value == f'{self._exercise[0][1]}':
                self._exercise.pop(0)
                return True
            return False
        finally:
            if not self._exercise:
                self.reset()