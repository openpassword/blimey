from nose.tools import *

from openpassword.item_collection import ItemCollection


class ItemCollectionSpec:
    def it_return_a_filtered_copy_of_itself(self):
        item_collection = ItemCollection(('aa', 'ab', 'ac', 'ad'))

        def f(item):
            return item.startswith('a')

        eq_(item_collection.filter(f), ('aa', 'ab', 'ac', 'ad'))

    def it_allows_chained_filters(self):
        item_collection = ItemCollection(('aa', 'ab', 'ac', 'ad'))

        def f1(item):
            return item.startswith('a')

        def f2(item):
            return item.endswith('b')

        eq_(item_collection.filter(f1).filter(f2), ('ab', ))
