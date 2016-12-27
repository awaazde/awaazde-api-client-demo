# ===============================================================================
#    Copyright (c) 2014 Awaaz.De
#    This file is part of awaaz.de xact api client lib
#
#    @author Nikhil (nikhil@awaaz.de, nikhil.navadiya@gmail.com)
#
# ===============================================================================
import requests
import simplejson as json

GROUP_WS_URL = '/groups'
WEBHOOK_WS_URL = '/callwebhook'
MESSAGE_WS_URL = '/messages'
RESULT_WS_URL = '/bcastresults'


class GroupMgr:
    '''
    GroupMgr Manager is responsible for dealing with groups data
    '''

    def __init__(self, authdata):
        self.authdata = authdata

    '''
    returns all templates
    '''

    def getAll(self):
        response = requests.get(self.authdata.getUrl() + GROUP_WS_URL + "/",
                                auth=(self.authdata.getUsername(), self.authdata.getPassword()))
        if response.status_code == 200:
            templates_data = []
            for template in response.json()['results']:
                templates_data.append(template)

            return templates_data
        else:
            return response.text

    '''
    returns template detail for given template id
    '''

    def get(self, id):
        response = requests.get(self.authdata.getUrl() + GROUP_WS_URL + '/' + id,
                                auth=(self.authdata.getUsername(), self.authdata.getPassword()))
        if response.status_code == 200:
            template = None
            if response.json():
                template = response.json()

            return template
        else:
            return response.text

    def create(self, groupdata):
        headers = {'content-type': 'application/json'}
        response = requests.post(self.authdata.getUrl() + GROUP_WS_URL + "/", data=json.dumps(groupdata),
                                 headers=headers, auth=(self.authdata.getUsername(), self.authdata.getPassword()))
        if response.status_code == 201:
            group = None
            if response.json():
                group = response.json()

            return group
        else:
            return response.text

    def update(self, id, groupdata):
        headers = {'content-type': 'application/json'}
        response = requests.put(self.authdata.getUrl() + GROUP_WS_URL + '/' + str(id) + "/", data=json.dumps(groupdata),
                                headers=headers, auth=(self.authdata.getUsername(), self.authdata.getPassword()))
        if response.status_code == 201:
            group = None
            if response.json():
                group = response.json()

            return group
        else:
            return response.text

    def delete(self, id):
        headers = {'content-type': 'application/json'}
        response = requests.delete(self.authdata.getUrl() + GROUP_WS_URL + '/' + str(id) + "/", headers=headers,
                                   auth=(self.authdata.getUsername(), self.authdata.getPassword()))
        if response.status_code == 204:
            return "true"
        else:
            return response.text

    def add_members(self, id, members):
        """
        Adds members using bulk api
        :param id:
        :param members:
        :return:
        """
        headers = {'content-type': 'application/json'}
        response = requests.post(self.authdata.getUrl() + GROUP_WS_URL + "/" + str(id) + "/memberships/",
                                 data=json.dumps(members),
                                 headers=headers, auth=(self.authdata.getUsername(), self.authdata.getPassword()))
        if response.status_code == 201:
            if response.json():
                return response.json()
        return response.text

    def delete_members(self, id, members):
        """
        Delete members in bulk
        :param id: group id
        :param members: members you would like to delete
        :return:
        """
        headers = {'content-type': 'application/json'}
        response = requests.delete(self.authdata.getUrl() + GROUP_WS_URL + "/" + str(id) + "/memberships/",
                                   data=json.dumps(members),
                                   headers=headers, auth=(self.authdata.getUsername(), self.authdata.getPassword()))
        if response.status_code == 201:
            if response.json():
                return response.json()
        return response.text

    def schedule_call(self, id, message, send_on):
        """
        Schedules the broadcast at specified time
        :param id: group id
        :param message: message file i.e. mp3 or  wav
        :param send_on: send on date and time
        :return:
        """
        message_data = {
            'send_on': send_on,
            'group_id': id,
            'file': message
        }
        files = {'file': open(message, 'rb')}

        response = requests.post(self.authdata.getUrl() + MESSAGE_WS_URL + '/', data=message_data, files=files,
                                 auth=(self.authdata.getUsername(), self.authdata.getPassword()))
        if response.status_code == 201:
            if response.json():
                return response.json()
        return response.text

    def get_results(self, message_id, send_on_from=None, send_on_till=None):
        """
        Call-level results of message broadcasts. When the call was sent, whether it was completed, and a list of any
        user responses (touchtone or voice)
        :param message_id: message id
        :param send_on_from: send on from date and time, allows you to filter the calls, optional
        :param send_on_till: send on till date and time, allows you to filter the calls, optional
        :return:
        """
        url = self.authdata.getUrl() + RESULT_WS_URL + "?"

        if message_id:
            url += "message_id=" + str(message_id) + "&"
        if send_on_from:
            url += "send_on_from=" + send_on_from + "&"
        if send_on_till:
            url += "send_on_till=" + send_on_till + "&"

        response = requests.get(url, auth=(self.authdata.getUsername(), self.authdata.getPassword()))
        if response.status_code == 200:
            if response.json():
                return response.json()
        return response.text


class WebhookMgr:
    '''
    Webhook - creates webhook
    '''

    def __init__(self, authdata):
        self.authdata = authdata

    def getAll(self):
        response = requests.get(self.authdata.getUrl() + WEBHOOK_WS_URL,
                                auth=(self.authdata.getUsername(), self.authdata.getPassword()))
        if response.status_code == 200:
            return response.json()['results']
        else:
            return response.text

    def get(self, id):
        response = requests.get(self.authdata.getUrl() + WEBHOOK_WS_URL + '/' + str(id) + "/",
                                auth=(self.authdata.getUsername(), self.authdata.getPassword()))
        if response.status_code == 200:
            return response.json()
        else:
            return response.text

    def create(self, url):
        headers = {'content-type': 'application/json'}
        data = {'url': url}
        response = requests.post(self.authdata.getUrl() + WEBHOOK_WS_URL + "/", data=json.dumps(data), headers=headers,
                                 auth=(self.authdata.getUsername(), self.authdata.getPassword()))
        if response.status_code == 201:
            return response.json()
        else:
            return response.text

    def update(self, id, new_url):
        headers = {'content-type': 'application/json'}
        data = {'url': new_url}
        response = requests.put(self.authdata.getUrl() + WEBHOOK_WS_URL + '/' + str(id) + "/", data=json.dumps(data),
                                headers=headers, auth=(self.authdata.getUsername(), self.authdata.getPassword()))
        if response.status_code == 201:
            return response.json()
        else:
            return response.text

    def delete(self, id):
        headers = {'content-type': 'application/json'}
        response = requests.delete(self.authdata.getUrl() + WEBHOOK_WS_URL + '/' + str(id) + "/", headers=headers,
                                   auth=(self.authdata.getUsername(), self.authdata.getPassword()))
        if response.status_code == 204:
            return "true"
        else:
            return response.text
