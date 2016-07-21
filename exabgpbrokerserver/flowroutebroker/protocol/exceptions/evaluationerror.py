__author__ = 'markus'


class EvaluationError (Exception):
    def __init__(self):
        self.message = "Syntactic Error detected."
