# try-ansible-runner
Sometimes you need to trigger & control ansible via code. There are some tutorials below that are helpful on the but I've always felt less than thrilled about their interfaces. Recently I discovered the `ansible-runner` package that makes it easier to interact with ansible programmatically.

This proof of concept installs PHP, MySQL, & Redis.

## Building
```sh
docker build -t try-ansible-runner .
docker run -d -e=container=docker --stop-signal=SIGRTMIN+3 --cap-add=SYS_ADMIN --security-opt=seccomp:unconfined -v /sys/fs/cgroup:/sys/fs/cgroup:ro -v $(pwd):/app try-ansible-runner /sbin/init
```

# mkdir -p /var/run/mysqld
# chown -R mysql:mysql /var/run/mysqld

```sh
source /etc/apache2/envvars
apache2 -S
```


## Resources
- https://serversforhackers.com/c/running-ansible-2-programmatically
- https://github.com/jtyr/ansible-run_playbook/blob/master/run.py
- https://www.felixchr.com/2017/10/ansible-2-4-api-run-playbook-with-extra-variables/
- https://stackoverflow.com/questions/34860131/running-an-ansible-playbook-using-python-api-2-0-0-1
- https://medium.com/@navaneethrvce/minimal-python-code-to-run-an-ansible-playbook-using-ansible-api-601a9564b03e
- https://docs.ansible.com/ansible/latest/dev_guide/developing_plugins.html
- https://github.com/ansible/ansible-runner
- https://www.renemoser.net/blog/2017/09/02/decoupling-ansible-handlers/
- http://codeheaven.io/15-things-you-should-know-about-ansible/
- https://www.ansible.com/power-of-callback-plugins
- https://developers.redhat.com/blog/2019/04/24/how-to-run-systemd-in-a-container/