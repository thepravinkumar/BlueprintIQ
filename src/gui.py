import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import random
from dxf_processor import DXFProcessor
from calculations import Calculations
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class BlueprintIQApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BlueprintIQ - Civil Engineering DXF Analyzer")
        self.root.geometry("1000x700")
        self.root.configure(bg="#F0F0F0")  # Light gray background

        self.file_path = None
        self.entities = []
        self.mottos = [
            "Precision is the key to great engineering.",
            "A strong foundation leads to a strong structure.",
            "Measure twice, cut once.",
            "Every structure tells a story of its engineer.",
            "Engineering is about doing, not just knowing.",
            "Accuracy builds trust in construction.",
            "Bridges connect places, engineers connect ideas."
        ]
        self.used_mottos = set()

        self.create_home_screen()

    def get_unique_motto(self):
        """Returns a unique motto every time."""
        available_mottos = [m for m in self.mottos if m not in self.used_mottos]
        if not available_mottos:
            self.used_mottos.clear()
            available_mottos = self.mottos
        motto = random.choice(available_mottos)
        self.used_mottos.add(motto)
        return motto

    def create_home_screen(self):
        """Creates the home screen UI."""
        self.clear_frame()

        frame = ttk.Frame(self.root, padding=20)
        frame.pack(expand=True, fill=tk.BOTH)

        title = ttk.Label(frame, text="BlueprintIQ - DXF Analyzer", font=("Helvetica", 18, "bold"))
        title.pack(pady=20)

        select_btn = ttk.Button(frame, text="📂 Select DXF File", command=self.select_file, style="TButton")
        select_btn.pack(pady=10)

    def select_file(self):
        """Opens file dialog to select a DXF file."""
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
        """Displays the results and DXF preview with labels."""
        self.clear_frame()
        
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(expand=True, fill=tk.BOTH)

        # Engineering Motto
        motto_label = ttk.Label(frame, text=f"🏗️ Engineering Motto: {self.get_unique_motto()}", 
                                font=("Helvetica", 12, "italic"), foreground="blue")
        motto_label.pack(pady=5)

        # Results section
        result_text = f"""
        📏 Internal Length (l): {l:.2f} units
        📐 External Length (L): {L:.2f} units
        🏗 Internal Breadth (b): {b:.2f} units
        🏠 External Breadth (B): {B:.2f} units
        🔲 Perimeter: {perimeter:.2f} units
        """

        label = ttk.Label(frame, text=result_text, font=("Helvetica", 12), justify=tk.LEFT)
        label.pack(pady=10)

        # Create a visualization canvas
        viz_frame = ttk.Frame(frame)
        viz_frame.pack(fill=tk.BOTH, expand=True)

        fig = Figure(figsize=(6, 6), facecolor="white")
        ax = fig.add_subplot(111)
        ax.set_facecolor("#F0F0F0")
        ax.set_title("DXF Blueprint Preview", color="black")
        ax.tick_params(colors="black")

        self.plot_entities(ax, l, L, b, B)

        canvas = FigureCanvasTkAgg(fig, master=viz_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        back_btn = ttk.Button(frame, text="🔙 Back to Home", command=self.create_home_screen, style="TButton")
        back_btn.pack(pady=10)

    def plot_entities(self, ax, l, L, b, B):
        """Visualizes DXF entities with labeled dimensions."""
        for entity in self.entities:
            if entity.dxftype() == 'LINE':
                x = [entity.dxf.start[0], entity.dxf.end[0]]
                y = [entity.dxf.start[1], entity.dxf.end[1]]
                ax.plot(x, y, color="black", linewidth=1)

            elif entity.dxftype() == 'LWPOLYLINE':
                points = list(entity.vertices())
                poly = plt.Polygon([point[:2] for point in points], closed=True, fill=False, edgecolor="blue")
                ax.add_patch(poly)

        # Add labels for dimensions
        ax.text(L / 2, -2, f"External Length (L) = {L:.2f}", fontsize=10, color="red", ha="center")
        ax.text(l / 2, -4, f"Internal Length (l) = {l:.2f}", fontsize=10, color="blue", ha="center")
        ax.text(-2, B / 2, f"External Breadth (B) = {B:.2f}", fontsize=10, color="red", rotation=90, va="center")
        ax.text(-4, b / 2, f"Internal Breadth (b) = {b:.2f}", fontsize=10, color="blue", rotation=90, va="center")

        ax.autoscale()

    def clear_frame(self):
        """Removes all existing UI elements."""
        for widget in self.root.winfo_children():
            widget.destroy()

# Custom Styles
style = ttk.Style()
style.configure("TButton", font=("Helvetica", 12, "bold"), padding=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = BlueprintIQApp(root)
    root.mainloop()
