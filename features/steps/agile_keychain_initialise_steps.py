import os
from subprocess import call
import openpassword
from openpassword.exceptions import NonInitialisedKeychainException, KeychainAlreadyInitialisedException


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


@given('I have a non-initialised keychain in "{somepath}"')
def step_impl(context, somepath):
    context.keychain = openpassword.AgileKeychain(somepath)
    context.path = somepath


@when('I initialise it using "{password}"')
def step_impl(context, password):
    context.keychain.initialise(password)


@then('the agile keychain folder structure is created')
def step_impl(context):
        assert os.path.exists(context.path) and os.path.isdir(context.path)

        data_default_dir = os.path.join(context.path, "data", "default")
        assert os.path.exists(data_default_dir) and os.path.isdir(data_default_dir)

        keys_file = os.path.join(data_default_dir, '1password.keys')
        assert os.path.exists(keys_file) and os.path.isfile(keys_file)

        contents_file = os.path.join(data_default_dir, 'contents.js')
        assert os.path.exists(contents_file) and os.path.isfile(contents_file)

        encryption_keys_file = os.path.join(data_default_dir, 'encryptionKeys.js')
        assert os.path.exists(encryption_keys_file) and os.path.isfile(encryption_keys_file)

        call(['rm', '-fr', context.path])


@given('I have a keychain that is already initialised')
def step_impl(context):
    context.keychain = openpassword.AgileKeychain(os.path.join('tests', 'fixtures', 'test.agilekeychain'))


@when('I check it initialisation status')
def step_impl(context):
    context.keychain_initialisations_state = context.keychain.is_initialised()


@then('It should be reported as initialised')
def step_impl(context):
    assert context.keychain_initialisations_state is True


@given('I have an initialised keychain')
def step_impl(context):
    context.keychain = openpassword.AgileKeychain(os.path.join('tests', 'fixtures', 'test.agilekeychain'))


@when('I try to initialise it')
def step_impl(context):
    context.initialisation_failed = False
    try:
        context.keychain.initialise("somepassword")
    except KeychainAlreadyInitialisedException:
        context.initialisation_failed = True


@then('I should get a KeychainAlreadyInitialisedException')
def step_impl(context):
    assert context.initialisation_failed is True
