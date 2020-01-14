### Next Hop Health Check

#### Usage cases
1. to monitor next-hop ip adresses of static routes, to remove dead routes from the network device. 
2. Cumulus supports next-hop BFD tracking for both BGP and OSFP, for static routes BFD is not supported

#On the switch: 
#To install Pip 
wget http://ftp.us.debian.org/debian/pool/main/p/python-pip/python-pip-whl_18.1-5_all.deb
wget http://ftp.us.debian.org/debian/pool/main/p/python-pip/python-pip_9.0.1-2+deb9u1_all.deb

#To install Ansible
pip install wheel
pip install ansible


#### Use staticroutes-to-json.py to convert your static routes to json format
staticroutes-to-json.py, is used to convert your routes into JSON format, use static-routes-covert-to-txt.xlsx and staticroutes.txt as examples, all text routes should be saved in staticroutes.txt file. Make sure no leading spaces in each line or any trailing spaces



#### Steps
##### WARNING: make sure to backup /etc/frr/frr.conf file before deploying this on your switch for the first time.
1. $ `copy healthcheck-nexthop to local Linux server and cd into it`
1. $ `apt-get install sshpass`
1. $ `sudo pip install virtualenv`
1. $ `virtualenv venv && source venv/bin/activate`
1. $ `pip install ansible==2.5 
1. $ `./venv/bin/ansible-playbook deploy-on-sw.yml`
1. $ Login into the switch
1. $  `sudo -i '
1. $  `cd /var/ansible-cronjob && source venv/bin/activate' 
1. $ update the `staticroutes.txt` with routes, you want to convert to json, you will not be able to add static routes manually to switch while this is running, they will be removed automatically. Please make sure to follow the correct syntax, you can configure if you want to monitor the route using ansible-playbook or not `check_healthy`

1. $ In `staticroutes.yml` update `default_route` and `default_route2` if these are not pingable this whole program will not start, make any changes.
Note: IF you have one gateway, set `default_route` and `default_route2` to same ip address
1. $ Also in `roles/routes-health/tasks/main.yml`  for task 1 and task 2  in list update the VRF in which the default routes reside by default that VRF is set to `VRF_I`
           `script: test.py {{ default_route }} YOURVRFNAMEHERE `
1. $ Next run `python staticroutes-to-json.py`
1. $ Run command `cp staticroutes.yml group_vars/all.yml`, now the ansible-playbook will use the updated routes for your environment 
1. $ `crontab -e` to change the interval at which cronjob runs, by default its set to run every 8 minutes


##### deploy-on-sw.yml short description
The ansible deploy-on-sw.yml playbook installs dependencies for pip's ansible, copies "ansible-project" folder to
/var/ansible-cronjob directory, creates a virtual  python ```venv``` environment , installs required pip packages and sets up a cronjob on the switch. 

##### check-routes-health.yml short description

##### WARNING: all static routes must be configured in /var/ansible-cronjob/group_vars/all.yml file, or will be deleted when new frr.conf file is generated 

The Ansible check-routes-health.yml playbook is used for generating frr.conf file based on routes defined in ```all.yml``` file. It runs the role ```routes-health``` to check the health of all the next-hop ip addresses. It uses the python script ```test.py``` to ping the next-hop ```ipv4``` and ```ipv6``` addresses. 
###### check-routes-health.yml run summary 
1. It checks if the default route 1 or 2 is active, if neither is active it stops ( this to prevent unwanted config changes)
2. pings the ip only if we have enabled health checking for that route in  ```/var/ansible-cronjob/group_vars/all.yml``` file
3. It does diff between next-hop ip's active now vs last run, it recogonizes the change, it generates a new ```/etc/frr/frr.conf```  file and reloads ```frr``` configurations 

##### Logs
The logs can be found here:
/var/ansible-cronjob/name-of-playbook.log (these can be enabled from crontab, currently disabled)


