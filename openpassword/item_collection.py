class ItemCollection(tuple):
    def filter(self, callback):
        return ItemCollection([item for item in self if(callback(item))])
