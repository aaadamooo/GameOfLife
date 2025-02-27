[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/e9oOIXnI)
[![Open in Codespaces](https://classroom.github.com/assets/launch-codespace-2972f46106e565e64193e422d61a12cf1da4916b45550586e14ef0a7c637dd04.svg)](https://classroom.github.com/open-in-codespaces?assignment_repo_id=17857811)

> [!NOTE]
>
> #### Informacje ogólne
> W tym pliku należy udokumentować projekt. W nagłówku poniżej wpisz nazwę projektu, a następnie wpisz dokumentację, korzystając z formatu `markdown` ([GitHub doc](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax)).
>
> W ramach oceny, poza wykonaniem projektu, oceniane będzie stosowanie dobrych praktyk programistycznych w Pythonie, sprawdzane za pomocą programu `pylint` (**wszystkie flagi aktywne**). Ocena kodu przez `pylint` będzie stanowiła 10% oceny za projekt.

# Game of Life

Program implementuje automat komórkowy (The Game of Life) wymyślony przez Johna Conwaya w 1970 roku.

## Opis Automatu

Symulacja ma miejsce w tablicy o wymiarach zadanych przez użytkownika, której krawędzie są sklejone, tzn. jeżeli komórka próbuje przemieścić się do pola wykraczającego poza rozmiar tablicy, to pojawia się po drugiej stronie tablicy, jakby była ona zwinięta w torus. Dzięki temu symulacja może działać w sposób ciągły, a granice tablicy nie stanowią bariery dla przemieszczających się komórek.

Pole w siatce reprezentującej tablicę ma dwa możliwe stany:
- **Zamalowane** (pole zasiedlone przez komórkę)
- **Niezamalowane** (pole niezasiedlone przez komórkę)

Co interwał czasu z przedziału 10 ms do 1 s, określony przez użytkownika, obliczany jest następny stan automatu według następujących zasad:

1. Każda komórka wchodzi w interakcję z 8 polami, z którymi sąsiaduje (4 boki i 4 wierzchołki).
2. Każda komórka, która sąsiaduje z mniej niż dwiema innymi komórkami, umiera. - **Zasada niewystarczającej populacji**
3. Każda żywa komórka z dwoma lub trzema sąsiadami nie zmienia swojego stanu - **Zasada zachowania populacji**
4. Każda żywa komórka z więcej niż trzema sąsiadami umiera - **Zasada nadmiernej populacji**
5. Jeżeli niezasiedlone pole ma dokładnie 3 żywych sąsiadów, to zostaje zasiedlone żywą komórką.

```mermaid
graph TD;
    T[Tick czasu gry] --> A[Komórka żywa];
    T --> E[Komórka martwa];
    
    A --> B[Ma mniej niż 2 sąsiadów - umiera z samotności];
    A --> C[Ma 2 lub 3 sąsiadów - przeżywa];
    A --> D[Ma więcej niż 3 sąsiadów - umiera z przeludnienia];
    
    E --> F[Ma dokładnie 3 sąsiadów - ożywa];
    
    B --> T;
    C --> T;
    D --> T;
    F --> T;
```

## GUI

Program posiada prosty interfejs graficzny wykonany w Tkinter, umożliwiający:

* Zmianę rozmiaru siatki.

* Rozpoczęcie i zatrzymanie symulacji.

* Wyczyszczenie siatki (wszystkie komórki stają się martwe).

* Ustawienie losowego układu żywych komórek na siatce.

* Zmianę szybkości symulacji (parametr tick).


![Screen GUI](images/screen.png)


# [Uruchamianie]

Program uruchamia się z terminala polceniem  `Python GOL.py`

