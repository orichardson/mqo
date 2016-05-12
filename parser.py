import sys, re
# this is for using z3 properly.
sys.path.insert(0,'../z3/build')

from z3 import *
import conversion
import query
import greedy
import utils

# Need types for tables; lead to z3 functions.
# This can be grabbed from an actual sql table.
COL_DATA = {'A': Int, 'B': Int, 'C': Int}


# parsing for SELECT
# Returns a list of z3 variables with the proper types, and names of aliases.
def parse_select(sql):
	# lazy way: they're all reals, without aliasing.
	# return [x.strip() for x in sql.split(',') ]

	#Better way: aliases are taken care of;
	result = []
	for x in sql.split(','):
		x = x.strip()
		index = (x+' ').find(' ')
		#Can't be global in the future.
		if (index < len(x)) :
			COL_DATA[x[index+1:]] = x[:index]
			result.append(x[:index])
	return result

# Parsing for WHERE clause
# returns a z3 solver
def parse_where(sql, tablenname):
	for row in REPLACEMENT_LIST:
		sql = sql.replace(row[0], row[1])

	#We're going to use bottom up parsing from this point forwards.
	# First replace varaibles:
	varor = '([\s^](%s)[\s$])' % ('|'.join(COL_DATA.keys()))
	express = []

	search_result = re.search(varor, sql)

	while(search_result) :
		sql = sql[:search_result.start()] +'$$EXP%d$$'%len(express) + sql[search_result.end():]
		#Instantiate z3 variable
		express.append(COL_DATA[search_result.group(0)]())
		search_result = re.search(varor,sql)

	for (patt, fun) in POSSIBLE_EXPRESSIONS:
		search_result = re.search(patt, sql)
		while(search_result):
			sql = sql[:search_result.start()] +'$$EXP%d$$'%len(express) + sql[search_result.end():]
			express.append(fun(search_result.groups()))
			search_result = re.search(patt, sql)
			print('INTERMEDIATE: '+sql)

	s = Solver()
	s.add(express[-1]) #assume that the last expression captured the whole thing.
	return s;

# Parsing for FROM clause
# TODO: Needs to handle joins.
# For now, just returns the table name.
def parse_from(sql):
	return sql

#SELECT A from Table where A < 10
# If the method was given no argument, let people type their own queries.
if len(sys.argv) == 1:
	print('press Ctrl+D to exit.')
	while True:
		queries = []

		while True:
			query = input('[Q%d or \"go\"] > ' % (len(queries)+1))
			if  query == 'go' :
				break

			# query = select [A a,B as b, C] from [T inner join R] (where [...] )
			#	TODO:(Group by [... ] (having [...]))
			sel,fro,whe = extract_all(query)

			fields = parse_select(sel)
			table = parse_from(fro)
			expr = parse_where(whe, table)
			queries.append(Query(fields, table, expr))

		# Now we have queries! Now we just need to do the real work.
		Q = greedy(queries)
