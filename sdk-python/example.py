from awaazde import AwaazDeAPI, APIException

username = 'nikhil@awaaz.de'
password = 'your password'
organization = 'awaazde'
awaazde = AwaazDeAPI(organization, username, password)


def demo_template_api():
    """
    # Template API
    """
    # list down all templates
    print awaazde.templates.list()

    # get specific template
    print awaazde.templates.get(1)  # 1 is the id of template

    # create new template
    # advance options
    phone_numbers = ['+917961344101']
    advanced_options = [
        {"option": "response_type", "value": "voice"},
        {"option": "num_backups", "value": 0},
        {"option": "max_touchtone_retries", "value": 3},
        {"option": "phone_numbers", "value": ",".join(phone_numbers)}]

    new_template = {
        "name": "Welcome Message1",
        "description": "This template is for sending welcome calls to beneficiaries",
        "medium": "voice",
        "advanced_options": advanced_options
    }
    try:
        print awaazde.templates.create(new_template)
    except APIException as e:
        print e

    # try to update template
    update_template = {
        "name": "Welcome Message11",
        "description": "This template is for sending welcome calls to beneficiaries"
    }
    try:
        print awaazde.templates.update(1, update_template)
    except APIException as e:
        print e

    # delete template
    try:
        print awaazde.templates.delete(1)
    except APIException as e:
        print e

    # get template reports
    print awaazde.templates.get_reports(1)

    # get template statistics
    print awaazde.templates.get_statistics(1)


def demo_content_api():
    """
    # Content API
    """
    # list down all contents
    print awaazde.contents.list()

    # get specific content
    print awaazde.contents.get(1)  # 1 is the id of content

    # create new content
    new_content = {
        'type': 1,
        'name': '1',
        'file': '1.wav'
    }
    try:
        print awaazde.contents.create(new_content)
    except APIException as e:
        print "Error occurred: " + str(e)

    # try to update content
    content = {
        "name": "2",
        "description": "content file"
    }
    try:
        print awaazde.contents.update(1, content)
    except APIException as e:
        print "Error occurred: " + str(e)

    # delete content
    try:
        print awaazde.contents.delete(1)
    except APIException as e:
        print "Error occurred: " + str(e)


def demo_template_language_api():
    """
    # Template language API
    """
    # list down all languages
    print awaazde.template_languages.list()

    # get specific language
    print awaazde.template_languages.get(1)  # 1 is the id of language

    # create new language
    language = {
        'template': {'id': 16},
        'language': 'gu',
        'syntax': 'one _N_ two _W_',
        'content': [{'id': 24}, {'id': 25}, {'id': 26}]
    }
    try:
        print awaazde.template_languages.create(language)
    except APIException as e:
        print "Error occurred: " + str(e)

    # update language
    language = {
        'template': {'id': 16},
        'language': 'en'
    }
    try:
        print awaazde.template_languages.update(2, language)
    except APIException as e:
        print "Error occurred: " + str(e)

    # delete language
    try:
        print awaazde.template_languages.delete(2)
    except APIException as e:
        print "Error occurred: " + str(e)


def demo_message_api():
    """
    # Message API
    """
    # list down all messages
    # print awaazde.messages.list()

    # search messages - by language
    print awaazde.messages.list(templatelanguage=1)

    # search messages - by recipient_phone_number
    print awaazde.messages.list(recipient_phone_number="+918888888888")

    # get specific message
    print awaazde.messages.get(1)  # 1 is the id of message

    # create new message
    message = {
        'templatelanguage': 1,
        'phone_number': '+919904602242',
        'values': ['test2'],
        'tags': ['ad']
    }
    try:
        print awaazde.messages.create(message)
    except APIException as e:
        print "Error occurred: " + str(e)

    # update message
    message = {
        'phone_number': '+919999999999',
        'values': ['test2'],
        'tags': ['ad2']
    }
    try:
        print awaazde.messages.update(9, message)
    except APIException as e:
        print "Error occurred: " + str(e)

    # delete message
    try:
        print awaazde.messages.delete(9)
    except APIException as e:
        print "Error occurred: " + str(e)


if __name__ == "__main__":
    demo_template_api()
    demo_content_api()
    demo_template_language_api()
    demo_message_api()
