from nose.tools import *
from openpassword import EncryptionKeyRepository


class EncryptionKeyRepositorySpec:
    def setUp(self):
        keys = {
            "SL3": "BE4CC37CD7C044E79B5CC1CC19A82A13",
            "SL5": "98EB2E946008403280A3A8D9261018A4",
            "list": [
                {
                    "data": "U2FsdGVkX1+PGVUYaEAHsE6aWEtF1982rnS0hM/+XhjucFsRSoigpJKCg+KGyxybo5/7U84G+PH4LrB9CCj9m+k9HsRO2/mcRUfPIV0hyLwEyNbmwp29RCmiuqHC4JtfC85VDW+etCIKveyE4ry9N8kHWTFNLbFjymqblcuhw2i1ltocttC09OKyyG03n14xuQsM1Tj02/I3NYE7yFoml+6eau8knCxpeucNVPu29Ddhy9PkmD0VMyWfqf1Xhsia0DjJvfAbYVCT+M8uYQ8Ouasfee6HwNHPIq4uE+01rCkhjfIQ2330lBJtWxeQjIkMkvgYDa6zA5Or1glA1pUoollkPiLFdZyVmUXhwp59cZahkVZwjPGnhSkrtMcwha3ncKHUU1B3vcRyqYYzjbbhgFST4+Y9Cizp1YBTk/G20nIObmuC7Cbt3IMrFaaZ6s7Ml6Fukiy/WFpN/qwMw1L4RnFzwiRxDg7Pxg8+xXWt6NiAonzmr367nKKgSY3RtbPsY4ik20223jYGnTC7PjOOsEGxCfhdFh825atoOcQhtTOEM80v2JiG7EZvWa2vCZvtrR/KiAZxeNxpawP46wrHsyzbrlONCsv2tOp2d7+kemP6dkTWauBLpgTmunz9aVak+wi+tZ4W3DRefgvQ9tZdsLN7hPhuKNF6xhszPuBK9LMlFzZ1NxSum38GMZLqF0lb45jbmhxiJD05vrpJq/Z4LjoBb6/oe0PKmnOPFtwbyCcItfmUCePueRUa2X+/Q7lmyrPQPpx5Q3f0RtQ6LM0S9l28UOWoGEzReDW45MCAX+67MVXjVBL3N08aUjDHn5RjqFGw3vDKMf1wmvN8DGDfWGGXq5tD7PslMrHn0HDAwrNLpu040m6InC9DXkk+4vcvPa3T4noz3/tr9/7PXEtQX86FjsiMffqKKm2b4nAAtiJzUfslvbvgcVo6WEffuEDyTd2jveTC6FAu1i4Lk2VEVn8Lftv6pc/m6RslOQWjUMm2hs4SQu1h/NFP0M2vYOHiGJY+E7gKyDC6BFozbMcffxHwu0/+S2gHwVs/bc374oNboo40O6WpaCQs31FVDmnGtVJ1/ytlR7fylb7DEt/TqR4C0HLnD+dtFriX5KRl0TKFBGG8STlIC6KhTg2ewEVjfiObwqK55OjQtbY0PAmGh0v3ct3o4ZyKqI4RY1uvTqf0GXJBonD6ng3XkFu+gBTN1Rs67N39QPYoaOXEq1AlVwmLW3uQvmjLusJo/9FnMzpY+tp/7jPO16vMf1WYOonWhYBWc8TV77e3OJYzIhgk3QUUltL7pt4iL+L6mAaeMPW0dzZ1Y1mUdDyQDNEtAir9cS7nKpuli1GyV+jQNY/W43/1G4UAMyCPQ8nVmGnKJx7fQK106f+fMixdE5b51uE6\u0000",  # nopep8
                    "validation": "U2FsdGVkX1/TZ7cvOi0EcC7yJeSoYJKUzythkAOyQQnGOSat0IDmEYJ3lOLJLx6iPFxKVxT+2zpG3iQ8OLc3Fj0raer8wbdMa3wux5VElNssjXNC1W3lfkB9QgPG2QCwpWo1PQnYSMDpJSswuGW670/IgrawV5vzXE1CiZtR82AyI0WNkfdZhMY9TrGmx5z+cYcyJHsRTFmFuNijfO/myebm+udVSJIgss4Fb0Y6Vq5uGCCqCneEFNy0IV0hIS1m6BlENAZi4zkcm5Aw6DEtdLgGRBb0kg+mU9bLtIzzAVvPi698oRQBF2zRLMcCkng1avn6E0PYhK4ioiRINMNbIOkmwe6R9r1f/CcTd8ZdymE8crwR9APqxrvim7YjTuA3XrsNT0rfpkLwVKmxFYXpLPBNJzsOznJKtsgmRwxsl+xkuOVtjD5ousF0484MTAfaVQUh1Ttoz/1Q0D2uuFCOmQu93Nyc17ItaJ8WVbzlIOCy6cQHAs5FVB+DLVUBCUeVgwD4fE/NZzXlltsTZJJTNm77byAFErtIC1iYRGKNLQucljMhyO9v8OwIU+0V/gAxLIozdSTWVNu003BflhScnXFis+/MzUATeatFbaiF5TRn6LZSQRRakyho734ZYAP/4JNC4HUWlEzJCayZvDbX6X85/fintEWX0cI9Mt5q+g2nqtPQzhhD0jyIiYe2sTFwbh5iWPb6/Sx7NjZLGICAoTCemIVlEx381DEL1Ey9VozznoZWPzfPCtKvmysKKSMFevQFM4Kp/3Clh6L2mZBQMvKt73fcHzmJVR9k+IDxSutWGgPJJV2yRy2My5czni3XhTi4WsxNbSBYBSPnqI+qQLj/hovNvd2H958YR4L2viUIatOGDxFFuoIYefPYzzX5FQBEIh0jT2QkRP5NULKwePzzqD4/sW1Fke99xTAIHnfeJGhNpPNnrM3A8JmoxLPOvCUokb8rOn7RhtGlh9KJv2RGDjGZHd66IUtUI4E3HKtxgqO9ZeSo0HWy61R90vuZdybqW8D+XWH4K8WfXTunqjdmrCrAPY0DYuMm8URD89/RoyhF+uzMEVXOvX807lknUqW2HOgCMqrMj72jyAxLy5+h+81U7Y/2iWHmMffrZvWV33OPN9zViHPGvyZW40K/S9XRF8OZkG6P96u+kO2ipmpyNcIRDjuYMJFtl3Vr39DXE3nv54/aLNpqhNyKJv1ZBgxXVowcWCjU3TSyijKHRYmpbBeplNE7OKVb8tdxH4RN5S7J5hCaRx3PyvWLW4RVPHncL8MfsthrERDiRfZ2t+M3/RP6JC/fawqX0bkABa2cVx+WtZ5MFtDQfXxax00V7eLqVCbAmH/YjEVZmWF6PWH13Vy0Q5q2GFJfIxRwED8dZXuB1CXj+AILmN2Af+vK\u0000",  # nopep8
                    "level": "SL3",
                    "identifier": "BE4CC37CD7C044E79B5CC1CC19A82A13",
                    "iterations": 25000
                },
                {
                    "data": "U2FsdGVkX19CNF/5SazpsyC2/axBCsrpy1MBjTuulGu+hQgbMAT3COZgxGOfLUKG7VypKI/LpD3I5VxUP2NiIBqqLolwkTpQW79NJOUYlqv+3argoTwz4JL9j4wyay4BJbclVkZMY8xn+UXf8TlSffLMj3aWbXqfv10stbPI8S9DzAQ/0rYFCHP83E82NueF6t7RXk9PZcsprqFcQpxdU0lxTWT5fJZscwdYy/M88bVgnTHfIwI1V9RxxAKj0lDkUBppCrkGhN7pWP4mvCR1+iI9xTAxASH5WQxNp7v+9T5btNK0hpe3532fuVbhEJ6XVVTbRMEJRYAGNXp4TOc0q8yaW//eSPCs/S/eYw6Dnai4MA0IZqpdydj7viaPrQR/z18Dv3jKq0K+E0fh8wn/EHrrIvhQofdyaX6slqIVx7jI9Mi7BGNz6qKeIZXdQekXiY9F1vxTsaMXtzRCO79id3rI/UmuBtTVmQ7kV/RVErWfxU98oDFTbMqqS4J59PMqfhamlBFlv5nfsC/oKPZrROdxG69RT7upWSLiN02PS3eIjgfEWfdDNInppwWv9ig/QZ3eeiVVSAcWqr6+zlXpXLTKV0T9pBWe4Rq2cCTs32XQvz+3BphlKtSeUm50aL/ftiml1hv39Ks44JIwsZzFtXF3LhZVqwUFJsk+fdT3qDtxcEjuOuQ/TauPSUdD6duD0YjMBKroRefGAxyrFCZ1gWHRLdLxRTu0JQUmhxN+T8AHoDJSY4KvNjaCFsxFLPbGLqT3zds7RjrAdchC/swhwG9iOsOU8qpaI7Ew1YVQ8d0Ms+SdSz/JCzuoIiaKigsIXvH6/BOwoTdM46qZIe+KgqbsOJc7YOMsuZosEacYwvD1LQ5waklXP8h/0LnbVnw0sCLc/h3JX78sWNWBJjnvT29oCDrALzlNbFrsjtubn27IZWhVeIqnN7cxLlbDgunK2FZsNJr1r5ACxwGMiC/klT3uZWQyyNkLCZkReQ8N9utskSFrhs9pv+lFDvWcfUbQfPt8GeP/C8fSdxHAA3DLtzlVcajaNHXF2zdofetZfSOS9y9pvbt6IuFrcNmMqlZQu3f7Tvvga3rSmqK8v08UiV8/KTxIqJ9oVS+/tFPe+aYGL9dJG9I2f7Yo9H8OvgNLDqK1tfULTppAdWpq863XxVz/MV6AP+bIRXuy9jviKjRrT2h2KVPM1fx3Fy0efYro3FzLQlu86iVtQqn64zPGWP1Sfph2/IeRiCsFh+wKc6k/5X0TZEbsWpk0RRFN855SUYSUXgNwPqCHnS91zTm4f28CJ/mXqtdu9Y1wzwB/wTSilp4huyg5GkXyk+ZNuH7wqsOkdr8+Qg2Ckylh8hX18KVmP6DZ2EW+mykjzKkMXuLC6t4U89VtsUm4S8uX3rY5\u0000",  # nopep8
                    "validation": "U2FsdGVkX19YMZ3cXoetbbnP+uMx6orlxhjYLIKtQxZnwqaN9A/NaF26+8gJPc/Ow7MubfnwX0ja0kgkRtrLVVonteZRYjoWhNi6ksg1YOWGUhO61PoUxHqJ7ZMPkn9XQw2dfNjfvi/CSVRcO4wUEBHzGGn+josnmknS2O8qQrUOysSYgsk3nSFByaFYEp4oKDTJePVeWUgiy9ytGynWPzaeye8SxXymwo7le9ufNSFjGiUqwaKmLoyzCBRQXe5PPbSHl9wqZ7AePCMA5gt8DRKXcC8MKrWHQqGZPmwfJlkP/0PWPrpam90JnnKOH8pWwoIR+zeDZSZxpENhuaLgxLoq9MVBs5t/nO1kMZFepTMu2JBOo4nguFFEJ+Br/H5m0ith88q80/Xeq2c3tUImKlE6GzFVCR2aFhiZnT/ZTbS8jt1ac/ygfXofuP1b2lNWK7WjwFz8GHtVMVT3NuSG6TN+LbpQwzVu9ofQ/ijXn9fe40OM4CDOm1fZrLK+NzdmmFKrD2wzcMultBp2bDJ0dL6xueNeVHDUjgLq1zjL1bHoi3aBqBrJuzyHBZ9VU4d5DT5ct78bT+df29kgbD3PA4wBsVEhCVbR+m/r21IVHv44BxCMV/eCIdLcsNSY4Nv7R/E9ppYlKx056hrfjOhkrlEIOOWqjzXFlJ1XVLjwv8JIb8QaovXNZ9B/6l1yCjtzeR5WXRtEG0d4aC61TKfHCGiasMZXbgzEg/UIk2cwecl8dhPqrPdysvlxLKKldX6kD7v8tISe/JwkfjiLZoiHUzN+P857KrNldWVBnL84cJAHQCs95fxK/d8G9VUr9SBcbuuz/qKdp9qM+ooi3yZZOrXSKxJIclXWGwwZmo9T9DDlRBi7D0kzjNvmxjoWk/8LD78tF6YcqSxuogQut+JSGisXut460iX8GPzhjSKtsieA7fMynWlrFnUdEkPtgkSwJidxkWF7RjhP48iyLFDWET4aGtIJN0VbNf6c74i4EIvQIeOmVIuPaSUhmHePm4jZiC/j0zxQ/kP9Q20aM+VJV2x3D/ege3l+OrpeE/Tom0OLNzdVNtLALW9lHD3hqFbYl+hSwNT8/KbRherIYhJJo+5fK5A4EuHf6KCuKliePIAGVLbk/mCkKSnBuRh9O6zfmnnzOlsrtnuLoFXJQgp12gJFzIIOV0jNiwnQB4slxhbzySzv7kaZZWbzWqRVEbRxxZJsxhsTOpN3nOuhRCO2iE7hiRQwO5zw2MJ5uoA2PUtsLoo0R5C3kNEwTgL5IZnEa08ca7ogP9SSj58umqen3TLj48VcYJeXL7n6av2eDLDeQQLQkZoYN+D5U14IpYE2+mUKoaocQffAYeRx7eDgccPE8fVfpvfg98xD+9UXSS8OS7WZeeZHOxoIOQVj/3xb\u0000",  # nopep8
                    "level": "SL5",
                    "identifier": "98EB2E946008403280A3A8D9261018A4",
                    "iterations": 25000
                }
            ]
        }

        self.key_repository = EncryptionKeyRepository(keys)

    def it_returns_encryption_key_for_given_security_level(self):
        sl3 = self.key_repository.key_for_security_level("SL3")
        sl5 = self.key_repository.key_for_security_level("SL5")

        eq_(sl3["identifier"], "BE4CC37CD7C044E79B5CC1CC19A82A13")
        eq_(sl5["identifier"], "98EB2E946008403280A3A8D9261018A4")
