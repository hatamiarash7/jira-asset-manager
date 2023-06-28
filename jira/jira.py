import requests
import json
import typer

from jira import utils, config


class JiraAssetHandler:
    def __init__(self, server, pat):
        self.url = server + '/rest/assets/1.0'
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer " + pat
        }

    # Assets

    def get_asset(self, asset_name):
        path = '/object/navlist/aql'
        data = {
            "objectTypeId": config.JIRA_OBJECT,
            "attributesToDisplay": {
                "attributesToDisplayIds": ["155"]
            },
            "page": 1,
            "asc": 1,
            "resultsPerPage": 25,
            "includeAttributes": "false",
            "objectSchemaId": "1",
            "qlQuery": f"Name = \"{asset_name}\""
        }
        return self._make_api_call("POST", path, data)

    def create_asset(self, role, name, sid, status, env, provider, dc, city, os, ip, bgp, katran):
        path = '/object/create'
        data = {
            "objectTypeId": config.JIRA_OBJECT,
            "attributes": [
                {
                    "objectTypeAttributeId": 141,
                    "objectAttributeValues": [{"value": name}]
                },
                {
                    "objectTypeAttributeId": "144",
                    "objectAttributeValues": [{"value": utils.getStatus(status)}]
                },
                {
                    "objectTypeAttributeId": "145",
                    "objectAttributeValues": [{"value": env}]
                },
                {
                    "objectTypeAttributeId": "156",
                    "objectAttributeValues": [{"value": os}]
                },
                {
                    "objectTypeAttributeId": "157",
                    "objectAttributeValues": [{"value": ip}]
                },
                {
                    "objectTypeAttributeId": "150",
                    "objectAttributeValues": [{"value": utils.getBGP(bgp)}]
                },
                {
                    "objectTypeAttributeId": "151",
                    "objectAttributeValues": [{"value": utils.getKatran(katran)}]
                },
                {
                    "objectTypeAttributeId": "152",
                    "objectAttributeValues": [{"value": provider}]
                },
                {
                    "objectTypeAttributeId": "153",
                    "objectAttributeValues": [{"value": dc}]
                },
                {
                    "objectTypeAttributeId": "154",
                    "objectAttributeValues": [{"value": city}]
                },
                {
                    "objectTypeAttributeId": "155",
                    "objectAttributeValues": [{"value": sid}]
                },
                {
                    "objectTypeAttributeId": "158",
                    "objectAttributeValues": [{"value": role}]
                }
            ]
        }
        return self._make_api_call("POST", path, data)

    def update_asset(self, asset_name, attr_name, attr_value):
        if attr_name == 'status':
            attr_value = utils.getStatus(attr_value)
        elif attr_name == 'bgp':
            attr_value = utils.getBGP(attr_value)
        elif attr_name == 'katran':
            attr_value = utils.getKatran(attr_value)

        attr_name = utils.getAttribute(attr_name)

        object = self.get_asset(asset_name)
        id = json.loads(object.text)['matchedFilterValues'][0]['objectId']

        path = f"/object/{id}"
        data = {
            "objectTypeId": config.JIRA_OBJECT,
            "attributes": [
                {
                    "objectTypeAttributeId": attr_name,
                    "objectAttributeValues": [{"value": attr_value}]
                }
            ]
        }
        return self._make_api_call("PUT", path, data)

    # Comments

    def add_comment(self, asset_name, comment):
        object = self.get_asset(asset_name)
        id = json.loads(object.text)['matchedFilterValues'][0]['objectId']

        path = f"/comment/create"
        data = {
            "comment": comment,
            "objectId": f"{id}",
            "role": 0
        }

        return self._make_api_call("POST", path, data)

    # Objects

    def get_schema(self):
        path = '/objectschema/list'
        return self._make_api_call("GET", path, {})

    def get_objecttypes(self, id):
        path = f'/objectschema/{id}/objecttypes/flat'
        return self._make_api_call("GET", path, {})

    def get_attributes(self, objectType):
        path = f'/objecttype/{objectType}/attributes'
        return self._make_api_call("GET", path, {})

    def _make_api_call(self, method, path, data):
        try:
            response = requests.request(
                method,
                self.url + path,
                headers=self.headers,
                data=json.dumps(data)
            )
            return response
        except Exception as e:
            typer.secho(f"API call failed: {str(e)}", fg=typer.colors.YELLOW)
            return None
