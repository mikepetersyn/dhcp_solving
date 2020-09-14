import operator
from functools import reduce


class SATto3SAT:

    def __init__(self, formula, dimacs_dict=None):
        self.sat_formula = formula
        self.dimacs_dict = dimacs_dict
        self.t_sat_formula = []

    def chunks(self, lst, n):
        return [lst[i:i + n] for i in range(0, len(lst), n)]

    def convert(self):
        for i, clause in enumerate(self.sat_formula):
            if len(clause) < 3:
                while len(clause) < 3:
                    clause.append(clause[0])
                self.t_sat_formula.append(clause)
            elif len(clause) == 3:
                self.t_sat_formula.append(clause)
            elif len(clause) == 4:
                a = clause[:2]
                b = clause[-2:]
                if self.dimacs_dict is not None:
                    a.append(1000 * a[-1] + b[0])
                    b.insert(0, a[-1] * -1)
                else:
                    a.append((1000 * a[-1][1] + b[0][1], 1000 * a[-1][1] + b[0][1]))
                    b.insert(0, (a[-1][1] * -1, a[-1][1] * -1))
                self.t_sat_formula.append(a)
                self.t_sat_formula.append(b)
            elif len(clause) > 4:
                a = clause[:2]
                b = self.chunks(clause[2:-2], 1)
                c = clause[-2:]
                if len(b) == 1:
                    b = reduce(operator.concat, b)
                    if self.dimacs_dict is not None:
                        a.append(1000 * a[-1] + b[0])
                        b.insert(0, a[-1] * -1)
                        b.append(1000 * b[-1] + c[0])
                        c.insert(0, b[-1] * -1)
                    else:
                        a.append((1000 * a[-1][1] + b[0][1], 1000 * a[-1][1] + b[0][1]))
                        b.insert(0, (a[-1][1] * -1, a[-1][1] * -1))
                        b.append((1000 * b[-1][1] + c[0][1], 1000 * b[-1][1] + c[0][1]))
                        c.insert(0, (b[-1][1] * -1, b[-1][1] * -1))
                    self.t_sat_formula.append(a)
                    self.t_sat_formula.append(b)
                    self.t_sat_formula.append(c)
                else:
                    for j, literal in enumerate(b):
                        if j == 0:
                            if self.dimacs_dict is not None:
                                a.append(1000 * a[-1] + literal[0])
                                literal.insert(0, (1000 * a[-2] + literal[0]) * -1)
                                literal.append(1000 * literal[-1] + b[j + 1][0])
                            else:
                                a.append((1000 * a[-1][1] + literal[0][1], 1000 * a[-1][1] + literal[0][1]))
                                literal.insert(0, (a[-1][1] * -1, a[-1][1] * -1))
                                literal.append((1000 * literal[-1][1] + b[j + 1][0][1], 1000 * literal[-1][1] + b[j + 1][0][1]))



                        elif j == len(b) - 1:
                            if self.dimacs_dict is not None:
                                literal.insert(0, b[j - 1][-1] * -1)
                                literal.append(1000 * literal[-1] + c[0])
                                c.insert(0, (literal[-1]) * -1)
                            else:
                                literal.insert(0, (b[j - 1][-1][1] * -1, b[j - 1][-1][1] * -1))
                                literal.append((1000 * literal[-1][1] + c[0][1], 1000 * literal[-1][1] + c[0][1]))
                                c.insert(0, (literal[-1][1] * -1, literal[-1][1] * -1))

                        else:
                            if self.dimacs_dict is not None:
                                literal.insert(0, b[j - 1][-1] * -1)
                                literal.append(1000 * literal[-1] + b[j + 1][0])
                            else:
                                literal.insert(0, (b[j - 1][-1][1] * -1, b[j - 1][-1][1] * -1))
                                literal.append((1000 * literal[-1][1] + b[j + 1][0][1], 1000 * literal[-1][1] + b[j + 1][0][1]))

                    self.t_sat_formula.append(a)
                    for clause in b:
                        self.t_sat_formula.append(clause)
                    self.t_sat_formula.append(c)

        return self.t_sat_formula
