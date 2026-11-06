import itertools

P_B = {1: 0.001}
P_E = {1: 0.002}
P_A = {(0, 0): 0.001, (0, 1): 0.29, (1, 0): 0.94, (1, 1): 0.95}
P_J = {0: 0.05, 1: 0.90}
P_M = {0: 0.01, 1: 0.70}

NAMES = ['B', 'E', 'A', 'J', 'M']

PGMPY = {
    ('B', (('J', 1),)): 0.0162837299,
    ('B', (('J', 1), ('M', 1))): 0.2841718354,
    ('E', (('J', 1), ('M', 1))): 0.1760668384,
    ('A', (('J', 1), ('M', 1))): 0.7606920389,
    ('B', (('J', 1), ('M', 0))): 0.0051298581,
    ('J', (('B', 1),)): 0.8490170000,
}


def pr(p1, x):
    return p1 if x == 1 else 1 - p1


def joint(b, e, a, j, m):
    return (pr(P_B[1], b) * pr(P_E[1], e) * pr(P_A[(b, e)], a)
            * pr(P_J[a], j) * pr(P_M[a], m))


def query(var, evidence):
    total = {0: 0.0, 1: 0.0}
    for combo in itertools.product([0, 1], repeat=5):
        world = dict(zip(NAMES, combo))
        if any(world[k] != v for k, v in evidence.items()):
            continue
        total[world[var]] += joint(*combo)
    return total[1] / (total[0] + total[1])


print(f"query('B', {{'J': 1, 'M': 1}}) = {query('B', {'J': 1, 'M': 1}):.4f}")
print(f"query('J', {{}}) = {query('J', {}):.4f}")
print(f"query('M', {{}}) = {query('M', {}):.4f}")
print(f"query('A', {{}}) = {query('A', {}):.4f}")

for (var, ev), ref in PGMPY.items():
    mine = query(var, dict(ev))
    print(f'P({var}=1 | {dict(ev)}) enum={mine:.10f} pgmpy={ref:.10f} diff={abs(mine - ref):.1e}', abs(mine - ref) < 1e-6)

for ev in [{'A': 1}, {'A': 1, 'E': 1}, {'A': 1, 'E': 0}]:
    print(f'P(B=1 | {ev}) = {query("B", ev):.4f}')

P_A[(0, 0)] = 0.1
print(f"P_A(0,0)=0.1: query('B', {{'J': 1, 'M': 1}}) = {query('B', {'J': 1, 'M': 1}):.4f}")
