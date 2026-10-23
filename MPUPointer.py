"""MPUPointer -- a 32-bit virtual address for the MPU, as a bitfield.

DRAFT constructed at the author's request (2026-10-23) for his
desk-check; not yet part of the engine tree.

The word, in Motorola order (MSB first, the paper's parlance):

    Virtual   1 bit   top bit: the word belongs to the user's
                      application; it is not to be exposed directly
                      to the microprocessor for decoding
    Reserved  1 bit   not needed today; held against someday
    Start    15 bits  starting sector -- a name: 0..32767
    Count    15 bits  stored shifted: stored + 1 is the true count,
                      so counts run 1..32768, the whole cube is
                      representable, and a zero count is not

The format exists for fast deallocation: origin and length are both
in the word, so freeing is a sweep of the cube from the start over
the count, consulting nothing outside the word.

Decode order is a code switch, never a bit in the word: `order`
selects Motorola (the default) or Intel allocation, for benches
where this machine serves as memory to a microcontroller of the
other house. The Intel form declares the same fields from the low
end upward.

Every MPUPointer is BORN VIRTUAL (the author's consistency rule):
creation always raises the Virtual flag, the full cube included --
there is no `virtual` argument to `load`, because a newborn pointer
has no say in the matter. A word with the flag down can only enter
by adoption, MPUPointer(word), as an existing word read from
somewhere -- never by creation.
"""
from collections import namedtuple

import bitstruct

from Geometry   import Geometry
from Coordinate import Coordinate
from Bijection  import Bijection


MOTOROLA = 'motorola'
INTEL    = 'intel'

_FORMATS = {
    MOTOROLA: bitstruct.CompiledFormat('u1u1u15u15'),  # V, R, start, stored
    INTEL:    bitstruct.CompiledFormat('u15u15u1u1'),  # stored, start, R, V
}

Fields = namedtuple('Fields', ['virtual', 'reserved', 'start', 'count'])


class MPUPointer (int):
    """An int whose value is the packed 32-bit word.

    Born two ways, by named classmethods (never constructor tricks):
    `load` packs named fields into a word; `load_coordinate` packs
    from a Coordinate. `unload` is the way back out. Nothing is ever
    masked or truncated silently: a field outside its width is
    refused, because a reliable pointer cannot be built by quietly
    changing the caller's numbers.
    """

    MAX_WORD  = (1 << 32) - 1
    MAX_START = Geometry.ARITY ** 3 - 1     # 32767, the last name
    MAX_COUNT = Geometry.ARITY ** 3         # 32768, the whole cube

    def __new__ (cls, word=0):
        if not 0 <= word <= cls.MAX_WORD:
            raise ValueError(f"not a 32-bit word: {word!r}")
        return super().__new__(cls, word)

    @classmethod
    def load (cls, start, count, reserved=0, order=MOTOROLA):
        """Pack fields into a word, the Virtual flag raised.

        `count` is the true count. Creation always raises Virtual,
        so there is deliberately no way to ask load for a flag-down
        word.
        """
        virtual = 1
        if reserved not in (0, 1):
            raise ValueError(f"reserved must be 0 or 1, not {reserved!r}")
        if not 0 <= start <= cls.MAX_START:
            raise ValueError(f"start must be 0..{cls.MAX_START}, "
                             f"not {start!r}")
        if not 1 <= count <= cls.MAX_COUNT:
            raise ValueError(f"count must be 1..{cls.MAX_COUNT}, "
                             f"not {count!r}")
        stored = count - 1
        if order == INTEL:
            data = _FORMATS[INTEL].pack(stored, start, reserved, virtual)
        elif order == MOTOROLA:
            data = _FORMATS[MOTOROLA].pack(virtual, reserved, start, stored)
        else:
            raise ValueError(f"unknown order: {order!r}")
        return cls(int.from_bytes(data, 'big'))

    @classmethod
    def load_coordinate (cls, coordinate, count,
                         reserved=0, order=MOTOROLA):
        """Pack the block beginning at a Coordinate, flag raised."""
        return cls.load(coordinate.displacement, count,
                        reserved, order)

    def unload (self, order=MOTOROLA):
        """The word's fields, with the count back in true form."""
        data = int(self).to_bytes(4, 'big')
        if order == INTEL:
            stored, start, reserved, virtual = \
                _FORMATS[INTEL].unpack(data)
        elif order == MOTOROLA:
            virtual, reserved, start, stored = \
                _FORMATS[MOTOROLA].unpack(data)
        else:
            raise ValueError(f"unknown order: {order!r}")
        return Fields(virtual, reserved, start, stored + 1)

    # The fields at a glance, Motorola order.
    @property
    def virtual  (self): return self.unload().virtual

    @property
    def reserved (self): return self.unload().reserved

    @property
    def start    (self): return self.unload().start

    @property
    def count    (self): return self.unload().count

    def coordinate (self, order=MOTOROLA):
        """The start of this block, as a Coordinate."""
        return Bijection().to_coordinate(self.unload(order).start)

    def __repr__ (self):
        return f"MPUPointer(0x{int(self):08X})"
