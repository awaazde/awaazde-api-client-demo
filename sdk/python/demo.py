#===============================================================================
#    Copyright (c) 2014 Awaaz.De
#    Sample SDK to call awaaz.de xact api in python
#
#    @author Nikhil (nikhil@awaaz.de, nikhil.navadiya@gmail.com)
#
#===============================================================================


from xactclient.data.datamgr import TemplateMgr
from xactclient.data.datamgr import CallMgr
from xactclient.common.authdata import AuthData

USERNAME = 'your username'
PASSWORD = 'password'
WS_URL = 'https://awaaz.de/console/xact'

def main():
    authdata= AuthData(USERNAME,PASSWORD,WS_URL)
    
    templateMgr = TemplateMgr(authdata)
    
    print 'Getting all templates'
    print templateMgr.getAll()
    
    print 'Getting template data with id 1'
    print templateMgr.getTemplate('1')
    
    callMgr = CallMgr(authdata);
    print "Getting all calls"
    callMgr.getAll()
    
    print "Getting call with id 1"
    print callMgr.getCall("1")
    
    #creating new call
    data  = {"recipient":"0123456789", "text":"You have 99 elephants waiting at awaaz","send_on":"2014-01-29T14:32:00"}
    print "Creating a call with data " + str(data)
    print callMgr.create(data)
    
    #updating call
    data  = {"recipient":"9904602242", "text":"You have 99 elephants waiting at awaaz","send_on":"2014-01-29T14:32:00"}
    print "Updating a call with data " + str(data)
    print callMgr.update("5007", data)
    
    print "deleting a call"
    print callMgr.delete("5007")
    
if __name__ =='__main__':main()

