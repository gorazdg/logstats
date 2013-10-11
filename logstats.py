#!/usr/bin/python
# vim: set fileencoding=utf8 :

import time, sys, os, random, getopt


def usage():
    print "logstats.py <arguments>"
    print "logstats.py exports simple statistics of response times given by stdin"
    print "default input stream should include a response times in onlt or in second field separated by coma" 
    print " -h current output"
    # TODO
    #print " -z host=<host> exports zabbix agent format as <host> value <value> " 
    #print " -d exports also distribution of values in csv"
    #print " -t include req/s analytics" 
    #print " -d and -t can be combined to export distribution of req/s values"

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

def read_to_array_file(inf):
    # obsolete 

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

def read_to_array():
    # obsolete
    j = {}
    for onel in sys.stdin:
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

    #new_dict = read_to_array_file('ts-01.prod.log')
    #new_dict = read_to_array_file('test.log')

    try:
        opts, args = getopt.getopt(sys.argv[1:], "zhdt", ["host="])
    except getopt.GetoptError as err:
        # print help information and exit:dd
        print err
        usage()
        sys.exit(2)
    for o, a in opts:
        if o == "-h":
            usage()
            sys.exit(0)
        elif o == '-z':
            print 'zabbix mode'
        else:
            usage()
            sys.exit(2)

    new_dict = read_to_array()

    print new_dict
    print "\n"
    res = count_percentiles(new_dict)
    print res
    
    




