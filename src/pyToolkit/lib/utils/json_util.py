import json


def read_json_from_file(json_fpath):
    with open(json_fpath) as f:
        data = json.load(f)
    return data


def write_json_to_file(json_obj, json_fpath, if_pretty):
    if if_pretty:
        with open(json_fpath, 'w') as f:
            json.dump(json_obj, f, indent=4, sort_keys=True)
    else:
        with open(json_fpath, 'w') as f:
            json.dump(json_obj, f)
