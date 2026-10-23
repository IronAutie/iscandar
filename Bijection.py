from Geometry   import Geometry
from Coordinate import Coordinate



class Bijection:
    """Conversions from paper: displacement <-> coordinate, exactly."""

    A = Geometry.ARITY

    def to_coordinate (self, displacement):
        plane, rem  = divmod (displacement, self.A * self.A)
        row, sector = divmod (rem, self.A)
        return Coordinate (sector=sector, row=row, plane=plane)

    def to_displacement (self, coordinate):
        return (coordinate.plane * self.A + coordinate.row)
                * self.A + coordinate.sector

