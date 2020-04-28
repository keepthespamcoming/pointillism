import uuid
from ldapauth.base import LDIFRecord

PT_SESSION_TOKEN = 'employeeNumber'
SESSION = 'initials'
GIT_TOKEN = 'givenName'
BALANCE = 'facsimileTelephoneNumber' # Fax
SUBSCRIBED = 'telexNumber'


class GitHubUser(LDIFRecord):
    type = 'cn'
    attributes = ['sn', 'cn', 'description', GIT_TOKEN, PT_SESSION_TOKEN, BALANCE]

    def __init__(self, *users):
        self.users = users

    @classmethod
    def create(cls, *node, **attributes):
        eid = attributes.get(PT_SESSION_TOKEN, str(uuid.uuid4()))
        attributes[PT_SESSION_TOKEN] = eid

        return super(GitHubUser, cls).create(*node, **attributes)

    @classmethod
    def first(cls, cn, **attributes):
        base_dn = 'dc=ipsumllc,dc=com' # cls.base_dn
        search_filter = f'(cn={cn})'

        response = cls._search(base_dn, search_filter, **attributes)
        return next(iter([User(**args) for args in response]))

    @classmethod
    def find(cls, token=None, **attributes):
        base_dn = 'dc=ipsumllc,dc=com' # cls.base_dn
        # if 'base_dn' in attributes:
        #     base_dn = ','.join((attributes['base_dn'], base_dn))
        # f'(&(objectClass={cls.type_name()})({search}))'

        filters = []
        if token:
            filters.append(f'({GIT_TOKEN}={token})')

        if attributes.get('email'):
            email = attributes.get('email')
            filters.append(f'(mail={email})')

        search_filter = ''.join(filters)
        # search_filter = f'(&{search_filter})'
        response = cls._search(base_dn, search_filter, **attributes)
        return list([User(**args) for args in response])


class User:
    """
    github token: givenName
    p.io token: employeeNumber
    """
    def __init__(self, **record):
        self.record = record
        self.dn = record.get('dn')
        attrs = record.get('attributes', {})
        self.name = next(iter(attrs.get('cn', [])), None)
        self.cn = next(iter(attrs.get('cn', [])), None)
        self.git_token = attrs.get(GIT_TOKEN, [])
        self.email = attrs.get('mail')
        if len(self.git_token) > 0:
            self.git_token = self.git_token[-1]
        else:
            self.git_token = None
        self.token = attrs.get(PT_SESSION_TOKEN)
        if self.token:
            self.token = self.token[-1]
        else:
            self.token = None
        self.balance = attrs.get(BALANCE, 0)
        if isinstance(self.balance, list):
            if len(self.balance) > 0:
                self.balance = self.balance[-1]
            else:
                self.balance = 0
        self.balance = int(self.balance)
        self.subscribed = attrs.get(SUBSCRIBED) == 'true'

    def is_active(self):
        return True

    def is_authentic(self, session_token):
        return session_token == self.token

    def as_json(self):
        return dict(
            github_name=self.name,
            email=self.email,
            balance=self.balance,
            status=self.status
        )

    @property
    def status(self):
        if self.subscribed:
            return 'subscribed'

        return 'expired'

    def __str__(self):
        return f'User<{self.name}>'

    def __repr__(self):
        return f'User<{self.name}>'
