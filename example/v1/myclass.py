from example.v1.myenum import MyEnum
# from example.version_manager import VersionManager

# ver_man = VersionManager()
# ver_man.version_import('myenum', 'MyEnum')

# if 'version' in locals():
#     print('local version: {}'.format(version))
#
# if 'version' in globals():
#     print('global version: {}'.format(version))

class MyClass:
    def __init__(self):
        enum_version = MyEnum.VERSION.value
        print('MyClass is using MyEnum of v{}.'.format(enum_version))
