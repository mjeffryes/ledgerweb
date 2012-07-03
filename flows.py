import ledger, json, sys, re

accounts = []
regexs = []
if len(sys.argv) == 2:
	accounts = json.loads( sys.argv[1] )
	regexs = [ re.compile(a) for a in accounts ]

journal = ledger.read_journal( "drewr.dat" )

flows = {}
for x in journal.xacts():
	posts = []
	for regex in regexs:
		posts += [(regex.pattern, p.amount) for p in x.posts() if regex.match(p.account.fullname())]
	pos_posts = [ p for p in posts if p[1] > 0 ]
	neg_posts = [ p for p in posts if p[1] < 0 ]
	total_flow = sum( [ amount for (name,amount) in pos_posts ] )
	for (name1, amount1) in pos_posts:
		for (name2, amount2) in neg_posts:
			v = - amount1 * amount2 / total_flow
			if name1 < name2:
				flows[(name1,name2)] = flows.get( (name1,name2), 0 ) + v
			elif name1 > name2:
				flows[(name2,name1)] = flows.get( (name2,name1), 0 ) - v

out={}
out["links"] = [ { "source": accounts.index(n[0]), "target": accounts.index(n[1]), "value": abs(v.to_long()) } for (n,v) in flows.items() ]
print json.dumps( out )

