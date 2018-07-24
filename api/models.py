import datetime

from peewee import *
from .config import Config

database = Config.DATABASE

# monkey patch the DateTimeField to add support for the isoformt which is what
# peewee exports as from DataSet
DateTimeField.formats.append('%Y-%m-%dT%H:%M:%S')
DateField.formats.append('%Y-%m-%dT%H:%M:%S')

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    # Example usage
    #       doc = AdminDocument.create()
    #       doc.apply(request.form)
    #       doc.apply(request.json)
    #       doc.apply(request.json, required=['filename'], dates=['uploaddate'])
    def apply_request(self, source, ignore = None, required = None, dates = None):

        for field in self._meta.get_sorted_fields():
            data = source.get(field)
            if field == "id": continue
            if field in ignore: continue
            # Verify in required_fields
            if field in required and data == None:
                return {'error': 'Empty required field'}
            if field in dates:
                data = "" # strp==]===
            if data is None or data == "": continue
            self.__dict__[field] = data

        return ""

    class Meta:
        database = database

class Users(BaseModel):
    id = CharField(column_name='user_id', null=False)
    username = CharField(column_name='username', null=False)
    password = CharField(column_name='password', null=False)
    email = CharField(column_name='email', null=False)

    class Meta:
        table_name = 'Users'

class Clients(BaseModel):
    id = CharField(column_name='client_id', null=False)
    secret = CharField(column_name='client_secret', null=False)
    name = CharField(column_name='name', null=False)
    description = CharField(column_name='description', null=False)

    user = ForeignKeyField(
        column_name='user_id',
        field='id',
        model=Users,
        null=False)

    @classmethod
    def get_pages(cls):
        pass

    class Meta:
        table_name = 'Clients'

class Tokens(BaseModel):
    token = CharField(column_name='token', null=False)
    refresh_token = CharField(column_name='refresh_token', null=False)
    expiry = DateTimeField(column_name='expiry', null=False)

    client = ForeignKeyField(
        column_name='client_id',
        field='id',
        model=Clients,
        null=False)

    class Meta:
        table_name = 'Tokens'
