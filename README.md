ALE_AOS
=======

An Ansible role to access Alcatel-Lucent Enterprise OmniSwitch devices.

Requirements
------------

Requires netmiko >= 2.9

Example Playbook
----------------

  - name: This is a test for ale_aos_ping module
    hosts: ale
    connection: local
    roles:
      - ale_aos
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

License
-------

Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0).

Author Information
------------------

Gilbert MOISIO, Network & Methodology Senior Consultant.
