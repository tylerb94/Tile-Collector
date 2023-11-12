import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

class TileCollector:
    def __init__(self, master):
        self.master = master
        self.master.title("Tile Collector")

        # GUI Variables
        self.input_type_var = tk.StringVar(value="Folder")
        self.input_path_var = tk.StringVar()
        self.output_path_var = tk.StringVar()
        self.tile_size_var = tk.StringVar(value="16,16")

        # Image View
        self.image_label = tk.Label(self.master, text="Image View:")
        self.image_label.grid(row=0, column=2, rowspan=10, padx=(20, 0))

        # Pygame Initialization - Removed

        # GUI Setup
        self.setup_gui()

    def setup_gui(self):
        self.create_widgets()
    def create_widgets(self):

        # Column 0
        # Input Type
        input_type_label = tk.Label(self.master, text="Input Type:")
        input_type_label.grid(row=0, column=0, sticky="w", padx=10, pady=(10, 0))

        folder_radio = tk.Radiobutton(self.master, text="Folder", variable=self.input_type_var, value="Folder")
        folder_radio.grid(row=1, column=0, sticky="w", padx=20)

        file_radio = tk.Radiobutton(self.master, text="File", variable=self.input_type_var, value="File")
        file_radio.grid(row=2, column=0, sticky="w", padx=20)

        # Input Path
        input_path_label = tk.Label(self.master, text="Input Path:")
        input_path_label.grid(row=3, column=0, sticky="w", padx=10, pady=(10, 0))

        input_path_entry = tk.Entry(self.master, textvariable=self.input_path_var, width=40)
        input_path_entry.grid(row=4, column=0, padx=20)

        # Output Path
        output_path_label = tk.Label(self.master, text="Output Path:")
        output_path_label.grid(row=5, column=0, sticky="w", padx=10, pady=(10, 0))

        output_path_entry = tk.Entry(self.master, textvariable=self.output_path_var, width=40)
        output_path_entry.grid(row=6, column=0, padx=20)

        # Tile Size
        tile_size_label = tk.Label(self.master, text="Tile Size (width, height):")
        tile_size_label.grid(row=7, column=0, sticky="w", padx=10, pady=(10, 0))

        tile_size_entry = tk.Entry(self.master, textvariable=self.tile_size_var, width=20)
        tile_size_entry.grid(row=8, column=0, padx=20)

        # Start Button
        start_button = tk.Button(self.master, text="Start", command=self.start_process)
        start_button.grid(row=9, column=0, pady=(20, 0))

        # Column 1
        # Browse Buttons
        browse_input_button = tk.Button(self.master, text="Browse", command=self.browse_input_path)
        browse_input_button.grid(row=4, column=1)

        browse_output_button = tk.Button(self.master, text="Browse", command=self.browse_output_path)
        browse_output_button.grid(row=6, column=1)

        # Column 2
        # Empty for Image View

    def browse_input_path(self):
        path = filedialog.askdirectory() if self.input_type_var.get() == "Folder" else filedialog.askopenfilename()
        if path:
            self.input_path_var.set(path)

    def browse_output_path(self):
        path = filedialog.asksaveasfilename(defaultextension=".png")
        if path:
            self.output_path_var.set(path)

    def start_process(self):
        input_type = self.input_type_var.get()
        input_path = self.input_path_var.get()
        output_path = self.output_path_var.get()
        tile_size = tuple(map(int, self.tile_size_var.get().strip('()').split(',')))

        all_image_tiles = []

        if input_type == "Folder" and os.path.isdir(input_path):
            self.process_folder(input_path, all_image_tiles, tile_size)
        elif input_type == "File" and os.path.isfile(input_path) and input_path.endswith(".png"):
            image_tiles = self.break_image_into_tiles(Image.open(input_path), tile_size)

            unique_tiles = [tile for tile in image_tiles if not any(self.are_images_equal(tile, u_tile) for u_tile in all_image_tiles)]
            all_image_tiles.extend(unique_tiles)

            self.save_spritesheet(all_image_tiles, output_path)
            self.show_image()

    def process_folder(self, input_directory, all_image_tiles, tile_size):
        for filename in os.listdir(input_directory):
            if filename.endswith(".png"):
                image_path = os.path.join(input_directory, filename)
                image_tiles = self.break_image_into_tiles(Image.open(image_path), tile_size)

                unique_tiles = [tile for tile in image_tiles if
                                not any(self.are_images_equal(tile, u_tile) for u_tile in all_image_tiles)]
                all_image_tiles.extend(unique_tiles)

        self.save_spritesheet(all_image_tiles, self.output_path_var.get())
        self.show_image()

    @staticmethod
    def break_image_into_tiles(image, tile_size):
        width, height = image.size
        tiles = [image.crop((x, y, x + tile_size[0], y + tile_size[1])) for y in range(0, height, tile_size[1]) for x in range(0, width, tile_size[0])]
        return tiles

    @staticmethod
    def are_images_equal(image1, image2):
        return image1.tobytes() == image2.tobytes()

    @staticmethod
    def save_spritesheet(tiles, output_path):
        num_tiles = len(tiles)
        num_columns = int(num_tiles**0.5)
        num_rows = (num_tiles + num_columns - 1) // num_columns

        sheet_width = num_columns * tiles[0].width
        sheet_height = num_rows * tiles[0].height

        spritesheet = Image.new("RGBA", (sheet_width, sheet_height), (0, 0, 0, 0))

        for i, tile in enumerate(tiles):
            row = i // num_columns
            col = i % num_columns
            spritesheet.paste(tile, (col * tile.width, row * tile.height))

        spritesheet.save(output_path)

    def show_image(self):
        image_path = self.output_path_var.get()
        if os.path.isfile(image_path):
            image = Image.open(image_path)
            photo = ImageTk.PhotoImage(image)

            self.image_label.configure(image=photo)
            self.image_label.image = photo
        else:
            self.image_label.configure(text="Image not found")

if __name__ == "__main__":
    root = tk.Tk()
    app = TileCollector(root)
    root.mainloop()
