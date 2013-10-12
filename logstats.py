#!/usr/bin/python
# vim: set fileencoding=utf8 :
'''
   Copyright 2013  Gorazd Golob

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.


'''



import time, sys, os, random, getopt


def usage():
    print "logstats.py <arguments>"
    print "logstats.py exports simple statistics of response times given by stdin"
    print "default input stream should include a response times in onlt or in second field separated by coma" 
    print " -h current output"
    print " -d exports also distribution of values in csv"
    # TODO
    #print " -z host=<host> exports zabbix agent format as <host> value <value> " 
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

def read_to_dict():
    # obsolete
    j = {}
    req = {}
    # TODO: loop below should be done more general regardles the data input 
    for onel in sys.stdin:
        # very specific - cvs with two values in place
        both = str.split(onel,',')
        if len(both)>1:
            if len(str(both[0]))>10:
                timez = int(int(both[0])/1000)
            else:
                timez = int(both[0])
            value = to_mil(float(both[1]))
        else:
            value = to_mil(float(onel.rstrip()))
            timez = None
        if value in j.keys():
            j[value] = j[value] + 1
        else:
            j[value] = 1
        if timez in req.keys():
            req[timez] = req[timez] + 1
        else:
            req[timez] = 1
    return {'values':j, 'requests':req}



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

def count_reqs(in_dict):
    i = 0
    max_reqs = 0 
    for k, v in in_dict.iteritems():
        if i == 0:
            min_reqs = v
        if v < min_reqs:
            min_reqs = v
        if v > max_reqs:
            max_reqs = v 
        i += v
    return {'avg':round(float(i)/len(in_dict),2),'min':min_reqs,'max':max_reqs}

def simple_out(resdict, reqsdict):
    print "response times"
    for k in sorted(resdict.iterkeys()):
        try:
            if float(k) > 0:
                outk = 'perc' + str(int (k*100))
        except:
            outk = k
        print outk+','+str(resdict[k])
    if reqsdict != None:
        print "requests per second"
        for k in sorted(reqsdict.iterkeys()):
            print str(k)+','+str(reqsdict[k])
    
def more_out(dicts):
    print "distribution of values - reponse times"
    for k in sorted(dicts['values'].iterkeys()):
        print str(k),',',str(dicts['values'][k])
    
    if len(dicts['requests'])>1:
        print "distribution of values - requests per second"
        for k in sorted(dicts['requests'].iterkeys()):
               print str(k)+','+str(dicts['requests'][k])

# do not forget to cound reqs/sec in similar fasgion as req times with deltas!

if __name__ == "__main__":
    random.seed ('test')

    #generate_data('test.log',1000)

    #new_dict = read_to_array_file('ts-01.prod.log')
    #new_dict = read_to_array_file('test.log')
    distv = False
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
        elif o == '-d':
            distv = True
        else:
            usage()
            sys.exit(2)

    new_dict = read_to_dict()
    res = count_percentiles(new_dict['values'])
    if len(new_dict['requests'])>1:
        reqs = count_reqs(new_dict['requests'])
    else:
        reqs = None
    simple_out(res,reqs)
    if distv:
        more_out(new_dict)
    
    




