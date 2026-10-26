"""Acceptance suites for the Iscandar engine.

These are the desk-checks Muse ran against every push during the
engine's construction (October 2026), written down as a permanent
suite at the author's direction: the verification is part of the
work, so it belongs in the repo beside the code it verifies.

Run from the repository root:

    python -m unittest test_engine -v

The MPUPointer suites need the bitstruct package; without it they
skip, and everything else still runs.
"""
import unittest

from Geometry   import Geometry
from Row        import Row
from Plane      import Plane
from Cube       import Cube
from Modes      import Modes
from allocator  import Engine
from Coordinate import Coordinate
from Bijection  import Bijection

try:
    from MPUPointer import MPUPointer, MOTOROLA, INTEL
    HAVE_BITSTRUCT = True
except ImportError:
    HAVE_BITSTRUCT = False


A = Geometry.ARITY                 # 32
SECTORS = A ** 3                    # 32768, a cube's worth


class GeometrySuites (unittest.TestCase):

    def test_constants (self):
        self.assertEqual(Geometry.ARITY, 32)
        self.assertEqual(Geometry.DIMENSIONS, 3)
        self.assertEqual(Row.SECTORS_PER_ROW, 32)
        self.assertEqual(Plane.SECTORS_PER_PLANE, 1024)
        self.assertEqual(Cube.SECTORS_PER_CUBE, 32768)

    def test_row_masks_to_width (self):
        self.assertEqual(Row(0x1FFFFFFFF), 0xFFFFFFFF)
        self.assertEqual(Row(0), 0)

    def test_plane_view_reads_words_and_writes_through (self):
        # Plane is a view over the flat cube store (its words
        # array), not a sparse container: every row index reads
        # the word beneath it, and a write lands in the store.
        # (Updated 2026-10-26: the original form of this test
        # constructed Plane() bare and deleted a row, against
        # the pre-view Plane.)
        words = [0] * SECTORS
        plane = Plane(words)
        self.assertEqual(len(plane), 32)
        self.assertTrue(all(plane[i] == 0 for i in range(32)))
        plane[7] = Row(0x0F)
        self.assertEqual(words[7], 0x0F)          # writes through
        self.assertEqual(plane[7], 0x0F)
        second = Plane(words, plane=1)            # offset view
        self.assertEqual(second[0], 0)            # words[32], untouched

    def test_cube_nested_write_persists (self):
        cube = Cube()
        cube[7][1] = Row(0x0F)
        self.assertEqual(cube[7][1], 0x0F)


class ModesSuites (unittest.TestCase):
    """The decision table: one entry per legal request size.

    32769 entries, keys 0..32768 -- the keys are request sizes
    (counts), not addresses. Nothing owns 0; Huge runs through
    32767; CubeCheck owns 32768 exactly, the whole-cube request
    (the author's settled ranges: 32768 is not an address, it is
    the count of the whole cube, and the gatekeeper tier checks
    it). Updated 2026-10-26: the original form of this suite put
    CubeCheck at 32767 with 32768 keys, before the ranges were
    settled in their final form.
    """

    EXPECTED = {0: 'Nothing', 1: 'Nano', 8: 'Nano', 9: 'Tiny',
                32: 'Tiny', 33: 'Small', 64: 'Small', 65: 'Large',
                1024: 'Large', 1025: 'Huge', 32766: 'Huge',
                32767: 'Huge', 32768: 'CubeCheck'}

    def test_table_size_and_keys (self):
        modes = Modes()
        self.assertEqual(len(modes), SECTORS + 1)
        self.assertEqual(set(modes), set(range(SECTORS + 1)))

    def test_boundary_keys (self):
        modes = Modes()
        for key, name in self.EXPECTED.items():
            with self.subTest(key=key):
                self.assertEqual(type(modes[key]).__name__, name)

    def test_no_key_left_on_error_underlay (self):
        modes = Modes()
        self.assertNotIn('Error',
                         {type(v).__name__ for v in modes.values()})

    def test_dispatch_executes_everywhere (self):
        # The finished dispatch contract (updated 2026-10-26;
        # the original form called every mode bare with one
        # argument, an interface from when Large and Huge were
        # stubs -- Mode.__call__ now carries the bullet
        # signature and its own docstring says it should never
        # be called bare). Dispatch is: the table selects the
        # mode, and the engine executes the mode's search.
        # The searches that are pure Python execute here on an
        # empty cube; the gear modes (Nano, Tiny, Small) search
        # through the C gears, so this suite asserts their
        # selection and entry point, and their execution is
        # covered by the harness runs and the CIC DLL build.
        from Status import Status
        modes = Modes()
        planes = [0] * 32
        rows = [0] * 1024
        words = [0] * 1024
        # Nothing: request 0 places nothing, silently.
        self.assertIsNone(modes[0].search(0, planes, rows, words))
        # The Python-search modes convict at the origin of an
        # empty cube, in the uniform gear-tuple shape.
        for request in (65, 1025, 32768):
            with self.subTest(request=request):
                result = modes[request].search(
                    request, planes, rows, words, 0)
                self.assertEqual(result,
                                 (Status.GEAR_SUCCESS, 0, 0, 0))
        # The Error sentinel answers in the same shape, as FAIL.
        self.assertEqual(modes.error.search(1, planes, rows,
                                            words),
                         (Status.FAIL, 0, 0, 0))
        # The gear modes are selected and carry the standard
        # search entry point.
        for request in (1, 9, 33):
            with self.subTest(request=request):
                self.assertTrue(callable(modes[request].search))
        # Out-of-domain requests fall back to Nothing, and
        # Nothing answers a bare call with an int.
        for request in (40000, -1):
            with self.subTest(request=request):
                self.assertIsInstance(modes(request), int)
        self.assertEqual(type(modes.get(40000, modes.nothing)).__name__,
                         'Nothing')

    def test_engine_constructs_and_dispatches (self):
        engine = Engine()
        self.assertEqual(engine.count_overall, 0)
        self.assertEqual(len(engine.count_planes), 32)
        self.assertEqual(len(engine.count_rows), 1024)
        self.assertEqual(type(engine.modes[5]).__name__, 'Nano')


class BijectionSuites (unittest.TestCase):
    """Axiom IV: coordinate <-> displacement, exactly, exhaustively."""

    def test_displacement_round_trip_exhaustive (self):
        b = Bijection()
        for s in range(SECTORS):
            self.assertEqual(b.to_displacement(b.to_coordinate(s)), s)

    def test_coordinate_round_trip_exhaustive (self):
        b = Bijection()
        for p in range(A):
            for r in range(A):
                for s in range(A):
                    c = Coordinate(s, r, p)
                    self.assertEqual(b.to_coordinate(b.to_displacement(c)),
                                     c)

    def test_coordinate_displacement_agrees_exhaustive (self):
        # Two independent implementations of Equation 6 cross-check:
        # Coordinate.displacement (strides) vs Bijection (Horner).
        b = Bijection()
        for p in range(A):
            for r in range(A):
                for s in range(A):
                    c = Coordinate(s, r, p)
                    self.assertEqual(c.displacement, b.to_displacement(c))

    def test_origin_and_far_corner (self):
        self.assertEqual(Coordinate(0, 0, 0).displacement, 0)
        self.assertEqual(Coordinate(31, 31, 31).displacement, 32767)
        self.assertEqual(Bijection().to_coordinate(1093),
                         Coordinate(5, 2, 1))

    def test_displacements_stay_in_domain (self):
        for p in (0, 31):
            for r in (0, 31):
                for s in (0, 31):
                    d = Coordinate(s, r, p).displacement
                    self.assertTrue(0 <= d <= 32767)


@unittest.skipUnless(HAVE_BITSTRUCT, "bitstruct not installed")
class MPUPointerSuites (unittest.TestCase):
    """The bitfield: V(1) Reserved(1) Start(15) Count(15, shifted).

    Every created pointer is born virtual. Hand arithmetic is the
    independent oracle:
        Motorola: virtual<<31 | reserved<<30 | start<<15 | (count-1)
        Intel:    virtual | reserved<<1 | start<<2 | (count-1)<<17
    """

    COUNTS = [1, 2, 3, 7, 8, 255, 1024, 32767, 32768]
    STARTS = [0, 1, 1093, 32766, 32767]

    @staticmethod
    def manual_moto (start, count, reserved=0):
        return (1 << 31) | (reserved << 30) | (start << 15) | (count - 1)

    @staticmethod
    def manual_intel (start, count, reserved=0):
        return 1 | (reserved << 1) | (start << 2) | ((count - 1) << 17)

    def test_worked_example (self):
        p = MPUPointer.load(1093, 7)
        self.assertEqual(int(p), 0x82228006)
        self.assertEqual(p.unload(), (1, 0, 1093, 7))
        self.assertEqual(p.coordinate(), Coordinate(5, 2, 1))

    def test_whole_cube_both_orders (self):
        self.assertEqual(int(MPUPointer.load(0, 32768)), 0x80007FFF)
        self.assertEqual(int(MPUPointer.load(0, 32768, order=INTEL)),
                         0xFFFE0001)

    def test_all_starts_representative_counts_both_orders (self):
        for order, manual in [(MOTOROLA, self.manual_moto),
                              (INTEL, self.manual_intel)]:
            for count in self.COUNTS:
                for start in range(SECTORS):
                    p = MPUPointer.load(start, count, order=order)
                    self.assertEqual(int(p), manual(start, count))
                    self.assertEqual(p.unload(order),
                                     (1, 0, start, count))

    def test_all_counts_representative_starts_both_orders (self):
        for order, manual in [(MOTOROLA, self.manual_moto),
                              (INTEL, self.manual_intel)]:
            for start in self.STARTS:
                for count in range(1, SECTORS + 1):
                    p = MPUPointer.load(start, count, order=order)
                    self.assertEqual(int(p), manual(start, count))
                    self.assertEqual(p.unload(order).count, count)

    def test_born_virtual_always (self):
        for order in (MOTOROLA, INTEL):
            for count in self.COUNTS:
                p = MPUPointer.load(12345, count, order=order)
                self.assertEqual(p.unload(order).virtual, 1)

    def test_coordinate_overlay_exhaustive (self):
        for p in range(A):
            for r in range(A):
                for s in range(A):
                    c = Coordinate(s, r, p)
                    ptr = MPUPointer.load_coordinate(c, 1)
                    self.assertEqual(ptr.coordinate(), c)
                    self.assertEqual(ptr.virtual, 1)

    def test_adopted_flag_down_word_reads_honestly (self):
        adopted = MPUPointer(0x00007FFF)
        self.assertEqual(adopted.virtual, 0)
        self.assertEqual(adopted.unload(), (0, 0, 0, 32768))

    def test_refusals (self):
        bad = [lambda: MPUPointer.load(0, 0),            # count 0
               lambda: MPUPointer.load(0, 32769),        # count too big
               lambda: MPUPointer.load(32768, 1),        # 32768 is
                                                         # not an address
               lambda: MPUPointer.load(-1, 1),
               lambda: MPUPointer.load(0, 1, reserved=2),
               lambda: MPUPointer.load(0, 1, order='z80'),
               lambda: MPUPointer(1 << 32),
               lambda: MPUPointer(-1),
               lambda: MPUPointer.load(0, 1).unload('z80')]
        for call in bad:
            with self.subTest(call=call):
                with self.assertRaises(ValueError):
                    call()


if __name__ == '__main__':
    unittest.main()
