import pygame
import math
from datetime import datetime
def start_text(app,pos):app.text_mode=True;app.text_pos=pos;app.text_input=""
def finalize_text(app):
    if app.text_input:text_surface=app.text_font.render(app.text_input,True,app.get_current_color());app.canvas.blit(text_surface,app.text_pos)
    app.text_mode=False
def cancel_text(app):app.text_mode=False;app.text_input=""
def start_line(app,pos):app.line_drawing=True;app.start_x=pos[0];app.start_y=pos[1]
def finalize_line(app):
    mouse_pos=pygame.mouse.get_pos()
    color=app.get_current_color()
    pygame.draw.line(app.canvas,color,(app.start_x,app.start_y),mouse_pos,app.brush_size)
    app.line_drawing=False
def flood_fill(app,pos):
    x,y=pos
    w=app.canvas.get_width()
    h=app.canvas.get_height()
    if not(0<=x<w and 0<=y<h):return
    target=app.canvas.get_at((x,y))
    fill=app.get_current_color()
    if target==fill:return
    stack=[(x,y)]
    while stack:
        cx,cy=stack.pop()
        if not(0<=cx<w and 0<=cy<h):continue
        if app.canvas.get_at((cx,cy))!=target:continue
        app.canvas.set_at((cx,cy),fill)
        stack.extend([(cx+1,cy),(cx-1,cy),(cx,cy+1),(cx,cy-1)])
def save_canvas(app):
    timestamp=datetime.now().strftime("%Y%m%d_%H%M%S")
    filename=f"canvas_{timestamp}.png"
    pygame.image.save(app.canvas,filename)
    print(f"Saved canvas as {filename}")
def draw_brush(app,pos):
    color=app.get_current_color()
    pygame.draw.line(app.canvas,color,(app.prev_x,app.prev_y),(pos[0],pos[1]),app.brush_size)
    app.prev_x=pos[0]
    app.prev_y=pos[1]
def draw_rectangle(app):
    color=app.get_current_color()
    mouse_pos=pygame.mouse.get_pos()
    x1,y1=app.start_x,app.start_y
    x2,y2=mouse_pos[0],mouse_pos[1]
    x=min(x1,x2)
    y=min(y1,y2)
    width=abs(x2-x1)
    height=abs(y2-y1)
    temp=app.canvas.copy()
    pygame.draw.rect(temp,color,(x,y,width,height),app.brush_size)
    return temp
def finalize_rectangle(app):
    color=app.get_current_color()
    mouse_pos=pygame.mouse.get_pos()
    x1,y1=app.start_x,app.start_y
    x2,y2=mouse_pos[0],mouse_pos[1]
    x=min(x1,x2)
    y=min(y1,y2)
    width=abs(x2-x1)
    height=abs(y2-y1)
    pygame.draw.rect(app.canvas,color,(x,y,width,height),app.brush_size)
def draw_circle(app):
    color=app.get_current_color()
    mouse_pos=pygame.mouse.get_pos()
    dx=mouse_pos[0]-app.start_x
    dy=mouse_pos[1]-app.start_y
    radius=max(1,int((dx**2+dy**2)**0.5))
    temp=app.canvas.copy()
    if radius>0:pygame.draw.circle(temp,color,(app.start_x,app.start_y),radius,app.brush_size)
    return temp
def finalize_circle(app):
    color=app.get_current_color()
    mouse_pos=pygame.mouse.get_pos()
    dx=mouse_pos[0]-app.start_x
    dy=mouse_pos[1]-app.start_y
    radius=max(1,int((dx**2+dy**2)**0.5))
    if radius>0:pygame.draw.circle(app.canvas,color,(app.start_x,app.start_y),radius,app.brush_size)
def draw_right_triangle(app):
    color=app.get_current_color()
    mouse_pos=pygame.mouse.get_pos()
    x1,y1=app.start_x,app.start_y
    x2,y2=mouse_pos[0],mouse_pos[1]
    points=[(x1,y1),(x2,y1),(x1,y2)]
    temp=app.canvas.copy()
    pygame.draw.polygon(temp,color,points,app.brush_size)
    return temp
def finalize_right_triangle(app):
    color=app.get_current_color()
    mouse_pos=pygame.mouse.get_pos()
    x1,y1=app.start_x,app.start_y
    x2,y2=mouse_pos[0],mouse_pos[1]
    points=[(x1,y1),(x2,y1),(x1,y2)]
    pygame.draw.polygon(app.canvas,color,points,app.brush_size)
def draw_equilateral_triangle(app):
    color=app.get_current_color()
    mouse_pos=pygame.mouse.get_pos()
    x1,y1=app.start_x,app.start_y
    x2,y2=mouse_pos[0],mouse_pos[1]
    dx=x2-x1
    dy=y2-y1
    side=max(10,int((dx**2+dy**2)**0.5))
    height=side*math.sqrt(3)/2
    points=[(x1,y1),(x1+side,y1),(x1+side/2,y1-height)]
    temp=app.canvas.copy()
    pygame.draw.polygon(temp,color,points,app.brush_size)
    return temp
def finalize_equilateral_triangle(app):
    color=app.get_current_color()
    mouse_pos=pygame.mouse.get_pos()
    x1,y1=app.start_x,app.start_y
    x2,y2=mouse_pos[0],mouse_pos[1]
    dx=x2-x1
    dy=y2-y1
    side=max(10,int((dx**2+dy**2)**0.5))
    height=side*math.sqrt(3)/2
    points=[(x1,y1),(x1+side,y1),(x1+side/2,y1-height)]
    pygame.draw.polygon(app.canvas,color,points,app.brush_size)
def draw_rhombus(app):
    color=app.get_current_color()
    mouse_pos=pygame.mouse.get_pos()
    x1,y1=app.start_x,app.start_y
    x2,y2=mouse_pos[0],mouse_pos[1]
    width=abs(x2-x1)
    height=abs(y2-y1)
    cx=(x1+x2)/2
    cy=(y1+y2)/2
    points=[(cx,y1),(x2,cy),(cx,y2),(x1,cy)]
    temp=app.canvas.copy()
    pygame.draw.polygon(temp,color,points,app.brush_size)
    return temp
def finalize_rhombus(app):
    color=app.get_current_color()
    mouse_pos=pygame.mouse.get_pos()
    x1,y1=app.start_x,app.start_y
    x2,y2=mouse_pos[0],mouse_pos[1]
    width=abs(x2-x1)
    height=abs(y2-y1)
    cx=(x1+x2)/2
    cy=(y1+y2)/2
    points=[(cx,y1),(x2,cy),(cx,y2),(x1,cy)]
    pygame.draw.polygon(app.canvas,color,points,app.brush_size)