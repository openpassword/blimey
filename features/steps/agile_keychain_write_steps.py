import os
from openpassword.exceptions import MissingIdAttributeException

TEMP_KEYCHAIN_PATH = os.path.join('tests', 'fixtures', 'temp.agilekeychain')
CORRECT_PASSWORD = "correctpassword"
INCORRECT_PASSWORD = "incorrectpassword"


@when('I append a new password to the keychain')
def step_impl(context):
    context.item_id = '39da7e8b5f0d4f83898e247055dd9ea4'
    item = {
        'id': context.item_id,
        'username': 'me',
        'password': 'my_awesome_password',
        'no_secret_data': 'some random non secret stuff'
    }

    context.keychain.append(item)


@when('I append an item missing a usable id')
def step_impl(context):
    context.exception_was_raised = False

    item = {
        'username': 'me',
        'password': 'my_awesome_password',
        'no_secret_data': 'some random non secret stuff'
    }

    try:
        context.keychain.append(item)
    except MissingIdAttributeException:
        context.exception_was_raised = True


@then('that password should be stored in the agile keychain file structure')
def step_impl(context):
    file_name = "{0}.1password".format(context.item_id)
    item_path = os.path.join(TEMP_KEYCHAIN_PATH, 'data', 'default', file_name)
    item_file = open(item_path, "r")
    assert("some random non secret stuff" in item_file.read())
    item_file.close()
    os.remove(item_path)


@then('a MissingIdAttributeException should be raised')
def step_impl(context):
    if not context.exception_was_raised:
        assert False
