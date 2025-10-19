#!/usr/bin/env python3
"""
Christmas Tree Decorator
A simple GUI application that allows users to decorate a Christmas tree
by dragging decorations onto it.
"""

import tkinter as tk
from tkinter import Canvas
import random
from dataclasses import dataclass
from typing import List, Tuple, Optional

@dataclass
class Decoration:
    """Represents a decoration that can be placed on the tree"""
    name: str
    color: str
    symbol: str
    size: int = 20

@dataclass
class PlacedDecoration:
    """Represents a decoration that has been placed on the tree"""
    decoration: Decoration
    x: int
    y: int
    canvas_id: int

class ChristmasTreeDecorator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Christmas Tree Decorator")
        self.root.geometry("800x600")
        self.root.configure(bg="#001122")
        
        # Available decorations
        self.decorations = [
            Decoration("Star", "#FFD700", "★", 25),
            Decoration("Ball Red", "#FF0000", "●", 20),
            Decoration("Ball Blue", "#0066FF", "●", 20),
            Decoration("Ball Gold", "#FFD700", "●", 20),
            Decoration("Bell", "#C0C0C0", "🔔", 18),
            Decoration("Candy Cane", "#FF69B4", "🍭", 18),
            Decoration("Gift", "#00FF00", "🎁", 22),
            Decoration("Angel", "#FFFFFF", "👼", 20),
        ]
        
        # Track placed decorations
        self.placed_decorations: List[PlacedDecoration] = []
        
        # Drag and drop state
        self.dragging_decoration = None
        self.drag_start_x = 0
        self.drag_start_y = 0
        
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the user interface"""
        # Main frame
        main_frame = tk.Frame(self.root, bg="#001122")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tree canvas (left side)
        self.tree_canvas = Canvas(
            main_frame,
            width=500,
            height=550,
            bg="#001122",
            highlightthickness=2,
            highlightcolor="#006600",
            name="tree_canvas"
        )
        self.tree_canvas.pack(side=tk.LEFT, padx=(0, 10))
        
        # Draw the Christmas tree
        self.draw_christmas_tree()
        
        # Decorations panel (right side)
        decorations_frame = tk.Frame(main_frame, bg="#001122")
        decorations_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Title for decorations
        title_label = tk.Label(
            decorations_frame,
            text="🎄 Decorations 🎄",
            font=("Arial", 16, "bold"),
            fg="#00FF00",
            bg="#001122"
        )
        title_label.pack(pady=(0, 20))
        
        # Decorations canvas
        self.decorations_canvas = Canvas(
            decorations_frame,
            width=250,
            height=500,
            bg="#112233",
            highlightthickness=2,
            highlightcolor="#006600",
            name="decorations_canvas"
        )
        self.decorations_canvas.pack()
        
        self.draw_decoration_palette()
        self.bind_events()
        
    def draw_christmas_tree(self):
        """Draw a Christmas tree on the canvas"""
        canvas = self.tree_canvas
        
        # Tree trunk
        canvas.create_rectangle(235, 450, 265, 500, fill="#8B4513", outline="#654321", width=2)
        
        # Tree layers (from bottom to top)
        tree_layers = [
            (250, 380, 150),  # Bottom layer
            (250, 320, 120),  # Middle layer  
            (250, 260, 90),   # Top layer
        ]
        
        for x, y, width in tree_layers:
            # Create triangular tree layer
            points = [
                x - width//2, y + 70,  # Bottom left
                x + width//2, y + 70,  # Bottom right
                x, y                   # Top
            ]
            canvas.create_polygon(points, fill="#006600", outline="#004400", width=2)
            
        # Tree star (can be replaced by user)
        canvas.create_text(250, 250, text="☆", font=("Arial", 30), fill="#FFD700")
        
        # Ground line
        canvas.create_line(50, 500, 450, 500, fill="#FFFFFF", width=2)
        
        # Add some snow effect
        for _ in range(20):
            x = random.randint(50, 450)
            y = random.randint(50, 200)
            canvas.create_text(x, y, text="❄", font=("Arial", 12), fill="#FFFFFF")
            
    def draw_decoration_palette(self):
        """Draw the decoration palette on the right side"""
        canvas = self.decorations_canvas
        
        # Draw decorations in a grid
        cols = 2
        x_start, y_start = 50, 50
        x_spacing, y_spacing = 100, 80
        
        for i, decoration in enumerate(self.decorations):
            row = i // cols
            col = i % cols
            
            x = x_start + col * x_spacing
            y = y_start + row * y_spacing
            
            # Create clickable rectangle background
            rect_id = canvas.create_rectangle(
                x - 30, y - 20, x + 30, y + 20,
                fill="#334455", outline="#FFFFFF", width=2,
                tags=f"decoration_{i}"
            )
            
            # Create decoration symbol on top
            text_id = canvas.create_text(
                x, y, 
                text=decoration.symbol,
                font=("Arial", decoration.size),
                fill=decoration.color,
                tags=f"decoration_{i}"
            )
            
            # Add label
            canvas.create_text(
                x, y + 30,
                text=decoration.name.split()[0],  # First word only
                font=("Arial", 10),
                fill="#FFFFFF"
            )
            
    def bind_events(self):
        """Bind mouse events for drag and drop"""
        self.decorations_canvas.bind("<Button-1>", self.on_decoration_click)
        self.decorations_canvas.bind("<B1-Motion>", self.on_drag)
        
        self.tree_canvas.bind("<Button-1>", self.on_tree_click)
        self.tree_canvas.bind("<B1-Motion>", self.on_drag)
        
        # Use only global drop handler for cross-canvas dragging
        self.root.bind("<ButtonRelease-1>", self.on_global_drop)
        
    def on_decoration_click(self, event):
        """Handle clicking on a decoration in the palette"""
        # Find all items at this point
        items = self.decorations_canvas.find_overlapping(event.x-1, event.y-1, event.x+1, event.y+1)
        
        for item in items:
            tags = self.decorations_canvas.gettags(item)
            
            for tag in tags:
                if tag.startswith("decoration_"):
                    decoration_index = int(tag.split("_")[1])
                    self.dragging_decoration = self.decorations[decoration_index]
                    self.drag_start_x = event.x
                    self.drag_start_y = event.y
                    return
                
    def on_tree_click(self, event):
        """Handle clicking on the tree canvas"""
        # Check if clicking on an existing decoration to remove it
        item = self.tree_canvas.find_closest(event.x, event.y)[0]
        for placed_decoration in self.placed_decorations:
            if placed_decoration.canvas_id == item:
                self.tree_canvas.delete(item)
                self.placed_decorations.remove(placed_decoration)
                break
                
    def on_drag(self, event):
        """Handle dragging motion"""
        if self.dragging_decoration:
            # Change cursor to indicate dragging
            event.widget.config(cursor="hand2")
            
    
    def on_global_drop(self, event):
        """Handle global mouse release for cross-canvas dragging"""
        if self.dragging_decoration:
            # Get screen coordinates
            screen_x = self.root.winfo_pointerx()
            screen_y = self.root.winfo_pointery()
            
            # Get tree canvas position
            tree_x = self.tree_canvas.winfo_rootx()
            tree_y = self.tree_canvas.winfo_rooty()
            tree_width = self.tree_canvas.winfo_width()
            tree_height = self.tree_canvas.winfo_height()
            
            # Check if mouse is over tree canvas
            if (tree_x <= screen_x <= tree_x + tree_width and 
                tree_y <= screen_y <= tree_y + tree_height):
                
                # Convert to canvas coordinates
                canvas_x = screen_x - tree_x
                canvas_y = screen_y - tree_y
                
                # Check if within tree bounds
                if self.is_on_tree(canvas_x, canvas_y):
                    self.place_decoration(canvas_x, canvas_y, self.dragging_decoration)
            
            # Reset state
            self.decorations_canvas.config(cursor="")
            self.tree_canvas.config(cursor="")
            self.dragging_decoration = None
            
    def is_on_tree(self, x: int, y: int) -> bool:
        """Check if coordinates are within the tree area"""
        # Simple tree bounds check
        if y < 250 or y > 450:  # Above star or below tree
            return False
            
        # Check if within triangular bounds of tree layers
        tree_layers = [
            (250, 380, 150),  # Bottom layer
            (250, 320, 120),  # Middle layer
            (250, 260, 90),   # Top layer
        ]
        
        for center_x, center_y, width in tree_layers:
            if abs(y - center_y) <= 70:  # Within layer height
                # Calculate width at this y position
                layer_width = width * (1 - abs(y - center_y) / 70)
                if abs(x - center_x) <= layer_width / 2:
                    return True
        
        return False
        
    def place_decoration(self, x: int, y: int, decoration: Decoration):
        """Place a decoration on the tree"""
        # Add some randomness to placement to avoid overlapping
        x += random.randint(-10, 10)
        y += random.randint(-10, 10)
        
        # Create the decoration on the tree
        item_id = self.tree_canvas.create_text(
            x, y,
            text=decoration.symbol,
            font=("Arial", decoration.size),
            fill=decoration.color
        )
        
        # Track the placed decoration
        placed_decoration = PlacedDecoration(decoration, x, y, item_id)
        self.placed_decorations.append(placed_decoration)
        
    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = ChristmasTreeDecorator()
    app.run()