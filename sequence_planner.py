import itertools
import random
import heapq
from itertools import permutations




def min_distance_move(source, destination, circumference):
    direct = abs(destination - source)
    reverse = circumference - direct
    return min(direct, reverse)



##################################### Greedy Lookahead ######################################

def greedy_lookahead(current_position, remaining_objects, data_dict, circumference, lookahead):
    if not remaining_objects:
        return [], 0

    if lookahead == 0 or len(remaining_objects) == 1:
        next_obj_id = remaining_objects[0]
        source, destination = data_dict[next_obj_id][0:2]
        total_dist = (min_distance_move(current_position, source, circumference) +
                      min_distance_move(source, destination, circumference))
        return [next_obj_id], total_dist

    best_sequence = None
    min_distance = float('inf')

    for perm in itertools.permutations(remaining_objects[:lookahead]):
        perm_distance = 0
        current_perm_position = current_position
        valid = True
        for obj_id in perm:
            source, destination = data_dict[obj_id][0:2]
            perm_distance += min_distance_move(current_perm_position, source, circumference)
            perm_distance += min_distance_move(source, destination, circumference)
            current_perm_position = destination
            if perm_distance >= min_distance: 
                valid = False
                break

        if valid:
            remaining_after_perm = [obj for obj in remaining_objects if obj not in perm]
            next_sequence, future_distance = greedy_lookahead(current_perm_position, remaining_after_perm, data_dict, circumference, lookahead)
            total_dist = perm_distance + future_distance

            if total_dist < min_distance:
                min_distance = total_dist
                best_sequence = list(perm) + next_sequence

    return best_sequence, min_distance




##################################### Lin-Kernighan ######################################


def calculate_tour_length(tour, data_dict, circumference):
    total_distance = 0
    for i in range(len(tour)):
        source = data_dict[tour[i]][0]
        dest = data_dict[tour[i]][1]
        next_source = data_dict[tour[(i+1) % len(tour)]][0]
        
        total_distance += min_distance_move(source, dest, circumference)
        total_distance += min_distance_move(dest, next_source, circumference)
        
    return total_distance

def generate_initial_tour(data_dict):
    # Generate a random initial tour.
    return random.sample(list(data_dict.keys()), len(data_dict))

def two_opt_swap(tour, i, k):
    # Perform a 2-opt swap by reversing the order of tour between i and k.
    new_tour = tour[:i] + tour[i:k+1][::-1] + tour[k+1:]
    return new_tour

def lin_kernighan(data_dict, circumference):
    # Lin-Kernighan heuristic to solve the TSP problem.
    current_tour = generate_initial_tour(data_dict)
    current_length = calculate_tour_length(current_tour, data_dict, circumference)
    improved = True

    while improved:
        improved = False
        for i in range(1, len(current_tour) - 1):
            for k in range(i+1, len(current_tour)):
                new_tour = two_opt_swap(current_tour, i, k)
                new_length = calculate_tour_length(new_tour, data_dict, circumference)

                if new_length < current_length:
                    current_tour = new_tour
                    current_length = new_length
                    improved = True

    return current_tour, current_length




##################################### Dynamic Programming ######################################


def dp_with_lookahead(data_dict, start_position, circumference, lookahead):
    num_objects = len(data_dict)
    all_visited = (1 << num_objects) - 1  # Bitmask for all objects visited
    dp = [[float('inf')] * num_objects for _ in range(1 << num_objects)]
    backtrack = [[-1] * num_objects for _ in range(1 << num_objects)]
    
    # Map from index to object ID
    object_list = list(data_dict.keys())
    
    # Precompute distances between objects
    dist = [[0] * num_objects for _ in range(num_objects)]
    for i in range(num_objects):
        for j in range(num_objects):
            if i != j:
                source_i, dest_i = data_dict[object_list[i]]
                source_j, dest_j = data_dict[object_list[j]]
                dist[i][j] = (min_distance_move(dest_i, source_j, circumference) + 
                              min_distance_move(source_j, dest_j, circumference))
    
    # Initialize DP table with cost of reaching each object's destination from the start
    for i in range(num_objects):
        source, destination = data_dict[object_list[i]]
        dp[1 << i][i] = min_distance_move(start_position, source, circumference) + min_distance_move(source, destination, circumference)
    
    # Fill the DP table with lookahead optimization
    for mask in range(1 << num_objects):
        for last in range(num_objects):
            if mask & (1 << last) == 0:
                continue

            # Limit the lookahead to a subset of remaining objects
            remaining_objects = [i for i in range(num_objects) if mask & (1 << i) == 0]
            if len(remaining_objects) > lookahead:
                # Sort remaining objects by the distance from the last position and pick the closest ones
                remaining_objects = sorted(remaining_objects, key=lambda i: dist[last][i])[:lookahead]
            
            for next_obj in remaining_objects:
                next_mask = mask | (1 << next_obj)
                new_dist = dp[mask][last] + dist[last][next_obj]
                if new_dist < dp[next_mask][next_obj]:
                    dp[next_mask][next_obj] = new_dist
                    backtrack[next_mask][next_obj] = last
    
    # Find the minimum cost to visit all objects
    min_cost = float('inf')
    last_object = -1
    for i in range(num_objects):
        if dp[all_visited][i] < min_cost:
            min_cost = dp[all_visited][i]
            last_object = i
    
    # Reconstruct the optimal order of objects visited
    optimal_order = []
    mask = all_visited
    while last_object != -1:
        optimal_order.append(object_list[last_object])
        temp = last_object
        last_object = backtrack[mask][last_object]
        mask ^= (1 << temp)
    
    optimal_order.reverse()
    return optimal_order, min_cost



##################################### A* ######################################


def heuristic(unvisited, current_position, data_dict, circumference):
    # Heuristic: Use the minimum distance from current position to the closest unvisited object.
    if not unvisited:
        return 0
    return min(min_distance_move(current_position, data_dict[obj][0], circumference) for obj in unvisited)

def a_star_tsp(data_dict, start_position, circumference):
    # A* algorithm to approximate the TSP-like problem.
    num_objects = len(data_dict)
    object_list = list(data_dict.keys())
    
    # Priority queue for A* search, elements are (g(n) + h(n), g(n), current_position, visited_mask)
    pq = []
    start_mask = 0
    heapq.heappush(pq, (0, 0, start_position, start_mask, []))  # (total_cost, current_cost, current_position, visited_mask, path)

    # Visited states (memoization)
    visited = {}

    while pq:
        total_cost, current_cost, current_position, visited_mask, path = heapq.heappop(pq)

        # Check if all objects are visited
        if visited_mask == (1 << num_objects) - 1:
            return path, current_cost
        
        # Avoid revisiting the same state
        if (current_position, visited_mask) in visited and visited[(current_position, visited_mask)] <= current_cost:
            continue
        visited[(current_position, visited_mask)] = current_cost
        
        # Explore next unvisited objects
        for i, obj_id in enumerate(object_list):
            obj_mask = 1 << i
            if visited_mask & obj_mask:  # Skip already visited objects
                continue
            
            source, destination = data_dict[obj_id]
            new_visited_mask = visited_mask | obj_mask

            # Move to the source and then the destination of the next object
            move_cost = (min_distance_move(current_position, source, circumference) +
                         min_distance_move(source, destination, circumference))
            
            # Calculate heuristic and push to the priority queue
            remaining_unvisited = [object_list[j] for j in range(num_objects) if not (new_visited_mask & (1 << j))]
            heuristic_cost = heuristic(remaining_unvisited, destination, data_dict, circumference)
            heapq.heappush(pq, (current_cost + move_cost + heuristic_cost, current_cost + move_cost, destination, new_visited_mask, path + [obj_id]))

    return [], float('inf')