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

from streamclient.data.datamgr import GroupMgr, WebhookMgr

USERNAME = 'your user name'
PASSWORD = 'password'
WS_URL = 'https://awaaz.de/console/streams-api'

def main():
    authdata= AuthData(USERNAME,PASSWORD,WS_URL)
    
    # stream
    
    groupMgr = GroupMgr(authdata)
    
    group_data = {'name': 'test1', 'language': 'eng', 'backup_calls': 2, 'touchtone_max_digits': 0}
    group = groupMgr.create(group_data)

    # update

    group_id = group['id']

    update_group_data = {
        "name": "test2", 
        "language": "hin", 
        "backup_calls": 2, 
        "touchtone_max_digits": 4
    }
    
    print groupMgr.update(group_id, update_group_data)

    # # delete
    print groupMgr.delete(group_id)
    
    
    webhookMgr = WebhookMgr(authdata)
    print "getting all webhooks"
    print webhookMgr.getAll()
    
    print "getting specific webhook"
    print webhookMgr.get(1)
    
    print "creating new webhook"
    print webhookMgr.create('https://awaaz.de/webhook/')
    
    print "updating webhook"
    print webhookMgr.update(9, 'https://awaaz.de/webhook_upd/')
    
    print "deleting webhook"
    print webhookMgr.delete(9)

    
if __name__ =='__main__':main()

