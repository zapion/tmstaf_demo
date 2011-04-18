#!/usr/bin/env python
#-*- coding: utf-8 -*-
import urllib, urllib2, cookielib
import cPickle
import simplejson as json
import codecs

class plurk(object):
    def __init__( self, file_name):
        self.opener = urllib2.build_opener( urllib2.HTTPCookieProcessor() )
        self.filename = file_name
#       try:
#           self.data = cPickle.load( open( self.filename, 'r' ) )
#       except cPickle.UnpicklingError, EOFError:
#           pass

        
    def set( self, account, password, api_key=None ):
        if api_key == None:
            return 0
        self.data= { 'user' : account, 'password' : password, 'api_key' : api_key }
        return 1

#        self.user = account
#        self.password = password
#        self.api_key = api_key

    def api( self, cmd ):
        return "http://www.plurk.com/API%s" % cmd

    def login(self):
        ( user, password, api_key ) = ( self.data[ 'user' ], self.data[ 'password' ], self.data[ 'api_key' ] )
        fp = self.opener.open( self.api( '/Users/login' ), encode( { 'username' : user,
                                                     'password' : password,
                                                     'api_key' : api_key } ) )
        return json.load( fp )

    def new_plurk( self ):
        import uuid
        fp = self.opener.open( self.api( '/Timeline/plurkAdd' ), encode( { 'content' : uuid.uuid1(), 
                                                                           'qualifier' : 'feels', 
                                                                           'lang' : 'jp',
                                                                           'api_key' : self.data[ 'api_key' ]
                                                                            } ) )
        return json.load( fp )
#--- Requests ----------------------------------------------

#fp = opener.open(get_api_url('/Timeline/plurkAdd'),
#                 encode({'content': 'hello world',
#                                          'qualifier': 'says',
#                                                                   'lang': 'en',
 #                                                                                           'api_key': api_key}))
#print fp.read()

    def reply( self ):
        pass        

    def get_plurk( self, id='all' ):
        if id == 'all':
            return json.load( 
                self.opener.open( self.api( '/Timeline/getPlurks' ), encode( {'api_key' : self.data[ 'api_key' ] } ) )
                )


    def flush(self):
        cPickle.dump( self.data, open( self.filename, 'w' ) )

    def __del__(self):
        self.flush()

def encode( items ):
    encode = urllib.urlencode
    return encode( items )

def connect( dumper ):
## setup properties for connecting plurk api
    fh = open( '/home/sapphirez/keys/plurk.properties', 'r' )
    passwd = fh.readline().strip().split( '=' )[ 1 ]
    api_key = fh.readline().strip().split( '=' )[ 1 ]
    fh.close()
    user = 'tmstaf'
    encode = urllib.urlencode
    

    p = plurk( dumper )
    p.set( user, passwd, api_key )
    return p


def main():
    p = connect( "/tmp/plurk_data" )
    p.login()
    #p.new_plurk()
    res = p.get_plurk()
    save = codecs.open('/tmp/response_plurk', "w", encoding="utf-8")
    string = res['plurks'][15]['content']
    #.encode( 'UTF-8' )
    #string = u'中文'
    #string.encode('UTF-8')
    save.write( string )
    save.close()
    return 0


if __name__ == '__main__':
    import sys
    sys.exit( main() )


#encode = urllib.urlencode


