import numpy as np
from typing import List, Tuple
from collections import Counter
import random

distances = None
n_destinations = None

tasks = ["lett", "middels", "vanskelig", "veldig_vanskelig"]
def load_distances(task: int) -> np.ndarray:
    global distances
    global n_destinations

    distances = np.loadtxt(f'BioAI_Konkurranse/data/{tasks[task - 1]}.txt')
    n_destinations = distances.shape[0]

    return distances


def fitness_function(route: List[int]) -> float:
    route = list(route)
    validate_route(route)

    route_legs = [distances[stop1][stop2] for stop1, stop2 in zip(route, route[1:] + route[0:1])]
    return sum(route_legs)


def validate_route(route: List[int]):
    if len(route) != n_destinations:
        context1 = f"Antallet destinasjoner i ruten din {len(route)} er ikke det samme som antallet destinasjoner {n_destinations}"
        context2 = f"Følgende destinasjoner mangler: {set(range(n_destinations)) - set(route)}"
        assert False, f"{context1}\n{context2}"
    if len(set(route)) != n_destinations:
        dest_counter = Counter(route)
        context1 = f"Antallet *unike* destinasjoner i ruten din {len(set(route))} er ikke det samme som antallet destinasjoner {n_destinations}"
        context2 = f"Følgende destinasjoner forekommer mer enn en gang i ruten (vises på formen Counter(dict(destinasjon: antall, ...)): {Counter({k: c for k, c in dest_counter.items() if c > 1})}"
        assert False, f"{context1}\n{context2}"
    assert np.max(route) == n_destinations - 1
    assert np.min(route) == 0


def init_population(pop_size: int) -> List[List[int]]:
    global n_destinations
    pop = [list(range(n_destinations)) for _ in range(pop_size)]
    [random.shuffle(route) for route in pop]

    return pop

def start_task(task: int,  pop_size: int, gens: int) -> Tuple[int, List[int]]:
    
    assert 0 < task <= len(tasks), f"Du må velge enten oppgave 1, 2, 3, eller 4, ikke {task}"
    assert pop_size % 2 == 0, "For enkelhetsskyld bruker man hovedsaklig partall i POP_SIZE. Legg til 1 på POP_SIZE og prøv igjen."
    assert pop_size <= 500, "Maks størrelse på populasjonen er 500"
    assert gens <= 300, "Maks antall generasjoner er 300"

    load_distances(task)
    pop = init_population(pop_size)

    return n_destinations, pop
