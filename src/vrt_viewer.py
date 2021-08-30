import base64
import io
import os
from osgeo import gdal
import rasterio
from matplotlib import pyplot

def get_base64_image_from_vrt(src_path, output_type, experiment_type = None, xy_resolution = 1000):

    # src_path = '/home/jovyan/data-vol-1/SATELLITE/RESULTS/hu_raster'
    # experiment_type = 'km area level 0 no border 50 continental'.replace(' ', '_')
    # output_type = 'pred'

    if experiment_type is not None:
        full_path = '/'.join([src_path, experiment_type])
        all_subdirs = [d for d in os.listdir(full_path) if os.path.isdir('/'.join([src_path, experiment_type, d]))]
        latest_subdir = max(['/'.join([src_path, experiment_type, d]) for d in all_subdirs], key=os.path.getmtime)
        full_path = latest_subdir
    else:
        full_path = src_path

    print(full_path)
    file_list = []
    for r, d, f in os.walk(full_path):
        print(f)
        for file in f:
            print(file)
            if file[-4:] == '.tif' and f'output_{output_type}' in file:
                file_list.append(os.path.join(r, file))
    print(file_list)


    if output_type in ['prob', 'detailed']: 
        with rasterio.open(file_list[0].replace('prob','detailed')) as ds:
            band_count = ds.count

    vrt_fn = '/tmp/test.vrt'
    if os.path.exists(vrt_fn):
        os.remove(vrt_fn)

    if output_type in ['prob', 'detailed']:
        nodata = 1/band_count
    else:
        nodata = 0

    vrt_options = gdal.BuildVRTOptions(
        xRes = xy_resolution,
        yRes = xy_resolution,
        addAlpha=False,
        srcNodata=nodata,
        VRTNodata=nodata,
        hideNodata = True
    )
    test_vrt = gdal.BuildVRT(
        vrt_fn,
        file_list,
        options=vrt_options
    )

    test_vrt = None

    band = 1

    src = rasterio.open(vrt_fn)
    pyplot.figure(figsize = (40,40))
    data = src.read(band)
    if output_type == 'pred':
        pyplot.imshow(data, cmap='tab20')
    else:
        pyplot.imshow(data, cmap='pink')

    pic_IObytes = io.BytesIO()
    pyplot.savefig(pic_IObytes,  format='png')
    pic_IObytes.seek(0)
    pic_hash = base64.b64encode(pic_IObytes.read())
    pic_hash = str(pic_hash)[2:-1]
    pyplot.close()
    return pic_hash