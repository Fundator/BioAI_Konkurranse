import numpy as np
from typing import List, Tuple
from collections import Counter
import random

distances = None
n_destinations = None

round_trip = True # Use True unless you know what you are doing! False is not competition-ready


tasks = ["lett", "vanskelig", "veldig_vanskelig", "abakus_bedpres"]
def load_distances(task: int, file_name: str = "") -> np.ndarray:
    global distances
    global n_destinations

    file_name = file_name if file_name != "" else f"{tasks[task - 1]}.txt"

    distances = np.loadtxt(f'BioAI_Konkurranse/data/{file_name}')
    n_destinations = distances.shape[0]

    return distances


def fitness_function(route: List[int]) -> float:
    route = list(route)
    if not round_trip:
        # Add start and stop for non round_trip tasks
        route = [0] + route + [n_destinations - 1]
    route_legs = [distances[route[idx]][route[(idx + 1) % n_destinations]] for idx in range(n_destinations)]
    return sum(route_legs) if round_trip else sum(route_legs) - route_legs[-1]


def validate_route(route: List[int]):
    if len(route) != n_destinations:
        context1 = f"Antallet destinasjoner i ruten din ({len(route)}) er ikke det samme som antallet destinasjoner i oppgaven ({n_destinations})"
        context2 = f"Følgende destinasjoner mangler: {set(range(n_destinations)) - set(route)}"
        assert False, f"{context1}\n{context2}"
    if len(set(route)) != n_destinations:
        dest_counter = Counter(route)
        context1 = f"Antallet *unike* destinasjoner i ruten din ({len(set(route))}) er ikke det samme som antallet destinasjoner i oppgaven ({n_destinations})"
        context2 = f"Følgende destinasjoner forekommer mer enn en gang i ruten (vises på formen Counter(dict(destinasjon: antall, ...)): {Counter({k: c for k, c in dest_counter.items() if c > 1})}"
        assert False, f"{context1}\n{context2}"
    assert np.max(route) == n_destinations - 1
    assert np.min(route) == 0


def init_population(pop_size: int) -> List[List[int]]:
    global n_destinations
    global round_trip
    
    if round_trip:
        pop = [list(range(n_destinations)) for _ in range(pop_size)]
    else:
        pop = [list(range(1, n_destinations - 1)) for _ in range(pop_size)]
    [random.shuffle(route) for route in pop]

    return pop

def start_task(task: int,  pop_size: int, gens: int, file_name: str = "", is_round_trip: bool = True) -> Tuple[int, List[int]]:
    global round_trip
    round_trip = is_round_trip

    if file_name == "":
        assert 0 < task <= len(tasks), f"Du må velge enten oppgave 1, 2, 3, eller 4, ikke {task}"
    assert pop_size % 2 == 0, "For enkelhetsskyld bruker man hovedsaklig partall i POP_SIZE. Legg til 1 på POP_SIZE og prøv igjen."
    assert pop_size <= 400, "Maks størrelse på populasjonen er 400"
    assert gens <= 300, "Maks antall generasjoner er 300"

    load_distances(task, file_name)
    pop = init_population(pop_size)

    return n_destinations, pop


if __name__ == "__main__":
    import json
    from sklearn.neighbors import NearestNeighbors
    from pathlib import Path

    json_file_name = Path("abakus_bedpres.json")
    folder = Path("data/travelling_student")

    with open(folder / json_file_name, "r") as f:
        raw = json.load(f)
        arr = raw["points"]

        assert arr[0]["type"] == "source"
        assert arr[-1]["type"] == "sink"

        points = np.array(list([point["x"], point["y"]] for point in arr))


        # Invert y axis to make visualization same as scoreboard
        points[:, 1] = -points[:, 1]

        nbrs = NearestNeighbors(n_neighbors=len(points), algorithm='kd_tree').fit(points)


        distances, neighbours = nbrs.kneighbors(points)

        sorted_indices = np.argsort(neighbours, axis=1)
        distances = np.take_along_axis(distances, sorted_indices, axis=1)

        xy_path = Path("data/xy") / json_file_name.with_suffix(".txt")
        dist_path = Path("data") / json_file_name.with_suffix(".txt")

        np.savetxt(xy_path, points, fmt="%.1f")
        np.savetxt(dist_path, distances, fmt="%.3f")


