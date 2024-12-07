import pygame
import random
import math

# Colores
COLORS = {
    'red': (220, 53, 69),
    'blue': (0, 123, 255),
    'green': (40, 167, 69),
    'yellow': (255, 193, 7),
    'purple': (111, 66, 193),
    'orange': (253, 126, 20)
}

class Sprite:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.original_y = y
        self.color = random.choice(list(COLORS.values()))
        self.animation_offset = 0
        self.animation_speed = random.uniform(0.05, 0.1)
        self.shape = random.choice(['circle', 'star', 'square', 'triangle'])
        self.rotation = 0
        self.scale = 1.0
        self.celebration = False
        self.celebration_time = 0

    def update(self):
        if self.celebration:
            self.celebration_time += 1
            self.rotation += 5
            self.scale = 1.0 + math.sin(self.celebration_time * 0.1) * 0.2
            if self.celebration_time > 60:  # 1 segundo a 60 FPS
                self.celebration = False
                self.celebration_time = 0
                self.scale = 1.0
                self.rotation = 0
        else:
            self.animation_offset = math.sin(pygame.time.get_ticks() * self.animation_speed) * 5
            self.y = self.original_y + self.animation_offset

    def start_celebration(self):
        self.celebration = True
        self.celebration_time = 0

    def draw(self, surface):
        if self.shape == 'circle':
            self.draw_circle(surface)
        elif self.shape == 'star':
            self.draw_star(surface)
        elif self.shape == 'square':
            self.draw_square(surface)
        elif self.shape == 'triangle':
            self.draw_triangle(surface)

    def draw_circle(self, surface):
        scaled_size = self.size * self.scale
        pygame.draw.circle(surface, self.color, (self.x, self.y), scaled_size)

    def draw_square(self, surface):
        scaled_size = self.size * self.scale
        rect = pygame.Rect(
            self.x - scaled_size,
            self.y - scaled_size,
            scaled_size * 2,
            scaled_size * 2
        )
        if self.rotation:
            surface_temp = pygame.Surface((scaled_size * 2, scaled_size * 2), pygame.SRCALPHA)
            pygame.draw.rect(surface_temp, self.color, (0, 0, scaled_size * 2, scaled_size * 2))
            rotated = pygame.transform.rotate(surface_temp, self.rotation)
            surface.blit(rotated, rotated.get_rect(center=(self.x, self.y)))
        else:
            pygame.draw.rect(surface, self.color, rect)

    def draw_triangle(self, surface):
        scaled_size = self.size * self.scale
        points = [
            (self.x, self.y - scaled_size),
            (self.x - scaled_size, self.y + scaled_size),
            (self.x + scaled_size, self.y + scaled_size)
        ]
        if self.rotation:
            # Rotar los puntos alrededor del centro
            center = (self.x, self.y)
            angle = math.radians(self.rotation)
            rotated_points = []
            for px, py in points:
                dx = px - center[0]
                dy = py - center[1]
                rx = dx * math.cos(angle) - dy * math.sin(angle)
                ry = dx * math.sin(angle) + dy * math.cos(angle)
                rotated_points.append((center[0] + rx, center[1] + ry))
            points = rotated_points
        pygame.draw.polygon(surface, self.color, points)

    def draw_star(self, surface):
        scaled_size = self.size * self.scale
        points = []
        for i in range(10):
            angle = math.pi * 2 * i / 10 - math.pi / 2
            radius = scaled_size if i % 2 == 0 else scaled_size * 0.5
            px = self.x + radius * math.cos(angle)
            py = self.y + radius * math.sin(angle)
            points.append((px, py))
        
        if self.rotation:
            # Rotar los puntos alrededor del centro
            center = (self.x, self.y)
            angle = math.radians(self.rotation)
            rotated_points = []
            for px, py in points:
                dx = px - center[0]
                dy = py - center[1]
                rx = dx * math.cos(angle) - dy * math.sin(angle)
                ry = dx * math.sin(angle) + dy * math.cos(angle)
                rotated_points.append((center[0] + rx, center[1] + ry))
            points = rotated_points
            
        pygame.draw.polygon(surface, self.color, points)

class ParticleSystem:
    def __init__(self):
        self.particles = []
        
    def create_particles(self, x, y, color, count=20):
        for _ in range(count):
            speed = random.uniform(2, 5)
            angle = random.uniform(0, math.pi * 2)
            self.particles.append({
                'x': x,
                'y': y,
                'dx': math.cos(angle) * speed,
                'dy': math.sin(angle) * speed,
                'life': 60,  # 1 segundo a 60 FPS
                'color': color,
                'size': random.randint(2, 4)
            })
            
    def update(self):
        for particle in self.particles[:]:
            particle['x'] += particle['dx']
            particle['y'] += particle['dy']
            particle['dy'] += 0.1  # Gravedad
            particle['life'] -= 1
            if particle['life'] <= 0:
                self.particles.remove(particle)
                
    def draw(self, surface):
        for particle in self.particles:
            alpha = min(255, particle['life'] * 4)
            color = list(particle['color'])
            if len(color) == 3:
                color.append(alpha)
            pygame.draw.circle(
                surface,
                color,
                (int(particle['x']), int(particle['y'])),
                particle['size']
            )
