#!/usr/bin/env python3
import argparse
import pickle

from src import raster_preprocessor
from src import sequence_separator

parser = argparse.ArgumentParser(description='My program description')
parser.add_argument('--input-path', type=str, help='Path of the local file containing the input data.')
parser.add_argument('--window-size', type=int, default=50, help='Window size.')
parser.add_argument('--nuts-level', type=int, default=0, help='Window size.')
parser.add_argument('--output-path', type=str, help='Path of the local file where the output data should be written.')
args = parser.parse_args()

if __name__ == "__main__":

    level = args.nuts_level

    rasters = {
        'pop': {
            'type': 'input',
            'fn': args.input_path + '/pop_rst.tif'
        },
        'dem': {
            'type': 'input',
            'fn': args.input_path + '/dem_aggr_rst.tif'
        },
        'ww': {
            'type': 'input',
            'fn': args.input_path + '/ww_aggr_rst.tif'
        },
        'nuts': {
            'type': 'output',
            'fn': args.input_path + f'/nuts_rst{level}.tif'
        },
        'area': {
            'type': 'aux',
            'fn': args.input_path + f'/nuts_area_rst{level}.tif'
        },
        'icb': {
            'type': 'aux',
            'fn': args.input_path + '/icb_rst.tif'
        }
    }
    window_size = args.window_size
    padding_size = args.window_size

    data_preprocessor = raster_preprocessor.DataPreprocessor(raster_config_dict = rasters, window_size = window_size)
    rasters = data_preprocessor.create_preprocessed_data()

    generator_sequences, output_value_dict = sequence_separator.create_separated_sequences(rasters, window_size, padding_size)

    pickle.dump(
        [rasters, generator_sequences, window_size, output_value_dict],
        open(args.output_path + "/features.p", "wb")
    )

    metadata = {
        'outputs' : [
            {
                'type': 'web-app',
                'storage': 'inline',
                'source': '<img src="data:image/gif;base64,xxxxxxxxxxxxx..." />'
            }
        ]
    }

    with open('/mlpipeline-ui-metadata.json', 'w') as f:
        json.dump(metadata, f)
