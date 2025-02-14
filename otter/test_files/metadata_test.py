"""Support for notebook metadata test files"""

import json

from .exception_test import ExceptionTestFile
from .ok_test import OKTestFile

from ..utils import NOTEBOOK_METADATA_KEY


class NotebookMetadataExceptionTestFile(ExceptionTestFile):
    """
    A single notebook metadata test file for Otter.

    Tests are defined in the metadata of a jupyter notebook as a JSON object with the ``otter`` key.
    The tests themselves are assumed to be base-64-encoded compiled ``code`` objects from test files.

    .. code-block:: json

    {
        "metadata": {
            "otter": {
                "tests": {
                    "q1": ""
                }
            }
        }
    }

    Args:
        name (``str``): the name of test file
        path (``str``): the path to the test file
        test_cases (``list`` of ``TestCase``): a list of parsed tests to be run
        value (``int``, optional): the point value of this test, defaults to 1
        all_or_nothing (``bool``, optional): whether the test should be graded all-or-nothing across
            cases

    Attributes:
        name (``str``): the name of test file
        path (``str``): the path to the test file
        test_cases (``list`` of ``TestCase``): a list of parsed tests to be run
        value (``int``): the point value of this test, defaults to 1
        all_or_nothing (``bool``): whether the test should be graded all-or-nothing across
            cases
        passed_all (``bool``): whether all of the test cases were passed
        test_case_results (``list`` of ``TestCaseResult``): a list of results for the test cases in
            ``test_cases``
        grade (``float``): the percentage of ``points`` earned for this test file as a decimal
    """

    @classmethod
    def from_file(cls, path, test_name):
        """
        Parse an exception-based test from a Jupyter notebook's metadata and return an 
        ``ExceptionTestFile``.

        Args:
            path (``str``): the path to the notebook
            test_name (``str``): the name of the test to extract from the metadata

        Returns:
            ``ExceptionTestFile``: the new ``ExceptionTestFile`` object created from the given file
        """
        with open(path) as f:
            nb = json.load(f)

        test_spec = nb["metadata"][NOTEBOOK_METADATA_KEY]["tests"]
        if test_name not in test_spec:
            raise ValueError(f"Test {test_name} not found")

        test_spec = test_spec[test_name]
        return cls.from_string(test_spec, path=path)


class NotebookMetadataOKTestFile(OKTestFile):
    """
    A single notebook metadata test file for Otter.

    Tests are defined in the metadata of a jupyter notebook as a JSON object with the ``otter`` key.
    The tests themselves are OK-formatted.

    .. code-block:: json

    {
        "metadata": {
            "otter": {
                "tests": {
                    "q1": {}
                }
            }
        }
    }

    Args:
        name (``str``): the name of test file
        path (``str``): the path to the test file
        test_cases (``list`` of ``TestCase``): a list of parsed tests to be run
        value (``int``, optional): the point value of this test, defaults to 1
        all_or_nothing (``bool``, optional): whether the test should be graded all-or-nothing across
            cases

    Attributes:
        name (``str``): the name of test file
        path (``str``): the path to the test file
        test_cases (``list`` of ``TestCase``): a list of parsed tests to be run
        value (``int``): the point value of this test, defaults to 1
        all_or_nothing (``bool``): whether the test should be graded all-or-nothing across
            cases
        passed_all (``bool``): whether all of the test cases were passed
        test_case_results (``list`` of ``TestCaseResult``): a list of results for the test cases in
            ``test_cases``
        grade (``float``): the percentage of ``points`` earned for this test file as a decimal
    """

    @classmethod
    def from_file(cls, path, test_name):
        """
        Parse an OK-formatted test from a Jupyter notebook's metadata and return an ``OKTestFile``.

        Args:
            path (``str``): the path to the notebook
            test_name (``str``): the name of the test to extract from the metadata

        Returns:
            ``OKTestFile``: the new ``OKTestFile`` object created from the given file
        """
        with open(path, encoding="utf-8") as f:
            nb = json.load(f)

        test_spec = nb["metadata"][NOTEBOOK_METADATA_KEY]["tests"]
        if test_name not in test_spec:
            raise ValueError(f"Test {test_name} not found")

        test_spec = test_spec[test_name]

        return cls.from_spec(test_spec, path=path)
