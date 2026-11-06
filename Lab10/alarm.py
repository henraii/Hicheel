import os
import sys
here = os.path.dirname(os.path.abspath(__file__))
sys.path = [p for p in sys.path if os.path.abspath(p or '.') != here]

from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.factors.discrete import TabularCPD, State
from pgmpy.inference import VariableElimination
from pgmpy.sampling import BayesianModelSampling


def rain_model():
    model = DiscreteBayesianNetwork([('Rain', 'WetGrass')])
    cpd_rain = TabularCPD('Rain', 2, [[0.8], [0.2]])
    cpd_wet = TabularCPD('WetGrass', 2, [[0.9, 0.1], [0.1, 0.9]],
                         evidence=['Rain'], evidence_card=[2])
    model.add_cpds(cpd_rain, cpd_wet)
    return model


def alarm_model():
    model = DiscreteBayesianNetwork([('Burglary', 'Alarm'), ('Earthquake', 'Alarm'),
                                     ('Alarm', 'JohnCalls'), ('Alarm', 'MaryCalls')])
    cpd_b = TabularCPD('Burglary', 2, [[0.999], [0.001]])
    cpd_e = TabularCPD('Earthquake', 2, [[0.998], [0.002]])
    cpd_a = TabularCPD('Alarm', 2,
                       [[0.999, 0.71, 0.06, 0.05],
                        [0.001, 0.29, 0.94, 0.95]],
                       evidence=['Burglary', 'Earthquake'], evidence_card=[2, 2])
    cpd_j = TabularCPD('JohnCalls', 2, [[0.95, 0.10], [0.05, 0.90]],
                       evidence=['Alarm'], evidence_card=[2])
    cpd_m = TabularCPD('MaryCalls', 2, [[0.99, 0.30], [0.01, 0.70]],
                       evidence=['Alarm'], evidence_card=[2])
    model.add_cpds(cpd_b, cpd_e, cpd_a, cpd_j, cpd_m)
    return model


def p(infer, var, evidence=None):
    return infer.query([var], evidence=evidence or {}, show_progress=False).values[1]


print('Step 1')
rain = rain_model()
print(rain.check_model())
print(VariableElimination(rain).query(['Rain'], evidence={'WetGrass': 1}))

print('Step 3')
model = alarm_model()
print(model.check_model())
print(model.get_cpds('Alarm'))
print(list(model.nodes()))
print(list(model.edges()))
params = sum(cpd.values.size // 2 for cpd in model.get_cpds())
print('full joint:', 2 ** 5 - 1, 'network:', params)

infer = VariableElimination(model)

print('Step 4')
for var in ['JohnCalls', 'MaryCalls', 'Alarm']:
    print(f'P({var}=1) = {p(infer, var):.4f}')

print('Step 5')
step5 = [
    ('Burglary', {'JohnCalls': 1}),
    ('Burglary', {'JohnCalls': 1, 'MaryCalls': 1}),
    ('Earthquake', {'JohnCalls': 1, 'MaryCalls': 1}),
    ('Alarm', {'JohnCalls': 1, 'MaryCalls': 1}),
    ('Burglary', {'JohnCalls': 1, 'MaryCalls': 0}),
    ('JohnCalls', {'Burglary': 1}),
]
for var, ev in step5:
    print(f'P({var}=1 | {ev}) = {p(infer, var, ev):.10f}')

print('Step 6')
for ev in [{'Alarm': 1}, {'Alarm': 1, 'Earthquake': 1}, {'Alarm': 1, 'Earthquake': 0}]:
    print(f'P(Burglary=1 | {ev}) = {p(infer, "Burglary", ev):.4f}')
print(model.active_trail_nodes('Burglary'))
print(model.active_trail_nodes('Burglary', observed=['Alarm']))
print(model.active_trail_nodes('JohnCalls'))
print(model.active_trail_nodes('JohnCalls', observed=['Alarm']))
print(model.local_independencies('JohnCalls'))
pairs = [('Burglary', 'Earthquake', []), ('Burglary', 'Earthquake', ['Alarm']),
         ('JohnCalls', 'MaryCalls', []), ('JohnCalls', 'MaryCalls', ['Alarm']),
         ('Burglary', 'JohnCalls', ['Alarm'])]
for x, y, obs in pairs:
    print(x, y, obs, 'dependent' if model.is_dconnected(x, y, observed=obs) else 'independent')

print('Step 8')
sampler = BayesianModelSampling(model)
ev = [State('JohnCalls', 1), State('MaryCalls', 1)]
for n in [1000, 10000, 100000]:
    data = sampler.forward_sample(size=n, seed=1, show_progress=False)
    pj = data['JohnCalls'].mean()
    acc = data[(data['JohnCalls'] == 1) & (data['MaryCalls'] == 1)]
    pb = acc['Burglary'].mean() if len(acc) else float('nan')
    print(f'N={n}: P(J=1)={pj:.4f} accepted={len(acc)} P(B=1|J,M)={pb:.4f}')
acc = sampler.rejection_sample(evidence=ev, size=1000, seed=1, show_progress=False)
print('pgmpy rejection_sample 1000 accepted:', len(acc), acc['Burglary'].mean())
