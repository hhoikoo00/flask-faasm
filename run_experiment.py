import argparse
import asyncio
import logging
from itertools import count
from time import perf_counter

import aiohttp

logger = logging.getLogger(__name__)

DEFAULT_URL_ENDPOINT = "http://localhost:8000"
DEFAULT_REQUEST_PER_SECOND = 5


async def make_request(session: aiohttp.ClientSession, url: str, method: str) -> float:
    start_time = perf_counter()
    async with session.request(method, url) as response:
        await response.text()
    end_time = perf_counter()

    latency = end_time - start_time
    return latency


async def run_experiment(requests_per_sec: int, url: str, method: str) -> None:
    async with aiohttp.ClientSession() as session:
        for i in count(start=1):
            logger.info(f"Running Experiment {i}...")
            tasks = [make_request(session, url, method) for _ in range(requests_per_sec)]
            latencies: list[float] = await asyncio.gather(*tasks)
            logger.info(f"Completed running experiment {i}!")
            logger.info(latencies)

            await asyncio.sleep(2)  # sleep for 2 seconds to clear the system.


def main():
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(description="Make N requests per second to a specified URL.")
    parser.add_argument(
        "--requests",
        metavar="N",
        type=int,
        default=DEFAULT_REQUEST_PER_SECOND,
        help="Number of requests per second to send to the endpoint",
    )
    parser.add_argument(
        "--url",
        metavar="URL",
        type=str,
        default=DEFAULT_URL_ENDPOINT,
        help="URL endpoint to make requests to",
    )
    parser.add_argument(
        "--method",
        metavar="METHOD",
        type=str,
        default="POST",
        choices=["GET", "POST", "PUT", "DELETE"],
        help="HTTP method to use",
    )

    args = parser.parse_args()
    requests_per_sec: int = args.requests
    url: str = args.url
    method: str = args.method

    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(run_experiment(requests_per_sec, url, method))
    except KeyboardInterrupt:
        logger.info("Finishing the experiments...")


if __name__ == "__main__":
    main()
