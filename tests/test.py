import os
import sys
import inspect

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir) 


from src.DirectAdminAPI_SGS_shohani.api import PrettyAPI
from getpass import getpass

api = PrettyAPI(username=input("admin_da_user:"),password=getpass("admin_da_pwd:"),server=input("Enter DA url:"),json=True)

#res_certs = api.get_ssl_certificates('androidsoftware.ir')
#res_disable = api.disable_ssl('androidsoftware.ir')
#res_enable = api.enable_ssl('androidsoftware.ir')
#res = api.enable_letsencrypt_ssl('androidsoftware.ir','name','sadegh.tkd@gmail.com',["androidsoftware.ir","www.androidsoftware.ir","mail.androidsoftware.ir"])

#da_files = api.search_files(input('Enter path to list files:'),'a.txt' , recursive=True)

#for key in da_files:
    #print(da_files[key])
res = api.get_all_users_with_quota()
print(res)