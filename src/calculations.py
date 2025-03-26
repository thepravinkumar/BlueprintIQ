import math

class Calculations:
    @staticmethod
    def calculate_dimensions(entities, wall_thickness=0.2):
        """Computes internal & external dimensions from DXF entities."""
        min_x, min_y = float("inf"), float("inf")
        max_x, max_y = float("-inf"), float("-inf")

        for entity in entities:
            if entity.dxftype() == "LINE":
                start, end = entity.dxf.start, entity.dxf.end
                min_x, min_y = min(min_x, start[0], end[0]), min(min_y, start[1], end[1])
                max_x, max_y = max(max_x, start[0], end[0]), max(max_y, start[1], end[1])
            elif entity.dxftype() == "LWPOLYLINE":
                for point in entity.vertices():
                    min_x, min_y = min(min_x, point[0]), min(min_y, point[1])
                    max_x, max_y = max(max_x, point[0]), max(max_y, point[1])

        # Compute internal & external dimensions
        l = max_x - min_x  # Internal Length
        b = max_y - min_y  # Internal Breadth
        L = l + 2 * wall_thickness  # External Length
        B = b + 2 * wall_thickness  # External Breadth

        return l, L, b, B

    @staticmethod
    def calculate_perimeter(l, L, b, B):
        """Computes perimeter using the formula: P = 2[(l + w/2) + (b + k/2)]"""
        w = L - l
        k = B - b
        perimeter = 2 * ((l + w / 2) + (b + k / 2))
        return perimeter
