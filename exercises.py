import random


class BaseExercise:
    def __init__(self, **kwargs):
        self._exercise = []
        self._shuffle = kwargs.get('shuffle', True)
        self.reset()

    def reset(self):
        self._exercise = list(self._get_exercises())
        if self._shuffle:
            random.shuffle(self._exercise)

    def _get_exercises(self):
        raise Exception("Not implemented")

    @property
    def result_width(self):
        return 2

    @property
    def current(self):
        return self._exercise[0][0].strip()

    def try_result(self, value):
        try:
            if value.strip() == f'{self._exercise[0][1]}'.strip():
                self._exercise.pop(0)
                return True
            return False
        finally:
            if not self._exercise:
                self.reset()


class ReadNumbers(BaseExercise):
    def _get_exercises(self):
        yield 'Eins:',  1
        yield 'Zwei:',  2
        yield 'Drei:',  3
        yield 'Vier:',  4
        yield 'Fünf:',  5
        yield 'Sechs:',  6
        yield 'Sieben:',  7
        yield 'Acht:',  8
        yield 'Neun:',  9


class FillMeUp(BaseExercise):
    def __init__(self, **kwargs):
        self._target = kwargs.get('target')
        super().__init__(**kwargs)

    def _get_exercises(self):
        for x in range(100):
            number = random.randint(1, 999)
            yield f'{self._target} = {self._target - number} + ', number

    @property
    def result_width(self):
        return 3

class SimpleMultiplication(BaseExercise):
    def _get_exercises(self):
        for x in range(1, 10):
            for y in range(1, 11):
                yield f'{x} * {y} =',  x * y

