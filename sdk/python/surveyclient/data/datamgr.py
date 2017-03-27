# ===============================================================================
#    Copyright (c) 2014 Awaaz.De
#    This file is part of awaaz.de xact api client lib
#
#    @author Nikhil (nikhil@awaaz.de, nikhil.navadiya@gmail.com)
#
# ===============================================================================
import requests
import simplejson as json

BROADCAST_WS_URL = '/multiinputbroadcasts'
WEBHOOK_WS_URL = '/callwebhook'
MULTI_INPUT_RESULT_WS_URL = '/multiinputresults'
MULTI_INPUT_RESULT_SUMMARY_WS_URL = '/multibcastsummaries'


class SurveyMgr(object):
    """
    Surveymgr class to interact with Awaaz.De survey api
    """

    def __init__(self, authdata):
        self.authdata = authdata

    def broadcast_multi_input(self, survey_number, recipients, send_on=None, backup_calls=0):
        """
        Schedule a survey broadcast. Specify the survey by phone number, and date of broadcast. Add recipients by
        specifying a list of 10-digit phone numbers. Get the results from the accompanying results and summary API

        :param recipients: list of recipients by specifying a list of 10-digit phone numbers
        :param send_on: The time in YYYY-MM-DDTHH:MM:SS format for when to schedule this broadcast
        :param backup_calls: Specify the number of retry attempts, up to 2, for this call in case there is no pickup. Defaults to 0
        """

        data = {
            'survey_number': survey_number,
            'recipients': recipients,
            'backup_calls': backup_calls
        }

        if send_on:
            data['send_on'] = send_on

        response = requests.post(self.authdata.getUrl() + BROADCAST_WS_URL + "/", data=data,
                                 auth=(self.authdata.getUsername(), self.authdata.getPassword()))
        if response.status_code == 200:
            templates_data = []
            for template in response.json()['results']:
                templates_data.append(template)

            return templates_data
        else:
            return response.text

    def get_results(self, bcast_id=None, survey_number=None, send_on_from=None, send_on_till=None):
        """
        Broadcast-level statistics on multi-input survey broadcasts. Credits will only be available once the broadcast
        has completed, so you can use it to check whether a bcast has completed or not.
        :param bcast_id: broadcast id (you can filter for multiple with bcast_id={id1}&bcast_id={id2}
        :param survey_number: survey's phone number (you can filter for multiple with survey_number={num1}&survey_number={num2}...
        :param send_on_from: send on from date and time, allows you to filter the calls, optional
        :param send_on_till: send on till date and time, allows you to filter the calls, optional
        :return:
        """
        url = self.authdata.getUrl() + MULTI_INPUT_RESULT_WS_URL + "?"

        if bcast_id:
            url += "bcast_id=" + str(bcast_id) + "&"
        if survey_number:
            url += "survey_number=" + str(survey_number) + "&"
        if send_on_from:
            url += "send_on_from=" + send_on_from + "&"
        if send_on_till:
            url += "send_on_till=" + send_on_till + "&"

        response = requests.get(url, auth=(self.authdata.getUsername(), self.authdata.getPassword()))
        if response.status_code == 200:
            if response.json():
                return response.json()
        return response.text

    def get_results_summary(self, bcast_id=None, survey_number=None, send_on_from=None, send_on_till=None):
        """
        Broadcast-level statistics on multi-input survey broadcasts. Credits will only be available once the broadcast
        has completed, so you can use it to check whether a bcast has completed or not.

        :param bcast_id: broadcast id (you can filter for multiple with bcast_id={id1}&bcast_id={id2}
        :param survey_number: survey's phone number (you can filter for multiple with survey_number={num1}&survey_number={num2}...
        :param send_on_from: send on from date and time, allows you to filter the calls, optional
        :param send_on_till: send on till date and time, allows you to filter the calls, optional
        :return:
        """
        url = self.authdata.getUrl() + MULTI_INPUT_RESULT_SUMMARY_WS_URL + "?"

        if bcast_id:
            url += "bcast_id=" + str(bcast_id) + "&"
        if survey_number:
            url += "survey_number=" + str(survey_number) + "&"
        if send_on_from:
            url += "send_on_from=" + send_on_from + "&"
        if send_on_till:
            url += "send_on_till=" + send_on_till + "&"

        response = requests.get(url, auth=(self.authdata.getUsername(), self.authdata.getPassword()))
        if response.status_code == 200:
            if response.json():
                return response.json()
        return response.text


class WebhookMgr(object):
    """
    Webhook - manage web hooks
    """

    def __init__(self, authdata):
        self.authdata = authdata

    def get_all(self):
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
