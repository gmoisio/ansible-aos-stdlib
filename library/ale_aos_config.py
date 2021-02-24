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
module: ale_aos_config
author: Gilbert MOISIO
version_added: "1.1.0" # of ale_aos role
short_description: Send config commands to an ALE OmniSwitch device.
description:
    - Connect to an OmniSwitch device and send configurations commands.
      It can take commands from a file or a commands list.
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
    file:
        description:
            - Path to the text file with one config command per line
        required: false
        default: ''
    commands:
        description:
            - List of the config commands to run
        required: false
        default: []
    save:
        description:
            - Boolean to save and synchronize memories after changes success
        required: false
        default: false
    backup:
        description:
            - Boolean to backup configuration in backups/file before changes
        required: false
        default: false
'''

EXAMPLES = '''
- ale_aos_config: 
    host: "{{ inventory_hostname }}"
    username: admin
    password: switch
    commands:
      - vlan 100 enable name test1
      - vlan 200 enable name test2

- ale_aos_config: 
    host: "{{ inventory_hostname }}"
    username: admin
    password: switch
    file: commands.txt
'''

RETURN = '''
msg:
    description: Error message
    returned: On fail
    type: string
output:
    description: Output returned from the commands
    returned: On exit
    type: string
'''

from ansible.module_utils.basic import *
from netmiko import ConnectHandler
from netmiko.ssh_exception import *
from datetime import datetime
from pathlib import Path


def error_exec(output):
    for key, value in output.items():
        if 'ERROR' in value:
            return True


def diff_config(output):
    if output['snapshot_before'] != output['snapshot_after']:
        return True


def backup_config(output, hostname):
    out_filename = hostname + '_' + datetime.now().strftime('%Y-%m-%d_%H:%M:%S') + '.conf'
    path_dir = Path('backups')
    path_dir.mkdir(exist_ok=True)
    with open(path_dir / out_filename, 'w') as out_file:
       out_file.write(output['snapshot_before'])
    return True

def main():

    output = {}

    module = AnsibleModule(
        argument_spec=dict(
            host=dict(type=str, required=True),
            port=dict(type=int, required=False, default=22),
            sshconfig=dict(type=str, required=False, default=None),
            username=dict(type=str, required=True),
            password=dict(type=str, required=True, no_log=True),
            file=dict(type=str, required=False, default=None),
            commands=dict(type=list, required=False, default=None),
            save=dict(type=bool, required=False, default=False),
            backup=dict(type=bool, required=False, default=False),
        ),
        supports_check_mode=False)

    net_device = {
        'device_type': 'alcatel_aos',
        'ip': module.params['host'],
        'port': module.params['port'],
        'ssh_config_file': module.params['sshconfig'],
        'username': module.params['username'],
        'password': module.params['password'],
    }

    if not module.params['commands'] and not module.params['file']:
        module.fail_json(msg="No commands nor file provided")


    try:
        ssh_conn = ConnectHandler(**net_device)
        output['snapshot_before'] = ssh_conn.send_command_timing('show configuration snapshot')
        if module.params['backup']:
            backup_config(output, module.params['host'])
        if module.params['commands']:
            output['command'] = ssh_conn.send_config_set(config_commands=\
                                              module.params['commands'])
        elif module.params['file']:
            output['command'] = ssh_conn.send_config_from_file(config_file=\
                                                    module.params['file'])
        output['snapshot_after'] = ssh_conn.send_command_timing('show configuration snapshot')
        if not error_exec(output) and diff_config(output) and module.params['save']:
            ssh_conn.save_config()
        ssh_conn.disconnect()
        if error_exec(output):
            module.fail_json(msg="Error in a command execution", output=output)
        elif diff_config(output):
            module.exit_json(changed=True, output=output['command'])
        else:
            module.exit_json(output=output['command'])
    except (NetMikoAuthenticationException, NetMikoTimeoutException):
        module.fail_json(msg="Failed to connect to device (%s)" %
                             (module.params['host']))

if __name__ == '__main__':
    main()
