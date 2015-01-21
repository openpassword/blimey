import os
from openpassword.agile_keychain.agile_keychain_item import DecryptedItem

TEMP_KEYCHAIN_PATH = os.path.join('tests', 'fixtures', 'temp.agilekeychain')


@given('a new item has been added to the keychain')
def step_impl(context):
    _add_item(context, DecryptedItem.create())


@given('a number of items is added to the keychain')
def step_impl(context):
    _add_item(context, DecryptedItem.create())
    _add_item(context, DecryptedItem.create())
    _add_item(context, DecryptedItem.create())


@when('I get an item by the same id')
def step_impl(context):
    if hasattr(context, 'retrieved_items') is False:
        context.retrieved_items = []

    item = context.keychain[context.added_items[0]]
    context.retrieved_items.append(item['uuid'])


@then('I should get the added item')
def step_impl(context):
    assert context.retrieved_items[0] == context.added_items[0]


@when('I iterate the items in the keychain')
def step_impl(context):
    if hasattr(context, 'retrieved_items') is False:
        context.retrieved_items = []

    for item in context.keychain:
        context.retrieved_items.append(item['uuid'])


@then('I should encounter all the added items')
def step_impl(context):
    for item in context.retrieved_items:
        assert item in context.added_items


def _add_item(context, item):
    if hasattr(context, 'added_items') is False:
        context.added_items = []

    context.added_items.append(item['uuid'])
    context.keychain.append(item)
