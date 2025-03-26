import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from dxf_processor import DXFProcessor
from calculations import Calculations

class BlueprintIQApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BlueprintIQ - DXF Analyzer")
        self.root.geometry("800x600")

        self.file_path = None
        self.entities = []
        self.create_home_screen()

    def create_home_screen(self):
        """Creates the main screen UI."""
        self.clear_frame()

        frame = ttk.Frame(self.root, padding=20)
        frame.pack(expand=True, fill=tk.BOTH)

        title = ttk.Label(frame, text="BlueprintIQ - DXF Analyzer", font=("Helvetica", 18, "bold"))
        title.pack(pady=20)

        select_btn = ttk.Button(frame, text="Select DXF File", command=self.select_file)
        select_btn.pack(pady=10)

    def select_file(self):
        """Opens a file dialog to select a DXF file."""
        self.file_path = filedialog.askopenfilename(filetypes=[("DXF files", "*.dxf")])
        if self.file_path:
            self.process_file()

    def process_file(self):
        """Processes the DXF file and calculates dimensions and perimeter."""
        processor = DXFProcessor(self.file_path)
        processor.load_dxf()
        self.entities = processor.get_lines() + processor.get_polylines()

        # Compute internal and external dimensions
        l, L, b, B = Calculations.calculate_dimensions(self.entities)

        # Compute perimeter
        perimeter = Calculations.calculate_perimeter(l, L, b, B)

        self.show_results(l, L, b, B, perimeter)

    def show_results(self, l, L, b, B, perimeter):
        """Displays the calculated results."""
        self.clear_frame()

        frame = ttk.Frame(self.root, padding=20)
        frame.pack(expand=True, fill=tk.BOTH)

        result_text = f"""
        Internal Length (l): {l:.2f} units
        External Length (L): {L:.2f} units
        Internal Breadth (b): {b:.2f} units
        External Breadth (B): {B:.2f} units
        Perimeter: {perimeter:.2f} units
        """

        label = ttk.Label(frame, text=result_text, font=("Helvetica", 12), justify=tk.LEFT)
        label.pack(pady=10)

        back_btn = ttk.Button(frame, text="Back to Home", command=self.create_home_screen)
        back_btn.pack(pady=10)

    def clear_frame(self):
        """Removes all existing UI elements."""
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = BlueprintIQApp(root)
    root.mainloop()
