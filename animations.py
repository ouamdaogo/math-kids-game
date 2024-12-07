import pygame
import random
import math

class ParticleEffect:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.particles = []
        self.color = color
        self.create_particles()
        
    def create_particles(self):
        for _ in range(20):
            particle = {
                'x': self.x,
                'y': self.y,
                'velocity_x': random.uniform(-5, 5),
                'velocity_y': random.uniform(-15, -5),
                'lifetime': 60,  # frames
                'size': random.randint(4, 8)
            }
            self.particles.append(particle)
    
    def update(self):
        for particle in self.particles[:]:
            particle['x'] += particle['velocity_x']
            particle['y'] += particle['velocity_y']
            particle['velocity_y'] += 0.5  # gravedad
            particle['lifetime'] -= 1
            
            if particle['lifetime'] <= 0:
                self.particles.remove(particle)
    
    def draw(self, surface):
        for particle in self.particles:
            alpha = min(255, particle['lifetime'] * 4)
            color = (*self.color, alpha)
            surf = pygame.Surface((particle['size'], particle['size']), pygame.SRCALPHA)
            pygame.draw.circle(surf, color, (particle['size']//2, particle['size']//2), particle['size']//2)
            surface.blit(surf, (particle['x'], particle['y']))
    
    def is_complete(self):
        return len(self.particles) == 0

class GameObject:
    SHAPES = ['circle', 'square', 'triangle', 'star']
    COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)]
    
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.shape = random.choice(self.SHAPES)
        self.color = random.choice(self.COLORS)
        self.animation_offset = 0
        self.animation_speed = random.uniform(0.05, 0.1)
        self.rotation = 0
        self.selected = False
    
    def update(self):
        self.animation_offset = math.sin(pygame.time.get_ticks() * self.animation_speed) * 5
        self.rotation += 1 if self.selected else 0
    
    def draw(self, surface):
        pos = (int(self.x), int(self.y + self.animation_offset))
        
        if self.shape == 'circle':
            pygame.draw.circle(surface, self.color, pos, self.size)
        elif self.shape == 'square':
            rect = pygame.Rect(pos[0] - self.size, pos[1] - self.size, self.size * 2, self.size * 2)
            if self.rotation:
                surf = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
                pygame.draw.rect(surf, self.color, surf.get_rect())
                rotated = pygame.transform.rotate(surf, self.rotation)
                surface.blit(rotated, rotated.get_rect(center=pos))
            else:
                pygame.draw.rect(surface, self.color, rect)
        elif self.shape == 'triangle':
            points = [
                (pos[0], pos[1] - self.size),
                (pos[0] - self.size, pos[1] + self.size),
                (pos[0] + self.size, pos[1] + self.size)
            ]
            pygame.draw.polygon(surface, self.color, points)
        elif self.shape == 'star':
            points = []
            for i in range(10):
                angle = math.pi * 2 * i / 10 - math.pi / 2
                r = self.size if i % 2 == 0 else self.size / 2
                points.append((
                    pos[0] + r * math.cos(angle),
                    pos[1] + r * math.sin(angle)
                ))
            pygame.draw.polygon(surface, self.color, points)
        
        if self.selected:
            pygame.draw.circle(surface, (255, 255, 255), pos, self.size + 2, 2)

class Celebration:
    def __init__(self, screen_width, screen_height):
        self.effects = []
        self.screen_width = screen_width
        self.screen_height = screen_height
    
    def add_celebration(self):
        for _ in range(5):
            x = random.randint(0, self.screen_width)
            y = random.randint(0, self.screen_height // 2)
            color = random.choice(GameObject.COLORS)
            self.effects.append(ParticleEffect(x, y, color))
    
    def update(self):
        for effect in self.effects[:]:
            effect.update()
            if effect.is_complete():
                self.effects.remove(effect)
    
    def draw(self, surface):
        for effect in self.effects:
            effect.draw(surface)
    
    def is_active(self):
        return len(self.effects) > 0
