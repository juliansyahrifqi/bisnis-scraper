from bisnis.crawler import crawl_latest
import logging
import sys
import argparse

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description="Crawl latest articles from bisnis.com")
parser.add_argument("--interval", type=int, default=60, required=True, help="Interval Penarikan, Default: 60 Seconds")
args = parser.parse_args()

crawl_latest(interval_sec=args.interval)