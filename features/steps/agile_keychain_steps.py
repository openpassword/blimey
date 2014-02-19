from behave import given, when, then, step
import os
import openpassword
from openpassword.item_collection import ItemCollection
from glob import glob

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


@given('I have an unlocked keychain')
def step_impl(context):
    context.keychain = _get_keychain()
    context.keychain.unlock(MASTER_PASSWORD)
    assert context.keychain.is_locked() is False


@given('the keychain has an item with id "{item_id}"')
def step_impl(context, item_id):
    context.item_id = item_id
    assert len(glob(os.path.join(_get_keychain_path(), 'data', 'default', "{0}.1password".format(context.item_id)))) > 0


@when('I request item with the given id')
def step_impl(context):
    context.item = context.keychain.get_item_by_unique_id(context.item_id)


@then('I should get the item with that id')
def step_impl(context):
    assert context.item.uuid == context.item_id


@given('the keychain has a given number of items')
def step_impl(context):
    context.number_of_items = len(glob(os.path.join(_get_keychain_path(), 'data', 'default', '*.1password')))


@when('I request all items from the keychain')
def step_impl(context):
    context.items = context.keychain.all_items()


@then('I should get a collection with the right number of items')
def step_impl(context):
    assert type(context.items) is ItemCollection
    assert len(context.items) is context.number_of_items


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
