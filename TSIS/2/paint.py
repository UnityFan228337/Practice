import pygame
import sys
import math
from datetime import datetime

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Paint Application - TSIS2")
clock = pygame.time.Clock()

# Fonts
font = pygame.font.SysFont("Arial", 18, bold=True)
small_font = pygame.font.SysFont("Arial", 14)
text_font = pygame.font.SysFont("Arial", 24)

# Paint application state
class PaintApp:
    def __init__(self):
        self.drawing = False
        self.line_drawing = False
        self.text_mode = False
        self.current_color = BLACK
        self.brush_sizes = [2, 5, 10]
        self.brush_size_index = 1  # medium
        self.current_tool = "pencil"  # pencil, line, rectangle, circle, eraser, right_triangle, equilateral_triangle, rhombus, fill, text
        self.start_x = 0
        self.start_y = 0
        self.prev_x = 0
        self.prev_y = 0
        self.canvas = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.canvas.fill(WHITE)
        self.colors = [BLACK, RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA]
        self.color_index = 0
        self.text_input = ""
        self.text_pos = (0, 0)
    
    @property
    def brush_size(self):
        return self.brush_sizes[self.brush_size_index]
    
    def get_current_color(self):
        if self.current_tool == "eraser":
            return WHITE
        return self.colors[self.color_index]
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.KEYDOWN:
                # Tool selection
                if event.key == pygame.K_p:
                    self.current_tool = "pencil"
                elif event.key == pygame.K_l:
                    self.current_tool = "line"
                elif event.key == pygame.K_r:
                    self.current_tool = "rectangle"
                elif event.key == pygame.K_c:
                    self.current_tool = "circle"
                elif event.key == pygame.K_e:
                    self.current_tool = "eraser"
                elif event.key == pygame.K_t:
                    self.current_tool = "right_triangle"
                elif event.key == pygame.K_y:
                    self.current_tool = "equilateral_triangle"
                elif event.key == pygame.K_h:
                    self.current_tool = "rhombus"
                elif event.key == pygame.K_f:
                    self.current_tool = "fill"
                elif event.key == pygame.K_x:
                    self.current_tool = "text"
                
                # Color selection
                elif event.key == pygame.K_1:
                    self.color_index = 0
                elif event.key == pygame.K_2:
                    self.color_index = 1
                elif event.key == pygame.K_3:
                    self.color_index = 2
                elif event.key == pygame.K_4:
                    self.color_index = 3
                elif event.key == pygame.K_5:
                    self.color_index = 4
                elif event.key == pygame.K_6:
                    self.color_index = 5
                elif event.key == pygame.K_7:
                    self.color_index = 6
                
                # Brush size
                elif event.key == pygame.K_F1:
                    self.brush_size_index = 0  # small
                elif event.key == pygame.K_F2:
                    self.brush_size_index = 1  # medium
                elif event.key == pygame.K_F3:
                    self.brush_size_index = 2  # large
                
                # Save
                elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    self.save_canvas()
                
                # Clear canvas
                elif event.key == pygame.K_DELETE:
                    self.canvas.fill(WHITE)
                
                # Text input
                if self.text_mode:
                    if event.key == pygame.K_RETURN:
                        self.finalize_text()
                    elif event.key == pygame.K_ESCAPE:
                        self.cancel_text()
                    elif event.key == pygame.K_BACKSPACE:
                        self.text_input = self.text_input[:-1]
                    else:
                        char = event.unicode
                        if char:
                            self.text_input += char
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    if self.current_tool == "text":
                        if not self.text_mode:
                            self.start_text(event.pos)
                        # else: continue typing
                    elif self.current_tool == "fill":
                        self.flood_fill(event.pos)
                    elif self.current_tool == "line":
                        if not self.line_drawing:
                            self.start_line(event.pos)
                        else:
                            self.finalize_line(event.pos)
                    else:
                        self.drawing = True
                        self.start_x = event.pos[0]
                        self.start_y = event.pos[1]
                        self.prev_x = event.pos[0]
                        self.prev_y = event.pos[1]
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if self.drawing and self.current_tool not in ["pencil", "eraser", "line"]:
                        # Finalize shape drawing
                        if self.current_tool == "rectangle":
                            self.finalize_rectangle()
                        elif self.current_tool == "circle":
                            self.finalize_circle()
                        elif self.current_tool == "right_triangle":
                            self.finalize_right_triangle()
                        elif self.current_tool == "equilateral_triangle":
                            self.finalize_equilateral_triangle()
                        elif self.current_tool == "rhombus":
                            self.finalize_rhombus()
                        self.drawing = False
            
            elif event.type == pygame.MOUSEMOTION:
                if self.drawing and self.current_tool in ["pencil", "eraser"]:
                    self.draw_brush(event.pos)
        
        return True
    
    def start_text(self, pos):
        self.text_mode = True
        self.text_pos = pos
        self.text_input = ""
    
    def finalize_text(self):
        if self.text_input:
            text_surface = text_font.render(self.text_input, True, self.get_current_color())
            self.canvas.blit(text_surface, self.text_pos)
        self.text_mode = False
    
    def cancel_text(self):
        self.text_mode = False
        self.text_input = ""
    
    def start_line(self, pos):
        self.line_drawing = True
        self.start_x = pos[0]
        self.start_y = pos[1]
    
    def finalize_line(self):
        mouse_pos = pygame.mouse.get_pos()
        color = self.get_current_color()
        pygame.draw.line(self.canvas, color, (self.start_x, self.start_y), mouse_pos, self.brush_size)
        self.line_drawing = False
    
    def flood_fill(self, pos):
        x, y = pos
        if not (0 <= x < SCREEN_WIDTH and 0 <= y < SCREEN_HEIGHT):
            return
        
        target_color = self.canvas.get_at((x, y))
        fill_color = self.get_current_color()
        if target_color == fill_color:
            return
        
        # Simple flood fill using stack
        stack = [(x, y)]
        while stack:
            cx, cy = stack.pop()
            if not (0 <= cx < SCREEN_WIDTH and 0 <= cy < SCREEN_HEIGHT):
                continue
            if self.canvas.get_at((cx, cy)) != target_color:
                continue
            self.canvas.set_at((cx, cy), fill_color)
            stack.extend([(cx+1, cy), (cx-1, cy), (cx, cy+1), (cx, cy-1)])
    
    def save_canvas(self):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"canvas_{timestamp}.png"
        pygame.image.save(self.canvas, filename)
        print(f"Saved canvas as {filename}")
    
    def draw_brush(self, pos):
        """Draw with brush tool"""
        color = self.get_current_color()
        # Draw line from previous position to current position
        self.draw_line_segment(self.prev_x, self.prev_y, pos[0], pos[1], color)
        self.prev_x = pos[0]
        self.prev_y = pos[1]
    
    def draw_line_segment(self, x1, y1, x2, y2, color):
        """Draw a line segment by interpolating circles"""
        dx = x2 - x1
        dy = y2 - y1
        distance = math.sqrt(dx * dx + dy * dy)
        
        if distance == 0:
            pygame.draw.circle(self.canvas, color, (int(x1), int(y1)), self.brush_size)
            return
        
        # Number of steps to draw between points
        steps = int(distance) + 1
        for i in range(steps):
            t = i / steps if steps > 0 else 0
            x = int(x1 + dx * t)
            y = int(y1 + dy * t)
            pygame.draw.circle(self.canvas, color, (x, y), self.brush_size)
    
    def draw_rectangle(self):
        """Draw rectangle from start to current mouse position"""
        color = self.get_current_color()
        mouse_pos = pygame.mouse.get_pos()
        x1, y1 = self.start_x, self.start_y
        x2, y2 = mouse_pos[0], mouse_pos[1]
        
        # Normalize coordinates so x1,y1 is top-left
        x = min(x1, x2)
        y = min(y1, y2)
        width = abs(x2 - x1)
        height = abs(y2 - y1)
        
        # Create temporary surface to show preview
        temp_surface = self.canvas.copy()
        pygame.draw.rect(temp_surface, color, (x, y, width, height), self.brush_size)
        return temp_surface
    
    def finalize_rectangle(self):
        """Finalize rectangle drawing"""
        color = self.get_current_color()
        mouse_pos = pygame.mouse.get_pos()
        x1, y1 = self.start_x, self.start_y
        x2, y2 = mouse_pos[0], mouse_pos[1]
        
        # Normalize coordinates so x1,y1 is top-left
        x = min(x1, x2)
        y = min(y1, y2)
        width = abs(x2 - x1)
        height = abs(y2 - y1)
        
        pygame.draw.rect(self.canvas, color, (x, y, width, height), self.brush_size)
    
    def draw_circle(self):
        """Draw circle from start to current mouse position"""
        color = self.get_current_color()
        mouse_pos = pygame.mouse.get_pos()
        dx = mouse_pos[0] - self.start_x
        dy = mouse_pos[1] - self.start_y
        radius = max(1, int((dx ** 2 + dy ** 2) ** 0.5))
        
        # Create temporary surface to show preview
        temp_surface = self.canvas.copy()
        if radius > 0:
            pygame.draw.circle(temp_surface, color, (self.start_x, self.start_y), radius, self.brush_size)
        return temp_surface
    
    def finalize_circle(self):
        """Finalize circle drawing"""
        color = self.get_current_color()
        mouse_pos = pygame.mouse.get_pos()
        dx = mouse_pos[0] - self.start_x
        dy = mouse_pos[1] - self.start_y
        radius = max(1, int((dx ** 2 + dy ** 2) ** 0.5))
        if radius > 0:
            pygame.draw.circle(self.canvas, color, (self.start_x, self.start_y), radius, self.brush_size)
    
    def draw_right_triangle(self):
        """Draw right triangle from start to current mouse position"""
        color = self.get_current_color()
        mouse_pos = pygame.mouse.get_pos()
        x1, y1 = self.start_x, self.start_y
        x2, y2 = mouse_pos[0], mouse_pos[1]
        
        # Points: (x1,y1), (x2,y1), (x1,y2)
        points = [(x1, y1), (x2, y1), (x1, y2)]
        
        # Create temporary surface to show preview
        temp_surface = self.canvas.copy()
        pygame.draw.polygon(temp_surface, color, points, self.brush_size)
        return temp_surface
    
    def finalize_right_triangle(self):
        """Finalize right triangle drawing"""
        color = self.get_current_color()
        mouse_pos = pygame.mouse.get_pos()
        x1, y1 = self.start_x, self.start_y
        x2, y2 = mouse_pos[0], mouse_pos[1]
        
        points = [(x1, y1), (x2, y1), (x1, y2)]
        pygame.draw.polygon(self.canvas, color, points, self.brush_size)
    
    def draw_equilateral_triangle(self):
        """Draw equilateral triangle from start to current mouse position"""
        color = self.get_current_color()
        mouse_pos = pygame.mouse.get_pos()
        x1, y1 = self.start_x, self.start_y
        x2, y2 = mouse_pos[0], mouse_pos[1]
        
        # Calculate side length
        dx = x2 - x1
        dy = y2 - y1
        side = max(10, int((dx**2 + dy**2)**0.5))
        
        # Points for equilateral triangle
        height = side * math.sqrt(3) / 2
        points = [
            (x1, y1),
            (x1 + side, y1),
            (x1 + side/2, y1 - height)
        ]
        
        # Create temporary surface to show preview
        temp_surface = self.canvas.copy()
        pygame.draw.polygon(temp_surface, color, points, self.brush_size)
        return temp_surface
    
    def finalize_equilateral_triangle(self):
        """Finalize equilateral triangle drawing"""
        color = self.get_current_color()
        mouse_pos = pygame.mouse.get_pos()
        x1, y1 = self.start_x, self.start_y
        x2, y2 = mouse_pos[0], mouse_pos[1]
        
        dx = x2 - x1
        dy = y2 - y1
        side = max(10, int((dx**2 + dy**2)**0.5))
        
        height = side * math.sqrt(3) / 2
        points = [
            (x1, y1),
            (x1 + side, y1),
            (x1 + side/2, y1 - height)
        ]
        pygame.draw.polygon(self.canvas, color, points, self.brush_size)
    
    def draw_rhombus(self):
        """Draw rhombus from start to current mouse position"""
        color = self.get_current_color()
        mouse_pos = pygame.mouse.get_pos()
        x1, y1 = self.start_x, self.start_y
        x2, y2 = mouse_pos[0], mouse_pos[1]
        
        # Calculate width and height
        width = abs(x2 - x1)
        height = abs(y2 - y1)
        
        # Points for rhombus
        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2
        points = [
            (cx, y1),
            (x2, cy),
            (cx, y2),
            (x1, cy)
        ]
        
        # Create temporary surface to show preview
        temp_surface = self.canvas.copy()
        pygame.draw.polygon(temp_surface, color, points, self.brush_size)
        return temp_surface
    
    def finalize_rhombus(self):
        """Finalize rhombus drawing"""
        color = self.get_current_color()
        mouse_pos = pygame.mouse.get_pos()
        x1, y1 = self.start_x, self.start_y
        x2, y2 = mouse_pos[0], mouse_pos[1]
        
        width = abs(x2 - x1)
        height = abs(y2 - y1)
        
        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2
        points = [
            (cx, y1),
            (x2, cy),
            (cx, y2),
            (x1, cy)
        ]
        pygame.draw.polygon(self.canvas, color, points, self.brush_size)
    
    def update(self):
        """Update logic"""
        pass
    
    def render(self, screen):
        """Render everything"""
        # Draw canvas
        screen.blit(self.canvas, (0, 0))
        
        # Show preview for shapes while drawing
        if self.drawing:
            if self.current_tool == "rectangle":
                preview = self.draw_rectangle()
                screen.blit(preview, (0, 0))
            elif self.current_tool == "circle":
                preview = self.draw_circle()
                screen.blit(preview, (0, 0))
            elif self.current_tool == "right_triangle":
                preview = self.draw_right_triangle()
                screen.blit(preview, (0, 0))
            elif self.current_tool == "equilateral_triangle":
                preview = self.draw_equilateral_triangle()
                screen.blit(preview, (0, 0))
            elif self.current_tool == "rhombus":
                preview = self.draw_rhombus()
                screen.blit(preview, (0, 0))
        
        # Show line preview
        if self.line_drawing:
            mouse_pos = pygame.mouse.get_pos()
            temp_surface = self.canvas.copy()
            pygame.draw.line(temp_surface, self.get_current_color(), (self.start_x, self.start_y), mouse_pos, self.brush_size)
            screen.blit(temp_surface, (0, 0))
        
        # Show text input
        if self.text_mode:
            # Draw cursor
            cursor_x = self.text_pos[0] + text_font.size(self.text_input)[0]
            cursor_y = self.text_pos[1]
            pygame.draw.line(screen, BLACK, (cursor_x, cursor_y), (cursor_x, cursor_y + text_font.get_height()), 2)
            
            # Draw current text
            if self.text_input:
                text_surface = text_font.render(self.text_input, True, self.get_current_color())
                screen.blit(text_surface, self.text_pos)
        
        # Draw UI
        self.draw_ui(screen)
        pygame.display.flip()
    
    def draw_ui(self, screen):
        """Draw user interface"""
        # Tool indicator
        tool_text = font.render(f"Tool: {self.current_tool.upper()}", True, BLACK)
        screen.blit(tool_text, (10, 10))
        
        # Color indicator
        color_name = {0: "Black", 1: "Red", 2: "Green", 3: "Blue", 4: "Yellow", 5: "Cyan", 6: "Magenta"}
        color_text = font.render(f"Color: {color_name[self.color_index]}", True, BLACK)
        screen.blit(color_text, (10, 35))
        
        # Brush size
        size_text = font.render(f"Size: {self.brush_size}", True, BLACK)
        screen.blit(size_text, (10, 60))
        
        # Color palette
        palette_x = SCREEN_WIDTH - 200
        palette_y = 10
        palette_text = small_font.render("Colors (1-7):", True, BLACK)
        screen.blit(palette_text, (palette_x, palette_y))
        
        for i, color in enumerate(self.colors):
            rect = pygame.Rect(palette_x + i * 25, palette_y + 25, 20, 20)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, BLACK, rect, 2)
        
        # Instructions
        instructions = [
            "P: Pencil | L: Line | R: Rectangle | C: Circle | E: Eraser",
            "T: Right Triangle | Y: Equilateral Triangle | H: Rhombus",
            "F: Fill | X: Text | 1-7: Colors | F1-F3: Size",
            "Ctrl+S: Save | DEL: Clear"
        ]
        for i, instruction in enumerate(instructions):
            text = small_font.render(instruction, True, GRAY)
            screen.blit(text, (10, SCREEN_HEIGHT - 70 + i * 20))


def main():
    app = PaintApp()
    running = True
    
    while running:
        running = app.handle_events()
        app.update()
        app.render(screen)
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()