import base64
import io

from matplotlib import pyplot
import numpy as np
import rasterio


def read_raster_file(input_fn, band = 1):
    with rasterio.open(input_fn) as src:
        return src.read(band)
    

def plot_raster_layer(input_fn, band = 1, from_logits = True):
    pyplot.figure(figsize = (10,10))
    data = read_raster_file(input_fn, band)
    if from_logits:
        data = np.exp(data)
    pyplot.imshow(data, cmap='viridis')
    pyplot.show()

    
def plot_histogram(input_fn, band = 1, from_logits = True):
    pyplot.figure(figsize = (10,10))
    data = read_raster_file(input_fn, band)
    pyplot.hist(np.rint(data), bins='auto') 
    pyplot.show()


def get_base64_image(input_fn, band = 1, from_logits = True):
    pyplot.figure(figsize = (10,10))
    data = read_raster_file(input_fn, band)
    pyplot.imshow(data, cmap='viridis')

    pic_IObytes = io.BytesIO()
    pyplot.savefig(pic_IObytes,  format='png')
    pic_IObytes.seek(0)
    pic_hash = base64.b64encode(pic_IObytes.read())
    # We need to remove the quotation and b character
    pic_hash = pic_hash[2:-1]
    return pic_hash
