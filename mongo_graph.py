#
# mongo_graph: a mongo -> rrd creation program
# best used with something like drraw for display of the rrd's
# v.2b
# 2010 Kenny Gorman
#

import settings
import rrd_graph
import urllib
import json
import sys, os, time, socket, commands, signal

class mongoGraph:
    
    def __init__(self):

        self.setSignalHandler()
        self.printStats()
        
    # pull data from web interface
    def getdata(host,port,type,db):
        names=[]
        values=[]
        if (type == 'disk'): 
            url="http://"+host+":28017/"+db+"/$cmd/?filter_dbstats=1&limit=1"
            data = json.loads(urllib.urlopen(url).read())
            names =  data['rows'][0].keys()
            values = data['rows'][0].values()
        if (type == 'repl'):
            url="http://"+host+":28017/_status?repl=2"
            data = json.loads(urllib.urlopen(url).read())
            mydata=data["serverStatus"]["repl"]["sources"]
            for i in mydata:
                names.append(i['host'].split(':')[0])
                values.append(i['lagSeconds'])
        if (type == 'opcounters'):
            url="http://"+host+":28017/_status"
            data = urllib.urlopen(url).read()
            names = json.loads(data)["serverStatus"]["opcounters"].keys()
            values = json.loads(data)["serverStatus"]["opcounters"].values()
        return names,values
        
    def setSignalHandler(self):
          def handler(signal, frame):
            print "Goodbye!"
            sys.exit()
          signal.signal(signal.SIGINT, handler)

    # main loop
    while (1):
        for h,p in settings.hosts.iteritems():
          for gn, gt in settings.metrics.iteritems():
            try:
                file=settings.filepath+"/"+h+"_mongo_stats_"+gn+".rrd"
                n,v=getdata(h,p,gn,'test')
                if n:
                   rrd_graph.update_rrd(n,v,file,gt)
            except socket.herror,info:
                print info
            except IOError,info:
                print "Error: ", info
        time.sleep(30)

if __name__ == "__main__":
    mongoGraph()
