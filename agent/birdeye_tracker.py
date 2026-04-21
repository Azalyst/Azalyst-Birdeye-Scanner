"""
Birdeye Whale Tracking Module
Implements the complete whale tracking workflow for Birdeye.so
"""

import requests
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict


@dataclass
class WhaleWallet:
    """Represents a whale wallet being tracked"""
    address: str
    total_holdings: float
    recent_activity: List[Dict]
    most_held_tokens: List[Dict]
    last_updated: str
    
    def to_dict(self):
        return asdict(self)


@dataclass
class TokenSignal:
    """Represents pump/dump signals for a token"""
    token_address: str
    token_name: str
    signal_type: str  # 'pump' or 'dump'
    confidence: float  # 0-1
    indicators: List[str]
    timestamp: str
    
    def to_dict(self):
        return asdict(self)


class BirdeyeAPI:
    """Wrapper for Birdeye API interactions"""
    
    BASE_URL = "https://public-api.birdeye.so"
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.headers = {
            "X-API-KEY": api_key if api_key else "",
            "Accept": "application/json"
        }
    
    def get_trending_tokens(self, chain: str = "solana", time_frame: str = "24h") -> List[Dict]:
        """Get trending tokens on Birdeye"""
        endpoint = f"{self.BASE_URL}/defi/trending_tokens/{chain}"
        params = {"time_frame": time_frame}
        
        try:
            response = requests.get(endpoint, headers=self.headers, params=params, timeout=10)
            if response.status_code == 200:
                return response.json().get("data", [])
            return []
        except Exception as e:
            return [{"error": str(e)}]
    
    def get_wallet_portfolio(self, wallet_address: str) -> Dict:
        """Get wallet holdings and portfolio breakdown"""
        endpoint = f"{self.BASE_URL}/v1/wallet/token_list"
        params = {"wallet": wallet_address}
        
        try:
            response = requests.get(endpoint, headers=self.headers, params=params, timeout=10)
            if response.status_code == 200:
                return response.json().get("data", {})
            return {}
        except Exception as e:
            return {"error": str(e)}
    
    def get_token_overview(self, token_address: str) -> Dict:
        """Get comprehensive token overview including metrics"""
        endpoint = f"{self.BASE_URL}/defi/token_overview"
        params = {"address": token_address}
        
        try:
            response = requests.get(endpoint, headers=self.headers, params=params, timeout=10)
            if response.status_code == 200:
                return response.json().get("data", {})
            return {}
        except Exception as e:
            return {"error": str(e)}
    
    def get_token_trades(self, token_address: str, limit: int = 100) -> List[Dict]:
        """Get recent trades for a token"""
        endpoint = f"{self.BASE_URL}/defi/txs/token"
        params = {
            "address": token_address,
            "limit": limit,
            "offset": 0
        }
        
        try:
            response = requests.get(endpoint, headers=self.headers, params=params, timeout=10)
            if response.status_code == 200:
                return response.json().get("data", {}).get("items", [])
            return []
        except Exception as e:
            return [{"error": str(e)}]
    
    def get_token_security(self, token_address: str) -> Dict:
        """Get token security analysis"""
        endpoint = f"{self.BASE_URL}/defi/token_security"
        params = {"address": token_address}
        
        try:
            response = requests.get(endpoint, headers=self.headers, params=params, timeout=10)
            if response.status_code == 200:
                return response.json().get("data", {})
            return {}
        except Exception as e:
            return {"error": str(e)}


class WhaleTracker:
    """Main whale tracking logic implementing the Birdeye workflow"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api = BirdeyeAPI(api_key)
        self.tracked_wallets: Dict[str, WhaleWallet] = {}
        self.watchlist: List[str] = []
    
    # STEP 1: Find and Track Whale Wallets
    
    def find_whale_trades(self, min_value_usd: float = 10000) -> List[Dict]:
        """
        Find large whale trades from recent activity
        Step 1: Whale ka wallet pakad
        """
        trending = self.api.get_trending_tokens()
        whale_trades = []
        
        for token in trending[:10]:  # Check top 10 trending
            token_address = token.get("address", "")
            if not token_address:
                continue
                
            trades = self.api.get_token_trades(token_address, limit=50)
            
            for trade in trades:
                value_usd = float(trade.get("value_usd", 0))
                if value_usd >= min_value_usd:
                    whale_trades.append({
                        "token": token.get("symbol", "Unknown"),
                        "token_address": token_address,
                        "wallet": trade.get("owner", ""),
                        "type": trade.get("type", ""),
                        "value_usd": value_usd,
                        "timestamp": trade.get("block_unix_time", 0)
                    })
        
        return sorted(whale_trades, key=lambda x: x["value_usd"], reverse=True)
    
    def add_to_watchlist(self, wallet_address: str) -> str:
        """Add wallet to tracking watchlist"""
        if wallet_address not in self.watchlist:
            self.watchlist.append(wallet_address)
            return f"Added {wallet_address} to watchlist. Total: {len(self.watchlist)} wallets"
        return f"Wallet already in watchlist"
    
    # STEP 2: Deep Dive into Wallet
    
    def analyze_wallet(self, wallet_address: str) -> WhaleWallet:
        """
        Deep dive into wallet holdings and activity
        Step 2: Wallet deep dive
        """
        portfolio = self.api.get_wallet_portfolio(wallet_address)
        
        tokens = portfolio.get("tokens", [])
        total_value = sum(float(t.get("value_usd", 0)) for t in tokens)
        
        most_held = sorted(
            tokens,
            key=lambda x: float(x.get("value_usd", 0)),
            reverse=True
        )[:10]
        
        wallet = WhaleWallet(
            address=wallet_address,
            total_holdings=total_value,
            recent_activity=[],
            most_held_tokens=most_held,
            last_updated=datetime.now().isoformat()
        )
        
        self.tracked_wallets[wallet_address] = wallet
        return wallet
    
    # STEP 3: Pre-Pump Signals Detection
    
    def detect_accumulation_pattern(self, wallet_address: str, token_address: str) -> Dict:
        """
        Detect if wallet is accumulating a specific token
        Part of Step 3: Pump aane se pehle signals
        """
        trades = self.api.get_token_trades(token_address, limit=100)
        
        wallet_trades = [t for t in trades if t.get("owner") == wallet_address]
        
        buys = [t for t in wallet_trades if t.get("type") == "buy"]
        sells = [t for t in wallet_trades if t.get("type") == "sell"]
        
        buy_volume = sum(float(t.get("value_usd", 0)) for t in buys)
        sell_volume = sum(float(t.get("value_usd", 0)) for t in sells)
        
        return {
            "wallet": wallet_address,
            "token": token_address,
            "buy_count": len(buys),
            "sell_count": len(sells),
            "buy_volume_usd": buy_volume,
            "sell_volume_usd": sell_volume,
            "net_position": buy_volume - sell_volume,
            "is_accumulating": buy_volume > sell_volume * 2
        }
    
    def check_holder_growth(self, token_address: str) -> Dict:
        """
        Check if token is getting new holders (viral signal)
        Agar ek token mein 2,000 naye holders ek din mein aayein
        """
        token_data = self.api.get_token_overview(token_address)
        
        holder_count = token_data.get("holder", 0)
        holder_change_24h = token_data.get("holder_change_24h", 0)
        
        return {
            "token": token_address,
            "current_holders": holder_count,
            "holder_change_24h": holder_change_24h,
            "is_viral": holder_change_24h > 1000,
            "growth_rate": (holder_change_24h / holder_count * 100) if holder_count > 0 else 0
        }
    
    # STEP 4: Hidden Gem Filter
    
    def find_hidden_gems(self, 
                        min_lp_size: float = 2000,
                        min_volume_1h: float = 10000,
                        max_age_hours: int = 24) -> List[Dict]:
        """
        Filter tokens for early pump potential
        Step 4: Hidden gem filter (pump prediction)
        Filters: token age <24h, LP >2K, volume growth >10K in 1H
        """
        trending = self.api.get_trending_tokens(time_frame="1h")
        gems = []
        
        for token in trending:
            token_address = token.get("address", "")
            if not token_address:
                continue
            
            overview = self.api.get_token_overview(token_address)
            security = self.api.get_token_security(token_address)
            
            # Check filters
            liquidity = float(overview.get("liquidity", 0))
            volume_1h = float(overview.get("v1h", 0))
            created_at = overview.get("created_at", 0)
            
            age_hours = (time.time() - created_at) / 3600 if created_at else 999
            
            # Security checks
            is_mintable = security.get("is_mintable", True)
            top_holders = security.get("top_10_holder_percent", 100)
            
            if (liquidity >= min_lp_size and 
                volume_1h >= min_volume_1h and 
                age_hours <= max_age_hours and
                not is_mintable and
                top_holders < 50):  # Not too concentrated
                
                gems.append({
                    "token": token.get("symbol", "Unknown"),
                    "address": token_address,
                    "liquidity_usd": liquidity,
                    "volume_1h_usd": volume_1h,
                    "age_hours": round(age_hours, 2),
                    "holder_count": overview.get("holder", 0),
                    "price": overview.get("price", 0),
                    "score": self._calculate_gem_score(overview, security)
                })
        
        return sorted(gems, key=lambda x: x["score"], reverse=True)
    
    def _calculate_gem_score(self, overview: Dict, security: Dict) -> float:
        """Calculate gem potential score (0-100)"""
        score = 0
        
        # Volume spike
        volume_1h = float(overview.get("v1h", 0))
        volume_24h = float(overview.get("v24h", 1))
        if volume_24h > 0:
            volume_spike = (volume_1h / (volume_24h / 24)) * 10
            score += min(volume_spike, 30)
        
        # Holder growth
        holder_change = float(overview.get("holder_change_24h", 0))
        score += min(holder_change / 50, 30)
        
        # Liquidity strength
        liquidity = float(overview.get("liquidity", 0))
        score += min(liquidity / 1000, 20)
        
        # Security bonus
        if not security.get("is_mintable"):
            score += 10
        if security.get("top_10_holder_percent", 100) < 30:
            score += 10
        
        return min(score, 100)
    
    # STEP 5: Signal Analysis (Pump vs Dump)
    
    def analyze_pump_dump_signals(self, token_address: str) -> TokenSignal:
        """
        Comprehensive pump/dump signal detection
        Combines all red/green flags from requirements
        """
        overview = self.api.get_token_overview(token_address)
        trades = self.api.get_token_trades(token_address, limit=100)
        security = self.api.get_token_security(token_address)
        
        red_flags = []
        green_flags = []
        
        # Analyze large wallet movements
        large_sells = [t for t in trades if t.get("type") == "sell" and float(t.get("value_usd", 0)) > 5000]
        large_buys = [t for t in trades if t.get("type") == "buy" and float(t.get("value_usd", 0)) > 5000]
        
        if len(large_sells) > len(large_buys) * 2:
            red_flags.append("Large wallet outflows detected")
        
        # LP analysis
        liquidity = float(overview.get("liquidity", 0))
        liquidity_change = float(overview.get("liquidity_change_24h", 0))
        
        if liquidity_change < -20:
            red_flags.append("LP pulled significantly")
        
        # Holder analysis
        holder_change = float(overview.get("holder_change_24h", 0))
        
        if holder_change < -100:
            red_flags.append("Holder count dropping")
        elif holder_change > 500:
            green_flags.append("New holders spike - viral signal")
        
        # Volume analysis
        volume_1h = float(overview.get("v1h", 0))
        volume_24h = float(overview.get("v24h", 1))
        
        if volume_24h > 0:
            volume_spike = volume_1h / (volume_24h / 24)
            if volume_spike > 10:
                green_flags.append("Volume 10x in 1H - momentum building")
        
        # Smart money analysis
        smart_wallets_buying = sum(1 for t in large_buys if self._is_smart_wallet(t.get("owner", "")))
        
        if smart_wallets_buying > 3:
            green_flags.append("Smart wallets accumulating")
        
        # Dev wallet check
        dev_address = security.get("owner_address", "")
        dev_sells = [t for t in trades if t.get("owner") == dev_address and t.get("type") == "sell"]
        
        if len(dev_sells) > 0:
            red_flags.append("Dev wallet selling - inside job risk")
        
        # Determine signal type
        if len(red_flags) > len(green_flags):
            signal_type = "dump"
            confidence = min(len(red_flags) / 5, 1.0)
            indicators = red_flags
        else:
            signal_type = "pump"
            confidence = min(len(green_flags) / 5, 1.0)
            indicators = green_flags
        
        return TokenSignal(
            token_address=token_address,
            token_name=overview.get("symbol", "Unknown"),
            signal_type=signal_type,
            confidence=confidence,
            indicators=indicators,
            timestamp=datetime.now().isoformat()
        )
    
    def _is_smart_wallet(self, wallet_address: str) -> bool:
        """Check if wallet has history of profitable early entries"""
        # Simplified - in production, maintain database of verified smart wallets
        # or check wallet's historical performance
        return len(wallet_address) > 30  # Placeholder logic
    
    # Alert & Monitoring
    
    def generate_alert_config(self, 
                            volume_threshold: float = 10000,
                            whale_threshold: float = 5000) -> Dict:
        """
        Generate Telegram alert configuration
        Step 5: Alerts set karo
        """
        config = {
            "alert_types": [
                {
                    "name": "volume_spike",
                    "description": "Volume increases 10x in 1 hour",
                    "threshold": volume_threshold,
                    "enabled": True
                },
                {
                    "name": "whale_movement",
                    "description": "Whale buy/sell above threshold",
                    "threshold": whale_threshold,
                    "enabled": True
                },
                {
                    "name": "new_token_launch",
                    "description": "Token launched <1h ago with liquidity",
                    "min_liquidity": 2000,
                    "enabled": True
                },
                {
                    "name": "lp_change",
                    "description": "LP pool changes >20%",
                    "threshold_percent": 20,
                    "enabled": True
                },
                {
                    "name": "holder_spike",
                    "description": "Holder count increases >1000 in 24h",
                    "threshold": 1000,
                    "enabled": True
                }
            ],
            "notification_method": "telegram",
            "check_interval_seconds": 60
        }
        return config
    
    # Practical Workflow Implementation
    
    def run_daily_scan(self) -> Dict:
        """
        Complete daily scan workflow as described in requirements
        Practical Workflow: aaj pump pakdna hai toh
        """
        results = {
            "timestamp": datetime.now().isoformat(),
            "trending_analysis": [],
            "whale_trades": [],
            "hidden_gems": [],
            "watchlist_updates": []
        }
        
        # 1. Check trending tokens (24H)
        trending = self.api.get_trending_tokens(time_frame="24h")
        
        for token in trending[:20]:
            token_address = token.get("address", "")
            if not token_address:
                continue
            
            # Analyze for unusual activity
            signal = self.analyze_pump_dump_signals(token_address)
            
            results["trending_analysis"].append({
                "token": token.get("symbol"),
                "address": token_address,
                "signal": signal.to_dict()
            })
        
        # 2. Find whale trades
        whale_trades = self.find_whale_trades(min_value_usd=10000)
        results["whale_trades"] = whale_trades[:10]
        
        # 3. Scan for hidden gems
        gems = self.find_hidden_gems()
        results["hidden_gems"] = gems[:10]
        
        # 4. Update watchlist wallets
        for wallet_addr in self.watchlist:
            wallet_data = self.analyze_wallet(wallet_addr)
            results["watchlist_updates"].append({
                "wallet": wallet_addr,
                "total_holdings": wallet_data.total_holdings,
                "top_tokens": wallet_data.most_held_tokens[:5]
            })
        
        return results
    
    def format_report(self, scan_results: Dict) -> str:
        """Format scan results into readable report"""
        report = [
            "=" * 60,
            f"BIRDEYE WHALE TRACKING REPORT",
            f"Generated: {scan_results['timestamp']}",
            "=" * 60,
            ""
        ]
        
        # Trending Analysis
        report.append("📊 TRENDING TOKENS ANALYSIS")
        report.append("-" * 60)
        for item in scan_results["trending_analysis"][:5]:
            signal = item["signal"]
            emoji = "🚀" if signal["signal_type"] == "pump" else "⚠️"
            report.append(f"{emoji} {item['token']}")
            report.append(f"   Signal: {signal['signal_type'].upper()} (confidence: {signal['confidence']:.0%})")
            report.append(f"   Indicators: {', '.join(signal['indicators'][:3])}")
            report.append("")
        
        # Whale Trades
        report.append("\n🐋 TOP WHALE TRADES")
        report.append("-" * 60)
        for trade in scan_results["whale_trades"][:5]:
            report.append(f"${trade['value_usd']:,.0f} - {trade['type'].upper()} {trade['token']}")
            report.append(f"   Wallet: {trade['wallet'][:8]}...{trade['wallet'][-6:]}")
            report.append("")
        
        # Hidden Gems
        report.append("\n💎 HIDDEN GEMS")
        report.append("-" * 60)
        for gem in scan_results["hidden_gems"][:5]:
            report.append(f"{gem['token']} (Score: {gem['score']:.0f}/100)")
            report.append(f"   Age: {gem['age_hours']:.1f}h | Volume 1H: ${gem['volume_1h_usd']:,.0f}")
            report.append(f"   Liquidity: ${gem['liquidity_usd']:,.0f} | Holders: {gem['holder_count']}")
            report.append("")
        
        return "\n".join(report)


# Utility functions for agent integration

def track_whale(wallet_address: str, api_key: Optional[str] = None) -> str:
    """Add whale wallet to tracking list"""
    tracker = WhaleTracker(api_key)
    result = tracker.add_to_watchlist(wallet_address)
    wallet_data = tracker.analyze_wallet(wallet_address)
    
    return f"{result}\n\nWallet Analysis:\n" + json.dumps(wallet_data.to_dict(), indent=2)


def find_pumps(api_key: Optional[str] = None) -> str:
    """Find potential pump tokens"""
    tracker = WhaleTracker(api_key)
    gems = tracker.find_hidden_gems()
    
    if not gems:
        return "No hidden gems found matching criteria"
    
    result = ["🔍 POTENTIAL PUMP TOKENS\n"]
    for i, gem in enumerate(gems[:10], 1):
        result.append(f"{i}. {gem['token']} - Score: {gem['score']:.0f}/100")
        result.append(f"   ${gem['volume_1h_usd']:,.0f} vol | {gem['age_hours']:.1f}h old")
    
    return "\n".join(result)


def analyze_token(token_address: str, api_key: Optional[str] = None) -> str:
    """Analyze token for pump/dump signals"""
    tracker = WhaleTracker(api_key)
    signal = tracker.analyze_pump_dump_signals(token_address)
    
    emoji = "🚀" if signal.signal_type == "pump" else "⚠️"
    
    result = [
        f"{emoji} TOKEN SIGNAL ANALYSIS",
        f"Token: {signal.token_name}",
        f"Signal: {signal.signal_type.upper()}",
        f"Confidence: {signal.confidence:.0%}",
        "",
        "Indicators:"
    ]
    
    for indicator in signal.indicators:
        result.append(f"  • {indicator}")
    
    return "\n".join(result)


def daily_scan(api_key: Optional[str] = None) -> str:
    """Run complete daily whale tracking scan"""
    tracker = WhaleTracker(api_key)
    results = tracker.run_daily_scan()
    return tracker.format_report(results)
