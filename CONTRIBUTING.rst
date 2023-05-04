Contributing to django-tag-fields
=================================

By contributing you agree to abide by the `Contributor Code of Conduct
<https://github.com/imAsparky/django-tag-fields/blob/main/CODE_OF_CONDUCT.md>`_.

Thank you for taking the time to contribute to django-tag-fields.

Follow these guidelines to speed up the process.

Reach out before you start
--------------------------

Before opening a new issue, check if somebody else has already started working
on the same issue in the ``GitHub`` `issues
<https://github.com/imAsparky/django-tag-fields/issues>`_ and `pull requests
<https://github.com/imAsparky/django-tag-fields/pulls>`_.

Fork the repository
-------------------

After forking this repository to your GitHub account, install your fork in your
local development environment.

.. code-block:: console

    # Clone your forked repository
    git clone git@github.com:<your_fork>/django-tag-fields.git

    # Change to the working directory
    cd django-tag-fields

Setup a virtual environment
---------------------------

Use ``venv`` or your preferred virtual environment tool.

Install the dependencies and setup ``pre-commit``.

.. code-block:: console
    :caption: **Create a virtual environment**

    python -m venv venv


.. code-block:: console
    :caption: **Activate your virtual environment, if venv it will be**

    . venv/bin/activate


.. code-block:: console
    :caption: **Install dependencies**

    pip install --upgrade pip
    pip install -r requirements/test.txt
    pip install -r requirements/docs.txt

.. code-block:: console
    :caption: **Setup pre-commit**

    pre-commit install
.. code-block:: console
    :caption: **Install django-tag-fields for local development**

    python -m pip install -e .


Running tests
-------------

django-tag-fields uses `tox <https://tox.readthedocs.io/>`_ to run tests:

.. code-block:: console

    tox


Follow style conventions (black, flake8, isort)
-----------------------------------------------

Check that your changes are not breaking the style conventions with pre-commit.

.. code-block:: console

    git add <your updated files>

    pre-commit

Update the documentation
------------------------

When adding new features or modifying documented behaviour, it is important
to remember to update the corresponding documentation.

You can find the documentation in the "docs" directory of the repository.

To make changes to the documentation, follow these steps.

.. code-block:: console

    sphinx-build -n -W docs docs/_build

Add a changelog line
--------------------

Including a changelog line, even for minor changes, is helpful, as it helps
explain the intention behind the change and alerts users who are upgrading.
To do this, add a line to the ``(Unreleased)`` section of the ``CHANGELOG.rst``
file and any additional details for more complex changes.

Commit/Release process
----------------------

Releases are handled by `python-semantic-release <https://python-semantic-
release.readthedocs.io/en/latest/>`_.

.. caution::

    Its important that you **DO NOT** change the version numbers in the code.
    This will confuse the automatic release updating.

For automatic releases to operate correctly its important to follow the
`Conventional Commits Format <https://www.conventionalcommits.org/en/v1.0.0/>`_.

Conventional commits provides a nice easy to read format in the repository and helps to
find relevent commit information with a quick scan.

.. code-block:: vim
    :caption: TLDR: Example of commit message with issue number.

    docs(Contrib): Update README typos #42

    # Long description of commit if needed.

    closes #42


``django-tag-fields`` comes with a custom commit message template, see an
excerpt below.

If you would like to use this template, which has some built in help you can
simply update your local git repo with the following command.


.. code-block:: bash

    git config --local commit.template .github/.git-commit-template.txt

.. code-block:: vim
    :caption:  Available tags for commit message.

    # Tags with ** will be included in the CHANGELOG

    # **   chore    (a chore that needs to be done)
    #      dbg      (changes in debugging code/frameworks; no production code change)
    #      defaults (changes default options)
    # **   docs     (changes to documentation)
    # **   feat     (new feature)
    # **   fix      (bug fix)
    #      hack     (temporary fix to make things move forward; please avoid it)
    #      license  (edits regarding licensing; no production code change)
    # **   perf     (performance improvement)
    # **   refactor (refactoring code)
    # **   style    (formatting, missing semi colons, etc; no code change)
    # **   test     (adding or refactoring tests; no production code change)
    #      version  (version bump/new release; no production code change)
    #      WIP      (Work In Progress; for intermediate commits to keep patches reasonably sized)
    #      jsrXXX   (patches related to the implementation of jsrXXX, where XXX the JSR number)
    #      jdkX     (patches related to supporting jdkX as the host VM, where X the JDK version)


Send pull request
-----------------

It is now time to push your changes to GitHub and open a `pull request
<https://github.com/imAsparky/django-tag-fields/pulls>`_!

|

Thank you for your contribution.

|
