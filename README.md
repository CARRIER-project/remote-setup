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

## Tips and Workarounds
The ansible scripts contains a couple of workarounds and handy features for deploying the vantage6 infrastructure

### Vantage6 server configuration
[ansible/files/server/vserver-hpc-cloud.yml](ansible/files/server/vserver-hpc-cloud.yml) is the configuration file used to set up the vantage6 server. It will give you an idea of how to create a working configuration.


### Creating sample data
The script [ansible/files/node/download_sample_data.py](ansible/files/node/download_sample_data.py) will download sample data as a csv file to a specied file path.
Example:
```shell
python download_sample_data.py --target diabetes.csv
```

# Adding a node to the vantage6 server
[ansible/files/node/configure_node.py](ansible/files/node/configure_node.py) is a cli script that automates the process of creating a new organization, collaboration and node for vantage6.


The easiest way to call the script without using ansible is in the following way:
```shell
python configure_node.py ORGANIZATION_NAME
```
Where `ORGANIZATION_NAME` needs to be replaced with the name of the organization that this nodes belongs to. The CLI will prompt you for additional information.


