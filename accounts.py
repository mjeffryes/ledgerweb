import ledger, json, sys, re

prefix = ""
if len(sys.argv) == 2:
	prefix = sys.argv[1] + ":"
regex = re.compile(prefix)

bal = {}
journal = ledger.read_journal( "drewr.dat" )
for x in journal.xacts():
	for p in x.posts():
		name = p.account.fullname()
		if regex.match( name ):
			name = prefix + name[len(prefix):].split(":")[0]
			bal[name] = bal.get(name, 0) + p.amount

bal_list = bal.items()

out={}
out["nodes"] = [ { "name": n, "value": abs(v.to_long()), "group": 1 } for (n,v) in bal_list ]
print json.dumps( out )

