from stages import Stage

import logging
log = logging.getLogger("DummyStage")


class SanityStage(Stage):
    async def __call__(self, out_q):
        for i in range(10):
            await out_q.put(i)
        await out_q.put(None)


class TenStage(Stage):
    async def __call__(self, in_q, out_q):
        while True:
            i = await in_q.get()
            if i is None:
                break
            await out_q.put(i * 10)
        await out_q.put(None)


class DidItWorkStage(Stage):
    async def __call__(self, in_q):
        while True:
            log_it = await in_q.get()
            if log_it is not None:
                print(log_it)
                # log.info(log_it)
            else:
                break
