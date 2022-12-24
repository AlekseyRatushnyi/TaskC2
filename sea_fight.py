import random
import sys


class Error(Exception):
    pass


class BoardOutException(Error):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message


class Dot:
    empty_cell = '○'
    ship_cell = '▮'
    destroyed_ship = 'X'
    damaged_ship = '▯'
    miss_cell = 'T'

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def check_point(z):
        if 1 <= z <= 6:
            return True
        else:
            return False

    @property
    def point_x(self):
        return self.x

    @point_x.setter
    def point_x(self, new_x):
        if Dot.check_point(new_x):
            self.x = new_x
        else:
            print('Значение некорректно')

    @property
    def point_y(self):
        return self.y

    @point_y.setter
    def point_y(self, new_y):
        if Dot.check_point(new_y):
            self.y = new_y
        else:
            print('Значение некорректно')

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f'Dot:{self.x, self.y}'


class Ship:

    def __init__(self, length, x, y, direction):

        self.size = length
        self.life = length
        self.x = x
        self.y = y
        self.direction = direction
        self.set_direction(direction)

    def __str__(self):
        return Dot.ship_cell

    def set_position(self, x, y, d):
        self.x = x
        self.y = y
        self.set_direction(d)

    def set_direction(self, d):

        self.direction = d

        if self.direction == 0:
            self.width = self.size
            self.height = 1
        elif self.direction == 1:
            self.width = 1
            self.height = self.size
        elif self.direction == 2:
            self.y = self.y - self.size + 1
            self.width = self.size
            self.height = 1
        elif self.direction == 3:
            self.x = self.x - self.size + 1
            self.width = 1
            self.height = self.size


class Board:
    X = ("1", "2", "3", "4", "5", "6")
    list_ships = [3, 2, 2, 1, 1, 1, 1]
    field_size = 6
    main = 'map'
    enemy = 'enemy'

    def __init__(self):
        self.map = [[Dot.empty_cell for i in range(6)] for i in range(6)]
        self.enemy = [[Dot.empty_cell for i in range(6)] for i in range(6)]

    def get_field_part(self, element):
        if element == Board.main:
            return self.map
        if element == Board.enemy:
            return self.enemy

    def draw_field(self, element):
        field = self.get_field_part(element)
        print("    | 1 |  2 |  3 |  4 | 5 |  6 |")
        for x in range(0, 6):
            for y in range(-1, 6):
                if y == -1:
                    print("   " + Board.X[x] + "|", end='')
                    continue
                print(" " + str(field[x][y]) + " |", end='')
            print("")
        print("")

    def check_ship(self, ship, element):
        field = self.get_field_part(element)
        if ship.x + ship.height - 1 >= 6 or ship.x < 0 or ship.y + ship.width - 1 >= 6 or ship.y < 0:
            return False
        x = ship.x
        y = ship.y
        width = ship.width
        height = ship.height

        for p_x in range(x, x + height):
            for p_y in range(y, y + width):
                if str(field[p_x][p_y]) == Dot.miss_cell:
                    return False

        for p_x in range(x - 1, x + height + 1):
            for p_y in range(y - 1, y + width + 1):
                if p_x < 0 or p_x >= len(field) or p_y < 0 or p_y >= len(field):
                    continue
                if str(field[p_x][p_y]) in (Dot.ship_cell, Dot.destroyed_ship):
                    return False

        return True

    def contour(self, ship, element):

        field = self.get_field_part(element)

        x, y = ship.x, ship.y
        width, height = ship.width, ship.height

        for p_x in range(x - 1, x + height + 1):
            for p_y in range(y - 1, y + width + 1):
                if p_x < 0 or p_x >= len(field) or p_y < 0 or p_y >= len(field):
                    continue
                field[p_x][p_y] = Dot.miss_cell

        for p_x in range(x, x + height):
            for p_y in range(y, y + width):
                field[p_x][p_y] = Dot.destroyed_ship

    def add_ship_to_field(self, ship, element):

        field = self.get_field_part(element)

        x, y = ship.x, ship.y
        width, height = ship.width, ship.height

        for p_x in range(x, x + height):
            for p_y in range(y, y + width):
                field[p_x][p_y] = ship


class Game:

    def __init__(self):

        self.players = []
        self.current_player = None
        self.next_player = None
        self.status = 'prepare'
        self.attempt = 900

    @property
    def game_inf(self):
        return f'{self.players},{self.current_player},{self.next_player},{self.status} '

    def loop(self):

        if self.status == 'prepare' and len(self.players) == 2:
            self.status = 'in game'
            self.current_player = self.players[0]
            self.next_player = self.players[1]
            return True

        if self.status == 'in game' and len(self.next_player.ships) == 0:
            self.status = 'game over'
            return True

    def add_player(self, player):
        player.field = Board()
        player.enemy_ships = list(Board.list_ships)
        self.random_board(player)
        self.players.append(player)

    def random_board(self, player):
        for i in Board.list_ships:
            ship = Ship(i, random.randint(0, 5), random.randint(0, 5), random.randint(0, 1))
            while True:
                player.message.clear()

                x, y, d = player.move('ship_setup')
                if x + y + d == 0:
                    continue
                ship.set_position(x, y, d)

                if player.field.check_ship(ship, Board.main):
                    player.field.add_ship_to_field(ship, Board.main)
                    player.ships.append(ship)
                    break
                self.attempt -= 1
                if self.attempt <= 0:
                    player.field.map = [[Dot.empty_cell for i in range(Board.field_size)] for i in
                                        range(Board.field_size)]
                    player.ships = []
                    try:
                        self.random_board(player)
                    except RecursionError:
                        print('Не удалось расставить корабли! Поробуйте ещё раз!')
                        break
                    return True

    def draw(self):
        if not self.current_player.hid:
            self.current_player.field.draw_field(Board.main)
            self.current_player.field.draw_field(Board.enemy)
        for line in self.current_player.message:
            print(line)

    def switch_players(self):
        self.current_player, self.next_player = self.next_player, self.current_player

    def greet(self):
        print("-" * 90)
        print("""        Приветствую! 
        Вы начинаете игру Морской бой с AI на поле размерностью 6x6.
        Цель игры: уничтожить все корабли противникa. Необходимо вводить координаты 
        предполагаемого места корабля противника через пробел от 1 до 6. 
        Удачи!
                """)
        print("-" * 90)

    def start(self):
        game.greet()
        while True:
            game.loop()
            if game.status == 'prepare':
                game.add_player(players.pop(0))

            if game.status == 'in game':
                game.current_player.message.append("Введите координаты через пробел от 1 до 6: ")
                game.draw()
                game.current_player.message.clear()
                shot_result = game.current_player.make_shot(game.next_player)
                if shot_result == 'miss':
                    game.next_player.message.append(f'{game.current_player.name} промахнулся')
                    game.next_player.message.append(f'{game.next_player.name} ходит')
                    game.switch_players()
                    continue
                elif shot_result == 'occuped':
                    game.current_player.message.append('Координата недоступна для выстрела, введите ещё раз!')
                    continue
                elif shot_result == 'out':
                    continue
                elif shot_result == 'get':
                    game.current_player.message.append('Есть попадание, введите координаты следующего выстрела!')
                    game.next_player.message.append('Наш корабль подбит!')
                    continue
                elif shot_result == 'kill':
                    game.current_player.message.append('Корабль противника уничтожен!')
                    game.next_player.message.append('Наш корабль уничтожен!')
                    continue

            if game.status == 'game over':
                game.next_player.field.draw_field(Board.main)
                game.current_player.field.draw_field(Board.main)
                print(f'{game.next_player.name} потерял последний корабль')
                print(f'{game.current_player.name} выиграл!')
                break


class Player:

    def __init__(self, name, hid):
        self.name = name
        self.hid = hid
        self.message = []
        self.ships = []
        self.enemy_ships = []
        self.field = None

    def move(self, input_type):

        if input_type == "ship_setup":
            return random.randint(0, 5), random.randint(0, 5), random.randint(0, 1)
        if input_type == "shot":
            if self.hid:
                AI.move(self, input_type)
            else:
                User.move(self, input_type)

    def make_shot(self, target_player):

        if self.hid:
            sx, sy = AI.move(self, 'shot')
        else:
            sx, sy = User.move(self, 'shot')

        if self.field.enemy[sx][sy] != Dot.empty_cell:
            return 'occuped'
        if sx + sy == -1:
            return 'out'
        shot_res = target_player.receive_shot((sx, sy))
        if shot_res == 'miss':
            self.field.enemy[sx][sy] = Dot.miss_cell
        if shot_res == 'get':
            self.field.enemy[sx][sy] = Dot.damaged_ship
        if type(shot_res) == Ship:
            destroyed_ship = shot_res
            self.field.contour(destroyed_ship, Board.enemy)
            self.enemy_ships.remove(destroyed_ship.size)
            shot_res = 'kill'

        return shot_res

    def receive_shot(self, shot):

        sx, sy = shot

        if type(self.field.map[sx][sy]) == Ship:
            ship = self.field.map[sx][sy]
            ship.life -= 1

            if ship.life <= 0:
                self.field.contour(ship, Board.main)
                self.ships.remove(ship)
                return ship

            self.field.map[sx][sy] = Dot.damaged_ship
            return 'get'

        else:
            self.field.map[sx][sy] = Dot.miss_cell
            return 'miss'


class AI(Player):
    def __init__(self, name, hid):
        super(AI, self).__init__(name, hid)

    def move(self, input_type):
        if input_type == "ship_setup":
            return random.randint(0, 5), random.randint(0, 5), random.randint(0, 1)
        if input_type == "shot":
            x, y = random.randint(0, 5), random.randint(0, 5)
        return x, y


class User(Player):
    def __init__(self, name, hid):
        super(AI, self).__init__(name, hid)

    def move(self, input_type):

        if input_type == "ship_setup":
            return random.randint(0, 5), random.randint(0, 5), random.randint(0, 1)
        if input_type == "shot":
            my_shot = list(input().split())

            if my_shot == "q":
                sys.exit('Выход!')
            try:
                x, y = my_shot[0], my_shot[1]
                if int(x) <= 0 or int(y) <= 0 or int(x) > 6 or int(y) > 6:
                    raise BoardOutException(f'{x, y}', ' ↑ Этот выстрел за пределами поля')
            except ValueError:
                e = 'Ошибка формата данных'
                game.current_player.message.append(e)
                return -1, 0
            except BoardOutException as e:
                game.current_player.message.append(e.expression)
                game.current_player.message.append(e.message)
                return -1, 0
            except IndexError:
                e = 'Ошибка формата данных'
                game.current_player.message.append(e)
                return -1, 0
            x = int(x) - 1
            y = int(y) - 1
            return x, y


class Ship:

    def __init__(self, size, x, y, rotation):

        self.size = size
        self.life = size
        self.x = x
        self.y = y
        self.rotation = rotation
        self.set_rotation(rotation)

    def __str__(self):
        return Dot.ship_cell

    def set_position(self, x, y, r):
        self.x = x
        self.y = y
        self.set_rotation(r)

    def set_rotation(self, r):

        self.rotation = r

        if self.rotation == 0:
            self.width = self.size
            self.height = 1
        elif self.rotation == 1:
            self.width = 1
            self.height = self.size
        elif self.rotation == 2:
            self.y = self.y - self.size + 1
            self.width = self.size
            self.height = 1
        elif self.rotation == 3:
            self.x = self.x - self.size + 1
            self.width = 1
            self.height = self.size

    def dots(self):
        pass


if __name__ == '__main__':
    players = []
    players.append(Player(name='I ', hid=False))
    players.append(Player(name='AI', hid=True))

    game = Game()
    game.start()
    print('Игра завершена!')
