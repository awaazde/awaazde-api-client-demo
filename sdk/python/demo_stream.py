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

from streamclient.data.datamgr import GroupMgr

USERNAME = 'your user name'
PASSWORD = 'password'
WS_URL = 'https://awaaz.de/console'

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

    
if __name__ =='__main__':main()

