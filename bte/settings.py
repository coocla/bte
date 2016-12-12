#coding:utf-8
from tornado.options import parse_config_file

app_opts = [
    {
        "name": "address",
        "type": str,
        "default": "0.0.0.0",
        "help": "API listen address",
    },
    {
        "name": "port",
        "type": int,
        "default": "8337",
        "help": "API listen port",
    },
    {
        "name": "config",
        "type": str,
        "default": "/etc/bte/config",
        "callback": lambda p: parse_config_file(p, final=False),
        "help": "Path of config file.",
    },
    {
        "name": "cached_uri",
        "default": 'redis://yWZESkZ3VseoR8ybswSrdkVWC8TpvQVFa4kXucMr@127.0.0.1:6379/0',
        "help": 'cached backend uri',
        "type": str,
    },
    {
        "name": 'cache_timeout',
        "default": '3600',
        "help": 'cache timeout seconds',
        "type": str,
    }
]

