import requests
import json
import typer

from jira_amt import config


class JiraAssetHandler:
    def __init__(self, server, pat):
        self.url = server + '/rest/assets/1.0'
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Bearer " + pat
        }

    # ------ Assets ------

    def get_asset(self, schema, object, asset):
        schema_id = config.getSchema(schema)
        path = '/object/navlist/aql'
        data = {
            "objectTypeId": config.getObject(schema_id+":"+schema, object),
            "resultsPerPage": 1,
            "includeAttributes": "false",
            "objectSchemaId": schema_id,
            "qlQuery": f"Name = \"{asset}\""
        }
        return self._make_api_call("POST", path, data)

    def create_asset(self, schema, object, attributes):
        schema_id = config.getSchema(schema)

        input = []

        for attribute_name, value in attributes.items():
            object_type_attribute_id = config.getAttribute(
                object,
                attribute_name
            )

            if object_type_attribute_id is not None and isinstance(value, list):
                output_dict = {
                    "objectTypeAttributeId": object_type_attribute_id,
                    "objectAttributeValues": [{"value": config.getAttributeValue(
                        object,
                        attribute_name,
                        v
                    )} for v in value]
                }

                input.append(output_dict)
            elif object_type_attribute_id is not None:
                output_dict = {
                    "objectTypeAttributeId": object_type_attribute_id,
                    "objectAttributeValues": [{"value": config.getAttributeValue(
                        object,
                        attribute_name,
                        value
                    )}]
                }

                input.append(output_dict)

        path = '/object/create'
        data = {
            "objectTypeId": config.getObject(schema_id+":"+schema, object),
            "attributes": input
        }
        return self._make_api_call("POST", path, data)

    def update_asset(self, schema, object, asset_name, attr_name, attr_value):
        attr_value = config.getAttributeValue(object, attr_name, attr_value)
        attr_name = config.getAttribute(object, attr_name)

        object = self.get_asset(schema, object, asset_name)
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

    # ------ Comments ------

    def add_comment(self, schema, object, asset_name, comment):
        object = self.get_asset(schema, object, asset_name)
        id = json.loads(object.text)['matchedFilterValues'][0]['objectId']

        path = f"/comment/create"
        data = {
            "comment": comment,
            "objectId": f"{id}",
            "role": 0
        }

        return self._make_api_call("POST", path, data)

    # ------ Objects ------

    def get_schema(self):
        path = '/objectschema/list'
        return self._make_api_call("GET", path, {})

    def get_objecttypes(self, id):
        path = f'/objectschema/{id}/objecttypes/flat'
        return self._make_api_call("GET", path, {})

    def get_attributes(self, objectType):
        path = f'/objecttype/{objectType}/attributes'
        return self._make_api_call("GET", path, {})

    # ------ Status ------

    def get_global_statustypes(self):
        path = f'/config/statustype'
        return self._make_api_call("GET", path, {})

    def get_statustypes(self, id):
        path = f'/config/statustype?objectSchemaId={id}'
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
