# k3s - Ansible

Ansible code is copied from https://github.com/k3s-io/k3s-ansible and is licensed under Apache-2.0 License. A copy of the license file can be found in the same directory as this file.

#### Changes to code
1. inventory folder to match local machine setup
2. added node name flag to k3s exec command


### Usage
1. Ensure each of your nodes has a different hostname
2. edit `inventory/hosts.ini` and `inventory/group_vars/all.yml` to match the system information gathered from your machines
3. Run the echo playbook to test your connection
   ```
   ansible-playbook echo.yml -i inventory/hosts.ini
   ```
4. Run the site playbook for installing k3s
   ```
   ansible-playbook site.yml -i inventory/hosts.ini
   ```
5. Get kube config
   ```
   scp -i keys/id_rsa <user>@<master_ip>:~/.kube/config ~/.kube/config
   ```
