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
module: ale_aos_ping
author: Gilbert MOISIO
version_added: "0.1"
short_description: Check SSH connectivity for an ALE OmniSwitch device.
description:
    - Try to connect to an OmniSwitch device. The module check to see is the
      check_string is present in the output returned by find_prompt().
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
        default: '22'
    username:
        description:
            - Login username
        required: true
    password:
        description:
            - Login password
        required: true
    check_string:
        description:
            - String to check in the returned prompt
        required: false
        default: '>'
'''

EXAMPLES = '''
- ale_aos_ping: 
    host: "{{ inventory_hostname }}"
    username: admin
    password: switch
'''

RETURN = '''
Status and completion message that can be displayed with debug var.
'''

from ansible.module_utils.basic import *
from netmiko import ConnectHandler

def main():

    module = AnsibleModule(
        argument_spec=dict(
            host=dict(required=True),
            port=dict(required=False, default='22'),
            username=dict(required=True),
            password=dict(required=True, no_log=True),
            check_string=dict(required=False, default='>'),
        ),
        supports_check_mode=False)

    net_device = {
        'device_type': 'alcatel_aos',
        'ip': module.params['host'],
        'port': int(module.params['port']),
        'username': module.params['username'],
        'password': module.params['password'],
    }

    ssh_conn = ConnectHandler(**net_device)
    output = ssh_conn.find_prompt()
    if module.params['check_string'] in output:
        module.exit_json(msg="SSH connection completed successfully")
    else:
        module.fail_json(msg="Failed to detect check_string in output", output=output)

if __name__ == '__main__':
    main()