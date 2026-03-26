#!/usr/bin/env python3
"""Claude Code statusLine script - displays usage quota with progress bars."""
import json
import sys
import io
from datetime import datetime, timezone, timedelta

# Force UTF-8 output on Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# Colors (ANSI escape codes)
PURPLE = "\033[38;5;135m"  # 蓝紫色
DIM_PURPLE = "\033[38;5;99m"  # 暗紫色（未用部分）
WHITE = "\033[97m"
RESET = "\033[0m"
BOLD = "\033[1m"

BAR_FILLED = "█"
BAR_EMPTY = "░"
BAR_LENGTH = 8


LOCAL_TZ = timezone(timedelta(hours=8))  # UTC+8 中国时间


def format_reset_time(resets_at, is_short_window):
    """Format reset timestamp. Short window (5h) shows time, long window (7d) shows date+time."""
    if not resets_at:
        return ""
    try:
        if isinstance(resets_at, (int, float)):
            dt = datetime.fromtimestamp(resets_at, tz=timezone.utc).astimezone(LOCAL_TZ)
        else:
            dt = datetime.fromisoformat(resets_at.replace("Z", "+00:00")).astimezone(LOCAL_TZ)
        if is_short_window:
            return f"{DIM_PURPLE}({dt.strftime('%H:%M')}){RESET}"
        else:
            return f"{DIM_PURPLE}({dt.month}/{dt.day} {dt.strftime('%H:%M')}){RESET}"
    except (ValueError, AttributeError):
        return ""


def make_bar(percentage, resets_at=None, is_short_window=True):
    """Generate a colored progress bar with optional reset time."""
    if percentage is None:
        return f"{DIM_PURPLE}no data{RESET}"
    pct = min(100, max(0, percentage))
    filled = round(pct / 100 * BAR_LENGTH)
    empty = BAR_LENGTH - filled
    bar = f"{PURPLE}{BAR_FILLED * filled}{DIM_PURPLE}{BAR_EMPTY * empty}{RESET}"
    reset_str = format_reset_time(resets_at, is_short_window)
    return f"{bar}{WHITE}{pct:.0f}%{RESET}{reset_str}"


def main():
    try:
        raw = sys.stdin.read()
        data = json.loads(raw)
    except (json.JSONDecodeError, ValueError):
        print("waiting...")
        return

    # Model name
    model = data.get("model", {}).get("display_name", "")
    if model:
        model_str = f"{BOLD}{WHITE}[{model}]{RESET}"
    else:
        model_str = ""

    # Rate limits
    rate_limits = data.get("rate_limits", {})
    five_hour_data = rate_limits.get("five_hour", {})
    seven_day_data = rate_limits.get("seven_day", {})
    five_hour = five_hour_data.get("used_percentage")
    seven_day = seven_day_data.get("used_percentage")
    five_hour_reset = five_hour_data.get("resets_at")
    seven_day_reset = seven_day_data.get("resets_at")

    parts = []
    if model_str:
        parts.append(model_str)
    if five_hour is not None or seven_day is not None:
        if five_hour is not None:
            parts.append(f"{DIM_PURPLE}5h{RESET}{make_bar(five_hour, five_hour_reset, True)}")
        if seven_day is not None:
            parts.append(f"{DIM_PURPLE}7d{RESET}{make_bar(seven_day, seven_day_reset, False)}")
    else:
        parts.append(f"{DIM_PURPLE}waiting...{RESET}")

    print(" | ".join(parts))


if __name__ == "__main__":
    main()
