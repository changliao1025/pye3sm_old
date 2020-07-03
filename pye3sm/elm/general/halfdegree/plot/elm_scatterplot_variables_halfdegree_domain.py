import os, sys
import numpy as np
import numpy.ma as ma
import datetime

sSystem_paths = os.environ['PATH'].split(os.pathsep)
sys.path.extend(sSystem_paths)

from pyes.system.define_global_variables import *
from pyes.gis.envi.envi_write_header import envi_write_header
from pyes.gis.gdal.read.gdal_read_envi_file_multiple_band import gdal_read_envi_file_multiple_band
from pyes.visual.scatter.scatter_plot_data_density import scatter_plot_data_density
from pyes.gis.gdal.read.gdal_read_geotiff import gdal_read_geotiff

sPath_pye3sm = sWorkspace_code + slash + 'python' + slash + 'e3sm' + slash + 'e3sm_python'
sys.path.append(sPath_pye3sm)

from e3sm.shared import oE3SM
from e3sm.shared.e3sm_read_configuration_file import e3sm_read_configuration_file

def elm_scatterplot_variables_halfdegree_domain(sFilename_configuration_x_in,\
                                    sFilename_configuration_y_in, \
                                   iCase_index, \
                                   iYear_start_in = None,\
                                   iYear_end_in = None,\
                                   iFlag_same_grid_in = None,\
                                        dMin_x_in = None, \
    dMax_x_in = None, \
    dMin_y_in = None, \
    dMax_y_in = None, \
    dSpace_x_in = None, \
    dSpace_y_in = None, \
                                   sDate_in = None, \
                                       sLabel_x_in = None, \
                                       sLabel_y_in = None,\
                                           sLabel_legend_in =None, \
                                       ):

    #extract information
    e3sm_read_configuration_file(sFilename_configuration_x_in,\
                                 iCase_index_in = iCase_index, \
                                 iYear_start_in = iYear_start_in,\
                                 iYear_end_in = iYear_end_in,\
                                 sDate_in= sDate_in)

    sModel = oE3SM.sModel
    sRegion = oE3SM.sRegion
    if iYear_start_in is not None:
        iYear_start = iYear_start_in
    else:
        iYear_start = oE3SM.iYear_start
    if iYear_end_in is not None:
        iYear_end = iYear_end_in
    else:
        iYear_end = oE3SM.iYear_end

    if iFlag_same_grid_in is not None:
        iFlag_same_grid = iFlag_same_grid_in
    else:
        iFlag_same_grid = 0

    print('The following model is processed: ', sModel)
    if (sModel == 'h2sc'):
        pass
    else:
        if (sModel == 'vsfm'):
            aDimension = [96, 144]
        else:
            pass
    dConversion = oE3SM.dConversion
    sVariable_x = oE3SM.sVariable.lower()
 
    e3sm_read_configuration_file(sFilename_configuration_y_in,\
                                 iCase_index_in = iCase_index, \
                                 iYear_start_in = iYear_start_in,\
                                 iYear_end_in = iYear_end_in,\
                                 sDate_in= sDate_in)
    sVariable_y = oE3SM.sVariable.lower()
    sCase = oE3SM.sCase
    sWorkspace_simulation_case_run =oE3SM.sWorkspace_simulation_case_run
    sWorkspace_analysis_case = oE3SM.sWorkspace_analysis_case

    iFlag_optional = 1

    
    nrow = 360
    ncolumn = 720
    sWorkspace_data_auxiliary_basin = sWorkspace_data + slash + sModel + slash + sRegion + slash \
        + 'auxiliary' + slash + 'basins' 
    aBasin = ['amazon','congo','mississippi','yangtze']

    nDomain = len(aBasin)
    aMask = np.full( (nDomain, nrow, ncolumn), 0, dtype=int)
    for i in range(nDomain):
        sFilename_basin = sWorkspace_data_auxiliary_basin + slash + aBasin[i] + slash + aBasin[i] + '.tif'
        dummy = gdal_read_geotiff(sFilename_basin)
        aMask[i, :,:] = dummy[0]
    
    
    sWorkspace_variable_dat = sWorkspace_analysis_case + slash + sVariable_x.lower() +    slash + 'dat'
    #read the stack data

    sFilename_x = sWorkspace_variable_dat + slash + sVariable_x.lower()  + sExtension_envi

    aData_all_x = gdal_read_envi_file_multiple_band(sFilename_x)
    aVariable_x = aData_all_x[0]

    sWorkspace_variable_dat = sWorkspace_analysis_case + slash + sVariable_y.lower() +    slash + 'dat'
    #read the stack data

    sFilename_y = sWorkspace_variable_dat + slash + sVariable_y.lower()  + sExtension_envi

    aData_all_y = gdal_read_envi_file_multiple_band(sFilename_y)
    aVariable_y = aData_all_y[0]


    #plot
    sWorkspace_analysis_case_variable = sWorkspace_analysis_case + slash + sVariable_x
    if not os.path.exists(sWorkspace_analysis_case_variable):
        os.makedirs(sWorkspace_analysis_case_variable)
    sWorkspace_analysis_case_grid = sWorkspace_analysis_case_variable + slash + 'scatterplot'
    if not os.path.exists(sWorkspace_analysis_case_grid):
        os.makedirs(sWorkspace_analysis_case_grid)



    #reshape the data
    #pick a year and month
    iYear = 2000
    iMonth = 8
    iIndex  = ( iYear - iYear_start ) * 12 + iMonth
    x0 = aVariable_x[iIndex, :, :]
    y0 = aVariable_y[iIndex, :, :]


    for iDomain in np.arange(nDomain):
        sDomain = aBasin[iDomain]
        sLabel_legend = sDomain.title()
        #apply domain mask
        dummy_mask0 = aMask[iDomain, :, :]
        dummy_mask1 = np.reshape(dummy_mask0, (nrow, ncolumn))
        dummy_mask = 1 - dummy_mask1
        x1 = ma.masked_array(x0, mask= dummy_mask)
        y1 = ma.masked_array(y0, mask= dummy_mask)
        #remove missing value
        good_index = np.where(  (x1 != missing_value)&(y1 != missing_value)  ) 
        x2= x1[good_index]
        y2= y1[good_index]

        good_index = np.where(  (x2 > 0.001)&(y2 < 60)  ) 
        x3 = x2[good_index]
        y3 = y2[good_index]

        x=x3[~x3.mask]
        y=y3[~y3.mask]
        sFilename_out = sWorkspace_analysis_case_grid + slash + sVariable_x + '-' +  sVariable_y +'-'+ sDomain + '_scatterplot.png'

        scatter_plot_data_density(x, y,\
                                              sFilename_out,\
                                              iSize_x_in = 8,\
                                              iSize_y_in = 8, \
                                            dMin_x_in = dMin_x_in, \
                                    dMax_x_in = dMax_x_in, \
                                    dMin_y_in = dMin_y_in, \
                                    dMax_y_in = dMax_y_in, \
                                    dSpace_x_in = dSpace_x_in, \
                                    dSpace_y_in = dSpace_y_in, \
                                              sTitle_in = '', \
                                              sLabel_x_in= sLabel_x_in,\
                                              sLabel_y_in= sLabel_y_in,\
                                              sLabel_legend_in = sLabel_legend)

    print("finished")


if __name__ == '__main__':
    import argparse
