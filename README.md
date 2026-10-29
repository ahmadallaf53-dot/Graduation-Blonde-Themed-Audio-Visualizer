# Graduation / Blonde Audio Visualizer

I chose for my first project at cresent the Audio Visualizer Card. You can pick between a UI inspired by the album Blonded by Frank Ocean or a UI inspired by the album Graduation from Kanye West.
You can chose between bars, which show how loud each pich range is at the moment and a wave, which shows the actual shape of the sound over a certain moment, so that the louder the music gets, the higher and lower it swings up and down. 
There is additonaly a figure (depending on which UI you picked) which moves up and down with the volume.

![Screenshot](screenshot.png)

**Demo video:** https://youtu.be/s5xd160k-S0

## Thats how you try it: 

1. Go to the my latest release or try this link (https://github.com/ahmadallaf53-dot/Graduation-Blonde-Themed-Audio-Visualizer/releases/latest).
2. Download `GraduationBlondeVisualizer-windows.zip` and unzip the whole folder.
3. Start the code and pick your audio source.
4. Pick a UI
5. Enjoy my excellent coding !

**Windows may show a SmartScreen warning because the app is not signed. Click More info → Run anyway**.

## What you see (explained in detail)

Everything you see on the screen comes from the sound, so it works with every song:

- **Bars:** There are 16 bars, and each bar is one frequency range. The louder a range is, the taller its bar gets.
- **Wave:** This is the real sound wave, drawn as a line (like on an oscilloscope).
- **Fiur:** The figure jumps higher when the music is louder.
  
## How it works

- The program reads the sound in small pieces (1024 samples). It gets them from the microphone with PyAudio or from a file with soundfile. For files, the program asks the pygame mixer where the song is right now, so the visuals match what you hear.
- NumPy does an FFT (`np.fft.rfft`) on each piece. This splits the sound into its frequencies.
- The frequencies are put into 16 groups. The groups get bigger for the high sounds, so the bass has more space.
- The bars and the wave do not jump directly to a new value. Each value moves slowly towards its target, so the movement looks smoother.
- The loudness (RMS) of each piece decides how high the character jumps.
- Pygame draws everything on the screen

## Music and image credits

-  The demo video uses The Britons by Kevibn MAcLeod
- This is a non-commercial fan project. *Graduation* and *Blonde* and their artwork belong to their respective owners. The images are used for demonstration only and can be replaced with your own images using the same file names.
- The Frank Ocean image was made by me, I hope you like it :).

## License

The code is released under the [MIT License](LICENSE). The license does not cover the third-party artwork mentioned above.
