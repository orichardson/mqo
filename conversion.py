#Parentheses
def paren(gps):
	return gps[0];

# Arithmetic:
def add(gps):
	return gps[0] + gps[1]
def sub(gps):
	return gps[0] - gps[1]
def mod(gps):
	return gps[0] % gps[1]
def times(gps):
	return gps[0] * gps[1]
def div(gps):
	return gps[0] / gps[1];

# Comparison
def less(gps):
	return gps[0] < gps[1]
def more(gps):
	return gps[0] > gps[1]
def eq(gps):
	return gps[0] == gps[1]
def neq(gps):
	return gps[0] != gps[1]
def geq(gps):
	return gps[0] >= gps[1]
def leq(gps):
	return gps[0] <= gps[1]

EXP = '\s*?$$EXP\d+$$\s*?'
REPLACEMENT_LIST = [('<>', '!='), ('!<', '>='), ('!>', '<=')]


POSSIBLE_EXPRESSIONS = [
	('('+EXP+')', paren),
	(EXP + '\*' + EXP, times),
	(EXP + '%' + EXP, mod),
	(EXP + '/' + EXP, div),
	(EXP + '\+' + EXP, add),
	(EXP + '-' + EXP, sub),
	(EXP + '<' + EXP, less),
	(EXP + '>' + EXP, more),
	(EXP + '==' + EXP, eq),
	(EXP + '!=' + EXP, neq),
	(EXP + '>=' + EXP, geq),
	(EXP + '<=' + EXP, leq)
]
