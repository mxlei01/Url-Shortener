from concurrent import futures
import executor_settings

# executors.py will create our thread pools, and this can be shared around different python files modules.

# Create a X thread thread pool that we can use to call any synchronous/blocking functions
# defined in the executors_settings.py
executor = futures.ThreadPoolExecutor(executor_settings.worker_count)