# -*- coding:utf-8 -*-
import os
import imp
import logging
from tornado.options import define, parse_command_line,\
        parse_config_file, options

def register_opt(opt, group=None):
    """Register an option schema
    opt = {
            "name": 'config',
            "default": 'ops.conf',
            "help": 'path of config file',
            "tyle": str,
            "callback": lambda path: parse_config_file(path, final=False)
        }
    """
    if opt.get('name', ''):
        optname = opt.pop('name')
        if optname in options._options.keys():
            options._options.pop(optname)
        define(optname, **opt)


def register_opts(opts, group=None):
    """Register multiple option schemas at once."""
    for opt in opts:
        register_opt(opt, group)
    return options

def get_options(opts=None, group=None):
    if opts:
        options = register_opts(opts, group)
    if hasattr(options,'config'):
        parse_config_file(options.config, final=False)
    parse_command_line()
    return options

def load_url_map(path):
    url_maps = []
    our_dir = path[0]
    for dirpath, dirnames, filenames in os.walk(our_dir):
        for fs in filenames:
            f, f_ext = os.path.splitext(fs)
            if f == '__init__' or f_ext != '.py':
                continue
            fn_, path, desc = imp.find_module(f, [dirpath])
            mod = imp.load_module(f, fn_, path, desc)
            if getattr(mod, 'url_map', None):
                for url, hander in getattr(mod, 'url_map').iteritems():
                    url_maps.append((url, getattr(mod, hander)))
    return url_maps

def Log(cfg=None):
    if cfg is None or not hasattr(cfg, 'log'):
        log_opts = [
            {
                "name": "log",
                "type": "str",
                "default": "/var/log/bte_api.log",
                "help": "API process log file",
            },
        ]
        cfg = get_options(log_opts)
    logger = logging.getLogger('bte_api')
    DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
    FORMAT = '[%(levelname)-8s] [%(asctime)s] %(message)s'
    FileHandler = logging.FileHandler(cfg.log)
    FileHandler.setFormatter(logging.Formatter(fmt=FORMAT, datefmt=DATE_FORMAT))
    logger.addHandler(FileHandler)
    logger.setLevel(logging.INFO)
    return logging.getLogger('bte_api')
