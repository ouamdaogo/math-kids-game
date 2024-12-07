import winsound
import wave
import struct
import os

def create_sound_file(filename, frequency, duration, volume=1.0):
    # Parámetros de audio
    sample_rate = 44100
    num_samples = int(sample_rate * duration)
    
    # Crear directorio si no existe
    os.makedirs('assets/sounds', exist_ok=True)
    
    # Generar el archivo de sonido
    with wave.open(f'assets/sounds/{filename}', 'w') as wav_file:
        # Configurar parámetros
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 2 bytes por muestra
        wav_file.setframerate(sample_rate)
        
        # Generar las muestras de audio
        for i in range(num_samples):
            t = float(i) / sample_rate
            sample = int(volume * 32767.0 * struct.pack('h', int(32767.0 * 
                       math.sin(2 * math.pi * frequency * t))))
            wav_file.writeframes(struct.pack('h', sample))

# Crear sonidos
if __name__ == "__main__":
    # Sonido de click
    create_sound_file('click.wav', 1000, 0.1, 0.5)
    
    # Sonido de respuesta correcta
    create_sound_file('correct.wav', 800, 0.2, 0.7)
    
    # Sonido de respuesta incorrecta
    create_sound_file('incorrect.wav', 300, 0.3, 0.6)
    
    # Sonido de victoria
    create_sound_file('victory.wav', 600, 0.5, 0.8)
