#-*- coding:utf-8 -*-
import redis
import cPickle

from bte.utils import get_options

cache_opts = [
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
    }]

class Backend(object):
    def __init__(self, cfg=None):
        if cfg is None:
            self.cfg = get_options(cache_opts)
        else:
            self.cfg = cfg
        conn_str = self.cfg.cached_uri
        backend_auth, host_db = conn_str.split('@')
        passwd = backend_auth.split('://')[-1]
        host, port_db = host_db.split(':')
        port, db = port_db.split("/")
        if passwd:
            self.conn = redis.StrictRedis(host=host, port=port, db=db, password=passwd)
        else:
            self.conn = redis.StrictRedis(host=host, port=port, db=db)

    def get(self, id, default=None):
        """
        Return object with id 
        """
        try:
            ret = self.conn.get(id)
            if ret:
                ret = cPickle.loads(ret)["msg"]
        except:
            ret = default
        return ret

    def set(self, id, user_msg, timeout=None):
        """
        Set obj into redis-server.
        Expire 3600 sec
        """
        timeout = timeout or self.cfg.cache_timeout
        try:
            if user_msg:
                msg = cPickle.dumps({"msg": user_msg})
                self.conn.set(id, msg)
                self.conn.expire(id, timeout)
                return True
        except:
            self.conn.delete(id)
            return False

    def delete(self, id):
        try:
            self.conn.delete(id)
        except:
            pass
