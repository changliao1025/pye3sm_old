import os, sys
import numpy as np
import datetime

import scipy.stats



from pyearth.system.define_global_variables import *
from pyearth.gis.gdal.read.gdal_read_geotiff_file import gdal_read_geotiff_file_multiple_band
from pyearth.visual.scatter.scatter_plot_data_density import scatter_plot_data_density
from pyearth.visual.scatter.scatter_plot_data import scatter_plot_data

from pye3sm.shared.e3sm import pye3sm
from pye3sm.shared.case import pycase

def elm_scatterplot_variable_2d(oE3SM_in,\
                                         aData_x_in,\
                                         oCase_x_in, \
                                         iFlag_scientific_notation_x_in=None,\
                                         iFlag_scientific_notation_y_in=None,\
                                         iFlag_log_x_in=None,\
                                         iFlag_log_y_in=None,\
                                         dMin_x_in = None, \
                                         dMax_x_in = None, \
                                         dMin_y_in = None, \
                                         dMax_y_in = None, \
                                         dSpace_x_in = None, \
                                         dSpace_y_in = None, \
                                         sLabel_x_in = None, \
                                         sLabel_y_in = None,\
                                         sLabel_legend_in =None   ):



    sModel = oCase_x_in.sModel
    sRegion = oCase_x_in.sRegion

    iYear_start = oCase_x_in.iYear_start
    iYear_end = oCase_x_in.iYear_end
    iFlag_same_grid = oCase_x_in.iFlag_same_grid

    dConversion = oCase_x_in.dConversion
    sVariable_x = oCase_x_in.sVariable
    sVariable_y = oCase_y_in.sVariable
    sCase = oCase_x_in.sCase

    sWorkspace_analysis_case_x = oCase_x_in.sWorkspace_analysis_case
    sWorkspace_analysis_case_y = oCase_y_in.sWorkspace_analysis_case

   
    #plot
    sWorkspace_analysis_case_variable_x = sWorkspace_analysis_case_x + slash + sVariable_x
    sWorkspace_analysis_case_variable_y = sWorkspace_analysis_case_y + slash + sVariable_y
    sWorkspace_analysis_case_grid = sWorkspace_analysis_case_variable_y + slash + 'scatterplot'
    if not os.path.exists(sWorkspace_analysis_case_grid):
        os.makedirs(sWorkspace_analysis_case_grid)
        pass

    sWorkspace_variable_dat = sWorkspace_analysis_case_x + slash + sVariable_x + slash + 'tiff'
    #read the stack data
    sFilename_x = sWorkspace_variable_dat + slash + sVariable_x  + sExtension_tiff
    aData_all_x = gdal_read_geotiff_file_multiple_band(sFilename_x)
    aVariable_x = np.array(aData_all_x[0]).astype(float)

    sWorkspace_variable_dat = sWorkspace_analysis_case_y + slash + sVariable_y +  slash + 'tiff'
    #read the stack data
    sFilename_y = sWorkspace_variable_dat + slash + sVariable_y  + sExtension_tiff
    aData_all_y = gdal_read_geotiff_file_multiple_band(sFilename_y)
    aVariable_y = np.array(aData_all_y[0]).astype(float)

    #reshape the data
    #pick a year and month as a snapshot
    iYear = 2000
    iMonth = 8
    iIndex  = ( iYear - iYear_start ) * 12 + iMonth
    x = aVariable_x[iIndex, :, :]
    y = aVariable_y[iIndex, :, :]

    #remove missing value
    good_index = np.where(  (x != missing_value)&(y != missing_value)  )
    x= x[good_index]
    y= y[good_index]

    aCorrelation = scipy.stats.kendalltau(x, y)
    print(aCorrelation)

    x = x * oCase_x_in.dConversion
    y = y * oCase_y_in.dConversion

    x.flatten()
    y.flatten()

    

    if iFlag_log_y_in == 1:
        aData_y = np.log10(y)
        dMin_y_dummy = aData_y[np.isfinite(aData_y)].min()
        #set inf to min
        bad_index = np.where( np.isinf(  aData_y) == True  )
        aData_y[bad_index] = dMin_y_dummy
        #we can also calculate correlation here
        y= aData_y

    #we could have two options to produce simple scatter plot or density map
    sFilename_out = sWorkspace_analysis_case_grid + slash + sVariable_x + '_' + sVariable_y + '_scatterplot.png'
    scatter_plot_data(x, y,\
                              sFilename_out,\
                              iSize_x_in = 8,\
                              iSize_y_in = 8, \
                              iFlag_scientific_notation_x_in=iFlag_scientific_notation_x_in,\
                              iFlag_scientific_notation_y_in=iFlag_scientific_notation_y_in,\
                              iFlag_log_x_in=iFlag_log_x_in,\
                              iFlag_log_y_in=iFlag_log_y_in,\
                                iFlag_lowess_in=1,\
                              dMin_x_in = dMin_x_in, \
                              dMax_x_in = dMax_x_in, \
                              dMin_y_in = dMin_y_in, \
                              dMax_y_in = dMax_y_in, \
                              dSpace_x_in = dSpace_x_in, \
                              dSpace_y_in = dSpace_y_in, \
                              sTitle_in = '', \
                              sLabel_x_in= sLabel_x_in,\
                              sLabel_y_in= sLabel_y_in,\
                              sLabel_legend_in = sLabel_legend_in)

    sFilename_out = sWorkspace_analysis_case_grid + slash + sVariable_x + '_' + sVariable_y + '_densityplot.png'
    scatter_plot_data_density(x, y,\
                              sFilename_out,\
                              iSize_x_in = 8,\
                              iSize_y_in = 8, \
                              iFlag_scientific_notation_x_in=iFlag_scientific_notation_x_in,\
                              iFlag_scientific_notation_y_in=iFlag_scientific_notation_y_in,\
                              iFlag_log_x_in=iFlag_log_x_in,\
                              iFlag_log_y_in=iFlag_log_y_in,\
                              dMin_x_in = dMin_x_in, \
                              dMax_x_in = dMax_x_in, \
                              dMin_y_in = dMin_y_in, \
                              dMax_y_in = dMax_y_in, \
                              dSpace_x_in = dSpace_x_in, \
                              dSpace_y_in = dSpace_y_in, \
                              sTitle_in = '', \
                              sLabel_x_in= sLabel_x_in,\
                              sLabel_y_in= sLabel_y_in,\
                              sLabel_legend_in = sLabel_legend_in)

    print("finished")



