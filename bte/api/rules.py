# -*- coding:utf-8 -*-
import os
import sys
from tornado import escape
from tornado.httpclient import HTTPClient

from bte.api import base
from bte import cache as Cache
from bte.utils import get_options, Log

url_map = {
    r"/rules": "Hack",
}

rule_opts = [
    {
        "name": "black_rule",
        "type": str,
        "default": "/etc/bte/black.json",
        "help": "Hack operate black list",
    },
    {
        "name": "white_rule",
        "type": str,
        "default": "/etc/bte/white.json",
        "help": "Hack operate black list",
    },
    {
        "name": "minion_provide",
        "type": str,
        "default": "http://127.0.0.1/serveruuid/",
        "help": "Check minion is exists",
    },
]

cfg = get_options(rule_opts)
cache = Cache.Backend()
log = Log(cfg)

if not os.path.isfile(cfg.black_rule):
    log.error("%s: no such file or directory" % cfg.black_rule)
    print "%s: no such file or directory" % cfg.black_rule
    sys.exit(1)

if not os.path.isfile(cfg.white_rule):
    log.error("%s: no such file or directory" % cfg.black_rule)
    print "%s: no such file or directory" % cfg.black_rule
    sys.exit(1)


class Hack(base.Base):
    def get(self):
        minion = self.request.headers.get("X-Forwarded-For", self.request.headers.get("X-Real-Ip", self.request.remote_ip))
        #if self.check_hosts(minion):
        rule = self.generate_rule(minion)
        return self.finish(escape.json_encode(rule))
        self.write('{}')

    def generate_rule(self, minion):
        BLACK_RULE = cache.get('rule_policy_black') or {}
        WHITE_RULE = cache.get('rule_policy_white') or {}

        if BLACK_RULE.get("mtime", None) != self._mtime(cfg.black_rule):
            BLACK_RULE = self.read_cached_file(cfg.black_rule, BLACK_RULE)
            cache.set('rule_policy_black', BLACK_RULE)
        if WHITE_RULE.get('mtime', None) != self._mtime(cfg.white_rule):
            WHITE_RULE = self.read_cached_file(cfg.white_rule, WHITE_RULE)
            cache.set('rule_policy_white', WHITE_RULE)

        rule = {"b": [], "w": []}
        maps = {"b": BLACK_RULE["data"], "w": WHITE_RULE["data"]}
        for page, rules in maps.items():
            _rule = rules.get(minion, None) or rules.get("default", {})
            for r in _rule.get("rule", []):
                v = rules.get(r, None)
                if v:
                    rule[page].append(v)
        return rule

    def _mtime(self, filename):
        return os.path.getmtime(filename)

    def read_cached_file(self, filename, cache_info):
        mtime = self._mtime(filename)
        cache_info['mtime'] = mtime
        with open(filename) as fap:
            data = fap.read()
            try:
                data = escape.json_decode(data)
            except Exception,e:
                log.error("policy file %s synax error: %s" % (filename, str(e)))
                if 'data' not in cache_info:
                    cache_info['data'] = {}
                return cache_info
            cache_info['data'] = data
        return cache_info

    def check_hosts(self, minion):
        if hasattr(cfg, 'minion_provide'):
            http = HTTPClient()
            try:
                req = http.fetch(cfg.minion_provide+minion)
                http.close()
                return req.body
            except:
                log.error("minion %s dose not exists in cmdb" % minion)
                return None
        return None
