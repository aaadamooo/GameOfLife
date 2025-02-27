import pytest
from game_of_life.game import GameLogic 

@pytest.fixture
def game():
    """Fixture tworzące instancję gry do testów."""
    return GameLogic(width=10, height=10)  

def test_initial_grid_size(game):
    """Testuje, czy siatka jest poprawnie inicjalizowana."""
    assert len(game.grid) == 10  # Domyślna wysokość
    assert len(game.grid[0]) == 10  # Domyślna szerokość

def test_toggle_cell(game):
    """Testuje przełączanie stanu komórki."""
    game.toggle_cell(0, 0)  # Przełącz komórkę (0, 0)
    assert game.grid[0][0] == 1  # Komórka powinna być "żywa"

    game.toggle_cell(0, 0)  # Przełącz ponownie
    assert game.grid[0][0] == 0  # Komórka powinna być "martwa"

def test_count_live_neighbors(game):
    """Testuje liczenie żywych sąsiadów."""
    game.grid[1][1] = 1  # Ustawienie żywej komórki
    assert game.count_live_neighbors(1, 1) == 0  # Brak sąsiadów

    game.grid[0][1] = 1  # Dodanie sąsiada
    assert game.count_live_neighbors(1, 1) == 1  # Jeden sąsiad

    # Testowanie krawędzi siatki
    game.grid[0][0] = 1  # Lewy górny róg
    assert game.count_live_neighbors(0, 0) == 2  # torus

def test_update_grid(game):
    """Testuje aktualizację siatki."""
    game.grid[1][1] = 1
    game.grid[1][2] = 1
    game.grid[2][1] = 1  # Tworzenie wzorca dla 3 żywych komórek
    game.update_grid()
    assert game.grid[2][2] == 1  # Nowa komórka powinna się narodzić

    # Testowanie stabilnego wzorca (blok)
    game.clear_grid()
    game.grid[1][1] = 1
    game.grid[1][2] = 1
    game.grid[2][1] = 1
    game.grid[2][2] = 1
    game.update_grid()
    assert game.grid[1][1] == 1  # Blok powinien pozostać stabilny
    assert game.grid[1][2] == 1
    assert game.grid[2][1] == 1
    assert game.grid[2][2] == 1

def test_clear_grid(game):
    """Testuje czyszczenie siatki."""
    game.grid[0][0] = 1
    game.clear_grid()
    assert game.grid[0][0] == 0  # Siatka powinna być pusta
    assert game.population == 0  # Populacja powinna wynosić 0
    assert game.generation == 0  # Licznik generacji powinien być zresetowany

def test_randomize_grid(game):
    """Testuje losowe wypełnienie siatki."""
    game.randomize_grid()
    assert sum(sum(row) for row in game.grid) > 0  # Siatka powinna zawierać żywe komórki

def test_set_grid_size(game):
    """Testuje zmianę rozmiaru siatki."""
    game.set_grid_size(20, 20)
    assert len(game.grid) == 20  # Nowa wysokość
    assert len(game.grid[0]) == 20  # Nowa szerokość
    assert game.generation == 0  # Licznik generacji powinien być zresetowany
    assert game.population == 0  # Populacja powinna wynosić 0