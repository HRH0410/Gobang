import pygame
import sys

pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 550
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Gobang")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# 棋盘相关定义
GRID_SIZE = 30  # 网格大小
BOARD_SIZE = 15  # 棋盘为15x15
BOARD_OFFSET_X = (SCREEN_WIDTH - BOARD_SIZE * GRID_SIZE) // 2
BOARD_OFFSET_Y = (SCREEN_HEIGHT - BOARD_SIZE * GRID_SIZE) // 2
PIECE_RADIUS = GRID_SIZE // 2 - 2

font = pygame.font.Font("src/Fond1.ttf", 30)
background_image_1 = pygame.image.load("src/Surface1.jpg")
background_image_2 = pygame.image.load("src/Surface2.jpg")
background_image_3 = pygame.image.load("src/Surface3.jpg")
button_image = pygame.image.load("src/WoodButton.png")
board_image = pygame.image.load("src/ChessBoard.jpg")
black_piece_image = pygame.image.load("src/BlackPiece.png")
white_piece_image = pygame.image.load("src/WhitePiece.png")

background_image_1 = pygame.transform.scale(background_image_1, (SCREEN_WIDTH, SCREEN_HEIGHT))
background_image_2 = pygame.transform.scale(background_image_2, (SCREEN_WIDTH, SCREEN_HEIGHT))
background_image_3 = pygame.transform.scale(background_image_3, (SCREEN_WIDTH, SCREEN_HEIGHT))
button_image = pygame.transform.scale(button_image, (350, 120))
board_image = pygame.transform.scale(board_image, (BOARD_SIZE * GRID_SIZE+15, BOARD_SIZE * GRID_SIZE+22))
black_piece_image = pygame.transform.scale(black_piece_image, (GRID_SIZE-4, GRID_SIZE-4))  # 调整棋子大小
white_piece_image = pygame.transform.scale(white_piece_image, (GRID_SIZE-4, GRID_SIZE-4))  # 调整棋子大小

# 定义棋盘状态 0 表示空，1 表示黑子，2 表示白子
board_state = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
current_player = 1  # 1 表示黑子，2 表示白子
is_AI=False
is_BLACK=False

class Button:
    def __init__(self, image, text, x, y):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.text = text
        self.text_surface = font.render(self.text, True, (0, 0, 0))  # 黑色字体

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
        text_rect = self.text_surface.get_rect(center=self.rect.center)
        text_rect.y += 8
        screen.blit(self.text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

def draw_pieces():
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board_state[row][col] == 1:  # 黑子
                piece_x = BOARD_OFFSET_X + col * GRID_SIZE - PIECE_RADIUS
                piece_y = BOARD_OFFSET_Y + row * GRID_SIZE - PIECE_RADIUS
                screen.blit(black_piece_image, (piece_x, piece_y))
            elif board_state[row][col] == 2:  # 白子
                piece_x = BOARD_OFFSET_X + col * GRID_SIZE - PIECE_RADIUS
                piece_y = BOARD_OFFSET_Y + row * GRID_SIZE - PIECE_RADIUS
                screen.blit(white_piece_image, (piece_x, piece_y))

def place_piece(x, y):
    global current_player
    global is_AI
    global is_BLACK
    col = round((x - BOARD_OFFSET_X) / GRID_SIZE)  # 计算点击最近的列
    row = round((y - BOARD_OFFSET_Y) / GRID_SIZE)  # 计算点击最近的行

    # 检查是否点击在有效的棋盘范围内，并且该位置为空
    if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE and board_state[row][col] == 0:
        board_state[row][col] = current_player  # 在棋盘上记录当前玩家的落子

        # 检查当前玩家是否胜利
        if check_win(row, col):
            if(current_player == 1):
               is_BLACK=True
            end_screen()

    current_player = 3 - current_player  # 切换玩家

    #AI棋手
    if(is_AI):
        AI_player(row,col)

def check_win(row, col):
    def count_pieces(delta_row, delta_col):
        count = 1
        for i in range(1, 5):
            r = row + delta_row * i
            c = col + delta_col * i
            if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board_state[r][c] ==current_player:
                count += 1
            else:
                break

        for i in range(1, 5):
            r = row - delta_row * i
            c = col - delta_col * i
            if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board_state[r][c] == current_player:
                count += 1
            else:
                break
        return count

    # 检查四个方向是否有5颗连珠
    if count_pieces(1, 0) >= 5:  # 水平方向
        return True
    if count_pieces(0, 1) >= 5:  # 垂直方向
        return True
    if count_pieces(1, 1) >= 5:  # 主对角线
        return True
    if count_pieces(1, -1) >= 5:  # 副对角线
        return True

    return False

#AI棋手的下棋算法
def AI_player(row,col):
    global current_player
    if current_player == 2:
        check_white_win()
        check_four_outside(row,col)
        check_four_inside(row,col)
        check_white_tofour()
        check_three_outside(row,col)
        check_three_inside(row,col)
        check_white_tothree()
        check_random(row,col)

#优先看能不能直接获胜
def check_white_win():
    global current_player
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            def count_pieces(delta_row, delta_col):
                count = 0

                for i in range(1, 5):
                    r = row + delta_row * i
                    c = col + delta_col * i
                    if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board_state[r][c] == 2:
                        count += 1
                    else:
                        break

                for i in range(1, 5):
                    r = row - delta_row * i
                    c = col - delta_col * i
                    if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board_state[r][c] == 2:
                        count += 1
                    else:
                        break
                return count

            if(board_state[row][col] == 0 and current_player == 2):
                if count_pieces(1, 0) ==4 or count_pieces(0, 1) ==4 or count_pieces(1, 1) ==4 or count_pieces(1, -1) ==4:
                    board_state[row][col] = 2
                    current_player = 1
                    end_screen()

#阻挡已经连成四个的黑棋
def check_four_outside(row,col):
     global current_player

     def count_pieces_forward(delta_row, delta_col):
         count = 1

         for i in range(1, 4):
             r = row + delta_row * i
             c = col + delta_col * i
             if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board_state[r][c] == 1:
                 count += 1
             else:
                 break
         return count

     def count_pieces_backward(delta_row, delta_col):
         count = 1
         for i in range(1, 4):
             r = row - delta_row * i
             c = col - delta_col * i
             if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board_state[r][c] == 1:
                 count += 1
             else:
                 break
         return count

     if count_pieces_forward(1, 0) ==4 and current_player==2:
         if(board_state[row-1][col] == 0 and row-1>=0):
             board_state[row - 1][col] = 2
             if check_win(row-1, col):
                 end_screen()
             current_player=1
         elif(board_state[row+4][col] == 0 and row+4<=BOARD_SIZE):
             board_state[row + 4][col] = 2
             if check_win(row+4, col):
                 end_screen()
             current_player = 1
     if count_pieces_forward(0, 1) ==4 and current_player==2:
         if (board_state[row ][col-1] == 0 and col-1>=0):
             board_state[row ][col-1] = 2
             if check_win(row, col - 1):
                 end_screen()
             current_player = 1
         elif (board_state[row ][col+4] == 0 and col+4<=BOARD_SIZE):
             board_state[row ][col+4] = 2
             if check_win(row, col + 4):
                 end_screen()
             current_player = 1
     if count_pieces_forward(1, 1) ==4 and current_player==2:
         if (board_state[row-1 ][col-1] == 0 and col-1>=0 and row-1>=0):
             board_state[row-1 ][col-1] = 2
             if check_win(row-1, col - 1):
                 end_screen()
             current_player = 1
         elif (board_state[row+4 ][col+4] == 0 and col+4<=BOARD_SIZE and row+4<=BOARD_SIZE):
             board_state[row+4 ][col+4] = 2
             if check_win(row+4, col + 4):
                 end_screen()
             current_player = 1
     if count_pieces_forward(1, -1) ==4 and current_player==2:
         if (board_state[row-1 ][col+1] == 0 and col+1<=BOARD_SIZE and row-1>=0):
             board_state[row-1 ][col+1] = 2
             if check_win(row-1, col + 1):
                 end_screen()
             current_player = 1
         elif (board_state[row+4 ][col-4] == 0 and col-4>=0 and row+4<=BOARD_SIZE):
             board_state[row+4 ][col-4] = 2
             if check_win(row+4, col-4):
                 end_screen()
             current_player = 1

     if count_pieces_backward(1, 0) ==4 and current_player==2:
         if(board_state[row+1][col] == 0 and row+1<=BOARD_SIZE):
             board_state[row + 1][col] = 2
             if check_win(row+1, col):
                 end_screen()
             current_player=1
         elif(board_state[row-4][col] == 0 and row-4>=0):
             board_state[row - 4][col] = 2
             if check_win(row-4, col):
                 end_screen()
             current_player = 1
     if count_pieces_backward(0, 1) ==4 and current_player==2:
         if (board_state[row ][col+1] == 0 and col+1<=BOARD_SIZE):
             board_state[row ][col+1] = 2
             if check_win(row, col + 1):
                 end_screen()
             current_player = 1
         elif (board_state[row ][col-4] == 0 and col-4>=0):
             board_state[row ][col-4] = 2
             if check_win(row, col-4):
                 end_screen()
             current_player = 1
     if count_pieces_backward(1,1) == 4 and current_player==2:
         if (board_state[row+1 ][col+1] == 0 and col+1<=BOARD_SIZE and row+1<=BOARD_SIZE):
             board_state[row+1 ][col+1] = 2
             if check_win(row+1, col + 1):
                 end_screen()
             current_player = 1
         elif (board_state[row-4 ][col-4] == 0 and col-4>=0 and row-4>=0):
             board_state[row-4 ][col-4] = 2
             if check_win(row-4, col-4):
                 end_screen()
             current_player = 1
     if count_pieces_backward(1, -1) ==4 and current_player==2:
         if (board_state[row+1 ][col-1] == 0 and row+1<=BOARD_SIZE and col-1>=0):
             board_state[row+1 ][col-1] = 2
             if check_win(row+1, col - 1):
                 end_screen()
             current_player = 1
         elif (board_state[row-4 ][col+4] == 0 and col+4<=BOARD_SIZE and row-4>=0):
             board_state[row-4 ][col+4] = 2
             if check_win(row-4, col + 4):
                 end_screen()
             current_player = 1

#阻挡将要在内部连成四个的黑棋
def check_four_inside(row,col):
    global current_player

    if(board_state[row][col+1] == 1 and board_state[row][col+2] == 0 and board_state[row][col+3] == 1 and col+3<=BOARD_SIZE and current_player==2):
        board_state[row][col+2] = 2
        if check_win(row, col + 2):
            end_screen()
        current_player = 1
    elif (board_state[row][col + 1] == 0 and board_state[row][col + 2] == 1 and board_state[row][col + 3] == 1 and col + 3 <= BOARD_SIZE and current_player == 2):
        board_state[row][col + 1] = 2
        if check_win(row, col + 1):
            end_screen()
        current_player = 1
    elif (board_state[row][col - 1] == 1 and board_state[row][col + 1] == 0 and board_state[row][col + 2] == 1 and col + 2 <= BOARD_SIZE and col-1>=0 and current_player == 2):
        board_state[row][col + 1] = 2
        if check_win(row, col + 1):
            end_screen()
        current_player = 1
    elif (board_state[row][col - 1] == 0 and board_state[row][col - 2] == 1 and board_state[row][col + 1] == 1 and col + 1 <= BOARD_SIZE and col-2>=0 and current_player == 2):
        board_state[row][col - 1] = 2
        if check_win(row, col - 1):
            end_screen()
        current_player = 1
    elif (board_state[row][col - 1] == 0 and board_state[row][col - 2] == 1 and board_state[row][col - 3] == 1 and col - 3 >=0  and current_player == 2):
        board_state[row][col - 1] = 2
        if check_win(row, col - 1):
            end_screen()
        current_player = 1
    elif (board_state[row][col - 1] == 1 and board_state[row][col - 2] == 0 and board_state[row][col - 3] == 1 and col - 3 >=0 and current_player == 2):
        board_state[row][col -2] = 2
        if check_win(row, col -2):
            end_screen()
        current_player = 1
    elif (board_state[row+1][col] == 1 and board_state[row+2][col] == 0 and board_state[row+3][ col ] == 1 and row + 3 <= BOARD_SIZE and current_player == 2):
        board_state[row+2][col] = 2
        if check_win(row+2, col):
            end_screen()
        current_player = 1
    elif (board_state[row+1][col] == 0 and board_state[row+2][col] == 1 and board_state[row+3][ col ] == 1 and row + 3 <= BOARD_SIZE and current_player == 2):
        board_state[row+1][col] = 2
        if check_win(row+1, col):
            end_screen()
        current_player = 1
    elif (board_state[row+1][col] == 1 and board_state[row-1][col] == 0 and board_state[row-2][ col ] == 1 and row + 1 <= BOARD_SIZE and row-2>=0 and current_player == 2):
        board_state[row-1][col] = 2
        if check_win(row-1, col):
            end_screen()
        current_player = 1
    elif (board_state[row+1][col] == 0 and board_state[row+2][col] == 1 and board_state[row-1][ col ] == 1 and row + 2 <= BOARD_SIZE and row-1>=0 and current_player == 2):
        board_state[row+1][col] = 2
        if check_win(row+1, col):
            end_screen()
        current_player = 1
    elif (board_state[row-1][col] == 1 and board_state[row-2][col] == 0 and board_state[row-3][ col ] == 1 and row - 3 >=0 and current_player == 2):
        board_state[row-2][col] = 2
        if check_win(row-2, col):
            end_screen()
        current_player = 1
    elif (board_state[row-1][col] == 0 and board_state[row-2][col] == 1 and board_state[row-3][ col ] == 1 and row - 3 >=0 and current_player == 2):
        board_state[row-1][col] = 2
        if check_win(row-1, col):
            end_screen()
        current_player = 1
    elif (board_state[row+1][col+1] == 1 and board_state[row+2][col+2] == 0 and board_state[row+3][ col+3 ] == 1 and row + 3 <= BOARD_SIZE and col+3<=BOARD_SIZE and current_player == 2):
        board_state[row+2][col+2] = 2
        if check_win(row+2, col+2):
            end_screen()
        current_player = 1
    elif (board_state[row+1][col+1] == 0 and board_state[row+2][col+2] == 1 and board_state[row+3][ col+3 ] == 1 and row + 3 <= BOARD_SIZE and col+3<=BOARD_SIZE and current_player == 2):
        board_state[row+1][col+1] = 2
        if check_win(row+1, col + 1):
            end_screen()
        current_player = 1
    elif (board_state[row+1][col+1] == 0 and board_state[row+2][col+2] == 1 and board_state[row-1][ col-1 ] == 1 and row + 2 <= BOARD_SIZE and col+2<=BOARD_SIZE and row-1>=0 and col-1>=0 and current_player == 2):
        board_state[row+1][col+1] = 2
        if check_win(row+1, col + 1):
            end_screen()
        current_player = 1
    elif (board_state[row+1][col+1] == 1 and board_state[row-1][col-1] == 0 and board_state[row-2][ col-2 ] == 1 and row +1 <= BOARD_SIZE and col+1<=BOARD_SIZE and row-2>=0 and col-2>=0 and current_player == 2):
        board_state[row-1][col-1] = 2
        if check_win(row-1, col - 1):
            end_screen()
        current_player = 1
    elif (board_state[row-1][col-1] == 1 and board_state[row-2][col-2]== 0 and board_state[row-3][ col-3 ] == 1 and row - 3 >=0 and col-3>=0 and current_player == 2):
        board_state[row-2][col-2] = 2
        if check_win(row-2, col-2):
            end_screen()
        current_player = 1
    elif (board_state[row-1][col-1] == 0 and board_state[row-2][col-2]== 1 and board_state[row-3][ col-3 ] == 1 and row - 3 >=0 and col-3>=0 and current_player == 2):
        board_state[row-1][col-1] = 2
        if check_win(row-1, col - 1):
            end_screen()
        current_player = 1
    elif (board_state[row-1][col+1] == 1 and board_state[row-2][col+2]== 0 and board_state[row-3][ col+3 ] == 1 and row - 3 >=0 and col+3<=BOARD_SIZE and current_player == 2):
        board_state[row-2][col+2] = 2
        if check_win(row-2, col + 2):
            end_screen()
        current_player = 1
    elif (board_state[row-1][col+1] ==0 and board_state[row-2][col+2]== 1 and board_state[row-3][ col+3 ] == 1 and row - 3 >=0 and col+3<=BOARD_SIZE and current_player == 2):
        board_state[row-1][col+1] = 2
        if check_win(row-1, col + 1):
            end_screen()
        current_player = 1
    elif (board_state[row-1][col+1] == 0 and board_state[row-2][col+2]== 1 and board_state[row+1][ col-1 ] == 1 and row - 2 >=0 and col+2<=BOARD_SIZE and row+1<=BOARD_SIZE and col-1>=0 and current_player == 2):
        board_state[row-1][col+1] = 2
        if check_win(row-1, col + 1):
            end_screen()
        current_player = 1
    elif (board_state[row-1][col+1] == 1 and board_state[row+1][col-1]== 0 and board_state[row+2][ col-2 ] == 1 and row - 1 >=0 and col+1<=BOARD_SIZE and row+2<=BOARD_SIZE and col-2>=0 and current_player == 2):
        board_state[row+1][col-1] = 2
        if check_win(row+1, col - 1):
            end_screen()
        current_player = 1
    elif (board_state[row+1][col-1] == 1 and board_state[row+2][col-2]== 0 and board_state[row+3][ col-3 ] == 1 and col - 3 >=0 and row+3<=BOARD_SIZE and current_player == 2):
        board_state[row+2][col-2] = 2
        if check_win(row+2, col-2):
            end_screen()
        current_player = 1
    elif (board_state[row+1][col-1] == 0 and board_state[row+2][col-2]== 1 and board_state[row+3][ col-3 ] == 1 and col - 3 >=0 and row+3<=BOARD_SIZE and current_player == 2):
        board_state[row+1][col-1] = 2
        if check_win(row+1, col - 1):
            end_screen()
        current_player = 1

#检查有没有能够连成四个的白棋
def check_white_tofour():
    global current_player
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            def count_pieces(delta_row, delta_col):
                count = 0

                for i in range(1, 4):
                    r = row + delta_row * i
                    c = col + delta_col * i
                    if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board_state[r][c] == 2:
                        count += 1
                    else:
                        break

                for i in range(1, 4):
                    r = row - delta_row * i
                    c = col - delta_col * i
                    if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board_state[r][c] == 2:
                        count += 1
                    else:
                        break
                return count

            if (board_state[row][col] == 0 and current_player == 2):
                if count_pieces(1, 0) == 3 or count_pieces(0, 1) == 3 or count_pieces(1, 1) == 3 or count_pieces(1,
                                                                                                                 -1) == 3:
                    board_state[row][col] = 2
                    current_player = 1

#阻挡将要在外部连成四个的黑棋
def check_three_outside(row,col):
    global current_player

    def count_pieces_forward(delta_row, delta_col):
        count = 1

        for i in range(1, 3):
            r = row + delta_row * i
            c = col + delta_col * i
            if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board_state[r][c] == 1:
                count += 1
            else:
                break
        return count

    def count_pieces_backward(delta_row, delta_col):
        count = 1
        for i in range(1, 3):
            r = row - delta_row * i
            c = col - delta_col * i
            if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board_state[r][c] == 1:
                count += 1
            else:
                break
        return count

    if count_pieces_forward(1, 0) == 3 and current_player==2:
        if (board_state[row - 1][col] == 0 and row-1>=0):
            board_state[row - 1][col] = 2
            if check_win(row-1, col):
                end_screen()
            current_player = 1
        elif (board_state[row + 4][col] == 0 and row+4<=BOARD_SIZE):
            board_state[row + 4][col] = 2
            if check_win(row+4, col):
                end_screen()
            current_player = 1
    if count_pieces_forward(0, 1) == 3 and current_player==2:
        if (board_state[row][col - 1] == 0 and col-1>=0):
            board_state[row][col - 1] = 2
            if check_win(row, col-1):
                end_screen()
            current_player = 1
        elif (board_state[row][col + 4] == 0 and col+4<=BOARD_SIZE):
            board_state[row][col + 4] = 2
            if check_win(row, col+4):
                end_screen()
            current_player = 1
    if count_pieces_forward(1, 1) == 3 and current_player==2:
        if (board_state[row - 1][col - 1] == 0 and col-1>=0 and row-1>=0):
            board_state[row - 1][col - 1] = 2
            if check_win(row-1, col-1):
                end_screen()
            current_player = 1
        elif (board_state[row + 4][col + 4] == 0 and col+4<=BOARD_SIZE and row+4<=BOARD_SIZE):
            board_state[row + 4][col + 4] = 2
            if check_win(row+4, col+4):
                end_screen()
            current_player = 1
    if count_pieces_forward(1, -1) == 3 and current_player==2:
        if (board_state[row - 1][col + 1] == 0 and row-1>=0 and col+1<=BOARD_SIZE):
            board_state[row - 1][col + 1] = 2
            if check_win(row-1, col+1):
                end_screen()
            current_player = 1
        elif (board_state[row + 4][col - 4] == 0 and row+4<=BOARD_SIZE and col-4>=0):
            board_state[row + 4][col - 4] = 2
            if check_win(row+4, col-4):
                end_screen()
            current_player = 1

    if count_pieces_backward(1, 0) == 3 and current_player==2:
        if (board_state[row + 1][col] == 0 and row+1<=BOARD_SIZE):
            board_state[row + 1][col] = 2
            if check_win(row+1, col):
                end_screen()
            current_player = 1
        elif (board_state[row - 4][col] == 0 and row-4>=0):
            board_state[row - 4][col] = 2
            if check_win(row-4, col):
                end_screen()
            current_player = 1
    if count_pieces_backward(0, 1) == 3 and current_player==2:
        if (board_state[row][col + 1] == 0 and col+1<=BOARD_SIZE):
            board_state[row][col + 1] = 2
            if check_win(row, col+1):
                end_screen()
            current_player = 1
        elif (board_state[row][col - 4] == 0 and col-4>=0):
            board_state[row][col - 4] = 2
            if check_win(row, col-4):
                end_screen()
            current_player = 1
    if count_pieces_backward(1, 1) == 3 and current_player==2:
        if (board_state[row + 1][col + 1] == 0 and col+1<=BOARD_SIZE and row+1<=BOARD_SIZE):
            board_state[row + 1][col + 1] = 2
            if check_win(row+1, col+1):
                end_screen()
            current_player = 1
        elif (board_state[row - 4][col - 4] == 0 and row-4>+0 and col-4>=0):
            board_state[row - 4][col - 4] = 2
            if check_win(row-4, col-4):
                end_screen()
            current_player = 1
    if count_pieces_backward(1, -1) == 3 and current_player==2:
        if (board_state[row + 1][col - 1] == 0 and row+1<=BOARD_SIZE and col-1>=0):
            board_state[row + 1][col - 1] = 2
            if check_win(row+1, col-1):
                end_screen()
            current_player = 1
        elif (board_state[row - 4][col + 4] == 0 and row-4>=0 and col+4<=BOARD_SIZE):
            board_state[row - 4][col + 4] = 2
            if check_win(row-4, col+4):
                end_screen()
            current_player = 1

#阻挡要在内部连成三个的黑棋
def check_three_inside(row,col):
    global current_player

    if(board_state[row][col+1] == 1 and board_state[row][col-1]==1 and col+1<=BOARD_SIZE and col-1>=0 and current_player==2 ):
        if(board_state[row][col+2]==0 and col+2<=BOARD_SIZE):
            board_state[row][col+2] = 2
            if check_win(row, col+2):
                end_screen()
            current_player = 1
        elif(board_state[row][col-2]==0 and col-2>=0):
            board_state[row][col-2]=2
            if check_win(row, col-2):
                end_screen()
            current_player=1
    elif(board_state[row+1][col] == 1 and board_state[row-1][col]==1 and row+1<=BOARD_SIZE and row-1>=0 and current_player==2 ):
        if(board_state[row+2][col]==0 and row+2<=BOARD_SIZE):
            board_state[row+2][col] = 2
            if check_win(row+2, col):
                end_screen()
            current_player = 1
        elif(board_state[row-2][col]==0 and row-2>=0):
            board_state[row-2][col]=2
            if check_win(row-2, col):
                end_screen()
            current_player=1
    elif (board_state[row+1][col + 1] == 1 and board_state[row-1][col - 1] == 1 and col + 1 <= BOARD_SIZE and col - 1 >= 0 and row+1<=BOARD_SIZE and row-1>=0 and current_player == 2):
        if (board_state[row+2][col + 2] == 0 and col + 2 <= BOARD_SIZE and row+2<=BOARD_SIZE):
            board_state[row+2][col + 2] = 2
            if check_win(row+2, col+2):
                end_screen()
            current_player = 1
        elif (board_state[row-2][col - 2] == 0 and col - 2 >= 0 and row-2>=0):
            board_state[row-2][col - 2] = 2
            if check_win(row-2, col+2):
                end_screen()
            current_player = 1
    elif (board_state[row-1][col + 1] == 1 and board_state[row+1][col - 1] == 1 and col + 1 <= BOARD_SIZE and col - 1 >= 0 and row+1<=BOARD_SIZE and row-1>=0 and current_player == 2):
        if (board_state[row-2][col + 2] == 0 and col + 2 <= BOARD_SIZE and row-2>=0):
            board_state[row-2][col + 2] = 2
            if check_win(row-2, col+2):
                end_screen()
            current_player = 1
        elif (board_state[row+2][col - 2] == 0 and col - 2 >= 0 and row+2<=BOARD_SIZE):
            board_state[row+2][col - 2] = 2
            if check_win(row+2, col-2):
                end_screen()
            current_player = 1
    elif(board_state[row][col+1] == 0 and board_state[row][col+2] == 1 and col+2<=BOARD_SIZE and current_player==2):
        board_state[row][col+1] = 2
        if check_win(row, col + 1):
            end_screen()
        current_player=1
    elif (board_state[row][col -1] == 0 and board_state[row][col - 2] == 1 and col - 2 >=0 and current_player == 2):
        board_state[row][col - 1] = 2
        if check_win(row, col - 1):
            end_screen()
        current_player = 1
    elif (board_state[row+1][col] == 0 and board_state[row+2][col] == 1 and row+2>=BOARD_SIZE and current_player == 2):
        board_state[row+1][col] = 2
        if check_win(row+1, col):
            end_screen()
        current_player = 1
    elif (board_state[row-1][col] == 0 and board_state[row-2][col] == 1 and row-2 >=0 and current_player == 2):
        board_state[row-1][col] = 2
        if check_win(row-1, col):
            end_screen()
        current_player = 1
    elif (board_state[row-1][col -1] == 0 and board_state[row-2][col - 2] == 1 and col - 2 >=0 and row-2>=0 and current_player == 2):
        board_state[row-1][col - 1] = 2
        if check_win(row-1, col - 1):
            end_screen()
        current_player = 1
    elif (board_state[row+1][col +1] == 0 and board_state[row+2][col + 2] == 1 and col + 2 <=BOARD_SIZE and row+2<=BOARD_SIZE and current_player == 2):
        board_state[row+1][col + 1] = 2
        if check_win(row+1, col + 1):
            end_screen()
        current_player = 1
    elif (board_state[row+1][col -1] == 0 and board_state[row+2][col - 2] == 1 and col - 2 >=0 and row+2<=BOARD_SIZE and current_player == 2):
        board_state[row+1][col - 1] = 2
        if check_win(row+1, col - 1):
            end_screen()
        current_player = 1
    elif (board_state[row-1][col +1] == 0 and board_state[row-2][col + 2] == 1 and row - 2 >=0 and col+2<=BOARD_SIZE and current_player == 2):
        board_state[row-1][col + 1] = 2
        if check_win(row-1, col + 1):
            end_screen()
        current_player = 1

#检查有没有能够连成三个的白棋
def check_white_tothree():
    global current_player
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            def count_pieces(delta_row, delta_col):
                count = 0

                for i in range(1, 3):
                    r = row + delta_row * i
                    c = col + delta_col * i
                    if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board_state[r][c] == 2:
                        count += 1
                    else:
                        break

                for i in range(1, 3):
                    r = row - delta_row * i
                    c = col - delta_col * i
                    if 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board_state[r][c] == 2:
                        count += 1
                    else:
                        break
                return count

            if (board_state[row][col] == 0 and current_player == 2):
                if count_pieces(1, 0) == 2 or count_pieces(0, 1) == 2 or count_pieces(1, 1) == 2 or count_pieces(1,-1)==2:
                    board_state[row][col] = 2
                    current_player = 1

#其余情况围绕黑棋周围下即可
def check_random(row,col):
    global current_player
    if (board_state[row][col + 1] == 0 and current_player == 2):
        board_state[row][col + 1] = 2
        if check_win(row, col + 1):
            end_screen()
        current_player = 1
    elif (board_state[row][col - 1] == 0 and current_player == 2):
        board_state[row][col - 1] = 2
        if check_win(row, col - 1):
            end_screen()
        current_player = 1
    elif (board_state[row + 1][col] == 0 and current_player == 2):
        board_state[row + 1][col] = 2
        if check_win(row + 1, col):
            end_screen()
        current_player = 1
    elif (board_state[row - 1][col] == 0 and current_player == 2):
        board_state[row - 1][col] = 2
        if check_win(row - 1, col):
            end_screen()
        current_player = 1
    elif (board_state[row + 1][col + 1] == 0 and current_player == 2):
        board_state[row + 1][col + 1] = 2
        if check_win(row + 1, col + 1):
            end_screen()
        current_player = 1
    elif (board_state[row - 1][col + 1] == 0 and current_player == 2):
        board_state[row - 1][col + 1] = 2
        if check_win(row - 1, col + 1):
            end_screen()
        current_player = 1
    elif (board_state[row + 1][col - 1] == 0 and current_player == 2):
        board_state[row + 1][col - 1] = 2
        if check_win(row + 1, col - 1):
            end_screen()
        current_player = 1
    elif (board_state[row - 1][col - 1] == 0 and current_player == 2):
        board_state[row - 1][col - 1] = 2
        if check_win(row - 1, col - 1):
            end_screen()
        current_player = 1

# 开始界面
def start_screen():
    global is_AI
    start_button1 = Button(button_image, "player VS player", 125,250 )
    start_button2 = Button(button_image, "player VS AI", 125, 380)

    while True:
        screen.blit(background_image_1, (0, 0))
        start_button1.draw(screen)
        start_button2.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button1.is_clicked(event.pos):
                    game_screen()  # 跳转到双人对战界面
                elif start_button2.is_clicked(event.pos):
                    is_AI=True
                    game_screen()  # 跳转到人机对战界面

        pygame.display.flip()

# 游戏界面
def game_screen():
    while True:
        screen.blit(background_image_2, (0, 0))
        screen.blit(board_image, (BOARD_OFFSET_X-23, BOARD_OFFSET_Y-27))
        draw_pieces()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                place_piece(mouse_x, mouse_y)

        pygame.display.flip()

#结束界面
def end_screen():
    global is_BLACK
    while True:
        if(is_BLACK):
            screen.blit(background_image_2, (0, 0))
        else:
            screen.blit(background_image_3, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.flip()

# 主函数
def main():
    start_screen()

if __name__ == "__main__":
    main()
