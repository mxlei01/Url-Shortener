from unittest import TestLoader, TextTestRunner, TestSuite
from unit_tests.tests_executor import TestExecutor
from unit_tests.tests_random_url_generator import TestURLGenerator
from unit_tests.tests_database import TestDB
from unit_tests.tests_url_server import TestURLGenHandler

# Uses a testLoader to run multiple tests from different python unit tests file
if __name__ == "__main__":
    loader = TestLoader()

    suite = TestSuite((
            loader.loadTestsFromTestCase(TestExecutor),
            loader.loadTestsFromTestCase(TestURLGenerator),
            loader.loadTestsFromTestCase(TestDB),
            loader.loadTestsFromTestCase(TestURLGenHandler)
        ))

    runner = TextTestRunner()
    runner.run(suite)
