import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 
from src.DirectAdminAPI_SGS_shohani.api import PrettyAPI
from getpass import getpass

api = PrettyAPI(username=input("admin_da_user:"),password=getpass("admin_da_pwd:"),server=input("Enter DA url:"),json=True)

#while True:
#    res_certs = api.get_ssl_certificates(input("domain name:"))
#    print(res_certs)

#res_disable = api.disable_ssl('androidsoftware.ir')
res_enable = api.enable_ssl('flutoday.ir')
res = api.enable_letsencrypt_ssl('flutoday.ir','flutoday.ir','sadegh.tkd@gmail.com',["*.flutoday.ir","flutoday.ir"] , wildcard='yes')
print(res)
#da_files = api.search_files(input('Enter path to list files:'),'a.txt' , recursive=True)

#for key in da_files:
    #print(da_files[key])
#res = api.get_domains()


#res = api.get_user_dns('ghanbari.ir')
#print(res)


