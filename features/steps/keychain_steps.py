from behave import given, when, then, step
import os
import openpassword
from openpassword.item_collection import ItemCollection
from glob import glob


@given('I have a locked keychain')
def step_impl(context):
    context.keychain = _get_keychain()
    assert context.keychain.is_locked() is True


@when('I unlock it')
def step_impl(context):
    context.keychain.unlock("masterpassword123")


@then('it will become unlocked')
def step_impl(context):
    assert context.keychain.is_locked() is False


@given('I have an unlocked keychain')
def step_impl(context):
    context.keychain = _get_keychain()
    context.keychain.unlock("masterpassword123")
    assert context.keychain.is_locked() is False


@given('the keychain has an item with id "{item_id}"')
def step_impl(context, item_id):
    context.item_id = item_id
    assert len([a for a in glob(_get_keychain_path() + "/data/default/*.1password") if
                a.endswith(context.item_id + ".1password") > 0])


@when('I request item with the given id')
def step_impl(context):
    context.item = context.keychain.get_item_by_unique_id(context.item_id)


@then('I should get the item with that id')
def step_impl(context):
    assert context.item.uuid == context.item_id


@given('the keychain has a given number of items')
def step_impl(context):
    context.keychain_len = len(glob(_get_keychain_path() + "/data/default/*.1password"))


@when('I request all items from the keychain')
def step_impl(context):
    context.items = context.keychain.all_items()


@then('I should get a collection with the right number of items')
def step_impl(context):
    assert type(context.items) is ItemCollection
    assert len(context.items) is context.keychain_len


@when('I lock the keychain')
def step_impl(context):
    context.keychain.lock()


@then('it will become locked')
def step_impl(context):
    assert context.keychain.is_locked() is True


def _get_keychain():
    current_path = os.path.dirname(os.path.realpath(__file__))
    fixture_path = current_path + '/../../tests/fixtures/test.agilekeychain'
    return openpassword.AgileKeychain(fixture_path)


def _get_keychain_path():
    current_path = os.path.dirname(os.path.realpath(__file__))
    return current_path + '/../../tests/fixtures/test.agilekeychain'
