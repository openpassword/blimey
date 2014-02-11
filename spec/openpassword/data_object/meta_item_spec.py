from nose.tools import *
from openpassword.data_object import MetaItem
from openpassword.exceptions import InvalidMetadataException


class MetaItemSpec:
    def it_is_created_with_a_title(self):
        data = {'title': "mega meta item", 'unique_id': 'random unique id'}
        meta_item = MetaItem(data)
        eq_(meta_item.title, "mega meta item")

    def it_is_created_with_an_unique_id(self):
        data = {'unique_id': "123456", 'title': 'random title'}
        meta_item = MetaItem(data)
        eq_(meta_item.unique_id, "123456")

    @raises(InvalidMetadataException)
    def it_raises_invalidmetadataexception_when_required_data_is_missing(self):
        data = {}
        MetaItem(data)
