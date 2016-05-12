import query

def omega(q1, q2):
	return Query.overlap(q1, q2)

def greedy(queries):
	while True:
		best = 0
		bl1, bl2 = -1, -1

		for l1 in range(len(queries)):
			for l2 in range(len(queries)) :
				w = omega(queries[l1], queries[l2])
				if (w > best):
					best, bl1, bl2, = w, l1, l2

		if best == 0:
			break;

		q1 = queries.remove(bl1)
		q1 = queries.remove(bl2)
		Q = Query.merge(q1,q2)
		Q.children = [q1,q2]
		queries.append(Q)

	return queries
