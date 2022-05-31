# STM32_NUCLEO_oscilloscope
<h1>Digital oscilloscope for the STM32 NUCLEO board </h1>
A public digital oscilloscope downloadable on the NUCLEO board to display analogue signals up to two different channels, from 0V up to 3.3V, between 10Hz – 100kHz.
It can work out of the box with a STM32F401RE board by flashing on it the contenent of the STM_CUBE_BUILD directory as shown in the following.
Anyway it is shown how to use it on every board compatible with the STM32CubeIDE.

Input channels: 2
Input voltage range: 0V – 3,3V
Resolution: 256 levels
Sample frequency: 10Hz – 100kHz
Trigger types:  Auto / Normal / Single / Stop
Trigger levels [V]: 0V – 3,3V
Display resolution: 256 x 256 points

By default, the pins used for the acquisition of the signals are:
•CH1: PA0
•CH2: PC5

Voltage samples are taken from the card which via serial communication transmits the signal to the PC, via USB interface, to be displayed.

For the graphical realization of the UI the library tkinter was used.

# How to start on STM32F401RE

The main features of this device are:

•clock frequency up to 84 MHz
•512 Kbytes of Flash memory
•96 Kbytes of SRAM

To use this project out of the shelf it is needed to download the STM32CubeIDE SW.
Open the IDE and choose File -> Import Projects from File System then select the content of the directory STM_CUBE_BUILD (Oscilloscope_II) as source.
Click on finish then the project can be buid and run on the board.

![image](https://user-images.githubusercontent.com/70527145/171236459-c89cbb28-1d52-494b-83bd-f8f7f2141326.png)

# How to start on a different board

#utilizzare stesso setup ma selezionando al primo passaggio la propria scheda 

# Execute the software


