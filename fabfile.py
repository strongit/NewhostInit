from fabric.api import *
import zabbix_install_salt as zs

env.hosts = zs.get_ip()
env.password='fangcang'
def auth():
#    with settings(sudo_user='root'):
    with settings(warn_only=True):
        run("mkdir /root/.ssh/")
        run("echo 'ssh-rsa AAAAB3NzaC1yc2EAAAABIwAAAQEAvTamk4JtllINKDUj8ITZ4PrwqNIQyXkLj/l/gmmJqaxtaWsdsXMJ72WbLmDC2LD9emKGj+jt8vL5s6W74yiNQCEbWJ7hIqsN1zdecYtGRvFuT8RAB/QwYZ9NalKbSKqXkfCdUGvZxYtCgcxV0jPosvNUcWsLKhxNKmJgSQaAmALVcRw4IHuTAm6UjvjcGSC5+kXtHVmKOr1ZQKoLmzjanEHgQDg7pb9Pn+obv0uuvHksUNoMf0RzuWWDvWO1SzNyINYQRFPUFxAZcFH1cDA4+nTtZFfNMl7rFFtnC7lhCM+JuV1j1quirKYrMEHMrkijSVOPx0AlUWtJjdUAJQhiXQ== root@localhost.localdomain' >> /root/.ssh/authorized_keys")
