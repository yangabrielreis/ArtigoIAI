import csv
import ast
from collections import deque, defaultdict

def load_graph(csv_path):
    graph = defaultdict(set)
    movie_dict = defaultdict(set)
    with open(csv_path, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                stars = ast.literal_eval(row['stars'])
                actors = []
                for a in stars:
                    name = a.strip().strip(',').strip('"').strip("'")
                    if not name or name.lower() in {'stars:', 'star:', '|'}:
                        continue
                    if 'star:' in name.lower() or 'stars:' in name.lower() or name == '|':
                        continue
                    if name in {'', 'Stars:', 'Star:', '|'}:
                        continue
                    actors.append(name)
                for i, actor1 in enumerate(actors):
                    for actor2 in actors[i+1:]:
                        graph[actor1].add(actor2)
                        graph[actor2].add(actor1)
                        movie_dict[frozenset([actor1, actor2])].add(row['title'])
            except Exception as e:
                continue
    return graph, movie_dict

def heuristic(actor, goal):
    return 0 if actor == goal else 1

def a_star(graph, movie_dict, start, goal):
    from heapq import heappush, heappop
    open_set = []
    heappush(open_set, (heuristic(start, goal), 0, start, [start]))
    visited = set()
    while open_set:
        f, g, current, path = heappop(open_set)
        if current == goal:
            return path
        if current in visited:
            continue
        visited.add(current)
        for neighbor in graph[current]:
            if neighbor not in visited:
                heappush(open_set, (g+1+heuristic(neighbor, goal), g+1, neighbor, path+[neighbor]))
    return None

def print_path(path, movie_dict):
    if not path:
        print('No connection found.')
        return
    print(f"Caminho encontrado ({len(path)-1} passos):")
    for i in range(len(path)-1):
        actors = frozenset([path[i], path[i+1]])
        movies = movie_dict.get(actors, {'? '})
        print(f"{path[i]} --[{', '.join(movies)}]--> {path[i+1]}")

def main():
    graph, movie_dict = load_graph('database/IMBD.csv')
    start = input('Ator inicial: ').strip()
    goal = input('Ator final: ').strip()
    path = a_star(graph, movie_dict, start, goal)
    print_path(path, movie_dict)

if __name__ == '__main__':
    main()
