from kivy.config import Config
import numpy as np

Config.set("input", "mouse", "mouse,disable_multitouch")

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from kivy.properties import ListProperty, NumericProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.properties import BooleanProperty
from kivy.graphics import *

class MyScreenManager(ScreenManager):
    returned = False


class TopOfEverything(FloatLayout):
    window_size = [800, 600]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.keyboard_setup()
        Clock.schedule_once(self.after_init)
        Window.size = self.window_size

    def after_init(self, *args):
        pass

    def keyboard_setup(self, me=None, *args):
        # Keyboard for debug
        if me == None:
            me = self
        me._keyboard = Window.request_keyboard(me._keyboard_closed, me)
        me._keyboard.bind(on_key_down=me._on_keyboard_down)
        me._keyboard.bind(on_key_up=me._on_keyboard_up)
        self.key_pressed = None

    def _keyboard_closed(self):
        pass

    def _on_keyboard_up(self, keycode, text):
        pass

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        pass


class MyWidget(Widget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ClickableImage(ButtonBehavior, Image):
    selected = BooleanProperty(False)
    highlight_rect = None

    def highlight(self):
        if self.selected:
            self.canvas.remove(self.highlight_rect)
            self.highlight_rect = None
        else:
            with self.canvas:
                Color(.498, .149, 1, .3)
                self.highlight_rect = Rectangle(pos=self.pos, size=self.size)
        self.selected = not self.selected

    def on_release(self):
        super().on_release()
        self.highlight()

    pass


class Tile(ClickableImage):
    def __init__(self, tile_color, number, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tile_color = tile_color
        self.number = number

    def highlight(self):
        super().highlight()
        print(self.number)
    pass


class GameBoard(Screen):
    tiles_source = [
        "chess_images/square gray light _png_shadow_128px.png",
        "chess_images/square gray dark _png_shadow_128px.png"
    ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Clock.schedule_once(self.after_init)

    def after_init(self, *args):
        self.make_board()
        self.place_chess()

    def call_abs_coord(self, tile_x, tile_y):
        abs_coord = tile_x + (tile_y * 8)
        return abs_coord

    def make_board(self):
        board = self.ids.board
        tile_mod = 0
        for tile in range(64):
            tile_image = Tile(source=self.tiles_source[(tile + tile_mod) % 2],
                              allow_stretch=True,
                              keep_ratio=False,
                              number=tile,
                              tile_color=["white", "black"][(tile + tile_mod) % 2])
            tile_image.number = tile
            board.add_widget(tile_image)
            if tile % 8 == 7:
                tile_mod += 1

    black_pieces = {
        "pawn": "chess_images/b_pawn_png_shadow_128px.png",
        "rook": "chess_images/b_rook_png_shadow_128px.png",
        "knight": "chess_images/b_knight_png_shadow_128px.png",
        "bishop": "chess_images/b_bishop_png_shadow_128px.png",
        "king": "chess_images/b_king_png_shadow_128px.png",
        "queen": "chess_images/b_queen_png_shadow_128px.png"
    }
    white_pieces = {
        "pawn": "chess_images/w_pawn_png_shadow_128px.png",
        "rook": "chess_images/w_rook_png_shadow_128px.png",
        "knight": "chess_images/w_knight_png_shadow_128px.png",
        "bishop": "chess_images/w_bishop_png_shadow_128px.png",
        "queen": "chess_images/w_queen_png_shadow_128px.png",
        "king": "chess_images/w_king_png_shadow_128px.png"
    }
    opponent_pieces_dict = {
        "rook": [(0, 0), (7, 0)],
        "knight": [(1, 0), (6, 0)],
        "bishop": [(2, 0), (5, 0)],
        "queen": [(3, 0)],
        "king": [(4, 0)],
        "pawn": [(i, 1) for i in range(8)]
    }
    player_pieces_dict = {
        "rook": [(0, 7), (7, 7)],
        "knight": [(1, 7), (6, 7)],
        "bishop": [(2, 7), (5, 7)],
        "queen": [(3, 7)],
        "king": [(4, 7)],
        "pawn": [(i, 6) for i in range(8)]
    }

    # def piece_mov(self, coord_list, p_type):
    #     # Generates a list of tuples with the possible move coordinates (considers an empty board, the pieces which
    #     # prevents the movement to be done will be considered after
    #     move_list = []
    #     board_checker = Piece.position_tracking()
    #     piece_x = coord_list[0]
    #     piece_y = coord_list[1]
    #     if p_type == "pawn":
    #         if piece_y == 6:
    #             for p_mov in range(1, 3):
    #                 if board_checker[piece_y+p_mov][piece_x] == 0 or board_checker[piece_y+p_mov][piece_x] == 2:
    #                     move_list.append((piece_x, piece_y+p_mov))
    #         else:
    #             if board_checker[piece_y+1][piece_x] == 0 or board_checker[piece_y+1][piece_x] == 2:
    #                 move_list.append((piece_x, piece_y + 1))
    #
    #     # elif p_type == "rook":
    #     #     for x_r_axis in range(8):
    #     #         if board_checker[piece_y][x_r_axis] == 1 or board_checker[piece_y][x_r_axis] == 2:
    #     #             move_list.append((x_r_axis, piece_y))
    #     #         elif board_checker[piece_y][x_r_axis] == 0:
    #     #     for y_r_axis in range(8):
    #     #         if y_r_axis != piece_y:
    #     #             move_list.append((piece_x, y_r_axis))
    #
    #     elif p_type == "knight":
    #         # the if statements with range(8) check if the coordinate will be inside the board
    #         # the -2, 2 range refers to the x axis. When the knight moves +/-2 in X (if abs(x_kn) == 2:)
    #         # it moves +/-1 in Y
    #         # When it moves +/- 1 in X (elif abs(x_kn) == 1:)
    #         # then it moves +/- 2 in Y
    #         for x_kn in range(-2, 2):
    #             if x_kn + piece_x in range(8):
    #                 if abs(x_kn) == 2:
    #                     if piece_y + 1 in range(8):
    #                         move_list.append((piece_x+x_kn, piece_y+1))
    #                     elif piece_y - 1 in range(8):
    #                         move_list.append((piece_x+x_kn, piece_y-1))
    #                 elif abs(x_kn) == 1:
    #                     if piece_y + 2 in range(8):
    #                         move_list.append((piece_x+x_kn, piece_y+2))
    #                     elif piece_y - 2 in range(8):
    #                         move_list.append((piece_x+x_kn, piece_y-2))
    #
    #     elif p_type == "bishop":
    #         board_list = [(x, y) for x in range(8) for y in range(8)]
    #         for (x_b, y_b) in board_list:
    #             if abs(piece_x - abs(x_b)) == abs(piece_y - abs(y_b)) and (piece_x, piece_y) != (x_b, y_b):
    #                 move_list.append((x_b, y_b))
    #
    #     elif p_type == "queen":
    #         board_list = [(x, y) for x in range(8) for y in range(8)]
    #         for x_q_axis in range(8):
    #             if x_q_axis != piece_x:
    #                 move_list.append((x_q_axis, piece_y))
    #         for y_q_axis in range(8):
    #             if y_q_axis != piece_y:
    #                 move_list.append((piece_x, y_q_axis))
    #         for (x_q, y_q) in board_list:
    #             if piece_x - abs(x_q) == piece_y - abs(y_q) and (piece_x, piece_y) != (x_q, y_q):
    #                 move_list.append((x_q, y_q))
    #
    #     # else is king
    #     else:
    #         king_pre_list = list([(piece_x + 1, piece_y + move) for move in range(-1, 1)] +
    #                              [(piece_x - 1, piece_y + move) for move in range(-1, 1)] +
    #                              [(piece_x, piece_y + 1), (piece_x, piece_y - 1)])
    #         for (x_ki, y_ki) in king_pre_list:
    #             if x_ki and y_ki in range(8):
    #                 move_list.append((x_ki, y_ki))
    #     print(p_type)
    #     print(move_list)
    #     return move_list

    def place_chess(self):
        for piece_name, coordinates in self.opponent_pieces_dict.items():
            for coordinate in coordinates:
                # adds black pieces
                black_piece = Piece(source=self.black_pieces[piece_name],
                                    allow_stretch=True,
                                    keep_ratio=False,
                                    piece_color="black",
                                    coordinate=list(coordinate),
                                    piece_type=piece_name)
                tile_ind = self.call_abs_coord(list(coordinate)[0], list(coordinate)[1])
                self.ids.board.children[63-tile_ind].ids.anchor.add_widget(black_piece)
        for piece_name, coordinates in self.player_pieces_dict.items():
            for coordinate in coordinates:
                # adds white pieces
                white_piece = Piece(source=self.white_pieces[piece_name],
                                    allow_stretch=True,
                                    keep_ratio=False,
                                    piece_color="white",
                                    coordinate=list(coordinate),
                                    piece_type=piece_name)
                tile_ind = self.call_abs_coord(list(coordinate)[0], list(coordinate)[1])
                self.ids.board.children[63-tile_ind].ids.anchor.add_widget(white_piece)
                # self.ids.board.children's index is the reverse of tile_ind's, because the first tile generated is the
                #  last one in the GridLayout, while the matrix coordinates we use for organize the chessboard considers
                # the first left superior tile as the (0, 0) coordinate,
                # so: self.ids.board.children's index == 63 - tile_ind
            # troubleshooting
            # for ind, tile in enumerate(self.ids.board.children):
            #     print(ind, tile.number, end=' ')
            #     if len(tile.children[0].children) > 0:
            #         piece = tile.children[0].children[0]
            #         print(piece.piece_type, piece.piece_color, piece.coordinate)
            #     else:
            #         print()


class Piece(ClickableImage):
    piece_instances = []

    def __init__(self, piece_color, coordinate, piece_type, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.piece_instances.append(self)
        self.piece_color = piece_color
        self.coordinate = coordinate
        self.piece_type = piece_type

    def position_tracking(self):
        # makes an array which represents the empty (value = 0)  or the full tiles (white = 1 black = 2)
        pieces_pos = np.zeros((8, 8), dtype=int)
        for instance in Piece.piece_instances:
            if instance.piece_color == "white":
                pieces_pos[instance.coordinate[1]][instance.coordinate[0]] = 1
            if instance.piece_color == "black":
                pieces_pos[instance.coordinate[1]][instance.coordinate[0]] = 2
        print(pieces_pos)
        return pieces_pos

    def piece_mov(self):
        # Generates a list of tuples with the possible move coordinates (considers an empty board, the pieces which
        # prevents the movement to be done will be considered after
        move_list = []
        board_checker = self.position_tracking()
        piece_x = self.coordinate[0]
        piece_y = self.coordinate[1]
        if self.piece_type == "pawn":
            if piece_y == 6:
                for p_mov in range(1, 3):
                    if board_checker[piece_y - p_mov][piece_x] == 0:
                        move_list.append((piece_x, piece_y - p_mov))
                    if board_checker[piece_y - p_mov][piece_x] == 2:
                        move_list.append((piece_x, piece_y - p_mov))
                        break
            else:
                if board_checker[piece_y + 1][piece_x] == 0 or board_checker[piece_y + 1][piece_x] == 2:
                    move_list.append((piece_x, piece_y + 1))

        elif self.piece_type == "rook":
            for r_up in range(piece_y):
                if board_checker[piece_y - r_up][piece_x] == 0:
                    move_list.append((piece_x, piece_y - r_up))
                elif board_checker[piece_y - r_up][piece_x] == 2:
                    move_list.append((piece_x, piece_y - r_up))
                    break
                else:
                    break

            for r_down in range(7 - piece_y):
                if board_checker[piece_y + r_down][piece_x] == 0:
                    move_list.append((piece_x, piece_y + r_down))
                elif board_checker[piece_y + r_down][piece_x] == 2:
                    move_list.append((piece_x, piece_y + r_down))
                    break
                else:
                    break

            for r_left in range(piece_x):
                if board_checker[piece_y][piece_x - r_left] == 0:
                    move_list.append((piece_x - r_left, piece_y))
                elif board_checker[piece_y][piece_x - r_left] == 2:
                    move_list.append((piece_x - r_left, piece_y))
                    break
                else:
                    break

            for r_right in range(7 - piece_x):
                if board_checker[piece_y][piece_x + r_right] == 0:
                    move_list.append((r_right, piece_x + piece_y))
                elif board_checker[piece_y][piece_x + r_right] == 2:
                    move_list.append((piece_x + r_right, piece_y))
                    break
                else:
                    break

        elif self.piece_type == "knight":
            # the if statements with range(8) check if the coordinate will be inside the board
            # the -2, 2 range refers to the x axis. When the knight moves +/-2 in X (if abs(x_kn) == 2:)
            # it moves +/-1 in Y
            # When it moves +/- 1 in X (elif abs(x_kn) == 1:)
            # then it moves +/- 2 in Y
            for x_kn in range(-2, 3):
                if x_kn + piece_x in range(8):
                    if abs(x_kn) == 2:
                        if piece_y + 1 in range(8) and board_checker[piece_y+1][piece_x+x_kn] != 1:
                            move_list.append((piece_x+x_kn, piece_y+1))
                        elif piece_y - 1 in range(8) and board_checker[piece_y-1][piece_x+x_kn] != 1:
                            move_list.append((piece_x+x_kn, piece_y-1))
                    elif abs(x_kn) == 1:
                        if piece_y + 2 in range(8) and board_checker[piece_y+2][piece_x+x_kn] != 1:
                            move_list.append((piece_x+x_kn, piece_y+2))
                        elif piece_y - 2 in range(8) and board_checker[piece_y-2][piece_x+x_kn] != 1:
                            move_list.append((piece_x+x_kn, piece_y-2))

        elif self.piece_type == "bishop":
            # board_list = [(x, y) for x in range(8) for y in range(8)]
            # for (x_b, y_b) in board_list:
            #     if abs(piece_x - abs(x_b)) == abs(piece_y - abs(y_b)) and board_checker[y_b][x_b] != 1:
            #         move_list.append((x_b, y_b))
            for b_up_right in range(7 - piece_x):
                if b_up_right in range(piece_y):
                    if board_checker[piece_y - b_up_right][piece_x + b_up_right] == 0:
                        move_list.append((piece_x + b_up_right, piece_y - b_up_right))
                    if board_checker[piece_y - b_up_right][piece_x + b_up_right] == 2:
                        move_list.append((piece_x + b_up_right, piece_y - b_up_right))
                        break
                    else:
                        break

            for b_up_left in range(piece_x):
                if b_up_left in range(piece_y):
                    if board_checker[piece_y - b_up_left][piece_x - b_up_left] == 0:
                        move_list.append((piece_x - b_up_left, piece_y - b_up_left))
                    if board_checker[piece_y - b_up_left][piece_x + b_up_left] == 2:
                        move_list.append((piece_x - b_up_left, piece_y - b_up_left))
                        break
                    else:
                        break

            for b_down_right in range(7 - piece_x):
                if b_down_right in range(7 - piece_y):
                    if board_checker[piece_y + b_down_right][piece_x + b_down_right] == 0:
                        move_list.append((piece_x + b_down_right, piece_y + b_down_right))
                    if board_checker[piece_y + b_down_right][piece_x + b_down_right] == 2:
                        move_list.append((piece_x + b_down_right, piece_y + b_down_right))
                        break
                    else:
                        break

            for b_down_left in range(piece_x):
                if b_down_left in range(7 - piece_y):
                    if board_checker[piece_y + b_down_left][piece_x - b_down_left] == 0:
                        move_list.append((piece_x - b_down_left, piece_y + b_down_left))
                    if board_checker[piece_y + b_down_left][piece_x - b_down_left] == 2:
                        move_list.append((piece_x - b_down_left, piece_y + b_down_left))
                        break
                    else:
                        break

        # queen is bishop + rook
        elif self.piece_type == "queen":
            for q_up in range(piece_y):
                if board_checker[piece_y - q_up][piece_x] == 0:
                    move_list.append((piece_x, piece_y - q_up))
                elif board_checker[piece_y - q_up][piece_x] == 2:
                    move_list.append((piece_x, piece_y - q_up))
                    break
                else:
                    break

            for q_down in range(7 - piece_y):
                if board_checker[piece_y + q_down][piece_x] == 0:
                    move_list.append((piece_x, piece_y + q_down))
                elif board_checker[piece_y + q_down][piece_x] == 2:
                    move_list.append((piece_x, piece_y + q_down))
                    break
                else:
                    break

            for q_left in range(piece_x):
                if board_checker[piece_y][piece_x - q_left] == 0:
                    move_list.append((piece_x - q_left, piece_y))
                elif board_checker[piece_y][piece_x - q_left] == 2:
                    move_list.append((piece_x - q_left, piece_y))
                    break
                else:
                    break

            for q_right in range(7 - piece_x):
                if board_checker[piece_y][piece_x + q_right] == 0:
                    move_list.append((q_right, piece_x + piece_y))
                elif board_checker[piece_y][piece_x + q_right] == 2:
                    move_list.append((piece_x + q_right, piece_y))
                    break
                else:
                    break

            for q_up_right in range(7 - piece_x):
                if q_up_right in range(piece_y):
                    if board_checker[piece_y - q_up_right][piece_x + q_up_right] == 0:
                        move_list.append((piece_x + q_up_right, piece_y - q_up_right))
                    if board_checker[piece_y - q_up_right][piece_x + q_up_right] == 2:
                        move_list.append((piece_x + q_up_right, piece_y - q_up_right))
                        break
                    else:
                        break

            for q_up_left in range(piece_x):
                if q_up_left in range(piece_y):
                    if board_checker[piece_y - q_up_left][piece_x - q_up_left] == 0:
                        move_list.append((piece_x - q_up_left, piece_y - q_up_left))
                    if board_checker[piece_y - q_up_left][piece_x + q_up_left] == 2:
                        move_list.append((piece_x - q_up_left, piece_y - q_up_left))
                        break
                    else:
                        break

            for q_down_right in range(7 - piece_x):
                if q_down_right in range(7 - piece_y):
                    if board_checker[piece_y + q_down_right][piece_x + q_down_right] == 0:
                        move_list.append((piece_x + q_down_right, piece_y + q_down_right))
                    if board_checker[piece_y + q_down_right][piece_x + q_down_right] == 2:
                        move_list.append((piece_x + q_down_right, piece_y + q_down_right))
                        break
                    else:
                        break

            for q_down_left in range(piece_x):
                if q_down_left in range(7 - piece_y):
                    if board_checker[piece_y + q_down_left][piece_x - q_down_left] == 0:
                        move_list.append((piece_x - q_down_left, piece_y + q_down_left))
                    if board_checker[piece_y + q_down_left][piece_x - q_down_left] == 2:
                        move_list.append((piece_x - q_down_left, piece_y + q_down_left))
                        break
                    else:
                        break

        # else is king
        else:
            king_pre_list = list([(piece_x + 1, piece_y + move) for move in range(-1, 1)] +
                                 [(piece_x - 1, piece_y + move) for move in range(-1, 1)] +
                                 [(piece_x, piece_y + 1), (piece_x, piece_y - 1)])
            for (x_ki, y_ki) in king_pre_list:
                if x_ki and y_ki in range(8):
                    if board_checker[y_ki][x_ki] != 1:
                        move_list.append((x_ki, y_ki))
        print(self.piece_type)
        print(move_list)
        return move_list

    def highlight(self):
        super().highlight()
        self.position_tracking()
        self.piece_mov()


####################
class MyKivyChess(App):
    def build(self):
        return TopOfEverything()


with open("C:\\Users\\Yu\\PycharmProjects\\untitled\\chess_layout.kv", "rb") as kvfile:
    kivystr = kvfile.read()
    Builder.load_string(kivystr.decode('cp1252'))

if __name__ == "__main__":
    MyKivyChess().run()
