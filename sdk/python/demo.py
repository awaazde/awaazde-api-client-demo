#===============================================================================
#    Copyright (c) 2014 Awaaz.De
#    Sample SDK to call awaaz.de xact api in python
#
#    @author Nikhil (nikhil@awaaz.de, nikhil.navadiya@gmail.com)
#
#===============================================================================


from xactclient.data.datamgr import TemplateMgr
from xactclient.common.authdata import AuthData

USERNAME = 'your username'
PASSWORD = 'password'
WS_URL = 'http://awaaz.de/console/xact'

def main():
    authdata= AuthData(USERNAME,PASSWORD,WS_URL)
    
    templateMgr = TemplateMgr(authdata)
    
    print 'Getting all templates'
    print templateMgr.getAll()
    
    print 'Getting template data with id 1'
    print templateMgr.getTemplate('1')
    
if __name__ =='__main__':main()

