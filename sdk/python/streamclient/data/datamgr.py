#===============================================================================
#    Copyright (c) 2014 Awaaz.De
#    This file is part of awaaz.de xact api client lib
#
#    @author Nikhil (nikhil@awaaz.de, nikhil.navadiya@gmail.com)
#
#===============================================================================
import requests
import simplejson as json

GROUP_WS_URL = '/streams-api/groups'
WEBHOOK_WS_URL = '/callwebhook'


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
        response = requests.get(self.authdata.getUrl() + GROUP_WS_URL, auth=(self.authdata.getUsername(), self.authdata.getPassword()))
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
        response = requests.get(self.authdata.getUrl() + GROUP_WS_URL + '/' + id, auth=(self.authdata.getUsername(), self.authdata.getPassword()))
        if response.status_code == 200:
            template = None
            if response.json():
                template = response.json()
                
            return template
        else:
            return response.text
    
    def create(self, groupdata):
        headers = {'content-type': 'application/json'}
        response = requests.post(self.authdata.getUrl() + GROUP_WS_URL + "/", data=json.dumps(groupdata), headers=headers, auth=(self.authdata.getUsername(), self.authdata.getPassword()))
        if response.status_code == 201:
            group = None
            if response.json():
                group = response.json()
             
            return group
        else:
            return response.text
        
    def update(self, id, groupdata):
        headers = {'content-type': 'application/json'}
        response = requests.put(self.authdata.getUrl() + GROUP_WS_URL + '/' + str(id) + "/", data=json.dumps(groupdata), headers=headers, auth=(self.authdata.getUsername(), self.authdata.getPassword()))
        if response.status_code == 201:
            group = None
            if response.json():
                group = response.json()
                
            return group
        else:
            return response.text

    def delete(self, id):
        headers = {'content-type': 'application/json'}
        response = requests.delete(self.authdata.getUrl() + GROUP_WS_URL + '/' + str(id) + "/", headers=headers, auth=(self.authdata.getUsername(), self.authdata.getPassword()))
        if response.status_code == 204:
            return "true"
        else:
            return response.text
        
        
        
class WebhookMgr:
    '''
    Webhook - creates webhook
    '''
    def __init__(self, authdata):
        self.authdata = authdata
    

    def getAll(self):
        response = requests.get(self.authdata.getUrl() + WEBHOOK_WS_URL, auth=(self.authdata.getUsername(), self.authdata.getPassword()))
        if response.status_code == 200:
            return response.json()['results']
        else:
            return response.text
    
    
    def get(self, id):
        response = requests.get(self.authdata.getUrl() + WEBHOOK_WS_URL + '/' + str(id) + "/", auth=(self.authdata.getUsername(), self.authdata.getPassword()))
        if response.status_code == 200:
            return response.json()
        else:
            return response.text
        
    def create(self, url):
        headers = {'content-type': 'application/json'}
        data = {'url': url}
        response = requests.post(self.authdata.getUrl() + WEBHOOK_WS_URL + "/", data=json.dumps(data), headers=headers, auth=(self.authdata.getUsername(), self.authdata.getPassword()))
        if response.status_code == 201:
            return response.json()
        else:
            return response.text
        
    
    def update(self, id, new_url):
        headers = {'content-type': 'application/json'}
        data = {'url': new_url}
        response = requests.put(self.authdata.getUrl() + WEBHOOK_WS_URL + '/' + str(id) + "/", data=json.dumps(data), headers=headers, auth=(self.authdata.getUsername(), self.authdata.getPassword()))
        if response.status_code == 201:
            return response.json()
        else:
            return response.text
        
    
    def delete(self, id):
        headers = {'content-type': 'application/json'}
        response = requests.delete(self.authdata.getUrl() + WEBHOOK_WS_URL + '/' + str(id) + "/", headers=headers, auth=(self.authdata.getUsername(), self.authdata.getPassword()))
        if response.status_code == 204:
            return "true"
        else:
            return response.text
