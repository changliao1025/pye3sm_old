
import os, sys, stat
import argparse
import subprocess

sSystem_paths = os.environ['PATH'].split(os.pathsep)
sys.path.extend(sSystem_paths)

from eslib.system.define_global_variables import *

sPath_e3sm_python = sWorkspace_code +  slash + 'python' + slash + 'e3sm' + slash + 'e3sm_python'
sys.path.append(sPath_e3sm_python)
from e3sm.shared import e3sm_global

from e3sm.shared.e3sm_read_configuration_file import e3sm_read_configuration_file

def e3sm_create_case(sFilename_configuration_in,\
    iFlag_branch_in = None, \
    iFlag_continue_in = None, \
    iFlag_debug_in = None,\
    iFlag_resubmit_in=None,\
    iFlag_short_in=None, \
    iCase_index_in = None,\
    iYear_end_in = None, \
    iYear_start_in = None, \
    iYear_data_end_in = None, \
    iYear_data_start_in = None, \
    sDate_in =None     ,\
    sFilename_clm_namelist_in = None, \
    sFilename_datm_namelist_in = None):

    #get configuration
    e3sm_read_configuration_file(sFilename_configuration_in,\
        iFlag_branch_in = iFlag_branch_in, \
        iFlag_continue_in = iFlag_continue_in ,\
        iFlag_debug_in = iFlag_debug_in, \
        iFlag_resubmit_in = iFlag_resubmit_in, \
        iFlag_short_in= iFlag_short_in, \
        iCase_index_in = iCase_index_in,\
        iYear_end_in = iYear_end_in,\
        iYear_start_in =iYear_start_in, \
            iYear_data_end_in = iYear_data_end_in,\
        iYear_data_start_in =iYear_data_start_in, \
        sDate_in= sDate_in,\
        sFilename_clm_namelist_in = sFilename_clm_namelist_in, \
        sFilename_datm_namelist_in = sFilename_datm_namelist_in)

    sDirectory_case = e3sm_global.sDirectory_case
    sDirectory_run = e3sm_global.sDirectory_run
    #start
    #currently we only need to calibrate H2SC so I will not use advanced I/O
    #we will the same variables used by corresponding CIME python script

    sPython=''
    sModel = e3sm_global.sModel #'h2sc'
    sCase = e3sm_global.sCase
    RES = e3sm_global.RES
    COMPSET = e3sm_global.COMPSET
    PROJECT = e3sm_global.PROJECT
    MACH = e3sm_global.MACH
    sCIME_directory = e3sm_global.sCIME_directory
    #GIT_HASH=`git log -n 1 --format=%h`
    iFlag_branch = e3sm_global.iFlag_branch
    iFlag_debug = e3sm_global.iFlag_debug
    iFlag_continue = e3sm_global.iFlag_continue
    iFlag_resubmit = e3sm_global.iFlag_resubmit
    iFlag_short = e3sm_global.iFlag_short

    sCasename = sDirectory_case  + sCase
    sJobname = sModel + sCase
    print(sCasename)
    sSimname = sDirectory_run + slash  + sCase
    sBldname = sSimname + slash + 'bld'
    sRunname = sSimname + slash + 'run'

    nYear = e3sm_global.nYear
    sYear =  "{:04d}".format(nYear)
    sYear_start = "{:04d}".format(e3sm_global.iYear_start)
    sYear_data_start = "{:04d}".format(e3sm_global.iYear_data_start)
    sYear_data_end = "{:04d}".format(e3sm_global.iYear_data_end)

    if (iFlag_short ==1 ):
        sQueue = 'short'
        sWalltime = '2:00:00'        
        sNode = '-10'
        sYear = '1'
    else:
        sQueue = 'slurm'
        sWalltime = '30:00:00'        
        sNode = '-40'
        sYear = '30'

    if(iFlag_continue != 1): #normal condition, no continue, no debug, but with resubmit
        #remove case directory
        if (os.path.exists(sCasename)):
            sCommand = 'rm -rf '  + sCasename
            print(sCommand)
            p = subprocess.Popen(sCommand, shell= True)
            p.wait()

        #remove bld directory
        if (os.path.exists(sBldname)):
            sCommand = 'rm -rf '  + sBldname
            print(sCommand)
            p = subprocess.Popen(sCommand, shell= True)
            p.wait()

        #remove run directory
        if (os.path.exists(sRunname)):
            sCommand = 'rm -rf '  + sRunname
            print(sCommand)
            p = subprocess.Popen(sCommand, shell= True)
            p.wait()

        #create case
        print(sCIME_directory)
        os.chdir(sCIME_directory)
        sCommand = './create_newcase --case ' + sCasename +  ' --res ' + RES \
            + ' --compset ' + COMPSET  + ' --project ' +  PROJECT +  ' --compiler intel --mach compy' + '\n'
        print(sCommand)
        sCommand = sCommand.lstrip()
        p = subprocess.Popen(sCommand, shell= True)
        p.wait()
        print('Finished creating case: ' + sCasename)

        os.chdir(sCasename)
        #Locks variables in env_case.xml after create_newcase.
        #The env_case.xml file can never be unlocked.
        #Locks variables in env_mach_pes.xml after case.setup.
        #To unlock env_mach_pes.xml, run case.setup –clean.
        #Locks variables in env_build.xml after completion of case.build.
        #To unlock env_build.xml, run case.build –clean

        #env_batch.xml: Sets batch system settings such as wallclock time and queue name.
        sCommand = ' ./xmlchange JOB_WALLCLOCK_TIME=' + sWalltime + '\n'
        sCommand = sCommand.lstrip()
        p = subprocess.Popen(sCommand, shell= True)
        p.wait()

        sCommand = ' ./xmlchange JOB_QUEUE=' + sQueue +' --force' + '\n'
        sCommand = sCommand.lstrip()
        p = subprocess.Popen(sCommand, shell= True)
        p.wait()

        #sCommand = ' ./xmlchange --mail-user=' + 'chang.liao@pnnl.gov' +' --force' + '\n'
        #sCommand = sCommand.lstrip()
        #p = subprocess.Popen(sCommand, shell= True)
        #p.wait()

        #env_mach_pes.xml: Sets component machine-specific processor layout (see changing pe layout ).
        #The settings in this are critical to a well-load-balanced simulation (see load balancing).
        sCommand = sPython + ' ./xmlchange NTASKS=' + sNode + '\n'
        sCommand = sCommand.lstrip()
        p = subprocess.Popen(sCommand, shell= True)
        p.wait()                                         

        if(iFlag_branch != 1):
            sCommand = sPython + ' ./xmlchange RUN_TYPE=startup' + '\n'
            sCommand = sCommand.lstrip()
            p = subprocess.Popen(sCommand, shell= True)
            p.wait()

            #env_run.xml: Sets runtime settings such as length of run, frequency of restarts, output of coupler diagnostics,
            #and short-term and long-term archiving. This file can be edited at any time before a job starts.
            sCommand = sPython + ' ./xmlchange RUN_STARTDATE=' + sYear_start +'-01-01,STOP_OPTION=nyears,STOP_N='+ sYear + '\n'
            sCommand = sCommand.lstrip()
            p = subprocess.Popen(sCommand, shell= True)
            p.wait()

            sCommand = sPython + ' ./xmlchange REST_OPTION=nyears,REST_N=10' + '\n'
            sCommand = sCommand.lstrip()
            p = subprocess.Popen(sCommand, shell= True)
            p.wait()

            sCommand = sPython + ' ./xmlchange DATM_CLMNCEP_YR_START=' + sYear_data_start + '\n'
            sCommand = sCommand.lstrip()
            p = subprocess.Popen(sCommand, shell= True)
            p.wait()
            sCommand = sPython + ' ./xmlchange DATM_CLMNCEP_YR_END=' + sYear_data_end + '\n'
            sCommand = sCommand.lstrip()
            p = subprocess.Popen(sCommand, shell= True)
            p.wait()
        else: ##branch run 
            sCommand = sPython + ' ./xmlchange RUN_TYPE=branch' + '\n'
            sCommand = sCommand.lstrip()
            p = subprocess.Popen(sCommand, shell= True)
            p.wait()

            sCommand = sPython + ' ./xmlchange RUN_REFDIR=/compyfs/liao313/e3sm_scratch/h2sc20200210002/run' + '\n'
            sCommand = sCommand.lstrip()
            p = subprocess.Popen(sCommand, shell= True)
            p.wait()

            sCommand = sPython + ' ./xmlchange RUN_REFCASE=h2sc20200210002' + '\n'
            sCommand = sCommand.lstrip()
            p = subprocess.Popen(sCommand, shell= True)
            p.wait()

            sCommand = sPython + ' ./xmlchange RUN_REFDATE=1981-01-01' + '\n'
            sCommand = sCommand.lstrip()
            p = subprocess.Popen(sCommand, shell= True)
            p.wait()

            sCommand = sPython + ' ./xmlchange GET_REFCASE=TRUE' + '\n'
            sCommand = sCommand.lstrip()
            p = subprocess.Popen(sCommand, shell= True)
            p.wait()

            sCommand = sPython + ' ./xmlchange REST_OPTION=nyears,REST_N=5' + '\n'
            sCommand = sCommand.lstrip()
            p = subprocess.Popen(sCommand, shell= True)
            p.wait()

            sCommand = sPython + ' ./xmlchange DATM_CLMNCEP_YR_START='+ sYear_data_start + '\n'
            sCommand = sCommand.lstrip()
            p = subprocess.Popen(sCommand, shell= True)
            p.wait()
            sCommand = sPython + ' ./xmlchange DATM_CLMNCEP_YR_END='+sYear_data_start + '\n'
            sCommand = sCommand.lstrip()
            p = subprocess.Popen(sCommand, shell= True)
            p.wait()

        sCommand = sPython + ' ./case.setup' + '\n'
        sCommand = sCommand.lstrip()
        p = subprocess.Popen(sCommand, shell= True)
        p.wait()

        #copy namelist
        #the mosart will be constant
        sCommand = 'cp ../user_nl_mosart ./user_nl_mosart' + '\n'
        sCommand = sCommand.lstrip()
        p = subprocess.Popen(sCommand, shell= True)
        p.wait()
        #we will generate clm name list in real time
        sCommand = 'cp ' + sFilename_clm_namelist_in + ' ./user_nl_clm' + '\n'
        sCommand = sCommand.lstrip()
        p = subprocess.Popen(sCommand, shell= True)
        p.wait()

        if(sFilename_datm_namelist_in is not None):
            sCommand = 'cp ' + sFilename_datm_namelist_in + ' ./user_nl_datm' + '\n'
            sCommand = sCommand.lstrip()
            p = subprocess.Popen(sCommand, shell= True)
            p.wait()


        #Build and submit
        sCommand = sPython + ' ./case.build' + '\n'
        sCommand = sCommand.lstrip()
        p = subprocess.Popen(sCommand, shell= True)
        p.wait()

        if (iFlag_debug != 1):
            pass
        else:
            #create the timing.checkpoints folder for debug
            os.chdir(sRunname)
            os.mkdir('timing')
            os.chdir('timing')
            os.mkdir('checkpoints')

    else: #special condition, this is a continue run, may debug, also with resubmit

    
        if (iFlag_debug !=1):
            #not debugging
            #sCommand = sPython + ' ./xmlchange RESUBMIT=5' + '\n'
            #sCommand = sCommand.lstrip()
            #p = subprocess.Popen(sCommand, shell= True)
            #p.wait()
            pass

            

        else:
            #debug,
            sCommand = sPython + ' ./xmlchange -file env_build.xml DEBUG=TRUE' + '\n'
            sCommand = sCommand.lstrip()
            p = subprocess.Popen(sCommand)
            p.wait()

            #Build and submit
            sCommand = sPython + ' ./case.build' + '\n'
            sCommand = sCommand.lstrip()
            p = subprocess.Popen(sCommand, shell= True)
            p.wait()

    #run the script anyway
    os.chdir(sCasename)
    sCommand = sPython + ' ./case.submit' + '\n'
    sCommand = sCommand.lstrip()
    #p = subprocess.Popen(sCommand, shell= True, executable='/people/liao313/bin/interactive_bash' )
    p = subprocess.Popen(['/bin/bash', '-i', '-c', sCommand])
    p.wait()

    print('Finished case: ' + sCasename)

if __name__ == '__main__':
    #import argparse
    #parser = argparse.ArgumentParser()
    #parser.add_argument("--iCase", help = "the id of the e3sm case", type=int, choices=range(1000))
    #args = parser.parse_args()

    sModel = 'h2sc'
    sRegion ='global'
    sFilename_configuration = sWorkspace_configuration + slash + sModel + slash \
        + sRegion + slash + 'h2sc_configuration.txt'

    dHydraulic_anisotropy = 0.1
    sHydraulic_anisotropy = "{:0f}".format( dHydraulic_anisotropy)
    iCase = 1

    iFlag_debug = 0
    iFlag_branch = 0
    iFlag_initial = 1
    iFlag_spinup = 0
    iFlag_short = 0
    iFlag_continue = 0
    iFlag_resubmit = 0
    sDate = '20200329'
    sCase =  sModel + sDate + "{:03d}".format(iCase)

    sFilename_clm_namelist = sWorkspace_scratch + slash + '04model' + slash + sModel + slash + sRegion + slash \
        + 'cases' + slash + 'user_nl_clm_' + sCase
    if (iFlag_initial !=1):
        #normal case,      
        ofs = open(sFilename_clm_namelist, 'w')
        sCommand_out = "fsurdat = " + "'" \
            + '/compyfs/inputdata/lnd/clm2/surfdata_map/surfdata_0.5x0.5_simyr2010_c191025_log10.nc' + "'" + '\n'
        ofs.write(sCommand_out)
        sLine = "use_h2sc = .true." + '\n'
        ofs.write(sLine)
        sLine = "hydraulic_anisotropy = " + sHydraulic_anisotropy + '\n'
        ofs.write(sLine)
        ofs.close()
    else:
        ofs = open(sFilename_clm_namelist, 'w')
        sCommand_out = "fsurdat = " + "'" \
            + '/compyfs/inputdata/lnd/clm2/surfdata_map/surfdata_0.5x0.5_simyr2010_c191025_log10.nc' + "'" + '\n'
        ofs.write(sCommand_out)
        sLine = "use_h2sc = .true." + '\n'
        ofs.write(sLine)
        sLine = "hydraulic_anisotropy = " + sHydraulic_anisotropy + '\n'
        ofs.write(sLine)
        #this is a case that use existing restart file
        #be careful with the filename!!!
        
        #sCase_spinup =  sModel + sDate_spinup+ "{:03d}".format(iCase)
        sCase_spinup = sModel + '20200328001'

        sLine = "finidat = '/compyfs/liao313/e3sm_scratch/" \
            + sCase_spinup + '/run/' \
            + sCase_spinup +  ".clm2.rh0.1979-01-01-00000.nc'"  + '\n'
        ofs.write(sLine)
        ofs.close()

    sFilename_datm_namelist = sWorkspace_scratch + slash \
        + '04model' + slash + sModel + slash \
        + sRegion + slash \
        + 'cases' + slash + 'user_nl_datm_' + sCase

    if (iFlag_spinup ==1):
        #this is a case for spin up
        ofs = open(sFilename_datm_namelist, 'w')
        sLine = 'taxmode = "cycle", "cycle", "cycle"' + '\n'
        ofs.write(sLine)
    else:
        #no spin up needed
        pass
        
    #write the clm namelist file
    if (iFlag_spinup ==1):   
        e3sm_create_case(sFilename_configuration, \
                    iFlag_branch_in= iFlag_branch, \
                    iFlag_continue_in = iFlag_continue, \
                    iFlag_debug_in = iFlag_debug, \
                    iFlag_resubmit_in = iFlag_resubmit, \
                    iFlag_short_in = iFlag_short, \
                    iCase_index_in = iCase, \
                    iYear_end_in = 1978, \
                    iYear_start_in = 1949, \
                    iYear_data_end_in = 1988, \
                    iYear_data_start_in = 1979, \
                    sDate_in = sDate, \
                    sFilename_clm_namelist_in = sFilename_clm_namelist, \
                    sFilename_datm_namelist_in = sFilename_datm_namelist )
    else:
        e3sm_create_case(sFilename_configuration,\
                    iFlag_continue_in = iFlag_continue, \
                    iFlag_debug_in = iFlag_debug, \
                    iFlag_resubmit_in = iFlag_resubmit, \
                    iFlag_short_in = iFlag_short, \
                    iCase_index_in = iCase, \
                    iYear_end_in = 2008, \
                    iYear_start_in = 1979, \
                    iYear_data_end_in = 2008, \
                    iYear_data_start_in = 1979, \
                    sDate_in = sDate, \
                    sFilename_clm_namelist_in = sFilename_clm_namelist )