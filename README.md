# NIM Qwen Agent + Birdeye Whale Tracking

A GitHub Actions-hosted coding agent powered by Qwen 2.5 Coder 32B via NVIDIA NIM, now with comprehensive Birdeye whale tracking capabilities.

---

## 🆕 What's New: Birdeye Whale Tracking

This agent now includes a complete whale tracking system for Birdeye.so:

- 🐋 **Whale Wallet Tracking** - Monitor large holders and their movements
- 💎 **Hidden Gem Detection** - Find pump candidates before they trend
- 📊 **Pump/Dump Signal Analysis** - AI-driven signal detection
- 🔔 **Alert Configuration** - Set up Telegram alerts for key events
- 📈 **Daily Scans** - Automated comprehensive market analysis

### Quick Start Examples

```bash
# Find potential pump tokens
/agent find_pumps

# Analyze specific token
/agent analyze_token token_address=EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v

# Track whale wallet
/agent track_whale wallet_address=7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU

# Run complete daily scan
/agent daily_scan
```

---

## Setup

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

**Updated dependencies:**
- `openai>=1.0.0` - for NIM API
- `python-dotenv` - environment variables
- `requests>=2.31.0` - for Birdeye API calls

### 2. Get API Keys

#### NIM API Key (Required)
Sign up at [build.nvidia.com](https://build.nvidia.com) → get a free API key.

#### Birdeye API Key (Optional but Recommended)
Get from [birdeye.so](https://birdeye.so) - free tier available with rate limits.

### 3. Add Secrets to Your Repo

`Settings → Secrets and variables → Actions → New repository secret`

| Name | Value | Required |
|---|---|---|
| `NIM_API_KEY` | your NVIDIA NIM API key | Yes |
| `BIRDEYE_API_KEY` | your Birdeye API key | Optional |

**Note:** Agent works without Birdeye API key but with lower rate limits.

### 4. Enable Actions Write Permissions

`Settings → Actions → General → Workflow permissions → Read and write permissions`

---

## Installation

### Option 1: Fresh Install

```bash
git clone <your-repo>
cd <your-repo>
pip install -r requirements.txt

# Copy the updated files
cp tools_updated.py agent/tools.py
cp birdeye_tracker.py agent/birdeye_tracker.py
cp AGENTS_updated.md AGENTS.md
cp requirements_updated.txt requirements.txt

# Copy workflow (optional)
cp whale_tracking_workflow.yml .github/workflows/whale_tracking.yml
```

### Option 2: Update Existing Installation

Replace these files in your repository:
- `agent/tools.py` → use `tools_updated.py`
- `requirements.txt` → use `requirements_updated.txt`
- `AGENTS.md` → use `AGENTS_updated.md`

Add these new files:
- `agent/birdeye_tracker.py` → core whale tracking module
- `BIRDEYE_USAGE.md` → comprehensive usage guide
- `.github/workflows/whale_tracking.yml` → automated scanning workflow
- `example_whale_tracking.py` → standalone testing script

---

## Usage

### Via GitHub Actions (Recommended)

#### Manual Workflow
`Actions → NIM Qwen Agent → Run workflow → Enter task`

Example tasks:
```
find_pumps and show me top 5 potential tokens
analyze_token token_address=<TOKEN_ADDRESS>
track_whale wallet_address=<WALLET_ADDRESS>
daily_scan and save report
```

#### From Issue Comments
```
/agent find_pumps
/agent analyze_token token_address=EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v
/agent track_whale wallet_address=7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU
/agent daily_scan
```

#### Automated Scheduled Scans
The whale_tracking workflow runs automatically every 4 hours to scan the market.

### Via Command Line (Local Testing)

```bash
# Set environment variables
export NIM_API_KEY=your_nim_key
export BIRDEYE_API_KEY=your_birdeye_key  # optional

# Run tasks
python agent/agent.py "find_pumps"
python agent/agent.py "analyze_token token_address=EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
python agent/agent.py "daily_scan"
```

### Standalone Testing (Without Agent)

```bash
# Daily scan
python example_whale_tracking.py daily

# Find pumps
python example_whale_tracking.py pumps

# Track wallet
python example_whale_tracking.py track 7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU

# Analyze token
python example_whale_tracking.py analyze EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v
```

---

## Available Tools

### Original Tools
- `bash(cmd)` - Run shell commands
- `read_file(path)` - Read files
- `write_file(path, content)` - Write files
- `list_dir(path)` - List directory
- `search(pattern, path)` - Grep search

### New Birdeye Tools
- `track_whale(wallet_address)` - Track whale wallet
- `find_pumps()` - Find potential pump tokens
- `analyze_token(token_address)` - Analyze token signals
- `daily_scan()` - Complete market scan

---

## Understanding Signals

### 🚀 Pump Signals (Green Flags)
- Smart wallets accumulating
- Volume 10x+ in 1 hour
- New holders spike (>500 in 24h)
- Whale early entry on new token
- Fair token distribution

### ⚠️ Dump Signals (Red Flags)
- Large wallet outflows
- LP pulled (>20% drop)
- Holder count dropping
- Dev wallet selling
- Community exit pattern

### Confidence Levels
- **>70%** - Strong signal, act accordingly
- **40-70%** - Moderate signal, watch closely
- **<40%** - Weak signal, more data needed

---

## Complete Workflow (Aaj Pump Pakdna Hai)

### Morning Routine (Best Practice)

```bash
# 1. Run daily scan
/agent daily_scan

# 2. Review trending tokens
# Pick top 3 interesting tokens from report

# 3. Deep analysis
/agent analyze_token token_address=<TOKEN_1>
/agent analyze_token token_address=<TOKEN_2>
/agent analyze_token token_address=<TOKEN_3>

# 4. Track promising whales
/agent track_whale wallet_address=<WHALE_FROM_SCAN>

# 5. Monitor throughout day
# Check GitHub Actions for automated scans every 4 hours
```

### Real-Time Whale Following

```bash
# 1. Find active whales
/agent find_pumps

# 2. Pick token with unusual activity
/agent analyze_token token_address=<ACTIVE_TOKEN>

# 3. If signal strong, track whale
/agent track_whale wallet_address=<WHALE_BUYER>

# 4. Monitor whale's positions
/agent daily_scan
```

---

## File Structure

```
.
├── agent/
│   ├── agent.py                # Main agent loop
│   ├── tools.py                # Tool implementations (UPDATED)
│   └── birdeye_tracker.py      # Whale tracking module (NEW)
├── .github/
│   └── workflows/
│       └── whale_tracking.yml  # Automated scan workflow (NEW)
├── AGENTS.md                   # Agent guidelines (UPDATED)
├── BIRDEYE_USAGE.md           # Whale tracking guide (NEW)
├── example_whale_tracking.py  # Standalone testing (NEW)
├── requirements.txt           # Dependencies (UPDATED)
└── README.md                  # This file (UPDATED)
```

---

## Model Configuration

Uses `qwen/qwen2.5-coder-32b-instruct` via NVIDIA NIM.

To change model, edit `MODEL` in `agent/agent.py`.

---

## Advanced Configuration

### Custom Filters

Edit `agent/birdeye_tracker.py`:

```python
# Adjust hidden gem filters
tracker.find_hidden_gems(
    min_lp_size=5000,      # Higher liquidity requirement
    min_volume_1h=20000,   # More volume needed
    max_age_hours=12       # Only very new tokens
)
```

### Alert Configuration

```python
from agent.birdeye_tracker import WhaleTracker

tracker = WhaleTracker(api_key)
config = tracker.generate_alert_config(
    volume_threshold=20000,  # $20K+ volume spikes
    whale_threshold=10000    # $10K+ whale moves
)
```

---

## Security & Privacy

- Never commit API keys to the repository
- Use GitHub Secrets for all keys
- Agent runs in isolated GitHub Actions environment
- No user data is stored or transmitted beyond API calls

---

## Risk Disclaimer

**CRITICAL:** This tool is for education and awareness only.

- NOT financial advice
- Past signals ≠ future results
- Whales can dump without warning
- Always manage risk properly
- Never invest more than you can lose
- DYOR (Do Your Own Research)

Use for:
✅ Learning and pattern recognition
✅ Market awareness
✅ Risk assessment

NOT for:
❌ Guaranteed predictions
❌ Financial advice
❌ Unverified trading signals

---

## Troubleshooting

### Birdeye Tools Not Available
```bash
# Check if module imported correctly
python -c "from agent.birdeye_tracker import WhaleTracker; print('OK')"

# Install dependencies
pip install -r requirements.txt
```

### API Rate Limits
- Get Birdeye API key for higher limits
- Reduce scan frequency
- Cache results locally

### Empty Results
- Verify token/wallet addresses are correct
- Check if token exists on Solana
- Ensure API key is valid (if using one)

---

## Documentation

- **BIRDEYE_USAGE.md** - Complete whale tracking guide
- **AGENTS.md** - Agent behavior and tool reference
- **example_whale_tracking.py** - Standalone usage examples

---

## Contributing

Improvements welcome:
1. More data sources
2. Better scoring algorithms
3. Machine learning models
4. Enhanced alert systems
5. Backtesting framework

---

## Support

Questions or issues:
1. Check documentation
2. Review example scripts
3. Test with simple queries first
4. Verify API keys are set

---

## License

MIT License - use responsibly and at your own risk.

---

**Remember:** Whale tracking is informational. Always verify independently and manage risk carefully. Never full port karo! 🐋
