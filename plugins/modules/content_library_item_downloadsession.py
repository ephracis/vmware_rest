from __future__ import absolute_import, division, print_function

__metaclass__ = type
import socket
import json

DOCUMENTATION = """
module: content_library_item_downloadsession
short_description: Handle resource of type content_library_item_downloadsession
description: Handle resource of type content_library_item_downloadsession
options:
  client_error_message:
    description:
    - Client side error message. This can be useful in providing some extra details
      about the client side failure. Note that the message won't be translated to
      the user's locale. Required with I(state=['fail'])
    type: str
  client_token:
    description:
    - 'A unique token generated by the client for each creation request. The token
      should be a universally unique identifier (UUID), for example: {@code b8a2a2e3-2314-43cd-a871-6ede0f429751}.
      This token can be used to guarantee idempotent creation.'
    type: str
  create_spec:
    description:
    - Specification for the new download session to be created. Required with I(state=['create'])
    - 'Validate attributes are:'
    - ' - C(client_progress) (int): The progress that has been made with the download.
      This property is to be updated by the client during the download process to
      indicate the progress of its work in completing the download. The initial progress
      is 0 until updated by the client. The maximum value is 100, which indicates
      that the download is complete.'
    - ' - C(error_message) (dict): If the session is in the {@link State#ERROR} status
      this property will have more details about the error.'
    - ' - C(expiration_time) (str): Indicates the time after which the session will
      expire. The session is guaranteed not to expire before this time.'
    - ' - C(id) (str): The identifier of this download session.'
    - ' - C(library_item_content_version) (str): The content version of the library
      item whose content is being downloaded. This value is the {@link ItemModel#contentVersion}
      at the time when the session is created for the library item.'
    - ' - C(library_item_id) (str): The identifier of the library item whose content
      is being downloaded.'
    - ' - C(state) (str): The state of the download session.'
    type: dict
  download_session_id:
    description:
    - Identifier of the download session whose lifetime should be extended. Required
      with I(state=['cancel', 'delete', 'fail', 'keep_alive'])
    type: str
  progress:
    description:
    - Optional update to the progress property of the session. If specified, the new
      progress should be greater then the current progress. See {@link DownloadSessionModel#clientProgress}.
    type: int
  state:
    choices:
    - cancel
    - create
    - delete
    - fail
    - keep_alive
    description: []
    type: str
  ~action:
    choices:
    - keep-alive
    description:
    - ~action=keep-alive Required with I(state=['keep_alive'])
    type: str
author:
- Ansible VMware team
version_added: 1.0.0
requirements:
- python >= 3.6
"""
IN_QUERY_PARAMETER = ["~action"]
from ansible.module_utils.basic import env_fallback

try:
    from ansible_module.turbo.module import AnsibleTurboModule as AnsibleModule
except ImportError:
    from ansible.module_utils.basic import AnsibleModule
from ansible_collections.vmware.vmware_rest.plugins.module_utils.vmware_rest import (
    gen_args,
    open_session,
    update_changed_flag,
)


def prepare_argument_spec():
    argument_spec = {
        "vcenter_hostname": dict(
            type="str", required=False, fallback=(env_fallback, ["VMWARE_HOST"])
        ),
        "vcenter_username": dict(
            type="str", required=False, fallback=(env_fallback, ["VMWARE_USER"])
        ),
        "vcenter_password": dict(
            type="str",
            required=False,
            no_log=True,
            fallback=(env_fallback, ["VMWARE_PASSWORD"]),
        ),
        "vcenter_certs": dict(
            type="bool",
            required=False,
            no_log=True,
            fallback=(env_fallback, ["VMWARE_VALIDATE_CERTS"]),
        ),
    }
    argument_spec["~action"] = {
        "type": "str",
        "choices": ["keep-alive"],
        "operationIds": ["keep_alive"],
    }
    argument_spec["state"] = {
        "type": "str",
        "choices": ["cancel", "create", "delete", "fail", "keep_alive"],
    }
    argument_spec["progress"] = {"type": "int", "operationIds": ["keep_alive"]}
    argument_spec["download_session_id"] = {
        "type": "str",
        "operationIds": ["cancel", "delete", "fail", "keep_alive"],
    }
    argument_spec["create_spec"] = {"type": "dict", "operationIds": ["create"]}
    argument_spec["client_token"] = {"type": "str", "operationIds": ["create"]}
    argument_spec["client_error_message"] = {"type": "str", "operationIds": ["fail"]}
    return argument_spec


async def get_device_info(params, session, _url, _key):
    async with session.get(((_url + "/") + _key)) as resp:
        _json = await resp.json()
        entry = _json["value"]
        entry["_key"] = _key
        return entry


async def list_devices(params, session):
    existing_entries = []
    _url = url(params)
    async with session.get(_url) as resp:
        _json = await resp.json()
        devices = _json["value"]
    for device in devices:
        _id = list(device.values())[0]
        existing_entries.append((await get_device_info(params, session, _url, _id)))
    return existing_entries


async def exists(params, session):
    unicity_keys = ["bus", "pci_slot_number"]
    devices = await list_devices(params, session)
    for device in devices:
        for k in unicity_keys:
            if (params.get(k) is not None) and (device.get(k) != params.get(k)):
                break
        else:
            return device


async def main():
    module_args = prepare_argument_spec()
    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)
    session = await open_session(
        vcenter_hostname=module.params["vcenter_hostname"],
        vcenter_username=module.params["vcenter_username"],
        vcenter_password=module.params["vcenter_password"],
    )
    result = await entry_point(module, session)
    module.exit_json(**result)


def url(params):
    return "https://{vcenter_hostname}/rest/com/vmware/content/library/item/download-session".format(
        **params
    )


async def entry_point(module, session):
    func = globals()[("_" + module.params["state"])]
    return await func(module.params, session)


async def _cancel(params, session):
    _url = "https://{vcenter_hostname}/rest/com/vmware/content/library/item/download-session/id:{download_session_id}?~action=cancel".format(
        **params
    ) + gen_args(
        params, IN_QUERY_PARAMETER
    )
    async with session.post(_url) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        return await update_changed_flag(_json, resp.status, "cancel")


async def _create(params, session):
    accepted_fields = ["client_token", "create_spec"]
    if "create" == "create":
        _exists = await exists(params, session)
        if _exists:
            return await update_changed_flag({"value": _exists}, 200, "get")
    spec = {}
    for i in accepted_fields:
        if params[i]:
            spec[i] = params[i]
    _url = "https://{vcenter_hostname}/rest/com/vmware/content/library/item/download-session".format(
        **params
    )
    async with session.post(_url, json={"spec": spec}) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        if (
            ("create" == "create")
            and (resp.status in [200, 201])
            and ("value" in _json)
        ):
            if type(_json["value"]) == dict:
                _id = list(_json["value"].values())[0]
            else:
                _id = _json["value"]
            _json = {"value": (await get_device_info(params, session, _url, _id))}
        return await update_changed_flag(_json, resp.status, "create")


async def _delete(params, session):
    _url = "https://{vcenter_hostname}/rest/com/vmware/content/library/item/download-session/id:{download_session_id}".format(
        **params
    ) + gen_args(
        params, IN_QUERY_PARAMETER
    )
    async with session.delete(_url) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        return await update_changed_flag(_json, resp.status, "delete")


async def _fail(params, session):
    accepted_fields = ["client_error_message"]
    if "fail" == "create":
        _exists = await exists(params, session)
        if _exists:
            return await update_changed_flag({"value": _exists}, 200, "get")
    spec = {}
    for i in accepted_fields:
        if params[i]:
            spec[i] = params[i]
    _url = "https://{vcenter_hostname}/rest/com/vmware/content/library/item/download-session/id:{download_session_id}?~action=fail".format(
        **params
    )
    async with session.post(_url, json={"spec": spec}) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        if ("fail" == "create") and (resp.status in [200, 201]) and ("value" in _json):
            if type(_json["value"]) == dict:
                _id = list(_json["value"].values())[0]
            else:
                _id = _json["value"]
            _json = {"value": (await get_device_info(params, session, _url, _id))}
        return await update_changed_flag(_json, resp.status, "fail")


async def _keep_alive(params, session):
    accepted_fields = ["progress"]
    if "keep_alive" == "create":
        _exists = await exists(params, session)
        if _exists:
            return await update_changed_flag({"value": _exists}, 200, "get")
    spec = {}
    for i in accepted_fields:
        if params[i]:
            spec[i] = params[i]
    _url = "https://{vcenter_hostname}/rest/com/vmware/content/library/item/download-session/id:{download_session_id}".format(
        **params
    )
    async with session.post(_url, json={"spec": spec}) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        if (
            ("keep_alive" == "create")
            and (resp.status in [200, 201])
            and ("value" in _json)
        ):
            if type(_json["value"]) == dict:
                _id = list(_json["value"].values())[0]
            else:
                _id = _json["value"]
            _json = {"value": (await get_device_info(params, session, _url, _id))}
        return await update_changed_flag(_json, resp.status, "keep_alive")


if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
