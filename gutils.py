#!/usr/bin/python3
#
# gutils.py: index script of geohash-utils.
#

import sys
import argparse
import modules.adjacent as adjacent
import modules.codec as codec
import modules.kml as kml

# cmd_encode()
# gutils.py encode 35.1234 139.1234
# gutils.py encode 35.1234 139.1234 35.5678 139.5678
def cmd_encode(argv):
    parser = argparse.ArgumentParser(description=
        'Encode a point of (lat1,lng1) to a geohash. ' +
        'If lat2 and lng2 are specified, this command encodes ' +
        'a region of [(lat0,lng0),(lat1,lng1)] to geohash(es).')
    parser.add_argument('lat1', type=float, help=
        'Latitude to be encoded. If lat2 is specified, ' +
        'lat1 indicates the latitude of the lower left point ' +
        'of the region to be encoded.')
    parser.add_argument('lng1', type=float, help=
        'Longitudetude to be encoded. If lng2 is specified, ' +
        'lng1 indicates the longitude of the lower left point ' +
        'of the region to be encoded.')
    parser.add_argument('lat2', type=float, nargs='?', help=
        'Latitude of the upper right point ' +
        'of the region to be encoded.')
    parser.add_argument('lng2', type=float, nargs='?', help=
        'Longitude of the lower left point ' +
        'of the region to be encoded.')
    parser.add_argument('--length', '-n', type=int, default=11, help=
        'The length of encoded geohash(es).')
    parser.add_argument('--max', type=int, help=
        'If specified with lat2 and lng2, this commands outputs ' +
        'the geohash with the longest length less than MAX.')
    args = parser.parse_args(argv)
    if args.lat2 is None or args.lng2 is None:
        print(codec.encode(args.lat1, args.lng1, args.length))
    elif args.max is not None:
        # TODO: raise ValueError ? over args.max
        print(codec.encode_to_longest_geohash(
            (args.lat1, args.lng1), (args.lat2, args.lng2), args.max))
    else:
        print((codec.encode_to_geohashes(
            (args.lat1, args.lng1), (args.lat2, args.lng2), args.length)))
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

# cmd_kml()
def cmd_kml(argv):
    parser = argparse.ArgumentParser(
        description='Outputs KML string to draw ' +
        'the specified geohash or coordinates.')
    parser.add_argument('geohashes', type=str, nargs='*', help='geohashes to draw')
    parser.add_argument('lat1', type=float, nargs='?', help='lat1')
    parser.add_argument('lng1', type=float, nargs='?', help='lng1')
    parser.add_argument('lat2', type=float, nargs='?', help='lat2')
    parser.add_argument('lng2', type=float, nargs='?', help='lng2')
    parser.add_argument('--coordinates', '-c', action='store_true')
    args = parser.parse_args(argv)
    if args.coordinates:
        print(kml.from_latlngs(
            (args.lat1, args.lng1), (args.lat2, args.lng2)))
    else:
        print(kml.from_geohash(args.geohashes))
    return

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
    elif cmd == 'decode':
        return cmd_decode(sys.argv[2:])
    elif cmd == 'kml':
        return cmd_kml(sys.argv[2:])
    elif cmd == 'adjacent':
        return cmd_adjacent(sys.argv[2:])
    elif cmd == 'help':
        if 2 < len(sys.argv):
            # TODO: cleanup
            cmd1 = sys.argv[2]
            if cmd1 == 'encode':
                return cmd_encode(['-h'])
            elif cmd1 == 'decode':
                return cmd_decode(['-h'])
            elif cmd1 == 'kml':
                return cmd_kml(['-h'])
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

if __name__ == '__main__':
    sys.exit(main())
