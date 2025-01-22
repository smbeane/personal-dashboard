# Personal LED Dashboard
View the date and time, weather, and music playback on Spotify using a Raspberry Pi and 64 x 32 LED Matrix.

[Live Demo](https://youtube.com)

## Hardware:
### Main Controller:
The dashboard is controlled by a Raspberry Pi 4 Model B with an attached Adafruit RGB Matrix Bonnet. 

### Display: 
The display is a Waveshare 32 x 64 RGB LED Matrix, however any similar 32 x 64 matrix can be used. The power cable is a 5V 4A power supply.

## Software:
### Matrix Control:
The language I chose was Python and utilizes various libraries. For control of the LED Matrix, I have used the `hzeller/rpi-rgb-led-matrix`. This library allows for full control of the matrix and has built in functions for settings images and text, as well as control of individual pixels. Additionally there is  `RPi.GPIO`for getting inputs from the buttons and `PIL` and `requests` for getting the information needed to be displayed on the board.

### Weather Information:
The Weather API being used is from `open-meteo`, utilizing the maximum and minimum daily temperatures, weather codes, and wind speeds with a given location. 

### Spotify Playback:
For music playback, the `Spotify Web API`, utilizing the current playback and control features. To use the Spotify API, each user needs to obtain their refresh token, which I did by making a basic website to sign into my account and getting the token from the return URL.
 

## Accessories:
The buttons are basic push buttons with a few resistors, soldered to some perfboard. Jumper wires were then used to connect the bonnet to the buttons.

I utilized Fusion 360 to model and then 3D print the case and button covers. The files for this can be found in [extras/models](/extras/models/)


## Improvements to Be Made
- Page UI Updates
  - Organize the weather page differently (shown [here](extras/templates/))
  - Allow for different home screens

- Code Optimizations
  - Spotify: Update cover image only when a new song is played
  - Handle internet connectivity differently 
  - Increased error handling

- Switch to a lower-cost controller (ESP32, Raspberry Pi Zero, etc)
- Include a dedicated power button instead of having to plug and unplug the power
- Case Redesign
  - Allow for display tilting
  - Include a ring around the button inserts so you can't see inside 
  - Mount display from behind so none of it is covered