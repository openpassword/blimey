import openpassword
from openpassword.exceptions import NonInitialisedKeychainException


@given('I have an non-initialised keychain')
def step_impl(context):
    context.keychain = openpassword.AgileKeychain('somepath')


@when('I try to unlock it')
def step_impl(context):
    context.lock_failed = False
    try:
        context.keychain.unlock("somepassword")
    except NonInitialisedKeychainException:
        context.lock_failed = True


@then('I should get a NonInitialisedKeychainException')
def step_impl(context):
    assert context.lock_failed is True


