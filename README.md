# STM32_NUCLEO_oscilloscope
<h1>Digital oscilloscope for the STM32 NUCLEO board </h1>
A public digital oscilloscope downloadable on the NUCLEO board to display analogue signals, from 0V up to 3.3V, between 10Hz – 100kHz.
It can work out of the box with a STM32F401RE board by flashing on it the contenent of the STM_CUBE_BUILD directory as shown in the following.
Anyway it is shown how to use it on every board compatible with the STM32CubeIDE.

Input channels: 2
Input voltage range: 0V – 3,3V
Resolution: 256 levels
Sample frequency: 10Hz – 100kHz
Trigger types:  Auto / Normal / Single / Stop
Trigger levels [V]: 0V – 3,3V
Display resolution: 256 x 256 points

Voltage samples are taken from the card which via serial communication transmits the signal to the PC, via USB interface, to be displayed.

For the graphical realization of the interface the library tkinter was used.

# How to start on STM32F401RE

flashare firmware ed eseguire script

# How to start on a different board




I thank Stella Luigi and Mora Juan for their cooperation.
