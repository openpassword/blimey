from distutils.core import setup

setup(name='blimey',
      version='0.9.2',
      description='Library for reading AgileKeychain files',
      author='openpassword',
      url='https://github.com/openpassword/blimey',
      packages=[
          'blimey',
          'blimey.abstract',
          'blimey.agile_keychain',
          'blimey.agile_keychain._manager',
          'blimey.agile_keychain.template',
      ])
