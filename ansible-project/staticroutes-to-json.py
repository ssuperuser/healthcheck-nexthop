#!/usr/bin/env python3

import os
import yaml

print ('NOTE:');
#print('converts static routes from txt file to json format')
print ('remove the leading spaces in staticroutes.txt file, for each route ')


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROUT_TXT = os.path.join(BASE_DIR, 'staticroutes.txt')
STATIC_ROUT_YAML = os.path.join(BASE_DIR, 'staticroutes.yml')


def get_routes():
    routes = []
    with open(STATIC_ROUT_TXT) as fh:
        for line in fh.readlines():
            word_list = [w.strip() for w in line.split(' ')]
            if str(word_list[5]).startswith('null'):
                word_list[5]= '';
            if str(word_list[6]).startswith('null'):
                word_list[5]= '';
            word_list[6]=str(word_list[6]).replace("\n",'')
            routes.append({
                'dest': str(word_list[2]),
                'next_hop': str(word_list[3]),
                'vrf': str(word_list[4]),
                'next_hop_vrf': str(word_list[5]),
                'check_healthy': str(word_list[6])
            })
    return routes


def get_default_routes():
    routes = None
    default_routes = {
        'default_route': '',
        'default_route2': ''
    }
    try:
        with open(STATIC_ROUT_YAML, 'r') as fh:
            routes = yaml.load(fh, Loader=yaml.SafeLoader)
    except FileNotFoundError:
        pass
    if routes is not None:
        for k in default_routes.keys():
            try:
                v = routes.get(k)
            except AttributeError:
                v = None
            if v is not None:
                default_routes[k] = v
                continue
            for e in routes:
                if isinstance(e, str) and e.startswith("{}:".format(k)):
                    default_routes[k] = e.replace("{}:".format(k), '').strip()
                    break
    return default_routes


def main():
    data = get_default_routes()
    data['routes'] = get_routes()
    with open(STATIC_ROUT_YAML, 'w') as fh:
        yaml.dump(data, fh,  indent=4, sort_keys=True)


if __name__ == '__main__':
    main()
