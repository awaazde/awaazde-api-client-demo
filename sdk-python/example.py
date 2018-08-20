from awaazde import AwaazDeAPI, APIException

username = 'nikhil@awaaz.de'
password = 'AD!123'
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
        print awaazde.templates.update(16, update_template)
    except APIException as e:
        print e

    # delete template
    try:
        print awaazde.templates.delete(15)
    except APIException as e:
        print e


def demo_template_language_api():
    pass


if __name__ == "__main__":
    # demo_template_api()
    demo_template_language_api()
