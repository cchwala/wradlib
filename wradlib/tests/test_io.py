import unittest
import wradlib.io as io
import wradlib.util as util
import numpy as np
import zlib
import tempfile
import os
import datetime


class IOTest(unittest.TestCase):
    # testing functions related to readDX
    def test_getTimestampFromFilename(self):
        pass

    def test_getDXTimestamp(self):
        pass

    def test_unpackDX(self):
        pass

    def test_readDX(self):
        pass

class RadolanTest(unittest.TestCase):

    def test_get_radolan_header_token(self):
        keylist = ['BY', 'VS', 'SW', 'PR', 'INT', 'GP',
                   'MS', 'LV', 'CS', 'MX', 'BG']
        head = io.get_radolan_header_token()
        for key in keylist:
            self.assertIsNone(head[key])
    def test_get_token_position(self):
        header = 'RW030950100000814BY1620130VS 3SW   2.13.1PR E-01INT  60GP 900x 900' \
                 'MS 58<boo,ros,emd,hnr,pro,ess,asd,neu,nhb,oft,tur,isn,fbg,mem>'

        test_head = io.get_radolan_header_token()
        test_head['PR'] = (43,48)
        test_head['GP'] = (57,66)
        test_head['INT'] = (51,55)
        test_head['SW'] = (32,41)
        test_head['VS'] = (28,30)
        test_head['MS'] = (68,None)
        test_head['BY'] = (19,26)

        head = io.get_token_position(header)
        self.assertDictEqual(head, test_head)

    def test_decode_radolan_runlength_line(self):
        testarr = [ 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
          0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
          0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
          0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
          0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
          0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
          0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 0.,
          0., 0., 0., 0., 0., 0., 0., 0., 0., 0., 9., 9., 9., 9., 9., 9., 9., 9.,
          9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9.,
          9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9.,
          9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9.,
          9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9.,
          9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9.,
          9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9.,
          9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9.,
          9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9.,
          9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9.,
          9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9.,
          9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9.,
          9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9.,
          9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9.,
          9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9.,
          9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9., 9.,
          9., 9., 9., 9., 9.]

        testline = '\x10\x98\xf9\xf9\xf9\xf9\xf9\xf9\xf9\xf9\xf9\xf9\xf9\xf9\xf9\xf9\xf9\xf9\xf9\xf9\xd9\n'
        arr = np.frombuffer(testline, np.uint8).astype(np.uint8)
        line = io.decode_radolan_runlength_line(arr)
        self.assertTrue(np.allclose(line,testarr))

    def test_read_radolan_runlength_line(self):
        testline = '\x10\x98\xf9\xf9\xf9\xf9\xf9\xf9\xf9\xf9\xf9\xf9\xf9\xf9\xf9\xf9\xf9\xf9\xf9\xf9\xd9\n'
        testarr = np.frombuffer(testline, np.uint8).astype(np.uint8)
        fid, temp_path = tempfile.mkstemp()
        file = open(temp_path, 'w')
        file.write(testline)
        file.close()
        file = open(temp_path, 'r')
        line = io.read_radolan_runlength_line(file)
        file.close()
        os.close(fid)
        os.remove(temp_path)
        self.assertTrue(np.allclose(line, testarr))
    def test_read_radolan_runlength_array(self):
        pass

    def test_parse_DWD_quant_composite_header(self):
        rx_header = 'RW030950100000814BY1620130VS 3SW   2.13.1PR E-01INT  60GP 900x 900' \
                 'MS 58<boo,ros,emd,hnr,pro,ess,asd,neu,nhb,oft,tur,isn,fbg,mem>'
        test_rx = {'maxrange': '150 km', 'radarlocations': ['boo', 'ros', 'emd', 'hnr', 'pro',
                                                            'ess', 'asd', 'neu', 'nhb', 'oft',
                                                            'tur', 'isn', 'fbg', 'mem'],
                   'nrow': 900, 'intervalseconds': 3600, 'precision': 0.1,
                   'datetime': datetime.datetime(2014, 8, 3, 9, 50), 'ncol': 900,
                   'radolanversion': '2.13.1', 'producttype': 'RW', 'radarid': '10000'}

        pg_header = 'PG030905100000814BY20042LV 6  1.0 19.0 28.0 37.0 46.0 55.0CS0MX 0MS 82' \
                    '<boo,ros,emd,hnr,pro,ess,asd,neu,nhb,oft,tur,isn,fbg,mem,czbrd> are used, ' \
                    'BG460460'
        test_pg = {'radarlocations': ['boo', 'ros', 'emd', 'hnr', 'pro', 'ess', 'asd', 'neu',
                                      'nhb', 'oft', 'tur', 'isn', 'fbg', 'mem', 'czbrd'],
                   'nrow': 460, 'level': [  1.,  19.,  28.,  37.,  46.,  55.],
                   'datetime': datetime.datetime(2014, 8, 3, 9, 5), 'ncol': 460,
                   'producttype': 'PG', 'radarid': '10000', 'nlevel': 6}

        rx = io.parse_DWD_quant_composite_header(rx_header)
        pg = io.parse_DWD_quant_composite_header(pg_header)

        for key, value in rx.iteritems():
            self.assertEqual(value, test_rx[key])
        for key, value in pg.iteritems():
            print(type(value))
            if type(value) == np.ndarray:
                self.assertTrue(np.allclose(value, test_pg[key]))
            else:
                self.assertEqual(value, test_pg[key])

    def test_read_RADOLAN_composite(self):
        pass

class RainbowTest(unittest.TestCase):
    def test_read_rainbow(self):
        pass

    def test_find_key(self):
        indict = {'A': {'AA': {'AAA': 0, 'X': 1},
                        'AB': {'ABA': 2, 'X': 3},
                        'AC': {'ACA': 4, 'X': 5}}}
        outdict = [{'X': 1, 'AAA': 0}, {'X': 5, 'ACA': 4}, {'ABA': 2, 'X': 3}]
        self.assertEqual(list(io.find_key('X', indict)), outdict)
        self.assertEqual(list(io.find_key('Y', indict)), [])

    def test_decompress(self):
        dstring = 'very special compressed string'
        cstring = zlib.compress(dstring)
        self.assertEqual(io.decompress(cstring), dstring)

    def test_get_RB_data_layout(self):
        self.assertEqual(io.get_RB_data_layout(8), (1, '>u1'))
        self.assertEqual(io.get_RB_data_layout(16), (2, '>u2'))
        self.assertEqual(io.get_RB_data_layout(32), (4, '>u4'))
        self.assertRaises(ValueError, lambda: io.get_RB_data_layout(128))

    def test_get_RB_data_attribute(self):
        xmltodict = util.import_optional('xmltodict')
        data = xmltodict.parse('<slicedata time="13:30:05" date="2013-04-26"> \
        #<rayinfo refid="startangle" blobid="0" rays="361" depth="16"/> \
        #<rawdata blobid="1" rays="361" type="dBuZ" bins="400" min="-31.5" max="95.5" depth="8"/> \
        #</slicedata>')
        data = list(io.find_key('@blobid', data))
        self.assertEqual(io.get_RB_data_attribute(data[0], 'blobid'), 0)
        self.assertEqual(io.get_RB_data_attribute(data[1], 'blobid'), 1)
        self.assertEqual(io.get_RB_data_attribute(data[0], 'rays'), 361)
        self.assertIsNone(io.get_RB_data_attribute(data[0], 'bins'))
        self.assertEqual(io.get_RB_data_attribute(data[1], 'rays'), 361)
        self.assertEqual(io.get_RB_data_attribute(data[1], 'bins'), 400)
        self.assertRaises(KeyError, lambda: io.get_RB_data_attribute(data[0], 'Nonsense'))
        self.assertEqual(io.get_RB_data_attribute(data[0], 'depth'), 16)

    def test_get_RB_blob_attribute(self):
        xmltodict = util.import_optional('xmltodict')
        xmldict = xmltodict.parse('<BLOB blobid="0" size="737" compression="qt"></BLOB>')
        self.assertEqual(io.get_RB_blob_attribute(xmldict, 'compression'), 'qt')
        self.assertEqual(io.get_RB_blob_attribute(xmldict, 'size'), '737')
        self.assertEqual(io.get_RB_blob_attribute(xmldict, 'blobid'), '0')
        self.assertRaises(KeyError, lambda: io.get_RB_blob_attribute(xmldict, 'Nonsense'))

    def test_map_RB_data(self):
        indata = '0123456789'
        outdata8 = np.array([48, 49, 50, 51, 52, 53, 54, 55, 56, 57], dtype=np.uint8)
        outdata16 = np.array([12337, 12851, 13365, 13879, 14393], dtype=np.uint16)
        outdata32 = np.array([808530483, 875902519], dtype=np.uint32)
        self.assertTrue(np.allclose(io.map_RB_data(indata, 8), outdata8))
        self.assertTrue(np.allclose(io.map_RB_data(indata, 16), outdata16))
        self.assertTrue(np.allclose(io.map_RB_data(indata, 32), outdata32))

    def test_get_RB_blob_data(self):
        datastring = '<BLOB blobid="0" size="737" compression="qt"></BLOB>'
        self.assertRaises(EOFError, lambda: io.get_RB_blob_data(datastring, 1))


if __name__ == '__main__':
    unittest.main()