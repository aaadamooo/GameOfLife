import tkinter as tk
import random

# Config
CELL_SIZE = 10

class GameLogic:
    """Klasa odpowiedzialna za logikę gry w życie."""
    def __init__(self, width=80, height=60):
        self.width = width
        self.height = height
        self.grid = [[0 for _ in range(width)] for _ in range(height)]
        self.generation = 0
        self.population = 0

    def set_grid_size(self, width, height):
        """Ustawia rozmiar siatki."""
        self.width = width
        self.height = height
        self.grid = [[0 for _ in range(width)] for _ in range(height)]
        self.generation = 0
        self.population = 0

    def toggle_cell(self, x, y):
        """Przełącza stan komórki (żywa/martwa)."""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y][x] = 1 - self.grid[y][x]
            self.update_population()

    def update_grid(self):
        """Aktualizuje siatkę zgodnie z zasadami gry w życie."""
        new_grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
        for y in range(self.height):
            for x in range(self.width):
                live_neighbors = self.count_live_neighbors(x, y)
                if self.grid[y][x] == 1:
                    if live_neighbors in [2, 3]:
                        new_grid[y][x] = 1
                else:
                    if live_neighbors == 3:
                        new_grid[y][x] = 1
        self.grid = new_grid
        self.generation += 1
        self.update_population()

    def count_live_neighbors(self, x, y):
        """Liczy żywych sąsiadów dla danej komórki."""
        count = 0
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = (x + dx) % self.width, (y + dy) % self.height
                count += self.grid[ny][nx]
        return count

    def update_population(self):
        """Aktualizuje liczbę żywych komórek."""
        self.population = sum(sum(row) for row in self.grid)

    def clear_grid(self):
        """Czyści siatkę."""
        self.grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.generation = 0
        self.population = 0

    def randomize_grid(self):
        """Losowo wypełnia siatkę."""
        self.grid = [[random.choice([0, 1]) for _ in range(self.width)] for _ in range(self.height)]
        self.generation = 0
        self.population = 0


class GameOfLife:
    """Klasa odpowiedzialna za interfejs użytkownika."""
    def __init__(self, root):
        self.root = root
        self.root.title("Gra w życie")

        # Inicjalizacja logiki gry
        self.game_logic = GameLogic()

        # Interfejs użytkownika
        self.controls_frame = tk.Frame(root)
        self.controls_frame.pack()

        self.size_label = tk.Label(self.controls_frame, text="Rozmiar siatki: ")
        self.size_label.pack(side=tk.LEFT)

        self.width_entry = tk.Entry(self.controls_frame, width=5)
        self.width_entry.insert(0, "80")
        self.width_entry.pack(side=tk.LEFT)

        self.height_entry = tk.Entry(self.controls_frame, width=5)
        self.height_entry.insert(0, "60")
        self.height_entry.pack(side=tk.LEFT)

        self.set_size_button = tk.Button(self.controls_frame, text="Ustaw", command=self.set_grid_size)
        self.set_size_button.pack(side=tk.LEFT)

        self.start_button = tk.Button(self.controls_frame, text="Start", command=self.start_game)
        self.start_button.pack(side=tk.LEFT)

        self.stop_button = tk.Button(self.controls_frame, text="Stop", command=self.stop_game)
        self.stop_button.pack(side=tk.LEFT)

        self.clear_button = tk.Button(self.controls_frame, text="Wyczyść", command=self.clear_grid)
        self.clear_button.pack(side=tk.LEFT)

        self.random_button = tk.Button(self.controls_frame, text="Losowy układ", command=self.randomize_grid)
        self.random_button.pack(side=tk.LEFT)

        self.speed_label = tk.Label(self.controls_frame, text="Szybkość: ")
        self.speed_label.pack(side=tk.LEFT)

        self.speed_scale = tk.Scale(self.controls_frame, from_=10, to=1000, resolution=10, orient=tk.HORIZONTAL)
        self.speed_scale.set(100)
        self.speed_scale.pack(side=tk.LEFT)

        self.info_label = tk.Label(self.controls_frame, text="Generacja: 0 | Populacja: 0")
        self.info_label.pack(side=tk.LEFT)

        self.canvas = tk.Canvas(root, bg="white")
        self.canvas.pack()

        self.running = False
        self.canvas.bind("<Button-1>", self.toggle_cell)

        self.set_grid_size()

    def set_grid_size(self):
        """Ustawia rozmiar siatki na podstawie danych z interfejsu."""
        try:
            width = int(self.width_entry.get())
            height = int(self.height_entry.get())
            if width <= 0 or height <= 0:
                raise ValueError("Rozmiar siatki musi być dodatni.")
            self.game_logic.set_grid_size(width, height)
            self.canvas.config(width=width * CELL_SIZE, height=height * CELL_SIZE)
            self.draw_grid_lines()
            self.draw_cells()
            self.update_info()
        except ValueError as e:
            print(f"Błąd: {e}")

    def toggle_cell(self, event):
        """Przełącza stan komórki po kliknięciu."""
        x = event.x // CELL_SIZE
        y = event.y // CELL_SIZE
        self.game_logic.toggle_cell(x, y)
        self.draw_cells()

    def draw_grid_lines(self):
        """Rysuje linie siatki."""
        self.canvas.delete("grid_lines")
        for x in range(0, self.game_logic.width * CELL_SIZE, CELL_SIZE):
            self.canvas.create_line(x, 0, x, self.game_logic.height * CELL_SIZE, fill="gray", tags="grid_lines")
        for y in range(0, self.game_logic.height * CELL_SIZE, CELL_SIZE):
            self.canvas.create_line(0, y, self.game_logic.width * CELL_SIZE, y, fill="gray", tags="grid_lines")

    def draw_cells(self):
        """Rysuje komórki na siatce."""
        self.canvas.delete("cells")
        for y in range(self.game_logic.height):
            for x in range(self.game_logic.width):
                if self.game_logic.grid[y][x] == 1:
                    self.canvas.create_rectangle(
                        x * CELL_SIZE,
                        y * CELL_SIZE,
                        (x + 1) * CELL_SIZE,
                        (y + 1) * CELL_SIZE,
                        fill="black",
                        tags="cells"
                    )

    def update_info(self):
        """Aktualizuje informacje o generacji i populacji."""
        self.info_label.config(text=f"Generacja: {self.game_logic.generation} | Populacja: {self.game_logic.population}")

    def run(self):
        """Uruchamia symulację."""
        if self.running:
            self.game_logic.update_grid()
            self.draw_cells()
            self.update_info()
            self.root.after(self.speed_scale.get(), self.run)

    def start_game(self):
        """Rozpoczyna symulację."""
        if not self.running:
            self.running = True
            self.run()

    def stop_game(self):
        """Zatrzymuje symulację."""
        self.running = False

    def clear_grid(self):
        """Czyści siatkę."""
        self.running = False
        self.game_logic.clear_grid()
        self.draw_cells()
        self.update_info()

    def randomize_grid(self):
        """Losowo wypełnia siatkę."""
        self.running = False
        self.game_logic.randomize_grid()
        self.draw_cells()
        self.update_info()


if __name__ == "__main__":
    root = tk.Tk()
    game = GameOfLife(root)
    root.mainloop()
