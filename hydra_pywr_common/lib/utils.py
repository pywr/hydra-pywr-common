"""
    Type-related utilities
"""

import re

"""
  Enforces canonical name format on references.
"""
def parse_reference_key(key, strtok=':'):
    name, attr = key.split(strtok)
    name_pattern = r"^__[a-zA-Z0-9_ \.\-\(\)]+__$"
    if not re.search(name_pattern, name):
        raise ValueError(f"Invalid reference {name}")

    return name.strip('_'), attr

"""
  Combines integrated model inputs into a single file for import into hwi
"""
def combine_integrated_model_inputs(configfile, waterfile, energyfile, inline_params=True):
    import json
    with open(configfile, 'r') as fp:
        config = json.load(fp)

    with open(waterfile, 'r') as fp:
        water = json.load(fp)

    with open(energyfile, 'r') as fp:
        energy = json.load(fp)

    if inline_params:
        inline_dataframe_parameters(water)

    output = { "config" : config,
               "water_network": water,
               "energy_network": energy
             }

    return output


def inline_dataframe_parameters(network):
    nodes = network["nodes"]
    for node in nodes:
        for attr, val in node.items():
            if not isinstance(val, dict):
                continue

            if "url" in val:
                src = val["url"]
                column = val["column"]
                ptype = val["type"]
                index_col = val["index_col"]

                if src.endswith(".gz"):
                    dataframe = gzcsv_to_dataframe(src, index_col, column)
                else:
                    dataframe = csv_to_dataframe(src, index_col, column)

                node[attr] = dataframe


def csv_to_dataframe(filename, index_col, data_col):
    import csv
    dataframe = {"type": "dataframeparameter",
                 "data": {}
                }
    with open(filename, 'r') as fp:
        headline = fp.readline()
        headers = headline.strip().split(',')
        index_idx = headers.index(index_col)
        data_idx = headers.index(data_col)
        series = {}
        dataframe["data"][column] = series

        for row in csv.reader(fp):
            idx = row[index_idx]
            datum = row[data_idx]
            series[idx] = float(datum)

    return dataframe


def gzcsv_to_dataframe(filename, index_col, data_col):
    import gzip
    dataframe = {"type": "dataframeparameter",
                 "data": {}
                }
    with gzip.open(filename, 'rt') as fp:
        headline = fp.readline()
        headers = headline.strip().split(',')

        index_idx = headers.index(index_col)
        data_idx = headers.index(data_col)
        series = {}
        dataframe["data"][data_col] = series

        for row in fp:
            row = row.strip()
            row = row.split(',')
            idx = row[index_idx]
            datum = row[data_idx]
            series[idx] = float(datum)

    return dataframe
