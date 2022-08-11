import pygame
pygame.init()
clock = pygame.time.Clock()
screen_width = 720
screen_height = 720
screen = pygame.display.set_mode((screen_width,screen_height))
black_color = (0,0,0)
white_color = (255,255,255)
process_running = True
class Field:
    def __init__(self,width,height,above_indent=0):
        self.field = [[0]*width for y in range(height)]
        self.width = width
        self.height = height
        self.cell_size_x = screen_width//width
        self.cell_size_y = (screen_height-above_indent)//height
        self.above_indent=above_indent
    def draw(self):
        for y in range(self.above_indent,screen_height+1,self.cell_size_y):
            pygame.draw.line(screen, black_color,(0,y),(screen_width,y))
        for x in range(0,screen_width+1,self.cell_size_x):
            pygame.draw.line(screen, black_color,(x,self.above_indent),(x,screen_height))
def events_check():
    global process_running, scale, scale_value, objects,camera_center_x,camera_center_y,scale_number
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            process_running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                process_running = False
def drawing():
    screen.fill(white_color)
    field.draw()
    pygame.display.update()
def mainloop():
    while process_running:
        events_check()
        drawing()
        pygame.time.delay(20)
if __name__ == '__main__':
    field = Field(8,8,20)
    mainloop()