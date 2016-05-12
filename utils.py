import re

def find_between_keys(s, first, last):
	return re.search('.*((?i)%s)(.*?)((?i)%s).*' % (first,last) , s).group(2).strip()

def extract_all(s):
	rslt = re.search( ('((?i)SELECT)\s+(?P<select>.*)\s+'
				'((?i)FROM) (?P<table>.*)\s+'
				'(((?i)WHERE) (?P<where>.*?))?'
				'(\s+((?i)GROUP BY) (?P<gp>.*?))?\s*;'
			), s)
	return rslt.group('select').strip(), rslt.group('table').strip(), rslt.group('where').strip()
