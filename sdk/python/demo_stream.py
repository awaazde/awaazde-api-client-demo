# ===============================================================================
#    Copyright (c) 2014 Awaaz.De
#    Sample SDK to call awaaz.de xact api in python
#
#    @author Nikhil (nikhil@awaaz.de, nikhil.navadiya@gmail.com)
#
# ===============================================================================


from xactclient.common.authdata import AuthData
from streamclient.data.datamgr import GroupMgr, WebhookMgr

USERNAME = 'your username/email'
PASSWORD = 'password'
WS_URL = 'https://awaaz.de/console/streams-api'


def main():
    authdata = AuthData(USERNAME, PASSWORD, WS_URL)

    # stream
    """
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
    """

    """
    To add, delete members in your group
    """
    groupMgr = GroupMgr(authdata)

    # get your group details - id and other stuff
    groups = groupMgr.getAll()
    group = groups[0]  # my first group

    members = {'data': [
        {
            "number": "9904602242",
            "name": "Nikhil"
        },
        {
            "number": "9825643859",
            "name": "Bhaumik Shah"
        }
    ]}

    # removing group members - this will remove all the members specified above
    print groupMgr.delete_members(group['id'], members)

    # adding new members
    print groupMgr.add_members(group['id'], members)

    """
    scheduling the call to group
    """

    # the system will send call on this specified time, please note that A 10-min grace period is automatically
    # added from this time. Actual broadcast time will vary based on system load. Calls will only go out between
    # 8am-10pm of the recipients' day, anything outside of this range will get attempted the next morning 8am.
    # If left blank, defaults to scheduling right now
    send_on = "2016-12-27T14:50:00"  # format should be YYYY-MM-DDTHH:MM:SS
    group_id = group['id']

    # your message audio file, it must be wav or mp3
    message_file = '/home/nikhil/apps/awaazde-api-client-sdk/sdk/python/4.wav'

    print groupMgr.schedule_call(group_id, message_file, send_on)

    # getting the result of broadcast
    # you can get this from above schedule call method response
    message_id = 103747
    # print groupMgr.get_results(message_id)

    """
    Sample code for configuring/managing webhook
    """
    """
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

    """


if __name__ == '__main__': main()
