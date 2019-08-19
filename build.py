#!/usr/bin/env python
import os
import sys
import argparse

DATA_LOCATION = './domain-list-community/data'


def list_buildable():
    if not os.path.exists(DATA_LOCATION):
        sys.exit(f'Error: domain-list-community does not exists, try:\n',
                 f'    git submodule init\n',
                 f'    git submodule update')

    data_list = os.listdir(DATA_LOCATION)
    for index, data in enumerate(data_list, start=1):
        if (index % 4) == 0 or index == len(data_list):
            print(f'{data:20s}')
            continue
        print(f'{data:20s}', end='')


def build_target(target: str, server: str):
    lines = load(target)
    replace_include(lines)
    rules = build_dnsmasq(lines, server)
    for line in rules:
        print(line)


def load(target: str) -> list:
    if not os.path.exists(DATA_LOCATION + '/' + target):
        sys.exit(f'Error: domain-list {target} does not exists.')

    with open(DATA_LOCATION + '/' + target, 'r') as f:
        lines = list(f)

    return remove_comment(lines)


def remove_comment(lines: list) -> list:
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


def replace_include(lines: list):
    list_data = lines
    while 1:
        has_include = False
        for index, line in enumerate(list_data):
            if 'include:' in line:
                target = line[8:]
                del list_data[index]
                list_data.extend(load(target))
                has_include = True

        if not has_include:
            break


def build_dnsmasq(lines: list, server: str) -> list:
    rules = []
    for line in lines:
        if '@' in line:
            continue
        rules.append('server=/' + line + '/' + server)
    return rules


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='domain-list-community')
    parser.add_argument('target',
                        metavar='TARGET',
                        nargs='?',
                        default='cn',
                        help='target list to build (default: cn)')
    parser.add_argument('-l', '--list',
                        action='store_true',
                        help='list all buildable lists')
    parser.add_argument('-s', '--server',
                        metavar='SERVER',
                        nargs=1,
                        default=['223.5.5.5'],
                        help='public dns server (default: 223.5.5.5)')
    options = parser.parse_args()

    if options.list == True:
        list_buildable()
        sys.exit()

    build_target(options.target, options.server[0])
