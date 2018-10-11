import asyncio

from dummy_stages import SanityStage, TenStage, DidItWorkStage
from stage_group import StageGroup


# named to easily replace `synchronize` task by altering the imports.
def synchronize(remote_pk=None, repository_pk=None):
    """
    All we are going to do is n
    """
    pipeline = create_sync_pipeline()
    start_that_thing(pipeline)


def start_that_thing(pipeline):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(pipeline)


async def create_sync_pipeline(maxsize=100):
    futures = []
    #
    # even_out = asyncio.Queue()
    # odd_out = asyncio.Queue()
    # start = StartEmit2()
    # futures.append(asyncio.ensure_future(start(even_out, odd_out)))
    #
    # even_in = even_out
    # second_odd_out = asyncio.Queue()
    # make_odd = EvenInOddOut()
    # futures.append(asyncio.ensure_future(make_odd(even_in, second_odd_out)))
    #
    # jack_in = odd_out
    # walter_in = second_odd_out
    # together_out = asyncio.Queue()
    # confluence = ConfluenceStage()
    # futures.append(asyncio.ensure_future(confluence(jack_in, walter_in, together_out)))
    #
    sanity_stage = SanityStage()
    numbers_out = asyncio.Queue()
    futures.append(asyncio.ensure_future(sanity_stage(numbers_out)))

    ten_stage = TenStage()
    numbers_in = numbers_out
    hundred_out = asyncio.Queue()
    hundred_stage = StageGroup([ten_stage, ten_stage])
    stage_10000 = StageGroup([hundred_stage, hundred_stage])
    futures.append(asyncio.ensure_future(stage_10000(numbers_in, hundred_out)))

    # numbers_in = numbers_out
    # ten_out = asyncio.Queue()
    # futures.append(asyncio.ensure_future(ten_stage(numbers_in, ten_out)))
    #
    # numbers_in = ten_out
    # ten_out2 = asyncio.Queue()
    # futures.append(asyncio.ensure_future(ten_stage(numbers_in, ten_out2)))


    # in_q = odd_out
    # in_q = basic_shit
    # in_q = together_out
    # in_q = ten_out2

    in_q = hundred_out
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

synchronize()
