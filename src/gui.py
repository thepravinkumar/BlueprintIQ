import tkinter as tk
from tkinter import ttk, filedialog
from dxf_processor import DXFProcessor
from calculations import Calculations

class BlueprintIQApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BlueprintIQ")
        self.root.geometry("800x600")

        self.file_path = None
        self.entities = []

        self.create_home_screen()

    def create_home_screen(self):
        """Home screen UI."""
        frame = ttk.Frame(self.root)
        frame.pack(expand=True, fill=tk.BOTH)

        title = ttk.Label(frame, text="BlueprintIQ - DXF Analyzer", font=("Helvetica", 18, "bold"))
        title.pack(pady=20)

        select_btn = ttk.Button(frame, text="Select DXF File", command=self.select_file)
        select_btn.pack(pady=10)

    def select_file(self):
        """Opens file dialog to select DXF file."""
        self.file_path = filedialog.askopenfilename(filetypes=[("DXF files", "*.dxf")])
        if self.file_path:
            self.process_file()

    def process_file(self):
        """Processes the DXF file and calculates metrics."""
        processor = DXFProcessor(self.file_path)
        processor.load_dxf()
        self.entities = processor.get_lines() + processor.get_polylines()

        perimeter = Calculations.calculate_perimeter(self.entities)
        centerline = Calculations.calculate_centerline_length(self.entities)

        self.show_results(perimeter, centerline)

    def show_results(self, perimeter, centerline):
        """Displays the calculated results."""
        self.clear_frame()
        
        label = ttk.Label(self.root, text=f"Perimeter: {perimeter:.2f} units\nCenterline Length: {centerline:.2f} units")
        label.pack(pady=20)

    def clear_frame(self):
        """Removes existing UI elements."""
        for widget in self.root.winfo_children():
            widget.destroy()
