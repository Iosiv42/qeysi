""" Main module. """

import threading
from typing import Generic, TypeVar

from evaluator import Evaluator

T = TypeVar("T")


class MutexVar(Generic[T]):
    """ Wraps some variable into mutex variable.
        I.e. r/w variable with lock for eliminating race condition.
    """

    def __init__(self, inner: T):
        self.lock = threading.Lock()
        self.inner = inner

    @property
    def inner(self) -> T:
        """ Get inner variable using lock. """
        with self.lock:
            return self.__inner

    @inner.setter
    def inner(self, new_inner: T) -> None:
        with self.lock:
            self.__inner = new_inner


class MainApp(threading.Thread):
    """ Class wiht main application. """

    def __init__(self):
        super().__init__()
        self.daemon = True

        self.evaluator = Evaluator()
        self.eval_th = threading.Thread(target=self.__eval, daemon=True)
        self.eval_event = threading.Event()
        self.eval_event.clear()

        self.evaled_source = MutexVar("")
        self.source = MutexVar("")
        self.running = True

    def run(self):
        self.eval_th.start()
        while self.running:
            self.source.inner = input("> ")
            self.eval_event.set()
            self.eval_event.clear()
            self.eval_event.wait()
            print(f"\n    {self.evaled_source.inner}\n")

    def __eval(self):
        while True:
            self.eval_event.wait()

            try:
                self.evaled_source.inner = self.evaluator.evaluate(
                    self.source.inner
                )
            except ValueError as exc:
                self.evaled_source.inner = f"error: {exc}"

            self.eval_event.set()
            self.eval_event.clear()


if __name__ == "__main__":
    app = MainApp()
    app.start()
    app.join()
