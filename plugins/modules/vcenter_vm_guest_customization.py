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
module: vcenter_vm_guest_customization
short_description: Applies a customization specification on the virtual machine
description: Applies a customization specification on the virtual machine in {@param.name
    vm}. The actual customization happens inside the guest when the virtual machine
    is powered on. If there is a pending customization for the virtual machine and
    a new one is set, then the existing customization setting will be overwritten
    with the new settings.
options:
    configuration_spec:
        description:
        - Settings to be applied to the guest during the customization. This parameter
            is mandatory.
        - 'Valid attributes are:'
        - ' - C(windows_config) (dict): Guest customization specification for a Windows
            guest operating system ([''set''])'
        - '   - Accepted keys:'
        - '     - reboot (string): The C(reboot_option) specifies what should be done
            to the guest after the customization.'
        - 'Accepted value for this field:'
        - '       - C(NO_REBOOT)'
        - '       - C(REBOOT)'
        - '       - C(SHUTDOWN)'
        - '     - sysprep (object): Customization settings like user details, administrator
            details, etc for the windows guest operating system. Exactly one of C(#sysprep)
            or C(#sysprep_xml) must be specified.'
        - '     - sysprep_xml (string): All settings specified in a XML format. This
            is the content of a typical answer.xml file that is used by System administrators
            during the Windows image customization. Check https://docs.microsoft.com/en-us/windows-hardware/manufacture/desktop/update-windows-settings-and-scripts-create-your-own-answer-file-sxs
            Exactly one of C(#sysprep) or C(#sysprep_xml) must be specified.'
        - ' - C(linux_config) (dict): Guest customization specification for a linux
            guest operating system ([''set''])'
        - '   - Accepted keys:'
        - '     - hostname (object): The computer name of the (Windows) virtual machine.
            A computer name may contain letters (A-Z), numbers(0-9) and hyphens (-)
            but no spaces or periods (.). The name may not consist entirely of digits.
            A computer name is restricted to 15 characters in length. If the computer
            name is longer than 15 characters, it will be truncated to 15 characters.
            Check {@link HostnameGenerator} for various options.'
        - '     - domain (string): The fully qualified domain name.'
        - '     - time_zone (string): The case-sensitive time zone, such as Europe/Sofia.
            Valid time zone values are based on the tz (time zone) database used by
            Linux. The values are strings  in the form "Area/Location," in which Area
            is a continent or ocean name, and Location is the city, island, or other
            regional designation. See the https://kb.vmware.com/kb/2145518 for a list
            of supported time zones for different versions in Linux.'
        - '     - script_text (string): The script to run before and after Linux guest
            customization.<br> The max size of the script is 1500 bytes. As long as
            the script (shell, perl, python...) has the right "#!" in the header,
            it is supported. The caller should not assume any environment variables
            when the script is run. The script is invoked by the customization engine
            using the command line: 1) with argument "precustomization" before customization,
            2) with argument "postcustomization" after customization. The script should
            parse this argument and implement pre-customization or post-customization
            task code details in the corresponding block. A Linux shell script example:
            <code> #!/bin/sh<br> if [ x$1 == x"precustomization" ]; then<br> echo
            "Do Precustomization tasks"<br> #code for pre-customization actions...<br>
            elif [ x$1 == x"postcustomization" ]; then<br> echo "Do Postcustomization
            tasks"<br> #code for post-customization actions...<br> fi<br> </code>'
        required: true
        type: dict
    global_DNS_settings:
        description:
        - Global DNS settings constitute the DNS settings that are not specific to
            a particular virtual network adapter. This parameter is mandatory.
        - 'Valid attributes are:'
        - ' - C(dns_suffix_list) (list): List of name resolution suffixes for the
            virtual network adapter. This list applies to both Windows and Linux guest
            customization. For Linux, this setting is global, whereas in Windows,
            this setting is listed on a per-adapter basis. ([''set''])'
        - ' - C(dns_servers) (list): List of DNS servers, for a virtual network adapter
            with a static IP address. If this list is empty, then the guest operating
            system is expected to use a DHCP server to get its DNS server settings.
            These settings configure the virtual machine to use the specified DNS
            servers. These DNS server settings are listed in the order of preference.
            ([''set''])'
        required: true
        type: dict
    interfaces:
        description:
        - IP settings that are specific to a particular virtual network adapter. The
            {@link AdapterMapping} {@term structure} maps a network adapter's MAC
            address to its {@link IPSettings}. May be empty if there are no network
            adapters, else should match number of network adapters configured for
            the VM. This parameter is mandatory.
        - 'Valid attributes are:'
        - ' - C(mac_address) (str): The MAC address of a network adapter being customized.
            ([''set''])'
        - ' - C(adapter) (dict): The IP settings for the associated virtual network
            adapter. ([''set''])'
        - '   This key is required with [''set''].'
        - '   - Accepted keys:'
        - '     - ipv4 (object): Specification to configure IPv4 address, subnet mask
            and gateway info for this virtual network adapter.'
        - '     - ipv6 (object): Specification to configure IPv6 address, subnet mask
            and gateway info for this virtual network adapter.'
        - '     - windows (object): Windows settings to be configured for this specific
            virtual Network adapter. This is valid only for Windows guest operating
            systems.'
        elements: dict
        required: true
        type: list
    session_timeout:
        description:
        - 'Timeout settings for client session. '
        - 'The maximal number of seconds for the whole operation including connection
            establishment, request sending and response. '
        - The default value is 300s.
        type: float
        version_added: 2.1.0
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
    vm:
        description:
        - The unique identifier of the virtual machine that needs to be customized.
            This parameter is mandatory.
        required: true
        type: str
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
- name: Customize the VM
  vmware.vmware_rest.vcenter_vm_guest_customization:
    vm: "{{ lookup('vmware.vmware_rest.vm_moid', '/my_dc/vm/test_vm1') }}"
    configuration_spec:
      linux_config:
        domain: mydomain
        hostname:
          fixed_name: foobar
          type: FIXED
    interfaces:
    - adapter:
        ipv4:
          type: STATIC
          gateways:
          - 192.168.123.1
          ip_address: 192.168.123.50
          prefix: 24
    global_DNS_settings:
      dns_suffix_list: []
      dns_servers:
      - 1.1.1.1
"""

RETURN = r"""
# content generated by the update_return_section callback# task: Customize the VM
value:
  description: Customize the VM
  returned: On success
  sample: {}
  type: dict
"""

# This structure describes the format of the data expected by the end-points
PAYLOAD_FORMAT = {
    "set": {
        "query": {},
        "body": {
            "configuration_spec": "spec/configuration_spec",
            "global_DNS_settings": "spec/global_DNS_settings",
            "interfaces": "spec/interfaces",
        },
        "path": {"vm": "vm"},
    }
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

    argument_spec["configuration_spec"] = {"required": True, "type": "dict"}
    argument_spec["global_DNS_settings"] = {"required": True, "type": "dict"}
    argument_spec["interfaces"] = {"required": True, "type": "list", "elements": "dict"}
    argument_spec["vm"] = {"required": True, "type": "str"}

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
    return (
        "https://{vcenter_hostname}" "/api/vcenter/vm/{vm}/guest/customization"
    ).format(**params)


async def entry_point(module, session):
    func = globals()["_set"]

    return await func(module.params, session)


async def _set(params, session):
    _in_query_parameters = PAYLOAD_FORMAT["set"]["query"].keys()
    payload = prepare_payload(params, PAYLOAD_FORMAT["set"])
    subdevice_type = get_subdevice_type("/api/vcenter/vm/{vm}/guest/customization")
    if subdevice_type and not params[subdevice_type]:
        _json = await exists(params, session, build_url(params))
        if _json:
            params[subdevice_type] = _json["id"]
    _url = (
        "https://{vcenter_hostname}" "/api/vcenter/vm/{vm}/guest/customization"
    ).format(**params) + gen_args(params, _in_query_parameters)
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
