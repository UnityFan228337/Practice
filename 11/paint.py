import pygame
import sys

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
pygame.display.set_caption("Paint Application")
clock = pygame.time.Clock()

# Fonts
font = pygame.font.SysFont("Arial", 18, bold=True)
small_font = pygame.font.SysFont("Arial", 14)

# Tool class
class Tool:
    def __init__(self, name, key, color=None):
        self.name = name
        self.key = key
        self.color = color
        self.is_active = False

# Paint application state
class PaintApp:
    def __init__(self):
        self.drawing = False
        self.current_color = BLACK
        self.brush_size = 5
        self.current_tool = "brush"  # brush, rectangle, circle, eraser, right_triangle, equilateral_triangle, rhombus
        self.start_x = 0
        self.start_y = 0
        self.prev_x = 0
        self.prev_y = 0
        self.canvas = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.canvas.fill(WHITE)
        self.colors = [BLACK, RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA]
        self.color_index = 0
    
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
                if event.key == pygame.K_b:
                    self.current_tool = "brush"
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
                
                # Size adjustment
                elif event.key == pygame.K_UP:
                    self.brush_size = min(50, self.brush_size + 1)
                elif event.key == pygame.K_DOWN:
                    self.brush_size = max(1, self.brush_size - 1)
                
                # Clear canvas
                elif event.key == pygame.K_DELETE:
                    self.canvas.fill(WHITE)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    self.drawing = True
                    self.start_x = event.pos[0]
                    self.start_y = event.pos[1]
                    self.prev_x = event.pos[0]
                    self.prev_y = event.pos[1]
            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if self.drawing:
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
                if self.drawing and self.current_tool in ["brush", "eraser"]:
                    self.draw_brush(event.pos)
        
        return True
    
    def draw_brush(self, pos):
        """Draw with brush tool"""
        color = self.get_current_color()
        # Draw line from previous position to current position
        self.draw_line(self.prev_x, self.prev_y, pos[0], pos[1], color)
        self.prev_x = pos[0]
        self.prev_y = pos[1]
    
    def draw_line(self, x1, y1, x2, y2, color):
        """Draw a line by interpolating circles"""
        import math
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
        pygame.draw.rect(temp_surface, color, (x, y, width, height), 2)
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
        
        pygame.draw.rect(self.canvas, color, (x, y, width, height), 2)
    
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
            pygame.draw.circle(temp_surface, color, (self.start_x, self.start_y), radius, 2)
        return temp_surface
    
    def finalize_circle(self):
        """Finalize circle drawing"""
        color = self.get_current_color()
        mouse_pos = pygame.mouse.get_pos()
        dx = mouse_pos[0] - self.start_x
        dy = mouse_pos[1] - self.start_y
        radius = max(1, int((dx ** 2 + dy ** 2) ** 0.5))
        if radius > 0:
            pygame.draw.circle(self.canvas, color, (self.start_x, self.start_y), radius, 2)
    
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
        pygame.draw.polygon(temp_surface, color, points, 2)
        return temp_surface
    
    def finalize_right_triangle(self):
        """Finalize right triangle drawing"""
        color = self.get_current_color()
        mouse_pos = pygame.mouse.get_pos()
        x1, y1 = self.start_x, self.start_y
        x2, y2 = mouse_pos[0], mouse_pos[1]
        
        points = [(x1, y1), (x2, y1), (x1, y2)]
        pygame.draw.polygon(self.canvas, color, points, 2)
    
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
        import math
        height = side * math.sqrt(3) / 2
        points = [
            (x1, y1),
            (x1 + side, y1),
            (x1 + side/2, y1 - height)
        ]
        
        # Create temporary surface to show preview
        temp_surface = self.canvas.copy()
        pygame.draw.polygon(temp_surface, color, points, 2)
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
        
        import math
        height = side * math.sqrt(3) / 2
        points = [
            (x1, y1),
            (x1 + side, y1),
            (x1 + side/2, y1 - height)
        ]
        pygame.draw.polygon(self.canvas, color, points, 2)
    
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
        pygame.draw.polygon(temp_surface, color, points, 2)
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
        pygame.draw.polygon(self.canvas, color, points, 2)
    
    def update(self):
        """Update logic"""
        if self.drawing:
            if self.current_tool in ["rectangle", "circle", "right_triangle", "equilateral_triangle", "rhombus"]:
                pass  # Will be drawn in render
    
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
            "B: Brush | R: Rectangle | C: Circle | E: Eraser",
            "T: Right Triangle | Y: Equilateral Triangle | H: Rhombus",
            "1-7: Colors | UP/DOWN: Size | DEL: Clear"
        ]
        for i, instruction in enumerate(instructions):
            text = small_font.render(instruction, True, GRAY)
            screen.blit(text, (10, SCREEN_HEIGHT - 50 + i * 20))


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
