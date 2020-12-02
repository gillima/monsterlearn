import tkinter as tk

import click
from PIL import ImageTk, Image

from exercises import *


class Monster:
    def __init__(self, root, exercise, **kwargs):
        self._root = root
        self._handicap = kwargs.get('handicap', 500)
        self._exercise = exercise
        self.game_state = None
        self._reset()

    def start(self):
        if self._game_running:
            return
        if self._game_over:
            self._reset()
        self._tick()
        self._game_running = True

    def try_result(self, value):
        try:
            if self._exercise.try_result(value):
                self.player += 30
                return True
            return False
        finally:
            self._raise_state('exercise', '')

    @property
    def result_width(self):
        return self._exercise.result_width

    @property
    def exercise(self):
        return self._exercise.current

    @property
    def monster(self):
        return self._monster

    @monster.setter
    def monster(self, value):
        self._monster = value
        self._raise_state('moved', 'monster', x=value)

    @property
    def player(self):
        return self._player

    @player.setter
    def player(self, value):
        self._player = value
        self._raise_state('moved', 'player', x=value)

    @property
    def castle(self):
        return self._castle

    @castle.setter
    def castle(self, value):
        self._castle = value

    def _reset(self):
        self._monster = 0
        self._player = self._handicap
        self._castle = 1000
        self._game_over = False
        self._game_running = False
        self._raise_state('reset', '')

    def _raise_state(self, event, source, *args, **kwargs):
        if not self.game_state:
            return
        self.game_state(event, source, *args, **kwargs)

    def _check(self):
        if self._monster >= self._player:
            self._game_over = True
            self._game_running = False
            self._handicap = min(900, self._handicap + 50)
            self._raise_state('wins', 'monster')
        if self._player >= self._castle:
            self._game_over = True
            self._game_running = False
            self._handicap = max(100, self._handicap - 50)
            self._raise_state('wins', 'player')

    def _tick(self):
        self.monster += 1
        self._check()
        if not self._game_over:
            self._root.after(100, self._tick)


class Sprite:
    def __init__(self, canvas, source, x=0, offset=(0, 0), visible=True):
        self._canvas = canvas
        self._offset = offset if isinstance(offset, (list, set, tuple)) else (offset, 0)
        self._sprite = self._create_image(source)
        self.visible = visible
        self.x = x

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value
        self._canvas.coords(self._sprite, self._x + self._offset[0], self._y + self._offset[1])

    @property
    def visible(self):
        return self._visible

    @visible.setter
    def visible(self, value):
        self._visible = value
        self._canvas.itemconfigure(self._sprite, state='normal' if value else 'hidden')

    def _create_image(self, source):
        raw_image = Image.open(source)
        raw_image = raw_image.resize((raw_image.width // 2, raw_image.height // 2), Image.ANTIALIAS)
        self._photo_image = ImageTk.PhotoImage(raw_image)
        image = self._canvas.create_image(0, 0, anchor=tk.NW, image=self._photo_image)
        self._y = self._canvas.winfo_reqheight() - raw_image.height
        return image


class Ui(tk.Frame):
    font_size = 50

    def __init__(self, game, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.master.title('Monster 1x1')
        self.pack(fill=tk.BOTH, expand=0)

        self._canvas = tk.Canvas(self, bg='white', width=self.winfo_reqwidth(), height=500)
        self._canvas.pack()

        self._interact = tk.Frame(self, width=self.winfo_reqwidth())
        self._interact.pack(padx=10, pady=10, expand=1)

        self._exercise = tk.Label(self._interact, text='')
        self._exercise.config(font=('bold', Ui.font_size))
        self._exercise.pack(side=tk.LEFT)

        self._input = tk.Entry(self._interact, width=game.result_width)
        self._input.config(font=('normal', Ui.font_size))
        self._input.pack(side=tk.LEFT)

        self._init_sprites()

        self._game = game
        self._game.game_state = self._on_game_state
        self._input.bind("<Return>", self._verify)
        self._input.bind("<KP_Enter>", self._verify)

        self._reset()

    def _verify(self, event):
        self._game.start()
        self._game.try_result(self._input.get())
        self._input.select_range(0, 'end')
        return True

    def _init_sprites(self):
        self._ground = [
            Sprite(self._canvas, 'resources/ground.png', x=pos * 400, offset=(0, 10))
            for pos in range(0, 5)
        ]
        self._cactus = [
            Sprite(self._canvas, 'resources/cactus.png', x=pos, offset=(0, -35))
            for pos in [120, 760, 1100, 1650]
        ]
        self._bushes = [
            Sprite(self._canvas, 'resources/bush.png', x=pos, offset=(0, -35))
            for pos in [20, 350, 700, 945, 1775]
        ]

        self._castle = Sprite(self._canvas, 'resources/castle_open.png', offset=(220, -30))
        self._player = Sprite(self._canvas, 'resources/player.png', x=0, offset=(350, -30))
        self._player_wins = Sprite(self._canvas, 'resources/castle_closed.png', offset=(220, -30), visible=False)
        self._monster = Sprite(self._canvas, 'resources/monster.png', x=0, offset=(20, -30))
        self._monster_wins = Sprite(self._canvas, 'resources/monster_wins.png', x=0, offset=(20, -30), visible=False)

    def _reset(self):
        self._monster.x = self._game.monster
        self._player.x = self._game.player
        self._player_wins.x = self._game.castle
        self._castle.x = self._game.castle
        self._monster.visible = True
        self._monster_wins.visible = False
        self._player.visible = True
        self._player_wins.visible = False
        self._exercise.config(text=f'{self._game.exercise} ')

    def _on_game_state(self, event, source, *args, **kwargs):
        if event == 'moved':
            if source == 'monster':
                self._monster.x = kwargs.get('x')
            if source == 'player':
                self._player.x = kwargs.get('x')
        elif event == 'wins':
            self._player.visible = False
            self._monster.visible = source != 'monster'
            self._monster_wins.x = self._monster.x
            self._monster_wins.visible = source == 'monster'
            self._player_wins.visible = source == 'player'
        elif event == 'reset':
            self._reset()
        elif event == 'exercise':
            self._exercise.config(text=f'{self._game.exercise} ')


def run(exercise):
    root = tk.Tk()
    # exercise = SimpleMultiplication()
    # exercise = ReadNumbers()
    game = Monster(root, exercise)
    ui = Ui(game, root, width=1920, height=768)
    root.mainloop()


@click.command(help='Use addition to fill up to the target value')
@click.argument('target', default=1000, type=int)
def fill(target):
    exercise = FillMeUp(target=target)
    run(exercise)


@click.command(help='Simple multiplication in the range from 1..10')
def multiplication():
    exercise = SimpleMultiplication()
    run(exercise)


@click.command(help='Read written numbers')
def read_numbers():
    exercise = ReadNumbers()
    run(exercise)


@click.group()
def exercises():
  pass


exercises.add_command(fill)
exercises.add_command(multiplication)
exercises.add_command(read_numbers)


if __name__ == '__main__':
    exercises()
