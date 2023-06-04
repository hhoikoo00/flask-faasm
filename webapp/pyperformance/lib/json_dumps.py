"""
Adapted from: https://github.com/python/pyperformance/blob/main/pyperformance/data-files/benchmarks/bm_json_dumps/run_benchmark.py
"""

import json

EMPTY = ({}, 2000)
SIMPLE_DATA = {"key1": 0, "key2": True, "key3": "value", "key4": "foo", "key5": "string"}
SIMPLE = (SIMPLE_DATA, 1000)
NESTED_DATA = {
    "key1": 0,
    "key2": SIMPLE[0],
    "key3": "value",
    "key4": SIMPLE[0],
    "key5": SIMPLE[0],
    "key": "\u0105\u0107\u017c",
}
NESTED = (NESTED_DATA, 1000)
HUGE = ([NESTED[0]] * 1000, 1)


def bench_json_dumps():
    data = (EMPTY, SIMPLE, NESTED, HUGE)
    for obj, count_it in data:
        for _ in count_it:
            json.dumps(obj)
