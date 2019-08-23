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

pieces_pos = np.zeros((8, 8), dtype=int)
# this list is an piece index which is updated by the placement of the pieces and the movement of the pieces

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
    tile_instances = []

    def __init__(self, tile_color, number, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tile_instances.append(self)
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
                pieces_pos[coordinate[1]][coordinate[0]] = 2

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
                pieces_pos[coordinate[1]][coordinate[0]] = 1
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

    # makes an array which represents the empty (value = 0)  or the full tiles (white = 1 black = 2)
    # pieces_pos = np.zeros((8, 8), dtype=int)
    # for instance in piece_instances:
    #     if instance.piece_color == "white":
    #         pieces_pos[instance.coordinate[1]][instance.coordinate[0]] = 1
    #     if instance.piece_color == "black":
    #         pieces_pos[instance.coordinate[1]][instance.coordinate[0]] = 2

    def piece_mov(self):

        # Generates a list of tuples with the possible move coordinates
        move_list = []
        board_checker = pieces_pos
        piece_x = self.coordinate[0]
        piece_y = self.coordinate[1]

        if self.piece_type == "pawn":
            if piece_y == 6:
                for p_mov in range(1, 3):
                    if board_checker[piece_y - p_mov][piece_x] == 0:
                        move_list.append((piece_x, piece_y - p_mov))
                    elif board_checker[piece_y - p_mov][piece_x] == 2:
                        move_list.append((piece_x, piece_y - p_mov))
                        break
            else:
                if board_checker[piece_y - 1][piece_x] == 0 or board_checker[piece_y - 1][piece_x] == 2:
                    move_list.append((piece_x, piece_y + 1))

        elif self.piece_type == "rook":
            # EXPLANATION: it runs the four directions appending the possible coordinates (pretty much as the bishop)
            # when it finds a piece, it ends the loop appending the piece coordinate if it is an anemy piece,
            # else it just breaks
            rook_list = [[piece_y, -1, 0],
                         [8 - piece_y, 1, 0],
                         [piece_x, 0, -1],
                         [8 - piece_x, 0, 1]]
            # ROOK_LIST EXPLANATION: this list is a list of schedules in order
            # to the for loop work to the four directions of motion of the piece

            for r_list in rook_list:
                for r_direction in range(r_list[0]):
                    checker = board_checker[piece_y + (r_list[1] * r_direction)][piece_x + (r_list[2] * r_direction)]
                    if checker in (0, 2):
                        move_list.append((piece_x + (r_list[2] * r_direction), piece_y + (r_list[1] * r_direction)))
                        if checker in 2:
                            break
                    else:
                        break
            # for r_up in range(piece_y):
            #     if board_checker[piece_y - r_up][piece_x] == 0:
            #         move_list.append((piece_x, piece_y - r_up))
            #     elif board_checker[piece_y - r_up][piece_x] == 2:
            #         move_list.append((piece_x, piece_y - r_up))
            #         break
            #     else:
            #         break
            #
            # for r_down in range(8 - piece_y):
            #     if board_checker[piece_y + r_down][piece_x] == 0:
            #         move_list.append((piece_x, piece_y + r_down))
            #     elif board_checker[piece_y + r_down][piece_x] == 2:
            #         move_list.append((piece_x, piece_y + r_down))
            #         break
            #     else:
            #         break
            #
            # for r_left in range(piece_x):
            #     if board_checker[piece_y][piece_x - r_left] == 0:
            #         move_list.append((piece_x - r_left, piece_y))
            #     elif board_checker[piece_y][piece_x - r_left] == 2:
            #         move_list.append((piece_x - r_left, piece_y))
            #         break
            #     else:
            #         break
            #
            # for r_right in range(8 - piece_x):
            #     if board_checker[piece_y][piece_x + r_right] == 0:
            #         move_list.append((r_right, piece_x + piece_y))
            #     elif board_checker[piece_y][piece_x + r_right] == 2:
            #         move_list.append((piece_x + r_right, piece_y))
            #         break
            #     else:
            #         break

        elif self.piece_type == "knight":
            # EXPLANATION: the if statements with range(8) check if the coordinate will be inside the board
            # the -2, 2 range refers to the x axis. When the knight moves +/-2 in X (if abs(x_kn) == 2:)
            # it moves +/-1 in Y
            # When it moves +/- 1 in X (elif abs(x_kn) == 1:)
            # then it moves +/- 2 in Y

            for x_kn in range(-2, 3):
                if -1 < x_kn + piece_x < 8:

                    if abs(x_kn) == 2:
                        if -1 < piece_y + 1 < 8 and board_checker[piece_y+1][piece_x+x_kn] != 1:
                            move_list.append((piece_x+x_kn, piece_y+1))
                        elif -1 < piece_y - 1 < 8 and board_checker[piece_y-1][piece_x+x_kn] != 1:
                            move_list.append((piece_x+x_kn, piece_y-1))

                    elif abs(x_kn) == 1:
                        if -1 < piece_y + 2 < 8 and board_checker[piece_y+2][piece_x+x_kn] != 1:
                            move_list.append((piece_x+x_kn, piece_y+2))
                        elif -1 < piece_y - 2 < 8 and board_checker[piece_y-2][piece_x+x_kn] != 1:
                            move_list.append((piece_x+x_kn, piece_y-2))

        elif self.piece_type == "bishop":
            # board_list = [(x, y) for x in range(8) for y in range(8)]
            # for (x_b, y_b) in board_list:
            #     if abs(piece_x - abs(x_b)) == abs(piece_y - abs(y_b)) and board_checker[y_b][x_b] != 1:
            #         move_list.append((x_b, y_b))
            # EXPLANATION: bishop runs to the four diagonals  each one at a time,
            # when it finds with another piece, it ends the direction reading (appends if opponent's piece, else break)
            bishop_list = [[8 - piece_x, piece_y, -1, 1],
                           [piece_x, piece_y, -1, -1],
                           [8 - piece_x, 7 - piece_y, 1, 1],
                           [piece_x, 7 - piece_y, 1, -1]]
            # BISHOP_LIST EXPLANATION: this list is a list of schedules in order
            # to the for loop work to the four directions of motion of the piece

            for b_item in bishop_list:
                for b_diag in range(b_item[0]):
                    if -1 < b_diag < b_item[1]:
                        if board_checker[piece_y + (b_item[2] * b_diag)][piece_x + (b_item[3] * b_diag)] == 0:
                            move_list.append((piece_x + (b_item[3] * b_diag), piece_y + (b_item[2] * b_diag)))
                        if board_checker[piece_y + (b_item[2] * b_diag)][piece_x + (b_item[3] * b_diag)] == 2:
                            move_list.append((piece_x + (b_item[3] * b_diag), piece_y + (b_item[2] * b_diag)))
                            break
                        else:
                            break

            # THE FOLLOWING CODE DOES THE SAME AS THE ACTUAL BISHOP MOVE ALGORITHM *************************
            # for b_up_right in range(8 - piece_x):
            #     if b_up_right in range(piece_y):
            #         if board_checker[piece_y - b_up_right][piece_x + b_up_right] == 0:
            #             move_list.append((piece_x + b_up_right, piece_y - b_up_right))
            #         if board_checker[piece_y - b_up_right][piece_x + b_up_right] == 2:
            #             move_list.append((piece_x + b_up_right, piece_y - b_up_right))
            #             break
            #         else:
            #             break
            #
            # for b_up_left in range(piece_x):
            #     if b_up_left in range(piece_y):
            #         if board_checker[piece_y - b_up_left][piece_x - b_up_left] == 0:
            #             move_list.append((piece_x - b_up_left, piece_y - b_up_left))
            #         if board_checker[piece_y - b_up_left][piece_x + b_up_left] == 2:
            #             move_list.append((piece_x - b_up_left, piece_y - b_up_left))
            #             break
            #         else:
            #             break
            #
            # for b_down_right in range(8 - piece_x):
            #     if b_down_right in range(8 - piece_y):
            #         if board_checker[piece_y + b_down_right][piece_x + b_down_right] == 0:
            #             move_list.append((piece_x + b_down_right, piece_y + b_down_right))
            #         if board_checker[piece_y + b_down_right][piece_x + b_down_right] == 2:
            #             move_list.append((piece_x + b_down_right, piece_y + b_down_right))
            #             break
            #         else:
            #             break
            #
            # for b_down_left in range(piece_x):
            #     if b_down_left in range(8 - piece_y):
            #         if board_checker[piece_y + b_down_left][piece_x - b_down_left] == 0:
            #             move_list.append((piece_x - b_down_left, piece_y + b_down_left))
            #         if board_checker[piece_y + b_down_left][piece_x - b_down_left] == 2:
            #             move_list.append((piece_x - b_down_left, piece_y + b_down_left))
            #             break
            #         else:
            #             break
            #***************************************************************************************************

        # queen is bishop + rook
        elif self.piece_type == "queen":
            queen_list = [[piece_y, -1, 0],
                          [8 - piece_y, 1, 0],
                          [piece_x, 0, -1],
                          [8 - piece_x, 0, 1]]

            # vertical and horizontal movements (see more in rook)
            for q_list in queen_list:
                for q_vert_hor in range(q_list[0]):
                    if board_checker[piece_y + (q_list[1] * q_vert_hor)][piece_x + (q_list[2] * q_vert_hor)] == 0:
                        move_list.append((piece_x + (q_list[2] * q_vert_hor), piece_y + (q_list[1] * q_vert_hor)))
                    elif board_checker[piece_y + (q_list[1] * q_vert_hor)][piece_x + (q_list[2] * q_vert_hor)] == 2:
                        move_list.append((piece_x + (q_list[2] * q_vert_hor), piece_y + (q_list[1] * q_vert_hor)))
                        break
                    else:
                        break

            queen_diag = [[8 - piece_x, piece_y, -1, 1],
                          [piece_x, piece_y, -1, -1],
                          [8 - piece_x, 7 - piece_y, 1, 1],
                          [piece_x, 7 - piece_y, 1, -1]]

            # diagonal movements (see more in bishop)
            for q_list2 in queen_diag:
                for q_diag in range(q_list2[0]):
                    if -1 < q_diag < q_list2[1]:
                        if board_checker[piece_y + (q_list2[2] * q_diag)][piece_x + (q_list2[3] * q_diag)] == 0:
                            move_list.append((piece_x + (q_list2[3] * q_diag), piece_y + (q_list2[2] * q_diag)))
                        if board_checker[piece_y + (q_list2[2] * q_diag)][piece_x + (q_list2[3] * q_diag)] == 2:
                            move_list.append((piece_x + (q_list2[3] * q_diag), piece_y + (q_list2[2] * q_diag)))
                            break
                        else:
                            break
        # else is king
        else:
            # EXPLANATION: it checks the three vertical squares besides the king coordinate,
            # then it checks the coordinate at front and back of the king.
            # All those coordinates are checked: the ones inside the table and without a ally piece in it are appended
            king_pre_list = list([(piece_x + 1, piece_y + move) for move in range(-1, 2)] +
                                 [(piece_x - 1, piece_y + move) for move in range(-1, 2)] +
                                 [(piece_x, piece_y + 1), (piece_x, piece_y - 1)])
            for (x_ki, y_ki) in king_pre_list:
                if -1 < x_ki < 8 and -1 < y_ki < 8:
                    if board_checker[y_ki][x_ki] != 1:
                        move_list.append((x_ki, y_ki))
        print(move_list)
        print(board_checker)
        return move_list

    def highlight(self):

        for high_tile in Tile.tile_instances:
            if high_tile.highlight_rect is not None:
                high_tile.canvas.remove(high_tile.highlight_rect)
                high_tile.highlight_rect = None

        highlight_schedule = [(num[0] + (num[1] * 8)) for num in self.piece_mov()] + [(self.coordinate[0] + 8 * self.coordinate[1])]
        for t_coord in highlight_schedule:
            Tile.tile_instances[t_coord].highlight()


####################
class MyKivyChess(App):
    def build(self):
        return TopOfEverything()


with open("C:\\Users\\Yu\\PycharmProjects\\untitled\\chess_layout.kv", "rb") as kvfile:
    kivystr = kvfile.read()
    Builder.load_string(kivystr.decode('cp1252'))

if __name__ == "__main__":
    MyKivyChess().run()
