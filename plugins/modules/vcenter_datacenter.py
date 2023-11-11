#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2021, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
# template: header.j2
# This module is autogenerated by vmware_rest_code_generator.
# See: https://github.com/ansible-collections/vmware_rest_code_generator
from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = r"""
module: vcenter_datacenter
short_description: Create a new datacenter in the vCenter inventory
description: Create a new datacenter in the vCenter inventory
options:
    datacenter:
        description:
        - Identifier of the datacenter to be deleted. Required with I(state=['absent'])
        type: str
    folder:
        description:
        - Datacenter folder in which the new datacenter should be created.
        type: str
    force:
        description:
        - If true, delete the datacenter even if it is not empty.
        type: bool
    name:
        description:
        - The name of the datacenter to be created. Required with I(state=['present'])
        type: str
    session_timeout:
        description:
        - 'Timeout settings for client session. '
        - 'The maximal number of seconds for the whole operation including connection
            establishment, request sending and response. '
        - The default value is 300s.
        type: float
        version_added: 2.1.0
    state:
        choices:
        - absent
        - present
        default: present
        description: []
        type: str
    vcenter_hostname:
        description:
        - The hostname or IP address of the vSphere vCenter
        - If the value is not specified in the task, the value of environment variable
            C(VMWARE_HOST) will be used instead.
        required: true
        type: str
    vcenter_password:
        description:
        - The vSphere vCenter password
        - If the value is not specified in the task, the value of environment variable
            C(VMWARE_PASSWORD) will be used instead.
        required: true
        type: str
    vcenter_rest_log_file:
        description:
        - 'You can use this optional parameter to set the location of a log file. '
        - 'This file will be used to record the HTTP REST interaction. '
        - 'The file will be stored on the host that run the module. '
        - 'If the value is not specified in the task, the value of '
        - environment variable C(VMWARE_REST_LOG_FILE) will be used instead.
        type: str
    vcenter_username:
        description:
        - The vSphere vCenter username
        - If the value is not specified in the task, the value of environment variable
            C(VMWARE_USER) will be used instead.
        required: true
        type: str
    vcenter_validate_certs:
        default: true
        description:
        - Allows connection when SSL certificates are not valid. Set to C(false) when
            certificates are not trusted.
        - If the value is not specified in the task, the value of environment variable
            C(VMWARE_VALIDATE_CERTS) will be used instead.
        type: bool
author:
- Ansible Cloud Team (@ansible-collections)
version_added: 0.1.0
requirements:
- vSphere 7.0.2 or greater
- python >= 3.6
- aiohttp
notes:
- Tested on vSphere 7.0.2
"""

EXAMPLES = r"""
- name: Get a list of all the datacenters
  register: existing_datacenters
  vmware.vmware_rest.vcenter_datacenter_info:

- name: Force delete the existing DC
  vmware.vmware_rest.vcenter_datacenter:
    state: absent
    datacenter: '{{ item.datacenter }}'
    force: true
  with_items: '{{ existing_datacenters.value }}'
  until:
  - _result is not failed
  retries: 7

- name: Create datacenter my_dc
  vmware.vmware_rest.vcenter_datacenter:
    name: my_dc
    folder: '{{ my_datacenter_folder.folder }}'
"""

RETURN = r"""
# content generated by the update_return_section callback# task: Force delete the existing DC
msg:
  description: Force delete the existing DC
  returned: On success
  sample: All items completed
  type: str
results:
  description: Force delete the existing DC
  returned: On success
  sample:
  - _ansible_item_label:
      datacenter: datacenter-1001
      name: my_dc
    _ansible_no_log: null
    ansible_loop_var: item
    attempts: 1
    changed: 1
    failed: 0
    invocation:
      module_args:
        datacenter: datacenter-1001
        folder: null
        force: 1
        name: null
        session_timeout: null
        state: absent
        vcenter_hostname: vcenter.test
        vcenter_password: VALUE_SPECIFIED_IN_NO_LOG_PARAMETER
        vcenter_rest_log_file: /tmp/vmware_rest.log
        vcenter_username: administrator@vsphere.local
        vcenter_validate_certs: 0
    item:
      datacenter: datacenter-1001
      name: my_dc
    value: {}
  type: list
"""

# This structure describes the format of the data expected by the end-points
PAYLOAD_FORMAT = {
    "create": {"query": {}, "body": {"folder": "folder", "name": "name"}, "path": {}},
    "delete": {
        "query": {"force": "force"},
        "body": {},
        "path": {"datacenter": "datacenter"},
    },
}  # pylint: disable=line-too-long

from ansible.module_utils.basic import env_fallback

try:
    from ansible_collections.cloud.common.plugins.module_utils.turbo.exceptions import (
        EmbeddedModuleFailure,
    )
    from ansible_collections.cloud.common.plugins.module_utils.turbo.module import (
        AnsibleTurboModule as AnsibleModule,
    )

    AnsibleModule.collection_name = "vmware.vmware_rest"
except ImportError:
    from ansible.module_utils.basic import AnsibleModule

from ansible_collections.vmware.vmware_rest.plugins.module_utils.vmware_rest import (
    exists,
    gen_args,
    get_device_info,
    get_subdevice_type,
    open_session,
    prepare_payload,
    session_timeout,
    update_changed_flag,
)


def prepare_argument_spec():
    argument_spec = {
        "vcenter_hostname": dict(
            type="str",
            required=True,
            fallback=(env_fallback, ["VMWARE_HOST"]),
        ),
        "vcenter_username": dict(
            type="str",
            required=True,
            fallback=(env_fallback, ["VMWARE_USER"]),
        ),
        "vcenter_password": dict(
            type="str",
            required=True,
            no_log=True,
            fallback=(env_fallback, ["VMWARE_PASSWORD"]),
        ),
        "vcenter_validate_certs": dict(
            type="bool",
            required=False,
            default=True,
            fallback=(env_fallback, ["VMWARE_VALIDATE_CERTS"]),
        ),
        "vcenter_rest_log_file": dict(
            type="str",
            required=False,
            fallback=(env_fallback, ["VMWARE_REST_LOG_FILE"]),
        ),
        "session_timeout": dict(
            type="float",
            required=False,
            fallback=(env_fallback, ["VMWARE_SESSION_TIMEOUT"]),
        ),
    }

    argument_spec["datacenter"] = {"type": "str"}
    argument_spec["folder"] = {"type": "str"}
    argument_spec["force"] = {"type": "bool"}
    argument_spec["name"] = {"type": "str"}
    argument_spec["state"] = {
        "type": "str",
        "choices": ["absent", "present"],
        "default": "present",
    }

    return argument_spec


async def main():
    required_if = list([])

    module_args = prepare_argument_spec()
    module = AnsibleModule(
        argument_spec=module_args, required_if=required_if, supports_check_mode=True
    )
    if not module.params["vcenter_hostname"]:
        module.fail_json("vcenter_hostname cannot be empty")
    if not module.params["vcenter_username"]:
        module.fail_json("vcenter_username cannot be empty")
    if not module.params["vcenter_password"]:
        module.fail_json("vcenter_password cannot be empty")
    try:
        session = await open_session(
            vcenter_hostname=module.params["vcenter_hostname"],
            vcenter_username=module.params["vcenter_username"],
            vcenter_password=module.params["vcenter_password"],
            validate_certs=module.params["vcenter_validate_certs"],
            log_file=module.params["vcenter_rest_log_file"],
        )
    except EmbeddedModuleFailure as err:
        module.fail_json(err.get_message())
    result = await entry_point(module, session)
    module.exit_json(**result)


# template: default_module.j2
def build_url(params):
    return ("https://{vcenter_hostname}" "/api/vcenter/datacenter").format(**params)


async def entry_point(module, session):
    if module.params["state"] == "present":
        if "_create" in globals():
            operation = "create"
        else:
            operation = "update"
    elif module.params["state"] == "absent":
        operation = "delete"
    else:
        operation = module.params["state"]

    func = globals()["_" + operation]

    return await func(module.params, session)


async def _create(params, session):
    lookup_url = per_id_url = build_url(params)
    uniquity_keys = ["datacenter"]
    comp_func = None

    async def lookup_with_filters(params, session, url):
        # e.g: for the datacenter resources
        if "folder" not in params:
            return
        if "name" not in params:
            return
        async with session.get(
            f"{url}?names={params['name']}&folders={params['folder']}"
        ) as resp:
            _json = await resp.json()
            if isinstance(_json, list) and len(_json) == 1:
                return await get_device_info(session, url, _json[0]["datacenter"])

    _json = None

    if params["datacenter"]:
        _json = await get_device_info(session, build_url(params), params["datacenter"])

    if not _json and (uniquity_keys or comp_func):
        _json = await exists(
            params,
            session,
            url=lookup_url,
            uniquity_keys=uniquity_keys,
            per_id_url=per_id_url,
            comp_func=comp_func,
        )

    if not _json:
        _json = await lookup_with_filters(params, session, build_url(params))

    if _json:
        if "value" not in _json:  # 7.0.2+
            _json = {"value": _json}
        if "_update" in globals():
            params["datacenter"] = _json["id"]
            return await globals()["_update"](params, session)

        return await update_changed_flag(_json, 200, "get")

    payload = prepare_payload(params, PAYLOAD_FORMAT["create"])
    _url = ("https://{vcenter_hostname}" "/api/vcenter/datacenter").format(**params)
    async with session.post(_url, json=payload, **session_timeout(params)) as resp:
        if resp.status == 500:
            text = await resp.text()
            raise EmbeddedModuleFailure(
                f"Request has failed: status={resp.status}, {text}"
            )
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}

        if (resp.status in [200, 201]) and "error" not in _json:
            if isinstance(_json, str):  # 7.0.2 and greater
                _id = _json  # TODO: fetch the object
            elif isinstance(_json, dict) and "value" not in _json:
                _id = list(_json["value"].values())[0]
            elif isinstance(_json, dict) and "value" in _json:
                _id = _json["value"]
            _json_device_info = await get_device_info(session, _url, _id)
            if _json_device_info:
                _json = _json_device_info

        return await update_changed_flag(_json, resp.status, "create")


async def _delete(params, session):
    _in_query_parameters = PAYLOAD_FORMAT["delete"]["query"].keys()
    payload = prepare_payload(params, PAYLOAD_FORMAT["delete"])
    subdevice_type = get_subdevice_type("/api/vcenter/datacenter/{datacenter}")
    if subdevice_type and not params[subdevice_type]:
        _json = await exists(params, session, build_url(params))
        if _json:
            params[subdevice_type] = _json["id"]
    _url = ("https://{vcenter_hostname}" "/api/vcenter/datacenter/{datacenter}").format(
        **params
    ) + gen_args(params, _in_query_parameters)
    async with session.delete(_url, json=payload, **session_timeout(params)) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        return await update_changed_flag(_json, resp.status, "delete")


if __name__ == "__main__":
    import asyncio

    current_loop = asyncio.get_event_loop_policy().get_event_loop()
    current_loop.run_until_complete(main())
