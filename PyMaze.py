from sys import argv
import pygame
from pygame.locals import *
# from maze import Maze
from renderMaze import Maze

class Game:

    def __init__(self, diff, dim, path):
        self.size = (1200,900)
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption('Maze Demo')

        font = pygame.font.SysFont(pygame.font.get_default_font(), 55)
        text = font.render("Loading...", 1, (255,255,255))
        rect = text.get_rect()
        rect.center = self.size[0]/2, self.size[1]/2
        self.screen.blit(text, rect)
        pygame.display.update(rect)

        self.diff = diff
        self.dim = map(int, dim.split('x'))
        self.path = path

        self.cx = 0
        self.cy = 0

    def start(self):
        self.maze_obj = Maze(*self.dim)# pass args to change maze size: Maze(10, 10)
        if self.diff == 0:
            # self.maze_obj.dfs_generate((0, 0))
            self.maze_obj.random_kruskal_generate()
        else:
            self.maze_obj.dfs_generate((0, 0))
        self.draw_maze()
        self.reset_player()
        self.loop()

    def reset_player(self):
        # Make the sprites for the player.
        w, h = self.cell_width - 3, self.cell_height - 3
        rect = 0, 0, w, h
        base = pygame.Surface((w,h))
        base.fill( (255,255,255) )
        self.red_p = base.copy()
        self.green_p = base.copy()
        self.blue_p = base.copy()
        self.goldy = base.copy()
        if self.path == 1:
            r = (255,0,0)
            g = (0,255,0)
        else:
            r = g = (255,255,255)
        b = (0,0,255)
        gold = (0xc5,0x93,0x48)
        pygame.draw.ellipse(self.red_p, r, rect)
        pygame.draw.ellipse(self.green_p, g, rect)
        pygame.draw.ellipse(self.blue_p, b, rect)
        pygame.draw.ellipse(self.goldy, gold, rect)

        # Make a same-size matrix for the player.
        self.player_maze = {}
        for y in range(self.maze_obj.m):
            for x in range(self.maze_obj.n):
                cell = {'visited' : 0} # if 1, draws green. if >= 2, draws red.
                self.player_maze[(x,y)] = cell
                self.screen.blit(base, (x*self.cell_width+2, y*self.cell_height+2))

        self.screen.blit(self.goldy, (x*self.cell_width+2, y*self.cell_height+2))

        self.cx = 0
        self.cy = 0

        self.curr_cell = self.player_maze[(self.cx, self.cy)] # starts at origin

        self.last_move = None # For last move fun

    def draw_maze(self):
        self.screen.fill( (255,255,255) )
        '''
        self.cell_width = self.size[0]/self.maze_obj.cols
        self.cell_height = self.size[1]/self.maze_obj.rows
        '''
        self.cell_width = self.size[0]/self.maze_obj.n
        self.cell_height = self.size[1]/self.maze_obj.m

        for y in range(self.maze_obj.m):
            for x in range(self.maze_obj.n):
                if not self.maze_obj.D[y][x]:  # draw south wall
                    pygame.draw.line(self.screen, (0,0,0), \
                        (x*self.cell_width, y*self.cell_height + self.cell_height), \
                        (x*self.cell_width + self.cell_width, \
                        y*self.cell_height + self.cell_height) )
                if not self.maze_obj.R[y][x]:  # draw east wall
                    pygame.draw.line(self.screen, (0,0,0), \
                        (x*self.cell_width + self.cell_width, y*self.cell_height), \
                        (x*self.cell_width + self.cell_width, y*self.cell_height + \
                        self.cell_height) )
        # Screen border
        pygame.draw.rect(self.screen, (0,0,0), (0,0, self.size[0], self.size[1]), 1)
        pygame.display.update()

    def loop(self):
        self.clock = pygame.time.Clock()
        self.keep_going = 1

        while self.keep_going:
            moved = 0
            self.clock.tick(10)
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.keep_going = 0
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.keep_going = 0
                    if event.key == K_r:
                        self.reset_player()
                    if event.key == K_DOWN:
                        self.move_player('d')
                        moved = 1
                    if event.key == K_UP:
                        self.move_player('u')
                        moved = 1
                    if event.key == K_LEFT:
                        self.move_player('l')
                        moved = 1
                    if event.key == K_RIGHT:
                        self.move_player('r')
                        moved = 1
            keys = pygame.key.get_pressed()
            if not moved:
                if keys[K_DOWN]:
                    self.move_player('d')
                if keys[K_UP]:
                    self.move_player('u')
                if keys[K_LEFT]:
                    self.move_player('l')
                if keys[K_RIGHT]:
                    self.move_player('r')

            self.draw_player()
            pygame.display.update()

    def move_player(self, dir):
        no_move = 0
        try:
            if dir == 'u':
                if self.maze_obj.D[self.cy-1][self.cx]:
                    self.cy -= 1
                    self.curr_cell['visited'] += 1
                else: no_move = 1
            elif dir == 'd':
                if self.maze_obj.D[self.cy][self.cx]:
                    self.cy += 1
                    self.curr_cell['visited'] += 1
                else: no_move = 1
            elif dir == 'l':
                if self.maze_obj.R[self.cy][self.cx-1]:
                    self.cx -= 1
                    self.curr_cell['visited'] += 1
                else: no_move = 1
            elif dir == 'r':
                if self.maze_obj.R[self.cy][self.cx ]:
                    self.cx += 1
                    self.curr_cell['visited'] += 1
                else: no_move = 1
            else:
                no_move = 1
        except KeyError: # Tried to move outside screen
            no_move = 1


        # Handle last move...
        if ((dir == 'u' and self.last_move == 'd') or \
                (dir == 'd' and self.last_move == 'u') or \
                (dir == 'l' and self.last_move == 'r') or \
                (dir == 'r' and self.last_move == 'l')) and \
                not no_move:
            self.curr_cell['visited'] += 1

        if not no_move:
            self.last_move = dir
            self.curr_cell = self.player_maze[(self.cx, self.cy)]

        # Check for victory.
        # if self.cx + 1 == self.maze_obj.cols and self.cy + 1 == self.maze_obj.rows:
        # print((self.cx+1, self.cy+1,self.maze_obj.m, self.maze_obj.n))
        if self.cx + 1 == self.maze_obj.n and self.cy + 1 == self.maze_obj.m:
            print ('Congratumalations, you beat this maze.')
            self.keep_going = 0

    def draw_player(self):
        for y in range(self.maze_obj.m):
            for x in range(self.maze_obj.n):
                if self.player_maze[(x,y)]['visited'] > 0:
                    if self.player_maze[(x,y)]['visited'] == 1:
                        circ = self.green_p
                    else:
                        circ = self.red_p
                    # draw green circles
                    self.screen.blit(circ, (x*self.cell_width+2, y*self.cell_height+2))
        self.screen.blit(self.blue_p, (self.cx*self.cell_width+2, \
                self.cy*self.cell_height+2))

if __name__ == '__main__':
    pygame.init()
    args = argv[1:]
    diff = 0
    dim = '60x80'
    path = 1
    for arg in args:
        if '--diff' in arg:
            diff = int(arg.split('=')[-1])
        elif '--dim' in arg:
            dim = arg.split('=')[-1]
        elif '--path' in arg:
            path = int(arg.split('=')[-1])

    g = Game(diff, dim, path)
    g.start()
