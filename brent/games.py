from operator import add, mul, sub
from collections import defaultdict, Counter


class Dice:
    def __init__(self, probabilities):
        if any([not isinstance(k, (int, float)) for k in probabilities.keys()]):
            raise ValueError("Probability keys must be int/float!")
        if any([not isinstance(v, (int, float)) for v in probabilities.values()]):
            raise ValueError("Probability keys must be float!")
        self.probs = defaultdict(int, probabilities)

    def __str__(self):
        return f"<{type(self).__name__} with eyes {min(self.probs.keys())}-{max(self.probs.keys())} at 0x{id(self)}>"

    @property
    def exp(self):
        return sum(p * x for x, p in self.probs.items())

    @property
    def var(self):
        mu = self.exp
        return sum(p * (x - mu) ** 2 for x, p in self.probs.items())

    def __getitem__(self, idx):
        return self.probs[idx]

    def combine(self, other, operator):
        if isinstance(other, int) or isinstance(other, float):
            other = Dice({other: 1})
        new_probs = defaultdict(lambda: 0)
        for x_i, p_i in self.probs.items():
            for x_j, p_j in other.probs.items():
                new_probs[operator(x_i, x_j)] += p_i * p_j
        return Dice(dict(new_probs))

    def __add__(self, other):
        return self.combine(other, operator=add)

    def __mul__(self, other):
        return self.combine(other, operator=mul)

    def __sub__(self, other):
        return self.combine(other, operator=sub)

    def __radd__(self, other):
        return self.combine(other, operator=add)

    def __rmul__(self, other):
        return self.combine(other, operator=mul)

    def __rsub__(self, other):
        return self.combine(other, operator=sub)

    @classmethod
    def make_simple_dice(cls, max_eyes):
        return cls({i: 1 / max_eyes for i in range(1, max_eyes + 1)})

    @classmethod
    def from_string(cls, string):
        cnt = Counter(string)
        total = sum(cnt.values())
        return cls({int(k): v / total for k, v in cnt.items()})


# class DiceGraph:
#     def __init__(self, **kwargs):
#         self.edges = []
#         self.dice_dict = {}
#         for key, value in kwargs:
#             self.dice_dict[key] = value(self.dice_dict)
#
#
# DiceGraph(c1=lambda d: Dice.from_string("01"),
#           d1=lambda d: Dice.make_simple_dice(6),
#           d2=lambda d: d['d1'] + Dice.make_simple_dice(6) * d['d2'],
#           d3=lambda d: d['d2'] + Dice.make_simple_dice(6) * d['d3'],
#           c2=lambda d: d['d1'] + d['d2'] > 10)
#
# pd.DataFrame()
#