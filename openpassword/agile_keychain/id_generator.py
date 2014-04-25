import uuid

from openpassword import abstract


class IdGenerator(abstract.IdGenerator):
    def generate_id(self):
        return uuid.uuid4().hex
