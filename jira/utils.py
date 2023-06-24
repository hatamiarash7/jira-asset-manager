def getStatus(title: str):
    choices = {
        "running": "2",
        "stopped": "6",
        "in service": "3"
    }
    result = choices.get(title, 'invalid')

    if result != 'invalid':
        return result
    print("Invalid Status")


def getBGP(title: str):
    choices = {
        "active": "1",
        "inactive": "13"
    }
    result = choices.get(title, 'invalid')

    if result != 'invalid':
        return result
    print("Invalid BGP")


def getKatran(title: str):
    choices = {
        "running": "2",
        "stopped": "6"
    }
    result = choices.get(title, 'invalid')

    if result != 'invalid':
        return result
    print("Invalid Katran")


def getAttribute(title: str):
    choices = {
        "name": "141",
        "status": "144",
        "env": "145",
        "os": "156",
        "ip": "157",
        "bgp": "150",
        "katran": "151",
        "provider": "152",
        "dc": "153",
        "city": "154",
        "sid": "155",
        "role": "158"
    }
    result = choices.get(title, 'invalid')

    return result if result != 'invalid' else title
