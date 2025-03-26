import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import random
import os
import ezdxf
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class BlueprintIQApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Home Page")
        self.root.geometry("1000x700")
        self.root.configure(bg="#2E3B55")  # Engineering dark theme

        self.file_path = None
        self.entities = []
        self.history = []
        self.internal_length = 0
        self.external_length = 0
        self.internal_breadth = 0
        self.external_breadth = 0
        self.perimeter = 0
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
        """Creates the home screen UI with history and exit button."""
        self.clear_frame()

        frame = ttk.Frame(self.root, padding=20)
        frame.pack(expand=True, fill=tk.BOTH)

        title = ttk.Label(frame, text="DXF Analyzer", font=("Helvetica", 18, "bold"), background="#2E3B55", foreground="white")
        title.pack(pady=20)

        select_btn = ttk.Button(frame, text="📂 Select DXF File", command=self.select_file)
        select_btn.pack(pady=10)

        # Recent History Section
        if self.history:
            history_label = ttk.Label(frame, text="📜 Recent Files:", font=("Helvetica", 12, "bold"), background="#2E3B55", foreground="white")
            history_label.pack(pady=5)
            for file in self.history[-3:]:  # Show last 3 analyzed files
                ttk.Label(frame, text=f"🔹 {os.path.basename(file)}", background="#2E3B55", foreground="white").pack()

        # Exit Button at Bottom Right
        exit_btn = ttk.Button(frame, text="❌ Exit", command=self.exit_app)
        exit_btn.pack(side=tk.BOTTOM, pady=20)

    def select_file(self):
        """Opens file dialog to select a DXF file."""
        self.file_path = filedialog.askopenfilename(filetypes=[("DXF files", "*.dxf")])
        if self.file_path:
            self.history.append(self.file_path)  # Add to history
            self.process_file()

    def process_file(self):
        """Processes the DXF file and extracts drawing data."""
        doc = ezdxf.readfile(self.file_path)
        msp = doc.modelspace()
        
        # Extract entities (Lines and Polylines)
        self.entities = [e for e in msp.query('LINE POLYLINE LWPOLYLINE')]

        if not self.entities:
            messagebox.showerror("Error", "No valid entities found in the DXF file.")
            return

        # Compute dimensions
        self.calculate_dimensions()

        # Show results & preview
        self.show_results()

    def calculate_dimensions(self):
        """Calculates internal & external length, breadth, and perimeter."""
        x_coords = []
        y_coords = []

        for entity in self.entities:
            if entity.dxftype() == 'LINE':
                x_coords.extend([entity.dxf.start.x, entity.dxf.end.x])
                y_coords.extend([entity.dxf.start.y, entity.dxf.end.y])
            elif entity.dxftype() in ['LWPOLYLINE', 'POLYLINE']:
                points = [(p[0], p[1]) for p in entity.get_points()]
                x_coords.extend([p[0] for p in points])
                y_coords.extend([p[1] for p in points])

        # Calculate dimensions
        min_x, max_x = min(x_coords), max(x_coords)
        min_y, max_y = min(y_coords), max(y_coords)

        self.internal_length = max_x - min_x
        self.internal_breadth = max_y - min_y
        self.external_length = self.internal_length * 1.02  # Example: 2% extra for walls
        self.external_breadth = self.internal_breadth * 1.02

        w = self.external_length - self.internal_length
        k = self.external_breadth - self.internal_breadth
        self.perimeter = 2 * ((self.internal_length + w / 2) + (self.internal_breadth + k / 2))

    def show_results(self):
        """Displays the results and DXF preview with buttons correctly placed."""
        self.clear_frame()

        frame = ttk.Frame(self.root, padding=20)
        frame.pack(expand=True, fill=tk.BOTH)

        motto_label = ttk.Label(frame, text=f"🏗️ Engineering Motto: {self.get_unique_motto()}", font=("Helvetica", 12, "italic"), background="#2E3B55", foreground="lightblue")
        motto_label.pack(pady=5)

        results_text = f"""
        📏 Internal Length (l): {self.internal_length:.2f} units
        📐 External Length (L): {self.external_length:.2f} units
        📏 Internal Breadth (b): {self.internal_breadth:.2f} units
        📐 External Breadth (B): {self.external_breadth:.2f} units
        🔲 Perimeter: {self.perimeter:.2f} units
        """
        results_label = ttk.Label(frame, text=results_text, font=("Helvetica", 12), background="#2E3B55", foreground="white", justify="left")
        results_label.pack(pady=10)

        # Visualization
        viz_frame = ttk.Frame(frame)
        viz_frame.pack(fill=tk.BOTH, expand=True)

        fig = Figure(figsize=(4, 4), facecolor="white")  # **Reduced from 6x6 to 4x4**
        ax = fig.add_subplot(111)
        ax.set_title("DXF Blueprint Preview", color="black")

        self.plot_entities(ax)

        canvas = FigureCanvasTkAgg(fig, master=viz_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Buttons at Bottom Left & Right
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X, pady=20)

        home_btn = ttk.Button(btn_frame, text="🏠 Return to Home", command=self.create_home_screen)
        home_btn.pack(side=tk.LEFT, padx=20)

        analyze_again_btn = ttk.Button(btn_frame, text="🔄 Analyze Again", command=self.select_file)
        analyze_again_btn.pack(side=tk.RIGHT, padx=20)

    def plot_entities(self, ax):
        """Visualizes DXF entities properly."""
        for entity in self.entities:
            if entity.dxftype() == 'LINE':
                x = [entity.dxf.start.x, entity.dxf.end.x]
                y = [entity.dxf.start.y, entity.dxf.end.y]
                ax.plot(x, y, color="black", linewidth=2)
            elif entity.dxftype() in ['LWPOLYLINE', 'POLYLINE']:
                points = [(p[0], p[1]) for p in entity.get_points()]
                x, y = zip(*points)
                ax.plot(x, y, color="black", linewidth=2)

        ax.autoscale()

    def clear_frame(self):
        """Removes all existing UI elements."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def exit_app(self):
        """Closes the application."""
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = BlueprintIQApp(root)
    root.mainloop()
