import ansible_runner
import ruamel.yaml as yaml
import tempfile
import sys
import json


def handle_event(evt):
    # print(evt['event'])

    if evt['event'] == 'verbose':
        return False
    
    if evt['event'] == 'runner_on_failed':
        print("====== ON_FAILED")
        print(json.dumps(evt, indent=4, sort_keys=False))

    if evt['event'] == 'runner_on_start':
        action = evt['event_data'].get('task_action')
        label = evt['event_data'].get('task')
        # print("! Starting", label, action)

    if evt['event'] == 'runner_on_ok':
        action = evt['event_data'].get('task_action')
        label = evt['event_data'].get('task')
        # print("! Done", label, action, evt['event_data']['res'].get('stdout'))
        # print(json.dumps(evt, indent=4, sort_keys=False))
        return True
    return False


tasks = [
    {
        'name': 'Test echoing a variable',
        'shell': 'echo Using PHP version {{ php_version }}'
    }, 
    {
        'name': 'Setting facts!',
        'set_fact': {
            'cats': 'dogs'
        }
    }
]
"""
- name: Ensure MySQL is started and enabled on boot.
  service: "name={{ mysql_daemon }} state=started enabled={{ mysql_enabled_on_startup }}"
  register: mysql_service_configuration
"""
config = [{
    'hosts': '127.0.0.1',
    'gather_facts': True,
    'connection': 'local',
    'vars': {
        'ansible_python_interpreter': '/usr/bin/python3',
        'mysql_enabled_on_startup': True,
        'mysql_max_binlog_size': "100M",
        'mysql_binlog_format': "ROW",
        'mysql_expire_logs_days': "10",
         
        # 'mysql_port': "3306",
        # 'mysql_bind_address': '0.0.0.0',
        # https://stackoverflow.com/questions/62987154/mysql-wont-start-error-su-warning-cannot-change-directory-to-nonexistent
        'php_install_recommends': False,
        'php_version': '7.4',
        'php_memory_limit': "256M",
        'php_max_execution_time': "30",
        'php_upload_max_filesize': "256M",
        'php_enable_php_fpm': False,
        'php_disable_functions': [
            'proc_nice',
            'proc_open',
            'proc_terminate',
            'passthru',
            'ini_alter',
        ],
        'php_packages_extra': [],
        'php_packages': [
            "php{{ php_version }}"
          
        ]
    },
    'roles': [
        
#         {
#             'name': 'geerlingguy.redis',
#             'redis_port': 6379,
#             'redis_bind_interface': '127.0.0.1',
#         }, 
#         {
#             'name': 'geerlingguy.mysql',
#             'become': 'yes'
#             # 'ignore_errors': True,
#         },
#         'geerlingguy.apache',
       
        {
            'name':'geerlingguy.php-versions',
            'php_packages': [
                "php{{ php_version }}",
            ],
        },
        'geerlingguy.php',
        #'geerlingguy.composer',
        #'geerlingguy.certbot',
       
    ],
    'pre_tasks': [
        {
            'name': 'Test echoing a variable',
            'shell': 'echo Using PHP version {{ php_version }}'
        },  
           {
      "name": "Check if ondrej/php PPA is already present",
      "stat": {
         "path": "/etc/apt/sources.list.d/ppa_ondrej_php_{{ansible_distribution_release}}.list"
      },
      "register": "ondrej_sourcelist_status"
   },
   {
      "name": "Add ondrej/php PPA",
      "apt_repository": {
         "repo": "ppa:ondrej/php",
         "state": "present",
         "update_cache": "yes"
      },
      "when": "ondrej_sourcelist_status.stat.exists == False"
   }    
    ],
    'tasks': [],
    'handlers': [
        {
            'name': 'post on slack?',
            'shell': 'curl https://catscats.free.beeceptor.com?redis=1',
            'listen': 'restart redis',
        }
    ]
}]

#   notify: 

# _, task_file = tempfile.mkstemp(dir='./_tasks', suffix='_task.yml')

task_file = "_tasks/sample.yaml"

with open(task_file, 'w') as fh:
    yaml.dump(config, fh, yaml.RoundTripDumper)

with open(task_file, 'r') as fh:
    print(fh.read())


# ANSIBLE_STDOUT_CALLBACK=json_cb 
# don't use extra_vars for private data
# ANSIBLE_CONFIG=ansible.cfg
kwargs={
    'ident': 'test-install-php',
    'private_data_dir': "./env",
    'artifact_dir': "./",
    'playbook': task_file,
    'json_mode': True,
    'verbosity': 0,
    'project_dir': './',
    'quiet': False,
    'event_handler': handle_event,
    # 'cmdline': '--force-handlers',
}

r = ansible_runner.run(**kwargs)
print(r.status)
# print(len(r.stdout.read().split("\n")))
exit()
# successful: 0
for each_host_event in r.events:
    print(each_host_event['event'])
print("Final status:")
print(r.stats)