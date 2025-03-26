import ezdxf

class DXFProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.entities = []

    def load_dxf(self):
        """Loads a DXF file and extracts entities."""
        try:
            doc = ezdxf.readfile(self.file_path)
            self.entities = list(doc.modelspace())
        except Exception as e:
            print(f"Error loading DXF file: {e}")

    def get_lines(self):
        """Extracts lines from DXF file."""
        return [e for e in self.entities if e.dxftype() == "LINE"]

    def get_polylines(self):
        """Extracts polylines from DXF file."""
        return [e for e in self.entities if e.dxftype() == "LWPOLYLINE"]
