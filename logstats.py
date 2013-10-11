#!/usr/bin/python
# vim: set fileencoding=utf8 :

import time, sys, os, random


def generate_data(outf, lines):
    try:
        fsock = open(outf, 'w')
    except OSError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
    finally:
        for i in range(lines):
		
            
            line = str(time.time()) + ',' + str(random.randrange(0,978,1)) + '\n'
            #print line
	    fsock.write(line)
        
        fsock.close()


def to_mil(i):
    if int(i) != i:
         i = (i*1000)
    return int(i)

def read_to_array(inf):
    try:
        fsock = open (inf,"rb", 0)
    except OSError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)
    finally: 
        onel = fsock.readline()
        j = {}
        while onel:
            # very specific - cvs with two values in place
            both = str.split(onel,',')
            if len(both)>1:
                 value = to_mil(float(both[1]))
            else:
                 value = to_mil(float(onel.rstrip()))
            if value in j.keys():
                j[value] = j[value] + 1
            else:
                j[value] = 1

            onel = fsock.readline()
        fsock.close()	
    return j


def count_percentiles(in_dict):
    sum_all = 0
    sum_favg = 0
    i = 0
    mini = 0
    perc = {0.5:0, 0.75:0, 0.85:0, 0.95:0, 0.99:0, 1:0}
    for k, v in in_dict.iteritems():
        sum_all = sum_all+v
        sum_favg = sum_favg + (k*v)
    for k in sorted(in_dict.iterkeys()):
        if i == 0:
            mini = k
        v = in_dict[k]
	i = i + v
	for kp, vp in perc.iteritems():
	    if ((sum_all * kp) == i) or (((sum_all * kp) > (i - v)) and ((sum_all * kp) < (i))):
                perc[kp] = k
    perc["min"] = mini
    perc["avg"] = sum_favg / len(in_dict)
    return perc

# do not forget to cound reqs/sec in similar fasgion as req times with deltas!

if __name__ == "__main__":
    random.seed ('test')

    #generate_data('test.log',1000)

    new_dict = read_to_array('ts-01.prod.log')
    #new_dict = read_to_array('test.log')
    print new_dict
    print "\n"
    res = count_percentiles(new_dict)
    print res
    
    




