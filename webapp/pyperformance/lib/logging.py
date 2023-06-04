"""
Script for testing the performance of logging simple messages.

Rationale for logging_silent by Antoine Pitrou:

"The performance of silent logging calls is actually important for all
applications which have debug() calls in their critical paths.  This is
quite common in network and/or distributed programming where you want to
allow logging many events for diagnosis of unexpected runtime issues
(because many unexpected conditions can appear), but with those logs
disabled by default for performance and readability reasons."

https://mail.python.org/pipermail/speed/2017-May/000576.html

Adapted from: https://github.com/python/pyperformance/blob/main/pyperformance/data-files/benchmarks/bm_logging/run_benchmark.py
"""

# Python imports
import io
import logging as _logging
import time

# A simple format for parametered logging
FORMAT = "important: %s"
MESSAGE = "some important information to be logged"


def truncate_stream(stream):
    stream.seek(0)
    stream.truncate()


def bench_silent(logger, stream, loops):
    truncate_stream(stream)

    # micro-optimization: use fast local variables
    m = MESSAGE
    range_it = range(loops)
    t0 = time.perf_counter()

    for _ in range_it:
        # repeat 10 times
        logger.debug(m)
        logger.debug(m)
        logger.debug(m)
        logger.debug(m)
        logger.debug(m)
        logger.debug(m)
        logger.debug(m)
        logger.debug(m)
        logger.debug(m)
        logger.debug(m)

    dt = time.perf_counter() - t0

    if len(stream.getvalue()) != 0:
        raise ValueError("stream is expected to be empty")

    return dt


def bench_simple_output(logger, stream, loops):
    truncate_stream(stream)

    # micro-optimization: use fast local variables
    m = MESSAGE
    range_it = range(loops)
    t0 = time.perf_counter()

    for _ in range_it:
        # repeat 10 times
        logger.warning(m)
        logger.warning(m)
        logger.warning(m)
        logger.warning(m)
        logger.warning(m)
        logger.warning(m)
        logger.warning(m)
        logger.warning(m)
        logger.warning(m)
        logger.warning(m)

    dt = time.perf_counter() - t0

    lines = stream.getvalue().splitlines()
    if len(lines) != loops * 10:
        raise ValueError("wrong number of lines")

    return dt


def bench_formatted_output(logger, stream, loops):
    truncate_stream(stream)

    # micro-optimization: use fast local variables
    fmt = FORMAT
    msg = MESSAGE
    range_it = range(loops)
    t0 = time.perf_counter()

    for _ in range_it:
        # repeat 10 times
        logger.warning(fmt, msg)
        logger.warning(fmt, msg)
        logger.warning(fmt, msg)
        logger.warning(fmt, msg)
        logger.warning(fmt, msg)
        logger.warning(fmt, msg)
        logger.warning(fmt, msg)
        logger.warning(fmt, msg)
        logger.warning(fmt, msg)
        logger.warning(fmt, msg)

    dt = time.perf_counter() - t0

    lines = stream.getvalue().splitlines()
    if len(lines) != loops * 10:
        raise ValueError("wrong number of lines")

    return dt


BENCHMARKS = {
    "silent": bench_silent,
    "simple": bench_simple_output,
    "format": bench_formatted_output,
}


def bench_logging():
    # NOTE: StringIO performance will impact the results...
    stream = io.StringIO()
    handler = _logging.StreamHandler(stream=stream)
    logger = _logging.getLogger("benchlogger")
    logger.propagate = False
    logger.addHandler(handler)
    logger.setLevel(_logging.WARNING)

    num_loops = 10

    for bench in BENCHMARKS:
        bench_func = BENCHMARKS[bench]
        bench_func(logger, stream, loops=num_loops)