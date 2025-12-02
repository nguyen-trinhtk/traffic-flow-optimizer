from scipy.optimize import linprog
import numpy as np

class LPSolver:
    def __init__(self, A, b, p):
        self.__A = np.array(A)
        self.__b = np.array(b)
        self.__p = np.array(p)

    # ---------------- LE constraints ----------------
    def solveMaxLE(self, bounds=(0, None)):
        res = linprog(-self.__p, A_ub=self.__A, b_ub=self.__b, bounds=bounds, method='highs')
        if res.success:
            return (-res.fun, res.x)
        elif res.status == 3:
            raise Exception("Max LE is unbounded")
        else:
            raise Exception("No solution found")
        
    def solveMinLE(self, bounds=(0, None)):
        res = linprog(self.__p, A_ub=self.__A, b_ub=self.__b, bounds=bounds, method='highs')
        if res.success:
            return (res.fun, res.x)
        elif res.status == 3:
            raise Exception("Min LE is unbounded")
        else:
            raise Exception("No solution found")

    # ---------------- GE constraints ----------------
    def solveMinGE(self, bounds=(0, None)):
        res = linprog(self.__p, A_ub=-self.__A, b_ub=-self.__b, bounds=bounds, method='highs')
        if res.success:
            return (res.fun, res.x)
        elif res.status == 3:
            raise Exception("Min GE is unbounded")
        else:
            raise Exception("No solution found")
        
    def solveMaxGE(self, bounds=(0, None)):
        res = linprog(-self.__p, A_ub=-self.__A, b_ub=-self.__b, bounds=bounds, method='highs')
        if res.success:
            return (-res.fun, res.x)
        elif res.status == 3:
            raise Exception("Max GE is unbounded")
        else:
            raise Exception("No solution found")
