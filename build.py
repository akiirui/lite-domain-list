#!/usr/bin/env python
import os
import sys
import argparse

DATA_LOCATION = './domain-list-community/data'
DNSMASQ_LOCATION = './dnsmasq/'


def list_buildable():
    if not os.path.exists(DATA_LOCATION):
        sys.exit(f'Error: domain-list-community does not exists, try:\n',
                 f'    git submodule init\n',
                 f'    git submodule update --recursive --remote')

    data_list = os.listdir(DATA_LOCATION)
    for index, data in enumerate(data_list, start=1):
        print(f'{data:20s}', end='')
        if (index % 4) == 0 or index == len(data_list):
            print()


def build(target: str, server: str):
    lines = load(target)
    data = replace_include(lines)
    build_dnsmasq(data, server, target)
    print(f'Info: Build Successful')


def load(target: str) -> list:
    if not os.path.exists(DATA_LOCATION + '/' + target):
        sys.exit(f'Error: domain-list {target} does not exists.')

    with open(DATA_LOCATION + '/' + target, 'r') as f:
        lines = list(f)

    data = []

    for line in lines:
        index = line.find('#')
        if index != -1:
            line = line[:index]
        line = line.strip()
        if len(line) == 0:
            continue
        data.append(line)

    return data


def replace_include(lines: list) -> list:
    while True:
        tmp_data = []
        has_include = False
        for line in lines:
            if 'include:' in line:
                has_include = True
                target = line[8:]
                tmp_data.extend(load(target))
            else:
                tmp_data.append(line)

        lines = tmp_data

        if not has_include:
            return lines


def build_dnsmasq(lines: list, server: str, target: str):
    DNSMASQ_FILENAME = target + '.conf'
    rules = []
    for line in lines:
        if '@' in line:
            continue
        if ':' in line:
            continue
        rules.append('server=/' + line + '/' + server + '\n')

    with open(DNSMASQ_LOCATION + DNSMASQ_FILENAME, 'w') as f:
        f.writelines(rules)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='domain-list-community')
    parser.add_argument('target',
                        metavar='TARGET',
                        nargs='?',
                        default='cn',
                        help='target domain-list to build (default: cn)')
    parser.add_argument('-l', '--list',
                        action='store_true',
                        help='list all buildable domain-lists')
    parser.add_argument('-s', '--server',
                        metavar='SERVER',
                        nargs=1,
                        default=['223.5.5.5'],
                        help='public dns server (default: 223.5.5.5)')
    options = parser.parse_args()

    if options.list == True:
        list_buildable()
        sys.exit()

    build(options.target, options.server[0])
