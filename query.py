class Query:
	def __init__(self, cols, table, constrs):
		self.cols = cols
		self.table = table
		self.constr = constrs

	def isSuperset(self, other):
		if(not (set(other.cols) <= set(self.cols) )) :
			return False

		s = Solver()
		s.add(Not(self.constr))
		s.add(other.constr)
		return not s.check()

	def merge(q1, q2):
		return Query([set(q1.cols)|set(q2.cols)], q1.table, Or(q1.constrs, q2.constrs) );

	def overlap(q1, q2):
		if q1.isSuperset(q2) or q2.isSuperset(q1):
			return 1
		return 0
