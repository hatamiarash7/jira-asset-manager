def getStatus(title: str):
    match title:
        case "running": return "2"
        case "stopped": return "6"
        case "in service": return "3"
        case _: print("Invalid Status")


def getBGP(title: str):
    match title:
        case "active": return "1"
        case "inactive": return "13"
        case _: print("Invalid BGP")


def getKatran(title: str):
    match title:
        case "running": return "2"
        case "stopped": return "6"
        case _: print("Invalid Katran")


def getAttribute(title: str):
    match title.lower():
        case "name": return "141"
        case "status": return "144"
        case "env": return "145"
        case "os": return "156"
        case "ip": return "157"
        case "bgp": return "150"
        case "katran": return "151"
        case "provider": return "152"
        case "dc": return "153"
        case "city": return "154"
        case "sid": return "155"
        case "role": return "158"
        case _: return title
