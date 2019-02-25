import asyncio

from dummy_stages import SanityStage, TenStage, PrintStage
from stage_group import StageGroup
from many_many import ManyMany
from mock_docker import (Model, DockerStart, ProcessContent,
                         DownloadContent, SaveContent, ContentRelations)
from runner import SingletonQueue, ConcurrentRunner
from wait_complete import WaitUntilComplete


# named to easily replace `synchronize` task by altering the imports.
def run_pipeline(stages):
    """
    All we are going to do is n
    """
    pipeline = create_sync_pipeline(stages)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(pipeline)


async def create_sync_pipeline(stages, maxsize=100):
    futures = []
    in_q = None
    for stage in stages:
        out_q = asyncio.Queue(maxsize=maxsize)
        try:
            futures.append(asyncio.ensure_future(stage(in_q, out_q)))
        except Exception as e:
            print("Failed Stage:")
            print(stage)
        in_q = out_q

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


# Trashbin: used to test singleton q
def runner_demo():
    """
    All we are going to do is n
    """
    pipeline = runner_pipeline()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(pipeline)


async def runner_pipeline():
    futures = []

    single_use_q = SingletonQueue()
    single_run = SingleRunner()
    dummy_q = asyncio.Queue()
    futures.append(asyncio.ensure_future(single_run(dummy_q, single_use_q)))

    dummy_q = asyncio.Queue()
    printer = PrintStage()
    futures.append(asyncio.ensure_future(printer(single_use_q, dummy_q)))

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


def docker_demo():
    start = DockerStart()
    print_end = PrintStage(passthrough=False)
    download_stage = DownloadContent()
    process = ProcessContent()
    save = SaveContent()
    interrelate_content = ContentRelations()
    wait = WaitUntilComplete()

    # Download in parallel
    downloader = ConcurrentRunner(download_stage)

    # Download in serial
    # downloader = download_stage

    # Handle group in serial
    handle_content = StageGroup([downloader, process, save])

    handle_tag = StageGroup([handle_content, handle_content, handle_content, wait,
                            interrelate_content])

    # handle group in parallel
    # handle_group = ConcurrentRunner(StageGroup([downloader, process, save]))
    # stages = [start, handle_group, handle_group, handle_group, save, print_end]

    handle_all_tags = ConcurrentRunner(handle_tag)

    # concurrent tag groups
    stages = [start, handle_all_tags, print_end]

    # stages = [start, handle_tag, print_end]

    # stages = [start, dprint, handler, dprint]
    run_pipeline(stages)


def docker_concurrency_demo():
    start = DockerStart()
    pass_print = PrintStage(passthrough=True)
    print_end = PrintStage(passthrough=False)
    download_stage = DownloadContent()
    process = ProcessContent()
    save = SaveContent()
    # interrelate_content = ContentRelations()

    # Download in parallel
    downloader = ConcurrentRunner(download_stage)

    # Download in serial
    # downloader = download_stage

    # Handle group in serial
    handle_group = StageGroup([downloader, process])

    # handle group in parallel
    # handle_group = ConcurrentRunner(StageGroup([downloader, process, save]))
    stages = [start, handle_group, handle_group, handle_group, save, print_end]

    # stages = [start, dprint, handler, dprint]
    run_pipeline(stages)


def stage_groups_demo():
    singles = SanityStage()
    tens = TenStage()
    hundreds = StageGroup([tens, tens])
    millions = StageGroup([hundreds, hundreds, hundreds])
    print_q = PrintStage()
    stages = [singles, millions, print_q]
    print("Stage Groups Demo:\n")
    run_pipeline(stages)
    print("==================\n")


def main():
    # stage_groups_demo()
    # many_many_demo()
    docker_demo()
    # runner_demo()


main()
