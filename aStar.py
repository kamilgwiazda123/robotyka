import numpy as np


class Node:
    """
        Node jest to klasa A*
        rodzic jest rodzicem bieżącego węzła
        pozycja to bieżąca pozycja węzła w labiryncie
        g to koszt od początku do bieżącego węzła
        h jest szacowanym kosztem heurystycznym bieżącego węzła do końca węzła
        f to całkowity koszt węzła  f = g + h
    """

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

# Ta funkcja zwraca ścieżkę wyszukiwania
def return_path(current_node, maze):
    path = []
    no_rows, no_columns = np.shape(maze)
    #tutaj tworzymy zainicjowany labirynt wynikowy z -1 w każdej pozycji
    result = [[-1 for i in range(no_columns)] for j in range(no_rows)]
    current = current_node
    while current is not None:
        path.append(current.position)
        current = current.parent
    # Zwracamy tutaj odwróconą ścieżkę, ponieważ musimy pokazywać ścieżkę od początku do końca
    path = path[::-1]
    start_value = 0
    # aktualizujemy ścieżkę od początku do końca znalezioną przez wyszukiwanie A* z każdym krokiem o 1
    for i in range(len(path)):
        result[path[i][0]][path[i][1]] = start_value
        start_value += 1
    return result


def search(maze, cost, start, end):
    """
        Zwraca listę krotek jako ścieżkę od podanego początku do podanego końca w danym labiryncie
        :param maze:
        :param cost
        :param start:
        :param end:
        :return:
    """

    # Tworzymy węzeł początkowy i końcowy z zainicjowanymi wartościami dla g, h i f
    start_node = Node(None, tuple(start))
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, tuple(end))
    end_node.g = end_node.h = end_node.f = 0

    # Inicjuję listę do odwiedzenia oraz listę, która została odwiedzona
    # na tej liście umieszczam wszystkie węzły yet_to_visit do eksploracji.
    # Tutaj znajdziemy węzeł o najniższym koszcie, który należy rozwinąć w następnej kolejności
    yet_to_visit_list = []
    # na tej liście umieszczam wszystkie węzły już zbadane, zeby nie eksplorować go ponownie
    visited_list = []

    # Dodaje węzeł początkowy
    yet_to_visit_list.append(start_node)

    # Dodaje warunke zatrzymania. Uniknięcie nieskończonej pętli i zatrzymanie.
    outer_iterations = 0
    max_iterations = (len(maze) // 2) ** 10

    # Szukamy po kwadratach. Zaczynam wyszukiwania w kolejności lewy-prawy-górny-dolny
    # (4 movements) from every positon

    move = [[-1, 0],  # go up
            [0, -1],  # go left
            [1, 0],  # go down
            [0, 1]]  # go right

    """
        1) Najpierw uzyskuje bieżący węzeł, porównując wszystkie koszty f i wybierając węzeł o najniższym koszcie do dalszej rozbudowy.
        2) Sprawdzam, czy osiągnięto maksymalną iterację, czy nie. Ustawiam wiadomość i zatrzymanie wykonywania.
        3) Usuwam wybrany węzeł z listy yet_to_visit i dodaje ten węzeł do listy odwiedzanych
        4) Testuje i zwracam ścieżkę i potem robie poniższe kroki
        5) Dla wybranego węzła znajduje wszystkie children (użyj move, aby znaleźć child)
            5.1) pobierz bieżącą pozycję dla wybranego noda (staje się on węzłem nadrzędnym dla children)
            5.2) check if a valid position exist (boundary will make few nodes invalid)
            5.3) jeśli jakikolwiek węzeł jest ścianą, zignoruj to
            5.4 dodaj do prawidłowej listy węzłów potomnych dla wybranego rodzica

            Dla węzłów potomnych
            1) jeśli dziecko na liście odwiedzanych, zignoruj ​​je i spróbuj następnego węzła
            2) oblicz wartości g, h i f węzła potomnego
            3) Jeśli child jest na liście yet_to_visit list zignoguj to
            4) w przeciwnym razie przenies child na liste yet_to_visit 
    """
    # sprawdz ile labirynt ma  wierszy i kolumn
    no_rows, no_columns = np.shape(maze)

    # sprawdzam do konca

    while len(yet_to_visit_list) > 0:

        # Za każdym razem, gdy dowolny węzeł jest odsyłany z listy yet_to_visit, zwiększana jest operacja
        outer_iterations += 1

        # pobierama bierzący węzeł
        current_node = yet_to_visit_list[0]
        current_index = 0
        for index, item in enumerate(yet_to_visit_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # jeśli osiągniemy punkt, zwróć ścieżkę, ponieważ może to nie być rozwiązanie
        # lub koszt obliczeń jest zbyt wysoki
        if outer_iterations > max_iterations:
            print("giving up on pathfinding too many iterations")
            return return_path(current_node, maze)

        # Usuń bieżący węzeł z listy yet_to_visit, dodaj do listy odwiedzanych
        yet_to_visit_list.pop(current_index)
        visited_list.append(current_node)

        # sprawdź, czy cel został osiągnięty, czy nie, jeśli tak, zwróć ścieżkę
        if current_node == end_node:
            return return_path(current_node, maze)

        # Generuje children ze wszystkich sąsiednich kwadratów.
        children = []

        for new_position in move:

            # pobieram pozycje noda
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Sprawdzam zasięg (czy mieści sie w granicach labiryntu)
            if (node_position[0] > (no_rows - 1) or
                    node_position[0] < 0 or
                    node_position[1] > (no_columns - 1) or
                    node_position[1] < 0):
                continue

            # sprawdzam czy moge chodzic po tym terenie
            if maze[node_position[0]][node_position[1]] != 0:
                continue

            # tworze nowy node
            new_node = Node(current_node, node_position)

            children.append(new_node)

        for child in children:

            # Jeśli child jest na liście odwiedzanych przeszukuje cala liste od poczatkt visited_list
            if len([visited_child for visited_child in visited_list if visited_child == child]) > 0:
                continue

            # tworze wartosci f, g, h
            child.g = current_node.g + cost
            # Obliczam koszty heurestyczne (odlegosc eukledyjska)
            child.h = (((child.position[0] - end_node.position[0]) ** 2) +
                       ((child.position[1] - end_node.position[1]) ** 2))

            child.f = child.g + child.h

            # child jest już na liście yet_to_visit, a koszt g jest już niższy
            if len([i for i in yet_to_visit_list if child == i and child.g > i.g]) > 0:
                continue

            # dodaje dziecko do listy yet_to_visit
            yet_to_visit_list.append(child)


if __name__ == '__main__':
    maze = [[0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 1, 0, 1, 0, 0],
            [0, 1, 1, 0, 1, 0],
            [0, 0, 0, 0, 1, 0]]

    start = [0, 0]
    end = [4, 5]
    cost = 1

    path = search(maze, cost, start, end)
    print('\n'.join([''.join(["{:" ">3d}".format(item) for item in row]) for row in path]))
    print("\n")

   # print(path)