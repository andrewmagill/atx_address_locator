f = open('esri_pcs_to_wkid.txt', 'r')
fout = open('esri_pcs_to_wkid.py', 'w')

h = {}

for line in f.readlines():
    l = line.split('\t')
    try:
        h[l[1]] = l[0]
    except:
        print l

first_line = "pcs_to_wkid = { "
spaces = " " * len(first_line)

hackflag = True

for key, value in h.items():
    if hackflag:
        stuff = first_line
        hackflag = False
    else:
        stuff = "\n" + spaces
    fout.write("%s'%s' : %s," % (stuff, key.replace("\n",""), value))

fout.write('}')
f.close()
fout.close()
