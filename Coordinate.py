from Row   import Row
from Plane import Plane



class Coordinate:
    """A lattice coordinate: one sector, in one row, in one plane."""

    def __init__(self, sector=0, row=0, plane=0):
        self.sector = sector
        self.row    = row
        self.plane  = plane

    @property
    def displacement(self):
        """This coordinate as a scalar address (Axiom IV, Equation 6)."""
        return (self.sector
                + self.row   * Row.SECTORS_PER_ROW
                + self.plane * Plane.SECTORS_PER_PLANE)

    def __eq__(self, other):
        if not isinstance(other, Coordinate):
            return NotImplemented
        return (self.sector, self.row, self.plane) == \
               (other.sector, other.row, other.plane)

    def __hash__(self):
        return hash((self.sector, self.row, self.plane))

    def __repr__(self):
        return f"Coordinate(sector={self.sector}, row={self.row}, plane={self.plane})"