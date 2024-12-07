import pygame
import sys
import random
import math
from sprites import Sprite, ParticleSystem
from sound_manager import SoundManager

# Inicializar Pygame
pygame.init()
pygame.mixer.init()

# Configuración de la pantalla
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Math Kids")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (70, 130, 240)  # Azul más brillante
GREEN = (76, 175, 80)  # Verde más vivo
RED = (255, 89, 89)    # Rojo más suave
YELLOW = (255, 193, 7)
PURPLE = (156, 39, 176)
ORANGE = (255, 152, 0)
PINK = (233, 30, 99)
LIGHT_BLUE = (3, 169, 244)
BACKGROUND_COLOR = (179, 229, 252)  # Azul claro para el fondo

# Gradientes para botones
def create_gradient_surface(width, height, color1, color2):
    surface = pygame.Surface((width, height))
    for y in range(height):
        color = [
            int(c1 + (c2 - c1) * (y / height))
            for c1, c2 in zip(color1, color2)
        ]
        pygame.draw.line(surface, color, (0, y), (width, y))
    return surface

class Button:
    def __init__(self, x, y, width, height, text, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.font = pygame.font.Font(None, 36)
        self.gradient = create_gradient_surface(
            width, 
            height, 
            [min(c + 30, 255) for c in color], 
            color
        )
        
    def draw(self, surface):
        # Sombra
        shadow_rect = self.rect.copy()
        shadow_rect.x += 2
        shadow_rect.y += 2
        pygame.draw.rect(surface, (0, 0, 0, 128), shadow_rect, border_radius=15)
        
        # Botón con gradiente
        surface.blit(self.gradient, self.rect)
        pygame.draw.rect(surface, self.color, self.rect, border_radius=15)
        
        # Borde brillante
        pygame.draw.rect(surface, [min(c + 50, 255) for c in self.color], self.rect, 2, border_radius=15)
        
        # Texto con sombra
        text_shadow = self.font.render(self.text, True, (0, 0, 0))
        text = self.font.render(self.text, True, WHITE)
        
        # Centrar texto
        text_rect = text.get_rect(center=self.rect.center)
        text_shadow_rect = text_shadow.get_rect(center=(text_rect.centerx + 1, text_rect.centery + 1))
        
        surface.blit(text_shadow, text_shadow_rect)
        surface.blit(text, text_rect)

class Game:
    def __init__(self):
        self.state = "menu"
        self.difficulty = "facil"
        self.buttons = {
            "contar": Button(250, 100, 300, 80, "Contar", BLUE),
            "comparar": Button(250, 200, 300, 80, "Comparar", BLUE),
            "sumar": Button(250, 300, 300, 80, "Sumar", BLUE),
            "restar": Button(250, 400, 300, 80, "Restar", BLUE),
            "volver": Button(250, 500, 300, 80, "Volver al Menú", RED),
            "facil": Button(50, 500, 200, 60, "Fácil", GREEN),
            "medio": Button(300, 500, 200, 60, "Medio", YELLOW),
            "dificil": Button(550, 500, 200, 60, "Difícil", RED),
            "sonido": Button(10, 550, 140, 40, "Sonido: ON", GREEN),
            "musica": Button(160, 550, 140, 40, "Música: ON", GREEN)
        }
        self.current_problem = None
        self.score = 0
        self.high_score = 0
        self.sprites = []
        self.particle_system = ParticleSystem()
        self.sound_manager = SoundManager()
        self.generate_problem()
        self.celebration_active = False
        self.celebration_timer = 0

    def generate_sprites(self, count):
        self.sprites = []
        for _ in range(count):
            x = random.randint(100, SCREEN_WIDTH - 100)
            y = random.randint(100, SCREEN_HEIGHT - 200)
            self.sprites.append(Sprite(x, y, 20))

    def generate_problem(self):
        if self.state == "menu":
            return
            
        max_number = 20
        
        if self.state == "contar":
            num = random.randint(1, max_number)
            self.generate_sprites(num)
            self.current_problem = {
                "type": "contar",
                "number": num,
                "question": f"¿Cuántos objetos hay?",
                "answer": num,
                "options": [num, num-1, num+1, num+2]
            }
        elif self.state == "comparar":
            num1 = random.randint(1, max_number)
            num2 = random.randint(1, max_number)
            while num1 == num2:  # Asegurar que los números sean diferentes
                num2 = random.randint(1, max_number)
            self.current_problem = {
                "type": "comparar",
                "numbers": (num1, num2),
                "question": "¿Qué número es mayor?",
                "answer": max(num1, num2),
                "options": [num1, num2]
            }
        elif self.state == "sumar":
            num1 = random.randint(1, max_number//2)
            num2 = random.randint(1, max_number//2)
            result = num1 + num2
            while result > max_number:  # Asegurar que la suma no exceda el máximo
                num1 = random.randint(1, max_number//2)
                num2 = random.randint(1, max_number//2)
                result = num1 + num2
            self.current_problem = {
                "type": "sumar",
                "numbers": (num1, num2),
                "question": f"{num1} + {num2} = ?",
                "answer": result,
                "options": [result, result-1, result+1, result+2]
            }
        elif self.state == "restar":
            num1 = random.randint(max_number//2, max_number)
            num2 = random.randint(1, num1)
            self.current_problem = {
                "type": "restar",
                "numbers": (num1, num2),
                "question": f"{num1} - {num2} = ?",
                "answer": num1 - num2,
                "options": [num1 - num2, num1 - num2 - 1, num1 - num2 + 1, num1 - num2 + 2]
            }

    def start_celebration(self):
        self.celebration_active = True
        self.celebration_timer = 60  # 1 segundo a 60 FPS
        for sprite in self.sprites:
            sprite.start_celebration()
        # Crear partículas en posiciones aleatorias
        for _ in range(20):  # Aumentado el número de partículas
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            color = random.choice([BLUE, GREEN, RED, YELLOW, PURPLE, ORANGE])
            self.particle_system.create_particles(x, y, color)
        self.sound_manager.play_sound('celebration')

    def draw(self):
        # Fondo con degradado
        screen.fill(BACKGROUND_COLOR)
        
        if self.state == "menu":
            # Título con estilo infantil
            title_shadow = pygame.font.Font(None, 48).render("Math Kids", True, (0, 0, 0))
            title = pygame.font.Font(None, 48).render("Math Kids", True, PURPLE)
            
            for offset in range(3, 0, -1):
                shadow_rect = title_shadow.get_rect(center=(SCREEN_WIDTH//2 + offset, 50 + offset))
                screen.blit(title_shadow, shadow_rect)
            
            title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 50))
            screen.blit(title, title_rect)
            
            # Botones de operaciones con colores diferentes
            available_operations = ["contar", "comparar", "sumar", "restar"]
            operation_colors = [BLUE, GREEN, ORANGE, PINK]
            button_spacing = 80
            start_y = 120
            
            for i, op in enumerate(available_operations):
                self.buttons[op] = Button(
                    SCREEN_WIDTH//2 - 100,
                    start_y + (i * button_spacing),
                    200,
                    60,
                    op.capitalize(),
                    operation_colors[i % len(operation_colors)]
                )
                self.buttons[op].draw(screen)
            
            # Botones de dificultad con colores suaves
            diff_buttons = ["Fácil", "Medio", "Difícil"]
            diff_colors = [LIGHT_BLUE, ORANGE, RED]
            diff_width = 120
            diff_spacing = 140
            diff_y = SCREEN_HEIGHT - 160
            
            for i, (button, color) in enumerate(zip(diff_buttons, diff_colors)):
                x_pos = (SCREEN_WIDTH // 2) - (diff_spacing * (len(diff_buttons) - 1) // 2) + (i * diff_spacing)
                self.buttons[button.lower()] = Button(
                    x_pos - diff_width//2,
                    diff_y,
                    diff_width,
                    40,
                    button,
                    color
                )
                self.buttons[button.lower()].draw(screen)
            
            # Botones de sonido y música con iconos
            sound_y = SCREEN_HEIGHT - 80
            self.buttons["sonido"] = Button(
                SCREEN_WIDTH//4 - 75,
                sound_y,
                150,
                40,
                f"🔊 {'ON' if self.sound_manager.sound_enabled else 'OFF'}",
                GREEN if self.sound_manager.sound_enabled else RED
            )
            self.buttons["sonido"].draw(screen)
            
            self.buttons["musica"] = Button(
                3*SCREEN_WIDTH//4 - 75,
                sound_y,
                150,
                40,
                f"🎵 {'ON' if self.sound_manager.music_enabled else 'OFF'}",
                GREEN if self.sound_manager.music_enabled else RED
            )
            self.buttons["musica"].draw(screen)
            
            # Récord con estilo
            high_score_text = pygame.font.Font(None, 24).render("Récord:", True, PURPLE)
            high_score_value = pygame.font.Font(None, 36).render(str(self.high_score), True, ORANGE)
            high_score_rect = high_score_text.get_rect(topright=(SCREEN_WIDTH - 80, 20))
            value_rect = high_score_value.get_rect(topright=(SCREEN_WIDTH - 20, 15))
            screen.blit(high_score_text, high_score_rect)
            screen.blit(high_score_value, value_rect)
            
        else:
            # Panel de juego con borde
            game_panel = pygame.Rect(50, 100, SCREEN_WIDTH - 100, SCREEN_HEIGHT - 200)
            pygame.draw.rect(screen, WHITE, game_panel, border_radius=20)
            pygame.draw.rect(screen, BLUE, game_panel, 3, border_radius=20)
            
            # Puntuación actual con estilo
            score_text = pygame.font.Font(None, 24).render("Puntuación:", True, PURPLE)
            score_value = pygame.font.Font(None, 36).render(str(self.score), True, ORANGE)
            screen.blit(score_text, (20, 20))
            screen.blit(score_value, (140, 15))

            if self.current_problem:
                # Pregunta con estilo
                question = self.current_problem["question"]
                shadow_color = (0, 0, 0)
                
                for offset in range(2, 0, -1):
                    question_shadow = pygame.font.Font(None, 48).render(question, True, shadow_color)
                    shadow_rect = question_shadow.get_rect(center=(SCREEN_WIDTH//2 + offset, 150 + offset))
                    screen.blit(question_shadow, shadow_rect)
                
                question_text = pygame.font.Font(None, 48).render(question, True, BLUE)
                question_rect = question_text.get_rect(center=(SCREEN_WIDTH//2, 150))
                screen.blit(question_text, question_rect)
                
                # Opciones como botones coloridos
                if "options" in self.current_problem:
                    option_colors = [BLUE, GREEN, ORANGE, PINK]
                    option_width = 80
                    option_height = 80
                    spacing = 40
                    total_width = len(self.current_problem["options"]) * (option_width + spacing) - spacing
                    start_x = (SCREEN_WIDTH - total_width) // 2
                    
                    for i, option in enumerate(self.current_problem["options"]):
                        x_pos = start_x + i * (option_width + spacing)
                        option_button = Button(
                            x_pos,
                            350,
                            option_width,
                            option_height,
                            str(option),
                            option_colors[i % len(option_colors)]
                        )
                        option_button.draw(screen)
            
            # Botón de volver con estilo
            self.buttons["volver"] = Button(
                SCREEN_WIDTH//2 - 100,
                SCREEN_HEIGHT - 60,
                200,
                40,
                "↩ Volver al Menú",
                RED
            )
            self.buttons["volver"].draw(screen)
            
            # Dibujar sprites y efectos
            if self.state == "contar" and self.sprites:
                for sprite in self.sprites:
                    sprite.update()
                    sprite.draw(screen)

            if self.celebration_active:
                self.particle_system.update()
                self.particle_system.draw(screen)
                self.celebration_timer -= 1
                if self.celebration_timer <= 0:
                    self.celebration_active = False

        pygame.display.flip()

    def handle_answer(self, answer):
        try:
            if answer == self.current_problem["answer"]:
                self.score += 1
                if self.score > self.high_score:
                    self.high_score = self.score
                self.sound_manager.play_sound('correct')
                self.start_celebration()
            else:
                self.score = max(0, self.score - 1)
                self.sound_manager.play_sound('incorrect')
            
            # Forzar la creación de un nuevo problema
            self.current_problem = None
            pygame.time.delay(300)
            self.generate_problem()
            
        except Exception as e:
            print(f"Error en handle_answer: {e}")

    def run(self):
        clock = pygame.time.Clock()
        running = True
        
        # Asegurar que la pantalla esté limpia al inicio
        screen.fill(WHITE)
        pygame.display.flip()
        
        while running:
            try:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        continue
                    
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        
                        # Manejar botones de sonido y música
                        if self.buttons["sonido"].rect.collidepoint(mouse_pos):
                            self.sound_manager.toggle_sound()
                            self.sound_manager.play_sound('click')
                            continue
                            
                        if self.buttons["musica"].rect.collidepoint(mouse_pos):
                            self.sound_manager.toggle_music()
                            self.sound_manager.play_sound('click')
                            continue
                        
                        if self.state == "menu":
                            # Manejar clicks en botones de dificultad
                            difficulty_changed = False
                            for diff in ["facil", "medio", "dificil"]:
                                if self.buttons[diff].rect.collidepoint(mouse_pos):
                                    self.sound_manager.play_sound('click')
                                    self.difficulty = diff
                                    difficulty_changed = True
                                    break
                            
                            # Solo procesar operaciones si no cambió la dificultad
                            if not difficulty_changed:
                                # Manejar clicks en botones de operaciones
                                available_operations = ["contar", "comparar", "sumar", "restar"]
                                for op in available_operations:
                                    if self.buttons[op].rect.collidepoint(mouse_pos):
                                        self.sound_manager.play_sound('click')
                                        self.state = op
                                        self.score = 0
                                        self.current_problem = None
                                        self.generate_problem()
                                        break
                        else:
                            # Volver al menú
                            if self.buttons["volver"].rect.collidepoint(mouse_pos):
                                self.sound_manager.play_sound('click')
                                self.state = "menu"
                                self.score = 0
                                self.current_problem = None
                                continue
                            
                            # Manejar respuestas
                            if self.current_problem and "options" in self.current_problem:
                                option_width = 80  # Botones más pequeños
                                option_height = 80
                                spacing = 40  # Menos espacio entre botones
                                total_width = len(self.current_problem["options"]) * (option_width + spacing) - spacing
                                start_x = (SCREEN_WIDTH - total_width) // 2
                                
                                for i, option in enumerate(self.current_problem["options"]):
                                    x_pos = start_x + i * (option_width + spacing)
                                    option_rect = pygame.Rect(x_pos, 350, option_width, option_height)
                                    if option_rect.collidepoint(mouse_pos):
                                        self.handle_answer(option)
                                        break
                
                # Dibujar la pantalla
                self.draw()
                
                # Mantener el framerate
                clock.tick(60)
            except Exception as e:
                print(f"Error en el bucle principal: {e}")
                continue

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
