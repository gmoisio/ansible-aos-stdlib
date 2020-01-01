#!/usr/bin/env python3

# Copyright (c) 2019, Gilbert MOISIO
#
# All rights reserved.
#
# License: CC BY-NC-ND 4.0
#          Attribution-NonCommercial-NoDerivatives 4.0 International
#
# You are free to:
#
# Share — copy and redistribute the material in any medium or format
#
# Under the following terms:
#
# Attribution   — You must give appropriate credit, provide a link to the
#                 license, and indicate if changes were made. You may do so in
#                 any reasonable manner, but not in any way that suggests the
#                 licensor endorses you or your use.
# NonCommercial — You may not use the material for commercial purposes.
# NoDerivatives — If you remix, transform, or build upon the material, you may
#                 not distribute the modified material.
# No additional restrictions — You may not apply legal terms or technological
#                              measures that legally restrict others from doing
#                              anything the license permits.
#

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'supported_by': 'community',
                    'status': ['stableinterface']}

DOCUMENTATION = '''
---
module: ale_aos_command
author: Gilbert MOISIO
version_added: "2.9.2"
short_description: Send a command to an ALE OmniSwitch device.
description:
    - Connect to an OmniSwitch device and send a command. It can search for a
      string.
requirements:
    - netmiko >= 2.4.2
options:
    host:
        description:
            - Set to {{ inventory_hostname }}
        required: true
    port:
        description:
            - SSH connection port
        required: false
        default: 22
    username:
        description:
            - Login username
        required: true
    password:
        description:
            - Login password
        required: true
    command:
        description:
            - Command to send to the device
        required: true
    search:
        description:
            - String to search in the output of the command
        required: false
        default: ''
'''

EXAMPLES = '''
- ale_aos_command: 
    host: "{{ inventory_hostname }}"
    username: admin
    password: switch
    command: show running-directory
    search: "Running Configuration    : SYNCHRONIZED"
'''

RETURN = '''
msg:
    description: Error message
    returned: On fail
    type: string
output:
    description: Output returned by the command
    returned: On exit and on fail if the search string is not found
    type: string
'''

from ansible.module_utils.basic import *
from netmiko import ConnectHandler
from netmiko.ssh_exception import *

def main():

    module = AnsibleModule(
        argument_spec=dict(
            host=dict(type=str, equired=True),
            port=dict(type=int, required=False, default=22),
            username=dict(type=str, required=True),
            password=dict(type=str, required=True, no_log=True),
            command=dict(type=str, required=True),
            search=dict(type=str, required=False, default=None),
        ),
        supports_check_mode=False)

    net_device = {
        'device_type': 'alcatel_aos',
        'ip': module.params['host'],
        'port': module.params['port'],
        'username': module.params['username'],
        'password': module.params['password'],
    }

    try:
        ssh_conn = ConnectHandler(**net_device)
        output = ssh_conn.send_command(module.params['command'])
        ssh_conn.disconnect()
        if module.params['search'] and module.params['search'] not in output:
            module.fail_json(msg="Search string (%s) not in command output" %
                                 (module.params['search']), output=output)
        if 'ERROR' in output:
            module.fail_json(msg="Error in command execution", output=output)            
        module.exit_json(output=output)
    except (NetMikoAuthenticationException, NetMikoTimeoutException):
        module.fail_json(msg="Failed to connect to device (%s)" %
                             (module.params['host']))

if __name__ == '__main__':
    main()