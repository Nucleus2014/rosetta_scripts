import sys
fp = open(sys.argv[1],"r")
lines = fp.readlines()
fp.close()
filtered = []
for line in lines:
	if line[2] != ":":
		filtered.append(line)
gp = open("user_report_filtered_" + sys.argv[2] + ".txt","w")
for each in filtered:
	gp.write(each)
gp.close()
