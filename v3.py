import pygame
import math
import pyaudio
import numpy as np
import tkinter as tk
import soundfile as sf
import os
from tkinter import filedialog




screen_width = 1000
screen_height = 1000

pygame.init()
pygame.display.set_caption("Album Audio")
screen = pygame.display.set_mode((screen_width, screen_height))


THEMES_DEF = [ 
            ("Graduation - Kanye", "bear.png", "background.jpg"),
            ("Blonde - Frank Ocean", "frankocean.png", "blonded.jpg"),
]

themes = []

for name, char_file, bg_file in THEMES_DEF:
    if os.path.exists(char_file) and os.path.exists(bg_file):
        char_img = pygame.image.load(char_file).convert_alpha()
        char_img = pygame.transform.scale(char_img, (200, 250))
        bg_img = pygame.image.load(bg_file).convert()
        bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height))
        themes.append((name, char_img, bg_img))
bear = themes[0][1]
background = themes[0][2]


font_big = pygame.font.SysFont(None, 90)
font_small = pygame.font.SysFont(None, 40)

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

p = pyaudio.PyAudio()
stream = None



NUM_BARS = 16

edges = [1, 2, 3, 4, 5, 6, 8,  10, 13, 17, 22, 30, 40, 60, 90, 140, 250 ]
bar_heights = [0] * NUM_BARS

wave_y = [0] * 256
source = "mic"
file_samples = None
file_rate = 44100




SCALE = 5000

def mic_aviable():
    global p

    p.terminate()
    p = pyaudio.PyAudio()
    try:
        p.get_default_input_device_info()
        return True     

    except IOError:
        return False



def start_stream():
    global stream
    try:
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)



        return True
    except Exception:
        return False



def draw_text(text, y, font, color):
    image = font.render(text, True, color)
    rect = image.get_rect(center=(screen_width // 2, y))
    screen.blit(image, rect)



def get_audio():
    data = stream.read(CHUNK, exception_on_overflow=False)

    samples = np.frombuffer(data, dtype=np.int16).astype(float)

    level = math.sqrt(np.mean(samples * samples))

    spectrum = np.abs(np.fft.rfft(samples))
    return level, spectrum, samples

def open_file():
    global file_samples, file_rate, source

    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)



    path = filedialog.askopenfilename(filetypes=[("Audio", "*.wav *.mp3 *.ogg *.flac")])
    root.destroy()

    if path == "":
        return

    try: 
        data, rate = sf.read(path, dtype="float32")

    except Exception:
        return



    if data.ndim == 2:
        data = data.mean(axis=1)


    file_samples = data * 32768
    file_rate = rate 

    pygame.mixer.music.load(path)
    
    source = "file"

    return True

def get_audio_file():
    ms = pygame.mixer.music.get_pos()
    if ms < 0:
        samples = np.zeros(CHUNK)
    else:
        pos = int(ms / 1000 * file_rate)
        samples = file_samples[pos:pos + CHUNK].astype(float)
        if len(samples) < CHUNK:
            samples = np.zeros(CHUNK)

    level = math.sqrt(np.mean(samples * samples))
    spectrum = np.abs(np.fft.rfft(samples))
    return level, spectrum, samples

def go_home():
    global stream, state, message

    pygame.mixer.music.stop()

    if stream is not None:
        try:
            stream.stop_stream()
            stream.close()
        except OSError:
            pass
        stream = None

    for i in range(NUM_BARS):
        bar_heights[i] = 0
    for n in range(256):
        wave_y[n] = 0

    message= ""
    state = "start"



def start_with_theme(index):
    global bear, background, state, message, bear_y, current_theme

    if source == "mic":
        if not start_stream():
            message = "Can not open the mike or mic :("
            state = "start"
            return

    else:
        pygame.mixer.music.play()



    bear = themes[index][1]
    background = themes[index][2]
    current_theme = index  
    bear_y = ground_y
    state = "play"


  

clock = pygame.time.Clock()
ground_y = screen_height -250
bear_y = ground_y

state = "start"
has_mic = mic_aviable() #  I just noticed that I spelled it wrong, but i am too lazy to change evrything
message=""
mode = "bars"

current_theme = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False



        elif event.type == pygame.KEYDOWN and state == "start":


            if event.key == pygame.K_m:
                has_mic = mic_aviable()
                message = ""


                if has_mic:
                    source = "mic"
                    state = "style"

                else:
                    message = "No mike or mic or mikey found :("


            if event.key == pygame.K_f:
                message = ""

                if open_file():
                    state = "style"

                else:
                    message = "You did not select a file or your file could not be open :( "

            #if event.key == pygame.K_r:
                #has_mic = mic_aviable ()
                #message = ""
            

        elif event.type == pygame.KEYDOWN and state == "style":

            if event.key == pygame.K_h:
                go_home()

            elif event.unicode.isdigit():
                choice = int(event.unicode) - 1
                if 0 <= choice < len(themes):
                    start_with_theme(choice)

                    

           
        elif event.type == pygame.KEYDOWN and state == "play":
            if event.key == pygame.K_w:
                if mode == "bars":
                    mode = "wave"

                else:
                    mode = "bars"


            if event.key == pygame.K_h:
                go_home()
                


    if state == "start":
        screen.fill((0,0,0))

        draw_text("Album Audio", 300, font_big, (255, 255, 255))
        draw_text("Choose your audio source :) ", 390, font_small, (255, 255, 255))


        draw_text("M  -  Mic or Mike", 500, font_small, (180, 240, 120))
        draw_text("F  -  Audio file", 560, font_small, (180, 240, 120))


        

        if message != "":
            draw_text(message, 700, font_small, (255, 150, 100))


        pygame.display.flip()
        

        
        continue

    if state == "style":
        screen.fill((0,0,0))

        draw_text("Choose your style :)", 300, font_big, (255,255,255))

        for i in range(len(themes)):
            draw_text(f"{i+1} -  {themes[i][0]}", 430 + i * 60, font_small, (180, 240, 120))

        draw_text("H  - Home", 430 + len(themes) * 60 + 40, font_small, (255, 150, 100))


        pygame.display.flip()
        continue



    
    if source == "mic":
        try:
            level, spectrum, samples = get_audio()

        except (OSError, AttributeError):
            message = "Mic or mike error. Press M to retry or F for a file."


            if stream is not None:
                try:
                    stream.stop_stream()
                    stream.close()
                except OSError:
                    pass
                stream = None
            state="start"
            continue

    else:
        level, spectrum, samples = get_audio_file()
     




    jump_height = min(level / 20 , 700)
    target_y = ground_y - jump_height
    bear_y += (target_y - bear_y) * 0.15


    screen.blit(background, (0, 0))




    if mode == "bars":
        bar_width = screen_width / NUM_BARS
        for i in range(NUM_BARS):
            value = np.mean(spectrum[edges[i]: edges[i +1]])
            target = min(value / SCALE,  400)





            bar_heights[i] += (target - bar_heights[i]) *0.3

            if current_theme ==1:
                color = (30 + i * 5, 255-i*8, 80)

            else:
                color= (255, 200 -i* 10, 50 +i* 10)


            x = int(i * bar_width) +4
            h = int(bar_heights[i]) 
     
            pygame.draw.rect(screen, color, (x, screen_height - h, int(bar_width) -8, h))
    else: 
        points = []
        for n in range(256):
            i = n * 4
            target = max(-400, min(400, samples[i] / 80))

            wave_y[n] = wave_y[n] + (target - wave_y[n]) * 0.3

            x = int(n / 256 * screen_width)
            y = int(screen_height // 2 + wave_y[n])
            points.append((x, y))


        if current_theme ==1:
            wave_color = (50, 220, 80)
        else:
            wave_color = (255, 255, 255)


        pygame.draw.lines(screen, wave_color, False, points, 4)



    screen.blit(bear, (150, int(bear_y)))

    if mode == "bars":
        hint = font_small.render("Press W to change to wave", True, (0, 0, 0))


    else:
        hint = font_small.render("Press W to change to bars", True, (0, 0, 0))
    
    screen.blit(hint, (20, screen_height -40)) 


    hint2 = font_small.render("Press H to go back to the start screen", True, (0, 0, 0))
            
    screen.blit(hint2, (20, screen_height - 80))

    pygame.display.flip()

    

    

    clock.tick(50)

if stream is not None:
    stream.stop_stream()
    stream.close()
p.terminate()
pygame.quit()

