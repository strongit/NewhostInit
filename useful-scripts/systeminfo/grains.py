import salt.client
ips = ['192.168.2.25','storm2','storm5']
for ip in ips:
    print type(ip)
    c = salt.client.LocalClient()
    context = {}
    grain = c.cmd(ip,"grains.items")
    diskusage = c.cmd(ip,"disk.usage")
    cpu = grain[ip]['cpu_model']+grain[ip]['cpuarch']
    os = grain[ip]['os_family']+'-'+grain[ip]['osfullname']+'-'+grain[ip]['osrelease']+'-'+grain[ip]['osarch']
#    serialnumber = grain[ip]['serialnumber']
    mem_total = grain[ip]['mem_total']
    kernel = grain[ip]['kernel']+'-'+grain[ip]['kernelrelease']
    ipv4 = str(grain[ip]['ip4_interfaces']).replace("'lo': ['127.0.0.1'], ","").strip()
    if "/" not in diskusage[ip]:
      disk_data = "None"
    else:
      #disk_data = diskusage[ip]['/']['available'] / 1048576
      disk_data = str(int(diskusage[ip]['/']['available']) / 1048576) + 'G'
    ipinfo = []
    #for dev in ipv4:
    #    ipinfo.append(dev+':'+ipv4[dev][0])
    context['cpu'] = cpu
    context['os'] = os
    context['mem_total'] = mem_total
    context['kernel'] = kernel
    context['ipv4'] = ipv4
    context['root_freedata'] = disk_data
    print context
