from behave import given, when, then, step
import os
import openpassword

MASTER_PASSWORD = "masterpassword123"


@given('I have a locked keychain')
def step_impl(context):
    context.keychain = _get_keychain()
    assert context.keychain.is_locked() is True


@when('I unlock it')
def step_impl(context):
    context.keychain.unlock(MASTER_PASSWORD)


@then('it will become unlocked')
def step_impl(context):
    assert context.keychain.is_locked() is False


@then('I will be able to see it\'s contents')
def step_impl(context):
    try:
        items = list(context.keychain)
    except TypeError:
        assert False

    if isinstance(items, list):
        assert True
    else:
        assert False


@given('I have an unlocked keychain')
def step_impl(context):
    context.keychain = _get_keychain()
    context.keychain.unlock(MASTER_PASSWORD)
    assert context.keychain.is_locked() is False


@when('I lock the keychain')
def step_impl(context):
    context.keychain.lock()


@then('it will become locked')
def step_impl(context):
    assert context.keychain.is_locked() is True


def _get_keychain():
    return openpassword.AgileKeychain(_get_keychain_path())


def _get_keychain_path():
    current_path = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(current_path, '..', '..', 'tests', 'fixtures', 'test.agilekeychain')
