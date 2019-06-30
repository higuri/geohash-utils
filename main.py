#!/usr/bin/python3
#
# geohash-utils/main.py
#

import sys
import argparse
import modules.codec as codec
import modules.adjacent as adjacent

# cmd_encode()
def cmd_encode(argv):
    parser = argparse.ArgumentParser(
        description='Encode lat, lng to geohash.')
    parser.add_argument('lat', type=float, help='latitude')
    parser.add_argument('lng', type=float, help='longitude')
    args = parser.parse_args(argv)
    print(codec.encode(args.lat, args.lng))
    return

# cmd_decode()
def cmd_decode(argv):
    parser = argparse.ArgumentParser(
        description='Decode geohash to lat_range, lng_range.')
    parser.add_argument('geohash', type=str, help='geohash')
    parser.add_argument('--center', action='store_true')
    args = parser.parse_args(argv)
    if args.center:
        print(codec.decode_to_point(args.geohash))
    else:
        print(codec.decode_to_range(args.geohash))
    return

# cmd_adjacent()
def cmd_adjacent(argv):
    parser = argparse.ArgumentParser(
        description='Get adjacent geohashes.')
    parser.add_argument('geohash', type=str, help='geohash')
    # TODO: direction options.
    args = parser.parse_args(argv)
    print(adjacent.get_adjacent_geohashes(args.geohash))
    return

# main()
def main():
    parser = argparse.ArgumentParser(
        description='Geohash Utilities.',
        usage='main.py [-h] <command> [<args>]')
    parser.add_argument('command', help='command to run')
    args = parser.parse_args(sys.argv[1:2])
    cmd = args.command
    if cmd == 'encode':
        cmd_encode(sys.argv[2:])
    elif cmd == 'decode':
        cmd_decode(sys.argv[2:])
    elif cmd == 'adjacent':
        cmd_adjacent(sys.argv[2:])
    else:
        print('main.py: Unrecognized command \'%s\'.' % (cmd))
        parser.print_help()
        return -1
    return

if __name__ == "__main__":
    sys.exit(main())
