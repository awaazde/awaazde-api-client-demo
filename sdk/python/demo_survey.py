# ===============================================================================
#    Copyright (c) 2014 Awaaz.De
#    Sample SDK to call awaaz.de xact api in python
#
#    @author Nikhil (nikhil@awaaz.de, nikhil.navadiya@gmail.com)
#
# ===============================================================================


from surveyclient.data.datamgr import SurveyMgr, WebhookMgr
from xactclient.common.authdata import AuthData

USERNAME = 'your username'
PASSWORD = 'your password'
WS_URL = 'https://awaaz.de/console/surveys-api'


def main():
    auth_data = AuthData(USERNAME, PASSWORD, WS_URL)
    survey_mgr = SurveyMgr(auth_data)

    # sending new broadcast - assuming your survey account is already setup
    print "Sending broadcast:"
    print survey_mgr.broadcast_multi_input(survey_number="7966217942", recipients=["9904602242"])

    # getting detailed results for survey
    print "Getting results for survey number: " + "7966217942"
    print survey_mgr.get_results(survey_number="7966217942")

    # getting detailed results for individual blast
    print "Getting results for broadcast: " + "228614"
    print survey_mgr.get_results(bcast_id="228614")

    # getting result summary for survey number
    print "Getting result summary for survey number: " + "7966217942"
    print survey_mgr.get_results_summary(survey_number="7966217942")

    # getting result summary for broadcast
    print "Getting result summary for broadcast: " + "228614"
    print survey_mgr.get_results_summary(bcast_id="228614")


if __name__ == '__main__': main()
