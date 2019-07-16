import signal
from multiprocessing import Semaphore, Pool

from image_pipeline.task_generator import TaskGenerator
from image_pipeline.configuration import Configuration, SourceDirectory


class TaskExecutor:

    def __init__(self, configuration: Configuration):
        self._configuration = configuration
        self._stop = False
        if self._configuration.multiprocessing.active:
            self._workers = Semaphore(self._configuration.multiprocessing.processes + 1)
            self._pool = Pool(processes=self._configuration.multiprocessing.processes)

    def start(self, task_generator: TaskGenerator):
        for task in task_generator:
            if self._stop:
                self.stop()
                break
            if self._configuration.multiprocessing.active:
                self._workers.acquire()
                self._pool.apply_async(task.run_task, callback=self._task_done)
            else:
                task.run_task()
        self.stop()

    def stop(self):
        self._stop_multiprocessing()

    def _task_done(self, callback_value):
        self._workers.release()

    def _stop_multiprocessing(self):
        if self._configuration.multiprocessing.active:
            self._pool.close()
            self._pool.join()

    def _set_stop_signal_handler(self):
        signal.signal(signal.SIGTERM, self._handle_stop_signal)

    def _handle_stop_signal(self, signum, frame):
        self._stop = True

