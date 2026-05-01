import pygame
import sys
import math
from datetime import datetime
import tools
pygame.init()
SCREEN_WIDTH=800
SCREEN_HEIGHT=600
FPS=60
WHITE=(255,255,255)
BLACK=(0,0,0)
RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)
YELLOW=(255,255,0)
CYAN=(0,255,255)
MAGENTA=(255,0,255)
GRAY=(128,128,128)
LIGHT_GRAY=(200,200,200)
screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Paint Application - TSIS2")
clock=pygame.time.Clock()
font=pygame.font.SysFont("Arial",18,bold=True)
small_font=pygame.font.SysFont("Arial",14)
text_font=pygame.font.SysFont("Arial",24)
class PaintApp:
    def __init__(self):
        self.drawing=False
        self.line_drawing=False
        self.text_mode=False
        self.current_color=BLACK
        self.brush_sizes=[2,5,10]
        self.brush_size_index=1
        self.current_tool="pencil"
        self.start_x=0
        self.start_y=0
        self.prev_x=0
        self.prev_y=0
        self.canvas=pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT))
        self.canvas.fill(WHITE)
        self.colors=[BLACK,RED,GREEN,BLUE,YELLOW,CYAN,MAGENTA]
        self.color_index=0
        self.text_input=""
        self.text_pos=(0,0)
        self.text_font=text_font
    
    @property
    def brush_size(self):
        return self.brush_sizes[self.brush_size_index]
    def get_current_color(self):
        return WHITE if self.current_tool=="eraser" else self.colors[self.color_index]
    def handle_events(self):
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                return False
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_p:self.current_tool="pencil"
                elif event.key==pygame.K_l:self.current_tool="line"
                elif event.key==pygame.K_r:self.current_tool="rectangle"
                elif event.key==pygame.K_c:self.current_tool="circle"
                elif event.key==pygame.K_e:self.current_tool="eraser"
                elif event.key==pygame.K_t:self.current_tool="right_triangle"
                elif event.key==pygame.K_y:self.current_tool="equilateral_triangle"
                elif event.key==pygame.K_h:self.current_tool="rhombus"
                elif event.key==pygame.K_f:self.current_tool="fill"
                elif event.key==pygame.K_x:self.current_tool="text"
                elif event.key==pygame.K_F1:self.color_index=0
                elif event.key==pygame.K_F2:self.color_index=1
                elif event.key==pygame.K_F3:self.color_index=2
                elif event.key==pygame.K_F4:self.color_index=3
                elif event.key==pygame.K_F5:self.color_index=4
                elif event.key==pygame.K_F6:self.color_index=5
                elif event.key==pygame.K_F7:self.color_index=6
                elif event.key==pygame.K_1:self.brush_size_index=0
                elif event.key==pygame.K_2:self.brush_size_index=1
                elif event.key==pygame.K_3:self.brush_size_index=2
                elif event.key==pygame.K_s and pygame.key.get_mods()&pygame.KMOD_CTRL:tools.save_canvas(self)
                elif event.key==pygame.K_DELETE:self.canvas.fill(WHITE)
                if self.text_mode:
                    if event.key==pygame.K_RETURN:tools.finalize_text(self)
                    elif event.key==pygame.K_ESCAPE:tools.cancel_text(self)
                    elif event.key==pygame.K_BACKSPACE:self.text_input=self.text_input[:-1]
                    else:
                        char=event.unicode
                        if char:self.text_input+=char
            
            elif event.type==pygame.MOUSEBUTTONDOWN:
                if event.button==1:
                    palette_x=SCREEN_WIDTH-200
                    palette_y=10
                    for i in range(len(self.colors)):
                        rect=pygame.Rect(palette_x+i*25,palette_y+25,20,20)
                        if rect.collidepoint(event.pos):self.color_index=i;break
                    brush_y=palette_y+55
                    for i in range(len(self.brush_sizes)):
                        rect=pygame.Rect(palette_x+i*25,brush_y+25,20,20)
                        if rect.collidepoint(event.pos):self.brush_size_index=i;break
                    if self.current_tool=="text":
                        if not self.text_mode:tools.start_text(self,event.pos)
                    elif self.current_tool=="fill":tools.flood_fill(self,event.pos)
                    elif self.current_tool=="line":
                        if not self.line_drawing:tools.start_line(self,event.pos)
                        else:tools.finalize_line(self)
                    else:
                        self.drawing=True
                        self.start_x=event.pos[0]
                        self.start_y=event.pos[1]
                        self.prev_x=event.pos[0]
                        self.prev_y=event.pos[1]
            elif event.type==pygame.MOUSEBUTTONUP:
                if event.button==1:
                    if self.drawing and self.current_tool not in["pencil","eraser","line"]:
                        if self.current_tool=="rectangle":tools.finalize_rectangle(self)
                        elif self.current_tool=="circle":tools.finalize_circle(self)
                        elif self.current_tool=="right_triangle":tools.finalize_right_triangle(self)
                        elif self.current_tool=="equilateral_triangle":tools.finalize_equilateral_triangle(self)
                        elif self.current_tool=="rhombus":tools.finalize_rhombus(self)
                    self.drawing=False
            elif event.type==pygame.MOUSEMOTION:
                if self.drawing and self.current_tool in["pencil","eraser"]:tools.draw_brush(self,event.pos)
        return True
    def update(self):pass
    def render(self,screen):
        screen.blit(self.canvas,(0,0))
        if self.drawing:
            if self.current_tool=="rectangle":preview=tools.draw_rectangle(self);screen.blit(preview,(0,0))
            elif self.current_tool=="circle":preview=tools.draw_circle(self);screen.blit(preview,(0,0))
            elif self.current_tool=="right_triangle":preview=tools.draw_right_triangle(self);screen.blit(preview,(0,0))
            elif self.current_tool=="equilateral_triangle":preview=tools.draw_equilateral_triangle(self);screen.blit(preview,(0,0))
            elif self.current_tool=="rhombus":preview=tools.draw_rhombus(self);screen.blit(preview,(0,0))
        if self.line_drawing:
            mouse_pos=pygame.mouse.get_pos()
            temp_surface=self.canvas.copy()
            pygame.draw.line(temp_surface,self.get_current_color(),(self.start_x,self.start_y),mouse_pos,self.brush_size)
            screen.blit(temp_surface,(0,0))
        if self.text_mode:
            cursor_x=self.text_pos[0]+text_font.size(self.text_input)[0]
            cursor_y=self.text_pos[1]
            pygame.draw.line(screen,BLACK,(cursor_x,cursor_y),(cursor_x,cursor_y+text_font.get_height()),2)
            if self.text_input:text_surface=text_font.render(self.text_input,True,self.get_current_color());screen.blit(text_surface,self.text_pos)
        self.draw_ui(screen)
        pygame.display.flip()
    def draw_ui(self,screen):
        tool_text=font.render(f"Tool: {self.current_tool.upper()}",True,BLACK)
        screen.blit(tool_text,(10,10))
        color_name={0:"Black",1:"Red",2:"Green",3:"Blue",4:"Yellow",5:"Cyan",6:"Magenta"}
        color_text=font.render(f"Color: {color_name[self.color_index]}",True,BLACK)
        screen.blit(color_text,(10,35))
        size_text=font.render(f"Size: {self.brush_size}",True,BLACK)
        screen.blit(size_text,(10,60))
        palette_x=SCREEN_WIDTH-200
        palette_y=10
        palette_text=small_font.render("Colors (F1-F7):",True,BLACK)
        screen.blit(palette_text,(palette_x,palette_y))
        for i,color in enumerate(self.colors):
            rect=pygame.Rect(palette_x+i*25,palette_y+25,20,20)
            pygame.draw.rect(screen,color,rect)
            pygame.draw.rect(screen,BLACK,rect,2)
        brush_y=palette_y+55
        brush_text=small_font.render("Size (1-3):",True,BLACK)
        screen.blit(brush_text,(palette_x,brush_y))
        for i,size in enumerate(self.brush_sizes):
            rect=pygame.Rect(palette_x+i*25,brush_y+25,20,20)
            pygame.draw.rect(screen,LIGHT_GRAY if i==self.brush_size_index else GRAY,rect)
            pygame.draw.rect(screen,BLACK,rect,2)
            size_text=small_font.render(str(size),True,BLACK)
            screen.blit(size_text,(rect.centerx-size_text.get_width()//2,rect.centery-size_text.get_height()//2))
        instructions=["P: Pencil | L: Line | R: Rectangle | C: Circle | E: Eraser","T: Right Triangle | Y: Equilateral Triangle | H: Rhombus","F: Fill | X: Text | F1-F7: Colors | 1-3: Size","Ctrl+S: Save | DEL: Clear"]
        for i,instruction in enumerate(instructions):text=small_font.render(instruction,True,GRAY);screen.blit(text,(10,SCREEN_HEIGHT-70+i*20))


def main():
    app=PaintApp()
    running=True
    while running:
        running=app.handle_events()
        app.update()
        app.render(screen)
        clock.tick(FPS)
    pygame.quit()
    sys.exit()
if __name__=="__main__":main()