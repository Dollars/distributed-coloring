# -*-coding:Utf-8 -*

class Backtracking(object):
    def __init__(self, solutionRange, evaluations, showInfo = lambda a,b: 0):
        self.evaluations = evaluations
        self.solutionRange = solutionRange
        self.length = len(solutionRange)
        self.solution = [solutionRange[i][0] for i in range(self.length)]
        self.bestSolution = self.solution
        self.bestScore = self.evaluation()
        
        self.backtrack(0)
        
    def evaluation(self):
        result = 0
        for evaluation in self.evaluations:
            result += evaluation(self.solution)
        return result

    def backtrack(self, index):
        if index < self.length:
            for val in range(self.solutionRange[index][0], self.solutionRange[index][1]+1):
                self.solution[index] = val
                score = self.evaluation()
                if score <= self.bestScore:
                    self.bestSolution = self.solution
                    self.bestScore = score
                self.backtrack(index+1)