#===============================================================================
#    Copyright (c) 2014 Awaaz.De
#    This file is part of awaaz.de xact api client lib
#
#    @author Nikhil (nikhil@awaaz.de, nikhil.navadiya@gmail.com)
#
#===============================================================================
import requests

TEMPLATE_WS_URL = '/template'
CALL_WS_URL = '/call'

class TemplateMgr:
    '''
    Template Manager is responsible for dealing with template data
    '''
    def __init__(self, authdata):
        self.authdata = authdata
    
    '''
    returns all templates
    '''
    def getAll(self):
        response = requests.get(self.authdata.getUrl() + TEMPLATE_WS_URL, auth=(self.authdata.getUsername(), self.authdata.getPassword()))
        assert response.status_code == 200
        templates_data = []
        index = 0;
        for template in response.json():
            templates_data.insert(index, template)
            index = index + 1
        
        return templates_data
    
    '''
    returns template detail for given template id
    '''
    def getTemplate(self, id):
        response = requests.get(self.authdata.getUrl() + TEMPLATE_WS_URL + '/' + id, auth=(self.authdata.getUsername(), self.authdata.getPassword()))
        assert response.status_code == 200
        template = None
        if response.json():
            template = response.json()
            
        return template