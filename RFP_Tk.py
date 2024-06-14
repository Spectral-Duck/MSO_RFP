"""
    Remote Front Panel Toolkit

    The keys from the GUI are decoded to get which message should be sent to the scope.
    Everything after the last _ is the decode, will match something in the dicts below
    First value in the response is the related scpi command, used as a hint for users to quickly find commands related to what they are doing.
    Second value is the actual front panel command sent to the scope.

    Also includes a list of valid instruments to connect to, if the connecting scope is not found in that list, the program will error
"""

import os
def save_to_scope(scope = None, Path = None):
    
    # First verify that the file location exists.  
    # Since FileSystem commands on tekscope doesn't have a query for if a directory exists
    #   os.path.dirname will return the folder of a given file.
    scope.write(f'FILESystem:MKDir "{os.path.dirname(Path)}"')

    # Clear scopes buffer, in case something was already in it previously, to prevent corrupting files.
    scope.write('*CLS')

    # Get file extension from path
    path_split = Path.split('.')
    extension = path_split[-1].lower()

    match extension:
        case  img if img in ['png', 'jpg']:
            # Works well, clean and quick
            #print('requesting screencapture')
            scope.write(f'filesystem:delete "{Path}"') #remote file if it already exists.  
            scope.query("*OPC?")
            scope.write(f'save:image "{Path}"')
            #print("saving Image on scope")
            scope.query("*OPC?")
            
        case wfm if wfm in ['wfm','csv','mat']:
            """
            Saving waveforms is way more complicated than I expected... and I sort of deem it beyond the scope of this project. (for now)
            Flow:
                Have to itterate through the analog channels to determine which are active
                Then itterate through again to see if any digital channels are active
                Then again, to find if any SpectrumView channels are active
                Again, to find if any Math channels are active
                Refs are actually easy, you can directly query for a list of active refs. 
            Now we have the list of which wfms can be saved, unless I missed one...
            Now build the popup that will ask the user to decide which to save.
                Oh yea, and the formats are all over the place for each to save... 

            Beyond what I am wanting to do at this time.


            """
            #print('requesting a waveform')
            pass

        case 'set':
            #print("requesting setup file")
            scope.write(f'filesystem:delete "{Path}"')
            scope.query("*OPC?")
            scope.write(f'SAVe:SETup "{Path}"')
            #print("Saving setup file")
            scope.query("*OPC?")

        case report if report in ['pdf','mht']:
            # Currently able to save both report types, though something causes it to timeout after I try to request transfer to PC
            # Thus I will leave it out of the UI for saving to PC.  
            # Feel free to mess with it.  
            #print('requesting report')
            scope.write(f'filesystem:delete "{Path}"')
            scope.query("*OPC?")
            scope.write(f'SAVe:REPOrt "{Path}"')
            #print("Saving report file")
            scope.query("*OPC?")

        case 'tss':
            #print('requesting a session file')
            scope.write(f'filesystem:delete "{Path}"')
            scope.query("*OPC?")
            scope.write(f'SAVe:SESsion "{Path}"')
            #print("Saving session file")
            scope.query("*OPC?")

def get_file(scope, scope_path, pc_path):

    # First verify the directory exists 
    dir = os.path.dirname(pc_path)
    if not os.path.exists(dir):
        os.mkdir(dir)
    if os.path.isfile(pc_path):
        os.remove(pc_path)
    

    scope.write('*CLS')
    print(scope_path)
    scope.write(f'filesystem:readfile "{scope_path}"')
    data = scope.read_raw()
    scope.query("*OPC?")
    #print(f'Requesting {scope_path} from scope')
    
    file = open(pc_path,'wb') 
    file.write(data)
    #print(f'Saving file to local drive at {pc_path}')
    
    scope.write(f'filesystem:delete "{scope_path}"')
    scope.query('*OPC?')
    #print("Cleaning up, deleteing temp file on scope!")

def get_file_size(scope,file):
    """
    Saves the CWD (current working directory)
    Sets CWD to path
    Gets list of everything in dir
    Find index of desired path, size in bytes will be that index + 2
    set CWD to saved value
    return size of file in bytes
    """
    path = os.path.dirname(file)
    file_name = os.path.basename(file)
    innital_dir = scope.query('FILESystem:CWD?')
    scope.write(f'FILESystem:CWD "{path}"')
    ldir = scope.query(f'FILESystem:LDIR?').replace('"','').replace(',',";").strip("\n").split(';')
    #print(ldir)
    index = ldir.index(file_name)
    scope.write(f'FILESystem:CWD {innital_dir}')
    return(int(ldir[index+2]))

def file_clipboard(Path):
    cmd = f'powershell Set-Clipboard -LiteralPath {Path}'
    os.system(cmd)


# Libraries that handle all of the magic that is the UI
command = { 
 # button press messages
    'RUNSTop'            : ['ACQuire:STOPAfter','FPAnel:PRESS RUNSTop'], 
    'AUTOset'            : ['AUTOset','FPAnel:PRESS AUTOset'],
    'BUS'                : ['BUS:ADDNew','FPAnel:PRESS BUS'],
    'CH1'                : ['SELect:CH<x>','FPAnel:PRESS CH1'],
    'CH2'                : ['SELect:CH<x>','FPAnel:PRESS CH2'],
    'CH3'                : ['SELect:CH<x>','FPAnel:PRESS CH3'],
    'CH4'                : ['SELect:CH<x>','FPAnel:PRESS CH4'],
    'CH5'                : ['SELect:CH<x>','FPAnel:PRESS CH5'],
    'CH6'                : ['SELect:CH<x>','FPAnel:PRESS CH6'],
    'CH7'                : ['SELect:CH<x>','FPAnel:PRESS CH7'],
    'CH8'                : ['SELect:CH<x>','FPAnel:PRESS CH8'],
    'CLEAR'              : ['CLEAR','FPAnel:PRESS CLEAR'],
    'CURsor'             : ['','FPAnel:PRESS CURsor'],
    'DEFaultsetup'       : ['FACtory','FPAnel:PRESS DEFaultsetup'],
    'FASTAcq'            : ['ACQuire:FASTAcq:STATE','FPAnel:PRESS FASTAcq'],
    'FORCetrig'          : ['TRIGger FORCe','FPAnel:PRESS FORCetrig'],
    'GPKNOB1'            : ['','FPAnel:PRESS GPKNOB1'],
    'GPKNOB2'            : ['','FPAnel:PRESS GPKNOB2'],
    'HIGHRES'            : ['ACQuire:MODe HIRes','FPAnel:PRESS HIGHRES'],
    'HORZPOS'            : ['HORizontal:POSition','FPAnel:PRESS HORZPOS'],
    'HORZScale'          : ['HORizontal:SCAle','FPAnel:PRESS HORZScale'],
    'MATh'               : ['MATH:ADDNew "Math<x>"','FPAnel:PRESS MATh'],
    'NEXt'               : ['SEARCH:SEARCH<x>:NAVigate','FPAnel:PRESS NEXt'],
    'PREv'               : ['SEARCH:SEARCH<x>:NAVigate','FPAnel:PRESS PREv'],
    'REF'                : ['REF:ADDNew','FPAnel:PRESS REF'],
    'SETTO50'            : ['TRIGger:{A|B}:LEVel:CH<x>','FPAnel:PRESS SETTO50'],
    'SINGleseq'          : ['ACQuire:STOPAfter','FPAnel:PRESS SINGleseq'],
    'TOUCHSCReen'        : ['TOUCHSCReen:STATE','FPAnel:PRESS TOUCHSCReen'],
    'TRIGMode'           : ['TRIGger:A:MODe','FPAnel:PRESS TRIGMode'],
    'TRIGSlope'          : ['TRIGger:{A|B}:EDGE:SLOpe','FPAnel:PRESS TRIGSlope'],
    'USER'               : ['','FPAnel:PRESS USER'],
    'VERTPOS'            : ['CH<x>:POSition','FPAnel:PRESS VERTPOS'],
    'VERTSCALE'          : ['CH<x>:SCAle','FPAnel:PRESS VERTSCALE'],
    'ZOOM'               : ['DISplay:WAVEView<x>:ZOOM:ZOOM<x>:STATe','FPAnel:PRESS ZOOM'],
 # clockwise small messages
    'ClkS-GPKNOB1'       : ['','FPAnel:TURN GPKNOB1 ,-1'],
    'ClkS-GPKNOB2'       : ['','FPAnel:TURN GPKNOB2 ,-1'],
    'ClkS-HORZPOS'       : ['HORizontal:POSition','FPAnel:TURN HORZPOS ,-1'],
    'ClkS-HORZScale'     : ['HORizontal:SCAle','FPAnel:TURN HORZScale ,-1'],
    'ClkS-PANKNOB'       : ['DISplay:WAVEView<x>:ZOOM:ZOOM<x>:HORizontal:POSition','FPAnel:TURN PANKNOB ,-1'],
    'ClkS-TRIGLevel'     : ['TRIGger:{A|B}:LEVel:CH<x>','FPAnel:TURN TRIGLevel ,-1'],
    'ClkS-VERTPOS'       : ['CH<x>:POSition','FPAnel:TURN VERTPOS ,-1'],
    'ClkS-VERTSCALE'     : ['CH<x>:SCAle','FPAnel:TURN VERTSCALE ,-1'],
    'ClkS-ZOOM'          : ['DISplay:WAVEView<x>:ZOOM:ZOOM<x>:HORizontal:SCALe','FPAnel:TURN ZOOM ,-1'],
 # anti clockwise small messages
    'aClkS-GPKNOB1'      : ['','FPAnel:TURN GPKNOB1 ,1'],
    'aClkS-GPKNOB2'      : ['','FPAnel:TURN GPKNOB2 ,1'],
    'aClkS-HORZPOS'      : ['HORizontal:POSition','FPAnel:TURN HORZPOS ,1'],
    'aClkS-HORZScale'    : ['HORizontal:SCAle','FPAnel:TURN HORZScale ,1'],
    'aClkS-PANKNOB'      : ['DISplay:WAVEView<x>:ZOOM:ZOOM<x>:HORizontal:POSition','FPAnel:TURN PANKNOB ,1'],
    'aClkS-TRIGLevel'    : ['TRIGger:{A|B}:LEVel:CH<x>','FPAnel:TURN TRIGLevel ,1'],
    'aClkS-VERTPOS'      : ['CH<x>:POSition','FPAnel:TURN VERTPOS ,1'],
    'aClkS-VERTSCALE'    : ['CH<x>:SCAle','FPAnel:TURN VERTSCALE ,1'],
    'aClkS-ZOOM'         : ['DISplay:WAVEView<x>:ZOOM:ZOOM<x>:HORizontal:SCALe','FPAnel:TURN ZOOM ,1'],
 # clockwise large messages
    'ClkL-GPKNOB1'       : ['','FPAnel:TURN GPKNOB1 ,-10'],
    'ClkL-GPKNOB2'       : ['','FPAnel:TURN GPKNOB2 ,-10'],
    'ClkL-HORZPOS'       : ['HORizontal:POSition','FPAnel:TURN HORZPOS ,-10'],
    'ClkL-HORZScale'     : ['HORizontal:SCAle','FPAnel:TURN HORZScale ,-10'],
    'ClkL-PANKNOB'       : ['DISplay:WAVEView<x>:ZOOM:ZOOM<x>:HORizontal:POSition','FPAnel:TURN PANKNOB ,-10'],
    'ClkL-TRIGLevel'     : ['TRIGger:{A|B}:LEVel:CH<x>','FPAnel:TURN TRIGLevel ,-10'],
    'ClkL-VERTPOS'       : ['CH<x>:POSition','FPAnel:TURN VERTPOS ,-10'],
    'ClkL-VERTSCALE'     : ['CH<x>:SCAle','FPAnel:TURN VERTSCALE ,-10'],
    'ClkL-ZOOM'          : ['DISplay:WAVEView<x>:ZOOM:ZOOM<x>:HORizontal:SCALe','FPAnel:TURN ZOOM ,-10'],
 # anti clockwise large messages
    'aClkL-GPKNOB1'      : ['','FPAnel:TURN GPKNOB1 ,10'],
    'aClkL-GPKNOB2'      : ['','FPAnel:TURN GPKNOB2 ,10'],
    'aClkL-HORZPOS'      : ['HORizontal:POSition','FPAnel:TURN HORZPOS ,10'],
    'aClkL-HORZScale'    : ['HORizontal:SCAle','FPAnel:TURN HORZScale ,10'],
    'aClkL-PANKNOB'      : ['DISplay:WAVEView<x>:ZOOM:ZOOM<x>:HORizontal:POSition','FPAnel:TURN PANKNOB ,10'],
    'aClkL-TRIGLevel'    : ['TRIGger:{A|B}:LEVel:CH<x>','FPAnel:TURN TRIGLevel ,10'],
    'aClkL-VERTPOS'      : ['CH<x>:POSition','FPAnel:TURN VERTPOS ,10'],
    'aClkL-VERTSCALE'    : ['CH<x>:SCAle','FPAnel:TURN VERTSCALE ,10'],
    'aClkL-ZOOM'         : ['DISplay:WAVEView<x>:ZOOM:ZOOM<x>:HORizontal:SCALe','FPAnel:TURN ZOOM ,10'],
}

valid_instruments = [ #if additional instruments would work, add to list.  
    'MSO22',
    'MSO24',
    #'MDO32', # Command set for the MDO3 is slightly diffrent than MSO, thus RFP half works
    #'MDO34',
    'MSO44',
    'MSO46',
    'MSO44B',
    'MSO46B',
    'MSO54',
    'MSO56',
    'MSO58',
    'MSO54B',
    'MSO56B',
    'MSO58B',
    #'MSO58LP', # Not supported because its lacking a front panel command set
    'MSO64',
    #'LPD64', # Same as 58LP
    'MSO64B',
    'MSO66B',
    'MSO68B',
]