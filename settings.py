#
# settings file
#
# This is the path to rrdtool binaries
rrdpython_path='/home/kgorman/rrdtool/lib/python2.6/site-packages/'

# An array of hosts:ports to probe
hosts={'myserver1':27017,
       'myserver2':27017
}

# the metrics to fetch, no other options than listed here
metrics={'disk':'GAUGE','opcounters':'COUNTER','repl':'GAUGE'}

# where to save the rrd files.
filepath='/home/kgorman/apache/cgi-bin/'
