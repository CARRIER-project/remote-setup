# remote-setup
General utility files and script for setting up vantage6 on a remote server.

## Prerequisites
- [Ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html)

## Deploying the infrastructure
You will need to do the following steps:
1. Clone the repository
1. Copy `[PROJECT_ROOT]/ansible/hosts.example.yml` to `[PROJECT_ROOT]/ansible/hosts.yml`
1. Fill in the blanks in the `hosts.yml` file. Make sure there are ip adresses filled in for every host type.
1. In the terminal, cd to `[PROJECT_ROOT]/ansible`
1. Run `ansible-playbook -i hosts.yml -u ubuntu main.yml`
