import json
from datetime import datetime, timezone
import logging

logger = logging.getLogger(__name__)

def save_to_json(data, filename):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

        logger.info(f"✅ Finished. Saved {len(data)} records to '{filename}'")

def clean_text(text):
    return ' '.join(text.split())

def parse_iso_date(date_str):
    formats = [
        "%Y/%m/%d %H:%M:%S",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d"
    ]
    
    for fmt in formats:
        try:
            dt = datetime.strptime(date_str, fmt)
            dt = dt.replace(tzinfo=timezone.utc)
            return dt.isoformat().replace("+00:00", "Z")
        except ValueError:
            continue

    logger.error(f"Unknown date format: {date_str}")
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")