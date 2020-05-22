import os
import h5py
import numpy as np
import pandas as pd
import geopandas as gp
import holoviews as hv
import geoviews as gv

from shapely.geometry import Point
from geoviews import opts, tile_sources as gvts
gv.extension('bokeh', 'matplotlib')


def open_sds(gedi_data, beam_name):
    lon_sample = []
    lat_sample = []
    shot_sample = []
    quality_sample = []
    beam_sample = []

    lats = gedi_data[f'{beam_name}/lat_lowestmode'][()]
    lons = gedi_data[f'{beam_name}/lon_lowestmode'][()]
    shots = gedi_data[f'{beam_name}/shot_number'][()]
    quality = gedi_data[f'{beam_name}/quality_flag'][()]

    for i in range(len(shots)):
        if i % 100 == 0:
            shot_sample.append(str(shots[i]))
            lon_sample.append(lons[i])
            lat_sample.append(lats[i])
            quality_sample.append(quality[i])
            beam_sample.append(beam_name)

    latslons = pd.DataFrame({'Beam': beam_sample, 'Shot Number': shot_sample, 'Longitude': lon_sample,
                             'Latitude': lat_sample, 'Quality Flag': quality_sample})
    latslons['geometry'] = latslons.apply(lambda row: Point(row.Longitude, row.Latitude), axis=1)
    latslons = gp.GeoDataFrame(latslons)
    latslons = latslons.drop(columns=['Latitude', 'Longitude'])
    # latslons['geometry'][0]

    del beam_sample, quality, quality_sample, lat_sample, lats, lon_sample, lons, shot_sample, shots


def get_data(path):
    """
    :return:
    """
    gedi_files = [g for g in os.listdir(path) if g.startswith('GEDI02_A') and g.endswith('.h5')]

    for item in gedi_files:
        path_to_file = os.path.join(path, item)
        gedi_l2a = h5py.File(path_to_file, 'r')

        list(gedi_l2a.keys())
        for g in gedi_l2a['METADATA']['DatasetIdentification'].attrs:
            print(g)

        beam_names = [g for g in gedi_l2a.keys() if g.startswith('BEAM')]
        open_sds(gedi_l2a, beam_names[0])
