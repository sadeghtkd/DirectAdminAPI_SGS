# DirectAdmin API for Python
This package help you manage DirectAdmin control panel via API.
## Installation
```
pip install DirectAdminAPI-SGS-shohani
```
## Sample usage
```    
    from DirectAdminAPI_SGS_shohani.api import PrettyAPI

    api = PrettyAPI(username=admin_da_user,password=admin_da_pwd,server=da_url,json=True)
    #Get list of users that has access to a protected folder in DirectAdmin
    da_users = api.get_protected_directory_users('/domains/test.com/public_html/manager')
  
    users = da_users['users']
    for key in users:
        print(users[key])
    
    #search recursively for test.txt in root path
    da_files = api.search_files( '/','test.txt' , recursive=True)
    for key in da_files:
        print(da_files[key])
```