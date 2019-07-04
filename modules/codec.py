#!/usr/bin/python3
#
# codec.py
# - encode (lat,lng) to geohash.
# - decode geohash to (lat_range,lng_range).
# Geohash:
# https://en.wikipedia.org/wiki/Geohash
#

BASE32 = '0123456789bcdefghjkmnpqrstuvwxyz'
BASE32_TO_DECIMAL = dict((BASE32[i], i) for i in range(len(BASE32)))
def bits2char(bits):
    return BASE32[bits]
def char2bits(char):
    return BASE32_TO_DECIMAL[char]

# midpoint()
def midpoint(seq):
    assert(len(seq) == 2)
    return (seq[0] + seq[1]) / 2.0
# lower_half()
def lower_half(seq):
    assert(len(seq) == 2)
    return (seq[0], midpoint(seq))
# upper_half()
def upper_half(seq):
    assert(len(seq) == 2)
    return (midpoint(seq), seq[1])
# is_contained0()
def is_contained0(range0, range1):
    (min0, max0) = range0
    (min1, max1) = range1
    return (min1 <= min0 and max0 <= max1)

# is_contained1()
def is_contained1(lat_lng_range0, lat_lng_range1):
    ((minlat0, maxlat0), (minlng0, maxlng0)) = lat_lng_range0
    ((minlat1, maxlat1), (minlng1, maxlng1)) = lat_lng_range1
    return (
        minlat1 <= minlat0 and maxlat0 <= maxlat1
        and
        minlng1 <= minlng0 and maxlng0 <= maxlng1
    )

# encode()
def encode(lat, lng, length=11):
    chars = ''
    lat_lng_range = ((-90.0, +90.0), (-180.0, +180.0))
    for i_chars in range(length):
        (lat_range, lng_range) = lat_lng_range
        n_bits = 5
        bits = 0b00000
        for i_bits in range(n_bits):
            if (i_chars * n_bits + i_bits) % 2 == 0:
                # lng
                if lng < midpoint(lng_range):
                    #bits |=( 0b0000 >> i_bits)
                    lng_range = lower_half(lng_range)
                else:
                    bits |= (0b10000 >> i_bits)
                    lng_range = upper_half(lng_range)
            else:
                # lat
                if lat < midpoint(lat_range):
                    #bits |=( 0b0000 >> i_bits)
                    lat_range = lower_half(lat_range)
                else:
                    bits |= (0b10000 >> i_bits)
                    lat_range = upper_half(lat_range)
            lat_lng_range = (lat_range, lng_range)
        chars += bits2char(bits)
    return chars

# encode_to_longest_geohash()
def encode_to_longest_geohash(latlng0, latlng1, max_length=11):
    (lat0, lng0) = latlng0
    (lat1, lng1) = latlng1
    lat_lng_range = ((lat0, lat1), (lng0, lng1))
    lat_lng_range1 = ((-90.0, +90.0), (-180.0, +180.0))
    chars = ''
    for i_chars in range(max_length):
        (lat_range1, lng_range1) = lat_lng_range1
        n_bits = 5
        bits = 0b00000
        for i_bits in range(n_bits):
            if (i_chars * n_bits + i_bits) % 2 == 0:
                # lng
                if lng0 < midpoint(lng_range1):
                    #bits |=( 0b0000 >> i_bits)
                    lng_range1 = lower_half(lng_range1)
                else:
                    bits |= (0b10000 >> i_bits)
                    lng_range1 = upper_half(lng_range1)
            else:
                # lat
                if lat0 < midpoint(lat_range1):
                    #bits |=( 0b0000 >> i_bits)
                    lat_range1 = lower_half(lat_range1)
                else:
                    bits |= (0b10000 >> i_bits)
                    lat_range1 = upper_half(lat_range1)
            lat_lng_range1 = (lat_range1, lng_range1)
            if not is_contained1(lat_lng_range, lat_lng_range1):
                return chars
        chars += bits2char(bits)
    return chars

# encode_to_geohashes()
# TODO: CLEAN UP !!!
def encode_to_geohashes(latlng0, latlng1, length=11):
    (lat0, lng0) = latlng0
    (lat1, lng1) = latlng1
    chars = ''
    chars0 = [(
        '',
        ((lat0, lat1), (lng0, lng1)),
        ((-90.0, +90.0), (-180.0, +180.0)))]
    for i_chars in range(length):
        chars1 = []
        for (chars, range0, range1) in chars0:
            n_bits = 5
            bits0 = [(0b00000, range0, range1)]
            for i_bits in range(n_bits):
                bits1 = []
                for (bits, range00, range01) in bits0:
                    (lat_range0, lng_range0) = range00
                    (lat_range1, lng_range1) = range01
                    (lat0, _) = lat_range0
                    (_, lng0) = lng_range0
                    if (i_chars * n_bits + i_bits) % 2 == 0:
                        # lng
                        mid = midpoint(lng_range1)
                        lower = lower_half(lng_range1)
                        upper = upper_half(lng_range1)
                        if lng0 < mid:
                            if is_contained0(lng_range0, lower):
                                bits1.append((
                                    bits | (0b00000 >> i_bits),
                                    range00,
                                    (lat_range1, lower)))
                            else:
                                bits1.append((
                                    bits | (0b00000 >> i_bits),
                                    (lat_range0, (lng_range0[0], mid)),
                                    (lat_range1, lower)))
                                bits1.append((
                                    bits | (0b10000 >> i_bits),
                                    (lat_range0, (mid, lng_range0[1])),
                                    (lat_range1, upper)))
                        else:
                            if is_contained0(lng_range0, upper):
                                bits1.append((
                                    bits | (0b10000 >> i_bits),
                                    range00,
                                    (lat_range1, upper)))
                            else:
                                bits1.append((
                                    bits | (0b00000 >> i_bits),
                                    (lat_range0, (lng_range0[0], mid)),
                                    (lat_range1, lower)))
                                bits1.append((
                                    bits | (0b10000 >> i_bits),
                                    (lat_range0, (mid, lng_range0[1])),
                                    (lat_range1, upper)))
                    else:
                        # lat
                        mid = midpoint(lat_range1)
                        lower = lower_half(lat_range1)
                        upper = upper_half(lat_range1)
                        if lat0 < mid:
                            if is_contained0(lat_range0, lower):
                                bits1.append((
                                    bits | (0b00000 >> i_bits),
                                    range00,
                                    (lower, lng_range1)))
                            else:
                                bits1.append((
                                    bits | (0b00000 >> i_bits),
                                    ((lat_range0[0], mid), lng_range0),
                                    (lower, lng_range1)))
                                bits1.append((
                                    bits | (0b10000 >> i_bits),
                                    ((mid, lng_range0[1]), lng_range0),
                                    (upper, lng_range1)))
                        else:
                            if is_contained0(lat_range0, upper):
                                bits1.append((
                                    bits | (0b10000 >> i_bits),
                                    range00,
                                    (upper, lng_range1)))
                            else:
                                bits1.append((
                                    bits | (0b00000 >> i_bits),
                                    ((lat_range0[0], mid), lng_range0),
                                    (lower, lng_range1)))
                                bits1.append((
                                    bits | (0b10000 >> i_bits),
                                    ((mid, lng_range0[1]), lng_range0),
                                    (upper, lng_range1)))
                bits0 = bits1
            ##
            chars1 += [
                (chars + bits2char(bits), range00, range01)
                for (bits, range00, range01) in bits0
            ]
        chars0 = chars1
    return [chars for (chars, _, _) in chars0]

# decode()
def decode(geohash):
    lat_range = (-90.0, +90.0)
    lng_range = (-180.0, +180.0)
    for (i_chars, char) in enumerate(geohash):
        bits = char2bits(char)
        n_bits = 5
        for i_bits in range(n_bits):
            masked = bits & (0b10000 >> i_bits)
            if (i_chars * n_bits + i_bits) % 2 == 0:
                # lng
                if masked == 0:
                    lng_range = lower_half(lng_range)
                else:
                    lng_range = upper_half(lng_range)
            else:
                # lat
                if masked == 0:
                    lat_range = lower_half(lat_range)
                else:
                    lat_range = upper_half(lat_range)
    return (lat_range, lng_range)

# decode_to_range()
def decode_to_range(geohash):
    return decode(geohash)

# decode_to_point()
def decode_to_point(geohash):
    (lat_range, lng_range) =  decode(geohash)
    return (mid(lat_range), mid(lng_range))

if __name__ == "__main__":
    # test
    # - encode
    assert(encode(24.44944, 122.93361) == 'wsr7j6vs29z')
    assert(encode(20.42527, 136.06972) == 'x58u0q6cy63')
    assert(encode(24.28305, 153.98638) == 'xkmd0h97n8x')
    assert(encode(45.55722, 148.75222) == 'z21g0vqn1cq')
    assert(encode(35.68123, 139.76712) == 'xn76urx61zq')
    assert(encode(35.68123, 139.76712, 1) == 'x')
    assert(encode(35.68123, 139.76712, 10) == 'xn76urx61z')
    # - decode
    (lat_range, lng_range) = decode('xn76urx61zq')
    assert(lat_range[0] <= 35.68123 and 35.68123 < lat_range[1])
    assert(lng_range[0] <= 139.76712 and 139.76712 < lng_range[1])
    # - encode_to_geohashes
    #print(encode_to_geohashes((35.123, 135.123), (35.124, 135.124), 6))
    print('TEST: OK')
