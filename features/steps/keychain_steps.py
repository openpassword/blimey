from behave import given, when, then, step
import os
import openpassword


@given('I have a locked keychain')
def step_impl(context):
    context.keychain = _get_fixture_path()
    assert context.keychain.is_locked() is True


@when('I unlock it')
def step_impl(context):
    context.keychain.unlock("masterpassword123")


@then('it will become unlocked')
def step_impl(context):
    assert context.keychain.is_locked() is False


@given('I have an unlocked keychain')
def step_impl(context):
    context.keychain = _get_fixture_path()
    context.keychain.unlock("masterpassword123")
    assert context.keychain.is_locked() is False


@when('I request item with id "{id}"')
def step_impl(context, id):
    context.item_unique_id = id
    context.item = context.keychain.get_item_by_unique_id(context.item_unique_id)


@then('I should get an item with the same id')
def step_impl(context):
    assert context.item.uuid == context.item_unique_id


def _get_fixture_path():
    current_path = os.path.dirname(os.path.realpath(__file__))
    fixture_path = current_path + '/../../tests/fixtures/test.agilekeychain'
    return openpassword.AgileKeychain(fixture_path)
