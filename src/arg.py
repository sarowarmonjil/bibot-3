# coding: utf-8
import argparse


def parse_args(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('cmd', choices=['sync', 'show'])
    return parser.parse_args(args)


if __name__ == '__main__':
    print parse_args('sync'.split())
else:
    args = parse_args()
