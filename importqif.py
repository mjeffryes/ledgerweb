
import sys


acc_desc = False
curr_account = ""
date = "" 
total = "" 
payee = "" 
other_account = "" 
split_count = 0
split_account = ""
split_desc = ""
split_amount = ""
splits=[]

file = open( sys.argv[1] )
for line in file:

	if line[0] == '^':
		acc_desc = False
		if split_count != 0:
			splits.append( (split_account, split_amount, split_desc) )
			split_account = ""
			split_desc = ""
			split_amount = ""
		if date != "":
			print "%s %s" % ( date, payee )
			if split_count == 0:
				print "\t%s\t%s" % ( other_account, total )
			else:
				for s in splits:
					print "\t%s\t%s	; %s" % s
			print "\t%s" % curr_account 
		date = "" 
		total = "" 
		payee = "" 
		other_account = "" 
		split_count = 0
		splits=[]
		
	elif line.strip() == '!Account':
		acc_desc = True

	elif acc_desc:
		if line[0] == 'N':
			curr_account = line[1:-1]
	else:
		if line[0] == 'D':
			date = line[1:-1].split('/')
			date = '/'.join( [ date[2] , date[0], date[1] ] )

		elif line[0] == 'T':
			total = "$%0.2f" % ( -1 * float(line[1:-1]) )

		elif line[0] == 'P':
			payee = line[1:-1]

		elif line[0] == 'L':
			other_account = line[1:-1]

		elif line[0] == 'S':
			if split_count != 0:
				splits.append( (split_account, split_amount, split_desc) )
				split_account = ""
				split_desc = ""
				split_amount = ""
			split_count += 1;
			split_account = line[1:-1]

		elif line[0] == 'E':
			split_desc = line[1:-1]

		elif line[0] == '$':
			split_amount = "$%0.2f" % ( -1 * float(line[1:-1]) )

