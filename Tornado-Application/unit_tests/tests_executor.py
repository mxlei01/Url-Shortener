import tornado
from tornado.testing import AsyncTestCase
from executor_thread_pool.executor import executor

class TestExecutor(AsyncTestCase):
    @tornado.testing.gen_test
    def test_executor_math(self):
        # Usage:
        #       Test Case to yield a executor submit task of a mathematical function
        #       and see the correctness
        # Arguments:
        #       None

        result = yield executor.submit(pow, 2, 2)
        self.assertEqual(result, 4)