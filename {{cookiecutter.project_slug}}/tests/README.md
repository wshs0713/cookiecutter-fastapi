# README

## Framework

- [pytest](https://docs.pytest.org/en/6.2.x/)
- [pytest-cov](https://pytest-cov.readthedocs.io/en/latest/)

## Guide

- All the tests are kept in tests directory.
- The tests directory contains all the tests of the corresponding sub-packages.
- Test files should be named `test_*.py`.
- Test must be a function or a class.
- Test methods and functions should be named `test_*()`.
- Test classes should be named `Test*`.
- Using assert statements.
- Resources
  - Please put the data set or model file needed for the test in cloud storage, do'n push to GitHub.
  - Please mention the download link here.
  - Test code example:
    - If you need to share resources between multiple tests, you can use `conftest`.
    - Download the resources to temp directory for testing:

    ```python
    import tempfile
    import urllib.request
                
    source_url = 'download url'
    file_path = 'test file path'
    with tempfile.TemporaryDirectory() as td:
        urllib.request.urlretrieve(source_url, file_path)
        # Your test goes here.
    ```

## Passing Criteria

- 0 failed.
- coverage > 90%
