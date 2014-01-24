import sophia, tempfile, shutil

methods = ["set", "get", "contains", "delete", "begin", "commit", "rollback"]
itors = ["iterkeys", "itervalues", "iteritems"]

call = lambda db, method: getattr(db, method)

def test_operation_while_closed(path):
	db = sophia.Database()
	db.open(path)
	db.close()
	for m in methods + itors:
		try:
			call(db, m)()
		except sophia.Error:
			pass
		else:
			raise Exception

def test_iter_while_closed(path):
	db = sophia.Database()
	for it in itors:
		db.open(path)
		db.set("foo", "bar")
		cur = call(db, it)()
		db.close()
		assert next(cur)
		del cur

if __name__ == "__main__":
	path = tempfile.mkdtemp()
	try:
		test_operation_while_closed(path)
		test_iter_while_closed(path)
	finally:
		try: shutil.rmtree(path)
		except: pass