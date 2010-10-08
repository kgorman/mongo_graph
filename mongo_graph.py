#
# mongo_graph: a mongo -> rrd creation program
# best used with something like drraw for display of the rrd's
# v.5b
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
    def getdata(host,port,name,db):
        port=port+1000  # mongodb always uses this port for stats
        names=[]
        values=[]
        metrics={'avgObjSize':0,'dataSize':0,'storageSize':0,'indexSize':0,'fileSize':0}   # empty structure to hold aggregate stats
        print "%s: gathering %s stats" % (host,name)
        if (name == "disk"):
            # disk stats are trickier, we have to traverse each db adding up the storage usage.
            # get db list
            url="http://%s:%s/admin/$cmd/?filter_listDatabases=1&limit=1" % (host,port)
            try:
               data = json.loads(urllib.urlopen(url).read())
            except:
                print("unable to read url %s") % url
            # for each db, summate the disk usage
            for i in data['rows'][0]['databases']:
              url="http://%s:%s/%s/$cmd/?filter_dbstats=1&limit=1" % (host,port,i['name'])
              print url
              try:
                datas = json.loads(urllib.urlopen(url).read())
                c=0
                for m in metrics.keys():
                    metrics[m] = metrics[m]+datas['rows'][0][m]
                    c+=1
                metrics['avgObjSize'] = metrics['avgObjSize']/c  # this metric is a avg, not pure sum, so special handling
              except:
                print("no data found for url %s") % url
            names = metrics.keys()
            values = metrics.values()
            
        if (name == "repl"):
            url="http://%s:%s/_status?repl=2" % (host,port)
            data = json.loads(urllib.urlopen(url).read())
            mydata=data["serverStatus"]["repl"]["sources"]
            for i in mydata:
                names.append(i['host'].split(':')[0])
                values.append(i['lagSeconds'])
        if (name == "opcounters"):
            url="http://%s:%s/_status" % (host,port)
            data = urllib.urlopen(url).read()
            names = json.loads(data)["serverStatus"]["opcounters"].keys()
            values = json.loads(data)["serverStatus"]["opcounters"].values()
        if (name == "mem"):
            url="http://%s:%s/_status" % (host,port)
            data = urllib.urlopen(url).read()
            names = json.loads(data)["serverStatus"]["mem"].keys()
            values = json.loads(data)["serverStatus"]["mem"].values()
        if (name == "backgroundFlushing"):
            url="http://%s:%s/_status" % (host,port)
            data = urllib.urlopen(url).read()
            names = json.loads(data)["serverStatus"]["backgroundFlushing"].keys()
            values = json.loads(data)["serverStatus"]["backgroundFlushing"].values()
            names.pop(0)    # remove the first item because it's a dict
            values.pop(0)   # remove the first item because it's a dict
        if (name == "connections"):
            url="http://%s:%s/_status" % (host,port)
            data = urllib.urlopen(url).read()
            names = json.loads(data)["serverStatus"]["connections"].keys()
            values = json.loads(data)["serverStatus"]["connections"].values()
           
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
