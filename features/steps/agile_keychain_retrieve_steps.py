import os
from openpassword import AgileKeychainItem
from openpassword.exceptions import MissingIdAttributeException

TEMP_KEYCHAIN_PATH = os.path.join('tests', 'fixtures', 'temp.agilekeychain')


@given('an item with ID "{item_id}" has been added to the keychain')
def step_impl(context, item_id):
    item = AgileKeychainItem()
    item.id = item_id
    _add_item(context, item)


@given('a number of items is added to the keychain')
def step_impl(context):
    _add_item(context, AgileKeychainItem())
    _add_item(context, AgileKeychainItem())
    _add_item(context, AgileKeychainItem())


@when('I get an item by ID "{item_id}"')
def step_impl(context, item_id):
    if hasattr(context, 'retrieved_items') is False:
        context.retrieved_items = []

    context.retrieved_items.append(context.keychain[item_id])


@then('I should get the added item')
def step_impl(context):
    assert context.retrieved_items[0] == context.added_items[0]


@when('I iterate the items in the keychain')
def step_impl(context):
    if hasattr(context, 'retrieved_items') is False:
        context.retrieved_items = []

    for item in context.keychain:
        context.retrieved_items.append(item)


@then('I should encounter all the added items')
def step_impl(context):
    for item in context.retrieved_items:
        assert item in context.added_items


def _add_item(context, item):
    if hasattr(context, 'added_items') is False:
        context.added_items = []

    context.added_items.append(item)
    context.keychain.append(item)
