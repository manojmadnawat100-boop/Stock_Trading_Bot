# -*- coding: utf-8 -*-
"""
Institutional Nifty 50 & Bank Nifty F&O Pro Terminal  -  v7.9.3 (SCORE-7 + 9:30) + v7.9.2 (ALL-15) + v7.9.1 (REVERSE-MODE) + v7.9 (SECTOR-HEDGE + INDEX-DIR + TICK-SL + SOFT-HALT + BURST-CD) + v7.8.3 (CONFIRM-1 + WHY-COL + TS-FIX) NO-STRICT + 2-CYCLE CONFIRM + CONFIRM-LOG + NO-PCR-FILTER + PULLBACK-ENTRY + SL-MODE (Equity Intraday + LIVE + Choppy NO-TRADE + Master-loop safety + Profit protect)
(All NSE+BSE F&O, All Indices, Two-tier scan, Live Open/Closed Paper Trade DB,
 Day Report tab, Upstox real-trades viewer, re-entry/cooldown/stale-data fixes)

v7.9.3: Defaults: ek direction max 5, ek sector/group max 2, burst guard 3 entry / 10 min, ek minute me max 2 naye entry
      (v7.9.2 ke 15 wapas). Max trades/din 15 aur max khule positions 15 waise hi. Stock entry min score 5 -> 7.
      Entry window start 10:00 -> 9:30.
v7.9.2: Defaults 15: max trades/din 15, max khule positions 15, ek direction me max 15, ek sector/group me max 15,
      burst guard 15 entry / 10 min, ek minute me max 15 naye entry (sliders ki upar ki limit 20).
v7.9.1: REVERSE MODE (user rule): STRONG BUY signal entry ke liye ready ho to SHORT, STRONG SELL par LONG - usi stock me.
      Saare signal filter / confirm cycles waise hi; flip sirf entry ke pal. SL/target ulti disha ke liye dobara (SL mode se).
      Sector/direction/hedge guard asli (ulti) position par. Index gate default asli trade ki disha par (option se badlo).
      Reverse mode me pullback ka wait nahi (STRONG par turant ulti entry; EXTENDED signal skip). OPPOSITE SIGNAL exit
      bhi ulta samjha jata hai. LIVE orders me reverse tabhi jab alag checkbox ON ho (default OFF = sirf paper).
      trade_journal me naya column sig_side (signal kis disha ka tha) + Day Report me "Signal" aur "Signal-side Net"
      (agar signal ki disha me lete to kitna) - taaki 30+ trade baad pata chale reverse sach me kaam karta hai ya nahi.
v7.9: (03-Nov log review: 7 trade 22 min me, 6 finance stocks, SL ke paar exit, MAX SL HALT ne winners kaate)
      (1) Sector guard: ek sector-group me max 2 khule trade (default group = FINANCIALS: Bank + NBFC + PSU Fin +
          Insurance + Cap Mkt ek hi group) aur same group me ek saath LONG + SHORT block.
      (2) Index direction gate: entry se pehle index ka 5m trend usi disha me (aur 15m ulta nahi) zaroori.
          Bank/Finance stock => BANK NIFTY, baaki => NIFTY (sidebar se "dono" ya "sirf Nifty" bhi).
      (3) Tick SL: Upstox WebSocket (V3 feed, upstox-python-sdk) se har tick par SL/target check. SDK na ho ya feed
          ruk jaye to 1-sec REST LTP fallback. Paper exit SL todne wale PEHLE tick ke price par (refresh ka wait nahi).
      (4) MAX SL HALT = sirf naye trade band. Profit wale khule trade ka SL kam se kam entry par aur apne trail SL par
          chalte rahenge; loss wale band (sidebar se "sab apne SL par" bhi). KILL / MAX LOSS par pehle jaisa sab band.
      (5) Burst cooldown: 10 min me 3 entry ho gayi to agle 15 min naya entry nahi (teeno sidebar se badal sakte ho).
      Backtest tab ka simulation is version me NAHI badla (wahan ye 5 rules abhi lagu nahi).
v7.8.3: Confirm cycles default 2 -> 1 (Stock aur Index dono): signal pehli hi refresh cycle me STRONG ho aur
      baaki saare guards theek hon to turant entry. (Slider se 2-5 phir bhi kar sakte ho.)

v7.8.2: Naya column "Kyun nahi lagi" (Top Picks + Full Matrix + Scanner CSV): har STRONG / pullback stock ke saamne
      seedha likha aata hai ki paper-trade kyun nahi lagi - score kam, confirm cycle n/2, pullback order ka intezaar,
      cooldown, din ki limit, max positions, entry window, data purana, risk/capital guard, ya "Entry ho gayi / Position khuli".
      Entry logic BILKUL SAME hai - sirf har guard ki wajah record hoti hai.

v7.8.1: FIX "index ctx: Can only use .dt accessor with datetimelike values".
      Wajah: intraday API khaali / fail aaye to empty DataFrame ka "ts" object dtype hota tha; prior (datetime) ke saath
      concat karne par poora "ts" column object ban jata tha aur analyze_candles me .dt crash hota tha.
      (a) parse_candles ab khaali hone par bhi "ts" ko IST datetime dtype deta hai (aur galat timestamp row hata deta hai).
      (b) Naya merge_1m(): sirf non-empty frames jodta hai + "ts" ko hamesha IST datetime me badalta hai
          (index context aur stock dono jagah). (c) analyze_candles shuru me ensure_ts() safety check.

v7.8: (1) "Strict Filter" toggle code se HATA DIYA (sidebar + Backtest dono). Strict sirf ORB + Futures OI ko mandatory karta tha,
      baaki filter default me pehle se ON the - isliye trades bekar rukti thi. ORB/OI ab bhi score me +1/-1 dete hain.
      (2) Stock signal confirm cycles default 3 -> 2.
      (3) Naya DB table confirm_log: har stock signal ka safar - kitne refresh cycle tak bana, entry hui / pullback order bana /
      guard ne roka / beech me toot gaya, pehli baar dikhne aur khatam hone ka LTP. trade_journal me naye column confirm_n
      (entry ke waqt cycles), confirm_sec, confirm_ltp0 (pehli baar signal ke waqt LTP), confirm_set (setting).
      Filter Analysis tab me "🔁 Confirm cycles" report: kitne cycle par kitne signal/trade pass, unka win % aur P&L.
      (4) Stock ke liye alag "Max SL hits per day (STOCK)" setting, default 3 (pehle index wala 2 hi stocks par lagta tha).
      (5) Watchlist me 'WAIT (need ...)' near-signal stocks default ON - sirf ek shart se chooke stock har refresh par dobara
      check honge (15 min wait nahi). Watchlist me STRONG pehle, phir EXTENDED/RS, phir WAIT - STRONG kabhi bahar nahi hote.
      Koi filter / SL / target / score ki shart dheeli NAHI ki gayi.
v7.7: PCR FILTER HATA DIYA (stock + index dono). PCR equity intraday ke liye bharosemand filter nahi tha - ab koi bhi trade
      PCR ki wajah se block nahi hota (live, pullback aur Backtest/Strict sab me). Stock PCR column, OI Writing, daily PCR
      snapshot aur PCR history ab bhi jama/dikhte hain - sirf JAANKARI ke liye, entry decision me use nahi.
v7.6.3: Pullback order khula ho aur usi disha me SAAF STRONG signal aa jaye (RSI normal, volume >= pullback limit) to order
      cancel ("UPGRADE") aur seedhi entry ka raasta khulta hai (normal confirm cycles + saare guards ke saath).
      (02-Nov RELIANCE: 14:20 EXTENDED => pullback order, 14:27 saaf STRONG par bhi order ki wajah se entry ruk jaati thi.)
v7.6.2: Pullback ki volume shart ka default 1.2 -> 1.1 (F4 Min Vol Spike ke barabar). Ab 1.1-1.2x volume wale STRONG signal
      (jaise 02-Nov RELIANCE 1.14x) seedhi entry lete hain; pullback sirf garam RSI (LONG >= 70 / SHORT <= 30) ya EXTENDED par.
v7.6.1 FIX: EXTENDED se bane pullback order ab bhi wahi saari shartein dete hain jo STRONG dete hain - RS vs peers,
      index/stock trend ke khilaaf, choppy, Stock PCR rule aur bid-ask spread (v7.6 me ye check chhoot rahe the).
v7.6: (1) Pullback entry (LONG + SHORT dono): signal aane par chase nahi - RSI zyada garam / volume kamzor / EXTENDED ho to
      VWAP ya 15m zone tak price wapas aane ka intezaar (pending order, N min valid), wahan entry. 15m trend ulta ho jaye,
      price invalidation level tod de ya time khatam ho to order cancel. (2) SL mode chuno: 1.5 x ATR(5m) (purana) /
      15m zone ke bahar / 1 x ATR(15m). Target = SL doori x R:R. Scanner me VWAP + ATR(15m) column, sidebar me pending list.
v7.5: (1) Default universe = All NSE + BSE F&O. (2) Har full scan me SAARE stocks ka har filter ka data DB (scan_log) me save
      + sidebar se CSV download. (3) 20 din ka PCR baseline banne tak running-average rule:
      jitne din ka PCR jama hai unka AVERAGE = baseline; PCR upar = LONG, neeche = SHORT (+ optional put/call writing confirm).
      (4) Sector map ~218 F&O stocks + "Sector" / "Sector Day %" column (sirf display). (5) Defaults: chase filter LONG 3.5 /
      SHORT 2.5 ATR, Min Vol Spike 1.1, OI threshold 0.15%. (6) Daily PCR snapshot sab stocks ka (pehle top 80).
      (7) Data lag fix: bade universe me candle TTL 240 sec se upar nahi jaata (pehle 218 stocks = 327 sec => stale rows).
v7.4: Stock PCR ab scanner ke SAARE stocks ka dikhta hai (pehle sirf STRONG signal wale 25 ka) - har refresh me ek batch (round-robin),
      naya 'PCR Status' column (OK / low OI / data nahi / BSE), PCR fetch error ab ERR_LOG me. Filter logic pehle jaisa hi.
v7.3: Candles DB me SABHI time frame (1m,3m,5m,10m,15m,30m,60m,1D) - backtest/export/backfill ke liye.
v7.2: Candles DB me save (candles_1m), terminal-style chart (hari/laal candles, crosshair, OHLC readout, last-price tag), kisi bhi stock ka chart.
v7.1: Charts tab - har trade ke saamne chart checkbox; candles par entry, SL (trailing path), target, partial aur exit mark.
v7.0: sidebar ke upar Capital + Leverage + Quantity basis (lot size ya capital) - Default/Strict/Manual teeno me badal sakte ho.
v6.9: Correlation guard, bid-ask spread guard, Telegram commands (/status /kill /resume /exit SYM).
v6.8: orphan-close P&L me partial profit shamil, option expiry din bhar cache (API calls aadhi), illiquid stock ka negative cache, audit/PCR-log errors ab ERR_LOG me.
v6.7: dOI-PCR edge-case fix, Strict me spcr_trend/spcr_chg_confirm, FMT formats, min-OI lot-unit auto-detect.
v6.6: Stock PCR quality: disha (delta) default ON, min option OI filter, near-ATM range 4%, optional change-in-OI PCR confirm.
v6.5: stock entry ke saare filters STOCK ke apne data par (trend, RS vs sector peers, choppy, bull/bear power) - index par nahi (option se purana mode).
v6.4: jab tak 20 din ka PCR DB me jama na ho, Fixed rule (LONG > 1.0 / SHORT < 0.8); 20 din hote hi adaptive (avg +- band).
v6.3: Stock PCR ka adaptive neutral zone - har stock ke pichhle 20 din ke average PCR ke aas-paas (± band) = neutral; upar = LONG, neeche = SHORT.
v6.2: PCR ab har STOCK ka apna (option chain) - LONG tab jab PCR > 1.0, SHORT tab jab PCR < 0.8, beech ka neutral zone = trade nahi.
v6.1: ML auto-train roz (market band ke baad), model history, calibration guard, param suggestions, backtest trades se optional training.
v6.0: Risk Desk tab (exposure, stress test, VaR/CVaR, Sharpe/Sortino/Calmar, Kelly, Monte Carlo), capital-based pre-trade limits (gross/position notional), audit log.
v5.9.1: Default/Strict ON ke saath bhi "Manual adjust" option (settings khud badal sako) + reset button.
v5.9: sidebar me "Default Setting" (permanent ON) + "Strict Filter" (sab filter ON) toggles; defaults: max trades/din 15, max positions 15, direction limit 5.
v5.8: Backtest me sidebar ke SAARE settings lagu (futures OI, PCR history, earnings lock, ML, confirm cycles, strict mode).
v5.7: partial profit, candle-replay Backtest tab, ML trade-quality filter (optional).
v5.6: direction/sector/total-risk limits, ATR risk sizing (optional), time-stop, trade features DB me + Filter Analysis tab,
Telegram day summary, live slippage log, Google Sheet me extra columns.
Run:  streamlit run nifty_fno_pro_terminal_v7_9_3.py
Tick SL ke liye (optional, recommended):  pip install upstox-python-sdk
Secrets (.streamlit/secrets.toml): UPSTOX_TOKEN, TELEGRAM_TOKEN, TELEGRAM_CHAT_ID
"""
from __future__ import annotations

import html
import json
import math
import os
import sqlite3
import threading
import time
import zlib
from collections import defaultdict, deque
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from datetime import date, datetime, time as dtime, timedelta, timezone
from urllib.parse import quote

import numpy as np
import pandas as pd
import requests
import streamlit as st

# ====== SECTION: PAGE ======
st.set_page_config(
    page_title="Institutional Nifty 50 & Bank Nifty F&O Pro Terminal",
    page_icon="🏦",
    layout="wide",
)
st.title("🏦 Institutional Nifty 50 & Bank Nifty F&O Scanner, Signal Engine & Gamma Terminal")

# ====== SECTION: CONSTANTS ======
IST = timezone(timedelta(hours=5, minutes=30))
V2 = "https://api.upstox.com/v2"
QUOTE_URL = f"{V2}/market-quote/quotes"
BNF_INDEX_KEY = "NSE_INDEX|Nifty Bank"
NIFTY_KEY = "NSE_INDEX|Nifty 50"
VIX_KEY = "NSE_INDEX|India VIX"
INSTRUMENT_URL = "https://assets.upstox.com/market-quote/instruments/exchange/NSE.json.gz"
BSE_INSTRUMENT_URL = "https://assets.upstox.com/market-quote/instruments/exchange/BSE.json.gz"
DB_PATH = "bni_institutional_signals.db"
GSHEET_ID = "1goDj8UaT6cHQN7n2ZHiVio4IWr2gVGR3mqumzQuR1Qs"   # aapki Google Sheet
GS_TRADES_TAB = "Paper_Trades"
GS_SUMMARY_TAB = "Day_Summary"

PCR_RANGE = 800        # PCR ke liye ATM se +- points
CHAIN_RANGE = 1500     # Max pain / walls ke liye range
HIST_TTL = 3600        # Daily candle stats cache
PRIOR_TTL = 1800       # Pichhle din ke 1-min candle cache
STK_MAX_PER_SYM = 2    # ek stock me din bhar max itne paper trade
STK_COOLDOWN_MIN = 30  # SL/exit ke baad same stock me dobara entry se pehle wait (min)
KILL_FILE = "KILL_SWITCH"   # is naam ki file folder me banao => sab trading band + positions square-off
UNPROT_GRACE_SEC = 25       # live position par broker SL itne sec me na lage to square-off
SL_RETRY_SEC = 8            # broker SL order retry gap
FALLBACK_LOTS = {
    "NIFTY": 75, "BANKNIFTY": 30, "FINNIFTY": 65, "MIDCPNIFTY": 120, "NIFTYNXT50": 25,
    "SENSEX": 20, "BANKEX": 30, "SENSEX50": 60,
}

INDEX_CATALOG = {
    "NIFTY":      {"name": "NIFTY 50",             "key": "NSE_INDEX|Nifty 50",          "exch": "NSE", "step": 50.0},
    "BANKNIFTY":  {"name": "NIFTY BANK",           "key": "NSE_INDEX|Nifty Bank",        "exch": "NSE", "step": 100.0},
    "FINNIFTY":   {"name": "NIFTY FIN SERV",       "key": "NSE_INDEX|Nifty Fin Service", "exch": "NSE", "step": 50.0},
    "MIDCPNIFTY": {"name": "NIFTY MIDCAP SELECT",  "key": "NSE_INDEX|NIFTY MID SELECT",  "exch": "NSE", "step": 25.0},
    "NIFTYNXT50": {"name": "NIFTY NEXT 50",        "key": "NSE_INDEX|Nifty Next 50",     "exch": "NSE", "step": 100.0},
    "SENSEX":     {"name": "SENSEX",               "key": "BSE_INDEX|SENSEX",            "exch": "BSE", "step": 100.0},
    "BANKEX":     {"name": "BANKEX",               "key": "BSE_INDEX|BANKEX",            "exch": "BSE", "step": 100.0},
    "SENSEX50":   {"name": "SENSEX 50",            "key": "BSE_INDEX|SENSEX50",          "exch": "BSE", "step": 50.0},
}
DEMO_BASE = {
    "NIFTY": 24500.0, "BANKNIFTY": 55000.0, "FINNIFTY": 26000.0, "MIDCPNIFTY": 12500.0,
    "NIFTYNXT50": 68000.0, "SENSEX": 80500.0, "BANKEX": 62000.0, "SENSEX50": 25500.0,
}
ROLL_DAYS = 1          # Expiry se itne din pehle next-month future le lo (OI/volume shift)
NSE_HOLIDAYS: set = set()   # yahan date(2026, 11, 9) jaise holidays add karo
LOCK_TXT = "🔴 NO TRADE (RESULT WEEK)"
ALLOW_TXT = "🟢 TRADE ALLOWED"
ZONE_TXT = "🟠 NO TRADE ZONE (15m consolidation)"
MKT_CHOP_TXT = "🟠 NO TRADE ZONE (MARKET CHOPPY)"
PCR_BLOCK_TXT = "🟠 NO TRADE ZONE (PCR against, solo mover nahi)"

BANKNIFTY_WEIGHTS = {
    "HDFCBANK": 29.0, "ICICIBANK": 23.0, "SBIN": 10.5, "AXISBANK": 9.5,
    "KOTAKBANK": 9.0, "INDUSINDBK": 5.5, "BANKBARODA": 3.0, "FEDERALBNK": 3.0,
    "PNB": 2.5, "IDFCFIRSTB": 2.0, "AUBANK": 1.8, "BANDHANBNK": 1.2,
}

NIFTY50_FO_WEIGHTS = {
    "HDFCBANK": 11.5, "RELIANCE": 9.2, "ICICIBANK": 8.0, "INFY": 6.0, "ITC": 4.2,
    "TCS": 4.0, "LT": 3.9, "BHARTIARTL": 3.8, "AXISBANK": 3.3, "SBIN": 3.1,
    "KOTAKBANK": 2.6, "M&M": 2.4, "HINDUNILVR": 2.1, "SUNPHARMA": 1.9, "NTPC": 1.8,
    "TATAMOTORS": 1.7, "MARUTI": 1.6, "HCLTECH": 1.6, "BAJFINANCE": 1.6, "POWERGRID": 1.4,
    "TITAN": 1.4, "ULTRACEMCO": 1.3, "ASIANPAINT": 1.2, "TATASTEEL": 1.2, "COALINDIA": 1.1,
    "ADANIPORTS": 1.0, "ONGC": 1.0, "BAJAJ-AUTO": 1.0, "BEL": 1.0, "TRENT": 1.0,
    "JSWSTEEL": 0.9, "HINDALCO": 0.9, "GRASIM": 0.9, "BAJAJFINSV": 0.9, "TECHM": 0.9,
    "INDUSINDBK": 0.8, "NESTLEIND": 0.8, "ADANIENT": 0.8, "CIPLA": 0.8, "WIPRO": 0.7,
    "SHREECEM": 0.7, "DRREDDY": 0.7, "SBILIFE": 0.7, "TATACONSUM": 0.7, "BPCL": 0.6,
    "EICHERMOT": 0.6, "APOLLOHOSP": 0.6, "HEROMOTOCO": 0.6, "BRITANNIA": 0.6, "HDFCLIFE": 0.6,
}

_SECTORS = {
    # v7.5: ~218 NSE F&O stocks ka sector map (RS vs peers, sector risk limit aur "Sector Day %" isi se banta hai)
    "BANK": "HDFCBANK ICICIBANK SBIN AXISBANK KOTAKBANK INDUSINDBK BANKBARODA FEDERALBNK PNB IDFCFIRSTB AUBANK BANDHANBNK CANBK "
            "BANKINDIA CUB INDIANB KARURVYSYA MAHABANK RBLBANK UJJIVANSFB UNIONBANK YESBANK",
    "IT": "INFY TCS HCLTECH WIPRO TECHM LTIM LTM PERSISTENT COFORGE MPHASIS OFSS KPITTECH TATAELXSI SAGILITY",
    "AUTO": "MARUTI TATAMOTORS TMPV M&M BAJAJ-AUTO EICHERMOT HEROMOTOCO TVSMOTOR ASHOKLEY HYUNDAI FORCEMOT ATHERENERG",
    "AUTO_ANC": "BOSCHLTD MOTHERSON BHARATFORG SONACOMS UNOMINDA TIINDIA",
    "PHARMA": "SUNPHARMA CIPLA DRREDDY DIVISLAB LUPIN TORNTPHARM ALKEM AUROPHARMA BIOCON GLENMARK LAURUSLABS MANKIND ZYDUSLIFE",
    "HEALTHCARE": "APOLLOHOSP FORTIS MAXHEALTH",
    "METAL": "TATASTEEL JSWSTEEL HINDALCO COALINDIA VEDL JINDALSTEL NMDC SAIL NATIONALUM HINDZINC",
    "OIL_GAS": "RELIANCE ONGC BPCL IOC GAIL HINDPETRO OIL PETRONET",
    "POWER": "NTPC POWERGRID TATAPOWER ADANIPOWER ADANIGREEN ADANIENSOL JSWENERGY NHPC IEX",
    "RENEWABLE": "SUZLON INOXWIND WAAREEENER PREMIERENE",
    "CAPGOODS": "SIEMENS ABB CGPOWER BHEL CUMMINSIND POWERINDIA GVT&D ENRIN KEI POLYCAB",
    "DEFENCE": "HAL BEL BDL MAZDOCK COCHINSHIP DATAPATTNS SOLARINDS",
    "INFRA": "LT ADANIPORTS ADANIENT GMRAIRPORT CONCOR RVNL NBCC",
    "FMCG": "HINDUNILVR ITC NESTLEIND BRITANNIA TATACONSUM DABUR GODREJCP COLPAL MARICO PATANJALI VBL UNITDSPR RADICO GODFRYPHLP",
    "NBFC": "BAJFINANCE BAJAJFINSV SHRIRAMFIN CHOLAFIN JIOFIN ABCAPITAL LTF LICHSGFIN MANAPPURAM MUTHOOTFIN PNBHOUSING SBICARD PAYTM",
    "PSU_FIN": "PFC RECLTD IRFC IREDA",
    "INSURANCE": "SBILIFE HDFCLIFE LICI ICICIGI ICICILIFE MFSL POLICYBZR",
    "CAPMKT": "HDFCAMC NAM-INDIA 360ONE ANANDRATHI ANGELONE BSE CAMS CDSL KFINTECH MCX MOTILALOFS",
    "CEMENT": "ULTRACEMCO SHREECEM GRASIM AMBUJACEM",
    "REALTY": "DLF GODREJPROP LODHA OBEROIRLTY PHOENIXLTD PRESTIGE",
    "CONSUMER": "TITAN ASIANPAINT TRENT DMART KALYANKJIL PAGEIND PIDILITIND VMM NYKAA",
    "DURABLES": "BLUESTARCO VOLTAS CROMPTON HAVELLS",
    "ELECTRONICS": "DIXON AMBER PGEL KAYNES SYRMA",
    "BUILDING": "ASTRAL SUPREMEIND APLAPOLLO",
    "CHEMICALS": "SRF PIIND UPL COROMANDEL NAVINFLUOR",
    "TELECOM": "BHARTIARTL IDEA INDUSTOWER",
    "INTERNET": "ETERNAL SWIGGY NAUKRI DELHIVERY",
    "TRAVEL_LEISURE": "INDIGO INDHOTEL JUBLFOOD",
}
SECTOR_MAP = {sym: sec for sec, names in _SECTORS.items() for sym in names.split()}


def sector_of(sym: str) -> str:
    return SECTOR_MAP.get(str(sym).upper(), "OTHER")


FIN_SECTORS = {"BANK", "NBFC", "PSU_FIN", "INSURANCE", "CAPMKT"}     # v7.9: ek saath girte/chadhte hain


def sector_group_of(sec: str) -> str:
    """v7.9: sector guard ka group. 'Bada group' mode me saare finance sectors = FINANCIALS."""
    sec = str(sec or "OTHER")
    try:
        big = str(sec_group_mode).startswith("Bada")
    except NameError:
        big = True
    return "FINANCIALS" if (big and sec in FIN_SECTORS) else sec


DEFAULT_EARNINGS_WEEK_PATTERN = {
    "TCS": 2, "INFY": 2, "WIPRO": 2, "HCLTECH": 2, "HDFCBANK": 3, "ICICIBANK": 4,
    "RELIANCE": 3, "AXISBANK": 3, "KOTAKBANK": 3, "BAJFINANCE": 3, "BAJAJFINSV": 3,
    "ITC": 4, "LT": 4, "SBIN": 4, "MARUTI": 4, "TATAMOTORS": 4, "M&M": 4,
    "HINDUNILVR": 3, "SUNPHARMA": 4, "NTPC": 4, "BHARTIARTL": 4, "TITAN": 4,
    "ULTRACEMCO": 3, "ASIANPAINT": 3, "TATASTEEL": 4, "COALINDIA": 4, "ADANIPORTS": 4,
    "ONGC": 4, "BAJAJ-AUTO": 3, "BEL": 4, "TRENT": 4, "JSWSTEEL": 3, "HINDALCO": 4,
    "GRASIM": 4, "TECHM": 3, "INDUSINDBK": 3, "NESTLEIND": 3, "ADANIENT": 4,
    "CIPLA": 3, "SHREECEM": 4, "DRREDDY": 3, "SBILIFE": 3, "TATACONSUM": 3,
    "BPCL": 4, "EICHERMOT": 4, "APOLLOHOSP": 4, "HEROMOTOCO": 4, "BRITANNIA": 4,
    "HDFCLIFE": 2, "BANKBARODA": 4, "FEDERALBNK": 3, "PNB": 4, "IDFCFIRSTB": 3,
    "AUBANK": 3, "BANDHANBNK": 3,
}

EMPTY_M = {
    "ok": False, "has_today": False, "n_today": 0, "last_ts": None, "last_close": 0.0,
    "rsi": 50.0, "adx": 0.0, "ema9": 0.0, "ema21": 0.0, "ema9_15m": 0.0, "ema21_15m": 0.0,
    "vwap": 0.0, "vwap_ok": False
