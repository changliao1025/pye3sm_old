import os

from pye3sm.mosart.grid.create_customized_mosart_domain import create_customized_mosart_domain


sFilename_netcdf = '/compyfs/inputdata/rof/mosart/MOSART_Global_half_20210616.nc'
    
lCellID_outlet_in=128418

sFilename_netcdf_out = '/qfs/people/liao313/data/e3sm/mosart/amazon/mosart_half_degree.nc'

create_customized_mosart_domain(sFilename_netcdf,sFilename_netcdf_out, lCellID_outlet_in)