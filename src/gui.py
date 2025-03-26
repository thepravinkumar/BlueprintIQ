def process_file(self):
    """Processes the DXF file and calculates the correct dimensions and perimeter."""
    processor = DXFProcessor(self.file_path)
    processor.load_dxf()
    self.entities = processor.get_lines() + processor.get_polylines()

    # Compute dimensions
    l, L, b, B = Calculations.calculate_dimensions(self.entities)

    # Compute perimeter
    perimeter = Calculations.calculate_perimeter(l, L, b, B)

    self.show_results(l, L, b, B, perimeter)

def show_results(self, l, L, b, B, perimeter):
    """Displays the calculated results."""
    self.clear_frame()

    result_text = f"""
    Internal Length (l): {l:.2f} units
    External Length (L): {L:.2f} units
    Internal Breadth (b): {b:.2f} units
    External Breadth (B): {B:.2f} units
    Perimeter: {perimeter:.2f} units
    """

    label = ttk.Label(self.root, text=result_text, font=("Helvetica", 12))
    label.pack(pady=20)
