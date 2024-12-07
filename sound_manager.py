import pygame
import os
import math
import wave
import struct
import random

class SoundManager:
    def __init__(self):
        self.sounds = {}
        self.music_playing = False
        self.sound_enabled = True
        self.music_enabled = True
        
        # Asegurarse de que existen los directorios necesarios
        if not os.path.exists('assets/sounds'):
            os.makedirs('assets/sounds')
        if not os.path.exists('assets/music'):
            os.makedirs('assets/music')
            
        # Crear sonidos básicos si no existen
        self._create_basic_sounds()
        
        # Cargar sonidos
        self.load_sounds()
        
        # Iniciar música de ambiente
        self.start_background_music()

    def _create_basic_sounds(self):
        """Crea sonidos básicos usando pygame.mixer.Sound"""
        if not os.path.exists('assets/sounds/correct.wav'):
            self._create_correct_sound()
        if not os.path.exists('assets/sounds/incorrect.wav'):
            self._create_incorrect_sound()
        if not os.path.exists('assets/sounds/click.wav'):
            self._create_click_sound()
        if not os.path.exists('assets/sounds/celebration.wav'):
            self._create_celebration_sound()
        if not os.path.exists('assets/music/background.wav'):
            self._create_background_music()

    def _create_correct_sound(self):
        """Crea un sonido de respuesta correcta"""
        sample_rate = 44100
        duration = 0.2  # segundos
        frequency = 880  # Hz (A5)
        
        # Generar un tono simple
        samples = []
        num_samples = int(duration * sample_rate)
        for i in range(num_samples):
            t = i / sample_rate
            sample = int(32767.0 * math.sin(2.0 * math.pi * frequency * t))
            samples.append(sample)
        
        # Crear archivo WAV
        with wave.open('assets/sounds/correct.wav', 'wb') as wav_file:
            # Configurar parámetros del archivo WAV
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 2 bytes por muestra
            wav_file.setframerate(sample_rate)
            
            # Convertir samples a bytes y escribir
            for sample in samples:
                # Asegurar que el sample esté en el rango correcto
                sample = max(-32767, min(32767, sample))
                wav_file.writeframes(struct.pack('h', sample))

    def _create_incorrect_sound(self):
        """Crea un sonido de respuesta incorrecta"""
        sample_rate = 44100
        duration = 0.3  # segundos
        frequency = 440  # Hz (A4)
        
        samples = []
        num_samples = int(duration * sample_rate)
        for i in range(num_samples):
            t = i / sample_rate
            sample = int(16383.0 * math.sin(2.0 * math.pi * frequency * t))
            samples.append(sample)
        
        # Crear archivo WAV
        with wave.open('assets/sounds/incorrect.wav', 'wb') as wav_file:
            # Configurar parámetros del archivo WAV
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 2 bytes por muestra
            wav_file.setframerate(sample_rate)
            
            # Convertir samples a bytes y escribir
            for sample in samples:
                # Asegurar que el sample esté en el rango correcto
                sample = max(-32767, min(32767, sample))
                wav_file.writeframes(struct.pack('h', sample))

    def _create_click_sound(self):
        """Crea un sonido de click"""
        sample_rate = 44100
        duration = 0.1  # segundos
        frequency = 1000  # Hz
        
        samples = []
        num_samples = int(duration * sample_rate)
        for i in range(num_samples):
            t = i / sample_rate
            sample = int(8191.0 * math.sin(2.0 * math.pi * frequency * t))
            samples.append(sample)
        
        # Crear archivo WAV
        with wave.open('assets/sounds/click.wav', 'wb') as wav_file:
            # Configurar parámetros del archivo WAV
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 2 bytes por muestra
            wav_file.setframerate(sample_rate)
            
            # Convertir samples a bytes y escribir
            for sample in samples:
                # Asegurar que el sample esté en el rango correcto
                sample = max(-32767, min(32767, sample))
                wav_file.writeframes(struct.pack('h', sample))

    def _create_celebration_sound(self):
        """Crea un sonido de celebración"""
        sample_rate = 44100
        duration = 0.5  # segundos
        
        samples = []
        num_samples = int(duration * sample_rate)
        for i in range(num_samples):
            t = i / sample_rate
            # Mezclar diferentes frecuencias para un sonido más rico
            sample = int(10922.0 * (
                math.sin(2.0 * math.pi * 440 * t) +  # A4
                0.5 * math.sin(2.0 * math.pi * 880 * t) +  # A5
                0.25 * math.sin(2.0 * math.pi * 1760 * t)  # A6
            ))
            samples.append(sample)
        
        # Crear archivo WAV
        with wave.open('assets/sounds/celebration.wav', 'wb') as wav_file:
            # Configurar parámetros del archivo WAV
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 2 bytes por muestra
            wav_file.setframerate(sample_rate)
            
            # Convertir samples a bytes y escribir
            for sample in samples:
                # Asegurar que el sample esté en el rango correcto
                sample = max(-32767, min(32767, sample))
                wav_file.writeframes(struct.pack('h', sample))

    def _create_background_music(self):
        """Crea música de fondo con sonidos de niños y naturaleza"""
        if not os.path.exists('assets/music'):
            os.makedirs('assets/music')

        duration = 15.0  # 15 segundos de música
        sample_rate = 44100
        num_samples = int(duration * sample_rate)
        
        # Generar muestras base
        samples = []
        
        # Frecuencias base para sonidos de naturaleza
        nature_sounds = [
            (220.0, 0.05),   # Viento suave (más bajo)
            (440.0, 0.08),   # Pájaros (volumen medio)
            (880.0, 0.06),   # Pájaros agudos (más suave)
            (1760.0, 0.03)   # Sonidos agudos de ambiente (muy suave)
        ]
        
        # Generar el sonido base
        for i in range(num_samples):
            t = i / sample_rate
            sample = 0
            
            # Sonidos de naturaleza con modulación más suave
            for freq, base_amp in nature_sounds:
                # Modulación de amplitud más suave
                amp = base_amp * (1.0 + 0.3 * math.sin(2.0 * math.pi * 0.2 * t))
                # Añadir variación de frecuencia suave
                freq_mod = freq * (1.0 + 0.01 * math.sin(2.0 * math.pi * 0.1 * t))
                sample += amp * math.sin(2.0 * math.pi * freq_mod * t)
            
            # Añadir risas de niños más suaves y naturales
            if random.random() < 0.0005:  # Menos frecuente
                laugh_duration = int(0.3 * sample_rate)  # Risas más largas
                if i + laugh_duration < num_samples:
                    # Frecuencias más variadas para diferentes tipos de risas
                    laugh_freq = random.uniform(600, 1400)
                    # Modulación de frecuencia para risas más naturales
                    mod_freq = random.uniform(4, 8)
                    for j in range(laugh_duration):
                        t_laugh = (i + j) / sample_rate
                        # Envolvente más suave para el inicio y final de la risa
                        env = math.sin(math.pi * j / laugh_duration)
                        # Modulación de frecuencia para hacer la risa más natural
                        freq_mod = laugh_freq * (1.0 + 0.1 * math.sin(2.0 * math.pi * mod_freq * t_laugh))
                        amp = 0.15 * env  # Amplitud reducida
                        samples.append(int(32767.0 * (
                            sample + 
                            amp * math.sin(2.0 * math.pi * freq_mod * t_laugh)
                        )))
                    i += laugh_duration
                    continue
            
            samples.append(int(32767.0 * sample))

        # Suavizar las transiciones para el loop
        fade_samples = int(0.1 * sample_rate)  # 0.1 segundos de fade
        for i in range(fade_samples):
            # Fade in al inicio
            samples[i] = int(samples[i] * (i / fade_samples))
            # Fade out al final
            samples[-i-1] = int(samples[-i-1] * (i / fade_samples))

        # Crear archivo WAV
        with wave.open('assets/music/background.wav', 'wb') as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 2 bytes por muestra
            wav_file.setframerate(sample_rate)
            
            # Convertir samples a bytes y escribir
            for sample in samples:
                # Asegurar que el sample esté en el rango correcto
                sample = max(-32767, min(32767, sample))
                wav_file.writeframes(struct.pack('h', sample))

    def load_sounds(self):
        """Carga todos los sonidos del directorio assets/sounds"""
        for filename in os.listdir('assets/sounds'):
            if filename.endswith('.wav'):
                sound_name = os.path.splitext(filename)[0]
                self.sounds[sound_name] = pygame.mixer.Sound(os.path.join('assets/sounds', filename))

    def start_background_music(self):
        """Inicia la música de fondo"""
        if self.music_enabled:
            try:
                pygame.mixer.music.load('assets/music/background.wav')
                pygame.mixer.music.set_volume(0.2)  # Volumen reducido al 20%
                pygame.mixer.music.play(-1)  # -1 significa reproducir en bucle
                self.music_playing = True
            except:
                print("No se pudo cargar la música de fondo")

    def stop_background_music(self):
        """Detiene la música de fondo"""
        if self.music_playing:
            pygame.mixer.music.stop()
            self.music_playing = False

    def toggle_music(self):
        """Activa/desactiva la música"""
        self.music_enabled = not self.music_enabled
        if self.music_enabled:
            self.start_background_music()
        else:
            self.stop_background_music()

    def toggle_sound(self):
        """Activa/desactiva los efectos de sonido"""
        self.sound_enabled = not self.sound_enabled
        return self.sound_enabled

    def play_sound(self, sound_name):
        """Reproduce un efecto de sonido"""
        if self.sound_enabled and sound_name in self.sounds:
            self.sounds[sound_name].play()
