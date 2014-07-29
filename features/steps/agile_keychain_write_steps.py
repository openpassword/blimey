import os
from openpassword.exceptions import MissingIdAttributeException


@when('I append new data to the keychain')
def step_impl(context):
    context.item_id = '39da7e8b5f0d4f83898e247055dd9ea4'
    item = {
        'id': context.item_id,
        'username': 'me',
        'password': 'my_awesome_password',
        'no_secret_data': 'some random non secret stuff'
    }

    context.keychain.append(item)


@then('that data should be stored in the agile keychain file structure')
def step_impl(context):
    file_name = "{0}.1password".format(context.item_id)
    item_file = open(os.path.join('tests', 'fixtures', 'test.agilekeychain', 'data', 'default', file_name), "r")
    assert("some random non secret stuff" in item_file.read())
    item_file.close()
    os.remove(os.path.join('tests', 'fixtures', 'test.agilekeychain', 'data', 'default', file_name))


@when('I append data missing a usable id')
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


@then('a MissingIdAttributeException should be raised')
def step_impl(context):
    if not context.exception_was_raised:
        assert False
