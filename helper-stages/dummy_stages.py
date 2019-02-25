from stages import Stage

import logging
log = logging.getLogger("DummyStage")


class SanityStage(Stage):
    async def __call__(self, unused_in_q, out_q):
        # 0 is weird
        for i in range(1, 10):
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


class PrintStage(Stage):
    def __init__(self, passthrough=False):
        self.passthrough = passthrough

    async def __call__(self, in_q, out_q):
        while True:
            log_it = await in_q.get()
            if log_it is not None:
                print(log_it)
                if self.passthrough:
                    await out_q.put(log_it)
            else:
                    break
        if self.passthrough:
            await out_q.put(None)

