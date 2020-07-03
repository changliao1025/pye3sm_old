from abc import ABCMeta, abstractmethod

class pye3sm(object):
    __metaclass__ = ABCMeta
    aParameter={}

    iFlag_debug=0
    iFlag_branch =0
    iFlag_continue=0
    iFlag_resubmit=0
    iFlag_short=0
    iCase_index=0
    iYear_start=0
    iYear_end=0
    iYear_data_start=0
    iYear_data_end=0
    nmonth=0
    dConversion=0.0

    RES=''
    COMPSET=''
    PROJECT=''
    MACH=''
    sDirectory_case=''
    sDirectory_run=''
    sCIME_directory=''
    sModel=''
    sRegion=''
    sCase=''
    sDate =''
    sVariable=''
    sFilename_clm_namelist=''
    sFilename_mask=''
    sWorkspace_analysis=''
    sWorkspace_cases=''
    sWorkspace_case=''
    sWorkspace_analysis_case=''
    sWorkspace_simulation_case=''
    sWorkspace_simulation_case_build=''
    sWorkspace_simulation_case_run=''
    sWorkspace_forcing=''

    def __init__(self, aParameter):
        print('PEST model is being initialized')
        self.aParameter = aParameter

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
        if 'iCase_index' in aParameter:
            self.iCase_index             = int(aParameter[ 'iCase_index'])
        if 'iYear_start' in aParameter:
            self.iYear_start             = int(aParameter[ 'iYear_start'])
        if 'iYear_end' in aParameter:
            self.iYear_end             = int(aParameter[ 'iYear_end'])
        if 'iYear_data_start' in aParameter:
            self.iYear_data_start             = int(aParameter[ 'iYear_data_start'])
        if 'iYear_data_end' in aParameter:
            self.iYear_data_end             = int(aParameter[ 'iYear_data_end'])
        if 'nmonth' in aParameter:
            self.nmonth             = int(aParameter[ 'nmonth'])
        if 'dConversion' in aParameter:
            self.dConversion             = float(aParameter[ 'dConversion'])
        if 'RES' in aParameter:
            self.RES = aParameter['RES']
        if 'COMPSET' in aParameter:
            self.COMPSET = aParameter['COMPSET']
        if 'PROJECT' in aParameter:
            self.PROJECT = aParameter['PROJECT']
        if 'MACH' in aParameter:
            self.MACH = aParameter['MACH']
        if 'sDirectory_case' in aParameter:
            self.sDirectory_case = aParameter['sDirectory_case']
        if 'sDirectory_run' in aParameter:
            self.sDirectory_run       = aParameter[ 'sDirectory_run' ]
        if 'sCIME_directory' in aParameter:
            self.sCIME_directory    = aParameter[ 'sCIME_directory']
        if 'sModel' in aParameter:
            self.sModel                = aParameter[ 'sModel']
        if 'sRegion' in aParameter:
            self.sRegion               = aParameter[ 'sRegion']
        if 'sCase' in aParameter:
            self.sCase                = aParameter[ 'sCase']
        if 'sDate' in aParameter:
            self.sDate                = aParameter[ 'sDate']
        if 'sVariable' in aParameter:
            self.sVariable               = aParameter[ 'sVariable']
        if 'sFilename_clm_namelist' in aParameter:
            self.sFilename_clm_namelist      = aParameter[ 'sFilename_clm_namelist']
        if 'sFilename_mask' in aParameter:
            self.sFilename_mask               = aParameter[ 'sFilename_mask']
        if 'sWorkspace_analysis' in aParameter:
            self.sWorkspace_analysis       = aParameter[ 'sWorkspace_analysis']
        if 'sWorkspace_cases' in aParameter:
            self.sWorkspace_cases    = aParameter[ 'sWorkspace_cases']
        if 'sWorkspace_case' in aParameter:
            self.sWorkspace_case = aParameter[ 'sWorkspace_case']

        if 'sWorkspace_simulation_case' in aParameter:
            self.sWorkspace_simulation_case= aParameter[ 'sWorkspace_simulation_case']
        if 'sWorkspace_analysis_case' in aParameter:
            self.sWorkspace_analysis_case= aParameter[ 'sWorkspace_analysis_case']
        if 'sWorkspace_simulation_case_build' in aParameter:
            self.sWorkspace_simulation_case_build= aParameter[ 'sWorkspace_simulation_case_build']
        if 'sWorkspace_simulation_case_run' in aParameter:
            self.sWorkspace_simulation_case_run= aParameter[ 'sWorkspace_simulation_case_run']
        if 'sWorkspace_forcing' in aParameter:
            self.sWorkspace_forcing= aParameter[ 'sWorkspace_forcing']

        sCase_index = "{:03d}".format( self.iCase_index )
        sCase = self.sModel + self.sDate + sCase_index
        self.sCase = sCase
        pass
