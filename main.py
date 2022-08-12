import pygame
pygame.init()
clock = pygame.time.Clock()
screen_width = 720
screen_height = 720
screen = pygame.display.set_mode((screen_width,screen_height))
black_color = (0,0,0)
white_color = (255,255,255)
yellow_color = (255,255,0)
red_color=(255,0,0)
process_running = True
active_chessman = None
active_cell = None
active_player = "white"
looks="white"
def has_chessmate_on_way(pos,new_pos,direction):
    x_speed = 0
    y_speed = 0
    if "left" in direction:
        x_speed-=1
    if "right" in direction:
        x_speed+=1
    if "up" in direction:
        y_speed-=1
    if "down" in direction:
        y_speed +=1
    while True:
        if not 0 <= pos[1] + y_speed < field.height or not 0 <= pos[0] + x_speed < field.width:
            break
        if field.field[pos[1]+y_speed][pos[0]+x_speed] != 0:
            if field.field[pos[1]+y_speed][pos[0]+x_speed][0] != active_player and pos[1]+y_speed ==new_pos[1] and pos[0]+x_speed == new_pos[0]:
                return "take"
            else:
                return True
        else:
            if pos[1] + y_speed == new_pos[1] and pos[0] + x_speed == new_pos[0]:
                break
            pos=(pos[0]+x_speed,pos[1]+y_speed)
    return False

def has_chessmate_on_way_for_pawn(pos,direction,new_pos):
    y_speed = 0
    x_speed =0
    if "up" in direction:
        y_speed-=1
    if "down" in direction:
        y_speed+=1
    if "left" in direction:
        x_speed-=1
    if "right" in direction:
        x_speed += 1
    if abs(new_pos[1]-pos[1]) ==2:
        if x_speed == 0:
            if x_speed != 0:
                return True
            return False
    if field.field[pos[1]+y_speed][pos[0]+x_speed] != 0:
        if x_speed !=0:
            if field.field[pos[1]+y_speed][pos[0]+x_speed][0] != active_player:
                return "take"
        return True
    return False
class ChessMan:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def move(self,new_pos):
        field.field[self.y][self.x] = 0
        self.x, self.y = new_pos[0], new_pos[1]

def get_direction(pos,new_pos):
    if new_pos == pos:
        return None
    if pos[0] == new_pos[0]:
        if new_pos[1] < pos[1]:
            return "up"
        elif new_pos[1] > pos[1]:
            return "down"
    if pos[1] == new_pos[1]:
        if new_pos[0] > pos[1]:
            return "right"
        elif new_pos[0] < pos[1]:
            return "left"
    if new_pos[0] > pos[0] and new_pos[1] < pos[1]:
        return "right up"
    if new_pos[0] < pos[0] and new_pos[1] < pos[1]:
        return "left up"
    if new_pos[0] < pos[0] and new_pos[1] > pos[1]:
        return "left down"
    else:
        return "right down"
def take_chessman(pos):
    if field.field[pos[1]][pos[0]][0] == "white":
        for chessman in field.white_chessmans:
            if pos[0] == chessman.x and pos[1] == chessman.y:
                del (field.white_chessmans[field.white_chessmans.index(chessman)])
    else:
        for chessman in field.black_chessmans:
            if pos[0] == chessman.x and pos[1] == chessman.y:
                del (field.black_chessmans[field.black_chessmans.index(chessman)])

class King(ChessMan):
    def __init__(self,x,y,color):
        super(King, self).__init__(x,y)
        if color == "black":
            self.image=pics.black_king
        else:
            self.image=pics.white_king
    def move(self,new_pos):
        super(King, self).move(new_pos)
        field.field[self.y][self.x] = (active_player, "k")
    def is_can_move(self,new_pos):
        # if (abs(new_x-self.x) == 1 and self.y == new_y) or (abs(new_y-self.y) == 1 and self.x == new_x):
        direction = get_direction((self.x, self.y), new_pos)
        if direction:
            if abs(new_pos[0]-self.x) == 1 or abs(new_pos[1]-self.y) == 1:
                res = has_chessmate_on_way((self.x, self.y), new_pos, direction)
                if res == "take":
                    take_chessman(new_pos)
                    return True
                if not res:
                    return True
                else:
                    return False
class Queen(ChessMan):
    def __init__(self,x,y,color):
        super(Queen, self).__init__(x,y)
        if color == "black":
            self.image=pics.black_queen
        else:
            self.image=pics.white_queen
    def move(self,new_pos):
        super(Queen, self).move(new_pos)
        field.field[self.y][self.x] = (active_player, "q")
    def is_can_move(self,new_pos):
        direction = get_direction((self.x,self.y),new_pos)
        if direction:
            res = has_chessmate_on_way((self.x,self.y),new_pos,direction)
            if res == "take":
                take_chessman(new_pos)
                return True
            if not res:
                return True
            else:
                return False

                # return True
class Castle(ChessMan):
    def __init__(self,x,y,color):
        super(Castle, self).__init__(x,y)
        if color == "black":
            self.image=pics.black_castle
        else:
            self.image=pics.white_castle
    def move(self,new_pos):
        super(Castle, self).move(new_pos)
        field.field[self.y][self.x] = (active_player, "c")
    # def move(self,new_x,new_y):
    #     if (abs(new_x-self.x) !=0 and abs(new_y-self.y)==0) or(abs(new_x-self.x) ==0 and abs(new_y-self.y)!=0):
    #         self.x,self.y = new_x, new_y
    def is_can_move(self,new_pos):

        direction = get_direction((self.x, self.y), new_pos)
        if direction and len(direction.split()) == 1:
            res = has_chessmate_on_way((self.x, self.y), new_pos, direction)
            if res == "take":
                take_chessman(new_pos)
                return True
            if not res:
                return True
            else:
                return False
class Horse(ChessMan):
    def __init__(self,x,y,color):
        super(Horse, self).__init__(x,y)
        if color == "black":
            self.image=pics.black_horse
        else:
            self.image=pics.white_horse
    def move(self,new_x,new_y):
        if (abs(new_x-self.x) == 1 and abs(new_y-self.y)==2) or (abs(new_x-self.x) == 2 and abs(new_y-self.y)==1):
            self.x,self.y = new_x, new_y
class Bishop(ChessMan):
    def __init__(self,x,y,color):
        super(Bishop, self).__init__(x,y)
        if color == "black":
            self.image=pics.black_bishop
        else:
            self.image=pics.white_bishop
    def move(self,new_pos):
        super(Bishop, self).move(new_pos)
        field.field[self.y][self.x] = (active_player, "b")
    def is_can_move(self, new_pos):
        direction = get_direction((self.x, self.y), new_pos)
        if direction and len(direction.split()) == 2:
            res = has_chessmate_on_way((self.x, self.y), new_pos, direction)
            if res == "take":
                take_chessman(new_pos)
                return True
            if not res:
                return True
            else:
                return False
class Pawn(ChessMan):
    def __init__(self,x,y,color):
        super(Pawn, self).__init__(x,y)
        if color == "black":
            self.image = pics.black_pawn
        else:
            self.image=pics.white_pawn
    def move(self,new_pos):
        super(Pawn, self).move(new_pos)
        field.field[self.y][self.x] = (active_player, "p")
    def is_can_move(self, new_pos):
        if (abs(new_pos[1] - self.y) == 1) or \
                ((abs(new_pos[1] - self.y) == 2) and (self.y ==1 or self.y ==6)):
            direction = get_direction((self.x, self.y), new_pos)
            passing=False
            if looks=="white":
                if active_player=="white":
                    if "up" in direction:
                        passing=True
                else:
                    if "down" in direction:
                        passing = True
            else:
                if active_player == "black":
                    if "up" in direction:
                        passing = True
                else:
                    if "down" in direction:
                        passing = True
            if passing:
                res = has_chessmate_on_way_for_pawn((self.x, self.y), direction,new_pos)
                if res == "take":
                    take_chessman(new_pos)
                    return True
                if not res:
                    return True
                else:
                    return False

class Field:
    def __init__(self,width,height,above_indent=0,left_indent=0):
        self.field = [[0]*width for y in range(height)]
        self.width = width
        self.height = height
        self.cell_size_x = (screen_width-left_indent)//width
        self.cell_size_y = (screen_height-above_indent)//height
        self.above_indent=above_indent
        self.left_indent=left_indent
    def create_chessmans(self):

        self.white_king = Pawn(4,7,        "white")
        self.white_chessmans=[self.white_king]
        self.black_king = Pawn(3,0,        "black")
        self.black_chessmans=[self.black_king]
        self.field[7][4] = ["white","p"]
        self.field[0][3] = ["black","p"]
        # self.white_queen = Queen(3,7,      "white")
        # self.white_castle_l = Castle(0,7,  "white")
        # self.white_horse_l = Horse(1,7,    "white")
        # self.white_bishop_l = Bishop(2,7,  "white")
        # self.white_bishop_r = Bishop(5, 7, "white")
        # self.white_horse_r = Horse(6, 7,   "white")
        # self.white_castle_r = Castle(7, 7, "white")
        # self.white_chessmans=[self.white_king,self.white_queen,self.white_castle_l,self.white_horse_l,self.white_bishop_l,
        #                 self.white_castle_r,self.white_horse_r,self.white_bishop_r]
        # for i in range(8):
        #     white_pawn = Pawn(i, 6, "white")
        #     self.white_chessmans.append(white_pawn)
        # self.black_king = King(4, 0,       "black")
        # self.black_queen = Queen(3, 0,     "black")
        # self.black_castle_l = Castle(0,0, "black")
        # self.black_horse_l = Horse(1, 0,   "black")
        # self.black_bishop_l = Bishop(2, 0, "black")
        # self.black_bishop_r = Bishop(5, 0, "black")
        # self.black_horse_r = Horse(6, 0,   "black")
        # self.black_castle_r = Castle(7, 0, "black")
        # self.black_chessmans = [self.black_king, self.black_queen, self.black_castle_l, self.black_horse_l,
        #                         self.black_bishop_l,
        #                         self.black_castle_r, self.black_horse_r, self.black_bishop_r]
        # for i in range(8):
        #     black_pawn = Pawn(i, 1, "black")
        #     self.black_chessmans.append(black_pawn)
        # self.field[0][0] =("black","c")
        # self.field[0][1] =("black","h")
        # self.field[0][2] =("black","b")
        # self.field[0][3] =("black","q")
        # self.field[0][4] =("black","k")
        # self.field[0][5] =("black","b")
        # self.field[0][6] =("black","h")
        # self.field[0][7] =("black","c")
        # self.field[7][0] = ("white", "c")
        # self.field[7][1] = ("white", "h")
        # self.field[7][2] = ("white", "b")
        # self.field[7][3] = ("white", "q")
        # self.field[7][4] = ("white", "k")
        # self.field[7][5] = ("white", "b")
        # self.field[7][6] = ("white", "h")
        # self.field[7][7] = ("white", "c")
        # for i in range(8):
        #     self.field[1][i] = ("black", "p")
        # for i in range(8):
        #     self.field[6][i] = ("white", "p")
    def draw(self):
        for y in range(self.above_indent,screen_height,self.cell_size_y):
            pygame.draw.line(screen, black_color,(self.left_indent,y),(screen_width,y))
        for x in range(self.left_indent,screen_width,self.cell_size_x):
            pygame.draw.line(screen, black_color,(x,self.above_indent),(x,screen_height))
        cell = 0
        for y in range(self.above_indent,screen_height,self.cell_size_y):
            for x in range(self.left_indent, screen_width, self.cell_size_x):
                cell += 1
                if cell %2==0:
                    pygame.draw.rect(screen,black_color,(x,y,field.cell_size_x,field.cell_size_y))
                else:
                    continue
        if active_cell:
            pos = coordinates_changer_in_pygame(active_cell[0],active_cell[1])
            pygame.draw.rect(screen,yellow_color,(pos[0],pos[1],self.cell_size_x,self.cell_size_y),6)

        for chessmate in self.white_chessmans:
            screen.blit(chessmate.image,coordinates_changer_in_pygame(chessmate.x,chessmate.y))
        for chessmate in self.black_chessmans:
            screen.blit(chessmate.image,coordinates_changer_in_pygame(chessmate.x,chessmate.y))

class Pics:
    def __init__(self,width,height):
        self.white_king = pygame.image.load("images/white_king.png")
        self.white_king= pygame.transform.scale(self.white_king, (width, height))
        self.black_king = pygame.image.load("images/black_king.png")
        self.black_king =pygame.transform.scale(self.black_king, (width, height))

        self.white_queen = pygame.image.load("images/white_queen.png")
        self.white_queen=pygame.transform.scale(self.white_queen, (width, height))
        self.black_queen = pygame.image.load("images/black_queen.png")
        self.black_queen=pygame.transform.scale(self.black_queen, (width, height))

        self.white_castle = pygame.image.load("images/white_castle.png")
        self.white_castle=pygame.transform.scale(self.white_castle, (width, height))
        self.black_castle = pygame.image.load("images/black_castle.png")
        self.black_castle=pygame.transform.scale(self.black_castle, (width, height))

        self.white_horse = pygame.image.load("images/white_horse.png")
        self.white_horse=pygame.transform.scale(self.white_horse, (width, height))
        self.black_horse = pygame.image.load("images/black_horse.png")
        self.black_horse=pygame.transform.scale(self.black_horse, (width, height))

        self.white_bishop = pygame.image.load("images/white_bishop.png")
        self.white_bishop=pygame.transform.scale(self.white_bishop, (width, height))
        self.black_bishop = pygame.image.load("images/black_bishop.png")
        self.black_bishop=pygame.transform.scale(self.black_bishop, (width, height))

        self.white_pawn = pygame.image.load("images/white_pawn.png")
        self.white_pawn=pygame.transform.scale(self.white_pawn, (width, height))
        self.black_pawn = pygame.image.load("images/black_pawn.png")
        self.black_pawn=pygame.transform.scale(self.black_pawn, (width, height))
def is_correct(pos):
    if field.left_indent < pos[0] < screen_width and field.above_indent < pos[1] < screen_height:
        return True
    return False
def coordinates_changer(pos):
    new_x = (pos[0] - field.left_indent)//field.cell_size_x
    new_y = (pos[1] - field.above_indent)//field.cell_size_y
    return (new_x,new_y)
def coordinates_changer_in_pygame(x,y):
    new_x = x*field.cell_size_x+field.left_indent
    new_y = y*field.cell_size_y+field.above_indent
    return(new_x,new_y)
def is_touch_chessman(new_pos):
    if field.field[new_pos[1]][new_pos[0]] !=0:
        return True
    return False
def choose_chessman(pos):
    return field.field[pos[1]][pos[0]]
def is_your_chessman_touched(pos):
    if field.field[pos[1]][pos[0]][0] == active_player:
        return True
    else:
        return False
def change_player():
    global active_player
    if active_player == "white":
        active_player = "black"
    else:
        active_player = "white"
def move(pos,new_pos,active_chessman):
    is_move=False
    if active_chessman[0] == "white":
        for chessman in field.white_chessmans:
            if pos[0] == chessman.x and pos[1] == chessman.y:
                if pos[0]==3 and pos[1]==5:
                    print("asd")
                if chessman.is_can_move(new_pos):
                    chessman.move(new_pos)
                    is_move=True
                    break
    else:
        for chessman in field.black_chessmans:
            if pos[0] == chessman.x and pos[1] == chessman.y:
                if chessman.is_can_move(new_pos):
                    chessman.move(new_pos)
                    is_move = True
                    break
    if is_move:
        change_player()
        return True

def events_check():
    global process_running, active_cell,active_chessman,active_player
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            process_running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                process_running = False
        elif event.type== pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pos = pygame.mouse.get_pos()
                if is_correct(pos):
                    new_pos = coordinates_changer(pos)
                    if not active_chessman:
                        print("active chessman")

                        if is_touch_chessman(new_pos):
                            if is_your_chessman_touched(new_pos):
                                print("make active")
                                active_chessman = choose_chessman(new_pos)
                                active_cell = new_pos

                    else:
                        if is_touch_chessman(new_pos):
                            if is_your_chessman_touched(new_pos):
                                if new_pos == active_cell:
                                    active_chessman=None
                                # active_chessman = choose_chessman(new_pos)
                                    active_cell = None
                                    continue
                        print("progress")
                        res = move(active_cell,new_pos,active_chessman)
                        if res:
                            active_chessman=None
                            active_cell = None
def drawing():
    screen.fill(white_color)
    field.draw()
    pygame.display.update()
def mainloop():
    while process_running:
        events_check()
        drawing()
        print(active_chessman)
        pygame.time.delay(20)
if __name__ == '__main__':
    field = Field(8,8,40,20)
    pics=Pics(field.cell_size_x,field.cell_size_y)
    field.create_chessmans()
    # for i in

    mainloop()