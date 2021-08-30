#!/usr/bin/env python3
import argparse
import json

from src import map_viewer, vrt_viewer

parser = argparse.ArgumentParser(description='My program description')
parser.add_argument('--input-path', type=str, help='Path of the local file containing the input data.')
parser.add_argument('--load-type', type=str, help='Type of the source of the image data.')
parser.add_argument('--rst-lst', type=str, help='List of rasters to create images from.')
parser.add_argument('--resolution', type=int, help='Resolution of the output map.')
args = parser.parse_args()

if __name__ == "__main__":

    metadata = {}
    output_list = []

    if args.load_type == 'from_raster':
        rst_list = args.rst_lst.split(";")
        for raster_file in rst_list:
            rst_fn = args.input_path + raster_file
            pic_hash = map_viewer.get_base64_image(rst_fn, 1, False)
            inner_dict = {
                'type': 'web-app',
                'storage': 'inline',
                'source': f'<img src="data:image/png;base64,{pic_hash}" width="100%" />'
            }
            output_list.append(inner_dict)
    elif args.load_type == 'from_vrt':
        rst_list = args.rst_lst.split(";")
        for output_type in rst_list:
            pic_hash = vrt_viewer.get_base64_image_from_vrt(args.input_path, output_type, resolution = args.resolution)
            inner_dict = {
                'type': 'web-app',
                'storage': 'inline',
                'source': f'<img src="data:image/png;base64,{pic_hash}" width="100%" />'
            }
            output_list.append(inner_dict)

    metadata['outputs'] = output_list

    with open('/mlpipeline-ui-metadata.json', 'w') as f:
        json.dump(metadata, f)