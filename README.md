# Jira Asset Manager

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) ![GitHub release (release name instead of tag name)](https://img.shields.io/github/v/release/hatamiarash7/jira-asset-manager?sort=date) ![GitHub](https://img.shields.io/github/license/hatamiarash7/jira-asset-manager)

Manage Jira assets in your code or CLI.

## Requirements

- Python 3.8+

## Install

```bash
poetry install
jira-amt --help
```

## How-to

You need to add these environment variables to use the CLI:

| Variable    | Description                                        |
| ----------- | -------------------------------------------------- |
| JIRA_SERVER | Jira server address like `https://jira.domain.com` |
| JIRA_PAT    | Your personal access token                         |

After setting these variables, you can configure the CLI:

```bash
jira-amt init
```

This command will get everything from your Jira server and save them to `~/.jira` directory for later use. With this data, you don't need to know/use ID of each asset/attribute.

## CLI

There is some commands to manage assets. Check them using the `--help` flag.

### Update assets

You can update asset's attribute using it's name. The script will get the asset id from the name automatically.

```bash
jira-amt attr <schema> <object> <asset name> <attr name> <attr value>
jira-amt attr "ITSM" "Servers" "Server-1" "IP" "1.2.3.4"
```

### Add comment

You can add comment to an asset using it's name. The script will get the asset id from the name automatically.

```bash
jira-amt comment <schema> <object> <asset name> <comment>
jira-amt comment "ITSM" "Servers" "Server-1" "This is a comment"
```

---

## Package

You can use this package in your code to manage Jira assets.

```python
from jira_amt.jira import JiraAssetHandler

jira = JiraAssetHandler(
    server="https://jira.example.com",
    pat="ABCD1234"
)
```

### Get asset

```python
asset = jira.get_asset("schema", "object", "asset's name")
```

### Create asset

```python
input = {
    "Name": "Server-1",
    "Status": "Running",
    "Environment": "Production",
    "OS": "Debian",
    "IP": "1.2.3.4"
}

asset = jira.create_asset("schema", "object", input)
```

## Support 💛

[![Donate with Bitcoin](https://en.cryptobadges.io/badge/micro/bc1qmmh6vt366yzjt3grjxjjqynrrxs3frun8gnxrz)](https://en.cryptobadges.io/donate/bc1qmmh6vt366yzjt3grjxjjqynrrxs3frun8gnxrz) [![Donate with Ethereum](https://en.cryptobadges.io/badge/micro/0x0831bD72Ea8904B38Be9D6185Da2f930d6078094)](https://en.cryptobadges.io/donate/0x0831bD72Ea8904B38Be9D6185Da2f930d6078094)

[![ko-fi](https://www.ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/D1D1WGU9)

<div><a href="https://payping.ir/@hatamiarash7"><img src="https://cdn.payping.ir/statics/Payping-logo/Trust/blue.svg" height="128" width="128"></a></div>

## Contributing 🤝

Don't be shy and reach out to us if you want to contribute 😉

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
