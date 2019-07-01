#!/usr/bin/python3
#
# gutils.py: index script of geohash-utils.
#

import sys
import argparse
import modules.codec as codec
import modules.adjacent as adjacent

# cmd_encode()
# gutils.py encode 35.1234 139.1234
def cmd_encode(argv):
    parser = argparse.ArgumentParser(
        description='Encode the point consisting of (lat,lng) to a geohash.')
    parser.add_argument('lat', type=float, help='Latitude to be encoded.')
    parser.add_argument('lng', type=float, help='Longitude to be encoded.')
    parser.add_argument('--length', type=int, default=11)
    args = parser.parse_args(argv)
    print(codec.encode(args.lat, args.lng, args.length))
    return 0

# cmd_encode_range()
# gutils.py encode 35.1234 139.1234 35.5678 139.5678
def cmd_encode_range(argv):
    parser = argparse.ArgumentParser(description=
        'Encode the range consisting of ' +
        '[(lat0,lng0),(lat1,lng1)] to geohash(es).')
    parser.add_argument('lat0', type=float,
        help='Latitude of the lower left point of the range to be encoded.')
    parser.add_argument('lng0', type=float,
        help='Longitude of the lower left point of the range to be encoded.')
    parser.add_argument('lat1', type=float,
        help='Latitude of the upper right point of the range to be encoded.')
    parser.add_argument('lng1', type=float,
        help='Longitude of the upper right point of the range to be encoded.')
    parser.add_argument('--max', type=int, default=11, help='TODO')
    parser.add_argument('--length', type=int, help=
        'If specified, this command prints the geohash(es) ' +
        'with LENGTH characters.')
    args = parser.parse_args(argv)
    if args.length is not None:
        # TODO: implement
        pass
    else:
        print(codec.encode_to_longest_geohash(
            ((args.lat0, args.lng0), (args.lat1, args.lng1)), args.max))
    return 0

# cmd_decode()
def cmd_decode(argv):
    parser = argparse.ArgumentParser(
        description='Decode geohash to lat_range, lng_range.')
    parser.add_argument('geohash', type=str, help='geohash')
    parser.add_argument('-c', '--center', action='store_true')
    args = parser.parse_args(argv)
    if args.center:
        print(codec.decode_to_point(args.geohash))
    else:
        print(codec.decode_to_range(args.geohash))
    return 0

# cmd_adjacent()
def cmd_adjacent(argv):
    parser = argparse.ArgumentParser(
        description='Get adjacent geohashes.')
    parser.add_argument('geohash', type=str, help='geohash')
    # TODO: direction options.
    args = parser.parse_args(argv)
    print(adjacent.get_adjacent_geohashes(args.geohash))
    return 0

# main()
def main():
    parser = argparse.ArgumentParser(
        description='Geohash Utilities.',
        usage='gutils.py [-h] <command> [<args>]')
    # TODO: add available command list.
    parser.add_argument('command', help='command to run')
    args = parser.parse_args(sys.argv[1:2])
    cmd = args.command
    if cmd == 'encode':
        return cmd_encode(sys.argv[2:])
    elif cmd == 'encode_range':
        return cmd_encode_range(sys.argv[2:])
    elif cmd == 'decode':
        return cmd_decode(sys.argv[2:])
    elif cmd == 'adjacent':
        return cmd_adjacent(sys.argv[2:])
    elif cmd == 'help':
        if 2 < len(sys.argv):
            # TODO: cleanup
            cmd1 = sys.argv[2]
            if cmd1 == 'encode':
                return cmd_encode(['-h'])
            elif cmd1 == 'encode_range':
                return cmd_encode_range(['-h'])
            elif cmd1 == 'decode':
                return cmd_decode(['-h'])
            elif cmd1 == 'adjacent':
                return cmd_adjacent(['-h'])
            else:
                print('main.py: Unrecognized command \'%s\'.' % (cmd))
                parser.print_help()
        else:
            parser.print_help()
            return 0
    else:
        print('main.py: Unrecognized command \'%s\'.' % (cmd))
        parser.print_help()
    return -1

if __name__ == "__main__":
    sys.exit(main())
