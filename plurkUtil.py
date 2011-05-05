#!/usr/bin/env python
#-*- coding: utf-8 -*-
import urllib, urllib2, cookielib
import cPickle
import simplejson as json
import codecs
import logging
import os.path

class plurk(object):
    def __init__( self, file_name):
        self.opener = urllib2.build_opener( urllib2.HTTPCookieProcessor() )
        self.filename = file_name

        
    def set( self, account, password, api_key=None ):
        if api_key == None:
            return 0
        self.data= { 'user' : account, 'password' : password, 'api_key' : api_key }
        return 1

    def api( self, cmd ):
        return "http://www.plurk.com/API%s" % cmd

    def login(self):
        ( user, password, api_key ) = ( self.data[ 'user' ], self.data[ 'password' ], self.data[ 'api_key' ] )
        fp = self.opener.open( self.api( '/Users/login' ), encode( { 'username' : user,
                                                     'password' : password,
                                                     'api_key' : api_key } ) )
        return json.load( fp )

    def new_plurk( self, content=None ):
        if ( content == None ):
            import uuid
            content = uuid.uuid1()
        try:
            fp = self.opener.open( self.api( '/Timeline/plurkAdd' ), encode( { 'content' : content, 
                                                                           'qualifier' : 'feels', 
                                                                           'lang' : 'jp',
                                                                           'api_key' : self.data[ 'api_key' ]
                                                                            } ) )
        except urllib2.URLError, e:
            return ( content, { 'content' : "%s" % e } )
        return ( content, json.load( fp ) )

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
    '''
    setup properties for connecting plurk api
    '''
    props = os.path.expandvars( '$tmstaf_home/TMSTAF-Components/testsuites/plurk_demo/plurk.properties' )
    fh = open( props, 'r' )
    passwd = fh.readline().strip().split( '=' )[ 1 ]
    api_key = fh.readline().strip().split( '=' )[ 1 ]
    fh.close()
    user = 'tmstaf'
    encode = urllib.urlencode

    p = plurk( dumper )
    p.set( user, passwd, api_key )
    return p

##=== Test APIs ===

def test_login():
    '''
    output: string of user_info if login successfully
    '''
    p = connect( "./plurk_data" )
    res = p.login()
    return "%s" % res[ 'user_info' ]

def test_new_plurk( content=None ):
    '''
    input: content for plurk
    output: return 1 if content reponsed equal to original one (success)
            return 0 if not match (fail)
    '''
    p = connect( "./plurk_data" )
    res = p.login()
    ( r_content, res ) = p.new_plurk( content )
    if( content == None ):
        logging.info( "%s" % r_content )
    logging.info( "%s" % res )
#compare responsed content with orginal item
    if( '%s' % r_content == res[ 'content' ] ):
        return 1
    return 0

def test_get_plurk( when ):
    '''
    input: (TODO) to get all plurks in a certain period
    output: plurks which match the search rule
    '''
    p = connect( "./plurk_data" )
    res = p.login()
    res = p.get_plurk()
    logging.info( "%s" % res['plurks'][0] )
    return res['plurks'][0]['content']
    

def main():
    '''
    test program
    '''
    p = connect( "./plurk_data" )
    p.login()
    res = p.get_plurk()
    save = codecs.open('./response_plurk', "w", encoding="utf-8")
    string = res['plurks'][15]['content']
    save.write( string )
    save.close()
    return 0


if __name__ == '__main__':
    import sys
    sys.exit( main() )

