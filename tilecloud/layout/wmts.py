from tilecloud import TileLayout


class WMTSTileLayout(TileLayout):

    def __init__(self, url='', layer=None, style=None, format=None, 
                 tile_matrix_set=None, tile_matrix=None,
                 dimensions=(), request_encoding='KVP'):
        self.url = url
        self.layer = layer
        self.style = style
        self.format = format
        self.tile_matrix_set = tile_matrix_set
        self.tile_matrix = tile_matrix
        self.dimensions = dimensions
        self.request_encoding = request_encoding

    def filename(self, tilecoord):
        # Careful the order is important for the REST request encoding
        query = []
        if self.request_encoding == 'KVP':
            query.extend([
                    ('Service', 'WMTS'),
                    ('Request', 'GetTile'),
                    ('Format', self.format),
            ])

        query.extend([
                ('Version', '1.0.0'),
                ('Layer', self.layer),
                ('Style', self.style),
        ])

        query.extend(self.dimensions);

        query.extend([
                ('TileMatrixSet', self.tile_matrix_set),
                ('TileMatrix', str(self.tile_matrix(tilecoord.z) 
                        if self.tile_matrix is not None else tilecoord.z)),
                ('TileRow', str(tilecoord.y)),
                ('TileCol', str(tilecoord.x))
        ])
        if self.request_encoding == 'KVP':
            return self.url + '?' + '&'.join('='.join(p) for p in query)
        else:
            return self.url + '/' + '/'.join(p[1] for p in query) + self.format
