# MSO_RFP
Simple Remote Front Pannel for Tektronix MSO2/4/5/6 Series Oscilloscopes

Built using the following:  
Python         V3.10.1  
FreeSimpleGUI  V5.1.0  
pyvisa         V1.13.0
pyvisa_py      V0.7.0


Key Features:  
Full front panel emmulation for supported instruments for ease of use.   
One click screenshot and session file to clipboard, useful for quickly sending to coworkers or other users.    
Save Screenshot/Session/Setup to the host PC.    
Autoconnect to last connected scope on startup.  
Stay on top, great for when using Windows Remote Desktop or e*Scope in fullscreen.  
Displays relevant SCPI commands when pressing buttons.  

Limitations:  
Does not support MSO58LP, LPD64, or MDO3 Series  
Remote saving of waveforms not supported.  Use session files instead.  

How to use:  
1. Make sure you have python 3.10.1 working.
2. Use pip to install FreeSimpleGUI 5.1.0, pyvisa 1.13.0, and pyvisa_py 0.7.0  
   pip install FreeSimpleGUI==5.1.0  
   pip install pyvisa==1.13.0  
   pip install pyvisa_py==0.7.0  
4. Place RemoteFrontPanel.py, RFP_Tk.py, and GUI.py in the same directory.
5. Run RemoteFrontPanel.py with python 3.10.1  
    I recommend creating a batch script, and shortcut to run the script with ease.
    Included batch script is an example, must be modified for opperation.  

UI next to MSO68B's front panel.  
![RFP](https://github.com/Spectral-Duck/MSO_RFP/assets/169471087/6a350cfd-454c-45fb-8112-7f5b270af8c0)
