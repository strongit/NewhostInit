#################################################################################
#       iplist.py - Lookup IPs -> Domain and Domain -> IPs from iplist.net      #
#       Copyrighted:  Primal Security Podcast - www.primalsecurity.net          #
#                                                                               #
#       This program is free software: you can redistribute it and/or modify    #
#       it under the terms of the GNU General Public License as published by    #
#       the Free Software Foundation, either version 3 of the License, or       #
#       (at your option) any later version.                                     #
#                                                                               #
#       This program is distributed in the hope that it will be useful,         #
#       but WITHOUT ANY WARRANTY; without even the implied warranty of          #
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the           #
#       GNU General Public License for more details.                            #
#                                                                               #
#       You should have received a copy of the GNU General Public License       #
#       along with this program.  If not, see <http://www.gnu.org/licenses/>.   #
#################################################################################


#!/usr/bin/env python

####################################
# Curent URL format:               #
# http://iplist.net/74.125.228.73/ #
####################################


import os, urllib, sys, optparse, re

# Function to check file  
def checkFile(cfile):
  	if not os.path.isfile(cfile):
    		print '[-] ' + cfile + ' does not exist.'
    		exit(0)

  	if not os.access(cfile, os.R_OK):
    		print '[-] ' + cfile + ' access denied.'
    		exit(0)

  	print '[+] Fetching URLs from  ' +cfile


# Function to perform the lookup 
def iplook(ips):
	if iplist != None:
  		iFile = open(iplist, 'r')
  		for ip in iFile:
			ei = ip.split()
			i = ei[0]
    			httpR = urllib.urlopen("http://iplist.net/"+i+"/")
    			f = httpR.readlines()
			for line in f:
                		if "<h2" in line:
                        		if "</table" in line:
                                		# Formatting line for domain
                                		htm = line.split("<")
                                		html = htm[2]
                                		dom = html.split(">")
                                		domain = str(dom[1])
                                		# Formatting line for IP
                                		i = line.split("/")
                                		ip = str(i[4])
                        		else:   
                                		htm = line.split("<")
                                		html = htm[1]
                                		dom = html.split(">")
                                		domain = str(dom[1])
                               			i = line.split("/")
                                		ip = str(i[3])
                        		l = '%-25s --> %20s' % (domain,ip)
                        		print l


	else:
		httpR = urllib.urlopen("http://iplist.net/"+ips+"/")
		f = httpR.readlines()
		for line in f:
			if "<h2" in line:
				if "</table" in line:
					# Formatting line for domain
					htm = line.split("<")
					html = htm[2]
					dom = html.split(">")
					domain = str(dom[1])
					# Formatting line for IP
					i = line.split("/")
					ip = str(i[4])
				else:
					htm = line.split("<")
					html = htm[1]
					dom = html.split(">")
					domain = str(dom[1])
					i = line.split("/")
					ip = str(i[3])
				l = '%-25s --> %20s' % (domain,ip)
				print l

def main():
  	parser = optparse.OptionParser(sys.argv[0] +\
    		'-r <file_with_ips> || -i <ip_addr>')
	parser.add_option('-i', dest='ip', type='string', \
		help ='specify a target IP')
  	parser.add_option('-r', dest='ips', type='string', \
    		help='specify target file with IPs')
  	(options, args) = parser.parse_args()
	global iplist
	global ip
  	iplist = options.ips
	ip = options.ip

	if (iplist == None) and (ip == None):
		print parser.usage
		exit(0)
	
        if iplist != None:
		checkFile(iplist)
		iplook(iplist)

	else:
		iplook(ip)


if __name__ == "__main__":
      main()
