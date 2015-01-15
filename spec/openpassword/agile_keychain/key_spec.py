from unittest.mock import patch
from nose.tools import eq_, raises

from openpassword.agile_keychain._key import Key
from openpassword.exceptions import KeyValidationException


class KeySpec:
    @raises(KeyValidationException)
    def it_throws_a_keyvalidationexception_if_validation_fails(self):
        key = self.get_key()
        key.validate('wrong')

    def it_silently_validates_with_correct_password(self):
        key = self.get_key()
        key.validate('masterpassword123')

    def it_creates_key(self):
        key = Key.create('password', 'SL4', 1000)
        key.validate('password')

        assert key.security_level == 'SL4'
        assert key.iterations == 1000

    def get_key(self):
        return Key({
            'identifier': '123',
            'iterations': 25000,
            'level': 'SL5',
            'data':
                'U2FsdGVkX1+PGVUYaEAHsE6aWEtF1982rnS0hM/+XhjucFsRSoigpJKCg+KGyxybo5/7U84G+PH4LrB9CCj9m+k9HsRO2/mcRU'
                'fPIV0hyLwEyNbmwp29RCmiuqHC4JtfC85VDW+etCIKveyE4ry9N8kHWTFNLbFjymqblcuhw2i1ltocttC09OKyyG03n14xuQsM'
                '1Tj02/I3NYE7yFoml+6eau8knCxpeucNVPu29Ddhy9PkmD0VMyWfqf1Xhsia0DjJvfAbYVCT+M8uYQ8Ouasfee6HwNHPIq4uE+'
                '01rCkhjfIQ2330lBJtWxeQjIkMkvgYDa6zA5Or1glA1pUoollkPiLFdZyVmUXhwp59cZahkVZwjPGnhSkrtMcwha3ncKHUU1B3'
                'vcRyqYYzjbbhgFST4+Y9Cizp1YBTk/G20nIObmuC7Cbt3IMrFaaZ6s7Ml6Fukiy/WFpN/qwMw1L4RnFzwiRxDg7Pxg8+xXWt6N'
                'iAonzmr367nKKgSY3RtbPsY4ik20223jYGnTC7PjOOsEGxCfhdFh825atoOcQhtTOEM80v2JiG7EZvWa2vCZvtrR/KiAZxeNxp'
                'awP46wrHsyzbrlONCsv2tOp2d7+kemP6dkTWauBLpgTmunz9aVak+wi+tZ4W3DRefgvQ9tZdsLN7hPhuKNF6xhszPuBK9LMlFz'
                'Z1NxSum38GMZLqF0lb45jbmhxiJD05vrpJq/Z4LjoBb6/oe0PKmnOPFtwbyCcItfmUCePueRUa2X+/Q7lmyrPQPpx5Q3f0RtQ6'
                'LM0S9l28UOWoGEzReDW45MCAX+67MVXjVBL3N08aUjDHn5RjqFGw3vDKMf1wmvN8DGDfWGGXq5tD7PslMrHn0HDAwrNLpu040m'
                '6InC9DXkk+4vcvPa3T4noz3/tr9/7PXEtQX86FjsiMffqKKm2b4nAAtiJzUfslvbvgcVo6WEffuEDyTd2jveTC6FAu1i4Lk2VE'
                'Vn8Lftv6pc/m6RslOQWjUMm2hs4SQu1h/NFP0M2vYOHiGJY+E7gKyDC6BFozbMcffxHwu0/+S2gHwVs/bc374oNboo40O6WpaC'
                'Qs31FVDmnGtVJ1/ytlR7fylb7DEt/TqR4C0HLnD+dtFriX5KRl0TKFBGG8STlIC6KhTg2ewEVjfiObwqK55OjQtbY0PAmGh0v3'
                'ct3o4ZyKqI4RY1uvTqf0GXJBonD6ng3XkFu+gBTN1Rs67N39QPYoaOXEq1AlVwmLW3uQvmjLusJo/9FnMzpY+tp/7jPO16vMf1'
                'WYOonWhYBWc8TV77e3OJYzIhgk3QUUltL7pt4iL+L6mAaeMPW0dzZ1Y1mUdDyQDNEtAir9cS7nKpuli1GyV+jQNY/W43/1G4UA'
                'MyCPQ8nVmGnKJx7fQK106f+fMixdE5b51uE6',
            'validation':
                'U2FsdGVkX1/TZ7cvOi0EcC7yJeSoYJKUzythkAOyQQnGOSat0IDmEYJ3lOLJLx6iPFxKVxT+2zpG3iQ8OLc3Fj0raer8wbdMa3'
                'wux5VElNssjXNC1W3lfkB9QgPG2QCwpWo1PQnYSMDpJSswuGW670/IgrawV5vzXE1CiZtR82AyI0WNkfdZhMY9TrGmx5z+cYcy'
                'JHsRTFmFuNijfO/myebm+udVSJIgss4Fb0Y6Vq5uGCCqCneEFNy0IV0hIS1m6BlENAZi4zkcm5Aw6DEtdLgGRBb0kg+mU9bLtI'
                'zzAVvPi698oRQBF2zRLMcCkng1avn6E0PYhK4ioiRINMNbIOkmwe6R9r1f/CcTd8ZdymE8crwR9APqxrvim7YjTuA3XrsNT0rf'
                'pkLwVKmxFYXpLPBNJzsOznJKtsgmRwxsl+xkuOVtjD5ousF0484MTAfaVQUh1Ttoz/1Q0D2uuFCOmQu93Nyc17ItaJ8WVbzlIO'
                'Cy6cQHAs5FVB+DLVUBCUeVgwD4fE/NZzXlltsTZJJTNm77byAFErtIC1iYRGKNLQucljMhyO9v8OwIU+0V/gAxLIozdSTWVNu0'
                '03BflhScnXFis+/MzUATeatFbaiF5TRn6LZSQRRakyho734ZYAP/4JNC4HUWlEzJCayZvDbX6X85/fintEWX0cI9Mt5q+g2nqt'
                'PQzhhD0jyIiYe2sTFwbh5iWPb6/Sx7NjZLGICAoTCemIVlEx381DEL1Ey9VozznoZWPzfPCtKvmysKKSMFevQFM4Kp/3Clh6L2'
                'mZBQMvKt73fcHzmJVR9k+IDxSutWGgPJJV2yRy2My5czni3XhTi4WsxNbSBYBSPnqI+qQLj/hovNvd2H958YR4L2viUIatOGDx'
                'FFuoIYefPYzzX5FQBEIh0jT2QkRP5NULKwePzzqD4/sW1Fke99xTAIHnfeJGhNpPNnrM3A8JmoxLPOvCUokb8rOn7RhtGlh9KJ'
                'v2RGDjGZHd66IUtUI4E3HKtxgqO9ZeSo0HWy61R90vuZdybqW8D+XWH4K8WfXTunqjdmrCrAPY0DYuMm8URD89/RoyhF+uzMEV'
                'XOvX807lknUqW2HOgCMqrMj72jyAxLy5+h+81U7Y/2iWHmMffrZvWV33OPN9zViHPGvyZW40K/S9XRF8OZkG6P96u+kO2ipmpy'
                'NcIRDjuYMJFtl3Vr39DXE3nv54/aLNpqhNyKJv1ZBgxXVowcWCjU3TSyijKHRYmpbBeplNE7OKVb8tdxH4RN5S7J5hCaRx3Pyv'
                'WLW4RVPHncL8MfsthrERDiRfZ2t+M3/RP6JC/fawqX0bkABa2cVx+WtZ5MFtDQfXxax00V7eLqVCbAmH/YjEVZmWF6PWH13Vy0'
                'Q5q2GFJfIxRwED8dZXuB1CXj+AILmN2Af+vK'
        })
