Contributing to django-tag-fields
=================================

This project is a clone of  `Jazzband <https://github.com/jazzband/django-taggit>`_ project.
By contributing you agree to abide by the `Contributor Code of Conduct
<https://github.com/imAsparky/django-tag-fields/blob/main/CODE_OF_CONDUCT.md>`_.

Thank you for taking the time to contribute to django-tag-fields.

Follow these guidelines to speed up the process.

Reach out before you start
--------------------------

Before opening a new issue, look if somebody else has already started working
on the same issue in the `GitHub issues
<https://github.com/imAsparky/django-tag-fields/issues>`_ and `pull requests
<https://github.com/imAsparky/django-tag-fields/pulls>`_.

Fork the repository
-------------------

Once you have forked this repository to your own GitHub account, install your
own fork in your development environment:

.. code-block:: console

    git clone git@github.com:<your_fork>/django-tag-fields.git
    cd django-tag-fields
    python -m pip install -e .

Running tests
-------------

django-tag-fields uses `tox <https://tox.readthedocs.io/>`_ to run tests:

.. code-block:: console

    tox

Follow style conventions (black, flake8, isort)
-----------------------------------------------

Check that your changes are not breaking the style conventions with:

.. code-block:: console

    tox -e black,flake8,isort

Update the documentation
------------------------

If you introduce new features or change existing documented behavior, please
remember to update the documentation.

The documentation is located in the ``docs`` directory of the repository.

To do work on the docs, proceed with the following steps:

.. code-block:: console

    pip install -r requirements/docs.txt
    sphinx-build -n -W docs docs/_build

Add a changelog line
--------------------

Even when the change is minor, a changelog line is helpful to both describe
the intent of the change, and to give a heads up to people upgrading. You can
add a line in the ``(Unreleased)`` section of ``CHANGELOG.rst``, along with
any more detailed explanations for more complicated changes.

Send pull request
-----------------

It is now time to push your changes to GitHub and open a `pull request
<https://github.com/imAsparky/django-tag-fields/pulls>`_!


Commit/Release process
----------------------

Releases are handled by `python-semantic-release <https://python-semantic-release.readthedocs.io/en/latest/>`_.

.. caution::

    Its important that you DO NOT change the version numbers in the code.
    This will confuse the automatic release updating.

For automatic releases to operate correctly its important to follow the
`Conventional Commits Format <https://www.conventionalcommits.org/en/v1.0.0/>`_.

Conventional commits provides a nice easy to read format in the repository and helps to
find relevent commit information with a quick scan.

|

.. code-block:: vim
    :caption: TLDR: Example of commit message with issue number.

    docs(Contrib): Update README typos #42

    Long description of commit if needed.

    closes #42


``django-tag-fields`` comes with a custom commit message template, see an
excerpt below.

If you would like to use this template, which has some built in help you can
simply update your local git repo with the following command.


.. code-block:: bash

    git config --local commit.template .github/.git-commit-template.txt

|

.. code-block:: vim
    :caption:  Available tags for commit message.

    # Tags with ** will be included in the CHANGELOG

    # **   chore    (a chore that needs to be done)
    #      dbg      (changes in debugging code/frameworks; no production code change)
    #      defaults (changes default options)
    # **   docs      (changes to documentation)
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
