import requests
import simplejson

try:
    from urllib.parse import urlparse, parse_qs # noqa
except ImportError:
    from urlparse import urlparse, parse_qs # noqa


class ResponseException(Exception):
    pass


class UnauthorizedException(Exception):
    pass


class API(object):
    '''API() connects, sends and processes API calls.'''
    def __init__(self, username, password, server, json=False, debug=False):
        self.username = username
        self.password = password
        self.server = server
        self.debug = debug
        self.json = json

    def lowerfirst(self, string):
        '''Set first character of string to lowercase'''
        return string[:1].lower() + string[1:] if string else ''

    def process_errors(self, data):
        # Check for errors
        if 'error' in data:
            if self.json:
                details = data['result']
                text = data['error']
            else:
                details = data['details'][0] if 'details' in data else ''
                text = data['text'][0] if 'text' in data else ''

            error = '{}: {}'.format(
                text.rstrip('\r\n'), self.lowerfirst(details).rstrip('\r\n')
            )

            raise ResponseException(error)

    def process_response(self, response):
        '''Process the response received from the API'''

        # Validate username and password
        if 'X-DirectAdmin' in response.headers:
            if response.headers['X-DirectAdmin'] == 'Unauthorized':
                raise UnauthorizedException('Invalid username or password')

        try:
            data = response.json()
        except simplejson.errors.JSONDecodeError:
            data = parse_qs(response.text)

        self.process_errors(data)

        # This is DirectAdmin's way of returning a list()
        if 'list[]' in data:
            return data['list[]']

        return data

    def debug_response(self, response):
        '''Print debug data'''
        print('Debugging data...')
        print('Connecting to:\r\n{}'.format(response.url))
        print('Headers:\r\n{}'.format(response.headers))
        print('Output:\r\n{}'.format(response.text))

    def call(self, command, params={}):
        '''Send data to the API through a post request'''
        # Only request json when we can
        if self.json:
            params['json'] = 'yes'

        if 'GET_METHOD' in params :
            response = requests.get(
                url='{}/{}'.format(self.server, command),
                auth=(self.username, self.password),
                params=params,
            )
        else:    
            response = requests.post(
                url='{}/{}'.format(self.server, command),
                auth=(self.username, self.password),
                params=params,
            )

        if self.debug:
            self.debug_response(response=response)

        return self.process_response(response=response)

    def become(self, username):
        '''become() allows you to login as a different user'''
        return self.__class__(
            username='{}|{}'.format(self.username, username),
            password=self.password,
            server=self.server,
        )

    def __getattr__(self, name):
        '''Process API calls'''
        def method(*args, **kwargs):
            params = {}

            # We prefer kwargs, but args are supported too
            if len(args) != 0:
                params = args[0]
            else:
                params = kwargs

            # Validate data before sending a request to the API
            if isinstance(params, dict):
                return self.call(
                    command=name.upper(),
                    params=params,
                )

            raise ResponseException('Invalid argument')

        return method


class PrettyAPI(API):
    '''PrettyAPI() provides simplified methods to interact with the API.'''
    def create_user(self, username, password, email, domain, package, ip='server'): # noqa
        '''A pretty wrapper to create a user'''
        return self.cmd_account_user(
            action='create',
            add='Submit',
            username=username,
            email=email,
            passwd=password,
            passwd2=password,
            domain=domain,
            package=package,
            ip=ip,
            notify='no',
        )

    def remove_user(self, username):
        '''Remove a user'''
        return self.cmd_select_users(
            confirmed='Confirm',
            delete='yes',
            select0=username,
        )

    def get_protected_directory_users(self, path):
        '''Get protected directory users list'''
        return self.cmd_file_manager(
            action='protect',
            path=path,            
            ipp=500 ,#item per page
            GET_METHOD = True
        )

    def get_files_list(self, domain):
        '''Get files and directories list'''
        return self.cmd_api_file_manager(
            domain=domain,
             GET_METHOD = True
        )

    def get_folders_by_path(self, path):
        '''Get directories list'''
        return self.cmd_api_file_manager(
            action='parent_tree',
             path = path,
             GET_METHOD = True
        )

    def search_files(self, path , value , recursive=False):
        '''Search for files or folders'''
        if recursive:
            return self.cmd_api_file_manager(
                action='recursive_search',
                path = path,
                search=value,
                type='all',
                GET_METHOD = True
            ) 
        else:
            return self.cmd_api_file_manager(
                action='json_all',
                path = path,
                page='1',
                comparison6='contains',
                value6=value,
                ipp=500 ,#item per page
                GET_METHOD = True
            )        

    def enable_letsencrypt_ssl(self, domain,name,email,domains,wildcard="no"):
        '''Enable free SSL '''
        if type(domains) != list:
            raise Exception("Domains must be a list of domains")
    
        keys =  ['le_select{}'.format(i) for i in range(len(domains))]

        domains_dict = dict(zip(keys,domains ))
        return self.cmd_api_ssl(
                action='save',
                domain=domain,
                type='create',
                request='letsencrypt',
                acme_provider="letsencrypt",
                name=name,
                email=email,
                keysize='secp384r1',
                encryption='sha256',
                wildcard=wildcard,
                **domains_dict
        )

    def enable_ssl(self, domain):
        '''Enable SSL for a domain '''        
        return self.cmd_api_domain(
                action='modify',
                domain=domain,
                only_affect='ssl',
                ssl="ON"
        )

    def disable_ssl(self, domain):
        '''Disable SSL for a domain '''        
        return self.cmd_api_domain(
                action='modify',
                domain=domain,
                only_affect='ssl'
        )

    def get_ssl_certificates(self, domain):
        '''Get ssl certificates'''
        return self.cmd_api_ssl(
            domain=domain,
            dnsproviders='no',
            GET_METHOD = True
        )