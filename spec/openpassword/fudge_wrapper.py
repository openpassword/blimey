import fudge
import inspect


class MethodNotAvailableInMockedObjectException(Exception):
    pass


def getMock(class_to_mock):
    return FudgeWrapper(class_to_mock)


class FudgeWrapper(fudge.Fake):
    def __init__(self, class_to_mock):
        self._class_to_mock = class_to_mock
        self._declared_calls = {}
        self._attributes = {}
        super(FudgeWrapper, self).__init__(self._class_to_mock.__name__)

    def provides(self, call_name):
        self._check_method_availability_on_mocked_object(call_name)
        super(FudgeWrapper, self).provides(call_name)

    def _check_method_availability_on_mocked_object(self, call_name):
        if call_name not in dir(self._class_to_mock):
            raise MethodNotAvailableInMockedObjectException
