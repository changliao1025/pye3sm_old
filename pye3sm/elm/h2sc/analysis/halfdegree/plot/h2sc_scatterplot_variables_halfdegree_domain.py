import os, sys
import argparse
import numpy as np

sSystem_paths = os.environ['PATH'].split(os.pathsep)
sys.path.extend(sSystem_paths)
from pyes.system.define_global_variables import *

sPath_pye3sm = sWorkspace_code +  slash + 'python' + slash + 'e3sm' + slash + 'pye3sm'
sys.path.append(sPath_pye3sm)
from pye3sm.shared.e3sm import pye3sm
from pye3sm.shared.case import pycase
from pye3sm.shared.pye3sm_read_configuration_file import pye3sm_read_e3sm_configuration_file
from pye3sm.shared.pye3sm_read_configuration_file import pye3sm_read_case_configuration_file
from pye3sm.elm.general.halfdegree.plot.elm_scatterplot_variables_halfdegree_domain import elm_scatterplot_variables_halfdegree_domain

def h2sc_scatterplot_variables_halfdegree_domain(oE3SM_in, \
                                                 oCase_x_in, \
                                                 oCase_y_in,\
                                                 dMin_x_in = None, \
                                                 dMax_x_in = None, \
                                                 dMin_y_in = None, \
                                                 dMax_y_in = None, \
                                                 dSpace_x_in = None, \
                                                 dSpace_y_in = None, \
                                                 sLabel_x_in=None,\
                                                 sLabel_y_in=None,\
                                                     sLabel_legend_in=None):

    elm_scatterplot_variables_halfdegree_domain(oE3SM_in, \
                                                oCase_x_in, \
                                                oCase_y_in,\
                                                dMin_x_in = dMin_x_in, \
                                                dMax_x_in = dMax_x_in, \
                                                dMin_y_in = dMin_y_in, \
                                                dMax_y_in = dMax_y_in, \
                                                dSpace_x_in = dSpace_x_in, \
                                                dSpace_y_in = dSpace_y_in, \
                                                sLabel_x_in = sLabel_x_in, \
                                                sLabel_y_in= sLabel_y_in,\
                                                    sLabel_legend_in=sLabel_legend_in)

if __name__ == '__main__':
    iFlag_debug = 1
    if iFlag_debug == 1:
        iIndex_start = 9
        iIndex_end = 9
    else:
        parser = argparse.ArgumentParser()
        parser.add_argument("--iIndex_start", help = "the path",   type = int)
        parser.add_argument("--iIndex_end", help = "the path",   type = int)
        pArgs = parser.parse_args()
        iIndex_start = pArgs.iIndex_start
        iIndex_end = pArgs.iIndex_end

    sModel = 'h2sc'
    sRegion = 'global'
    sDate = '20200924'

    iYear_start = 1979
    iYear_end = 2008

    sFilename_e3sm_configuration = '/qfs/people/liao313/workspace/python/e3sm/pye3sm/pye3sm/shared/e3sm.xml'
    sFilename_case_configuration = '/qfs/people/liao313/workspace/python/e3sm/pye3sm/pye3sm/shared/case.xml'

    aParameter_e3sm = pye3sm_read_e3sm_configuration_file(sFilename_e3sm_configuration)
    print(aParameter_e3sm)
    oE3SM = pye3sm(aParameter_e3sm)

    sLabel_x = 'Surface slope (percent)'
    sLabel_y = 'Water table depth (m)'

    iCase_index_start = iIndex_start
    iCase_index_end = iIndex_end
    aCase_index = np.arange(iCase_index_start, iCase_index_end + 1, 1)

        #iCase_index = 240
    for iCase_index in (aCase_index):
        sVariable = 'sur_slp'
        dConversion = 100
        aParameter_case  = pye3sm_read_case_configuration_file(sFilename_case_configuration,\
                                                               iCase_index_in =  iCase_index ,\
                                                               iYear_start_in = iYear_start, \
                                                               iYear_end_in = iYear_end,\
                                                               dConversion_in= dConversion,\
                                                               sDate_in= sDate,\
                                                               sVariable_in = sVariable )
        #print(aParameter_case)
        oCase_x  = pycase(aParameter_case)
        sVariable = 'zwt'
        aParameter_case  = pye3sm_read_case_configuration_file(sFilename_case_configuration,\
                                                               iCase_index_in =  iCase_index ,\
                                                               iYear_start_in = iYear_start, \
                                                               iYear_end_in = iYear_end,\
                                                               sDate_in= sDate,\
                                                               sVariable_in = sVariable )
        #print(aParameter_case)
        oCase_y  = pycase(aParameter_case)
        h2sc_scatterplot_variables_halfdegree_domain(oE3SM, \
                                                     oCase_x,\
                                                     oCase_y,\
                                                     dMin_x_in = 0,\
                                                     dMax_x_in = 10, \
                                                     dMin_y_in = 0, \
                                                     dMax_y_in = 40, \
                                                     dSpace_x_in = 1, \
                                                     dSpace_y_in = 10, \
                                                     sLabel_x_in = sLabel_x, \
                                                     sLabel_y_in = sLabel_y)

    print('finished')
