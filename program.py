#!/usr/bin/env python3
import argparse
import json

from src import map_viewer

parser = argparse.ArgumentParser(description='My program description')
parser.add_argument('--input-path', type=str, help='Path of the local file containing the input data.')
parser.add_argument('--load-type', type=str, help='Type of the source of the image data.')
parser.add_argument('--rst-lst', type=str, help='List of rasters to create images from.')
parser.add_argument('--output-path', type=str, help='Path of the local file where the output data should be written.')
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
                'source': f'<img src="data:image/png;base64,{pic_hash}" />'
            }
            output_list.append(inner_dict)

    metadata['outputs'] = output_list

    with open('/mlpipeline-ui-metadata.json', 'w') as f:
        json.dump(metadata, f)