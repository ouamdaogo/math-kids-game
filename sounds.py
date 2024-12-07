import pygame
import os

class SoundManager:
    def __init__(self):
        self.sounds = {}
        self.music_playing = False
        self.sound_enabled = True
        
        # Crear directorio de sonidos si no existe
        if not os.path.exists('assets/sounds'):
            os.makedirs('assets/sounds')
        
        # Intentar cargar los sonidos
        try:
            self.load_sounds()
        except:
            print("No se pudieron cargar algunos sonidos")
    
    def load_sounds(self):
        sound_files = {
            'correct': 'assets/sounds/correct.wav',
            'incorrect': 'assets/sounds/incorrect.wav',
            'click': 'assets/sounds/click.wav',
            'victory': 'assets/sounds/victory.wav'
        }
        
        for name, path in sound_files.items():
            if os.path.exists(path):
                self.sounds[name] = pygame.mixer.Sound(path)
    
    def play_sound(self, sound_name):
        if self.sound_enabled and sound_name in self.sounds:
            self.sounds[sound_name].play()
    
    def toggle_sound(self):
        self.sound_enabled = not self.sound_enabled
        
    def play_background_music(self):
        if os.path.exists('assets/sounds/background.mp3'):
            pygame.mixer.music.load('assets/sounds/background.mp3')
            pygame.mixer.music.play(-1)  # -1 significa reproducir en bucle
            self.music_playing = True
    
    def stop_background_music(self):
        pygame.mixer.music.stop()
        self.music_playing = False
        
    def toggle_background_music(self):
        if self.music_playing:
            self.stop_background_music()
        else:
            self.play_background_music()
