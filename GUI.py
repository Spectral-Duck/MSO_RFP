"""
    The GUI definition, evething in this file exists to define how the gui is displayed to the user.  
    Im not going to impliment disabling buttons when connected to a scope that does not use them
        Ie, MSO22 only has CH1,CH2 buttons 3-8 wont do anything.
    The only issue I can forsee for this apprach is using invalid buttons will enable ESR bit 32
"""

import PySimpleGUI as sg

# defining the widths for each button
small = 7
medium = 17
large = 30

supported_files = [('Screenshot - Portable Network Graphic','.png'),('Screenshot - JPEG','.jpg'),('Tektronix - Scope Setup','.set'),('Tektronix - Scope Session File','*.tss')]

connect_layout          = [[sg.Text('IP:'),sg.Push(),sg.Input(f'{sg.user_settings_get_entry("-SETTING-IP-",default = "0.0.0.0")}',key = '-SETTING-IP-',size=14,change_submits=True)],
                           [sg.Button('Connect',key='-BUTTON-CONNECT-',size=medium)]
                          ]
disconnect_layout       = [[sg.Text('No Scope Connected',key='-TEXT-SCOPE-NAME-'),sg.Push()],
                           [sg.Button('Disconnect',key='-BUTTON-DISCONNECT-',size=medium)]
                          ]

CurFast_layout          = [[sg.Button('Run/Stop',key='-BUTTON-SEND_RUNSTop',size=medium)],
                           [sg.Button('Cursors', key = '-BUTTON-SEND_CURsor',size=small),sg.Push(),sg.Button('Fast Acq', key = '-BUTTON-SEND_FASTAcq',size=small)]
                          ]
HiresClear_layout       = [[sg.Button('Single/Seq',key = '-BUTTON-SEND_SINGleseq',size=medium)],
                           [sg.Button('High Res', key = '-BUTTON-SEND_HIGHRES',size=small),sg.Push(),sg.Button('Clear',key = '-BUTTON-SEND_CLEAR',size=small)]
                          ]

knobs_layout            = [[sg.Text('Multipurpose Knobs')],
                           [sg.RealtimeButton('A>',key = '-KNOB_aClkS-GPKNOB1',size=small,),sg.Push(),sg.RealtimeButton('A>>',key='-KNOB_aClkL-GPKNOB1',size=small)],
                           [sg.Button('A Press', key = '-BUTTON-SEND_GPKNOB1',size=medium)],
                           [sg.RealtimeButton('<A',key = '-KNOB_ClkS-GPKNOB1',size=small),sg.Push(),sg.RealtimeButton('<<A',key='-KNOB_ClkL-GPKNOB1',size=small)],
                           [sg.RealtimeButton('B>',key = '-KNOB_aClkS-GPKNOB2',size=small),sg.Push(),sg.RealtimeButton('B>>',key='-KNOB_aClkL-GPKNOB2',size=small)],
                           [sg.Button('B Press', key = '-BUTTON-SEND_GPKNOB2',size=medium)],
                           [sg.RealtimeButton('<B',key = '-KNOB_ClkS-GPKNOB2',size=small),sg.Push(),sg.RealtimeButton('<<B',key='-KNOB_ClkL-GPKNOB2',size=small)],
                          ]
       
trigger_layout          = [[sg.Text('Trigger')],
                           [sg.Button('Force',key='BUTTON-SEND_FORCetrig',size=medium)],
                           [sg.RealtimeButton('^Lev',key = '-KNOB_aClkS-TRIGLevel',size=small),sg.Push(),sg.RealtimeButton('^^Lev',key = '-KNOB_aClkL-TRIGLevel',size=small)],
                           [sg.Button('Level Press',key = '-BUTTON-SEND_SETTO50',size=medium)],
                           [sg.RealtimeButton('⌄Lev',key = '-KNOB_ClkS-TRIGLevel',size = small),sg.Push(),sg.RealtimeButton('⌄⌄Lev',key = '-KNOB_ClkL-TRIGLevel',size=small)],
                           [sg.Button('Slope',key = '-BUTTON-SEND_TRIGSlope',size=medium)],
                           [sg.Button('Mode',key = '-BUTTON-SEND_TRIGMode',size=medium)]
                          ]

vertical_layout_left    = [[sg.RealtimeButton('^Pos',key = '-KNOB_aClkS-VERTPOS',size=small),sg.Push(),sg.RealtimeButton('^^Pos',key = '-KNOB_aClkL-VERTPOS',size=small)],
                           [sg.Button('Position Press',key = '-BUTTON-SEND_VERTPOS',size=medium)],
                           [sg.RealtimeButton('⌄Pos',key = '-KNOB_ClkS-VERTPOS',size=small),sg.Push(),sg.RealtimeButton('⌄⌄Pos',key = '-KNOB_ClkL-VERTPOS',size=small)],
                           [sg.Button('^Scale',key = '-BUTTON-SEND_aClkS-VERTSCALE',size=small),sg.Push(),sg.RealtimeButton('^^Scale',key = '-KNOB_aClkS-VERTSCALE',size=small)],#,sg.Button('Scal>>',key = '-KNOB_aClkL-VERTSCALE')
                           [sg.Button('Scale Press',key = '-BUTTON-SEND_VERTSCALE',size=medium)],
                           [sg.Button('⌄Scale',key = '-BUTTON-SEND_ClkS-VERTSCALE',size=small),sg.Push(),sg.RealtimeButton('⌄⌄Scale',key = '-KNOB_ClkS-VERTSCALE',size=small)],#,sg.Button('<<Scal',key = '-KNOB_ClkL-VERTSCALE')
                          ]

vertical_layout_right   = [[sg.Button('1',key='-BUTTON-SEND_CH1',size=small),sg.Push(),sg.Button('2',key='-BUTTON-SEND_CH2',size=small)],
                           [sg.Button('3',key='-BUTTON-SEND_CH3',size=small),sg.Push(),sg.Button('4',key='-BUTTON-SEND_CH4',size=small)],
                           [sg.Button('5',key='-BUTTON-SEND_CH5',size=small),sg.Push(),sg.Button('6',key='-BUTTON-SEND_CH6',size=small)],
                           [sg.Button('7',key='-BUTTON-SEND_CH7',size=small),sg.Push(),sg.Button('8',key='-BUTTON-SEND_CH8',size=small)],
                           [sg.Push(),sg.Button('Ref',key='-BUTTON-SEND_REF',size=small)],
                           [sg.Button('Math',key='-BUTTON-SEND_MATh',size=small),sg.Push(),sg.Button('Bus',key='-BUTTON-SEND_BUS',size=small)],                           
                          ]

horizontal_layout_left  = [[sg.RealtimeButton('<Pos',key = '-KNOB_ClkS-HORZPOS',size=small),sg.Push(),sg.RealtimeButton('<<Pos',key = '-KNOB_ClkL-HORZPOS',size=small)],
                           [sg.Button('Position Press',key = '-BUTTON-SEND_HORZPOS',size=medium)],
                           [sg.RealtimeButton('Pos>',key = '-KNOB_aClkS-HORZPOS',size=small),sg.Push(),sg.RealtimeButton('Pos>>',key = '-KNOB_aClkL-HORZPOS',size=small)],
                           [sg.Button('<Scale',key = '-BUTTON-SEND_ClkS-HORZScale',size=small),sg.Push(),sg.RealtimeButton('<<Scale',key = '-KNOB_ClkS-HORZScale',size=small)],#,sg.Button('<<Scal',key = '-KNOB_ClkL-HORZScale')
                           [sg.Button('Scale Press',key = '-BUTTON-SEND_HORZScale',size=medium)],
                           [sg.Button('Scale>',key = '-BUTTON-SEND_aClkS-HORZScale',size=small),sg.Push(),sg.RealtimeButton('Scale>>',key = '-KNOB_aClkS-HORZScale',size=small)],#,sg.Button('Scal>>',key = '-KNOB_aClkL-HORZScale')
                          ]

horizontal_layout_right = [[sg.Button('Zoom',key='-BUTTON-SEND_ZOOM',size=medium)],
                           [sg.Button('Zoom In',key = '-KNOB_aClkS-ZOOM',size=medium)],
                           [sg.Button('Zoom Out',key = '-KNOB_ClkS-ZOOM',size=medium)],
                           [sg.RealtimeButton('<Pan',key = '-KNOB_ClkS-PANKNOB',size=small),sg.Push(),sg.RealtimeButton('<<Pan',key = '-KNOB_ClkL-PANKNOB',size=small)],
                           [sg.RealtimeButton('Pan>',key = '-KNOB_aClkS-PANKNOB',size=small),sg.Push(),sg.RealtimeButton('Pan>>',key = '-KNOB_aClkL-PANKNOB',size=small)],
                           [sg.RealtimeButton('<',key = '-BUTTON-SEND_PREv',size=small),sg.Push(),sg.RealtimeButton('>',key = '-BUTTON-SEND_NEXt',size=small)]
                          ]

misc_left               = [[sg.Button('Touch Off',key = '-BUTTON-SEND_TOUCHSCReen',size=medium)],
                           [sg.Button('Save',key='-BUTTON-SEND_USER',size=medium)]
                          ]
misc_right              = [[sg.Button('Default Setup',key='-BUTTON-SEND_DEFaultsetup',size=medium)],
                           [sg.Button('Autoset',key='-BUTTON-SEND_AUTOset',size=medium)]
                          ]

save_utilities          = [
                           [sg.Button('Screenshot to Clipboard',key='-BUTTON-SCREENSHOT-CLIPBOARD-',size=medium),sg.Push(),sg.Button('Session to Clipboard',key='-BUTTON-SESSION-CLIPBOARD-',size=medium)],
                           #[sg.SaveAs('Save Session',target='-SAVE-LOCATION-',file_types=[('.tss','Tektronix Session Format')],size=medium),sg.Push()], 
                          ]

layout_main             = [[],#,sg.Text('Socket:'),sg.Input(f'{sg.user_settings_get_entry("-TEXT-SOCKET-",default="")}',size=4,key='-TEXT-SOCKET-',change_submits=True)
                           [sg.Column(connect_layout,element_justification='center'),sg.Push(),sg.Column(disconnect_layout,element_justification='center')],
                           [sg.Column(CurFast_layout,element_justification='center'),sg.Push(),sg.Column(HiresClear_layout,element_justification='center')],
                           [sg.Column(knobs_layout,element_justification='center'),sg.Push(),sg.Column(trigger_layout,element_justification='center')],
                           [sg.Push(),sg.Text('Vertical'),sg.Push()],
                           [sg.Column(vertical_layout_left,element_justification='center'),sg.Push(),sg.Column(vertical_layout_right,element_justification='center')],
                           [sg.Push(),sg.Text('Horizontal'),sg.Push()],
                           [sg.Column(horizontal_layout_left,element_justification='center'),sg.Push(),sg.Column(horizontal_layout_right,element_justification='center')],
                           [sg.Column(misc_left,element_justification='center'),sg.Push(),sg.Column(misc_right,element_justification='center')],
                           [sg.Push(),sg.Text('Remote Save Utilities'),sg.Push()],
                           [sg.Column(save_utilities,element_justification='center')],
                          ]

layout_settings         = [[sg.Push(),sg.Text('General Settings'),sg.Push()],
                           [sg.Checkbox('Connect on Startup?',default = sg.user_settings_get_entry('-SETTING-AUTOCONNECT-',default=False),key='-SETTING-AUTOCONNECT-',change_submits=True)],
                           [sg.Checkbox('Stay on top?',key='-SETTING-TOP-',default=sg.user_settings_get_entry('-SETTING-TOP-'),change_submits=True)],
                           [sg.Text('Knob scroll speed, in mS:'),sg.Push()],
                           [sg.Slider((25,1000),default_value=sg.user_settings_get_entry('-SETTING-SCROLL-SPEED-',default=250),key='-SETTING-SCROLL-SPEED-',orientation='horizontal',change_submits=True)],
                           [sg.Text('')],
                           [sg.Push(),sg.Text('Save Utilities Settings'),sg.Push()],
                           [sg.Text('On Scope Temp Storage:')],
                           [sg.Input(sg.user_settings_get_entry('-SETTING-SCOPE-FILE-',default='C:/Temp/RFP/Files'),key='-SETTING-SCOPE-FILE-',size=35,change_submits=True)],
                           [sg.Text('On PC Temp Storage:')],
                           [sg.Input(sg.user_settings_get_entry('-SETTING-PC-FILE-',default='C:/Temp/RFP/Files'),key='-SETTING-PC-FILE-',size=35,change_submits=True),sg.Push(),sg.FolderBrowse(target='-SETTING-PC-FILE-')],
                           [sg.Text('Screenshot to Clipboard default file name/type:')],
                           [sg.Input(sg.user_settings_get_entry('-SETTING-SCREENCAP-NAME-',default='ScreenCapture.png'),key='-SETTING-SCREENCAP-NAME-',size=35,change_submits=True)],
                           [sg.Text('Session to Clipboard default file name:')],
                           [sg.Input(sg.user_settings_get_entry('-SETTING-SESSION-NAME-',default='Session.tss'),key='-SETTING-SESSION-NAME-',size=35,change_submits=True)],
                           [sg.Text('File transfer size limit, in bytes:')],
                           [sg.Input(sg.user_settings_get_entry('-SETTING-MAXFILESIZE-',default=20000000),key='-SETTING-MAXFILESIZE-',size=35,change_submits=True)],
                           [], # User macro definitions,
                          ]

layout_save             = [[sg.Push(),sg.Text('Save Utilities'),sg.Push()],
                           [sg.SaveAs('Save Screenshot',target='-SETTING-SAVE-LOCATION-',file_types=[('Screenshot - Portable Network Graphic','.png'),('Screenshot - JPEG','.jpg')],size=medium),sg.Push(),sg.Button('Screenshot to Clipboard',key='-BUTTON-SCREENSHOT-CLIPBOARD-',size=medium)],
                           [sg.SaveAs('Save Setup',target='-SETTING-SAVE-LOCATION-',file_types=[('Tektronix - Scope Setup','.set')],size=medium),sg.Push(),sg.SaveAs('Save Session',target='-SETTING-SAVE-LOCATION-',file_types=[('Tektronix - Scope Session File','*.tss')],size=medium)],
                           [sg.Input(sg.user_settings_get_entry('-SETTING-SAVE-LOCATION-',default=''),key='-SETTING-SAVE-LOCATION-',size=35,change_submits=True),sg.Push(),sg.Button('Save',key='-BUTTON-SAVE-')],
                          ]

layout                  = [[sg.TabGroup([[sg.Tab('Scope',layout_main),sg.Tab('Save',layout_save),sg.Tab('Settings',layout_settings)]])],
                           [sg.Exit(),sg.Push(),sg.Text("SCPI:"),sg.Input('Related SCPI commands',key='-SCPI-HINT-',readonly=True,size=30)]
                          ]