[![Build Status](https://travis-ci.org/gmoisio/ansible-aos-stdlib.svg?branch=master)](https://travis-ci.org/gmoisio/ansible-aos-stdlib)
[![Ansible Galaxy](https://img.shields.io/badge/ansible--galaxy-ale_aos-blue.svg)](https://galaxy.ansible.com/gmoisio/ale_aos)

ALE_AOS
=======

An Ansible role to access Alcatel-Lucent Enterprise OmniSwitch devices.

Requirements
------------

Requires ansible >= 2.9.2 and netmiko >= 2.4.2

Example Playbook
----------------

~~~~
- name: This is a test for ale_aos_ping module
  hosts: ale
  connection: local
  roles:
    - gmoisio.ale_aos
  vars:
    ansible_python_interpreter: "python"
  tasks:
    - name: Test ale_aos_ping Python module
      ale_aos_ping: 
        host: "{{ inventory_hostname }}"
        username: admin
        password: switch
      register: result
    - debug: var=result 
~~~~

Add below setting to your ansible.cfg and get a better display:

~~~~
[defaults]
stdout_callback = yaml
~~~~

Modules
-------
~~~~
module: ale_aos_ping
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
        default: 22
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


EXAMPLES
- ale_aos_ping: 
    host: "{{ inventory_hostname }}"
    username: admin
    password: switch
~~~~

~~~~
module: ale_aos_command
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
              to validate the proper execution
        required: false
        default: ''
    timing:
        description:
            - Boolean to run send_command_timing instead of send_command
        required: false
        default: false


EXAMPLES
- ale_aos_command: 
    host: "{{ inventory_hostname }}"
    username: admin
    password: switch
    command: show running-directory
    search: "Running Configuration    : SYNCHRONIZED"
~~~~

~~~~
module: ale_aos_config
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
            - Boolean to backup configuration in a file before changes
        required: false
        default: false


EXAMPLES
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
~~~~

License
-------

Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0).

Author Information
------------------

Gilbert MOISIO, Network & Methodology Senior Consultant.
