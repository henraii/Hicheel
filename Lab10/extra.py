import os
import sys
here = os.path.dirname(os.path.abspath(__file__))
sys.path = [p for p in sys.path if os.path.abspath(p or '.') != here]

from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination


def p(infer, var, evidence):
    return infer.query([var], evidence=evidence, show_progress=False).values[1]


print('Sprinkler')
sprinkler = DiscreteBayesianNetwork([('Cloudy', 'Sprinkler'), ('Cloudy', 'Rain'),
                                     ('Sprinkler', 'WetGrass'), ('Rain', 'WetGrass')])
sprinkler.add_cpds(
    TabularCPD('Cloudy', 2, [[0.5], [0.5]]),
    TabularCPD('Sprinkler', 2, [[0.5, 0.9], [0.5, 0.1]], evidence=['Cloudy'], evidence_card=[2]),
    TabularCPD('Rain', 2, [[0.8, 0.2], [0.2, 0.8]], evidence=['Cloudy'], evidence_card=[2]),
    TabularCPD('WetGrass', 2,
               [[1.0, 0.1, 0.1, 0.01],
                [0.0, 0.9, 0.9, 0.99]],
               evidence=['Sprinkler', 'Rain'], evidence_card=[2, 2]),
)
print(sprinkler.check_model())
infer = VariableElimination(sprinkler)
print(f"P(Rain=1 | WetGrass=1) = {p(infer, 'Rain', {'WetGrass': 1}):.4f}")
print(f"P(Rain=1 | WetGrass=1, Sprinkler=1) = {p(infer, 'Rain', {'WetGrass': 1, 'Sprinkler': 1}):.4f}")
print(sprinkler.active_trail_nodes('Sprinkler'))
print(sprinkler.active_trail_nodes('Sprinkler', observed=['Cloudy']))
print(sprinkler.is_dconnected('Sprinkler', 'Rain', observed=['Cloudy']))

print('Naive Bayes')
nb = DiscreteBayesianNetwork([('Spam', 'Free'), ('Spam', 'Link'), ('Spam', 'Meeting')])
nb.add_cpds(
    TabularCPD('Spam', 2, [[0.7], [0.3]]),
    TabularCPD('Free', 2, [[0.9, 0.3], [0.1, 0.7]], evidence=['Spam'], evidence_card=[2]),
    TabularCPD('Link', 2, [[0.8, 0.4], [0.2, 0.6]], evidence=['Spam'], evidence_card=[2]),
    TabularCPD('Meeting', 2, [[0.6, 0.95], [0.4, 0.05]], evidence=['Spam'], evidence_card=[2]),
)
print(nb.check_model())
ev = {'Free': 1, 'Link': 1, 'Meeting': 0}
print(f'pgmpy P(Spam=1 | F=1, L=1, M=0) = {p(VariableElimination(nb), "Spam", ev):.4f}')
spam = 0.3 * 0.7 * 0.6 * 0.95
ham = 0.7 * 0.1 * 0.2 * 0.6
print(f'hand: {spam:.5f} / ({spam:.5f} + {ham:.5f}) = {spam / (spam + ham):.4f}')
