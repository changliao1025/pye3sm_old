from abc import ABCMeta, abstractmethod

class pye3sm(object):
    __metaclass__ = ABCMeta
    #aParameter={}

    iFlag_debug=0
    iFlag_branch =0
    iFlag_continue=0
    iFlag_resubmit=0
    iFlag_short=0
    
    RES=''
    COMPSET=''
    PROJECT=''
    MACH=''
   
    sCIME_directory=''
   
    sWorkspace_forcing=''
    sWorkspace_analysis=''
    sWorkspace_cases=''
    sFilename_mask=''

    def __init__(self, aParameter):
        print('PEST model is being initialized')
        #self.aParameter = aParameter

        #required with default variables

        #optional
        if 'iFlag_debug' in aParameter:
            self.iFlag_debug             = int(aParameter[ 'iFlag_debug'])
        if 'iFlag_branch' in aParameter:
            self.iFlag_branch             = int(aParameter[ 'iFlag_branch'])
        if 'iFlag_continue' in aParameter:
            self.iFlag_continue             = int(aParameter[ 'iFlag_continue'])
        if 'iFlag_resubmit' in aParameter:
            self.iFlag_resubmit             = int(aParameter[ 'iFlag_resubmit'])
        if 'iFlag_short' in aParameter:
            self.iFlag_short             = int(aParameter[ 'iFlag_short'])
      
     
        if 'RES' in aParameter:
            self.RES = aParameter['RES']
        if 'COMPSET' in aParameter:
            self.COMPSET = aParameter['COMPSET']
        if 'PROJECT' in aParameter:
            self.PROJECT = aParameter['PROJECT']
        if 'MACH' in aParameter:
            self.MACH = aParameter['MACH']
        
        if 'sCIME_directory' in aParameter:
            self.sCIME_directory    = aParameter[ 'sCIME_directory']
        if 'sWorkspace_analysis' in aParameter:
            self.sWorkspace_analysis       = aParameter[ 'sWorkspace_analysis']
        if 'sWorkspace_cases' in aParameter:
            self.sWorkspace_cases    = aParameter[ 'sWorkspace_cases']
        
        if 'sWorkspace_forcing' in aParameter:
            self.sWorkspace_forcing= aParameter[ 'sWorkspace_forcing']

        if 'sFilename_mask' in aParameter:
            self.sFilename_mask               = aParameter[ 'sFilename_mask']
        

       
        pass
