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


@when('I request item with id "{id}"')
def step_impl(context, id):
    context.item_unique_id = id
    context.item = context.keychain.get_item_by_unique_id(context.item_unique_id)


@then('I should get an item with the same id')
def step_impl(context):
    assert context.item.uuid == context.item_unique_id


@given('the keychain has 9 items')
def step_impl(context):
    assert len(glob(_get_keychain_path() + "/data/default/*.1password")) is 9


@when('I request all items from the keychain')
def step_impl(context):
    context.items = context.keychain.all_items()


@then('I should get a collection with 9 items')
def step_impl(context):
    assert type(context.items) is ItemCollection
    assert len(context.items) is 9


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
