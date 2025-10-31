# LINE ENCODING VISUALIZER

It is a Python-based interactive tool to *visualize line encoding schemes* for both digital and analog signals.  
This project helps you *understand how binary data is represented and transmitted* through various encoding techniques — from NRZ to scrambling and modulation schemes.

---

##  Features

### Digital-to-Digital Encoding:
- *NRZ-L (Non-Return-to-Zero Level)*
- *NRZ-I (Non-Return-to-Zero Inverted)*
- *Manchester Encoding*
- *Differential Manchester Encoding*
- *AMI (Alternate Mark Inversion)*

### Scrambling Techniques:
- *HDB3 (High-Density Bipolar 3-Zeros)*
- *B8ZS (Bipolar 8-Zero Substitution)*

### Analog-to-Digital Conversion:
- *PCM (Pulse Code Modulation)*
- *Delta Modulation*

### Other Features:
- Interactive CLI for user input  
- Step-by-step signal visualization
- Clean plots using Matplotlib  

---

## Installation

Make sure you have *Python 3.x* installed.

Install dependencies:
bash
git clone https://github.com/Riyanshi-Aditya/Data-Com-Assignment.git
cd Data-Com-Assignment
pip install -r requirements.txt

Run the visualizer:
bash
python project.py

##  Usage Guide

After running the program, you’ll be prompted to choose between *Digital* and *Analog* input modes.

For the digital mode, enter digital, followed by a binary sequence such as 1011001, and then select one of the available line encoding schemes — 
1. *NRZ-L*
2. *NRZ-I*
3. *Manchester*
4. *Differential Manchester*
5. *AMI*

If you choose AMI, you can optionally enable scrambling using either *B8ZS* (Bipolar 8-Zero Substitution) or *HDB3* (High Density Bipolar 3-Zeros) to handle long sequences of zeros. 

---

In the analog mode, enter analog when prompted and select either *PCM (Pulse Code Modulation)* or *Delta Modulation (DM)*. 

For PCM, input sampled analog amplitudes (e.g., -2.5, -1.2, 0.5, 1.8, 3.0). The program will:
1. Quantize the input amplitudes to 8 levels  
2. Display 3-bit binary codes for each level  
3. Generate the final bitstream  
4. Ask you to choose a digital line encoding to visualize the resulting bitstream

For Delta Modulation, provide sampled (quantized) values (e.g., 0.5, 1.0, 0.8, 1.2, 1.5). The program will:
1. Generate a bitstream using Delta Modulation rules (1 = increase, 0 = decrease)
2. Let you choose any digital encoding scheme (NRZ-L, NRZ-I, etc.)
3. Plot the encoded waveform

---

Each encoding generates a *Matplotlib* plot showing time on the X-axis and amplitude on the Y-axis, labeled with the chosen encoding scheme. 

To exit, close the plot window or press Ctrl + C in the terminal.

---

##  Conclusion

This project serves as a simple yet powerful visualization tool for understanding various *Digital Line Encoding* and *Analog-to-Digital Conversion* techniques. It can be used for educational purposes, lab demonstrations, or as a base for more advanced communication system simulations. Feel free to explore, modify, and enhance it to include more encoding schemes or visualization features!

---

## Author

Developed by *Riyanshi* and *Neharika Bajaj*
