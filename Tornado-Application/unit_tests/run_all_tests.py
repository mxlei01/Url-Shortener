from unittest import TestLoader, TextTestRunner, TestSuite
from unit_tests.tests_executor import TestExecutor
from unit_tests.tests_random_url_generator import TestURLGenerator
from unit_tests.tests_database import TestDB

if __name__ == "__main__":
    loader = TestLoader()

    suite = TestSuite((
            loader.loadTestsFromTestCase(TestExecutor),
            loader.loadTestsFromTestCase(TestURLGenerator),
            loader.loadTestFromTestCase(TestDB)
        ))

    runner = TextTestRunner()
    runner.run(suite)