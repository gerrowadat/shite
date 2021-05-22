Fiddling with Ansible. You also want a inventory.yml that looks like:

```
linux_all:
        hosts:
                picluster1:
                picluster2:
                picluster3:
                picluster4:
                picluster5:
                otherserver:
                        ansible_user: otheruser
        vars:
                ansible_user: ubuntu
```

And then:

```
ansible-playbook -i inventory.yml site.yml
```

Ansible really likes directories, the file you probably want to look at is roles/login/tasks/main.yml for now.

Note: You probably shouldn't use this, this is me learnign about ansible, so there are better ways out there.
