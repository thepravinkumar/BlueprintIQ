import math

class Calculations:
    @staticmethod
    def calculate_perimeter(entities):
        """Calculates total perimeter of DXF elements."""
        perimeter = 0.0
        for entity in entities:
            if entity.dxftype() == "LINE":
                start, end = entity.dxf.start, entity.dxf.end
                perimeter += math.dist(start, end)
            elif entity.dxftype() == "LWPOLYLINE":
                points = list(entity.vertices())
                for i in range(len(points) - 1):
                    perimeter += math.dist(points[i], points[i + 1])
        return perimeter

    @staticmethod
    def calculate_centerline_length(entities):
        """Computes centerline length (midpoint method)."""
        total_length = 0.0
        for entity in entities:
            if entity.dxftype() == "LINE":
                start, end = entity.dxf.start, entity.dxf.end
                midpoint = [(s + e) / 2 for s, e in zip(start, end)]
                total_length += math.dist(start, midpoint) * 2
        return total_length
