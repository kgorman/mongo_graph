#!/home/kgorman/python/bin/python
#
# rrd grapher functions
#

import sys, os
import settings
sys.path.append(settings.rrdpython_path)
import rrdtool

def create_rrd(n,f,t):
    dstr=[]
    for i,d in enumerate(n):
        d=str(d)
        dstr.append("DS:"+d+":"+t+":960000:U:U")
    fstr=[f,'--step','120','--start','1165708833']
    rrstr=["RRA:MAX:0.5:1:960000"]
    fstr=fstr+dstr+rrstr
    print fstr
    rrdtool.create( *fstr )

def update_rrd(n,v,f,t):
    dstr=''
    for i,d in enumerate(v):
        dstr=dstr+str(int(d))+":"

    dstr=dstr.rstrip(':')
    try:
        if os.path.isfile(f):
            print dstr
            rrdtool.update(f,"N:"+dstr)
        else:
            create_rrd(n,f,t)
    except Exception, e:
      print "Error processing file %s" % f
      print e
