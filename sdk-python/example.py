from awaazde import AwaazDeAPI


def test():
    username = 'nikhil@awaaz.de'
    password = 'AD!123'
    organization = 'awaazde'

    awaazde = AwaazDeAPI(organization, username, password)

    # list down all templates
    # print awaazde.templates.list()

    # get specific template
    # awaazde.templates.get(14)  # 14 is the id of template


if __name__ == "__main__":
    test()
