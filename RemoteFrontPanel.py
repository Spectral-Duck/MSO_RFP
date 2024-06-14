"""
    This code is provided "AS IS" with no support or warranty. 
    Daniel Schneider - Tektronix - 5/10/2024
    V1.4
"""

# Written in Python V3.10.1
import PySimpleGUI as sg  #https://www.pysimplegui.com/ V4.60.4 - Easy GUI builder for python
import pyvisa # https://pyvisa.readthedocs.io/en/latest/ V1.13.0 - PyVISA allows for communication with a scope
from GUI import * # GUI definitions, in its own file to reduce clutter
import RFP_Tk # Remote Front Panel Toolkit, in its own file to reduce clutter
import os # general OS utils default python lib
import time # time control default python lib

window = sg.Window("MSO RFP",layout,finalize=True,keep_on_top=sg.user_settings_get_entry('-SETTING-TOP-',default=False))

global scope 
scope = None
flag = False
RT_Button_Counter = 0

rm = pyvisa.ResourceManager('@py')

def connect():
    global scope
    scope = rm.open_resource(f'TCPIP::{sg.user_settings_get_entry("-SETTING-IP-")}::INSTR')
    scope.timeout = 30000
    scope_idn= scope.query("*IDN?")
    scope_name = scope_idn.split(',')
    if scope_name[1] in RFP_Tk.valid_instruments:
        window['-TEXT-SCOPE-NAME-'].update(value = f"{scope_name[1]}, {scope_name[2]}")
    else:
        scope.close()
        scope = None
        window['-TEXT-SCOPE-NAME-'].update('No Scope Connected')
        sg.popup_error(f'Nonsupported instrument.\nDisconnecting from {scope_name[1]}',keep_on_top=True)

if sg.user_settings_get_entry('-SETTING-AUTOCONNECT-') == True:
    try:
        connect()
    except:
        sg.popup_auto_close('Scope not found on startup.',auto_close_duration=3,keep_on_top=True)

while(True): #main event loop, program spends its time waiting for events here
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Exit': # if user closes window or clicks cance
        try:
            scope.close()
        except:
            pass
        break
    if 'SETTING' in event:
        # First much sanatize the input from user, IP sorts itself out when it errors.
        if '-SETTING-TOP-' in event: # In order to set keep_on_top you need two function calls, one to set and one to clear
            # I would much rather keep_on_top(values[event]) to work, but no... it doesn't 
            if values[event]:
                window.keep_on_top_set()
            else:
                window.keep_on_top_clear()

        sg.user_settings_set_entry(event,values[event])
        print(values[event])

    elif 'BUTTON' in event:
        if '-CONNECT' in event:
            if scope != None:
                sg.popup_error('Already connected to a Scope',keep_on_top=True)
            else:
                try:
                    connect()
                except:
                    sg.popup_error('Invalid scope address.\nPlase check the IP address.',keep_on_top=True)
        
        if 'DISCONNECT' in event:
            if scope == None:
                sg.popup_error('No scope connected.\nNothing to disconnect.',keep_on_top=True)
            else:
                scope.close()
                scope = None
                window['-TEXT-SCOPE-NAME-'].update('No Scope')
                
        elif 'SEND' in event:
            if scope == None:
                sg.popup_error('No scope connected.\nPlase connect a scope.',keep_on_top=True)
            else:
                message = event.split('_')
                scope.write(RFP_Tk.command[message[-1]][-1])
                window['-SCPI-HINT-'].update(RFP_Tk.command[message[-1]][0])
                #print(RFP_Tk.press[message[-1]][-1])
        elif 'MACRO' in event:
            # support for user macros, thinking 4 buttons should be enough?  Or should the number of macros be user definable?  
            pass

        elif 'SESSION-CLIPBOARD-' in event:
            """
            Saves Session to scope
            Checks if the file is too large to transfer, limit set in UI

            Transfers Session to PC
            Sets file to clipbaord
            """
            scope_file = values['-SETTING-SCOPE-FILE-'] + '/' + values['-SETTING-SESSION-NAME-']
            local_file = values['-SETTING-PC-FILE-'] + '/' + values['-SETTING-SESSION-NAME-']
            RFP_Tk.save_to_scope(scope,scope_file)
            size = RFP_Tk.get_file_size(scope,scope_file)
            if size > int(values['-SETTING-MAXFILESIZE-']):
                sg.popup_error('Session too large to transfer.\nUse alternate file transfer method.',keep_on_top=True)
            else:
                RFP_Tk.get_file(scope,scope_file,local_file)
                RFP_Tk.file_clipboard(local_file)
                sg.popup_notify('Finished, session on your clipboard')



        elif 'SCREENSHOT-CLIPBOARD' in event:
            # Save a screenshot from the scope, then copy it to clipboard.  
            scope_file = values['-SETTING-SCOPE-FILE-'] + '/' + values['-SETTING-SCREENCAP-NAME-']
            local_file = values['-SETTING-PC-FILE-'] + '/' + values['-SETTING-SCREENCAP-NAME-']
            RFP_Tk.save_to_scope(scope,scope_file)
            size = RFP_Tk.get_file_size(scope,scope_file)
            if size > int(values['-SETTING-MAXFILESIZE-']):
                sg.popup_error('Screenshot too large to transfer.\nUse alternate file transfer method.',keep_on_top=True)
            else:
                RFP_Tk.get_file(scope,scope_file,local_file)
                RFP_Tk.file_clipboard(local_file)
                sg.popup_notify('Finished, image on your clipboard')

        elif 'SAVE' in event:
            # Request to save to a given file.  
            file_name = os.path.basename(values['-SETTING-SAVE-LOCATION-'])
            scope_file = values['-SETTING-SCOPE-FILE-'] + '/' + file_name
            print(file_name)
            RFP_Tk.save_to_scope(scope,scope_file)
            size = RFP_Tk.get_file_size(scope,scope_file)
            if size > int(values['-SETTING-MAXFILESIZE-']):
                sg.popup_error('Screenshot too large to transfer.\nUse alternate file transfer method.',keep_on_top=True)
            else:
                RFP_Tk.get_file(scope,scope_file,values['-SETTING-SAVE-LOCATION-'])
                sg.popup_notify('Finshed, file saved to PC')


    elif 'KNOB' in event:
        RT_Button_Counter = RT_Button_Counter+1 # incriment counter, to slow down realtime buttons
        # Pysimplegui appears to still send events from a real time button if it gets intrupted with popup
        # Result, without the following logic it would create tens of thousands of error windows quickly...
        if scope == None and not flag:
            sg.popup_error('No scope connected.\nPlase connect a scope.',keep_on_top=True)
            flag = True
        elif scope == None and flag:
            pass
        else:  #There has got to be a better way to handle this series of checks, could use splits and possibly dictionary lookups for the correct message
            message = event.split('_')
            scope.write(RFP_Tk.command[message[-1]][-1])
            window['-SCPI-HINT-'].update(RFP_Tk.command[message[-1]][0])
            #print(RFP_Tk.command[message[-1]][-1])
            flag = False
            time.sleep(sg.user_settings_get_entry('-SETTING-SCROLL-SPEED-',default=250)/1000)