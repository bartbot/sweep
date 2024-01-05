import wave

import machine


def play_wav(filename):
    with wave.open(filename, 'rb') as wav_file:
        wav_data = wav_file.readframes(wav_file.getnframes())
        pico = machine.PWM(machine.Pin(0))
        pico.duty_u16(wav_data)

def main():
    play_wav('audio.wav')

if __name__ == "__main__":
    main()
