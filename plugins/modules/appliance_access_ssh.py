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
module: appliance_access_ssh
short_description: Set enabled state of the SSH-based controlled CLI.
description: Set enabled state of the SSH-based controlled CLI.
options:
    enabled:
        description:
        - SSH-based controlled CLI is enabled. This parameter is mandatory.
        required: true
        type: bool
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
        - set
        default: set
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
version_added: 2.0.0
requirements:
- vSphere 7.0.2 or greater
- python >= 3.6
- aiohttp
notes:
- Tested on vSphere 7.0.2
"""

EXAMPLES = r"""
- name: Ensure the SSH access ie enabled
  vmware.vmware_rest.appliance_access_ssh:
    enabled: true
  register: result
"""

RETURN = r"""
# content generated by the update_return_section callback# task: Ensure the SSH access ie enabled
value:
  description: Ensure the SSH access ie enabled
  returned: On success
  sample: 1
  type: int
"""

# This structure describes the format of the data expected by the end-points
PAYLOAD_FORMAT = {
    "set": {"query": {}, "body": {"enabled": "enabled"}, "path": {}}
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

    argument_spec["enabled"] = {"required": True, "type": "bool"}
    argument_spec["state"] = {"type": "str", "choices": ["set"], "default": "set"}

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
    return ("https://{vcenter_hostname}" "/api/appliance/access/ssh").format(**params)


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


async def _set(params, session):
    _in_query_parameters = PAYLOAD_FORMAT["set"]["query"].keys()
    payload = prepare_payload(params, PAYLOAD_FORMAT["set"])
    subdevice_type = get_subdevice_type("/api/appliance/access/ssh")
    if subdevice_type and not params[subdevice_type]:
        _json = await exists(params, session, build_url(params))
        if _json:
            params[subdevice_type] = _json["id"]
    _url = ("https://{vcenter_hostname}" "/api/appliance/access/ssh").format(
        **params
    ) + gen_args(params, _in_query_parameters)
    async with session.get(_url, json=payload, **session_timeout(params)) as resp:
        before = await resp.json()

    async with session.put(_url, json=payload, **session_timeout(params)) as resp:
        try:
            if resp.headers["Content-Type"] == "application/json":
                _json = await resp.json()
        except KeyError:
            _json = {}
        if "value" not in _json:  # 7.0.2
            _json = {"value": _json}

        # The PUT answer does not let us know if the resource has actually been
        # modified
        if resp.status < 300:
            async with session.get(
                _url, json=payload, **session_timeout(params)
            ) as resp_get:
                after = await resp_get.json()
                if before == after:
                    return await update_changed_flag(after, resp_get.status, "get")
        return await update_changed_flag(_json, resp.status, "set")


if __name__ == "__main__":
    import asyncio

    current_loop = asyncio.get_event_loop_policy().get_event_loop()
    current_loop.run_until_complete(main())
