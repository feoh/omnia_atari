import omnia_atari


def test_find_atari_files():
    test_files = [
        'DigDug.atr',
        'BogusRandomThing.png',
        'Mugwump.txt',
        'Moof.room',
        'Moof.rom',
        'ObviouslyNotAtari.exe',
        'this.xexis.moo'

    ]

    assert omnia_atari.find_atari_files(test_files) == [
        'DigDug.atr',
        'Moof.rom',
    ]


# THIS IS ENTIRELY WRONG. I guess I need to mock out all the internetarchive API objects? -CAP
#
# def test_get_item_files():
#     fake_item_files = [{'name': 'BP4kgXMeRjGVbPTkRfQ3g_thumb_a8b_archive.torrent',
#                         'source': 'metadata',
#                         'btih': '8ae6ff804ba1dbd76321fa92ced0533e972963a4',
#                         'mtime': '1613248077',
#                         'size': '2170',
#                         'md5': 'd35fca8e48203e68313468d918340a85',
#                         'crc32': 'bea74742',
#                         'sha1': 'a03e07fb1caed3ce34ee87c6d961207cdaf4db36',
#                         'format': 'Archive BitTorrent'},
#                        {'name': 'BP4kgXMeRjGVbPTkRfQ3g_thumb_a8b_files.xml',
#                         'source': 'original',
#                         'format': 'Metadata',
#                         'md5': '6ba5d3e8bf5a324c51f5202e664876bd'}]
#     assert omnia_atari.get_item_files(fake_item_files) == ['BP4kgXMeRjGVbPTkRfQ3g_thumb_a8b_archive.torrent',
#                                                            'BP4kgXMeRjGVbPTkRfQ3g_thumb_a8b_files.xml']
