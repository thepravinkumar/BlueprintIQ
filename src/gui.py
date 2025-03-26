import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from dxf_processor import DXFProcessor
from calculations import Calculations
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class BlueprintIQApp:
    def __init__(self, root):
        self.root = root
        self.root.title("BlueprintIQ - DXF Analyzer")
        self.root.geometry("900x650")
        self.root.configure(bg="#2A2A2A")  # Dark background

        self.file_path = None
        self.entities = []
        self.create_home_screen()

    def create_home_screen(self):
        """Creates the main screen UI."""
        self.clear_frame()

        frame = ttk.Frame(self.root, padding=20, style="Dark.TFrame")
        frame.pack(expand=True, fill=tk.BOTH)

        title = ttk.Label(frame, text="BlueprintIQ - DXF Analyzer", style="Title.TLabel")
        title.pack(pady=20)

        select_btn = ttk.Button(frame, text="Select DXF File", command=self.select_file, style="Button.TButton")
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
        """Displays the calculated results with a DXF preview."""
        self.clear_frame()

        frame = ttk.Frame(self.root, padding=20, style="Dark.TFrame")
        frame.pack(expand=True, fill=tk.BOTH)

        result_text = f"""
        📏 Internal Length (l): {l:.2f} units
        📐 External Length (L): {L:.2f} units
        🏗 Internal Breadth (b): {b:.2f} units
        🏠 External Breadth (B): {B:.2f} units
        🔲 Perimeter: {perimeter:.2f} units
        """

        label = ttk.Label(frame, text=result_text, style="Body.TLabel", justify=tk.LEFT)
        label.pack(pady=10)

        # Create a visualization canvas
        viz_frame = ttk.Frame(frame)
        viz_frame.pack(fill=tk.BOTH, expand=True)

        fig = Figure(figsize=(6, 6), facecolor="#2A2A2A")
        ax = fig.add_subplot(111)
        ax.set_facecolor("#2A2A2A")
        ax.set_title("DXF Preview", color="white")
        ax.tick_params(colors="white")

        self.plot_entities(ax)

        canvas = FigureCanvasTkAgg(fig, master=viz_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        back_btn = ttk.Button(frame, text="🔙 Back to Home", command=self.create_home_screen, style="Button.TButton")
        back_btn.pack(pady=10)

    def plot_entities(self, ax):
        """Visualizes DXF entities."""
        for entity in self.entities:
            if entity.dxftype() == 'LINE':
                x = [entity.dxf.start[0], entity.dxf.end[0]]
                y = [entity.dxf.start[1], entity.dxf.end[1]]
                ax.plot(x, y, color="lime", linewidth=1)

            elif entity.dxftype() == 'LWPOLYLINE':
                points = list(entity.vertices())
                poly = plt.Polygon([point[:2] for point in points], closed=True, fill=False, edgecolor="cyan")
                ax.add_patch(poly)

        ax.autoscale()

    def clear_frame(self):
        """Removes all existing UI elements."""
        for widget in self.root.winfo_children():
            widget.destroy()

# Custom Styles
style = ttk.Style()
style.configure("Dark.TFrame", background="#2A2A2A")
style.configure("Title.TLabel", background="#2A2A2A", foreground="white", font=("Helvetica", 18, "bold"))
style.configure("Body.TLabel", background="#2A2A2A", foreground="lightgray", font=("Helvetica", 12))
style.configure("Button.TButton", foreground="white", background="#4CAF50", font=("Helvetica", 12, "bold"), padding=10)
style.map("Button.TButton", background=[("active", "#45a049")])

if __name__ == "__main__":
    root = tk.Tk()
    app = BlueprintIQApp(root)
    root.mainloop()
