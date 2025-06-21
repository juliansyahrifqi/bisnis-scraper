import argparse
from datetime import datetime
from bisnis.crawler import crawl_by_date
from bisnis.utils import save_to_json
import sys
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Parsing Arguments
parser = argparse.ArgumentParser(description="Crawl articles from bisnis.com by date range")
parser.add_argument("--start", required=True, help="Start date (YYYY-MM-DD)")
parser.add_argument("--end", required=True, help="End date (YYYY-MM-DD)")
args = parser.parse_args()

if not args.start.strip():
  logger.error("❌ Start date is missing or empty.")
  sys.exit(1)

if not args.end.strip():
  logger.error("❌ End date is missing or empty.")
  sys.exit(1)

try:
  start = datetime.strptime(args.start, "%Y-%m-%d")
  end = datetime.strptime(args.end, "%Y-%m-%d")
except ValueError:
  logger.error("❌ Invalid date format. Please use YYYY-MM-DD.")
  sys.exit(1)

# Validasi end > start
if end < start:
  logger.error("❌ End date must be after start date.")
  sys.exit(1)

data = crawl_by_date(start, end)
filename = f"output/hasil_backtrack_{start.date()}_{end.date()}.json"

save_to_json(data, filename)
