class EdgebreakerDecompressor:
    def __init__(self):
        self.vertex_ids = None
        self.opposite_corner_ids = None
        self.last_triangle = None
        self.last_vertex = None
        self.clers = None
        self.clers_idx = None
        self.m = None
        self.u = None
        self.deltas = None
        self.delta_idx = None

    def decompress(self, clers: str, num_vertex_ids: int, deltas):
        # Table of vertex IDs for each corner
        self.vertex_ids = [0, 1, 2] + ([0] * num_vertex_ids)
        # Table of opposite corner IDs for corner
        self.opposite_corner_ids = [-1, -3, -1] + ([-3] * num_vertex_ids)
        # ID of the last triangle decompressed so far
        self.last_triangle = 0
        # ID of the last vertex encountered
        self.last_vertex = 2

        self.clers = clers
        self.clers_idx = 0

        self.decompress_connectivity(1)

        # TODO Vertices

    def decompress_connectivity(self, corner):
        # Loop builds triangle tree and zips it up
        while self.clers_idx < len(self.clers):
            self.last_triangle += 1
            # Attach new triangle, link opposite corners
            t3 = 3 * self.last_triangle
            self.opposite_corner_ids[corner] = t3
            self.opposite_corner_ids[t3] = corner
            # Enter vertex IDs for shared vertices
            self.vertex_ids[t3 + 1] = self.vertex_ids[self.prev_corner(corner)]
            self.vertex_ids[t3 + 2] = self.vertex_ids[self.next_corner(corner)]
            # Move corner to new triangle
            corner = self.next_corner(self.opposite_corner_ids[corner])

            # Select operation based on next symbol
            clers_symbol = self.clers[self.clers_idx]
            self.clers_idx += 1
            if clers_symbol == "C":
                # C: left edge is free, store ref to new vertex
                self.opposite_corner_ids[self.next_corner(corner)] = -1
                self.last_vertex += 1
                self.vertex_ids[t3] = self.last_vertex
            elif clers_symbol == "L":
                # L: orient free edge, try to zip once
                self.opposite_corner_ids[self.next_corner(corner)] = -2
                self.zip(self.next_corner(corner))
            elif clers_symbol == "R":
                # R: orient free edge, go left
                self.opposite_corner_ids[corner] = -2
                corner = self.next_corner(corner)
            elif clers_symbol == "S":
                # S: recursion going right, then go left
                self.decompress_connectivity(corner)
                corner = self.next_corner(corner)
            elif clers_symbol == "E":
                # E: zip, try more, pop
                self.opposite_corner_ids[corner] = -2
                self.opposite_corner_ids[self.next_corner(corner)] = -2
                self.zip(self.next_corner(corner))
                return

    # Tries to zip free edges opposite c
    def zip(self, c: int):
        # Search clockwise for free edge
        b = self.next_corner(c)
        while self.opposite_corner_ids[b] >= 0:
            b = self.next_corner(self.opposite_corner_ids[b])
        # Pop if no zip possible
        if self.opposite_corner_ids[b] != -1:
            return

        # Link opposite corners
        self.opposite_corner_ids[c] = b
        self.opposite_corner_ids[b] = c
        # Assign co-incident corners
        a = self.prev_corner(c)
        self.vertex_ids[self.prev_corner(a)] = self.vertex_ids[self.prev_corner(b)]

        while self.opposite_corner_ids[a] >= 0 and b != a:
            a = self.prev_corner(self.opposite_corner_ids[a])
            self.vertex_ids[self.prev_corner(a)] = self.vertex_ids[self.prev_corner(b)]

        # Find corner of next free edge on right
        c = self.prev_corner(c)
        while self.opposite_corner_ids[c] >= 0 and c != b:
            c = self.prev_corner(self.opposite_corner_ids[c])
        # Try to zip again
        if self.opposite_corner_ids[c] == -2:
            self.zip(c)

    def read(self):
        ...

    @staticmethod
    def next_corner(c):
        if c % 3 == 2:
            return c - 2
        return c + 1

    @staticmethod
    def prev_corner(c):
        return EdgebreakerDecompressor.next_corner(EdgebreakerDecompressor.next_corner(c))
