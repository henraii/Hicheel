import os
import sys
here = os.path.dirname(os.path.abspath(__file__))
sys.path = [p for p in sys.path if os.path.abspath(p or '.') != here]

import itertools
from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

P_SLEEP = 0.6
P_STUDY = 0.5
P_EXAM = {(0, 0): 0.1, (0, 1): 0.6, (1, 0): 0.4, (1, 1): 0.9}
P_STRESS = {0: 0.7, 1: 0.2}
NAMES = ['Sleep', 'Study', 'Exam', 'Stress']

model = DiscreteBayesianNetwork([('Sleep', 'Exam'), ('Study', 'Exam'), ('Exam', 'Stress')])
model.add_cpds(
    TabularCPD('Sleep', 2, [[1 - P_SLEEP], [P_SLEEP]]),
    TabularCPD('Study', 2, [[1 - P_STUDY], [P_STUDY]]),
    TabularCPD('Exam', 2,
               [[1 - P_EXAM[k] for k in [(0, 0), (0, 1), (1, 0), (1, 1)]],
                [P_EXAM[k] for k in [(0, 0), (0, 1), (1, 0), (1, 1)]]],
               evidence=['Sleep', 'Study'], evidence_card=[2, 2]),
    TabularCPD('Stress', 2, [[1 - P_STRESS[0], 1 - P_STRESS[1]], [P_STRESS[0], P_STRESS[1]]],
               evidence=['Exam'], evidence_card=[2]),
)
print(model.check_model())
infer = VariableElimination(model)


def pr(p1, x):
    return p1 if x == 1 else 1 - p1


def joint(sl, st, ex, sr):
    return pr(P_SLEEP, sl) * pr(P_STUDY, st) * pr(P_EXAM[(sl, st)], ex) * pr(P_STRESS[ex], sr)


def enum_query(var, evidence):
    total = {0: 0.0, 1: 0.0}
    for combo in itertools.product([0, 1], repeat=4):
        world = dict(zip(NAMES, combo))
        if any(world[k] != v for k, v in evidence.items()):
            continue
        total[world[var]] += joint(*combo)
    return total[1] / (total[0] + total[1])


questions = [
    ('Exam', {}),
    ('Stress', {}),
    ('Study', {'Stress': 1}),
    ('Study', {'Exam': 1}),
    ('Study', {'Exam': 1, 'Sleep': 1}),
    ('Study', {'Exam': 1, 'Sleep': 0}),
]
for var, ev in questions:
    a = infer.query([var], evidence=ev, show_progress=False).values[1]
    b = enum_query(var, ev)
    print(f'P({var}=1 | {ev}) pgmpy={a:.4f} enum={b:.4f}', abs(a - b) < 1e-6)

print(model.active_trail_nodes('Sleep'))
print(model.active_trail_nodes('Sleep', observed=['Exam']))
