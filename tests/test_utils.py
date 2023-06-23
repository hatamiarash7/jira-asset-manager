from jira import utils


def test_getStatus(capfd):
    assert utils.getStatus("running") == "2"
    assert utils.getStatus("stopped") == "6"
    assert utils.getStatus("in service") == "3"
    assert utils.getStatus("invalid") == None

    out, _ = capfd.readouterr()
    assert out == "Invalid Status\n"


def test_getBGP(capfd):
    assert utils.getBGP("active") == "1"
    assert utils.getBGP("inactive") == "13"
    assert utils.getBGP("invalid") == None

    out, _ = capfd.readouterr()
    assert out == "Invalid BGP\n"


def test_getKatran(capfd):
    assert utils.getKatran("running") == "2"
    assert utils.getKatran("stopped") == "6"
    assert utils.getKatran("invalid") == None

    out, _ = capfd.readouterr()
    assert out == "Invalid Katran\n"


def test_getAttribute():
    assert utils.getAttribute("name") == "141"
    assert utils.getAttribute("status") == "144"
    assert utils.getAttribute("env") == "145"
    assert utils.getAttribute("os") == "156"
    assert utils.getAttribute("ip") == "157"
    assert utils.getAttribute("bgp") == "150"
    assert utils.getAttribute("katran") == "151"
    assert utils.getAttribute("provider") == "152"
    assert utils.getAttribute("dc") == "153"
    assert utils.getAttribute("city") == "154"
    assert utils.getAttribute("sid") == "155"
    assert utils.getAttribute("role") == "158"
    assert utils.getAttribute("invalid") == "invalid"
