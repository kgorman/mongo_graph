#
# generic settings
#
rrdpython_path='/home/kgorman/rrdtool/lib/python2.6/site-packages/'
hosts={'al02':27017,
       'al01':27017,
       'mdb02.internal.shutterfly.com':27017,
       'mdb01.internal.shutterfly.com':27017
}
metrics={'disk':'GAUGE','opcounters':'COUNTER','repl':'GAUGE'}
filepath='/home/kgorman/apache/cgi-bin/'
