# 简介/原理

利用rsyslog将服务器的操作日志转发到agent监听的端口

agent通过HTTP API从服务端获取自己的安全规则, 利用规则对管理员的操作进行匹配

通过匹配从而触发对应的操作.


# 安装

* lion 运行在需要审计的服务器上,作为审计客户端
* bte_api  以服务端的身份运行


### 安装 lion




### 安装 bte_api

```
pip install -r requirement.txt
python setup.py install
nohup bte_api --config=/etc/bte/config > /dev/null &
```


# 规则编写

规则文件必须为合法的JSON格式,例如:

```
{
    "invalid_account": {"osuser": "root|fbsd|zone*"},
    "invalid_cmd": {"cmd": "^useradd|^groupadd|^nc"},

    "default": {"rule": ["invalid_account", "invalid_cmd"]},
    "1.1.1.1": {"rule": ["invalid_cmd"]}
}
```

* invalid_account  规则名字
* osuser  字段名
* root|fbsd|zone*  这里是正则表达式

* default 必须包含一个,主机默认应用次规则
* 1.1.1.1  针对特定的主机设置规则
