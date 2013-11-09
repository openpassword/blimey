## The Development Philosophy

OpenPassword is developed under the MIT license, which means it's Open Source and that we're accepting contributions to the project.

If you're thinking about contributing to OpenPassword, this page is the place to start.

We try to build OpenPassword as a robust piece of software, with a simple and elegant design. To try and achieve this we apply the principles of emergent design, and expect contributions to do so as well.

Quoting "The RSpec Book":

> "BDD calls Test-Driven Development coding by example, which places emphasis on using examples to drive out the behaviour of the code. The fact that these examples become tests once the code is written is a secondary concern"

So, what does this mean in the context of OnePassword?
It means that we couldn't care less about "code coverage" or writing tests for the sake of doing it.
It means that we write examples of how we imagine our code will be used, before writing our code, and then we write the minimum amount of code to make the expectations of those examples to pass.
It means that we don't do a lot of upfront design, instead, we let it emerge as a response to our examples.

The consequences of this are often: small, simple and clean methods and classes. Responsibility separation in methods and classes. Injection of dependencies. And a number of other advantages that become clear as the software progresses.

## Tools

OpenPassword is developed in **Python 3**. We try to keep the number of dependencies low, so currently we're using the following tools to help us achieve our goals:

* nose - A testing framework for Python
* spec - A nose plugin to allow for a more BBD like output
* fudge - A mocking framework for Python
* tissue - A nose plugin to check code for PEP8 style violations
* pbkdf2 - A python library for implementing the [Password-Based Key Derivation Function 2](http://en.wikipedia.org/wiki/PBKDF2)
* pycrypto - A python cryptography library

To install node you'll need to run pip. Depending on your setup, you pip executable might be called pip or pip3:

`pip3 install nose`

For the remaining tools, you can take advantage of the requirements.txt contained in the repository:

`pip3 install -r requirements.txt --use-mirrors`

## Writing a feature

WIP

## Running the examples

To run the examples you'll just need to run nose, as all the options are already taken care of by the setup.cfg file:

`nosetests`

## Making pull requests

Before making a pull request, be sure to run nose to make sure all the specs are still passing. It's advisable, as well, to check for code styling issues using pep8:

 `pep8 --statistics --count --show-source --format=default`

Both specs and code should follow the pep8 standards.

To make this easier, we provide a git_hooks folder that contains a pre-commit hook, that will do the work for you. Just copy it to your repository git hooks folder. From the base folder of your repository do:

`cp ./git_hooks/pre_commit .git/hooks`
