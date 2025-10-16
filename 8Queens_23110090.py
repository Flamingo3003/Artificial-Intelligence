import pygame
import sys
import time
import heapq
from collections import deque
import tkinter as tk
from tkinter import simpledialog

N = 8
CELL = 60
MARGIN = 30
BOARD_WIDTH = N * CELL
BOARD_HEIGHT = N * CELL
WINDOW_WIDTH = BOARD_WIDTH * 2 + MARGIN * 3
WINDOW_HEIGHT = BOARD_HEIGHT + 200

def is_safe(state, row, col):
    for r, c in enumerate(state):
        if c == col or abs(c - col) == abs(r - row):
            return False
    return True

def dfs_8_queens_steps():
    steps = []
    stack = [[]]
    while stack:
        state = stack.pop()
        steps.append(state)
        if len(state) == N:
            return steps
        row = len(state)
        for col in range(N):
            if is_safe(state, row, col):
                stack.append(state + [col])
    return steps

def bfs_8_queens_steps():
    steps = []
    queue = deque([[]])
    while queue:
        state = queue.popleft()
        steps.append(state)
        if len(state) == N:
            return steps
        row = len(state)
        for col in range(N):
            if is_safe(state, row, col):
                queue.append(state + [col])
    return steps

def ucs_8_queens_steps():
    steps = []
    heap = []
    heapq.heappush(heap, (0, []))
    while heap:
        cost, state = heapq.heappop(heap)
        steps.append(state)
        if len(state) == N:
            return steps
        row = len(state)
        for col in range(N):
            if is_safe(state, row, col):
                heapq.heappush(heap, (cost + 1, state + [col]))
    return steps

def dls_8_queens_steps(limit):
    steps = []
    stack = [(0, [])]
    while stack:
        depth, state = stack.pop()
        steps.append(state)
        if len(state) == N:
            return steps
        if depth < limit:
            row = len(state)
            for col in range(N):
                if is_safe(state, row, col):
                    stack.append((depth + 1, state + [col]))
    return steps

def ids_8_queens_steps():
    all_steps = []
    for depth in range(N + 1):
        steps = []
        stack = [(0, [])]
        while stack:
            d, state = stack.pop()
            steps.append(state)
            if len(state) == N:
                all_steps += steps
                return all_steps
            if d < depth:
                row = len(state)
                for col in range(N):
                    if is_safe(state, row, col):
                        stack.append((d + 1, state + [col]))
        all_steps += steps
    return all_steps

def h(state):
    """Heuristic: số cặp hậu tấn công nhau trong state."""
    conflicts = 0
    for i in range(len(state)):
        for j in range(i + 1, len(state)):
            if state[i] == state[j] or abs(state[i] - state[j]) == abs(i - j):
                conflicts += 1
    return conflicts

def g(state):
    """Cost: số hậu đã đặt lên bàn cờ."""
    return len(state)

def greedy_best_first_8_queens_steps():
    steps = []
    heap = []
    heapq.heappush(heap, (h([]), []))  # (heuristic, state)
    visited = set()
    while heap:
        heuristic, state = heapq.heappop(heap)
        steps.append(state)
        if len(state) == N and h(state) == 0:
            return steps
        row = len(state)
        for col in range(N):
            new_state = state + [col]
            state_tuple = tuple(new_state)
            if state_tuple not in visited and is_safe(state, row, col):
                visited.add(state_tuple)
                heapq.heappush(heap, (h(new_state), new_state))
    return steps

def astar_8_queens_steps():
    steps = []
    heap = []
    heapq.heappush(heap, (g([]) + h([]), [], g([])))  # (f, state, g)
    visited = set()
    while heap:
        f, state, cost = heapq.heappop(heap)
        steps.append(state)
        if len(state) == N and h(state) == 0:
            return steps
        row = len(state)
        for col in range(N):
            new_state = state + [col]
            state_tuple = tuple(new_state)
            if state_tuple not in visited and is_safe(state, row, col):
                visited.add(state_tuple)
                new_g = cost + 1
                new_f = new_g + h(new_state)
                heapq.heappush(heap, (new_f, new_state, new_g))
    return steps


def hill_climbing_8_queens_steps():
    import random
    steps = []
    # Khởi tạo ngẫu nhiên
    state = [random.randint(0, N-1) for _ in range(N)]
    steps.append(state[:])
    while True:
        current_h = h(state)
        found_better = False
        for row in range(N):
            for col in range(N):
                if col != state[row]:
                    new_state = state[:]
                    new_state[row] = col
                    if h(new_state) < current_h:
                        state = new_state
                        steps.append(state[:])
                        found_better = True
                        break
            if found_better:
                break
        if not found_better or h(state) == 0:
            break
    return steps


def beam_search_8_queens_steps(beam_width=3):
    steps = []
    queue = [[]]
    while queue:
        next_queue = []
        for state in queue:
            steps.append(state)
            if len(state) == N and h(state) == 0:
                return steps
            row = len(state)
            children = []
            for col in range(N):
                if is_safe(state, row, col):
                    new_state = state + [col]
                    children.append(new_state)
            # Chọn beam_width trạng thái tốt nhất
            children.sort(key=h)
            next_queue += children[:beam_width]
        queue = next_queue
    return steps

def genetic_8_queens_steps(pop_size=50, generations=1000, mutation_rate=0.2):
    import random
    steps = []
    def random_state():
        return [random.randint(0, N-1) for _ in range(N)]
    def crossover(p1, p2):
        point = random.randint(1, N-2)
        child = p1[:point] + p2[point:]
        return child
    def mutate(state):
        idx = random.randint(0, N-1)
        state[idx] = random.randint(0, N-1)
        return state
    population = [random_state() for _ in range(pop_size)]
    for gen in range(generations):
        population.sort(key=h)
        steps.append(population[0][:])
        if h(population[0]) == 0:
            return steps
        next_gen = population[:pop_size//2]
        while len(next_gen) < pop_size:
            p1, p2 = random.sample(population[:pop_size//2], 2)
            child = crossover(p1, p2)
            if random.random() < mutation_rate:
                child = mutate(child)
            next_gen.append(child)
        population = next_gen
    return steps

def backtracking_8_queens_steps():
    steps = []
    solution = []

    def solve(row):
        if row == N:
            steps.append(solution[:])
            return True
        for col in range(N):
            if is_safe(solution, row, col):
                solution.append(col)
                steps.append(solution[:])
                if solve(row + 1):
                    return True
                solution.pop()
        return False

    solve(0)
    return steps

def forward_checking_8_queens_steps():
    steps = []
    domains = [set(range(N)) for _ in range(N)]
    solution = []

    def forward_check(row):
        if row == N:
            steps.append(solution[:])
            return True
        for col in domains[row].copy():
            if is_safe(solution, row, col):
                solution.append(col)
                steps.append(solution[:])
                removed = []
                for r in range(row + 1, N):
                    for c in domains[r].copy():
                        if c == col or abs(c - col) == abs(r - row):
                            domains[r].remove(c)
                            removed.append((r, c))
                if forward_check(row + 1):
                    return True
                for r, c in removed:
                    domains[r].add(c)
                solution.pop()
        return False

    forward_check(0)
    return steps

def partial_observation_8_queens_steps(partial_state):
    steps = []
    solution = partial_state[:]

    def solve(row):
        if row == N:
            steps.append(solution[:])
            return True
        if row < len(partial_state):
            # Đã biết trước quân hậu ở hàng này
            steps.append(solution[:])
            return solve(row + 1)
        for col in range(N):
            if is_safe(solution, row, col):
                solution.append(col)
                steps.append(solution[:])
                if solve(row + 1):
                    return True
                solution.pop()
        return False

    solve(len(solution))
    return steps

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("8 Queens Algorithms")
font = pygame.font.SysFont(None, 28)
root_tk = tk.Tk()
root_tk.withdraw()



def draw_board(x_offset, state):
    for r in range(N):
        for c in range(N):
            rect = pygame.Rect(x_offset + c * CELL, MARGIN + r * CELL, CELL, CELL)
            color = (240, 240, 240) if (r + c) % 2 == 0 else (180, 180, 180)
            pygame.draw.rect(screen, color, rect)
            if r < len(state) and state[r] == c:
                q_center = (x_offset + c * CELL + CELL // 2, MARGIN + r * CELL + CELL // 2)
                pygame.draw.circle(screen, (200, 0, 0), q_center, CELL // 3)

def draw_button(x, y, text):
    rect = pygame.Rect(x, y, 120, 40)
    pygame.draw.rect(screen, (100, 100, 255), rect)
    label = font.render(text, True, (255, 255, 255))
    screen.blit(label, (x + 10, y + 8))
    return rect

def main():
    algo_steps = []
    current_index = 0
    final_solution = []
    running_algo = False
    skip_mode = False
    no_solution = False
    clock = pygame.time.Clock()

    while True:
        screen.fill((220, 220, 220))
        draw_board(MARGIN, algo_steps[current_index] if algo_steps else [])
        draw_board(MARGIN * 2 + BOARD_WIDTH, final_solution if final_solution else [])

        dfs_btn = draw_button(MARGIN, BOARD_HEIGHT + MARGIN + 20, "DFS")
        bfs_btn = draw_button(MARGIN + 130, BOARD_HEIGHT + MARGIN + 20, "BFS")
        ucs_btn = draw_button(MARGIN , BOARD_HEIGHT + MARGIN + 70, "UCS")
        dls_btn = draw_button(MARGIN + 130, BOARD_HEIGHT + MARGIN + 70, "DLS")
        ids_btn = draw_button(MARGIN + 260, BOARD_HEIGHT + MARGIN + 20, "IDS")
        greedy_btn = draw_button(MARGIN + 260, BOARD_HEIGHT + MARGIN + 70, "Greedy")
        astar_btn = draw_button(MARGIN + 390, BOARD_HEIGHT + MARGIN + 20, "A*")
        hill_btn = draw_button(MARGIN + 520, BOARD_HEIGHT + MARGIN + 20, "Hill")
        beam_btn = draw_button(MARGIN + 390, BOARD_HEIGHT + MARGIN + 70, "Beam")
        genetic_btn = draw_button(MARGIN + 650, BOARD_HEIGHT + MARGIN + 20, "Genetic")
        backtracking_btn = draw_button(MARGIN + 520, BOARD_HEIGHT + MARGIN + 70, "Backtrack")
        forward_checking_btn = draw_button(MARGIN + 780, BOARD_HEIGHT + MARGIN + 20, "F Check")
        partial_observation_btn = draw_button(MARGIN + 650, BOARD_HEIGHT + MARGIN + 70, "Partial Obs")
        step_btn = draw_button(MARGIN + 910, BOARD_HEIGHT + MARGIN + 20, "Steps")
        skip_btn = draw_button(MARGIN + 910, BOARD_HEIGHT + MARGIN + 70, "Skip")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if dfs_btn.collidepoint(mx, my):
                    algo_steps = dfs_8_queens_steps()
                    current_index = 0
                    final_solution = algo_steps[-1]
                    running_algo = True
                    skip_mode = False
                    no_solution = False
                elif bfs_btn.collidepoint(mx, my):
                    algo_steps = bfs_8_queens_steps()
                    current_index = 0
                    final_solution = algo_steps[-1]
                    running_algo = True
                    skip_mode = False
                    no_solution = False
                elif ucs_btn.collidepoint(mx, my):
                    algo_steps = ucs_8_queens_steps()
                    current_index = 0
                    final_solution = algo_steps[-1]
                    running_algo = True
                    skip_mode = False
                    no_solution = False
                elif dls_btn.collidepoint(mx, my):
                    depth = simpledialog.askinteger("Nhập độ sâu", "Nhập giới hạn độ sâu (0–8):", parent=root_tk, minvalue=0, maxvalue=8)
                    if depth is not None:
                        algo_steps = dls_8_queens_steps(limit=depth)
                        current_index = 0
                        if algo_steps and len(algo_steps[-1]) == N:
                            final_solution = algo_steps[-1]
                            no_solution = False
                        else:
                            final_solution = []
                            no_solution = True
                        running_algo = True
                        skip_mode = False
                elif ids_btn.collidepoint(mx, my):
                    algo_steps = ids_8_queens_steps()
                    current_index = 0
                    final_solution = algo_steps[-1]
                    running_algo = True
                    skip_mode = False
                    no_solution = False
                elif greedy_btn.collidepoint(mx, my):
                    algo_steps = greedy_best_first_8_queens_steps()
                    current_index = 0
                    final_solution = algo_steps[-1] if algo_steps and len(algo_steps[-1]) == N else []
                    running_algo = True
                    skip_mode = False
                    no_solution = False
                elif astar_8_queens_steps():
                    algo_steps = astar_8_queens_steps()
                    current_index = 0
                    final_solution = algo_steps[-1] if algo_steps and len(algo_steps[-1]) == N else []
                    running_algo = True
                    skip_mode = False
                    no_solution = False
                elif step_btn.collidepoint(mx, my):
                    for i, s in enumerate(algo_steps):
                        print(f"Step {i}: {s}")
                elif skip_btn.collidepoint(mx, my):
                    skip_mode = True
                elif hill_btn.collidepoint(mx, my):
                    algo_steps = hill_climbing_8_queens_steps()
                    current_index = 0
                    final_solution = algo_steps[-1] if algo_steps and h(algo_steps[-1]) == 0 else []
                    running_algo = True
                    skip_mode = False
                    no_solution = False
                elif beam_btn.collidepoint(mx, my):
                    algo_steps = beam_search_8_queens_steps(beam_width=3)
                    current_index = 0
                    final_solution = algo_steps[-1] if algo_steps and h(algo_steps[-1]) == 0 else []
                    running_algo = True
                    skip_mode = False
                    no_solution = False
                elif genetic_btn.collidepoint(mx, my):
                    algo_steps = genetic_8_queens_steps()
                    current_index = 0
                    final_solution = algo_steps[-1] if algo_steps and h(algo_steps[-1]) == 0 else []
                    running_algo = True
                    skip_mode = False
                    no_solution = False
                elif backtracking_btn.collidepoint(mx, my):
                    algo_steps = backtracking_8_queens_steps()
                    current_index = 0
                    final_solution = algo_steps[-1] if algo_steps and len(algo_steps[-1]) == N else []
                    running_algo = True
                    skip_mode = False
                    no_solution = False
                elif forward_checking_btn.collidepoint(mx, my):
                    algo_steps = forward_checking_8_queens_steps()
                    current_index = 0
                    final_solution = algo_steps[-1] if algo_steps and len(algo_steps[-1]) == N else []
                    running_algo = True
                    skip_mode = False
                    no_solution = False
                elif partial_observation_btn.collidepoint(mx, my):
                    partial_state = [0, 4]  
                    algo_steps = partial_observation_8_queens_steps(partial_state)
                    current_index = 0
                    final_solution = algo_steps[-1] if algo_steps and len(algo_steps[-1]) == N else []
                    running_algo = True
                    skip_mode = False
                    no_solution = False


        if running_algo:
            if skip_mode:
                current_index = len(algo_steps) - 1
                running_algo = False
            else:
                if current_index < len(algo_steps) - 1:
                    current_index += 1
                    time.sleep(0.3)
                else:
                    running_algo = False

        if no_solution:
            warn = font.render("DLS: Không tìm được kết quả trong độ sâu đã nhập!", True, (200, 0, 0))
            screen.blit(warn, (MARGIN, WINDOW_HEIGHT - 80))

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
