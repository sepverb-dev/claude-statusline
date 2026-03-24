# Claude Code Statusline

A minimal statusline script for [Claude Code](https://claude.ai/code) that displays your usage quota as progress bars — so you know at a glance how much of your plan you've used.

## Preview

```
[Sonnet 4.6] | 5h███░░░░░42%(19:07) | 7d█████░░░68%(3/28 11:00)
```

- 5-hour rolling window usage + reset time
- 7-day rolling window usage + reset date & time
- Purple progress bar, compact and unobtrusive

## Requirements

- [Claude Code](https://claude.ai/code) (Claude.ai Pro or Max subscription)
- Python 3

## Installation

**1. Download the script**

```bash
mkdir -p ~/.claude/scripts
curl -o ~/.claude/scripts/statusline.py https://raw.githubusercontent.com/sepverb-dev/claude-statusline/main/statusline.py
```

**2. Add to Claude Code settings**

Add the following to your `~/.claude/settings.json`:

```json
{
  "statusLine": {
    "type": "command",
    "command": "python3 ~/.claude/scripts/statusline.py"
  }
}
```

**3. Restart Claude Code**

The statusline appears at the bottom of the interface after your first response in a session.

## Notes

- Usage data is only available for Claude.ai Pro/Max subscribers
- Before the first API response, the statusline shows `waiting...`
- Reset times are displayed in UTC+8 (China Standard Time) — edit `LOCAL_TZ` in the script to change your timezone

## License

MIT
