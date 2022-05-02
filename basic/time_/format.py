from datetime import datetime
from typing import Optional


def iso8601_format(t: datetime, GMT_suffix: Optional[str] = "Z") -> str:
    s = t.isoformat()
    if GMT_suffix:
        s = s.replace("+00:00", GMT_suffix)

    return s
