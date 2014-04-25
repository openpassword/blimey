

@when('I append new data to the keychain')
def step_impl(context):
        context.keychain.append({
        'username': 'me',
        'password': 'my_awesome_password',
        'no_secret_data': 'some random non secret stuff'
    })

@then('that data should be stored in the agile keychain file structure')
def step_impl(context):
    assert False
