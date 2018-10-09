import asyncio
from gettext import gettext as _


# Not changed at all from pulpcore
class Stage:
    """
    The base class for all Stages API stages.

    To make a stage, inherit from this class and implement :meth:`__call__` on the subclass.
    """

    async def __call__(self, in_q, out_q):
        """
        The coroutine that is run as part of this stage.

        Args:
            in_q (:class:`asyncio.Queue`): The queue to receive items from the previous stage.
            out_q (:class:`asyncio.Queue`): The queue to put handled items into for the next stage.

        Returns:
            The coroutine that runs this stage.

        """
        raise NotImplementedError(_('A plugin writer must implement this method'))

    @staticmethod
    async def batches(in_q, minsize=1):
        """
        Asynchronous iterator yielding batches of :class:`DeclarativeContent` from `in_q`.

        The iterator will try to get as many instances of
        :class:`DeclarativeContent` as possible without blocking, but
        at least `minsize` instances.

        Args:
            in_q (:class:`asyncio.Queue`): The queue to receive
                :class:`~pulpcore.plugin.stages.DeclarativeContent` objects from.
            minsize (int): The minimum batch size to yield (unless it is the final batch)

        Yields:
            A list of :class:`DeclarativeContent` instances

        Examples:
            Used in stages to get large chunks of declarative_content instances from
            `in_q`::

                class MyStage(Stage):
                    async def __call__(self, in_q, out_q):
                        async for batch in self.batches(in_q):
                            for declarative_content in batch:
                                # process declarative content
                                await out_q.put(declarative_content)
                        await out_q.put(None)

        """
        batch = []
        shutdown = False

        def add_to_batch(batch, content):
            if content is None:
                return True
            batch.append(content)
            return False

        while not shutdown:
            content = await in_q.get()
            shutdown = add_to_batch(batch, content)
            while not shutdown:
                try:
                    content = in_q.get_nowait()
                except asyncio.QueueEmpty:
                    break
                else:
                    shutdown = add_to_batch(batch, content)
            if batch and (len(batch) >= minsize or shutdown):
                yield batch
                batch = []


class StartEmit2(Stage):
    """
    Starts without an in_q, emits to 2 different out_qs.
    """
    async def __call__(self, even_out, odd_out):
        for i in range(1, 10):
            if i % 2 == 0:
                await even_out.put(i)
            else:
                await odd_out.put(i)
        await even_out.put(None)
        await odd_out.put(None)


class EvenInOddOut(Stage):
    async def __call__(self, even_in, odd_out):
        while True:
            even = await even_in.get()
            if even is None:
                break
            # Extra digits will show which q it went through.
            new_odd = (even * 1000) + 1
            await odd_out.put(new_odd)
        await odd_out.put(None)


class ConfluenceStage(Stage):
    async def __call__(self, jack_in, walter_in, together_out):
        self._pending = set()
        self._finished = set()
        jack_task = self.add_to_pending(jack_in.get())
        walter_task = self.add_to_pending(walter_in.get())
        open_jack = True
        open_walter = True
        while open_jack or open_walter:
            done, self._pending = await asyncio.wait(
                self._pending,
                return_when=asyncio.FIRST_COMPLETED
            )
            self._finished = self._finished.union(done)

            while self._finished:
                in_from_one_of_em = self._finished.pop()
                if in_from_one_of_em.result() is None:
                    if in_from_one_of_em is jack_task:
                        open_jack = False
                    elif in_from_one_of_em is walter_task:
                        open_walter = False
                else:
                    if in_from_one_of_em is jack_task:
                        # TODO one bit of slop, this happens even when the whole task is finished,
                        # leaving doomed in.get()s in _pending.
                        jack_task = self.add_to_pending(jack_in.get())
                    elif in_from_one_of_em is walter_task:
                        walter_task = self.add_to_pending(walter_in.get())
                    await together_out.put(in_from_one_of_em.result())

        # After both inputs are finished (2 Nones) we close this stage
        await together_out.put(None)

    def add_to_pending(self, coro):
        task = asyncio.ensure_future(coro)
        self._pending.add(asyncio.ensure_future(task))
        return task


class SanityStage(Stage):
    async def __call__(self, out_q):
        for i in range(10):
            await out_q.put(i)
        await out_q.put(None)


class DidItWorkStage(Stage):
    async def __call__(self, in_q):
        while True:
            log_it = await in_q.get()
            if log_it is not None:
                print(log_it)
            else:
                break


async def create_sync_pipeline(maxsize=100):
    futures = []

    even_out = asyncio.Queue()
    odd_out = asyncio.Queue()
    start = StartEmit2()
    futures.append(asyncio.ensure_future(start(even_out, odd_out)))

    even_in = even_out
    second_odd_out = asyncio.Queue()
    make_odd = EvenInOddOut()
    futures.append(asyncio.ensure_future(make_odd(even_in, second_odd_out)))

    jack_in = odd_out
    walter_in = second_odd_out
    together_out = asyncio.Queue()
    confluence = ConfluenceStage()
    futures.append(asyncio.ensure_future(confluence(jack_in, walter_in, together_out)))

    # sanity_stage = SanityStage()
    # basic_shit = asyncio.Queue()
    # futures.append(asyncio.ensure_future(sanity_stage(basic_shit)))

    # in_q = odd_out
    # in_q = basic_shit
    in_q = together_out
    omg_please = DidItWorkStage()
    futures.append(asyncio.ensure_future(omg_please(in_q)))

    try:
        await asyncio.gather(*futures)
    except Exception:
        # One of the stages raised an exception, cancel all stages...
        pending = []
        for task in futures:
            if not task.done():
                task.cancel()
                pending.append(task)
        # ...and run until all Exceptions show up
        if pending:
            await asyncio.wait(pending, timeout=60)
        raise


def start_that_thing(pipeline):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(pipeline)


def main(remote_pk=None, repository_pk=None):
    """
    All we are going to do is n
    """
    pipeline = create_sync_pipeline()
    start_that_thing(pipeline)


main()
