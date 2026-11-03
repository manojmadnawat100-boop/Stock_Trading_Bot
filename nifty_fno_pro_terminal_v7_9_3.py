from nicegui import ui

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
    "vwap": 0.0, "vwap_ok": False, "vwap_up1": 0.0, "vwap_dn1": 0.0, "vwap_up2": 0.0, "vwap_dn2": 0.0,
    "atr": 0.0, "orh": 0.0, "orl": 0.0, "orb_ready": False, "day_high": 0.0, "day_low": 0.0,
    "day_open": 0.0, "vol_spike": 1.0, "monthly_move_pct": 0.0, "stale_min": 0.0,
    "atr15": 0.0, "adx15": 0.0, "z15_hi": 0.0, "z15_lo": 0.0, "z15_rng_atr": 0.0, "z15_cons": False, "vwap_cross": 0,
    "bar_pos": 0.5, "pdh": 0.0, "pdl": 0.0,
}


# ====== SECTION: UTILS ======
def now_ist() -> datetime:
    return datetime.now(IST)


def secret(name: str, default: str = "") -> str:
    try:
        return st.secrets.get(name, default)
    except Exception:
        return default


def esc(x) -> str:
    return html.escape(str(x))


def show_df(data, hide_index: bool = True):
    try:
        st.dataframe(data, use_container_width=True, hide_index=hide_index)
    except Exception:
        st.dataframe(data, hide_index=hide_index)


def get_week_of_month(d: date) -> int:
    return (d.day - 1) // 7 + 1


def iso_year_week(d: date) -> tuple:
    iso = d.isocalendar()
    return int(iso[0]), int(iso[1])


def market_open(dt: datetime | None = None) -> bool:
    dt = dt or now_ist()
    if dt.weekday() >= 5 or dt.date() in NSE_HOLIDAYS:
        return False
    return dtime(9, 15) <= dt.time() <= dtime(15, 30)


def trading_days_delta(a: date, b: date) -> int:
    """a se b tak trading days. b > a => positive."""
    if a == b:
        return 0
    step = 1 if b > a else -1
    n, cur = 0, a
    while cur != b and abs(n) < 400:
        cur += timedelta(days=step)
        if cur.weekday() < 5 and cur not in NSE_HOLIDAYS:
            n += step
    return n


def to_date(x):
    try:
        if x is None or (isinstance(x, float) and math.isnan(x)) or str(x).strip() in ("", "NaT", "None"):
            return None
        return pd.to_datetime(x, dayfirst=True).date()
    except Exception:
        return None


def exp_to_str(x) -> str:
    try:
        if isinstance(x, (int, float)):
            return datetime.fromtimestamp(float(x) / 1000.0, IST).date().isoformat()
        return str(x)[:10]
    except Exception:
        return ""


def safe_float(x, default: float = 0.0) -> float:
    try:
        v = float(x)
        return default if math.isnan(v) else v
    except Exception:
        return default


def generate_trade_special_note(rec: dict) -> str:
    """Trade ka Hinglish 'Special Note' (profit/loss ka karan + sudhar)."""
    pnl = safe_float(rec.get("pnl_rs"))
    pts = safe_float(rec.get("pts"))
    side = str(rec.get("side", "LONG")).upper()
    d = 1 if side == "LONG" else -1
    reason = str(rec.get("exit_reason", "")).upper()
    itype = str(rec.get("instrument_type", "INDEX"))
    entry = safe_float(rec.get("entry"))
    sl0 = safe_float(rec.get("sl0")) or safe_float(rec.get("sl"))
    mfe = safe_float(rec.get("mfe"))
    score = safe_float(rec.get("bull_pwr"), float("nan"))
    pcr = safe_float(rec.get("pcr"))
    vix = safe_float(rec.get("vix"))
    mins = safe_float(rec.get("mins"), float("nan"))

    risk = abs(entry - sl0) if (entry and sl0 and abs(entry - sl0) > 1e-6) else 0.0
    r_mult = (pts / risk) if risk > 0 else 0.0
    parts = []

    # ---- setup quality ----
    setup = []
    if itype == "INDEX" and not math.isnan(score):
        aligned = score >= 60 if d == 1 else score <= 40
        setup.append(f"Bull power {score:.0f}% ({'direction ke saath' if aligned else 'direction ke against/kamzor'})")
    elif itype != "INDEX" and not math.isnan(score):
        strong = abs(score) >= 5
        setup.append(f"Entry score {score:+.0f} ({'strong' if strong else 'average'})")
    if pcr > 0:
        pcr_ok = pcr >= 1.0 if d == 1 else pcr <= 1.0
        setup.append(f"PCR {pcr:.2f} ({'favour me' if pcr_ok else 'ulta'})")

    if abs(pnl) < 1e-9:
        parts.append("⚪ BREAKEVEN: Trade flat band hua (trailing SL entry par laga tha).")
        if mfe > 0 and risk > 0:
            parts.append(f"Beech me {mfe / risk:.1f}R tak profit tha - jab 1R mile tab partial profit lene par vichar karo.")

    elif pnl > 0:
        parts.append(f"🟢 PROFIT Rs {pnl:,.0f}" + (f" ({r_mult:.1f}R)" if r_mult is not None else "") + f": {side} trade chala.")
        if "TARGET" in reason:
            parts.append("Target hit - SL/Target ka ATR-based plan sahi baitha.")
        elif "TRAIL" in reason:
            parts.append("Trailing SL ne profit lock kiya - trail ka system kaam kar raha hai.")
        elif "EOD" in reason:
            parts.append("EOD par profit me band hua - trade din bhar chala.")
        elif "FADE" in reason or "OPPOSITE" in reason or "FLIP" in reason:
            parts.append("Signal palatne par samay se exit kiya - achha discipline.")
        if setup:
            parts.append("Setup: " + ", ".join(setup) + ".")
        if mfe > 0 and pts > 0 and mfe > pts * 1.5:
            parts.append(f"⚠ Peak profit {mfe:.1f} pts tha par mila {pts:.1f} pts - "
                         f"{(1 - pts / mfe) * 100:.0f}% wapas gaya. Trailing thodi tight karne par vichar karo.")
        parts.append("SUDHAR: Isi entry timing aur alignment ko repeat karo; size mat badhao jab tak 30+ trades ka data na ho.")

    else:
        parts.append(f"🔴 LOSS Rs {pnl:,.0f}" + (f" ({r_mult:.1f}R)" if r_mult is not None else "") +
                     f": {side} trade fail hua, exit: {rec.get('exit_reason', '-')}.")
        if "SL" in reason:
            if not math.isnan(mins) and mins <= 10:
                parts.append(f"SL sirf {mins:.0f} min me lag gaya - entry chase/whipsaw ka sanket. Pullback ka wait karo.")
            else:
                parts.append("SL hit: market ne entry ke ulta reversal kiya.")
        elif "TIME STOP" in reason:
            parts.append("Time-stop: trade der tak chala par aage nahi badha - sust chaal me paisa atkane se behtar hai nikalna.")
        elif "OPPOSITE" in reason or "FLIP" in reason or "FADE" in reason:
            parts.append("Signal jaldi palat gaya - confirmation cycles/min score badhao.")
        elif "KILL" in reason or "MAX LOSS" in reason or "UNPROTECTED" in reason or "HALT" in reason:
            parts.append("Safety rule se force-exit hua - risk system ne apna kaam kiya.")
        elif "EOD" in reason:
            parts.append("Din bhar trade chala par EOD par loss me band - trend/momentum nahi tha.")
        if vix > 20:
            parts.append(f"VIX {vix:.1f} high tha - false breakout ke chance zyada.")
        if setup:
            parts.append("Setup: " + ", ".join(setup) + ".")
        if "ulta" in " ".join(setup):
            parts.append("PCR trade ke ulta tha (sirf jaankari - v7.7 me PCR filter nahi hai).")
        if mfe > 0 and risk > 0 and mfe >= risk:
            parts.append(f"⚠ Trade pehle {mfe / risk:.1f}R profit me tha phir loss me gaya - breakeven trail jaldi lagao.")
        parts.append("SUDHAR: 15m consolidation aur high-VIX din par filter kadi karo, aur confirmation candle ka wait karo.")

    part = safe_float(rec.get("part_pnl"))
    if part:
        parts.append(f"Partial profit Rs {part:,.0f} pehle hi book ho chuka tha (final P&L me judaa hai).")
    return " | ".join(parts)


def _trade_minutes(rec: dict) -> float:
    try:
        a = pd.to_datetime(f"{rec['dt']} {rec['entry_time']}")
        b = pd.to_datetime(f"{rec['dt']} {rec['exit_time']}")
        return round((b - a).total_seconds() / 60.0, 1)
    except Exception:
        return float("nan")


# ====== SECTION: DATABASE (Live Open/Update/Close & Auto-Migration) ======
DB_ERR = ""


@contextmanager
def db():
    conn = sqlite3.connect(DB_PATH, timeout=15)
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db():
    global DB_ERR
    try:
        with db() as conn:
            try:
                conn.execute("PRAGMA journal_mode=WAL")
            except Exception:
                pass
            conn.execute("""
                CREATE TABLE IF NOT EXISTS signal_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, dt TEXT, time_ist TEXT, event TEXT,
                    spot REAL, bull_pwr REAL, bear_pwr REAL, pcr REAL, vix REAL,
                    sl REAL, tgt REAL, reason TEXT
                )""")
            # v7.5: har full scan (5-min slot) me har stock ke saare filter values - baad me analysis / backtest ke liye
            conn.execute("""
                CREATE TABLE IF NOT EXISTS scan_log (
                    dt TEXT, slot TEXT, time_ist TEXT, sym TEXT, action TEXT, score REAL, ltp REAL, day_pct REAL,
                    stock_pcr REAL, data TEXT, PRIMARY KEY (dt, slot, sym)
                )""")
            conn.execute("""
                CREATE TABLE IF NOT EXISTS trade_journal (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    dt TEXT,
                    symbol TEXT DEFAULT 'INDEX',
                    instrument_type TEXT DEFAULT 'INDEX',
                    side TEXT,
                    status TEXT DEFAULT 'CLOSED',
                    entry_time TEXT,
                    exit_time TEXT,
                    entry REAL,
                    exit REAL,
                    sl REAL DEFAULT 0.0,
                    tgt REAL DEFAULT 0.0,
                    sl0 REAL DEFAULT 0.0,
                    pts REAL,
                    pnl_rs REAL,
                    lots INTEGER,
                    lot_size INTEGER,
                    exit_reason TEXT,
                    mfe REAL,
                    mae REAL,
                    bull_pwr REAL,
                    pcr REAL,
                    vix REAL,
                    mode TEXT DEFAULT 'LIVE'
                )""")
            # Auto-migration for existing DB files without losing old data
            existing_cols = {r[1] for r in conn.execute("PRAGMA table_info(trade_journal)").fetchall()}
            migrations = [
                ("symbol", "TEXT DEFAULT 'INDEX'"),
                ("instrument_type", "TEXT DEFAULT 'INDEX'"),
                ("status", "TEXT DEFAULT 'CLOSED'"),
                ("sl", "REAL DEFAULT 0.0"),
                ("tgt", "REAL DEFAULT 0.0"),
                ("mode", "TEXT DEFAULT 'LIVE'"),
                ("note", "TEXT DEFAULT ''"),
                ("sl0", "REAL DEFAULT 0.0"),
                ("adx", "REAL"), ("volx", "REAL"), ("rs_idx", "REAL"), ("rank_v", "REAL"), ("atr_v", "REAL"),
                ("sector", "TEXT DEFAULT ''"),
                ("part_pnl", "REAL DEFAULT 0.0"), ("part_qty", "INTEGER DEFAULT 0"), ("ml_prob", "REAL"),
                # v7.8: confirm cycles ka record (entry ke waqt kitne cycle, kitne sec, pehli baar signal par LTP, setting, route)
                ("confirm_n", "INTEGER"), ("confirm_sec", "REAL"), ("confirm_ltp0", "REAL"), ("confirm_set", "INTEGER"),
                ("confirm_route", "TEXT DEFAULT ''"),
                ("sig_side", "TEXT DEFAULT ''"),           # v7.9.1: signal ki disha (reverse mode me trade side se alag)
            ]
            for col_name, col_def in migrations:
                if col_name not in existing_cols:
                    conn.execute(f"ALTER TABLE trade_journal ADD COLUMN {col_name} {col_def}")

            conn.execute("UPDATE trade_journal SET instrument_type = 'EQUITY_INTRADAY' WHERE instrument_type = 'STOCK_FO'")
            conn.execute("""
                CREATE TABLE IF NOT EXISTS live_orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, dt TEXT, ts TEXT, symbol TEXT, action TEXT,
                    side TEXT, qty INTEGER, order_id TEXT, status TEXT, msg TEXT
                )""")
            conn.execute("CREATE TABLE IF NOT EXISTS kv (k TEXT PRIMARY KEY, v TEXT)")
            # v7.8: har stock signal ka confirm-cycle safar (entry / pullback order / guard / toot gaya)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS confirm_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, dt TEXT, sym TEXT, side TEXT, t_first TEXT, t_end TEXT,
                    cycles INTEGER, secs REAL, need INTEGER, outcome TEXT, ltp_first REAL, ltp_end REAL,
                    trade_id INTEGER, note TEXT, mode TEXT
                )""")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_confirm_log ON confirm_log (dt, sym)")
            conn.execute("DELETE FROM confirm_log WHERE dt < date('now', '-120 day')")
            conn.execute("""
                CREATE TABLE IF NOT EXISTS pcr_hist (
                    dt TEXT, tm TEXT, und TEXT, pcr REAL, pcr_delta REAL
                )""")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_pcr_hist ON pcr_hist (und, dt, tm)")
            conn.execute("""
                CREATE TABLE IF NOT EXISTS audit_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, dt TEXT, tm TEXT, event TEXT, symbol TEXT, side TEXT, detail TEXT
                )""")
            conn.execute("DELETE FROM audit_log WHERE dt < date('now', '-60 day')")
            conn.execute("""
                CREATE TABLE IF NOT EXISTS ml_history (
                    dt TEXT, tm TEXT, n INTEGER, auc REAL, acc REAL, base REAL, gap REAL, valid INTEGER, note TEXT
                )""")
            conn.execute("""
                CREATE TABLE IF NOT EXISTS pcr_daily (
                    dt TEXT, sym TEXT, pcr REAL, PRIMARY KEY (dt, sym)
                )""")
            conn.execute("""
                CREATE TABLE IF NOT EXISTS candles_1m (
                    sym TEXT, ts TEXT, o REAL, h REAL, l REAL, c REAL, v REAL, PRIMARY KEY (sym, ts)
                )""")
            conn.execute("DELETE FROM candles_1m WHERE ts < date('now', '-60 day')")
            conn.execute("""
                CREATE TABLE IF NOT EXISTS candles_tf (
                    sym TEXT, tf TEXT, ts TEXT, o REAL, h REAL, l REAL, c REAL, v REAL, PRIMARY KEY (sym, tf, ts)
                )""")
            conn.execute("DELETE FROM candles_tf WHERE tf != '1D' AND ts < date('now', '-60 day')")
            conn.execute("DELETE FROM candles_tf WHERE tf = '1D' AND ts < date('now', '-800 day')")
            conn.execute("""
                CREATE TABLE IF NOT EXISTS trade_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, trade_id INTEGER, dt TEXT, tm TEXT,
                    kind TEXT, price REAL, price2 REAL, note TEXT
                )""")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_trade_events ON trade_events (trade_id)")
            conn.execute("DELETE FROM trade_events WHERE dt < date('now', '-90 day')")
            conn.execute("""
                CREATE TABLE IF NOT EXISTS bt_trades (
                    dt TEXT, sym TEXT, side TEXT, tin TEXT, score REAL, adx REAL, volx REAL, rs REAL, rank_v REAL,
                    atr REAL, entry REAL, pnl REAL, PRIMARY KEY (dt, sym, side, tin)
                )""")
            conn.execute("""
                CREATE TABLE IF NOT EXISTS earnings_calendar (
                    symbol TEXT PRIMARY KEY,
                    result_date TEXT
                )""")
            conn.execute("CREATE INDEX IF NOT EXISTS ix_journal_dt ON trade_journal(dt)")
            conn.execute("CREATE INDEX IF NOT EXISTS ix_journal_status ON trade_journal(status)")
            conn.execute("CREATE INDEX IF NOT EXISTS ix_journal_sym ON trade_journal(symbol)")
    except Exception as e:
        DB_ERR = str(e)


def close_orphan_open_trades(today_iso: str, last_ltp: float = 0.0) -> None:
    """Pichhle din ke jo trade app band hone se OPEN reh gaye, unhe CLOSED mark karo (last known LTP aur P&L ke saath)."""
    try:
        with db() as conn:
            conn.execute(
                """UPDATE trade_journal
                   SET status = 'CLOSED',
                       exit = CASE WHEN ? > 0 THEN ROUND(?, 2)
                                   WHEN exit IS NULL OR exit <= 0 THEN entry
                                   ELSE exit END,
                       pts = ROUND(
                           ((CASE WHEN ? > 0 THEN ?
                                  WHEN exit IS NULL OR exit <= 0 THEN entry
                                  ELSE exit END) - entry)
                           * (CASE WHEN UPPER(side) = 'LONG' THEN 1.0 ELSE -1.0 END), 2
                       ),
                       pnl_rs = ROUND(
                           COALESCE(part_pnl, 0.0) +
                           ((CASE WHEN ? > 0 THEN ?
                                  WHEN exit IS NULL OR exit <= 0 THEN entry
                                  ELSE exit END) - entry)
                           * (CASE WHEN UPPER(side) = 'LONG' THEN 1.0 ELSE -1.0 END)
                           * MAX(1, COALESCE(lots, 1) * COALESCE(lot_size, 1) - COALESCE(part_qty, 0)), 2
                       ),
                       exit_time = CASE WHEN exit_time IN ('-', '') OR exit_time IS NULL THEN '15:30:00' ELSE exit_time END,
                       exit_reason = 'ORPHAN: app band tha, last LTP (' || ROUND(CASE WHEN ? > 0 THEN ? WHEN exit IS NULL OR exit <= 0 THEN entry ELSE exit END, 2) || ') par close'
                   WHERE status = 'OPEN' AND dt < ?""",
                (last_ltp, last_ltp, last_ltp, last_ltp, last_ltp, last_ltp, last_ltp, last_ltp, today_iso),
            )
    except Exception:
        pass


def save_earnings_date(symbol: str, dt_str: str):
    try:
        with db() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO earnings_calendar (symbol, result_date) VALUES (?, ?)",
                (symbol.upper().strip(), dt_str.strip()),
            )
    except Exception:
        pass


def delete_earnings_date(symbol: str):
    try:
        with db() as conn:
            conn.execute("DELETE FROM earnings_calendar WHERE symbol = ?", (symbol.upper().strip(),))
    except Exception:
        pass


def load_custom_earnings() -> dict:
    try:
        with db() as conn:
            rows = conn.execute("SELECT symbol, result_date FROM earnings_calendar").fetchall()
        return {r[0]: r[1] for r in rows if r[1]}
    except Exception:
        return {}


def resolve_earnings_status(symbol: str, custom_map: dict, today: date, mode: str, pre_days: int, post_days: int,
                            use_pattern: bool = True) -> dict:
    r_dt = None
    if symbol in custom_map:
        cand = to_date(custom_map[symbol])
        if cand and today - timedelta(days=45) <= cand <= today + timedelta(days=150):
            r_dt = cand

    if r_dt is not None:
        delta = trading_days_delta(today, r_dt)
        if mode == "Window":
            locked = -post_days <= delta <= pre_days
        else:
            locked = iso_year_week(r_dt) == iso_year_week(today)
        return {
            "result_week": f"Week {get_week_of_month(r_dt)} ({r_dt.strftime('%d %b')})",
            "result_date": r_dt.isoformat(), "source": "Exact", "is_result_week": locked,
            "trade_status": LOCK_TXT if locked else ALLOW_TXT,
        }

    expected_wk = DEFAULT_EARNINGS_WEEK_PATTERN.get(symbol, 4)
    is_earn_month = today.month in (1, 2, 4, 5, 7, 8, 10, 11)
    locked = (use_pattern and (symbol in DEFAULT_EARNINGS_WEEK_PATTERN) and is_earn_month
              and get_week_of_month(today) == expected_wk)
    label = f"~Week {expected_wk} ({today.strftime('%b')})" if is_earn_month else f"Next Qtr ~Week {expected_wk}"
    return {
        "result_week": label, "result_date": "", "source": "Pattern (approx)", "is_result_week": locked,
        "trade_status": LOCK_TXT if locked else ALLOW_TXT,
    }


def log_to_db(dt_str, time_str, event, spot, bull, bear, pcr, vix, sl, tgt, reason):
    try:
        with db() as conn:
            conn.execute(
                """INSERT INTO signal_history
                   (dt, time_ist, event, spot, bull_pwr, bear_pwr, pcr, vix, sl, tgt, reason)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (dt_str, time_str, event, spot, bull, bear, pcr, vix, sl, tgt, reason),
            )
    except Exception:
        pass


def fetch_db_logs(limit: int = 100) -> pd.DataFrame:
    try:
        with db() as conn:
            return pd.read_sql_query(
                'SELECT dt AS "Date", time_ist AS "Time", event AS "Event", spot AS "Spot", '
                'bull_pwr AS "Bull%", bear_pwr AS "Bear%", pcr AS "PCR", vix AS "VIX", '
                'sl AS "SL", tgt AS "Target", reason AS "Reason" '
                "FROM signal_history ORDER BY id DESC LIMIT ?",
                conn, params=(int(limit),),
            )
    except Exception:
        return pd.DataFrame()


def _journal_open_trade_core(rec: dict) -> int:
    """Trade ENTRY hote hi DB mein OPEN status ke saath save karega aur row ID return karega."""
    try:
        with db() as conn:
            row = conn.execute(
                "SELECT id FROM trade_journal WHERE dt = ? AND symbol = ? AND instrument_type = ? AND status = 'OPEN' LIMIT 1",
                (rec["dt"], rec.get("symbol", "INDEX"), rec.get("instrument_type", "INDEX")),
            ).fetchone()
            if row:
                return int(row[0])

            cur = conn.execute(
                """INSERT INTO trade_journal
                   (dt, symbol, instrument_type, side, status, entry_time, exit_time,
                    entry, exit, sl, tgt, pts, pnl_rs, lots, lot_size, exit_reason,
                    mfe, mae, bull_pwr, pcr, vix, mode, sl0, adx, volx, rs_idx, rank_v, atr_v, sector, ml_prob)
                   VALUES (?,?,?,?, 'OPEN', ?, '-', ?, ?, ?, ?, 0.0, 0.0, ?, ?, 'LIVE OPEN', 0.0, 0.0, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    rec["dt"], rec.get("symbol", "INDEX"), rec.get("instrument_type", "INDEX"),
                    rec["side"], rec["entry_time"], round(float(rec["entry"]), 2), round(float(rec["entry"]), 2),
                    round(float(rec.get("sl", 0.0)), 2), round(float(rec.get("tgt", 0.0)), 2),
                    int(rec.get("lots", 1)), int(rec.get("lot_size", 1)),
                    round(float(rec.get("bull_pwr", 0.0)), 2), round(float(rec.get("pcr", 0.0)), 2),
                    round(float(rec.get("vix", 0.0)), 2), rec.get("mode", "LIVE"),
                    round(float(rec.get("sl", 0.0)), 2),
                    round(safe_float(rec.get("adx")), 2), round(safe_float(rec.get("volx")), 2),
                    round(safe_float(rec.get("rs_idx")), 2), round(safe_float(rec.get("rank_v")), 2),
                    round(safe_float(rec.get("atr_v")), 2), str(rec.get("sector", "") or ""),
                    round(safe_float(rec.get("ml_prob")), 3),
                ),
            )
            return int(cur.lastrowid)
    except Exception:
        return 0


def journal_update_open_trade(trade_id: int, ltp: float, sl: float, pts: float, pnl_rs: float, mfe: float, mae: float):
    """Har refresh par OPEN trade ka running LTP, P&L, MFE/MAE aur trailing SL DB mein update karega."""
    if not trade_id:
        return
    try:
        with db() as conn:
            conn.execute(
                """UPDATE trade_journal
                   SET exit = ?, sl = ?, pts = ?, pnl_rs = ?, mfe = ?, mae = ?
                   WHERE id = ? AND status = 'OPEN'""",
                (round(ltp, 2), round(sl, 2), round(pts, 2), round(pnl_rs, 2), round(mfe, 2), round(mae, 2), int(trade_id)),
            )
    except Exception:
        pass


def journal_open_trade(rec: dict) -> int:
    tid = _journal_open_trade_core(rec)
    trade_event(tid, "ENTRY", safe_float(rec.get("entry")), safe_float(rec.get("sl")), f"tgt {safe_float(rec.get('tgt')):.2f}")
    audit("ENTRY", rec.get("symbol", ""), rec.get("side", ""),
          f"entry {safe_float(rec.get('entry')):.2f} | SL {safe_float(rec.get('sl')):.2f} | TGT {safe_float(rec.get('tgt')):.2f} | "
          f"qty {int(safe_float(rec.get('lots'), 1) * safe_float(rec.get('lot_size'), 1))} | score {rec.get('bull_pwr')} | {rec.get('mode', '')}")
    return tid


def journal_close_trade(trade_id: int, rec: dict):
    r = _journal_close_trade_core(trade_id, rec)
    trade_event(trade_id, "EXIT", safe_float(rec.get("exit")), safe_float(rec.get("pnl_rs")), str(rec.get("exit_reason", "")))
    audit("EXIT", rec.get("symbol", ""), rec.get("side", ""),
          f"{rec.get('exit_reason', '')} | exit {safe_float(rec.get('exit')):.2f} | P&L Rs {safe_float(rec.get('pnl_rs')):+,.0f}")
    return r


def journal_partial(trade_id: int, part_qty: int, part_pnl: float) -> None:
    """Partial profit book hone par OPEN row me booked qty / P&L save."""
    if not trade_id:
        return
    try:
        with db() as conn:
            conn.execute("UPDATE trade_journal SET part_qty = ?, part_pnl = ? WHERE id = ? AND status = 'OPEN'",
                         (int(part_qty), round(float(part_pnl), 2), int(trade_id)))
    except Exception:
        pass


def journal_set_sig(trade_id: int, sig: str) -> None:
    """v7.9.1: trade ke saath original signal ki disha (reverse mode ka hisaab rakhne ke liye)."""
    if not trade_id:
        return
    try:
        with db() as conn:
            conn.execute("UPDATE trade_journal SET sig_side = ? WHERE id = ?", (str(sig or ""), int(trade_id)))
    except Exception:
        pass


def load_sig_flags(st_map: dict) -> None:
    """v7.9.1: app restart par khule trade ka 'rev' flag DB se wapas (warna OPPOSITE SIGNAL galat exit karta)."""
    ids = {int(p.get("db_id") or 0): k for k, p in st_map.items() if p.get("db_id")}
    if not ids:
        return
    try:
        with db() as conn:
            rows = conn.execute(f"SELECT id, COALESCE(sig_side, '') FROM trade_journal WHERE id IN ({','.join('?' * len(ids))})",
                                tuple(ids)).fetchall()
        for tid, sg in rows:
            p = st_map.get(ids.get(int(tid)))
            if p and sg in ("LONG", "SHORT"):
                p["sig"] = sg
                p["rev"] = sg != p["side"]
    except Exception:
        pass


def journal_set_confirm(trade_id: int, ci: dict) -> None:
    """v7.8: trade ke saath confirm-cycle info save (kitne cycle par entry, kitne sec, pehli baar signal par LTP)."""
    if not trade_id or not ci:
        return
    try:
        with db() as conn:
            conn.execute("UPDATE trade_journal SET confirm_n = ?, confirm_sec = ?, confirm_ltp0 = ?, confirm_set = ?, confirm_route = ? "
                         "WHERE id = ?",
                         (int(ci.get("n", 0)), round(safe_float(ci.get("sec")), 1), round(safe_float(ci.get("ltp0")), 2),
                          int(ci.get("need", 0)), str(ci.get("route", ""))[:40], int(trade_id)))
    except Exception as e:
        try:
            ERR_LOG.append((now_ist().strftime("%H:%M:%S"), -1, "confirm-journal", str(e)[:120]))
        except Exception:
            pass


def confirm_log_write(day: str, sym: str, p: dict, outcome: str, ltp_end: float = 0.0, trade_id: int = 0, note: str = "") -> None:
    """v7.8: ek signal ka confirm safar DB (confirm_log) me - kitne cycle tak bana aur kaise khatam hua."""
    if not p:
        return
    try:
        now = now_ist()
        t0 = float(p.get("t0") or p.get("t") or time.time())
        with db() as conn:
            conn.execute(
                "INSERT INTO confirm_log (dt, sym, side, t_first, t_end, cycles, secs, need, outcome, ltp_first, ltp_end, trade_id, note, mode) "
                "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (str(day), str(sym), str(p.get("side", "")), str(p.get("tf", "")), now.strftime("%H:%M:%S"),
                 int(p.get("n", 0)), round(time.time() - t0, 1), int(p.get("need", 0) or 0), str(outcome)[:60],
                 round(safe_float(p.get("ltp0")), 2), round(safe_float(ltp_end), 2), int(trade_id or 0), str(note)[:200],
                 str(p.get("mode", ""))))
    except Exception as e:
        try:
            ERR_LOG.append((now_ist().strftime("%H:%M:%S"), -1, "confirm-log", str(e)[:120]))
        except Exception:
            pass


def _journal_close_trade_core(trade_id: int, rec: dict):
    """Trade EXIT hone par usi OPEN row ko CLOSED mein update karega (ya naya insert karega agar ID na ho)."""
    try:
        exit_t = str(rec.get("exit_time") or now_ist().strftime("%H:%M:%S"))
        entry_t = str(rec.get("entry_time") or exit_t)
        rec_norm = {**rec, "entry_time": entry_t, "exit_time": exit_t}
        try:
            note = generate_trade_special_note({**rec_norm, "mins": rec_norm.get("mins", _trade_minutes(rec_norm))})
        except Exception:
            note = ""
        with db() as conn:
            if trade_id:
                cur = conn.execute(
                    """UPDATE trade_journal
                       SET status = 'CLOSED', exit_time = ?, exit = ?, sl = ?, tgt = ?,
                           pts = ?, pnl_rs = ?, exit_reason = ?, mfe = ?, mae = ?, note = ?
                       WHERE id = ?""",
                    (
                        exit_t, round(safe_float(rec.get("exit")), 2),
                        round(safe_float(rec.get("sl", 0.0)), 2), round(safe_float(rec.get("tgt", 0.0)), 2),
                        round(safe_float(rec.get("pts")), 2), round(safe_float(rec.get("pnl_rs")), 2),
                        str(rec.get("exit_reason", "CLOSED")),
                        round(safe_float(rec.get("mfe")), 2), round(safe_float(rec.get("mae")), 2),
                        note, int(trade_id),
                    ),
                )
                if cur.rowcount > 0:
                    return
            # Fallback: agar trade_id match na hua par DB mein usi din/symbol ka OPEN trade ho to use update karein
            cur2 = conn.execute(
                """UPDATE trade_journal
                   SET status = 'CLOSED', exit_time = ?, exit = ?, sl = ?, tgt = ?,
                       pts = ?, pnl_rs = ?, exit_reason = ?, mfe = ?, mae = ?, note = ?
                   WHERE dt = ? AND symbol = ? AND instrument_type = ? AND status = 'OPEN'""",
                (
                    exit_t, round(safe_float(rec.get("exit")), 2),
                    round(safe_float(rec.get("sl", 0.0)), 2), round(safe_float(rec.get("tgt", 0.0)), 2),
                    round(safe_float(rec.get("pts")), 2), round(safe_float(rec.get("pnl_rs")), 2),
                    str(rec.get("exit_reason", "CLOSED")),
                    round(safe_float(rec.get("mfe")), 2), round(safe_float(rec.get("mae")), 2),
                    note, str(rec.get("dt", now_ist().strftime("%Y-%m-%d"))),
                    str(rec.get("symbol", "INDEX")), str(rec.get("instrument_type", "INDEX")),
                ),
            )
            if cur2.rowcount > 0:
                return
            cols = (
                "dt", "symbol", "instrument_type", "side", "status",
                "entry_time", "exit_time", "entry", "exit", "sl", "tgt",
                "pts", "pnl_rs", "lots", "lot_size", "exit_reason",
                "mfe", "mae", "bull_pwr", "pcr", "vix", "mode", "note",
            )
            vals = (
                str(rec.get("dt", now_ist().strftime("%Y-%m-%d"))),
                str(rec.get("symbol", "INDEX")),
                str(rec.get("instrument_type", "INDEX")),
                str(rec.get("side", "LONG")),
                "CLOSED",
                entry_t,
                exit_t,
                round(safe_float(rec.get("entry")), 2),
                round(safe_float(rec.get("exit")), 2),
                round(safe_float(rec.get("sl", 0.0)), 2),
                round(safe_float(rec.get("tgt", 0.0)), 2),
                round(safe_float(rec.get("pts")), 2),
                round(safe_float(rec.get("pnl_rs")), 2),
                int(safe_float(rec.get("lots", 1), 1)),
                int(safe_float(rec.get("lot_size", 1), 1)),
                str(rec.get("exit_reason", "CLOSED")),
                round(safe_float(rec.get("mfe")), 2),
                round(safe_float(rec.get("mae")), 2),
                round(safe_float(rec.get("bull_pwr", 0.0)), 2),
                round(safe_float(rec.get("pcr", 0.0)), 2),
                round(safe_float(rec.get("vix", 0.0)), 2),
                str(rec.get("mode", "DEMO" if demo_mode else "LIVE")),
                note,
            )
            placeholders = ",".join(["?"] * len(cols))
            conn.execute(
                f"INSERT INTO trade_journal ({', '.join(cols)}) VALUES ({placeholders})",
                vals,
            )
    except Exception:
        pass


def fetch_open_stock_trades(today_iso: str) -> dict:
    """App restart hone par DB se aaj ke OPEN stock trades (MFE, MAE aur peak ke saath) wapas memory mein recover karta hai."""
    try:
        with db() as conn:
            rows = conn.execute(
                """SELECT id, symbol, side, entry, exit, sl, tgt, lots, lot_size, entry_time,
                          COALESCE(mfe, 0.0) AS mfe, COALESCE(mae, 0.0) AS mae, bull_pwr,
                          COALESCE(sl0, 0.0) AS sl0, COALESCE(sector, '') AS sector,
                          COALESCE(part_qty, 0) AS part_qty, COALESCE(part_pnl, 0.0) AS part_pnl
                   FROM trade_journal
                   WHERE dt = ? AND instrument_type = 'EQUITY_INTRADAY' AND status = 'OPEN'""",
                (today_iso,),
            ).fetchall()
        out = {}
        for r in rows:
            tid, sym, side, entry, cur_exit, sl, tgt, lots, lsz, tin, mfe, mae, sc, sl0_db, sector_db, pq_db, pp_db = r
            lots_i = int(lots or 1)
            lsz_i = int(lsz or 1)
            entry_f = float(entry or 0.0)
            mfe_f = float(mfe or 0.0)
            mae_f = float(mae or 0.0)
            side_s = str(side or "LONG").upper()
            d_dir = 1 if side_s == "LONG" else -1
            peak_f = (entry_f + d_dir * mfe_f) if mfe_f > 0 else float(cur_exit or entry_f)
            out[sym] = {
                "db_id": int(tid), "side": side_s, "entry": entry_f,
                "sl": float(sl or 0.0), "sl0": float(sl0_db or sl or 0.0), "tgt": float(tgt or 0.0),
                "sector": str(sector_db or sector_of(sym)),
                "peak": round(peak_f, 2), "lots": lots_i, "lot_size": lsz_i,
                "qty": max(1, lots_i * lsz_i - int(pq_db or 0)), "qty0": lots_i * lsz_i, "part_qty": int(pq_db or 0),
                "part_pnl": float(pp_db or 0.0), "partial_done": int(pq_db or 0) > 0, "t_entry": str(tin or ""),
                "mfe": mfe_f, "mae": mae_f, "score": float(sc or 0.0),
            }
        return out
    except Exception:
        return {}


def fetch_stock_trade_counts(today_iso: str) -> dict:
    """App restart ke baad bhi cooldown/max-trade count aur last_trade_result sahi rahe."""
    try:
        with db() as conn:
            rows = conn.execute(
                "SELECT symbol, COUNT(*), SUM(CASE WHEN exit_reason LIKE '%SL HIT%' AND pnl_rs < 0 THEN 1 ELSE 0 END) "
                "FROM trade_journal WHERE dt = ? AND instrument_type = 'EQUITY_INTRADAY' GROUP BY symbol",
                (today_iso,),
            ).fetchall()
            last_rows = conn.execute(
                "SELECT symbol, pnl_rs FROM trade_journal "
                "WHERE dt = ? AND instrument_type = 'EQUITY_INTRADAY' AND status = 'CLOSED' ORDER BY id ASC",
                (today_iso,),
            ).fetchall()
        last_map = {r[0]: float(r[1] or 0.0) for r in last_rows}
        return {
            r[0]: {
                "n": int(r[1]),
                "t": time.time(),
                "blocked": bool(r[2]),
                "last_result": last_map.get(r[0], 0.0),
            }
            for r in rows
        }
    except Exception:
        return {}


def stk_day_stats(day: str, mode: str) -> tuple:
    """(din ka running P&L [open samet], lagataar loss count, aaj ke total stock trades, aaj ke SL hits)."""
    try:
        with db() as conn:
            base = "FROM trade_journal WHERE dt = ? AND instrument_type = 'EQUITY_INTRADAY' AND mode = ?"
            pnl = conn.execute(f"SELECT COALESCE(SUM(pnl_rs), 0) {base}", (day, mode)).fetchone()[0]
            n = conn.execute(f"SELECT COUNT(*) {base}", (day, mode)).fetchone()[0]
            sl_hits = conn.execute(
                f"SELECT COUNT(*) {base} AND status = 'CLOSED' AND UPPER(exit_reason) LIKE '%SL HIT%' AND pnl_rs < 0",
                (day, mode),
            ).fetchone()[0]
            rows = conn.execute(f"SELECT pnl_rs {base} AND status = 'CLOSED' ORDER BY exit_time DESC, id DESC LIMIT 10",
                                (day, mode)).fetchall()
        cons = 0
        for (v,) in rows:
            if float(v or 0) < 0:
                cons += 1
            else:
                break
        return float(pnl or 0), cons, int(n or 0), int(sl_hits or 0)
    except Exception:
        return 0.0, 0, 0, 0


def fetch_journal(limit: int = 500, status_filter: str = "ALL", inst_filter: str = "ALL", mode_filter: str = "ALL") -> pd.DataFrame:
    try:
        with db() as conn:
            q = (
                'SELECT id AS "ID", dt AS "Date", symbol AS "Symbol", instrument_type AS "Type", '
                'side AS "Side", status AS "Status", entry_time AS "In", exit_time AS "Out", '
                'entry AS "Entry", exit AS "LTP/Exit", sl AS "SL", tgt AS "Target", '
                'pts AS "Pts", pnl_rs AS "P&L Rs", lots AS "Lots", lot_size AS "LotSize", '
                'exit_reason AS "Reason", mfe AS "MFE", mae AS "MAE", '
                'bull_pwr AS "Bull%/Score", pcr AS "PCR", vix AS "VIX", mode AS "Mode", '
                'adx AS "ADX", volx AS "VolX", rs_idx AS "RS vs Idx %", rank_v AS "Rank", atr_v AS "ATR", '
                'COALESCE(sector, \'\') AS "Sector", '
                'part_pnl AS "Partial P&L", ml_prob AS "ML Prob", '
                'COALESCE(sig_side, \'\') AS "Signal", '
                'COALESCE(note, \'\') AS "Special Note" '
                "FROM trade_journal "
            )
            conds, params = [], []
            if status_filter in ("OPEN", "CLOSED"):
                conds.append("status = ?")
                params.append(status_filter)
            if inst_filter in ("INDEX", "EQUITY_INTRADAY"):
                conds.append("instrument_type = ?")
                params.append(inst_filter)
            if mode_filter in ("LIVE", "DEMO"):
                conds.append("mode = ?")
                params.append(mode_filter)
            if conds:
                q += "WHERE " + " AND ".join(conds) + " "
            q += "ORDER BY id DESC LIMIT ?"
            params.append(int(limit))
            return pd.read_sql_query(q, conn, params=tuple(params))
    except Exception:
        return pd.DataFrame()


def log_pcr_hist(ic: dict, und: str) -> None:
    """Live PCR ko har ~1 min DB me save karo - taaki Backtest me PCR filter asli data se lage."""
    try:
        if demo_mode or ic.get("pcr") is None:
            return
        now = now_ist()
        k = f"_pcr_log_{und}"
        if time.time() - SNAP.get(k, 0.0) < 55:
            return
        SNAP[k] = time.time()
        with db() as conn:
            conn.execute("INSERT INTO pcr_hist (dt, tm, und, pcr, pcr_delta) VALUES (?,?,?,?,?)",
                         (now.date().isoformat(), now.strftime("%H:%M:%S"), und, float(ic["pcr"]),
                          None if ic.get("pcr_delta") is None else float(ic["pcr_delta"])))
    except Exception as e:
        try:
            ERR_LOG.append((now_ist().strftime("%H:%M:%S"), -1, "pcr-hist-log", str(e)[:120]))
        except Exception:
            pass


def audit(event: str, symbol: str = "", side: str = "", detail: str = "") -> None:
    """Compliance / audit trail: har entry, exit, halt aur risk-limit skip ka record (60 din)."""
    try:
        now = now_ist()
        with db() as conn:
            conn.execute("INSERT INTO audit_log (dt, tm, event, symbol, side, detail) VALUES (?,?,?,?,?,?)",
                         (now.date().isoformat(), now.strftime("%H:%M:%S"), str(event), str(symbol), str(side), str(detail)[:400]))
    except Exception as e:
        try:
            ERR_LOG.append((now_ist().strftime("%H:%M:%S"), -1, "audit-log", str(e)[:120]))     # chup-chaap gayab nahi - Diagnostics me dikhega
        except Exception:
            pass


def trade_event(trade_id, kind: str, price: float = 0.0, price2: float = 0.0, note: str = "") -> None:
    """Trade ki zindagi ke pal (ENTRY / SL_MOVE / PARTIAL / EXIT) - chart par mark karne ke liye."""
    if not trade_id:
        return
    try:
        now = now_ist()
        with db() as conn:
            conn.execute("INSERT INTO trade_events (trade_id, dt, tm, kind, price, price2, note) VALUES (?,?,?,?,?,?,?)",
                         (int(trade_id), now.date().isoformat(), now.strftime("%H:%M:%S"), str(kind), float(price or 0.0),
                          float(price2 or 0.0), str(note)[:200]))
    except Exception as e:
        try:
            ERR_LOG.append((now_ist().strftime("%H:%M:%S"), -1, "trade-event", str(e)[:120]))
        except Exception:
            pass


SAVE_TFS = (3, 5, 10, 15, 30, 60)          # 1m alag table (candles_1m) me; baaki candles_tf me; daily '1D' bhi candles_tf me


def resample_session(df: pd.DataFrame, minutes: int) -> pd.DataFrame:
    """NSE session (9:15) se aligned candles: 3m/5m/10m/15m/30m/60m. (60m: 9:15, 10:15 ... broker charts jaisa)"""
    if df is None or df.empty or minutes <= 1:
        return df
    return (df.set_index("ts").resample(f"{int(minutes)}min", offset="15min")
            .agg({"o": "first", "h": "max", "l": "min", "c": "last", "v": "sum"})
            .dropna(subset=["c"]).reset_index())


def tf_rows(sym: str, df1m: pd.DataFrame, recent_only: bool = False) -> list:
    """1-min candles se sabhi time frame ke rows. recent_only: sirf poori tarah dhake hue aakhri 2 buckets (incremental update)."""
    rows = []
    if df1m is None or df1m.empty:
        return rows
    first_ts = df1m["ts"].iloc[0]
    for m_ in SAVE_TFS:
        r = resample_session(df1m, m_)
        if r is None or r.empty:
            continue
        if recent_only:
            r = r[r["ts"] >= first_ts].tail(2)               # shuruaati adhura bucket mat likho
        for x in r.itertuples(index=False):
            rows.append((sym, f"{m_}m", pd.Timestamp(x.ts).tz_convert(IST).strftime("%Y-%m-%d %H:%M:%S"),
                         float(x.o), float(x.h), float(x.l), float(x.c), float(x.v)))
    return rows


def flush_candles() -> None:
    """Scan ke baad buffer ke naye candles DB me: 1-min (candles_1m) + sabhi time frame (candles_tf). Demo ke nakli candles save nahi hote."""
    buf = SNAP.get("candle_buf") or {}
    if not buf or demo_mode:
        return
    SNAP["candle_buf"] = {}
    r1, rt = [], []
    try:
        for sym, (d, full) in list(buf.items()):
            one = d if full else d.tail(6)
            for r in one.itertuples(index=False):
                r1.append((sym, pd.Timestamp(r.ts).tz_convert(IST).strftime("%Y-%m-%d %H:%M:%S"),
                           float(r.o), float(r.h), float(r.l), float(r.c), float(r.v)))
            rt += tf_rows(sym, d, recent_only=not full)
        with db() as conn:
            if r1:
                conn.executemany("INSERT OR REPLACE INTO candles_1m (sym, ts, o, h, l, c, v) VALUES (?,?,?,?,?,?,?)", r1)
            if rt:
                conn.executemany("INSERT OR REPLACE INTO candles_tf (sym, tf, ts, o, h, l, c, v) VALUES (?,?,?,?,?,?,?,?)", rt)
    except Exception as e:
        try:
            ERR_LOG.append((now_ist().strftime("%H:%M:%S"), -1, "candles-save", str(e)[:120]))
        except Exception:
            pass


def save_daily_candles(sym: str, df: pd.DataFrame) -> None:
    """Daily (1D) candles candles_tf me."""
    if df is None or df.empty or demo_mode or not sym:
        return
    try:
        rows = [(sym, "1D", pd.Timestamp(r.ts).tz_convert(IST).strftime("%Y-%m-%d 00:00:00"), float(r.o), float(r.h), float(r.l), float(r.c), float(r.v))
                for r in df[["ts", "o", "h", "l", "c", "v"]].itertuples(index=False)]
        with db() as conn:
            conn.executemany("INSERT OR REPLACE INTO candles_tf (sym, tf, ts, o, h, l, c, v) VALUES (?,?,?,?,?,?,?,?)", rows)
    except Exception:
        pass


def kv_set(k: str, obj) -> None:
    try:
        with db() as conn:
            conn.execute("INSERT OR REPLACE INTO kv (k, v) VALUES (?, ?)", (k, json.dumps(obj, default=str)))
    except Exception:
        pass


def kv_get(k: str):
    try:
        with db() as conn:
            row = conn.execute("SELECT v FROM kv WHERE k = ?", (k,)).fetchone()
        return json.loads(row[0]) if row else None
    except Exception:
        return None


def journal_today_summary(today_iso: str, inst_type: str = "INDEX") -> tuple:
    try:
        with db() as conn:
            rows = conn.execute(
                "SELECT pnl_rs, exit_reason FROM trade_journal WHERE dt = ? AND instrument_type = ? AND status = 'CLOSED'",
                (today_iso, inst_type),
            ).fetchall()
        pnl = sum(float(r[0] or 0.0) for r in rows)
        sl_cnt = sum(1 for r in rows if "SL" in str(r[1] or "").upper() and float(r[0] or 0.0) < 0)
        return pnl, sl_cnt
    except Exception:
        return 0.0, 0


init_db()
close_orphan_open_trades(datetime.now(IST).date().isoformat())


# ====== SECTION: INSTRUMENT UNIVERSE (NSE + BSE, auto F&O discovery) ======
def _fut_frame(inst, seg, today_dt):
    if inst is None or "segment" not in inst.columns:
        return pd.DataFrame()
    fo = inst[inst["segment"] == seg].copy()
    if fo.empty or "expiry" not in fo.columns or "instrument_type" not in fo.columns:
        return pd.DataFrame()
    raw = fo["expiry"]
    if pd.api.types.is_numeric_dtype(raw):
        ts = pd.to_datetime(raw, unit="ms", utc=True, errors="coerce").dt.tz_convert(IST)
    else:
        ts = pd.to_datetime(raw, errors="coerce")
    fo = fo[ts.notna()].copy()
    fo["exp_date"] = ts[ts.notna()].dt.date
    fo = fo[fo["exp_date"] >= today_dt]
    futs = fo[fo["instrument_type"] == "FUT"].copy()
    if futs.empty:
        return futs
    sym_col = "underlying_symbol" if "underlying_symbol" in futs.columns else "name"
    futs["_und"] = futs[sym_col].astype(str).str.upper().str.strip()
    if "underlying_type" in futs.columns:
        futs["_is_idx"] = futs["underlying_type"].astype(str).str.upper().str.contains("INDEX")
    else:
        futs["_is_idx"] = False
    futs["_is_idx"] = futs["_is_idx"] | futs["_und"].isin(list(INDEX_CATALOG.keys()))
    return futs


def _pick_row(sf, today_dt):
    if sf is None or sf.empty:
        return None
    sf = sf.sort_values("exp_date")
    row = sf.iloc[0]
    if (row["exp_date"] - today_dt).days <= ROLL_DAYS and len(sf) > 1:
        row = sf.iloc[1]
    return row


def _eq_map(df, seg):
    if df is None or df.empty:
        return {}
    sym_candidates = ("trading_symbol", "tradingsymbol", "symbol", "underlying_symbol", "short_name", "name")
    tc = next((c for c in sym_candidates if c in df.columns), None)
    ik_col = next((c for c in ("instrument_key", "instrument_token", "token") if c in df.columns), None)
    if not tc or not ik_col:
        return {}
    if "segment" in df.columns:
        eq_df = df[df["segment"].astype(str).str.upper() == seg.upper()]
    else:
        eq_df = df[df[ik_col].astype(str).str.startswith(seg)]
    if "instrument_type" in eq_df.columns:
        sub = eq_df[eq_df["instrument_type"].astype(str).str.upper().isin(("EQ", "EQUITY", "A", "B"))]
        if not sub.empty:
            eq_df = sub
    out = {}
    for c_name in sym_candidates:
        if c_name in eq_df.columns:
            for k_sym, v_ik in zip(eq_df[c_name].astype(str).str.upper().str.strip(), eq_df[ik_col].astype(str).str.strip()):
                if k_sym and k_sym != "NAN" and v_ik and k_sym not in out:
                    out[k_sym] = v_ik
    return out


@st.cache_data(ttl=43200, show_spinner="NSE + BSE Instruments map load ho raha hai...")
def load_instrument_bundle(symbols: tuple, day_key: str, discover: str = "") -> dict:
    """discover: "" = diye gaye symbols | "NSE" = sabhi NSE F&O stocks | "NSE+BSE" = NSE + BSE F&O stocks."""
    today_dt = datetime.now(IST).date()
    inst = pd.read_json(INSTRUMENT_URL)
    nse_futs = _fut_frame(inst, "NSE_FO", today_dt)
    bse_inst, bse_futs = pd.DataFrame(), pd.DataFrame()
    try:
        bse_inst = pd.read_json(BSE_INSTRUMENT_URL)
        bse_futs = _fut_frame(bse_inst, "BSE_FO", today_dt)
    except Exception:
        pass

    syms = list(symbols)
    if discover and not nse_futs.empty:
        syms = sorted(nse_futs[~nse_futs["_is_idx"]]["_und"].unique())
    exch = {s: "NSE" for s in syms}
    if discover == "NSE+BSE" and not bse_futs.empty:
        extra = sorted(set(bse_futs[~bse_futs["_is_idx"]]["_und"].unique()) - set(syms))
        for s in extra:
            exch[s] = "BSE"
        syms = syms + extra

    nse_eq, bse_eq = _eq_map(inst, "NSE_EQ"), _eq_map(bse_inst, "BSE_EQ")
    out = {"eq": {}, "fut": {}, "lot_map": {}, "idx": {}, "syms": syms, "exch": exch}
    for s in syms:
        k = (nse_eq if exch.get(s) == "NSE" else bse_eq).get(s)
        if k:
            out["eq"][s] = k
        fr = nse_futs if exch.get(s) == "NSE" else bse_futs
        if not fr.empty:
            row = _pick_row(fr[fr["_und"] == s], today_dt)
            if row is not None:
                out["fut"][s] = row["instrument_key"]
                if "lot_size" in row.index and pd.notna(row["lot_size"]):
                    out["lot_map"][s] = int(row["lot_size"])
    if discover:
        out["syms"] = [s for s in syms if s in out["eq"]]
    for und, meta in INDEX_CATALOG.items():
        fr = nse_futs if meta["exch"] == "NSE" else bse_futs
        if fr.empty:
            continue
        row = _pick_row(fr[fr["_und"] == und], today_dt)
        if row is not None:
            lot = int(row["lot_size"]) if "lot_size" in row.index and pd.notna(row["lot_size"]) else FALLBACK_LOTS.get(und, 1)
            out["idx"][und] = (row["instrument_key"], lot)
    return out


# ====== SECTION: 24x7 BACKGROUND AGENT (headless - browser/phone band hone par bhi chalta hai) ======
# Idea: ek daemon thread Streamlit ke AppTest se isi poori script ko bina browser ke baar-baar chalata hai.
# Isse scanner + signal engine + paper trades + DB + Google Sheet sync sab server par chalte rahte hain.
# - Browser khula/active ho to bg thread ruk jata hai (duplicate trade nahi banega).
# - Sidebar ki settings browser se copy hoti hain (jo aakhri baar app kholkar rakhi thi).
# - LIVE (asli paise) orders background me HAMESHA band rehte hain. Sirf paper trades + data.
import traceback as _tb

_IS_BG = bool(st.session_state.get("_is_bg", False))
_SELF_PATH = os.path.abspath(__file__)
BG_FORCE = {
    "LIVE trading ON (asli paise, asli orders)": False,
    "Enable Auto-Refresh": False,
}
BG_START, BG_END = dtime(9, 10), dtime(15, 55)   # IST; EOD square-off, sheet sync, ML train aur daily PCR snapshot ke liye 15:55 tak


def _bg_window(dt=None) -> bool:
    dt = dt or now_ist()
    if dt.weekday() >= 5 or dt.date() in NSE_HOLIDAYS:
        return False
    return BG_START <= dt.time() <= BG_END


@st.cache_resource
def _bg_agent(path: str) -> dict:
    store = {
        "enabled": True, "status": "starting", "cycles": 0, "last_tick": None, "last_dur": None,
        "last_error": None, "ui_last": 0.0, "has_token": False, "cfg": {}, "secrets": {},
        "run_lock": threading.Lock(), "wake": threading.Event(),
    }

    def loop():
        at = None
        while True:
            wait = 30.0
            try:
                wait = float(max(10, int(store["cfg"].get("Auto refresh (sec)", 30))))
                grace = max(90.0, 3 * wait)
                if not store["enabled"]:
                    store["status"] = "PAUSED"
                    wait = 5.0
                elif not _bg_window():
                    store["status"] = "IDLE (market closed)"
                    wait = 60.0
                elif not store["has_token"]:
                    store["status"] = "WAITING (token nahi / app ek baar kholo)"
                    wait = 30.0
                elif time.time() - store["ui_last"] < grace:
                    store["status"] = "BROWSER ACTIVE (bg ruka hai)"
                    wait = 10.0
                else:
                    store["status"] = "RUNNING"
                    if at is None:
                        from streamlit.testing.v1 import AppTest
                        at = AppTest.from_file(path, default_timeout=180)
                        at.session_state["_is_bg"] = True
                        for k, v in store["secrets"].items():
                            at.secrets[k] = v
                    t0 = time.time()
                    with store["run_lock"]:
                        at.run(timeout=180)
                    dur = time.time() - t0
                    errs = [str(e.value) for e in at.exception]
                    errs += [str(e.value) for e in at.error if "401" in str(e.value) or "Unauthorized" in str(e.value)]
                    store["cycles"] += 1
                    store["last_tick"] = now_ist()
                    store["last_dur"] = round(dur, 1)
                    store["last_error"] = errs[0][:800] if errs else None
                    wait = max(5.0, wait - dur)
            except Exception:
                store["last_error"] = _tb.format_exc(limit=4)
                at = None
                wait = 30.0
            store["wake"].wait(timeout=wait)
            store["wake"].clear()

    threading.Thread(target=loop, daemon=True, name="bg-agent").start()
    return store


BGS = _bg_agent(_SELF_PATH)
if not _IS_BG:
    BGS["ui_last"] = time.time()
    if BGS["run_lock"].acquire(timeout=120):      # bg cycle chal raha ho to uske khatam hone tak ruko
        BGS["run_lock"].release()
    BGS["ui_last"] = time.time()
    if not BGS["secrets"]:
        try:
            BGS["secrets"] = json.loads(json.dumps(dict(st.secrets), default=lambda o: dict(o)))
        except Exception:
            pass


# ---- v5.9: Default Setting (v7.8: Strict Filter hata diya) ----
_FORCE_SECTIONS = (
    "Index (Signal Engine)", "⚙ Signal & MTF Rules", "🛡 Risk & Trade Plan", "🎯 Win-Rate Filters (v5.3)",
    "🗓 Result Lock Rule", "📉 Volatility Filters", "🟠 15m Consolidation (No-Trade Zone)",
    "🟠 Choppy Market = NO TRADE ZONE", "📊 Stock PCR (sirf jaankari - filter nahi, v7.7)", "↩ Pullback Entry (v7.6)",
)
_FORCE_EXTRA_LABELS = ("OI / buildup comparison window (min)", "Stock futures OI change threshold (%)",
                       "Price change threshold for buildup (%)")


class _SbProxy:
    """st.sidebar wrapper: browser me widget values yaad rakhta hai, background run me wahi values wapas deta hai.
    v5.9: 'Default Setting' ON ho to strategy settings code ke default par lock. (v7.8: 'Strict Filter' hata diya.)"""
    _REC = ("checkbox", "selectbox", "slider", "number_input", "radio", "text_input", "time_input")

    def __init__(self, real, cfg: dict, is_bg: bool):
        self._real, self._cfg, self._bg = real, cfg, is_bg
        self._sec, self._defaults, self._locked = "", False, 0
        self._edit, self._rst = False, 0

    def set_mode(self, defaults_on: bool, edit_on: bool = False, rst: int = 0) -> None:
        self._defaults, self._locked = bool(defaults_on), 0
        self._edit, self._rst = bool(edit_on), int(rst)

    @staticmethod
    def _default_of(name, a, k):
        if name == "checkbox":
            return bool(k.get("value", a[0] if a else False))
        if name == "slider":
            return k.get("value", a[2] if len(a) > 2 else (a[0] if a else k.get("min_value", 0)))
        if name == "number_input":
            return k.get("value", a[2] if len(a) > 2 else k.get("min_value", a[0] if a else 0))
        if name in ("selectbox", "radio"):
            opts = list(a[0] if a else k["options"])
            idx = k.get("index", a[1] if len(a) > 1 else 0)
            return opts[idx] if idx is not None else None
        if name == "time_input":
            return k.get("value", a[0] if a else None)
        return None

    def __getattr__(self, name):
        attr = getattr(self._real, name)
        if name == "header" and callable(attr):
            def _h(title, *a, **k):
                self._sec = title
                return attr(title, *a, **k)
            return _h
        if name == "button" and self._bg:
            return lambda *a, **k: False
        if name not in self._REC or not callable(attr):
            return attr

        def wrapper(label, *a, **k):
            if self._bg and label in BG_FORCE:
                return BG_FORCE[label]
            if self._bg and label in self._cfg:
                return self._cfg[label]
            forced = None
            if not self._bg and name != "text_input" and (self._sec in _FORCE_SECTIONS or label in _FORCE_EXTRA_LABELS):
                try:
                    if self._defaults:
                        forced = self._default_of(name, a, k)
                except Exception:
                    forced = None
            if forced is not None and self._edit:
                # Manual adjust ON: widget editable; shuruaati value = default
                k2 = {kk: vv for kk, vv in k.items() if kk not in ("key", "disabled", "value")}
                k2["key"] = f"ed::{label}::{self._rst}"
                if name == "checkbox":
                    val = attr(label, value=bool(forced), **k2)
                else:
                    if "value" in k:
                        k2["value"] = k["value"]
                    val = attr(label, *a, **k2)
                self._cfg[label] = val
                return val
            if forced is not None:
                k2 = {kk: vv for kk, vv in k.items() if kk not in ("key", "disabled", "value")}
                k2["disabled"] = True
                k2["key"] = f"lk::{label}::{forced}"
                if name == "checkbox":
                    attr(label, value=bool(forced), **k2)
                else:
                    if "value" in k:
                        k2["value"] = k["value"]
                    attr(label, *a, **k2)
                self._locked += 1
                self._cfg[label] = forced
                return forced
            val = attr(label, *a, **k)
            if not self._bg:
                self._cfg[label] = val
            return val
        return wrapper


# ====== SECTION: SIDEBAR ======
sb = _SbProxy(st.sidebar, BGS["cfg"], _IS_BG)
sb.header("🔐 Connection")
manual_token = sb.text_input("Upstox Token (optional override)", type="password")
TOKEN = (
    (manual_token or "").strip()
    or secret("UPSTOX_TOKEN")
    or secret("UPSTOX_ACCESS_TOKEN")
    or secret("UPSTOX_API_TOKEN")
)
TG_TOKEN = secret("TELEGRAM_TOKEN")
TG_CHAT = secret("TELEGRAM_CHAT_ID")
if DB_ERR:
    sb.warning(f"Database error: {DB_ERR}")

sb.header("🎛 Filter Mode")
_ud0 = kv_get("ui_use_defaults")
_ud0 = True if _ud0 is None else bool(_ud0)
_ed0 = bool(kv_get("ui_edit_on"))
use_defaults = sb.checkbox("✅ Default Setting (permanent ON)", value=_ud0,
                           help="ON = strategy ki saari settings (score, filters, SL/target, limits, positions...) code ke default par lock. "
                                "Ye yaad rakhta hai - app band/khol karne par bhi ON rehta hai. Manual badalna ho to OFF karo.")
edit_on = sb.checkbox("✏ Manual adjust (Default ke saath bhi settings badlo)", value=_ed0,
                      help="ON = Default ON hone par bhi neeche ki settings khud badal sakte ho (shuruaati value default hogi). "
                           "OFF = settings lock. 'Reset' dabane par sab wapas default.")
if not _IS_BG:
    if sb.button("🔄 Sab settings default par wapas (reset)", key="ed_reset_btn"):
        st.session_state["ed_reset"] = int(st.session_state.get("ed_reset", 0)) + 1
    if edit_on != _ed0:
        kv_set("ui_edit_on", bool(edit_on))
    if use_defaults != _ud0:
        kv_set("ui_use_defaults", bool(use_defaults))
sb.set_mode(bool(use_defaults), bool(edit_on), int(st.session_state.get("ed_reset", 0)))
_mode_ph = sb.empty()

# ---- Capital aur quantity: Default / Manual dono me HAMESHA badal sakte ho (ye lock nahi hote)
QTY_BASIS_OPTS = ["Stock ke lot size ke hisab se (1 lot)", "Capital ke hisab se (shares)"]
_cap0 = kv_get("ui_capital")
_cap0 = int(_cap0) if _cap0 else 0
_lev0 = kv_get("ui_leverage")
_lev0 = float(_lev0) if _lev0 else 1.0
_qb0 = kv_get("ui_qty_basis")
_qb0 = _qb0 if _qb0 in QTY_BASIS_OPTS else QTY_BASIS_OPTS[0]
sb.markdown("**💰 Capital aur Quantity** (Default / Manual - dono me aap badal sakte ho)")
capital_rs = sb.number_input("💰 Capital Rs (0 = capital-based quantity aur capital limits band)", value=_cap0, min_value=0, step=50000,
                             help="Apni trading capital yahan daalo. 'Capital ke hisab se' chunne par har trade ka quantity isi se tay hota hai. "
                                  "Capital > 0 hone par 'gross exposure' aur 'ek position ka max notional' limits bhi lagti hain (Risk section).")
capital_lev = sb.number_input("Leverage (x) - intraday margin ka multiple (1 = sirf apni capital)", value=_lev0, min_value=1.0, max_value=20.0, step=0.5,
                              help="Sirf 'Capital ke hisab se' quantity me kaam aata hai. Broker ka margin multiple yahan daal sakte ho (jaise 5).")
qty_basis = sb.selectbox("Quantity kis hisab se", QTY_BASIS_OPTS, index=QTY_BASIS_OPTS.index(_qb0),
                         help="Lot size: har trade me us stock ka 1 F&O lot (shares). Capital: capital x leverage / max khule positions ko stock ke price se bhaag dekar shares.")
if not _IS_BG:
    if int(capital_rs) != _cap0:
        kv_set("ui_capital", int(capital_rs))
    if float(capital_lev) != _lev0:
        kv_set("ui_leverage", float(capital_lev))
    if qty_basis != _qb0:
        kv_set("ui_qty_basis", qty_basis)
use_cap_qty = bool(str(qty_basis).startswith("Capital") and float(capital_rs) > 0)
if str(qty_basis).startswith("Capital") and float(capital_rs) <= 0:
    sb.caption("⚠ Capital 0 hai - abhi lot size ke hisab se quantity chal rahi hai. Upar capital daalo.")


def cap_alloc() -> float:
    """Capital ke hisab se ek trade ko milne wala hissa = capital x leverage / max khule positions."""
    return float(capital_rs) * float(capital_lev) / max(1, int(max_open_pos))


def cap_qty(ltp: float) -> int:
    """Capital wale hisse me kitne shares aa sakte hain (0 = ek bhi nahi)."""
    return int(cap_alloc() // ltp) if ltp and ltp > 0 else 0

sb.header("📊 Universe Selection")
universe_mode = sb.radio(
    "Select F&O Stock Universe",
    [
        "Nifty 50 (All 50 F&O Shares)",
        "Bank Nifty (12 Shares)",
        "Combined (All Nifty + BankNifty F&O)",
        "All NSE F&O Stocks (auto)",
        "All NSE + BSE F&O Stocks (auto)",
    ],
    index=4,          # v7.5: default = All NSE + BSE F&O (sab stocks ka data/PCR baseline ek jaisa jama ho)
)

if universe_mode == "Bank Nifty (12 Shares)":
    ACTIVE_DEFAULT_WEIGHTS = BANKNIFTY_WEIGHTS
    PRIMARY_INDEX_KEY, PRIMARY_INDEX_NAME, IDX_UND = BNF_INDEX_KEY, "NIFTY BANK", "BANKNIFTY"
elif universe_mode == "Nifty 50 (All 50 F&O Shares)":
    ACTIVE_DEFAULT_WEIGHTS = NIFTY50_FO_WEIGHTS
    PRIMARY_INDEX_KEY, PRIMARY_INDEX_NAME, IDX_UND = NIFTY_KEY, "NIFTY 50", "NIFTY"
else:
    combined = dict(NIFTY50_FO_WEIGHTS)
    for k, v in BANKNIFTY_WEIGHTS.items():
        if k not in combined:
            combined[k] = round(v * 0.25, 2)
    ACTIVE_DEFAULT_WEIGHTS = combined
    PRIMARY_INDEX_KEY, PRIMARY_INDEX_NAME, IDX_UND = NIFTY_KEY, "NIFTY 50", "NIFTY"

DISCOVER = {"All NSE F&O Stocks (auto)": "NSE", "All NSE + BSE F&O Stocks (auto)": "NSE+BSE"}.get(universe_mode, "")
PRE_BUNDLE = None
if DISCOVER:
    try:
        PRE_BUNDLE = load_instrument_bundle((), now_ist().date().isoformat(), DISCOVER)
        ACTIVE_DEFAULT_WEIGHTS = {s: ACTIVE_DEFAULT_WEIGHTS.get(s, 0.5) for s in PRE_BUNDLE["syms"]}
        sb.caption(f"Auto universe: {len(PRE_BUNDLE['syms'])} stocks")
    except Exception as e:
        sb.error(f"Auto universe load fail ({e}) - Combined list use ho rahi hai")
        DISCOVER, PRE_BUNDLE = "", None
SYMBOLS = list(ACTIVE_DEFAULT_WEIGHTS.keys())

sb.header("Index (Signal Engine)")
_idx_opts = list(INDEX_CATALOG)
IDX_UND = sb.selectbox(
    "Signal engine index",
    _idx_opts,
    index=_idx_opts.index(IDX_UND) if IDX_UND in _idx_opts else 0,
    format_func=lambda u: INDEX_CATALOG[u]["name"],
)
PRIMARY_INDEX_KEY, PRIMARY_INDEX_NAME = INDEX_CATALOG[IDX_UND]["key"], INDEX_CATALOG[IDX_UND]["name"]
scan_all_idx = sb.checkbox(
    "Scan ALL indices (All Indices tab)",
    value=True,
    help="Har index ke liye alag API calls lagte hain. Rate limit issue ho to off karo.",
)

sb.header("⚙ Signal & MTF Rules")
enter_th = sb.slider("Entry power threshold (%)", 50, 85, 60)
exit_th = min(sb.slider("Exit threshold (hysteresis) (%)", 30, 75, 50), enter_th - 1)
min_net = sb.slider("Stock bias strength (min net score, max 8)", 2, 7, 4)
stk_min_score = sb.slider("Stock ENTRY ke liye min score (7+ = v7.9.3 default)", 4, 8, 7)
stk_confirm_n = sb.slider("Stock signal confirm cycles (jhoothe signal kam)", 1, 5, 1,
                          help="v7.8.3 default 1 (pehle 2, usse pehle 3). Signal lagataar itne refresh cycle bana rahe tab entry. "
                               "Filter Analysis tab ke '🔁 Confirm cycles' report me dekho kitne cycle par kitne signal/trade pass ho rahe hain.")
confirm_n = sb.slider("Signal confirm cycles", 1, 5, 1)          # v7.8.3: default 1
require_idx = sb.checkbox("Index 5m trend confirmation", value=True)
filter_basis = sb.selectbox("Filters ka aadhar (stock entry ke liye)", ["Stock par (har filter stock ka apna)", "Index par (purana)"], index=0,
                            help="Stock par: 'Index 5m trend confirmation' = us stock ka apna 5m trend; 'RS vs Index' = stock apne sector ke peers se behtar/kamzor; "
                                 "'Choppy market' = us stock ka apna VWAP whipsaw / kamzor ADX. Index par = purana tareeka (Nifty/BankNifty ka haal).")
basis_stock = str(filter_basis).startswith("Stock")
require_mtf = sb.checkbox("15m Multi-Timeframe confirmation", value=True)
require_orb = sb.checkbox("Opening Range Breakout confirmation", value=False)
require_pcr = False          # v7.7: PCR filter hataya
require_fut = sb.checkbox("Futures OI buildup confirmation", value=False)
exclude_result_wk = sb.checkbox("Auto-Block Result Week Stocks from Signal Power", value=True)
adx_min = sb.slider("Min ADX(5m) for entry (0 = off)", 0, 35, 20)
min_cov = sb.slider("Min data coverage (weight %)", 60, 100, 75)

sb.header("🛡 Risk & Trade Plan")
sl_atr_mult = sb.number_input("SL = ATR(5m) x", value=1.5, min_value=0.5, max_value=4.0, step=0.1)
rr_mult = sb.number_input("Target (Risk:Reward)", value=2.0, min_value=1.0, max_value=5.0, step=0.25)
SL_MODES = ["ATR(5m) x upar wala (purana, tight)", "15m zone ke bahar (zone low/high se aage)", "ATR(15m) x"]
sl_mode = sb.selectbox("SL mode (v7.6)", SL_MODES, index=1,
                       help="ATR(5m): SL = entry -/+ 1.5 x ATR(5m) - sabse tight, noise me jaldi lagta hai. "
                            "15m zone: LONG ka SL 15m zone ke LOW ke neeche, SHORT ka HIGH ke upar (buffer = ATR15 x niche wala). "
                            "ATR(15m): SL = entry -/+ ATR(15m) x niche wala. Zone/ATR15 data na ho to ATR(5m) wala.")
sl_atr15_mult = sb.number_input("SL mode ATR(15m): ATR(15m) x", value=1.0, min_value=0.3, max_value=3.0, step=0.1)
sl_zone_buf = sb.number_input("SL mode 15m zone: zone ke bahar buffer (ATR15 x)", value=0.25, min_value=0.0, max_value=1.5, step=0.05)
sl_min_atr5 = sb.number_input("SL kam se kam itna door (ATR(5m) x) - bahut tight SL rokne ke liye", value=1.0, min_value=0.3, max_value=3.0, step=0.1)
sl_max_atr15 = sb.number_input("SL zyada se zyada itna door (ATR(15m) x) - isse door ho to yahin tak", value=2.5, min_value=0.5, max_value=5.0, step=0.25)
use_trail = sb.checkbox("Breakeven + ATR trailing SL", value=True)
risk_per_trade = sb.number_input("Risk per trade (Rs) - sirf 'ATR risk sizing' ON hone par use hota hai", value=2000, min_value=200, step=200)
index_trading_on = sb.checkbox(
    "Index trading (paper) ON",
    value=False,
    help="OFF = Index me naya trade nahi khulega (sirf signals/analysis dikhenge). Stock F&O trades alag chalte rahenge.",
)
idx_lots = sb.number_input("Index paper-trade lots", value=1, min_value=1, max_value=50)
max_sl_day = sb.slider("Max SL hits per day (index engine)", 1, 5, 2)
daily_loss_limit = sb.number_input("Daily loss limit (Rs, index engine)", value=5000, min_value=500, step=500)
stk_loss_limit = sb.number_input("Daily loss limit (Rs, STOCK paper trades)", value=10000, min_value=1000, step=1000,
                                 help="Is se zyada loss hone par aaj naye stock paper trades band.")
stk_max_sl_day = sb.slider("Max SL hits per day (STOCK trades) - itne SL par aaj ka stock trading band", 1, 8, 3,
                           help="v7.8: pehle index engine wala 'Max SL hits' (2) hi stocks par bhi lagta tha. "
                                "Ab stocks ke liye alag. Daily loss limit aur lagataar-loss limit ab bhi lagu hain.")
max_stk_trades_day = sb.slider("Max stock trades / din (paper + live)", 1, 60, 15)
max_consec_losses = sb.slider("Lagataar itne loss ke baad aaj ke naye trade band", 2, 8, 3)
stk_profit_lock = sb.number_input("💰 Din ka profit target Rs (is par naye trade band, 0 = off)", value=15000, min_value=0, step=1000,
                                  help="Target pura hone par naye trade nahi; khule trade apne SL/target tak chalte hain.")
giveback_pct = sb.slider("💰 Peak profit se itna % wapas gaya to naye trade band", 20, 80, 40)
giveback_min_peak = sb.number_input("💰 Giveback tabhi dekho jab peak profit Rs", value=5000, min_value=500, step=500)
max_open_pos = sb.slider("Max ek saath khule stock positions", 1, 20, 15,
                         help="Ek saath bahut saare same-direction trade = ek saath SL. Isse loss ka dhamaka kam hota hai.")
max_new_per_min = sb.slider("Ek minute me max naye stock entry", 1, 20, 2)
max_same_dir = sb.slider("Ek hi direction (LONG ya SHORT) me max khule positions", 1, 20, 5,
                         help="Sab trade ek taraf hon to ek saath SL lagta hai. Isse wo jokhim kam hota hai.")
max_per_sector = sb.slider("Ek sector me max khule positions (jaise 2 bank stocks)", 1, 20, 2)
sec_group_mode = sb.selectbox("Sector guard ka aadhar (v7.9)",
                              ["Bada group (Bank+NBFC+PSU Fin+Insurance+Cap Mkt = FINANCIALS)", "Sirf apna sector (purana)"], index=0,
                              help="03-Nov: SBIN, HDFCBANK, UNIONBANK, BANKINDIA, MANAPPURAM, 360ONE alag sector the par ek saath chale. "
                                   "Bada group me ye sab ek gine jaate hain - max limit upar wala slider.")
sec_no_hedge = sb.checkbox("Same sector/group me ek saath LONG + SHORT block (v7.9)", value=True,
                           help="Jaise SBIN LONG khula ho to UNIONBANK SHORT nahi. Ek sector me ulti bet = noise par dono taraf SL.")
idx_dir_gate = sb.checkbox("🧭 Entry se pehle INDEX direction match zaroori (v7.9)", value=True,
                           help="Stock ka signal kitna bhi strong ho, index ulta chal raha ho to entry nahi.")
idx_dir_ref = sb.selectbox("Index direction: kaun sa index",
                           ["Stock ke hisaab se (Bank/Finance = BANK NIFTY, baaki = NIFTY)", "Dono (NIFTY + BANK NIFTY) match",
                            "Sirf NIFTY"], index=0)
idx_dir_strict = sb.checkbox("Index 5m trend flat ho to bhi entry nahi (sirf usi disha me ho to)", value=True,
                             help="ON = index ka 5m trend trade ki disha me hona chahiye. OFF = sirf ulta ho tab roko (flat par entry chalegi). "
                                  "Dono me index ka 15m trend ulta ho to entry nahi.")
burst_n = sb.slider("🧊 Burst guard: itni entry ke baad cooldown (0 = off) (v7.9)", 0, 20, 3)
burst_win = sb.slider("🧊 Burst guard: kitne min ki khidki me", 5, 30, 10)
burst_cd = sb.slider("🧊 Burst guard: cooldown kitne min", 5, 60, 15)
HALT_MODES = ["Profit wale chalne do (SL >= entry, trail par), loss wale band", "Sab khule trade apne SL/trail par chalne do",
              "Sab turant band (purana)"]
halt_mode = sb.selectbox("MAX SL HALT par khule trade (v7.9)", HALT_MODES, index=0,
                         help="Halt hamesha NAYE trade rokta hai. KILL SWITCH aur MAX LOSS par sab band hota hai (ye setting lagu nahi).")
reverse_on = sb.checkbox("🔄 REVERSE MODE: STRONG BUY par SHORT, STRONG SELL par LONG (v7.9.1)", value=True,
                         help="Signal ke saare filter waise hi; entry ke pal disha ulti. 03-Nov ke 7 trade me ulta 5 jeet-ta - "
                              "par ye ek din ka data hai. Day Report ka 'Signal-side Net' column dono hisaab dikhata hai.")
rev_idx_mode = sb.selectbox("Reverse mode: index gate kis disha par", ["Asli trade ki disha (ulti position index ke saath)",
                                                                      "Signal ki disha (purana filter)", "Index gate off"], index=0)
rev_no_pb = sb.checkbox("Reverse mode me pullback ka wait nahi (STRONG par turant ulti entry)", value=True)
rev_live = sb.checkbox("Reverse mode LIVE (asli) orders me bhi", value=False,
                       help="OFF = reverse trade sirf paper me; LIVE ON ho tab bhi asli order nahi jayega. Pehle paper me 30+ trade dekho.")
tick_sl_on = sb.checkbox("⚡ SL/target har TICK par check (WebSocket, REST 1s fallback) (v7.9)", value=True,
                         help="Upstox V3 market feed. 'pip install upstox-python-sdk' na ho to har 1 sec REST LTP. Demo mode me band.")
corr_guard_on = sb.checkbox("Correlation guard: naya stock khule trades se zyada correlated ho to skip", value=True,
                            help="Pichhle ~60 min ke 1-min returns ka correlation. Alag sector ke stocks bhi ek saath girte hain - isse 'ek jhatke me kai SL' kam hota hai.")
corr_max = sb.number_input("Correlation guard: max effective correlation", value=0.75, min_value=0.3, max_value=0.99, step=0.05,
                           help="Effective = correlation x (same side ho to +1, ulti side ho to -1). Isse upar ho to naya trade nahi.")
corr_window = sb.slider("Correlation guard: pichhle kitne min ke returns", 30, 120, 60)
corr_min_pts = sb.slider("Correlation guard: kam se kam kitne common 1-min points", 10, 60, 20,
                         help="Isse kam data ho to guard ye check nahi lagata (trade allowed).")
spread_guard_on = sb.checkbox("Bid-ask spread guard: spread zyada ho to entry nahi", value=True,
                              help="Quote ki depth ka best bid/ask. Depth na mile (jaise demo) to ye check nahi lagta.")
max_spread_pct = sb.number_input("Max bid-ask spread (% of LTP)", value=0.15, min_value=0.02, max_value=2.0, step=0.01)
max_open_risk = sb.number_input("Sab khule trades ka total risk Rs (SL tak) - isse zyada par naya entry nahi (0 = off)",
                                value=25000, min_value=0, step=5000)
max_gross_x = sb.number_input("Max gross exposure (capital ka x)", value=5.0, min_value=0.5, max_value=20.0, step=0.5)
max_pos_pct = sb.number_input("Ek position ka max notional (capital ka %)", value=40.0, min_value=1.0, max_value=300.0, step=5.0)
risk_sizing = sb.checkbox("ATR risk sizing: lots = Risk per trade / 1-lot SL risk", value=False,
                          help="OFF = hamesha 1 lot. ON = SL chhota ho to zyada lots, bada ho to 1 lot (max lots niche).")
max_lots_stk = sb.slider("Risk sizing me max lots", 1, 5, 2)
time_stop_min = sb.slider("Time-stop: itne min baad bhi profit < 0.3R ho to exit (0 = off)", 0, 240, 120, step=15)
partial_on = sb.checkbox("Partial profit ON (R x par aadha nikalo, baaki ka SL entry par)", value=False,
                         help="Backtest tab me ON/OFF compare karke hi chalu karo.")
partial_r = sb.number_input("Partial profit tab jab profit = R x", value=1.0, min_value=0.5, max_value=3.0, step=0.1)
partial_pct = sb.slider("Partial me kitna % qty band karo", 25, 75, 50, step=5)
partial_live = sb.checkbox("Partial exit LIVE orders me bhi bhejo (LIVE ON ho tab)", value=False,
                           help="OFF = partial sirf paper trade me. Live me pehle chhote size par test karo.")
ml_min_prob = sb.slider("ML filter: jeetne ki sambhavna kam se kam (0 = off)", 0.0, 0.8, 0.0, step=0.05,
                        help="Model tabhi use hota hai jab 100+ band trades par train ho aur test AUC >= 0.55 ho. Warna ignore.")
ml_auto = sb.checkbox("ML auto-train roz (market band hone ke baad; sirf model banata hai)", value=True,
                      help="Roz 15:35 ke baad aaj tak ke band trades se model dobara train hota hai. Ye trade tab hi rokta hai jab upar ML filter > 0 ho.")
ml_use_bt = sb.checkbox("ML training me Backtest ke trades bhi jodo (simulated data)", value=False,
                        help="Zyada trades milte hain par fill/slippage simulated hota hai. Default OFF.")
vix_max = sb.number_input("Block entries if India VIX >", value=22.0, min_value=10.0, max_value=60.0, step=0.5)
entry_start = sb.time_input("Entry window start (v7.9.3 default 9:30)", value=dtime(9, 30))
entry_end = sb.time_input("Entry window end", value=dtime(14, 45))
eod_exit = sb.time_input("EOD square-off time", value=dtime(15, 15))
wall_filter = sb.checkbox("OI wall proximity filter (index)", value=True)
ext_atr = sb.number_input("Chase filter LONG: VWAP se max doori (ATR x)", value=3.5, min_value=1.0, max_value=6.0, step=0.25,
                          help="v7.5: LONG ke liye 3.5 (trend day me achhe LONG 2.5 par ruk rahe the).")
ext_atr_s = sb.number_input("Chase filter SHORT: VWAP se max doori (ATR x)", value=2.5, min_value=1.0, max_value=6.0, step=0.25,
                            help="v7.5: SHORT ke liye alag. 2.5 par SHORT block karna 02-Nov ko sahi raha.")

sb.header("↩ Pullback Entry (v7.6)")
pb_on = sb.checkbox("Pullback entry ON (LONG + SHORT dono): garam signal par chase nahi, wapsi par entry", value=True,
                    help="STRONG signal par RSI zyada garam ya volume kamzor ho, ya signal EXTENDED ho, to turant entry nahi - "
                         "price VWAP / 15m zone tak wapas aaye tab entry. LONG me neeche aane ka, SHORT me upar aane ka intezaar.")
pb_ext = sb.checkbox("EXTENDED (🟡 BUY / 🟡 SELL) signals ko bhi pullback order banao", value=True)
pb_rsi = sb.slider("Pullback: LONG me RSI >= itna (SHORT me <= 100 - itna) ho to wapsi ka intezaar", 55, 85, 70)
pb_vol = sb.number_input("Pullback: volume spike isse kam ho to wapsi ka intezaar", value=1.1, min_value=1.0, max_value=3.0, step=0.05)
PB_LEVELS = ["VWAP ya 15m zone - jo price ke paas ho", "Sirf VWAP", "Sirf 15m zone (LONG: zone high, SHORT: zone low)", "ATR(15m) wapsi"]
pb_level_mode = sb.selectbox("Pullback entry level", PB_LEVELS, index=0)
pb_atr = sb.number_input("Pullback level 'ATR(15m) wapsi': kitna ATR(15m) wapas", value=0.5, min_value=0.2, max_value=2.0, step=0.1)
pb_valid_min = sb.slider("Pullback order kitne min tak valid", 10, 120, 45, step=5)
pb_inval_atr = sb.number_input("Pullback cancel: level se itna (ATR15 x) aage nikal jaye to order radd", value=1.0, min_value=0.3, max_value=3.0, step=0.1,
                               help="LONG: price level - ATR15 x itna se neeche gaya = trend toota, order cancel. SHORT me ulta.")

sb.header("🎯 Win-Rate Filters (v5.3)")
f_wall = sb.checkbox("F1: Day/Prev High-Low wall filter", value=True,
                     help="LONG block agar upar Day High / Kal ka High ATR x se kam door ho (breakout block nahi). SHORT ke liye Low.")
f_wall_atr = sb.number_input("F1: wall distance (ATR x)", value=1.0, min_value=0.25, max_value=3.0, step=0.25)
f_wick = sb.checkbox("F2: Signal candle wick rejection filter", value=True,
                     help="Aakhri closed 5m candle ka close LONG ke liye upari hisse me, SHORT ke liye nichle hisse me hona chahiye.")
f_wick_long = sb.number_input("F2: LONG ke liye close position >=", value=0.60, min_value=0.30, max_value=0.90, step=0.05)
f_wick_short = sb.number_input("F2: SHORT ke liye close position <=", value=0.40, min_value=0.10, max_value=0.70, step=0.05)
f_rs = sb.checkbox("F3: RS vs Index mandatory", value=True,
                   help="LONG ke liye stock Index se kam se kam barabar; SHORT ke liye Index se kamzor.")
f_rs_min = sb.number_input("F3: RS tolerance (%)", value=0.0, min_value=0.0, max_value=0.5, step=0.05,
                           help="0.0 = strict. 0.15 = thoda dheela (LONG RS >= -0.15)")
f_vol = sb.checkbox("F4: Volume spike mandatory", value=True)
f_vol_min = sb.number_input("F4: Min Vol Spike x", value=1.1, min_value=1.0, max_value=3.0, step=0.1)
f_minatr = sb.checkbox("F5: Min ATR % (dead candle) filter", value=True)
f_minatr_pct = sb.number_input("F5: ATR % of LTP kam se kam", value=0.12, min_value=0.05, max_value=0.5, step=0.01)
f_mid = sb.checkbox("F6: Mid-day lull (12:00-13:15) kadi shart", value=True,
                    help="Is time me min score +1 aur Vol Spike >= niche wali value chahiye.")
f_mid_vol = sb.number_input("F6: Mid-day Vol Spike x kam se kam", value=1.5, min_value=1.0, max_value=4.0, step=0.1)
be_r = sb.number_input("Breakeven SL tab lagao jab profit = R x", value=1.2, min_value=0.5, max_value=2.0, step=0.1,
                       help="Pehle 1.0R tha. Thoda late breakeven = chhoti pullback me kam stop-out.")
pcr_lo, pcr_hi = 0.80, 1.30  # v7.7: istemal nahi (require_pcr hamesha OFF)

sb.header("🔴 LIVE TRADING - Equity Intraday")
sb.caption("Instrument: EQUITY INTRADAY (NSE/BSE cash, product = Intraday). "
           "Quantity = us share ke 1 F&O lot ke shares. Default me OFF.")
live_on_cb = sb.checkbox(
    "LIVE trading ON (asli paise, asli orders)", value=False,
    help="ON karne par har paper-trade entry ke saath Upstox ko ASLI order jayega.")
live_confirm = sb.text_input("Confirm: yahan LIVE likho", value="")
live_max_trades = sb.number_input("Max live trades / din", value=5, min_value=1, max_value=50, step=1)
live_max_value = sb.number_input("Max order value Rs / trade", value=500000, min_value=10000, step=50000)
live_max_loss = sb.number_input("Upstox ACCOUNT ka max loss Rs (MTM) - isse zyada par SAB band", value=5000, min_value=500, step=500,
                                help="Account ki saari positions ka P&L (manual trade samet) dekha jata hai.")
live_kill = sb.button("🛑 SAARE LIVE POSITION ABHI BAND KARO")
live_resume = sb.button("▶ Live entries dobara allow karo")
stk_resume = sb.button("🔓 Aaj ki trading-halt hatao (max loss/kill ke baad)")

sb.header("📓 Paper Trade DB Settings")
save_demo_db = sb.checkbox(
    "Save Demo Paper Trades to DB",
    value=True,
    help="On rakhne par Demo mode ke trades bhi DB mein 'DEMO' tag ke saath save honge taaki aap test/analyze kar sakein.",
)
auto_paper_stocks = sb.checkbox(
    "Auto Paper-Trade Stock Signals (🟢/🔻)",
    value=True,
    help="Strong Buy / Strong Sell wale F&O stocks ka bhi live paper trade DB mein open/update/close karega.",
)

gsheet_on_cb = sb.checkbox(
    "Google Sheet auto-sync (trades + day summary)",
    value=True,
    help="Har trade entry/update/exit Google Sheet me jata hai. secrets.toml me [gcp_service_account] zaroori hai.",
)
sb.header("🗓 Result Lock Rule")
lock_mode = sb.selectbox(
    "Lock rule",
    ["Result Week", "Window"],
    index=0,
    help="Result Week = result usi hafte me ho to lock. Window = result se N din pehle se M din baad tak.",
)
pre_days = sb.slider("Window: trading days BEFORE result", 0, 5, 2)
post_days = sb.slider("Window: trading days AFTER result", 0, 3, 1)
lock_pattern = sb.checkbox(
    "Approx pattern dates par bhi lock lagao",
    value=True,
    help="Off = sirf exact date wale stocks lock honge.",
)

sb.header("📉 Volatility Filters")
max_monthly_move_th = sb.number_input("Low Volatility Threshold (% Monthly Move)", value=10.0, min_value=2.0, max_value=30.0, step=0.5)
use_range_filter = sb.checkbox("Avg daily range (Rs) filter on", value=False)
rng_min = sb.number_input("Avg daily range min (Rs)", value=5.0, min_value=0.0, step=1.0)
rng_max = sb.number_input("Avg daily range max (Rs)", value=15.0, min_value=0.0, step=1.0)

sb.header("🟠 15m Consolidation (No-Trade Zone)")
zone_filter = sb.checkbox("15m consolidation = NO TRADE ZONE", value=True)
zone_n = sb.slider(
    "Zone lookback (closed 15m candles)",
    4, 12, 6,
    help="Itni 15m candles ki range dekhi jati hai (6 = ~1.5 ghanta).",
)
zone_atr_th = sb.number_input("Zone range <= ATR(15m) x", value=2.5, min_value=1.0, max_value=5.0, step=0.25)
zone_adx_th = sb.slider("Zone: 15m ADX below", 10, 30, 20)
zone_buf = sb.number_input("Breakout buffer (ATR15 x)", value=0.10, min_value=0.0, max_value=1.0, step=0.05)

sb.header("🟠 Choppy Market = NO TRADE ZONE")
chop_filter = sb.checkbox(
    "Market choppy ho to naye stock trade band", value=True,
    help="Index ka haal dekh kar: 15m consolidation, VWAP whipsaw, ya kamzor ADX + flat trend = naye trade nahi.")
chop_adx = sb.slider("Index ADX(5m) is se neeche = kamzor trend", 10, 30, 18)
chop_flat = sb.checkbox("Kamzor ADX + Index 5m/15m dono flat = choppy", value=True)
chop_cross = sb.slider("Index 1 ghante me VWAP itni baar cross = choppy (whipsaw)", 2, 8, 3)

# v7.7: PCR filter + Solo Mover Override HATAYE. Ye variable sirf purane code/backtest ke liye fixed rakhe hain.
pcr_filter_on = False
pcr_long_min, pcr_short_max, pcr_stab = 1.02, 0.92, 0.03
solo_on, solo_need_orb, solo_need_oi = False, False, False
solo_min_score, solo_rs, solo_vol, solo_adx = 6, 0.5, 1.5, 25
spcr_trend, spcr_need, spcr_chg_confirm = False, False, False
sb.header("📊 Stock PCR (sirf jaankari - filter nahi, v7.7)")
sb.caption("ℹ PCR ab entry ko block NAHI karta. Scanner me Stock PCR / OI Writing / PCR base sirf dekhne ke liye hain.")
pcr_source = sb.selectbox("PCR source (sirf display/data)", ["Stock PCR (har stock ka apna)", "Index PCR (purana)"], index=0,
                          help="Stock PCR = us stock ke apne option chain ka PCR. v7.7: sirf Scanner columns / daily snapshot ke liye - trade block nahi hota.")
spcr_long = sb.number_input("Stock PCR: LONG tab jab PCR >", value=1.0, min_value=0.5, max_value=2.5, step=0.05)
spcr_short = sb.number_input("Stock PCR: SHORT tab jab PCR <", value=0.8, min_value=0.2, max_value=1.5, step=0.05)
spcr_range = sb.number_input("Stock PCR ke liye strike range (spot ka ± %) - near-ATM zyada tez signal", value=4.0, min_value=1.0, max_value=30.0, step=0.5,
                             help="Door ki strikes intraday me kam kaam ki hoti hain. 3-5% theek. Adaptive baseline jama hone ke beech ye badalna mat - purana aur naya PCR mismatch hoga.")
spcr_show_all = sb.checkbox("Scanner me SAARE stocks ka Stock PCR dikhao (sirf display)", value=True,
                            help="OFF = purana tareeka: PCR sirf STRONG BUY/SELL candidates ka fetch hota hai, baaki blank. "
                                 "ON = har refresh me neeche wale batch jitne stocks ka PCR (round-robin), baaki ka pichhla cached PCR.")
spcr_batch = sb.slider("Har refresh me kitne (non-signal) stocks ka PCR fetch karo", 5, 80, 30,
                       help="Har stock = 1 option-chain API call (+ din me ek baar expiry call). Zyada rakhoge to refresh dheema.")
spcr_min_oi = sb.number_input("Stock PCR: strike range me kam se kam total OI (call+put, LOTS me; 0 = off)", value=200, min_value=0, step=50,
                              help="Kam OI wale (illiquid) option chain me 2-4 bade orders se PCR jhootha dikhta hai. Kam OI ho to PCR 'data nahi' maana jaata hai. "
                                   "Upstox OI shares me de to code lot size se bhaag dekar lots me badal leta hai (unit auto-detect). "
                                   "Scanner ke 'PCR total OI (lots)' column se apne stocks ke hisaab se badlo.")
spcr_mode = sb.selectbox("Stock PCR neutral zone", ["20-din apna average (adaptive)", "Fixed (LONG > upar wali limit / SHORT < neeche wali)"], index=0,
                         help="Adaptive: har stock ke pichhle N din ke average PCR ke aas-paas (± band) = neutral. Average+band se upar = LONG, "
                              "average-band se neeche = SHORT, beech me trade nahi. Roz 15:35 ke baad PCR ka snapshot jama hota hai.")
spcr_days = sb.slider("Adaptive: pichhle kitne din ka average", 5, 60, 20)
spcr_min_days = sb.slider("Adaptive: kitne din ki history jama hone par adaptive shuru", 5, 60, 20,
                          help="Jab tak itne din ka PCR DB me jama na ho, Fixed rule (LONG > upar wali limit / SHORT < neeche wali) chalta hai. "
                               "Itne din hote hi adaptive (average +- band) shuru.")
spcr_k = sb.number_input("Adaptive: neutral band = k x (din-din ke PCR ka std)", value=0.5, min_value=0.0, max_value=3.0, step=0.1)
spcr_min_band = sb.number_input("Adaptive: neutral band ka minimum (± PCR)", value=0.05, min_value=0.0, max_value=0.5, step=0.01)
spcr_fallback_mode = sb.selectbox(
    "20 din ki history banne tak kaunsa PCR rule",
    ["Ab tak ke din ka average PCR = baseline (v7.5)", "Fixed limit (LONG > 1.0 / SHORT < 0.8)", "Koi nahi (trade band)"], index=0,
    help="Jitne din ka PCR DB me jama hai (1, 2, 3 ... 19 din) unka average = baseline. Stock PCR baseline se upar = LONG, "
         "neeche = SHORT. DB khaali ho to option chain ke prev OI wala pichhle din ka PCR baseline. 20 din poore hote hi "
         "adaptive rule (20 din avg +- band) apne aap.")
spcr_fallback = not str(spcr_fallback_mode).startswith("Koi")
spcr_prevday = str(spcr_fallback_mode).startswith("Ab tak")
spcr_writing_on = sb.checkbox("Baseline rule ke saath OI writing bhi confirm (LONG: put writing, SHORT: call writing)", value=True,
                              help="ON = PCR baseline se upar ho AUR aaj put writing ho tab LONG (SHORT me ulta). OFF = sirf PCR vs baseline.")
spcr_adaptive = str(spcr_mode).startswith("20")
try:
    with db() as _c:
        _hd = int(_c.execute("SELECT COUNT(DISTINCT dt) FROM pcr_daily").fetchone()[0] or 0)
except Exception:
    _hd = 0
_need_d = min(int(spcr_min_days), int(spcr_days))
if str(pcr_source).startswith("Stock") and spcr_adaptive:
    sb.caption(f"📈 Stock PCR history: {_hd}/{_need_d} din - " + ("adaptive zone ON ✅" if _hd >= _need_d else
               (f"abhi {_hd} din ke AVERAGE PCR ko baseline maan kar: upar LONG / neeche SHORT" if spcr_prevday else
                f"abhi Fixed rule chal raha hai (LONG > {float(spcr_long):.2f} / SHORT < {float(spcr_short):.2f})")))
use_stock_pcr = str(pcr_source).startswith("Stock")

_mode_ph.caption(
    (("✅ Default Setting ON: " + ("settings default se shuru, tum badal sakte ho (Manual adjust ON). " if edit_on
                                   else "strategy settings code default par lock. ")) if use_defaults else "✏ Default OFF: settings manual. ")
    + "Max positions 15 | Max trades/din 15 | Direction limit 5 (default).")
sb.header("📣 Alerts / Refresh")
oi_window = sb.selectbox("OI / buildup comparison window (min)", [10, 15, 30], index=1)
oi_th = sb.number_input("Stock futures OI change threshold (%)", value=0.15, min_value=0.05, max_value=3.0, step=0.05)
px_th = sb.number_input("Price change threshold for buildup (%)", value=0.10, min_value=0.02, max_value=2.0, step=0.02)
refresh_sec = sb.selectbox("Auto refresh (sec)", [15, 30, 60], index=1)
stock_ttl_base = sb.selectbox("Stock candle refetch (sec)", [45, 60, 90, 120], index=1)
auto_refresh = sb.checkbox("Enable Auto-Refresh", value=True)
two_tier = sb.checkbox(
    "Two-tier scan (full scan har N min, beech me sirf final shares)",
    value=True,
    help="Full scan me sabhi stocks. Uske baad sirf final (filter pass) shares har refresh par.",
)
full_scan_min = sb.selectbox("Full rescan every (min)", [5, 10, 15, 30], index=2)
watch_max = sb.slider("Max final shares in watchlist", 3, 30, 12)
watch_ext = sb.checkbox("Watchlist me EXTENDED / against-index shares bhi lo", value=True)
watch_wait = sb.checkbox("Watchlist me 'WAIT (need ...)' near-signal shares bhi lo", value=True,
                         help="v7.8 default ON: jo stock sirf ek-do shart (volume / 15m) se chooka, wo har refresh par dobara check hoga. "
                              "Filter dheele nahi hote. Watchlist me STRONG sabse pehle, WAIT sabse baad (jagah bache to).")
force_full = sb.button("Force full rescan now")
tg_alerts = sb.checkbox("Telegram alerts (entry/exit)", value=bool(TG_TOKEN and TG_CHAT))
tg_cmd_on = sb.checkbox("Telegram commands (/status /kill /resume /exit SYMBOL) - sirf aapki chat ID se", value=True,
                        help="Phone se hi status dekho, KILL_SWITCH lagao ya kisi stock ko band karwao. Sirf TELEGRAM_CHAT_ID wali chat ke commands maane jaate hain.")

with sb.expander("⚖ Customize Stock Weights (%)"):
    W = {
        s: st.number_input(s, value=float(w), min_value=0.0, max_value=60.0, step=0.1, key=f"w_{s}")
        for s, w in (ACTIVE_DEFAULT_WEIGHTS.items() if len(ACTIVE_DEFAULT_WEIGHTS) <= 60 else [])
    }
if sum(W.values()) <= 0:
    W = dict(ACTIVE_DEFAULT_WEIGHTS)


# ---- 24x7 Background Agent: sidebar control + status ----
if not _IS_BG:
    sb.markdown("---")
    sb.subheader("🤖 24x7 Background Agent")
    _bg_prev = BGS["enabled"]
    BGS["enabled"] = sb.checkbox("Keep Trading Agent Running (24x7)", value=_bg_prev)
    if BGS["enabled"] != _bg_prev:
        BGS["wake"].set()

    def _bg_status_body():
        _t = BGS["last_tick"].strftime("%H:%M:%S") if BGS["last_tick"] else "--"
        _d = BGS["last_dur"] if BGS["last_dur"] is not None else "--"
        with st.sidebar:
            st.caption(f"Status: {BGS['status']} | Last BG Tick (IST): {_t} | BG Cycles: {BGS['cycles']} | Last run: {_d}s")
            if BGS["last_error"]:
                with st.expander("⚠ BG last error"):
                    st.code(BGS["last_error"])

    try:
        _bg_frag = st.fragment(run_every=10)(_bg_status_body)
    except Exception:
        _bg_frag = _bg_status_body
    _bg_frag()
    sb.caption("Background me sirf PAPER trades + data. LIVE orders sirf browser se. Naya Upstox token daalne ke baad app ek baar kholo.")


# ====== SECTION: GLOBAL STORES & SAFE SESSION STATE ======
@st.cache_resource
def _hist_store() -> dict:
    return {}


@st.cache_resource
def _intra_store() -> dict:
    return {}


@st.cache_resource
def _snap_store() -> dict:
    return {}


@st.cache_resource
def _api_log() -> deque:
    return deque(maxlen=4000)


@st.cache_resource
def _err_log() -> deque:
    return deque(maxlen=60)


@st.cache_resource
def _snap_lock():
    return threading.Lock()


class RateLimiter:
    def __init__(self, per_sec: float = 20.0):
        self.lock = threading.Lock()
        self.gap = 1.0 / per_sec
        self.nxt = 0.0

    def wait(self):
        with self.lock:
            now = time.monotonic()
            t = max(now, self.nxt)
            self.nxt = t + self.gap
        d = t - now
        if d > 0:
            time.sleep(d)


@st.cache_resource
def _limiter() -> RateLimiter:
    return RateLimiter(20.0)


HIST_STORE = _hist_store()
INTRA_STORE = _intra_store()
SNAP = _snap_store()
API_LOG = _api_log()
ERR_LOG = _err_log()
SNAP_LOCK = _snap_lock()
LIMITER = _limiter()


def ensure_session_state():
    ss_ = st.session_state
    _day = now_ist().strftime("%Y-%m-%d")
    if SNAP.get("_day") != _day:
        SNAP.clear()
        SNAP["_day"] = _day
    ss_.setdefault("only_low_vol_10", False)
    return ss_


ss = ensure_session_state()


# ====== SECTION: DATA LAYER ======
def auth_headers(tok: str) -> dict:
    return {"Accept": "application/json", "Authorization": f"Bearer {tok}", "Api-Version": "2.0"}


def http_json(url: str, headers: dict, params=None, timeout: int = 8, retries: int = 2):
    code, js = 0, {}
    for attempt in range(retries + 1):
        LIMITER.wait()
        API_LOG.append(time.time())
        try:
            r = requests.get(url, headers=headers, params=params, timeout=timeout)
            code = r.status_code
            try:
                js = r.json()
            except Exception:
                js = {}
        except Exception as e:
            code, js = 0, {"error": str(e)}
        if code == 429:
            time.sleep(1.0 + attempt)
            continue
        if code in (0, 500, 502, 503, 504) and attempt < retries:
            time.sleep(0.4 * (attempt + 1))
            continue
        break
    if code == 401:
        SNAP["auth_error"] = True
    if code != 200:
        ERR_LOG.append((now_ist().strftime("%H:%M:%S"), code, url.replace(V2, "")[:70], str(js)[:140]))
    return code, js


def api_calls_last(sec: int = 60) -> int:
    cut = time.time() - sec
    return sum(1 for t in list(API_LOG) if t > cut)


def ensure_ts(df: pd.DataFrame) -> pd.DataFrame:
    """v7.8.1: "ts" column hamesha IST datetime ho (string / mixed tz / object dtype sab theek) - warna .dt crash hota hai."""
    if df is None:
        return pd.DataFrame(columns=["ts", "o", "h", "l", "c", "v"]).pipe(ensure_ts)
    if "ts" not in df.columns:
        return df
    if not (pd.api.types.is_datetime64_any_dtype(df["ts"]) and getattr(df["ts"].dt, "tz", None) is not None):
        df = df.copy()
        df["ts"] = pd.to_datetime(df["ts"], utc=True, errors="coerce")
    df["ts"] = df["ts"].dt.tz_convert(IST)
    if df["ts"].isna().any():
        df = df.dropna(subset=["ts"]).reset_index(drop=True)
    return df


def parse_candles(raw) -> pd.DataFrame:
    cols = ["ts", "o", "h", "l", "c", "v"]
    if not raw:
        return ensure_ts(pd.DataFrame(columns=cols))      # v7.8.1: khaali par bhi ts = datetime dtype
    df = pd.DataFrame([r[:6] for r in raw], columns=cols)
    df["ts"] = pd.to_datetime(df["ts"], utc=True, errors="coerce").dt.tz_convert(IST)
    for c in cols[1:]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna(subset=["ts", "o", "h", "l", "c"]).drop_duplicates("ts")
    return df.sort_values("ts").reset_index(drop=True)


def merge_1m(prior: pd.DataFrame, today_df: pd.DataFrame) -> pd.DataFrame:
    """v7.8.1: pichle din + aaj ki 1m candles jodo. Sirf non-empty frames concat (empty object column dtype nahi bigadta)."""
    parts = [ensure_ts(x) for x in (prior, today_df) if x is not None and not x.empty]
    if not parts:
        return parse_candles([])
    df = pd.concat(parts, ignore_index=True) if len(parts) > 1 else parts[0]
    df = ensure_ts(df)
    return df.drop_duplicates("ts").sort_values("ts").reset_index(drop=True)


def resample_ohlcv(df: pd.DataFrame, tf: str = "5min") -> pd.DataFrame:
    if df is None or df.empty:
        return df
    return (
        df.set_index("ts")
        .resample(tf)
        .agg({"o": "first", "h": "max", "l": "min", "c": "last", "v": "sum"})
        .dropna(subset=["c"])
        .reset_index()
    )


def drop_forming(df: pd.DataFrame, minutes: int, live: bool) -> pd.DataFrame:
    """Live market me abhi ban rahi (adhuri) candle hata do - signal sirf closed candle par."""
    if not live or df is None or df.empty:
        return df
    now = now_ist()
    last = df["ts"].iloc[-1]
    if last.date() == now.date() and last + timedelta(minutes=minutes) > now:
        return df.iloc[:-1].reset_index(drop=True)
    return df


def _candles_from(js, code):
    if code != 200:
        return []
    return (js.get("data") or {}).get("candles") or []


def fetch_intraday(ikey: str, tok: str, ttl: int) -> pd.DataFrame:
    now_t = time.time()
    cached = INTRA_STORE.get(ikey)
    if cached and now_t - cached[0] < ttl:
        return cached[1]
    enc, h = quote(ikey, safe=""), auth_headers(tok)
    code, js = http_json(f"{V2}/historical-candle/intraday/{enc}/1minute", h)
    if code != 200 and cached:
        return cached[1]
    df = parse_candles(_candles_from(js, code))
    INTRA_STORE[ikey] = (now_t, df)
    return df


def fetch_prior_1m(ikey: str, tok: str) -> pd.DataFrame:
    now_t = time.time()
    ck = "p1m:" + ikey
    cached = HIST_STORE.get(ck)
    if cached and now_t - cached[0] < PRIOR_TTL:
        return cached[1]
    enc, h = quote(ikey, safe=""), auth_headers(tok)
    today = now_ist().date()
    code, js = http_json(
        f"{V2}/historical-candle/{enc}/1minute/{today.isoformat()}/{(today - timedelta(days=7)).isoformat()}", h
    )
    df = parse_candles(_candles_from(js, code))
    if not df.empty:
        df = df[df["ts"].dt.date < today].reset_index(drop=True)
    if code != 200 and cached:
        return cached[1]
    # fail hua (429/network) to lamba cache mat karo - 2 min baad dobara try hoga
    HIST_STORE[ck] = (now_t if code == 200 else now_t - PRIOR_TTL + 120, df)
    return df


def fetch_daily_stats(ikey: str, tok: str) -> dict:
    now_t = time.time()
    ck = "d:" + ikey
    cached = HIST_STORE.get(ck)
    if cached and now_t - cached[0] < HIST_TTL:
        return cached[1]
    enc, h = quote(ikey, safe=""), auth_headers(tok)
    today = now_ist().date()
    code, js = http_json(
        f"{V2}/historical-candle/{enc}/day/{today.isoformat()}/{(today - timedelta(days=40)).isoformat()}", h
    )
    df = parse_candles(_candles_from(js, code))
    if code == 200 and not df.empty:
        try:
            save_daily_candles({v: k for k, v in C["eq"].items()}.get(ikey, ""), df)       # 1D candles bhi DB me
        except Exception:
            pass
    res = {"move": 0.0, "avg_rng": 0.0, "prev_close": 0.0}
    if code != 200 and cached:
        return cached[1]
    if not df.empty:
        done = df[df["ts"].dt.date < today]
        if not done.empty:
            res["prev_close"] = float(done["c"].iloc[-1])
        rec = df.tail(21)
        if len(rec) >= 5:
            mx, mn = float(rec["h"].max()), float(rec["l"].min())
            res["move"] = round((mx - mn) / mn * 100.0, 2) if mn > 0 else 0.0
        base = done.tail(20) if len(done) >= 5 else df.tail(20)
        res["avg_rng"] = round(float((base["h"] - base["l"]).mean()), 2)
    HIST_STORE[ck] = (now_t if code == 200 else now_t - HIST_TTL + 120, res)   # fail => 2 min me retry
    return res


def fetch_batch_quotes(keys: list, tok: str) -> dict:
    if not keys:
        return {}
    h = auth_headers(tok)
    out = {}
    for i in range(0, len(keys), 45):
        code, js = http_json(QUOTE_URL, h, params={"instrument_key": ",".join(keys[i:i + 45])})
        if code == 200 and isinstance(js.get("data"), dict):
            out.update(js["data"])
    return out


def fetch_chain_rows(ikey: str, tok: str, ttl: int = 60) -> dict:
    ck = "chain:" + ikey
    cached = INTRA_STORE.get(ck)
    if cached and time.time() - cached[0] < ttl:
        return cached[1]
    h = auth_headers(tok)
    res = {"rows": [], "expiry": ""}
    today_s = now_ist().date().isoformat()
    ec = SNAP.get("exp:" + ikey)                     # nazdeeki expiry din me badalti nahi - /option/contract roz ek hi baar
    exp0 = ec[1] if ec and ec[0] == today_s and ec[1] >= today_s else ""
    if not exp0:
        code, js = http_json(f"{V2}/option/contract", h, params={"instrument_key": ikey})
        if code == 200:
            exps = sorted({exp_to_str(x.get("expiry")) for x in (js.get("data") or []) if x.get("expiry")})
            exps = [e for e in exps if e and e >= today_s]
            exp0 = exps[0] if exps else ""
            if exp0:
                SNAP["exp:" + ikey] = (today_s, exp0)
    if exp0:
        code2, js2 = http_json(f"{V2}/option/chain", h, params={"instrument_key": ikey, "expiry_date": exp0})
        if code2 == 200:
            res = {"rows": js2.get("data") or [], "expiry": exp0}
    if not res["rows"] and cached:
        return cached[1]
    INTRA_STORE[ck] = (time.time(), res)
    return res


def oi_track(key: str, oi: float, ltp: float, window_min: int) -> tuple:
    now_t = time.time()
    with SNAP_LOCK:
        dq = SNAP.setdefault(f"oi:{key}", deque(maxlen=600))
        if oi > 0 and (not dq or now_t - dq[-1][0] >= 10):
            dq.append((now_t, oi, ltp))
        if not dq:
            return 0.0, 0.0, False
        target = now_t - window_min * 60
        base, ready = None, False
        for t, o, p in dq:
            if t <= target:
                base = (t, o, p)
            else:
                break
        if base is not None:
            ready = True
        else:
            base = dq[0]
            ready = (now_t - base[0]) >= window_min * 60 * 0.6
        cur_oi, cur_px = dq[-1][1], dq[-1][2]
    oi_chg = (cur_oi - base[1]) / base[1] * 100.0 if base[1] > 0 else 0.0
    px_chg = (cur_px - base[2]) / base[2] * 100.0 if base[2] > 0 else 0.0
    return round(oi_chg, 3), round(px_chg, 3), ready


# ====== SECTION: TECHNICAL INDICATORS ======
def compute_rsi(series: pd.Series, period: int = 14) -> float:
    if len(series) < period + 1:
        return 50.0
    delta = series.diff()
    up = delta.clip(lower=0.0)
    down = -1.0 * delta.clip(upper=0.0)
    ma_up = up.ewm(com=period - 1, adjust=False).mean()
    ma_down = down.ewm(com=period - 1, adjust=False).mean()
    rs = ma_up / ma_down.replace(0, np.nan)
    rsi = 100.0 - (100.0 / (1.0 + rs))
    val = float(rsi.iloc[-1])
    if np.isnan(val):
        return 100.0 if float(ma_up.iloc[-1]) > 0 else 50.0
    return round(val, 1)


def compute_atr_and_adx(df5: pd.DataFrame, period: int = 14) -> tuple:
    if len(df5) < period + 2:
        return 0.0, 0.0
    h, l, c = df5["h"], df5["l"], df5["c"]
    prev_c = c.shift(1)
    tr = pd.concat([h - l, (h - prev_c).abs(), (l - prev_c).abs()], axis=1).max(axis=1)
    atr_s = tr.ewm(alpha=1 / period, adjust=False).mean()

    up_move = h.diff()
    dn_move = -l.diff()
    plus_dm = np.where((up_move > dn_move) & (up_move > 0), up_move, 0.0)
    minus_dm = np.where((dn_move > up_move) & (dn_move > 0), dn_move, 0.0)

    plus_di = 100 * pd.Series(plus_dm, index=df5.index).ewm(alpha=1 / period, adjust=False).mean() / atr_s.replace(0, np.nan)
    minus_di = 100 * pd.Series(minus_dm, index=df5.index).ewm(alpha=1 / period, adjust=False).mean() / atr_s.replace(0, np.nan)
    dx = (100 * (plus_di - minus_di).abs() / (plus_di + minus_di).replace(0, np.nan)).fillna(0.0)
    adx = float(dx.ewm(alpha=1 / period, adjust=False).mean().iloc[-1])
    atr_val = float(atr_s.iloc[-1])
    return (0.0 if np.isnan(atr_val) else round(atr_val, 2)), (0.0 if np.isnan(adx) else round(adx, 1))


def analyze_candles(df1m: pd.DataFrame, monthly_move_pct: float = 0.0, live: bool = True, vwap_override: float = 0.0) -> dict:
    m = dict(EMPTY_M)
    m["monthly_move_pct"] = monthly_move_pct
    if df1m is None or df1m.empty:
        return m
    df1m = ensure_ts(df1m)                               # v7.8.1: .dt se pehle safety
    if df1m.empty:
        return m

    now = now_ist()
    session_d = df1m["ts"].dt.date.max()
    df_s = df1m[df1m["ts"].dt.date == session_d].copy()
    m["has_today"] = session_d == now.date()
    m["n_today"] = len(df_s) if m["has_today"] else 0

    df5 = drop_forming(resample_ohlcv(df1m, "5min"), 5, live)
    df15 = drop_forming(resample_ohlcv(df1m, "15min"), 15, live)
    if df5 is None or df5.empty:
        return m

    m["ok"] = True
    m["last_ts"] = df5["ts"].iloc[-1]
    m["last_close"] = round(float(df5["c"].iloc[-1]), 2)
    # v5.3: aakhri CLOSED 5m candle me close ki position (1.0 = high par band, 0.0 = low par band) -> wick rejection filter
    _h5, _l5, _c5 = float(df5["h"].iloc[-1]), float(df5["l"].iloc[-1]), float(df5["c"].iloc[-1])
    m["bar_pos"] = round((_c5 - _l5) / (_h5 - _l5), 2) if (_h5 - _l5) > 0 else 0.5
    m["ema9"] = round(float(df5["c"].ewm(span=9, adjust=False).mean().iloc[-1]), 2)
    m["ema21"] = round(float(df5["c"].ewm(span=21, adjust=False).mean().iloc[-1]), 2)
    if df15 is not None and not df15.empty:
        m["ema9_15m"] = round(float(df15["c"].ewm(span=9, adjust=False).mean().iloc[-1]), 2)
        m["ema21_15m"] = round(float(df15["c"].ewm(span=21, adjust=False).mean().iloc[-1]), 2)
    m["rsi"] = compute_rsi(df5["c"], 14)
    m["atr"], m["adx"] = compute_atr_and_adx(df5, 14)

    if df15 is not None and not df15.empty:
        m["atr15"], m["adx15"] = compute_atr_and_adx(df15, 14)
        d15 = df15[df15["ts"].dt.date == df15["ts"].iloc[-1].date()].tail(int(zone_n))
        if len(d15) >= int(zone_n) and m["atr15"] > 0:
            hi, lo = float(d15["h"].max()), float(d15["l"].min())
            rng_atr = (hi - lo) / m["atr15"]
            gap = abs(m["ema9_15m"] - m["ema21_15m"]) / m["atr15"]
            m["z15_hi"], m["z15_lo"], m["z15_rng_atr"] = round(hi, 2), round(lo, 2), round(rng_atr, 2)
            m["z15_cons"] = bool(rng_atr <= zone_atr_th and (m["adx15"] < zone_adx_th or gap < 0.35))

    tp = (df_s["h"] + df_s["l"] + df_s["c"]) / 3.0
    vol = df_s["v"].replace(0, 1)
    cum_v = vol.cumsum()
    vwap_s = (tp * vol).cumsum() / cum_v
    var = ((tp ** 2 * vol).cumsum() / cum_v - vwap_s ** 2).clip(lower=0)
    sd = float(np.sqrt(var.iloc[-1]))
    vw = float(vwap_s.iloc[-1])
    m["vwap_ok"] = bool(df_s["v"].sum() > 0)
    if vwap_override and vwap_override > 0:
        vw = float(vwap_override)
        m["vwap_ok"] = True
    m["vwap"] = round(vw, 2)
    m["vwap_up1"], m["vwap_dn1"] = round(vw + sd, 2), round(vw - sd, 2)
    m["vwap_up2"], m["vwap_dn2"] = round(vw + 2 * sd, 2), round(vw - 2 * sd, 2)

    t_idx = df_s["ts"].dt.time
    orb = df_s[(t_idx >= dtime(9, 15)) & (t_idx < dtime(9, 30))]
    if orb.empty:
        orb = df_s.head(15)
    m["orh"], m["orl"] = round(float(orb["h"].max()), 2), round(float(orb["l"].min()), 2)
    m["orb_ready"] = (not live) or (not m["has_today"]) or now.time() >= dtime(9, 30)
    m["day_high"], m["day_low"] = round(float(df_s["h"].max()), 2), round(float(df_s["l"].min()), 2)
    m["day_open"] = round(float(df_s["o"].iloc[0]), 2)
    try:   # v5.3: kal ka High/Low (agar prior-day candles data me hain)
        _prev = df1m[df1m["ts"].dt.date < session_d]
        if not _prev.empty:
            _pd = _prev[_prev["ts"].dt.date == _prev["ts"].dt.date.max()]
            m["pdh"], m["pdl"] = round(float(_pd["h"].max()), 2), round(float(_pd["l"].min()), 2)
    except Exception:
        pass
    try:   # pichhle ~1 ghante (12 x 5m) me price ne VWAP ko kitni baar cross kiya (whipsaw / choppy ka nishan)
        s5 = df5[df5["ts"].dt.date == session_d]
        v5 = vwap_s.groupby(df_s["ts"].dt.floor("5min")).last()
        sgn = np.sign(s5["c"].values - v5.reindex(s5["ts"]).values)
        sgn = sgn[~np.isnan(sgn)]
        sgn = sgn[sgn != 0][-12:]
        m["vwap_cross"] = int((sgn[1:] != sgn[:-1]).sum()) if len(sgn) > 1 else 0
    except Exception:
        m["vwap_cross"] = 0

    if len(df5) >= 12:
        avg_v = float(df5["v"].iloc[-11:-1].mean())
        cur_v = float(df5["v"].iloc[-1])
        m["vol_spike"] = round(cur_v / avg_v, 2) if avg_v > 0 else 1.0

    if live and market_open() and m["has_today"]:
        m["stale_min"] = round((now - df1m["ts"].iloc[-1]).total_seconds() / 60.0, 1)
    return m


def trend_dir(ltp: float, m: dict) -> int:
    if not m["ok"] or m["ema9"] <= 0 or m["ema21"] <= 0:
        return 0
    vw_up = (not m["vwap_ok"]) or ltp >= m["vwap"]
    vw_dn = (not m["vwap_ok"]) or ltp <= m["vwap"]
    if ltp > m["ema9"] > m["ema21"] and vw_up:
        return 1
    if ltp < m["ema9"] < m["ema21"] and vw_dn:
        return -1
    return 0


def zone_state(ltp: float, m: dict) -> tuple:
    if not m["ok"] or not m["z15_cons"] or m["atr15"] <= 0:
        return "-", False
    buf = zone_buf * m["atr15"]
    if ltp > m["z15_hi"] + buf:
        return "BREAKOUT ↑ (zone toota)", False
    if ltp < m["z15_lo"] - buf:
        return "BREAKDOWN ↓ (zone toota)", False
    return "🟠 IN ZONE", True


def score_stock_filters(ltp: float, prev_close: float, m: dict, oi_chg: float, px_chg: float, oi_ready: bool,
                        adx_min_th: float) -> dict:
    score = 0
    chg_pct = ((ltp - prev_close) / prev_close * 100.0) if prev_close > 0 else 0.0
    vwap_sig, ema5_sig, mtf15_sig, orb_sig = "NEUTRAL", "FLAT", "FLAT", "INSIDE ORB"
    mtf_d = orb_d = fut_d = 0

    if m["ok"] and m["vwap"] > 0:
        if ltp > m["vwap"]:
            score += 1
            vwap_sig = "ABOVE VWAP"
        elif ltp < m["vwap"]:
            score -= 1
            vwap_sig = "BELOW VWAP"

    if m["ok"] and m["ema9"] > 0 and m["ema21"] > 0:
        if ltp > m["ema9"] > m["ema21"]:
            score += 1
            ema5_sig = "BULL (9>21)"
        elif ltp < m["ema9"] < m["ema21"]:
            score -= 1
            ema5_sig = "BEAR (9<21)"

    if m["ok"] and m["ema9_15m"] > 0 and m["ema21_15m"] > 0:
        if m["ema9_15m"] > m["ema21_15m"]:
            score += 1
            mtf15_sig, mtf_d = "15m BULL", 1
        elif m["ema9_15m"] < m["ema21_15m"]:
            score -= 1
            mtf15_sig, mtf_d = "15m BEAR", -1

    if m["ok"]:
        if m["rsi"] >= 55.0:
            score += 1
        elif m["rsi"] <= 45.0:
            score -= 1

    if m["ok"] and m["orh"] > 0 and m["orl"] > 0:
        if not m["orb_ready"]:
            orb_sig = "ORB FORMING ⏳"
        elif ltp > m["orh"]:
            score += 1
            orb_sig, orb_d = "ORB BREAKOUT 🔼", 1
        elif ltp < m["orl"]:
            score -= 1
            orb_sig, orb_d = "ORB BREAKDOWN 🔽", -1

    if chg_pct >= 0.25:
        score += 1
    elif chg_pct <= -0.25:
        score -= 1

    fut_buildup = "BUILDING BASELINE ⏳" if not oi_ready else "NEUTRAL"
    if oi_ready:
        if oi_chg > oi_th and px_chg > px_th:
            score += 1
            fut_buildup, fut_d = "LONG BUILDUP 🟢", 1
        elif oi_chg > oi_th and px_chg < -px_th:
            score -= 1
            fut_buildup, fut_d = "SHORT BUILDUP 🔴", -1
        elif oi_chg < -oi_th and px_chg > px_th:
            fut_buildup = "SHORT COVERING ⬆"
        elif oi_chg < -oi_th and px_chg < -px_th:
            fut_buildup = "LONG UNWINDING ⬇"

    if m["ok"] and m["adx"] >= max(adx_min_th, 15.0) and m["vol_spike"] >= 1.2:
        score += 1 if score > 0 else (-1 if score < 0 else 0)

    ext_long = ext_short = False
    why_long, why_short = [], []
    if m["ok"] and m["atr"] > 0 and m["vwap"] > 0:
        dist = (ltp - m["vwap"]) / m["atr"]
        ext_long = dist > ext_atr or m["rsi"] >= 78
        ext_short = dist < -float(ext_atr_s) or m["rsi"] <= 22
        if ext_long:
            why_long.append("over-extended")
        if ext_short:
            why_short.append("over-extended")
        # v5.3 filter 1: Day High / Day Low (aur kal ke High/Low) ki deewar - breakout (ltp >= high) block nahi hota
        if f_wall:
            _w = float(f_wall_atr) * m["atr"]
            _res = [x for x in (m["day_high"], m.get("pdh", 0.0)) if x > ltp]
            _sup = [x for x in (m["day_low"], m.get("pdl", 0.0)) if 0 < x < ltp]
            if _res and (min(_res) - ltp) < _w:
                why_long.append("resistance (day/prev high) paas")
            if _sup and (ltp - max(_sup)) < _w:
                why_short.append("support (day/prev low) paas")
        # v5.3 filter 2: signal candle wick rejection
        if f_wick:
            _bp = m.get("bar_pos", 0.5)
            if _bp < float(f_wick_long):
                why_long.append(f"wick rejection (close {_bp:.2f})")
            if _bp > float(f_wick_short):
                why_short.append(f"wick rejection (close {_bp:.2f})")
        # v5.3 filter 5: dead candle / chhota ATR (SL brokerage me hi uth jayega)
        if f_minatr and ltp > 0 and (m["atr"] / ltp) < float(f_minatr_pct) / 100.0:
            why_long.append("ATR% kam")
            why_short.append("ATR% kam")
        ext_long, ext_short = bool(why_long), bool(why_short)

    zone_txt, in_zone = zone_state(ltp, m)

    return {
        "zone_txt": zone_txt, "in_zone": in_zone,
        "net_score": int(score), "chg_pct": round(chg_pct, 2), "vwap_sig": vwap_sig, "ema5_sig": ema5_sig,
        "mtf15_sig": mtf15_sig, "orb_sig": orb_sig, "fut_buildup": fut_buildup,
        "mtf_d": mtf_d, "orb_d": orb_d, "fut_d": fut_d, "ext_long": ext_long, "ext_short": ext_short,
        "why_long": ", ".join(why_long), "why_short": ", ".join(why_short),
    }


# ====== SECTION: OPTION CHAIN ANALYTICS ======
def analyze_chain(rows: list, spot: float) -> dict:
    recs = []
    for r in rows or []:
        try:
            k = float(r.get("strike_price"))
            co, po = r.get("call_options") or {}, r.get("put_options") or {}
            cm, pm = co.get("market_data") or {}, po.get("market_data") or {}
            cg = safe_float((co.get("option_greeks") or {}).get("gamma"))
            pg = safe_float((po.get("option_greeks") or {}).get("gamma"))
            recs.append((k, safe_float(cm.get("oi")), safe_float(cm.get("prev_oi")),
                         safe_float(pm.get("oi")), safe_float(pm.get("prev_oi")), cg, pg))
        except Exception:
            continue
    if not recs or spot <= 0:
        return {}
    df = pd.DataFrame(recs, columns=["k", "coi", "cprev", "poi", "pprev", "cg", "pg"]).sort_values("k").reset_index(drop=True)
    atm = float(df.iloc[(df["k"] - spot).abs().argmin()]["k"])
    near = df[(df["k"] >= atm - PCR_RANGE) & (df["k"] <= atm + PCR_RANGE)]
    out = {"atm": atm, "pcr": None, "pcr_oi_chg": None, "max_pain": None, "call_wall": None, "put_wall": None,
           "walls_c": [], "walls_p": [], "gex_ratio": None, "gex_text": "N/A"}
    if near["coi"].sum() > 0:
        out["pcr"] = round(float(near["poi"].sum() / near["coi"].sum()), 2)
    d_c = float((near["coi"] - near["cprev"]).sum())
    d_p = float((near["poi"] - near["pprev"]).sum())
    if d_c > 0:
        out["pcr_oi_chg"] = round(d_p / d_c, 2)

    ch = df[(df["k"] >= atm - CHAIN_RANGE) & (df["k"] <= atm + CHAIN_RANGE)]
    if not ch.empty:
        S, C_, P_ = ch["k"].values, ch["coi"].values, ch["poi"].values
        pain = [float((C_ * np.maximum(K - S, 0)).sum() + (P_ * np.maximum(S - K, 0)).sum()) for K in S]
        out["max_pain"] = float(S[int(np.argmin(pain))])
        up, dn = ch[ch["k"] >= spot].nlargest(3, "coi"), ch[ch["k"] <= spot].nlargest(3, "poi")
        out["walls_c"] = [(float(a), float(b)) for a, b in zip(up["k"], up["coi"])]
        out["walls_p"] = [(float(a), float(b)) for a, b in zip(dn["k"], dn["poi"])]
        if out["walls_c"]:
            out["call_wall"] = out["walls_c"][0][0]
        if out["walls_p"]:
            out["put_wall"] = out["walls_p"][0][0]
        g = ch["cg"] * ch["coi"] - ch["pg"] * ch["poi"]
        tot = float((ch["cg"] * ch["coi"]).abs().sum() + (ch["pg"] * ch["poi"]).abs().sum())
        if tot > 0:
            ratio = float(g.sum() / tot)
            out["gex_ratio"] = round(ratio, 2)
            out["gex_text"] = (
                "POSITIVE gamma - range/mean-reversion, chase mat karo" if ratio > 0.15 else
                "NEGATIVE gamma - trending/expansion, breakout follow karo" if ratio < -0.15 else
                "NEUTRAL gamma"
            )
    return out


# ====== SECTION: DEMO DATA (same pipeline, synthetic candles) ======
def synth_candles(seed: int, base: float, drift: float = 0.0, vol_scale: float = 1.0, days: int = 4) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    ds, cur = [], now_ist().date()
    while len(ds) < days:
        if cur.weekday() < 5:
            ds.append(cur)
        cur -= timedelta(days=1)
    ds.sort()
    frames, price = [], base
    for k, dd in enumerate(ds):
        n = 375
        dr = drift if k == len(ds) - 1 else drift * 0.3
        rets = rng.normal(dr / n, 0.0006 * vol_scale, n)
        closes = price * np.exp(np.cumsum(rets))
        opens = np.concatenate([[price], closes[:-1]])
        wig = np.abs(rng.normal(0, 0.0004 * vol_scale, n))
        highs, lows = np.maximum(opens, closes) * (1 + wig), np.minimum(opens, closes) * (1 - wig)
        vols = rng.integers(3000, 15000, n).astype(float) * (1 + (rng.random(n) > 0.97) * 3)
        ts = pd.date_range(datetime.combine(dd, dtime(9, 15), tzinfo=IST), periods=n, freq="1min")
        frames.append(pd.DataFrame({"ts": ts, "o": opens, "h": highs, "l": lows, "c": closes, "v": vols}))
        price = float(closes[-1])
    return pd.concat(frames, ignore_index=True)


def demo_mkt_drift() -> float:
    return 0.006 if now_ist().day % 2 == 0 else -0.006


def demo_stock_inputs(s: str) -> dict:
    seed = zlib.crc32(s.encode())
    rng = np.random.default_rng(seed)
    base = float(rng.integers(450, 3500))
    beta, idio, vs = rng.uniform(0.6, 1.4), rng.normal(0, 0.012), rng.uniform(0.7, 1.5)
    df = synth_candles(seed, base, drift=demo_mkt_drift() * beta + idio, vol_scale=vs)
    last_d = df["ts"].dt.date.max()
    prev = float(df[df["ts"].dt.date < last_d]["c"].iloc[-1])
    ltp = float(df["c"].iloc[-1])
    base_oi = float(rng.uniform(5e5, 5e6))
    oi = base_oi * (1 + 0.012 * math.sin(time.time() / 400.0 + (seed % 7)))
    return {"df1m": df, "ltp": ltp, "prev": prev, "atp": 0.0, "oi": oi, "fut_ltp": ltp,
            "move": round(float(rng.uniform(4.5, 15.5)), 2), "avg_rng": round(base * float(rng.uniform(0.01, 0.025)), 2),
            "spread_pct": round(0.02 + 0.2 * (((seed % 1000) / 1000.0) ** 4), 3)}


def demo_chain_rows(spot: float, step: float) -> list:
    rng = np.random.default_rng(5)
    atm = round(spot / step) * step
    rows = []
    for i in range(-30, 31):
        k = atm + i * step
        z = (k - spot) / (spot * 0.012)
        gam = math.exp(-0.5 * z * z) / (spot * 0.012)
        coi = float(rng.uniform(1e5, 6e5) * (1.8 if i in (6, 12) else 1.0) * (1.2 if i > 0 else 0.7))
        poi = float(rng.uniform(1e5, 6e5) * (1.8 if i in (-8, -14) else 1.0) * (1.2 if i < 0 else 0.7))
        rows.append({"strike_price": k,
                     "call_options": {"market_data": {"oi": coi, "prev_oi": coi * 0.93}, "option_greeks": {"gamma": gam}},
                     "put_options": {"market_data": {"oi": poi, "prev_oi": poi * 0.92}, "option_greeks": {"gamma": gam}}})
    return rows


def demo_bundle(symbols: list) -> dict:
    rng = np.random.default_rng(11)
    return {"eq": {s: f"DEMO|{s}" for s in symbols}, "fut": {s: f"DEMOF|{s}" for s in symbols},
            "lot_map": {s: int(rng.choice([250, 400, 500, 700, 1000, 1500])) for s in symbols},
            "idx": {u: (f"DEMOF|{u}", FALLBACK_LOTS.get(u, 1)) for u in INDEX_CATALOG}}


# ====== SECTION: MAIN EXECUTION ENGINE ======
if not TOKEN:
    st.info(
        "🔑 **Upstox Access Token Required:** Left sidebar mein apna Upstox API Token daalein "
        "ya `.streamlit/secrets.toml` mein `UPSTOX_TOKEN` configure karein. "
        "Neeche **Demo / Offline Simulation Mode** (same engine, synthetic data) bhi chala sakte hain."
    )
    demo_mode = st.checkbox("🧪 Run in Offline Demo Simulation Mode (No API Token needed)", value=True)
else:
    demo_mode = False
if not _IS_BG:
    BGS["has_token"] = bool(TOKEN) and not demo_mode

if SNAP.get("auth_tok") != TOKEN:          # token badla => purana 401 / auth error clear
    SNAP.pop("auth_error", None)
    SNAP.pop("live_auth_err", None)
    SNAP["auth_tok"] = TOKEN
if SNAP.get("auth_error") and TOKEN:
    st.error("🔒 Upstox 401 Unauthorized - token expire/galat hai (Upstox token roz expire hota hai). Naya token daalein.")

today_date = now_ist().date()
custom_earnings_map = load_custom_earnings()
LIVE_MKT = market_open()

col_btn1, col_btn2, col_btn3 = st.columns([2.2, 2.2, 2.6])
with col_btn1:
    if st.button(
        f"📉 {'[ACTIVE] ' if ss['only_low_vol_10'] else ''}Show Only < {max_monthly_move_th:.0f}% Monthly Mover Stocks",
        type="primary" if ss["only_low_vol_10"] else "secondary", use_container_width=True,
    ):
        ss["only_low_vol_10"] = not ss["only_low_vol_10"]
        st.rerun()
with col_btn2:
    if st.button("🔄 Show All F&O Stocks (Reset Filter)", use_container_width=True):
        ss["only_low_vol_10"] = False
        st.rerun()
with col_btn3:
    st.markdown(
        f"**Week:** `{get_week_of_month(today_date)} of {today_date.strftime('%B %Y')}` | "
        f"**Universe:** `{len(SYMBOLS)} stocks` | "
        f"**Market:** `{'OPEN 🟢' if LIVE_MKT else 'CLOSED 🔴 (last session data)'}`"
    )

# ---- Bundle + quotes ----
try:
    bundle = demo_bundle(SYMBOLS) if demo_mode else (PRE_BUNDLE or load_instrument_bundle(tuple(SYMBOLS), today_date.isoformat()))
except Exception as e:
    st.error(f"Instrument file load fail: {e}")
    bundle = {"eq": {}, "fut": {}, "lot_map": {}, "idx": {}}

eff_ttl = int(stock_ttl_base)
if not LIVE_MKT:
    eff_ttl = 600
elif api_calls_last(1800) > 1600:
    eff_ttl = int(stock_ttl_base) * 2
if LIVE_MKT:
    eff_ttl = max(eff_ttl, min(int(len(SYMBOLS) * 1.5), 240))   # v7.5: 218 stocks par 327s => data 5 min se purana (stale) ho jaata tha
idx_ttl = (45 if scan_all_idx else 20) if LIVE_MKT else 300

TWO_TIER = bool(two_tier)
_tt_sig = (universe_mode, len(SYMBOLS), bool(demo_mode))
if SNAP.get("tt_sig") != _tt_sig:
    for _k in ("rows_cache", "watch", "last_full"):
        SNAP.pop(_k, None)
    SNAP["tt_sig"] = _tt_sig
FULL_SCAN = (not TWO_TIER) or bool(force_full) or (SNAP.get("last_full") is None) \
    or (time.time() - SNAP["last_full"] >= int(full_scan_min) * 60)
if FULL_SCAN:
    SCAN_SYMS = list(SYMBOLS)
else:
    # Watchlist + currently open stock paper trades so their LTP/SL/Target stays updated
    _open_stk_syms = list(SNAP.get(f"stk_paper:{today_date.isoformat()}", {}).keys()) \
        + list(SNAP.get(f"stk_pb:{today_date.isoformat()}", {}).keys())          # v7.6: pending pullback wale bhi taaza rahein
    SCAN_SYMS = list(dict.fromkeys([s for s in (SNAP.get("watch", []) + _open_stk_syms) if s in SYMBOLS]))
    if LIVE_MKT:
        eff_ttl = max(15, int(refresh_sec) - 5)
idx_ttl_other = 120 if LIVE_MKT else 300

key_to_quote: dict = {}
if not demo_mode and TOKEN:
    all_keys = ([bundle["eq"][s] for s in SCAN_SYMS if s in bundle["eq"]]
                + [bundle["fut"][s] for s in SCAN_SYMS if s in bundle["fut"]] + [VIX_KEY])
    for _u in (list(INDEX_CATALOG) if scan_all_idx else [IDX_UND]):
        all_keys.append(INDEX_CATALOG[_u]["key"])
        _fk = (bundle["idx"].get(_u) or (None, 0))[0]
        if _fk:
            all_keys.append(_fk)
    quotes = fetch_batch_quotes(list(dict.fromkeys(all_keys)), TOKEN)
    for k, v in quotes.items():
        if isinstance(v, dict):
            ik = v.get("instrument_token") or v.get("instrument_key") or k
            key_to_quote[ik] = v
            key_to_quote[k] = v

C = {"tok": TOKEN, "demo": demo_mode, "live": LIVE_MKT, "eq": bundle["eq"], "fut": bundle["fut"],
     "exch": bundle.get("exch", {}), "lot": bundle["lot_map"], "q": key_to_quote, "ttl": eff_ttl}


def live_stock_inputs(s: str, ik: str, fk, c: dict) -> dict:
    tok = c["tok"]
    today_df = fetch_intraday(ik, tok, c["ttl"])
    prior = fetch_prior_1m(ik, tok)
    df1m = merge_1m(prior, today_df)                     # v7.8.1: ts dtype safe merge
    st_ = fetch_daily_stats(ik, tok)
    q = c["q"].get(ik) or {}
    ltp = safe_float(q.get("last_price")) or (safe_float(df1m["c"].iloc[-1]) if not df1m.empty else 0.0)
    prev = st_["prev_close"] or safe_float((q.get("ohlc") or {}).get("close")) or \
        ((ltp - safe_float(q.get("net_change"))) if ltp else 0.0) or ltp
    fq = c["q"].get(fk) or {} if fk else {}
    try:                                           # best bid/ask se spread % (depth na mile to NaN = check nahi lagega)
        dep = q.get("depth") or {}
        bid = safe_float(((dep.get("buy") or [{}])[0]).get("price"))
        ask = safe_float(((dep.get("sell") or [{}])[0]).get("price"))
    except Exception:
        bid = ask = 0.0
    spread = round((ask - bid) / ltp * 100.0, 3) if (bid > 0 and ask > 0 and ask >= bid and ltp > 0) else float("nan")
    return {"df1m": df1m, "ltp": ltp, "prev": prev, "atp": safe_float(q.get("average_price")),
            "oi": safe_float(fq.get("oi")), "fut_ltp": safe_float(fq.get("last_price")) or ltp,
            "move": st_["move"], "avg_rng": st_["avg_rng"], "spread_pct": spread}


def process_symbol(s: str, c: dict):
    ik = c["eq"].get(s)
    if not ik:
        return None
    fk = c["fut"].get(s)
    try:
        inp = demo_stock_inputs(s) if c["demo"] else live_stock_inputs(s, ik, fk, c)
        m = analyze_candles(inp["df1m"], inp["move"], live=c["live"] and not c["demo"], vwap_override=inp["atp"])
        ltp = inp["ltp"] or m["last_close"]
        oi_chg, px_chg, oi_ready = oi_track(s, inp["oi"], inp["fut_ltp"] or ltp, int(oi_window)) if inp["oi"] > 0 \
            else (0.0, 0.0, False)
        sc = score_stock_filters(ltp, inp["prev"], m, oi_chg, px_chg, oi_ready, float(adx_min))
        earn = resolve_earnings_status(s, custom_earnings_map, today_date, lock_mode, int(pre_days), int(post_days),
                                       lock_pattern)
        data_ok = bool(m["ok"] and ltp > 0)
        mv = inp["move"]
        try:                                       # correlation guard ke liye pichhle ~60 min ke 1-min log-returns
            if len(inp["df1m"]) > 30:
                _c1 = inp["df1m"][["ts", "c"]].tail(int(corr_window) + 1)
                _lr = np.log(_c1["c"].astype(float)).diff().dropna()
                SNAP.setdefault("ret1m", {})[s] = (_c1["ts"].iloc[1:].values, _lr.values)
        except Exception:
            pass
        try:                                       # candles DB me save karne ke liye buffer (main thread flush karega)
            if not c["demo"] and len(inp["df1m"]) > 0:
                _d1, _dayd = inp["df1m"], now_ist().date()
                _ck = f"candle_saved:{s}:{_dayd}"
                _first = _ck not in SNAP
                _tl = _d1[_d1["ts"].dt.date == _dayd] if _first else _d1.tail(130)
                if len(_tl):
                    SNAP.setdefault("candle_buf", {})[s] = (_tl[["ts", "o", "h", "l", "c", "v"]].copy(), _first)
                    SNAP[_ck] = True
        except Exception:
            pass
        return {
            "Symbol": s, "Exch": c["exch"].get(s, "NSE"), "Weight %": round(W.get(s, 1.0), 2), "LTP": round(ltp, 2), "Day %": sc["chg_pct"],
            "1M Move %": mv, f"Low Vol (<{max_monthly_move_th:.0f}%)": "✅ YES" if (0 < mv < max_monthly_move_th) else "❌ NO",
            "Avg Range Rs": inp["avg_rng"],
            "Result Date": earn["result_date"] or "-", "Result Week": earn["result_week"], "Date Source": earn["source"],
            "Result Trade Lock": earn["trade_status"], "Filter Score (-8..+8)": sc["net_score"],
            "5m EMA (9/21)": sc["ema5_sig"], "15m MTF": sc["mtf15_sig"], "VWAP Status": sc["vwap_sig"],
            "ORB (15m)": sc["orb_sig"], "RSI (14)": m["rsi"], "ADX (14)": m["adx"], "Vol Spike x": m["vol_spike"],
            "ATR (5m)": m["atr"], "F&O OI Buildup": sc["fut_buildup"], "OI Chg %": oi_chg if oi_ready else float("nan"),
            "Data Lag (min)": m["stale_min"],
            "15m Zone": sc["zone_txt"], "Zone Lo": m["z15_lo"] or float("nan"), "Zone Hi": m["z15_hi"] or float("nan"),
            "_zone": sc["in_zone"],
            "_lock": earn["is_result_week"], "_ok": data_ok, "_score": sc["net_score"], "_mtf": sc["mtf_d"],
            "_orb": sc["orb_d"], "_fut": sc["fut_d"], "_extL": sc["ext_long"], "_extS": sc["ext_short"],
            "_whyL": sc["why_long"], "_whyS": sc["why_short"],
            "_lot": c["lot"].get(s, 0),
            "_tdir": trend_dir(ltp, m), "_vwx": int(m.get("vwap_cross", 0) or 0),
            "Spread %": inp.get("spread_pct", float("nan")),
            "VWAP": round(float(m.get("vwap") or 0.0), 2) or float("nan"), "ATR (15m)": float(m.get("atr15") or 0.0),
        }
    except Exception as e:
        ERR_LOG.append((now_ist().strftime("%H:%M:%S"), -1, f"process {s}", str(e)[:140]))
        return None


# ---- Index context ----
def build_index_context(c: dict, und: str = None) -> dict:
    und = und or IDX_UND
    idx_key = INDEX_CATALOG[und]["key"]
    fk, lot = bundle["idx"].get(und, (None, FALLBACK_LOTS.get(und, 1)))
    ctx = {"ok": False, "spot": 0.0, "prev": 0.0, "chg_pct": 0.0, "lot": lot, "atr": 0.0, "adx": 0.0, "rsi": 50.0,
           "trend_dir": 0, "mtf_dir": 0, "orb_dir": 0, "fut_dir": 0, "fut_text": "N/A", "vix": 0.0, "vix_chg": 0.0,
           "pcr": None, "pcr_oi_chg": None, "pcr_delta": None, "max_pain": None, "call_wall": None, "put_wall": None,
           "walls_c": [], "walls_p": [], "gex_ratio": None, "gex_text": "N/A", "m": dict(EMPTY_M), "expiry": "",
           "orb_ready": False, "stale_min": 0.0, "src": "-",
           "zone": False, "zone_txt": "-", "z_hi": 0.0, "z_lo": 0.0, "z_rng": 0.0}
    try:
        if c["demo"]:
            seed = zlib.crc32(und.encode())
            base = DEMO_BASE.get(und, 20000.0)
            df = synth_candles(seed, base, drift=demo_mkt_drift(), vol_scale=0.6)
            last_d = df["ts"].dt.date.max()
            prev = float(df[df["ts"].dt.date < last_d]["c"].iloc[-1])
            spot = fut_ltp = float(df["c"].iloc[-1])
            atp, oi, vix, vix_chg = 0.0, 1.2e7 * (1 + 0.01 * math.sin(time.time() / 300.0)), 14.8, -1.2
            chain = {"rows": demo_chain_rows(spot, INDEX_CATALOG[und]["step"]), "expiry": "DEMO"}
            ctx["src"] = "DEMO FUT"
        else:
            tok = c["tok"]
            spot_q = c["q"].get(idx_key) or {}
            spot = safe_float(spot_q.get("last_price"))
            src_key = fk if fk else idx_key
            ctx["src"] = "INDEX FUT" if fk else "INDEX SPOT (no volume)"
            today_df = fetch_intraday(src_key, tok, idx_ttl if und == IDX_UND else idx_ttl_other)
            prior = fetch_prior_1m(src_key, tok)
            df = merge_1m(prior, today_df)                   # v7.8.1: ts dtype safe merge (index ctx .dt error fix)
            fq = c["q"].get(fk) or {} if fk else {}
            fut_ltp = safe_float(fq.get("last_price")) or (safe_float(df["c"].iloc[-1]) if not df.empty else 0.0)
            spot = spot or fut_ltp
            atp, oi = safe_float(fq.get("average_price")), safe_float(fq.get("oi"))
            dstats = fetch_daily_stats(idx_key, tok)
            prev = dstats["prev_close"] or safe_float((spot_q.get("ohlc") or {}).get("close")) or spot
            vq = c["q"].get(VIX_KEY) or {}
            vix = safe_float(vq.get("last_price"))
            vprev = vix - safe_float(vq.get("net_change"))
            vix_chg = (vix - vprev) / vprev * 100.0 if vprev > 0 else 0.0
            chain = fetch_chain_rows(idx_key, tok, 60 if und == IDX_UND else 180) if spot > 0 else {"rows": [], "expiry": ""}

        m = analyze_candles(df, 0.0, live=c["live"] and not c["demo"], vwap_override=atp)
        trend_px = fut_ltp if fut_ltp else spot
        ctx.update({"ok": bool(m["ok"] and spot > 0), "spot": round(spot, 2), "prev": round(prev, 2),
                    "chg_pct": round((spot - prev) / prev * 100.0, 2) if prev > 0 else 0.0,
                    "atr": m["atr"], "adx": m["adx"], "rsi": m["rsi"], "m": m, "vix": round(vix, 2),
                    "vix_chg": round(vix_chg, 2), "orb_ready": m["orb_ready"], "stale_min": m["stale_min"]})
        ctx["trend_dir"] = trend_dir(trend_px, m)
        ctx["zone_txt"], ctx["zone"] = zone_state(trend_px, m)
        ctx["z_hi"], ctx["z_lo"], ctx["z_rng"] = m["z15_hi"], m["z15_lo"], m["z15_rng_atr"]
        if m["ok"] and m["ema9_15m"] > 0 and m["ema21_15m"] > 0:
            ctx["mtf_dir"] = 1 if m["ema9_15m"] > m["ema21_15m"] else (-1 if m["ema9_15m"] < m["ema21_15m"] else 0)
        if m["ok"] and m["orb_ready"]:
            ctx["orb_dir"] = 1 if trend_px > m["orh"] else (-1 if trend_px < m["orl"] else 0)
        if oi > 0:
            o_chg, p_chg, ready = oi_track(f"IDX_{und}", oi, trend_px, int(oi_window))
            o_t, p_t = max(oi_th * 0.5, 0.1), max(px_th * 0.5, 0.04)
            if not ready:
                ctx["fut_text"] = "BUILDING BASELINE ⏳"
            elif o_chg > o_t and p_chg > p_t:
                ctx["fut_dir"], ctx["fut_text"] = 1, "LONG BUILDUP 🟢"
            elif o_chg > o_t and p_chg < -p_t:
                ctx["fut_dir"], ctx["fut_text"] = -1, "SHORT BUILDUP 🔴"
            elif o_chg < -o_t and p_chg > p_t:
                ctx["fut_text"] = "SHORT COVERING ⬆"
            elif o_chg < -o_t and p_chg < -p_t:
                ctx["fut_text"] = "LONG UNWINDING ⬇"
            else:
                ctx["fut_text"] = "NEUTRAL"
        ch = analyze_chain(chain.get("rows"), spot)
        if ch:
            ctx.update({k: ch.get(k) for k in ("pcr", "pcr_oi_chg", "max_pain", "call_wall", "put_wall",
                                               "walls_c", "walls_p", "gex_ratio", "gex_text")})
            ctx["expiry"] = chain.get("expiry", "")
            if ch.get("pcr"):
                with SNAP_LOCK:
                    dq = SNAP.setdefault(f"pcr_hist:{und}", deque(maxlen=600))
                    if not dq or time.time() - dq[-1][0] >= 20:
                        dq.append((time.time(), ch["pcr"]))
                    tgt = time.time() - int(oi_window) * 60
                    old = [p for t, p in dq if t <= tgt]
                    if old:
                        ctx["pcr_delta"] = round(ch["pcr"] - old[-1], 2)
    except Exception as e:
        ERR_LOG.append((now_ist().strftime("%H:%M:%S"), -1, "index ctx", str(e)[:140]))
    return ctx


with st.spinner("Live data aur indicators calculate ho rahe hain..."):
    ictx = build_index_context(C, IDX_UND)
    with ThreadPoolExecutor(max_workers=8) as ex:
        res_list = list(ex.map(lambda s: process_symbol(s, C), SCAN_SYMS))
        IDX_CTX = {IDX_UND: ictx}
        _others = [u for u in INDEX_CATALOG if u != IDX_UND] if scan_all_idx else \
            ([u for u in ("NIFTY", "BANKNIFTY") if u != IDX_UND] if idx_dir_gate else [])     # v7.9: index direction gate
        for _u, _cx in zip(_others, ex.map(lambda u: build_index_context(C, u), _others)):
            IDX_CTX[_u] = _cx
log_pcr_hist(ictx, IDX_UND)
flush_candles()
rows = [r for r in res_list if r is not None]
if TWO_TIER:
    _cache = SNAP.setdefault("rows_cache", {})
    _fresh = {r["Symbol"] for r in rows}
    for r in rows:
        _cache[r["Symbol"]] = r
    _age = int((time.time() - (SNAP.get("last_full") or time.time())) / 60)
    _merged = []
    for s in SYMBOLS:
        rr = _cache.get(s)
        if rr is None:
            continue
        rr = dict(rr)
        if FULL_SCAN:
            rr["Scan"] = "FULL"
        elif s in _fresh:
            rr["Scan"] = f"WATCH {int(refresh_sec)}s"
        else:
            rr["Scan"] = f"full-scan {_age}m ago"
        _merged.append(rr)
    rows = _merged
df_all = pd.DataFrame(rows)


# ---- Final action, SL/TGT, sizing, rank ----
STOCK_PCR_BLOCK_TXT = "🟠 NO TRADE (stock PCR neutral/against)"


def _spcr_info_from_rows(rows: list, spot: float, lot: int = 0):
    """Option chain rows se near-ATM (spot ± spcr_range %) PCR, change-in-OI PCR aur total OI (LOTS me)."""
    recs = []
    for r in rows or []:
        try:
            k = float(r.get("strike_price"))
            cm = ((r.get("call_options") or {}).get("market_data")) or {}
            pm = ((r.get("put_options") or {}).get("market_data")) or {}
            recs.append((k, safe_float(cm.get("oi")), safe_float(cm.get("prev_oi")), safe_float(pm.get("oi")), safe_float(pm.get("prev_oi"))))
        except Exception:
            continue
    if not recs or spot <= 0:
        return None
    d = pd.DataFrame(recs, columns=["k", "coi", "cprev", "poi", "pprev"])
    w = float(spcr_range) / 100.0 * spot
    near = d[(d["k"] >= spot - w) & (d["k"] <= spot + w)]
    c_sum, p_sum = float(near["coi"].sum()), float(near["poi"].sum())
    if c_sum <= 0:
        return None
    # OI ki unit: agar zyadatar OI lot size ke guna ho to Upstox shares me de raha hai => lots me badlo
    scale = 1.0
    if lot and lot > 1:
        vals = np.concatenate([near["coi"].values, near["poi"].values])
        vals = vals[vals > 0]
        if len(vals) and float((np.mod(vals, lot) == 0).mean()) >= 0.8:
            scale = 1.0 / lot
    tot = (c_sum + p_sum) * scale
    mo = float(spcr_min_oi)
    low = bool(mo > 0 and (tot < mo or c_sum * scale < mo * 0.1 or p_sum * scale < mo * 0.1))
    d_c = float((near["coi"] - near["cprev"]).sum())
    d_p = float((near["poi"] - near["pprev"]).sum())
    has_prev = float(near["cprev"].sum()) > 0 or float(near["pprev"].sum()) > 0     # prev_oi na ho to dOI jhootha (= poora OI) banta
    chg = None
    if has_prev:
        if d_c > max(1.0, 0.01 * c_sum):
            chg = round(d_p / d_c, 3)           # d_p negative (puts unwind) ho to ratio negative = bearish
        elif d_c <= 0 and d_p > 0:
            chg = 99.0                          # calls ghat rahe + puts badh rahe = bahut bullish
        elif d_c > 0 and d_p <= 0:
            chg = 0.0                           # calls ki nayi OI chhoti par puts ghat rahe = bearish
        # dono taraf OI ghat rahi (ya koi badlav nahi) => None: koi spasht dOI signal nahi
    c_prev, p_prev = float(near["cprev"].sum()), float(near["pprev"].sum())
    prev_pcr = round(p_prev / c_prev, 3) if (c_prev > 0 and p_prev > 0) else None      # v7.5: pichhle din (prev_oi) ka PCR
    return {"pcr": round(p_sum / c_sum, 3), "chg_pcr": chg, "tot_oi": tot, "low_oi": low, "prev_pcr": prev_pcr,
            "d_c": (d_c * scale) if has_prev else None, "d_p": (d_p * scale) if has_prev else None}


def _spcr_from_rows(rows: list, spot: float, lot: int = 0):
    """PCR = near-ATM put OI / call OI. Option OI kam (illiquid) ho to None (bharosemand nahi)."""
    info = _spcr_info_from_rows(rows, spot, lot)
    return None if info is None or info["low_oi"] else info["pcr"]


def demo_stock_pcr(sym: str) -> float:
    h = (zlib.crc32(sym.encode()) % 1000) / 1000.0
    return round(0.55 + 0.95 * h + 0.08 * math.sin(time.time() / 900.0 + h * 6.28), 3)


def get_stock_pcr(sym: str, ik: str, spot: float, tok: str, demo: bool) -> tuple:
    """(PCR, 10-min delta). 120 sec cache; har value DB (pcr_hist) me save - Backtest ke kaam aati hai."""
    now_t = time.time()
    c = SNAP.get(f"spcr:{sym}")
    if c and now_t - c[0] < 120:
        return c[1], SNAP.get(f"spcr_d:{sym}")
    info = None
    try:
        if demo:
            pcr = demo_stock_pcr(sym)
            h = (zlib.crc32(sym.encode()) % 1000) / 1000.0
            _dp = 500.0 * math.sin(time.time() / 800.0 + h * 6.28)
            info = {"pcr": pcr, "chg_pcr": round(pcr + 0.15 * math.sin(time.time() / 700.0 + h * 6.28), 3), "tot_oi": 1e6, "low_oi": False,
                    "prev_pcr": round(pcr - 0.05 * math.sin(time.time() / 900.0 + h * 6.28), 3), "d_p": _dp, "d_c": -_dp}
        else:
            info = _spcr_info_from_rows(fetch_chain_rows(ik, tok, 120).get("rows"), spot, int(C["lot"].get(sym, 0) or 0))
            pcr = None if info is None or info["low_oi"] else info["pcr"]
    except Exception as e:
        pcr = None
        try:
            ERR_LOG.append((now_ist().strftime("%H:%M:%S"), -1, f"stock-pcr {sym}", str(e)[:120]))
        except Exception:
            pass
    SNAP[f"spcr_try:{sym}"] = now_t
    SNAP[f"spcr_info:{sym}"] = info
    if pcr is None:
        if info is not None and info["low_oi"]:        # illiquid: purani value mat do, aur 120 sec dobara compute bhi mat karo
            SNAP[f"spcr:{sym}"] = (now_t, None)
            SNAP.pop(f"spcr_d:{sym}", None)
            return None, None
        return (c[1] if c and now_t - c[0] < 600 else None), SNAP.get(f"spcr_d:{sym}")
    dq = SNAP.setdefault(f"spcr_h:{sym}", deque(maxlen=200))
    dq.append((now_t, pcr))
    base = None
    for t_, p_ in dq:
        if now_t - t_ >= 600:
            base = p_
    if base is None and dq and now_t - dq[0][0] >= 300:
        base = dq[0][1]
    delta = round(pcr - base, 3) if base is not None else None
    SNAP[f"spcr:{sym}"], SNAP[f"spcr_d:{sym}"] = (now_t, pcr), delta
    log_pcr_hist({"pcr": pcr, "pcr_delta": delta}, sym)
    return pcr, delta


def _spcr_base_stats(vals: list):
    """Pichhle din ke daily PCR values -> (average, neutral band, din). Kam din ho to None."""
    vals = [float(v) for v in vals if v is not None and float(v) > 0]
    if len(vals) < min(int(spcr_min_days), int(spcr_days)):
        return None
    arr = np.array(vals[-int(spcr_days):], dtype=float)
    sd = float(arr.std(ddof=1)) if len(arr) > 1 else 0.0
    return round(float(arr.mean()), 3), round(max(float(spcr_k) * sd, float(spcr_min_band)), 3), len(arr)


def spcr_baseline(sym: str):
    """Is stock ka (pichhle N din ka average PCR, neutral band, din). Aaj ka din shamil nahi (look-ahead nahi)."""
    day = now_ist().strftime("%Y-%m-%d")
    key = f"spcr_base:{sym}:{day}"
    if key in SNAP:
        return SNAP[key]
    if demo_mode:
        h = (zlib.crc32(sym.encode()) % 1000) / 1000.0
        res = (round(0.55 + 0.95 * h, 3), max(0.5 * 0.08, float(spcr_min_band)), 20)
    else:
        try:
            with db() as conn:
                rows = conn.execute("SELECT pcr FROM pcr_daily WHERE sym = ? AND dt < ? ORDER BY dt DESC LIMIT ?",
                                    (sym, day, int(spcr_days))).fetchall()
            SNAP[f"spcr_cnt:{sym}:{day}"] = len(rows)
            res = _spcr_base_stats([r[0] for r in reversed(rows)])
        except Exception:
            res = None
    SNAP[key] = res
    return res


def collect_daily_pcr(day: str) -> None:
    """Roz 15:35 ke baad: universe ke stocks ka PCR ek baar save (baseline ke liye). Signal-wale stocks tak seemit nahi (bias nahi)."""
    if demo_mode or not use_stock_pcr or now_ist().time() < dtime(15, 35) or not TOKEN:
        return
    if kv_get(f"pcr_daily:{day}"):
        return
    tries = SNAP.get("pcr_daily_tries", 0)
    if tries >= 3:
        return
    SNAP["pcr_daily_tries"] = tries + 1
    try:
        syms = sorted(SYMBOLS, key=lambda z: -W.get(z, 0.0))          # v7.5: sab stocks (pehle top 80) - har stock ka baseline bane
        ltps = {}
        try:
            ltps = dict(zip(df_all["Symbol"], df_all["LTP"]))
        except Exception:
            pass

        def job(sy):
            ik, spot = C["eq"].get(sy), float(ltps.get(sy) or 0.0)
            if not ik or spot <= 0:
                return sy, None
            return sy, _spcr_from_rows(fetch_chain_rows(ik, TOKEN, 0).get("rows"), spot, int(C["lot"].get(sy, 0) or 0))

        with ThreadPoolExecutor(max_workers=6) as ex:
            res = [(sy, p) for sy, p in ex.map(job, syms) if p is not None]
        if res:
            with db() as conn:
                conn.executemany("INSERT OR REPLACE INTO pcr_daily (dt, sym, pcr) VALUES (?,?,?)", [(day, sy, float(p)) for sy, p in res])
            kv_set(f"pcr_daily:{day}", len(res))
            with db() as conn:
                nd_ = int(conn.execute("SELECT COUNT(DISTINCT dt) FROM pcr_daily").fetchone()[0] or 0)
            audit("PCR SNAPSHOT", "", "", f"{len(res)}/{len(syms)} stocks ka daily PCR save | history {nd_} din")
            need_ = min(int(spcr_min_days), int(spcr_days))
            send_telegram(f"📸 Daily stock PCR snapshot {day}: {len(res)}/{len(syms)} stocks | history {nd_}/{need_} din - "
                          + ("adaptive zone ON" if nd_ >= need_ else ("abhi ab-tak-ke-din average rule" if spcr_prevday else "abhi Fixed rule")))
    except Exception as e:
        ERR_LOG.append((now_ist().strftime("%H:%M:%S"), -1, "pcr snapshot", str(e)[:140]))


def pcr_running_avg(sym: str):
    """v7.5: DB (pcr_daily) me jitne din ka is stock ka PCR jama hai (aaj shamil nahi, max spcr_days) unka average.
    Returns (average, din) ya (None, 0)."""
    if not sym:
        return None, 0
    day = now_ist().strftime("%Y-%m-%d")
    key = f"spcr_runavg:{sym}:{day}"
    if key in SNAP:
        return SNAP[key]
    res = (None, 0)
    try:
        with db() as conn:
            rows = conn.execute("SELECT pcr FROM pcr_daily WHERE sym = ? AND dt < ? ORDER BY dt DESC LIMIT ?",
                                (sym, day, int(spcr_days))).fetchall()
        vals = [float(r[0]) for r in rows if r and r[0] and float(r[0]) > 0]
        if vals:
            res = (round(float(np.mean(vals)), 3), len(vals))
    except Exception:
        res = (None, 0)
    SNAP[key] = res
    return res


def pcr_base_for(sym: str, info=None):
    """Baseline jo trade decision me lagti hai: DB ke ab tak ke din ka average; DB khaali ho to option chain ka
    pichhle din (prev OI) wala PCR (= 1 din). Returns (base, din, source) ya (None, 0, "")."""
    avg, n = pcr_running_avg(sym)
    if avg is not None:
        return avg, n, f"{n} din avg"
    prev = (info or {}).get("prev_pcr")
    if prev is not None:
        return float(prev), 1, "pichhle din (prev OI)"
    return None, 0, ""


def oi_writing_label(info) -> str:
    """Aaj ki nayi OI (OI - prev OI) se: PUT WRITING / CALL WRITING / '-' ."""
    if not info:
        return "-"
    d_c, d_p = info.get("d_c"), info.get("d_p")
    if d_c is None or d_p is None:
        return "-"
    if d_p > 0 and d_p > max(d_c, 0.0):
        return "PUT WRITING 🟢"
    if d_c > 0 and d_c > max(d_p, 0.0):
        return "CALL WRITING 🔴"
    return "-"


def _prevday_pcr_decision(side: int, pcr, info=None, sym: str = "", have_days=None) -> tuple:
    """v7.5: 20 din ka baseline banne tak - jitne din ka PCR jama hai unka AVERAGE = baseline.
    PCR > baseline => LONG, PCR < baseline => SHORT. (Option: saath me aaj put/call writing bhi confirm.)
    Baseline bilkul na ho to (None, ...) => caller Fixed limit lagata hai."""
    info = info or {}
    base, n, src = pcr_base_for(sym, info)
    need_ = min(int(spcr_min_days), int(spcr_days))
    if base is None:
        return None, f"[PCR history 0/{need_} din - baseline nahi]"
    lab = f"[PCR history {n}/{need_} din - baseline {base:.2f} ({src})]"
    if side == 1 and pcr <= base:
        return False, f"stock PCR {pcr:.2f} baseline {base:.2f} se upar nahi - LONG nahi {lab}"
    if side == -1 and pcr >= base:
        return False, f"stock PCR {pcr:.2f} baseline {base:.2f} se neeche nahi - SHORT nahi {lab}"
    if spcr_writing_on and info.get("d_c") is not None and info.get("d_p") is not None:
        w = oi_writing_label(info)
        if side == 1 and not w.startswith("PUT"):
            return False, f"PCR baseline se upar par PUT WRITING nahi ({w if w != '-' else 'spasht writing nahi'}) {lab}"
        if side == -1 and not w.startswith("CALL"):
            return False, f"PCR baseline se neeche par CALL WRITING nahi ({w if w != '-' else 'spasht writing nahi'}) {lab}"
    return True, lab


def stock_pcr_decision(side: int, pcr, delta, base=None, have_days=None, chg_pcr=None, why_none: str = "", chg_check: bool = True,
                       info=None, sym: str = "") -> tuple:
    """Adaptive: LONG tab jab PCR > avg+band, SHORT tab jab PCR < avg-band, beech me neutral = trade nahi.
    Fixed: LONG > spcr_long, SHORT < spcr_short. History kam ho to fallback (agar ON)."""
    if pcr is None:
        return (not bool(spcr_need)), (why_none or "stock PCR data nahi mila")
    if spcr_adaptive and base:
        avg, band, nd = base
        hi, lo = avg + band, avg - band
        lab = f"[{nd}-din avg {avg:.2f} +- {band:.2f}]"
    elif spcr_adaptive and not spcr_fallback:
        return (not bool(spcr_need)), "stock PCR baseline history kam hai"
    elif spcr_adaptive and spcr_prevday and (info is not None or sym):
        ok_p, why_p = _prevday_pcr_decision(side, pcr, info, sym, have_days)
        if ok_p is not None:
            if not ok_p:
                return False, why_p
            if spcr_trend and delta is not None and ((side == 1 and delta < 0) or (side == -1 and delta > 0)):
                return False, f"stock PCR {pcr:.2f} {'gir' if side == 1 else 'badh'} raha ({delta:+.2f}) - {'LONG' if side == 1 else 'SHORT'} ke khilaaf {why_p}"
            return True, why_p
        hi, lo = float(spcr_long), float(spcr_short)                 # pichhle din ka data nahi => Fixed limit
        lab = why_p.replace("]", " - fixed limit]")
    else:
        hi, lo = float(spcr_long), float(spcr_short)
        need_ = min(int(spcr_min_days), int(spcr_days))
        lab = "[fixed limit]" if not spcr_adaptive else (
            f"[PCR history {have_days}/{need_} din - abhi fixed limit]" if have_days is not None else "[history kam - fixed limit]")
    if side == 1:
        if pcr <= hi:
            zone = "neutral zone" if pcr >= lo else "bearish zone (SHORT ke liye)"
            return False, f"stock PCR {pcr:.2f} {zone}: LONG ke liye {hi:.2f} se upar chahiye {lab}"
        if spcr_trend and delta is not None and delta < 0:
            return False, f"stock PCR {pcr:.2f} gir raha ({delta:+.2f}) - LONG ke liye PCR ghatna nahi chahiye {lab}"
    else:
        if pcr >= lo:
            zone = "neutral zone" if pcr <= hi else "bullish zone (LONG ke liye)"
            return False, f"stock PCR {pcr:.2f} {zone}: SHORT ke liye {lo:.2f} se neeche chahiye {lab}"
        if spcr_trend and delta is not None and delta > 0:
            return False, f"stock PCR {pcr:.2f} badh raha ({delta:+.2f}) - SHORT ke liye PCR badhna nahi chahiye {lab}"
    if spcr_chg_confirm and chg_check and chg_pcr is None:
        return False, f"ΔOI PCR confirm nahi ho paaya (nayi OI me spasht put/call badhat nahi, ya prev OI nahi) {lab}"
    if spcr_chg_confirm and chg_pcr is not None:
        if side == 1 and chg_pcr <= 1.0:
            return False, f"ΔOI PCR {chg_pcr:.2f} <= 1.0: nayi call-writing put-writing se zyada (LONG ke khilaaf) {lab}"
        if side == -1 and chg_pcr >= 1.0:
            return False, f"ΔOI PCR {chg_pcr:.2f} >= 1.0: nayi put-writing call-writing se zyada (SHORT ke khilaaf) {lab}"
    return True, ""


def _pcr_status(sym: str, exch: str, ik, info, pcr) -> str:
    if str(exch).upper() == "BSE":
        return "BSE (option chain nahi)"
    if not ik:
        return "instrument key nahi"
    if pcr is not None:
        return "OK"
    if info and info.get("low_oi"):
        return "low OI (illiquid)"
    if info is None and SNAP.get(f"spcr_try:{sym}"):
        return "data nahi (ERR_LOG dekho)"
    return "baari aane do"


def apply_stock_pcr(df: pd.DataFrame) -> pd.DataFrame:
    """finalize_actions ke baad.
    (a) Filter: sirf STRONG candidates (top 25) par stock PCR check - pehle jaisa.
    (b) v7.4 Display: baaki stocks ka PCR bhi - har refresh me spcr_batch stocks round-robin, baaki cache se."""
    df = df.copy()
    for c_ in ("Stock PCR", "PCR Δ(10m)", "PCR 20d avg", "PCR band ±", "ΔOI PCR", "PCR total OI (lots)", "PCR base (avg)", "Base din"):
        df[c_] = float("nan")
    df["PCR Status"] = ""
    df["OI Writing"] = "-"
    if df.empty or "Final Action" not in df.columns:
        return df
    decide = bool(pcr_filter_on and use_stock_pcr)
    if not decide and not spcr_show_all:
        return df
    acts, routes = df["Final Action"].tolist(), df["Entry Route"].tolist()
    syms = df["Symbol"].tolist()
    ltps = df["LTP"].tolist()
    exchs = df["Exch"].tolist() if "Exch" in df.columns else ["NSE"] * len(df)
    n = len(df)
    now_t = time.time()

    def _has_opt(i):
        return str(exchs[i]).upper() != "BSE" and bool(C["eq"].get(syms[i])) and safe_float(ltps[i]) > 0

    strong = []
    if decide:
        strong = [i for i, a in enumerate(acts) if str(a).startswith(("🟢 STRONG", "🔻 STRONG"))]
        strong = sorted(strong, key=lambda i: -(df["Rank"].iloc[i] if pd.notna(df["Rank"].iloc[i]) else -9))[:25]
    ext_i = []
    if decide and pb_on and pb_ext:                 # v7.6.1: pullback candidates (EXTENDED) ka bhi PCR check
        _pbb = df["_pb_block"].tolist() if "_pb_block" in df.columns else [""] * n
        ext_i = [i for i, a in enumerate(acts) if str(a).startswith(("🟡 BUY (EXTENDED", "🟡 SELL (EXTENDED")) and not _pbb[i]]
        ext_i = sorted(ext_i, key=lambda i: -(df["Rank"].iloc[i] if pd.notna(df["Rank"].iloc[i]) else -9))[:25]
    disp = []
    if spcr_show_all:
        rest = [i for i in range(n) if i not in set(strong) and i not in set(ext_i) and _has_opt(i)]
        # jiska PCR sabse purana (ya kabhi nahi liya) - pehle uski baari
        rest.sort(key=lambda i: SNAP.get(f"spcr_try:{syms[i]}", 0.0))
        disp = rest[:int(spcr_batch)]
    fetch_idx = strong + ext_i + disp

    def job(i):
        return i, get_stock_pcr(syms[i], C["eq"].get(syms[i]), float(ltps[i]), TOKEN, bool(demo_mode)), spcr_baseline(syms[i])

    res = []
    if fetch_idx:
        with ThreadPoolExecutor(max_workers=6) as ex:
            res = list(ex.map(job, fetch_idx))
    got = {i: (pd_, base) for i, pd_, base in res}

    pcrs, dels, avgs, bands, chgs, tots = ([float("nan")] * n for _ in range(6))
    stats = [""] * n
    prevs, writes, bdays = [float("nan")] * n, ["-"] * n, [float("nan")] * n
    today_s = now_ist().strftime("%Y-%m-%d")
    for i in range(n):
        sym = syms[i]
        if i in got:
            (pcr, d_), base = got[i]
        else:                                   # is refresh me baari nahi aayi: cache (10 min tak) se dikhao
            c = SNAP.get(f"spcr:{sym}")
            pcr = c[1] if c and now_t - c[0] < 600 else None
            d_ = SNAP.get(f"spcr_d:{sym}") if pcr is not None else None
            base = spcr_baseline(sym) if pcr is not None else None
        info = SNAP.get(f"spcr_info:{sym}") or {}
        pcrs[i] = float("nan") if pcr is None else pcr
        dels[i] = float("nan") if d_ is None else d_
        chg = info.get("chg_pcr")
        chgs[i] = float("nan") if chg is None else chg
        tots[i] = float(info.get("tot_oi", float("nan")))
        _pv, _pn, _ = pcr_base_for(sym, info) if pcr is not None else (None, 0, "")
        if base:                                   # 20 din poore: adaptive avg hi baseline
            _pv, _pn = base[0], base[2]
        prevs[i] = float("nan") if _pv is None else float(_pv)
        bdays[i] = float(_pn) if _pv is not None else float("nan")
        writes[i] = oi_writing_label(info) if pcr is not None else "-"
        if base:
            avgs[i], bands[i] = base[0], base[1]
        stats[i] = _pcr_status(sym, exchs[i], C["eq"].get(sym), SNAP.get(f"spcr_info:{sym}"), pcr) if (i in got or spcr_show_all) else ""

    if decide:
        done = set()
        for i in strong:
            done.add(i)
            (pcr, d_), base = got[i]
            info = SNAP.get(f"spcr_info:{syms[i]}") or {}
            why_none = (f"stock option OI kam ({info.get('tot_oi', 0):,.0f} lots < {int(spcr_min_oi):,}) - PCR bharosemand nahi"
                        if info.get("low_oi") else "")
            side = 1 if str(acts[i]).startswith("🟢") else -1
            have = SNAP.get(f"spcr_cnt:{syms[i]}:{today_s}")
            ok, why = stock_pcr_decision(side, pcr, d_, base, have, info.get("chg_pcr"), why_none, True, info, syms[i])
            if ok:
                routes[i] = (f"STOCK PCR OK ({pcr:.2f}) " + (why if why else ("" if base else "[fixed limit]"))) if pcr is not None else "STOCK PCR (data nahi - allowed)"
            else:
                acts[i], routes[i] = STOCK_PCR_BLOCK_TXT, f"BLOCKED: {why}"
        for i, a in enumerate(acts):           # 25 se zyada candidates me jinka PCR check nahi hua
            if i not in done and str(a).startswith(("🟢 STRONG", "🔻 STRONG")):
                acts[i], routes[i] = STOCK_PCR_BLOCK_TXT, "BLOCKED: stock PCR check nahi hua (limit)"
        df["Final Action"], df["Entry Route"] = acts, routes
    pbp = ["" if not decide else "PCR check nahi hua"] * n   # v7.6.1: '' = pullback ke liye PCR theek
    for i in ext_i:
        (pcr, d_), base = got[i]
        info = SNAP.get(f"spcr_info:{syms[i]}") or {}
        why_none = (f"stock option OI kam ({info.get('tot_oi', 0):,.0f} lots)" if info.get("low_oi") else "")
        side = 1 if "BUY" in str(acts[i]) else -1
        ok, why = stock_pcr_decision(side, pcr, d_, base, SNAP.get(f"spcr_cnt:{syms[i]}:{today_s}"), info.get("chg_pcr"),
                                     why_none, True, info, syms[i])
        pbp[i] = "" if ok else (why or "PCR ke khilaaf")
    df["_pb_pcr"] = pbp
    df["Stock PCR"], df["PCR Δ(10m)"], df["PCR 20d avg"], df["PCR band ±"] = pcrs, dels, avgs, bands
    df["ΔOI PCR"], df["PCR total OI (lots)"] = chgs, tots
    df["PCR base (avg)"], df["Base din"], df["OI Writing"] = prevs, bdays, writes
    df["PCR Status"] = stats
    return df


SPREAD_BLOCK_TXT = "🟠 NO TRADE (spread zyada)"


def apply_spread_guard(df: pd.DataFrame) -> pd.DataFrame:
    """STRONG signal par bid-ask spread (% of LTP) limit se zyada ho to entry nahi. Depth na ho to check nahi lagta."""
    if df.empty or not spread_guard_on or "Final Action" not in df.columns or "Spread %" not in df.columns:
        return df
    df = df.copy()
    acts, routes = df["Final Action"].tolist(), df["Entry Route"].tolist()
    for i, (a_, sp) in enumerate(zip(acts, df["Spread %"].tolist())):
        if str(a_).startswith(("🟢 STRONG", "🔻 STRONG")) and pd.notna(sp) and float(sp) > float(max_spread_pct):
            acts[i], routes[i] = SPREAD_BLOCK_TXT, f"BLOCKED: bid-ask spread {float(sp):.2f}% > {float(max_spread_pct):.2f}% (illiquid / slippage ka khatra)"
    df["Final Action"], df["Entry Route"] = acts, routes
    return df


def pcr_route(ic: dict, side: int) -> tuple:
    """Normal route: LONG => PCR >= pcr_long_min, SHORT => PCR <= pcr_short_max, aur PCR 'stable' (ulta na khisak raha ho)."""
    pcr = ic.get("pcr")
    if pcr is None:
        return False, "PCR available nahi"
    d = ic.get("pcr_delta")
    if side == 1:
        if pcr < float(pcr_long_min):
            return False, f"PCR {pcr:.2f} < {float(pcr_long_min):.2f}"
        if d is not None and d < -float(pcr_stab):
            return False, f"PCR gir raha ({d:+.2f})"
    else:
        if pcr > float(pcr_short_max):
            return False, f"PCR {pcr:.2f} > {float(pcr_short_max):.2f}"
        if d is not None and d > float(pcr_stab):
            return False, f"PCR chadh raha ({d:+.2f})"
    return True, ""


def is_solo_outperformer(r: dict, side: int, rs_raw: float) -> tuple:
    """7 kadi shartein. Sab pass => PCR favour me na ho tab bhi entry allowed (Solo Mover Override)."""
    fails = []
    if abs(r["_score"]) < int(solo_min_score):
        fails.append("score")
    if rs_raw * side < float(solo_rs):
        fails.append("RS vs index")
    if r["_mtf"] != side:
        fails.append("15m MTF")
    if solo_need_orb and r["_orb"] != side:
        fails.append("ORB")
    if r["Vol Spike x"] < float(solo_vol):
        fails.append("volume")
    if r["ADX (14)"] < float(solo_adx):
        fails.append("ADX")
    if solo_need_oi and r["_fut"] != side:
        fails.append("OI buildup")
    return (not fails), fails


def market_chop_state(ic: dict) -> tuple:
    """Index ke haal se market 'choppy' hai ya nahi. Choppy = naye stock trade band (NO TRADE ZONE)."""
    if not chop_filter:
        return False, []
    if not ic.get("ok"):
        return True, ["Index data nahi aaya - market ka haal verify nahi ho sakta"]
    m = ic.get("m") or {}
    why = []
    if ic.get("zone"):
        why.append(f"Index 15m consolidation ({ic.get('z_lo', 0):.0f}-{ic.get('z_hi', 0):.0f})")
    if m.get("vwap_cross", 0) >= int(chop_cross):
        why.append(f"Index VWAP ko 1 ghante me {m['vwap_cross']} baar cross kiya (whipsaw)")
    if chop_flat and ic.get("adx", 0) < float(chop_adx) and ic.get("trend_dir", 0) == 0 and ic.get("mtf_dir", 0) == 0:
        why.append(f"Kamzor trend: Index ADX {ic.get('adx', 0):.0f} < {chop_adx} aur 5m/15m flat")
    return bool(why), why


STOCK_CHOP_TXT = "🟠 NO TRADE ZONE (stock choppy)"


def stock_chop_flag(r: dict) -> tuple:
    """Us STOCK ka apna haal: VWAP whipsaw ya (kamzor ADX + 5m/15m dono flat) = choppy. (15m zone alag filter hai.)"""
    if not chop_filter:
        return False, ""
    why = []
    if int(r.get("_vwx", 0) or 0) >= int(chop_cross):
        why.append(f"stock ne VWAP ko 1 ghante me {int(r['_vwx'])} baar cross kiya (whipsaw)")
    if chop_flat and r["ADX (14)"] < float(chop_adx) and r.get("_tdir", 0) == 0 and r.get("_mtf", 0) == 0:
        why.append(f"stock ka kamzor trend: ADX {r['ADX (14)']:.0f} < {chop_adx} aur 5m/15m flat")
    return bool(why), "; ".join(why)


def rs_benchmark(df: pd.DataFrame, ic: dict) -> dict:
    """RS ka benchmark: Stock mode me us sector ke baaki stocks ka average Day % (kam peers ho to poore scanned stocks ka average); Index mode me index change."""
    if not basis_stock:
        return {s_: float(ic.get("chg_pct", 0.0)) for s_ in df["Symbol"]}
    day = dict(zip(df["Symbol"], df["Day %"]))
    sec = {s_: sector_of(s_) for s_ in day}
    uni = float(np.nanmean(list(day.values()))) if day else 0.0
    out = {}
    for s_ in day:
        peers = [v for p_, v in day.items() if p_ != s_ and sec[p_] == sec[s_] and pd.notna(v)] if sec[s_] != "OTHER" else []
        out[s_] = float(np.mean(peers)) if len(peers) >= 2 else uni
    return out


def _num(x) -> float:
    v = safe_float(x, 0.0)
    return v if v == v else 0.0


def calc_sl_tgt(entry: float, side: int, r: dict) -> tuple:
    """v7.6: SL mode ke hisaab se (sl, target, sl_doori, mode_label). side = +1 LONG / -1 SHORT.
    Doori hamesha [sl_min_atr5 x ATR5, sl_max_atr15 x ATR15] ke beech; data na ho to ATR(5m) wala purana tarika."""
    a5, a15 = _num(r.get("ATR (5m)")), _num(r.get("ATR (15m)"))
    zlo, zhi = _num(r.get("Zone Lo")), _num(r.get("Zone Hi"))
    if entry <= 0 or side == 0 or a5 <= 0:
        return float("nan"), float("nan"), 0.0, "-"
    mode = str(sl_mode)
    d, lab = a5 * float(sl_atr_mult), "ATR5"
    if mode.startswith("15m zone") and a15 > 0:
        if side == 1 and 0 < zlo < entry:
            d, lab = entry - (zlo - float(sl_zone_buf) * a15), "ZONE"
        elif side == -1 and zhi > entry:
            d, lab = (zhi + float(sl_zone_buf) * a15) - entry, "ZONE"
        else:
            d, lab = a15 * float(sl_atr15_mult), "ATR15 (zone nahi)"
    elif mode.startswith("ATR(15m)") and a15 > 0:
        d, lab = a15 * float(sl_atr15_mult), "ATR15"
    if lab != "ATR5":
        d = max(d, a5 * float(sl_min_atr5))
        if a15 > 0:
            d = min(d, a15 * float(sl_max_atr15))
    sl = round(entry - side * d, 2)
    tgt = round(entry + side * d * float(rr_mult), 2)
    return sl, tgt, d, lab


def finalize_actions(df: pd.DataFrame, ic: dict) -> pd.DataFrame:
    if df.empty:
        return df
    tdir_idx = ic.get("trend_dir", 0) if ic.get("ok") else 0
    bench = rs_benchmark(df, ic)
    acts, aligns, sls, tgts, lots_l, qty_l, ranks, routes, pbblk = [], [], [], [], [], [], [], [], []
    for r in df.to_dict("records"):
        tdir = r.get("_tdir", 0) if basis_stock else tdir_idx
        bm = bench.get(r["Symbol"], float(ic.get("chg_pct", 0.0)))
        chop_flag, chop_note = (stock_chop_flag(r) if basis_stock else (False, ""))
        sc, adx_v = r["_score"], r["ADX (14)"]
        adx_ok = adx_min == 0 or adx_v >= adx_min
        side = 1 if (sc >= min_net and adx_ok) else (-1 if (sc <= -min_net and adx_ok) else 0)
        pend = []
        if side:
            if require_mtf and r["_mtf"] != side:
                pend.append("15m")
            if require_orb and r["_orb"] != side:
                pend.append("ORB")
            if require_fut and r["_fut"] != side:
                pend.append("OI")
            if f_vol and r["Vol Spike x"] < float(f_vol_min):      # v5.3 filter 4: volume mandatory
                pend.append("VOL")
        ext = (side == 1 and r["_extL"]) or (side == -1 and r["_extS"])
        against = bool(side and require_idx and tdir == -side)
        rs_val = r["Day %"] - bm                                    # v5.3 filter 3: RS (stock mode: sector peers, index mode: index) mandatory
        weak_rs = bool(side and f_rs and ((side == 1 and rs_val < -float(f_rs_min)) or (side == -1 and rs_val > float(f_rs_min))))
        ext_why = (r.get("_whyL") if side == 1 else r.get("_whyS")) or "pullback wait"
        if r["_lock"]:
            act = LOCK_TXT
        elif not r["_ok"]:
            act = "⚠ NO DATA"
        elif zone_filter and r["_zone"]:
            act = ZONE_TXT
        elif side == 0:
            act = "⚪ WAIT / NEUTRAL"
        elif pend:
            act = f"⚪ WAIT (need {'+'.join(pend)})"
        elif ext:
            act = f"🟡 BUY (EXTENDED - {ext_why})" if side == 1 else f"🟡 SELL (EXTENDED - {ext_why})"
        elif against or weak_rs:
            _ref = "STOCK trend" if basis_stock else "INDEX"
            _rsn = f"against {_ref}" if against else f"against {_ref} - weak RS {rs_val:+.2f}%" if not basis_stock else f"weak RS vs peers {rs_val:+.2f}%"
            act = f"🟡 BUY ({_rsn})" if side == 1 else f"🟡 SELL ({_rsn})"
        else:
            act = "🟢 STRONG BUY" if side == 1 else "🔻 STRONG SELL"
        if (act.startswith("🟢 STRONG") or act.startswith("🔻 STRONG")):
            if basis_stock and chop_flag:
                act = STOCK_CHOP_TXT
            elif (not basis_stock) and MKT_CHOP:
                act = MKT_CHOP_TXT
        route = "-"
        if act.startswith("🟢 STRONG") or act.startswith("🔻 STRONG"):
            s_dir = 1 if act.startswith("🟢") else -1
            if not pcr_filter_on or use_stock_pcr:
                route = "NORMAL (PCR filter off)" if not pcr_filter_on else "STOCK PCR check baaki"
            else:
                ok_n, why_n = pcr_route(ic, s_dir)
                if ok_n:
                    route = "NORMAL (PCR ok)"
                else:
                    ok_s, fails_s = is_solo_outperformer(r, s_dir, r["Day %"] - bm) if solo_on else (False, ["override off"])
                    if ok_s:
                        route = f"SOLO OVERRIDE ({why_n})"
                    else:
                        act = PCR_BLOCK_TXT
                        route = f"BLOCKED: {why_n}; solo fail: {','.join(fails_s)}"
        if act == STOCK_CHOP_TXT:
            route = f"BLOCKED: {chop_note}"
        routes.append(route)
        _pbr = []                                   # v7.6.1: EXTENDED -> pullback order ke liye bhi STRONG wali shartein
        if str(act).startswith(("🟡 BUY (EXTENDED", "🟡 SELL (EXTENDED")):
            if against or weak_rs:
                _pbr.append(f"weak RS {rs_val:+.2f}%" if weak_rs else "trend ke khilaaf")
            if basis_stock and chop_flag:
                _pbr.append(f"choppy: {chop_note}")
            elif (not basis_stock) and MKT_CHOP:
                _pbr.append("market choppy")
        pbblk.append("; ".join(_pbr))
        acts.append(act)
        aligns.append("-" if not side or not tdir else (("✅ with stock trend" if basis_stock else "✅ with index") if tdir == side else "⚠ against"))

        sl = tgt = lots = qty = float("nan")
        if side and r["ATR (5m)"] > 0 and r["LTP"] > 0 and not (zone_filter and r["_zone"]):
            sl, tgt, _d, _lab = calc_sl_tgt(float(r["LTP"]), side, r)       # v7.6: SL mode
            if r["_lot"]:
                if use_cap_qty:
                    _cq = cap_qty(r["LTP"])
                    if _cq >= 1:
                        lots, qty = 1, _cq        # capital ke hisab se shares
                else:
                    lots, qty = 1, r["_lot"]      # Equity intraday: qty = us share ke 1 lot me jitne shares
        sls.append(sl), tgts.append(tgt), lots_l.append(lots), qty_l.append(qty)

        sg = side or int(np.sign(sc))
        rs = (r["Day %"] - bm) * sg
        ranks.append(round(abs(sc) + 0.5 * min(r["Vol Spike x"], 3.0) + 0.02 * adx_v + 0.3 * float(np.clip(rs, -2, 2)), 2)
                     if r["_ok"] and not r["_lock"] else float("nan"))
    df = df.copy()
    df["RS vs Index %"] = (df["Day %"] - df["Symbol"].map(bench)).round(2)      # stock mode me ye sector-peers ke mukable RS hai
    df["RS basis"] = "Sector peers" if basis_stock else "Index"
    df["Sector"] = df["Symbol"].map(sector_of)                                  # v7.5: sirf display (filter nahi)
    df["Sector Day %"] = df.groupby("Sector")["Day %"].transform("mean").round(2)
    df.loc[df["Sector"] == "OTHER", "Sector Day %"] = float("nan")
    df["Bull Power %"] = (df["_score"].clip(lower=0) / 8.0 * 100.0).round(0)    # us stock ke apne signals (score +8 = 100%)
    df["Bear Power %"] = ((-df["_score"]).clip(lower=0) / 8.0 * 100.0).round(0)
    df["Final Action"], df["Idx Align"] = acts, aligns
    df["Entry Route"] = routes
    df["_pb_block"] = pbblk
    df["SL"], df["Target"], df["Lots"], df["Qty"], df["Rank"] = sls, tgts, lots_l, qty_l, ranks
    return df


MKT_CHOP, MKT_CHOP_WHY = market_chop_state(ictx)
df_all = finalize_actions(df_all, ictx)
df_all = apply_stock_pcr(df_all)
df_all = apply_spread_guard(df_all)


def _jsonable(v):
    if isinstance(v, (np.integer,)):
        return int(v)
    if isinstance(v, (np.floating, float)):
        return None if (v != v or v in (float("inf"), float("-inf"))) else float(v)
    if isinstance(v, (np.bool_,)):
        return bool(v)
    if isinstance(v, (list, tuple)):
        return [_jsonable(x) for x in v]
    if isinstance(v, (str, int, bool)) or v is None:
        return v
    return str(v)


def save_scan_log(df: pd.DataFrame) -> int:
    """v7.5: SAARE stocks ki poori scanner row (har filter ki value + internal _flags) DB ke scan_log me.
    5-min slot me ek baar (dt, slot, sym unique) - full scan ya non-two-tier refresh par. Returns rows saved."""
    if df is None or df.empty:
        return 0
    now = now_ist()
    slot = now.replace(minute=(now.minute // 5) * 5, second=0, microsecond=0).strftime("%H:%M")
    day = now.strftime("%Y-%m-%d")
    if SNAP.get("scan_log_slot") == (day, slot):
        return 0
    rows = []
    for r in df.to_dict("records"):
        if str(r.get("Scan", "")).startswith("full-scan"):
            continue                                  # purani cached row - sirf taaza data save
        data = {k: _jsonable(v) for k, v in r.items()}
        rows.append((day, slot, now.strftime("%H:%M:%S"), str(r.get("Symbol")), str(r.get("Final Action", "")),
                     _jsonable(r.get("_score")), _jsonable(r.get("LTP")), _jsonable(r.get("Day %")),
                     _jsonable(r.get("Stock PCR")), json.dumps(data, ensure_ascii=False)))
    if not rows:
        return 0
    try:
        with db() as conn:
            conn.executemany("INSERT OR IGNORE INTO scan_log (dt, slot, time_ist, sym, action, score, ltp, day_pct, stock_pcr, data) "
                             "VALUES (?,?,?,?,?,?,?,?,?,?)", rows)
        SNAP["scan_log_slot"] = (day, slot)
    except Exception as e:
        ERR_LOG.append((now.strftime("%H:%M:%S"), -1, "scan_log", str(e)[:140]))
        return 0
    return len(rows)


def scan_log_frame(day: str) -> pd.DataFrame:
    """Ek din ka scan_log -> flat DataFrame (har slot x har stock, saare columns)."""
    with db() as conn:
        rows = conn.execute("SELECT slot, data FROM scan_log WHERE dt = ? ORDER BY slot, sym", (day,)).fetchall()
    recs = []
    for slot, data in rows:
        try:
            d = json.loads(data)
        except Exception:
            continue
        d = {"Slot": slot, **{k: (", ".join(map(str, v)) if isinstance(v, list) else v) for k, v in d.items()}}
        recs.append(d)
    return pd.DataFrame(recs)


if (not demo_mode or save_demo_db) and (LIVE_MKT or demo_mode) and (FULL_SCAN or not TWO_TIER):
    save_scan_log(df_all)

if not _IS_BG:
    with st.sidebar.expander("🗂 Scan log: har stock ka har filter data (CSV)"):
        try:
            with db() as _c:
                _sl = _c.execute("SELECT dt, COUNT(DISTINCT slot), COUNT(*) FROM scan_log GROUP BY dt ORDER BY dt DESC LIMIT 30").fetchall()
        except Exception:
            _sl = []
        if _sl:
            st.caption(" | ".join(f"{d}: {ns} scan, {nr} rows" for d, ns, nr in _sl[:5]))
            _sl_day = st.selectbox("Din chuno", [d for d, _, _ in _sl], key="scanlog_day")
            if st.button("CSV taiyaar karo", key="scanlog_btn"):
                try:
                    _sf = scan_log_frame(_sl_day)
                    st.download_button(f"⬇ scan_log_{_sl_day}.csv ({len(_sf)} rows)", _sf.to_csv(index=False).encode("utf-8-sig"),
                                       file_name=f"scan_log_{_sl_day}.csv", mime="text/csv", key="scanlog_dl")
                except Exception as _e:
                    st.error(f"Scan log CSV fail: {_e}")
        else:
            st.caption("Abhi koi scan log nahi - market time me har full scan (5-min slot) par save hoga.")
if TWO_TIER and FULL_SCAN and not df_all.empty and "Final Action" in df_all.columns:
    SNAP["last_full"] = time.time()
    _pat = ["STRONG BUY", "STRONG SELL"]
    if watch_ext:
        _pat += ["EXTENDED", "against INDEX", "against STOCK", "weak RS vs peers"]
    if watch_wait:
        _pat += ["WAIT (need"]
    if use_stock_pcr and pcr_filter_on:
        _pat += ["NO TRADE (stock PCR"]
    if spread_guard_on:
        _pat += ["NO TRADE (spread"]
    _msk = df_all["Final Action"].apply(lambda a: any(p in str(a) for p in _pat))

    def _wprio(a):                     # v7.8: STRONG pehle, phir EXTENDED/RS/spread, WAIT sabse aakhir me
        a = str(a)
        return 0 if "STRONG" in a else (2 if "WAIT (need" in a else 1)
    _wdf = df_all[_msk].assign(_wp=df_all.loc[_msk, "Final Action"].map(_wprio))
    SNAP["watch"] = (_wdf.sort_values(["_wp", "Rank"], ascending=[True, False], na_position="last")
                     .head(int(watch_max))["Symbol"].tolist())

# ---- Weighted Bull/Bear power + coverage ----
if not df_all.empty:
    total_all_w = df_all["Weight %"].sum() or 1.0
    coverage = round(df_all[df_all["_ok"]]["Weight %"].sum() / total_all_w * 100.0, 1)
    valid_df = df_all[df_all["_ok"]]
    if exclude_result_wk:
        valid_df = valid_df[~valid_df["_lock"]]
    total_w = valid_df["Weight %"].sum() or 1.0
    bull_pwr = round(valid_df[valid_df["_score"] >= min_net]["Weight %"].sum() / total_w * 100.0, 1)
    bear_pwr = round(valid_df[valid_df["_score"] <= -min_net]["Weight %"].sum() / total_w * 100.0, 1)
    result_wk_stocks = df_all[df_all["_lock"]]["Symbol"].tolist()
    lv_col = f"Low Vol (<{max_monthly_move_th:.0f}%)"
    low_vol_count = int(((df_all["1M Move %"] > 0) & (df_all["1M Move %"] < max_monthly_move_th)).sum())
    stale_cnt = int((df_all["Data Lag (min)"] > 5).sum())
else:
    coverage, bull_pwr, bear_pwr, result_wk_stocks, low_vol_count, stale_cnt = 0.0, 0.0, 0.0, [], 0, 0
    lv_col = f"Low Vol (<{max_monthly_move_th:.0f}%)"


# ====== SECTION: SIGNAL ENGINE (Index + Stock Paper Trade Engines with Live DB Persistence) ======
def default_state(day: str) -> dict:
    return {
        "day": day, "side": "FLAT", "pend": "FLAT", "pend_n": 0, "entry": 0.0, "sl": 0.0, "sl0": 0.0, "tgt": 0.0,
        "peak": 0.0, "t_entry": "", "mfe": 0.0, "mae": 0.0, "bull0": 0.0, "pcr0": 0.0, "vix0": 0.0,
        "last_eval": 0.0, "blockers": [], "last_event": "-", "sl_hits": 0, "pnl": 0.0, "db_id": 0,
    }


def send_telegram(text: str):
    if not (tg_alerts and TG_TOKEN and TG_CHAT) or demo_mode:
        return

    def _send():
        try:
            requests.post(f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage",
                          data={"chat_id": TG_CHAT, "text": text}, timeout=6)
        except Exception:
            pass
    threading.Thread(target=_send, daemon=True).start()


@st.cache_resource
def _tg_agent():
    """Telegram commands ka daemon thread: /status /kill /resume /exit SYMBOL /help. Sirf TELEGRAM_CHAT_ID ki chat ke commands.
    Thread sirf DB + KILL_SWITCH file + kv use karta hai (sidebar ki settings nahi) - isliye purane run ke namespace me bhi theek chalta hai."""
    store = {"token": "", "chat": "", "enabled": False, "offset": None, "last_err": None, "cmds": 0, "wake": threading.Event()}

    def reply(text: str) -> None:
        try:
            requests.post(f"https://api.telegram.org/bot{store['token']}/sendMessage",
                          data={"chat_id": store["chat"], "text": text[:3900]}, timeout=8)
        except Exception as e:
            store["last_err"] = str(e)[:120]

    def status_text() -> str:
        day = now_ist().strftime("%Y-%m-%d")
        with db() as conn:
            opn = conn.execute("SELECT symbol, side, entry, exit, pnl_rs, lots, lot_size, sl, tgt, mode FROM trade_journal "
                               "WHERE dt = ? AND status = 'OPEN' AND instrument_type = 'EQUITY_INTRADAY' ORDER BY id", (day,)).fetchall()
            cl = conn.execute("SELECT COUNT(*), COALESCE(SUM(pnl_rs), 0), COALESCE(SUM(CASE WHEN pnl_rs > 0 THEN 1 ELSE 0 END), 0) "
                              "FROM trade_journal WHERE dt = ? AND status = 'CLOSED' AND instrument_type = 'EQUITY_INTRADAY'", (day,)).fetchone()
        halt = kv_get(f"stk_halt:{day}") or ""
        run = sum(float(r[4] or 0) for r in opn)
        lines = [f"📟 STATUS {now_ist():%H:%M:%S}", f"Band trades: {cl[0]} (jeet {cl[2]}) | band P&L Rs {cl[1]:+,.0f}",
                 f"Khule: {len(opn)} | khule P&L Rs {run:+,.0f} | din ka total Rs {cl[1] + run:+,.0f}",
                 f"Halt: {halt or 'nahi'} | KILL file: {'HAAN' if os.path.exists(KILL_FILE) else 'nahi'}"]
        for r in opn[:25]:
            lines.append(f"• {r[0]} {r[1]} entry {r[2]:.2f} ltp {float(r[3] or 0):.2f} | Rs {float(r[4] or 0):+,.0f} | SL {r[7]:.2f} TGT {r[8]:.2f} [{r[9]}]")
        if len(opn) > 25:
            lines.append(f"... aur {len(opn) - 25}")
        return "\n".join(lines)

    def handle(text: str) -> str:
        parts = (text or "").strip().split()
        if not parts or not parts[0].startswith("/"):
            return ""
        cmd, args = parts[0].lower().split("@")[0], [p.upper() for p in parts[1:]]
        day = now_ist().strftime("%Y-%m-%d")
        store["cmds"] += 1
        audit("TG CMD", "", "", text[:80])
        if cmd in ("/start", "/help"):
            return "Commands:\n/status - khule trades + P&L\n/exit SYMBOL (ya ALL) - trade band karwao (agle cycle me)\n/kill - KILL_SWITCH: sab band + din bhar halt\n/resume - KILL_SWITCH hatao + halt clear"
        if cmd == "/status":
            return status_text()
        if cmd == "/kill":
            with open(KILL_FILE, "w") as f:
                f.write(f"telegram {now_ist():%Y-%m-%d %H:%M:%S}")
            return "🛑 KILL_SWITCH file bana di. Engine agle cycle (~30 sec) me saare khule trade band karke din bhar trading rok dega (app ya background agent chalta hona chahiye). /status se check karo."
        if cmd == "/resume":
            if os.path.exists(KILL_FILE):
                os.remove(KILL_FILE)
            kv_set(f"stk_halt:{day}", "")
            SNAP[f"stk_halt:{day}"] = ""
            return "✅ KILL_SWITCH hata di aur aaj ka halt clear kiya. (Loss/SL limit ab bhi lag sakti hai.)"
        if cmd == "/exit":
            if not args:
                return "Use: /exit SYMBOL  (jaise /exit SBIN) ya /exit ALL"
            with db() as conn:
                opn = {r[0].upper() for r in conn.execute("SELECT symbol FROM trade_journal WHERE dt = ? AND status = 'OPEN' "
                                                          "AND instrument_type = 'EQUITY_INTRADAY'", (day,)).fetchall()}
            want = opn if args[0] == "ALL" else {a for a in args if a in opn}
            miss = [a for a in args if args[0] != "ALL" and a not in opn]
            if want:
                kv_set("tg_exit_req", sorted(set(kv_get("tg_exit_req") or []) | want))
            msg = f"🚪 Exit queue me: {', '.join(sorted(want))} (agle cycle me band honge)" if want else "Koi khula trade nahi mila."
            return msg + (f" | khule nahi: {', '.join(miss)}" if miss else "")
        return "Samajh nahi aaya. /help dekho."

    def process_update(u: dict) -> None:
        msg = u.get("message") or {}
        if str((msg.get("chat") or {}).get("id")) != str(store["chat"]):
            return                                       # sirf aapki chat ID
        out = handle(msg.get("text", ""))
        if out:
            reply(out)

    def loop():
        while True:
            try:
                if not (store["enabled"] and store["token"] and store["chat"]):
                    store["offset"] = None
                    store["wake"].wait(10)
                    store["wake"].clear()
                    continue
                base = f"https://api.telegram.org/bot{store['token']}/getUpdates"
                if store["offset"] is None:              # pehli baar: purane commands ignore
                    js = requests.get(base, params={"offset": -1, "timeout": 0}, timeout=15).json()
                    res = js.get("result") or []
                    store["offset"] = (res[-1]["update_id"] + 1) if res else 0
                js = requests.get(base, params={"offset": store["offset"], "timeout": 20}, timeout=30).json()
                for u in js.get("result") or []:
                    store["offset"] = u["update_id"] + 1
                    process_update(u)
            except Exception as e:
                store["last_err"] = str(e)[:150]
                store["wake"].wait(5)
                store["wake"].clear()

    store["handle"], store["process_update"] = handle, process_update
    threading.Thread(target=loop, daemon=True, name="tg-cmd").start()
    return store


TGA = _tg_agent()
TGA.update(token=TG_TOKEN, chat=TG_CHAT, enabled=bool(tg_cmd_on and TG_TOKEN and TG_CHAT and not demo_mode))


def entry_blockers(side: str, bull: float, bear: float, ic: dict, now: datetime, st_: dict) -> list:
    d = 1 if side == "LONG" else -1
    b = []
    if not ic["ok"]:
        b.append("Index data unavailable")
    if coverage < min_cov:
        b.append(f"Coverage {coverage:.0f}% < {min_cov}%")
    if not demo_mode and not LIVE_MKT:
        b.append("Market closed")
    if not demo_mode and not (entry_start <= now.time() <= entry_end):
        b.append(f"Outside entry window ({entry_start:%H:%M}-{entry_end:%H:%M})")
    if ic["vix"] and ic["vix"] > vix_max:
        b.append(f"VIX {ic['vix']:.1f} > {vix_max:.1f}")
    if adx_min > 0 and ic["adx"] < adx_min:
        b.append(f"Index ADX {ic['adx']:.0f} < {adx_min}")
    if ic["stale_min"] > 5:
        b.append(f"Index data {ic['stale_min']:.0f} min stale")
    if zone_filter and ic["zone"]:
        b.append(f"15m CONSOLIDATION - NO TRADE ZONE ({ic['z_lo']:.0f}-{ic['z_hi']:.0f})")
    if MKT_CHOP:
        b.append("MARKET CHOPPY - NO TRADE ZONE")
    if require_idx and ic["trend_dir"] != d:
        b.append("Index 5m trend not aligned")
    if require_mtf and ic["mtf_dir"] != d:
        b.append("Index 15m MTF not aligned")
    if require_orb:
        if not ic["orb_ready"]:
            b.append("ORB still forming")
        elif ic["orb_dir"] != d:
            b.append("No ORB breakout in direction")
    if require_pcr:
        p = ic["pcr"]
        if p is None:
            b.append("PCR unavailable")
        elif d == 1 and p < pcr_lo:
            b.append(f"PCR {p} < {pcr_lo} (bearish)")
        elif d == -1 and p > pcr_hi:
            b.append(f"PCR {p} > {pcr_hi} (bullish)")
    if require_fut and ic["fut_dir"] != d:
        b.append("Index futures OI not confirming")
    if wall_filter and ic["atr"] > 0:
        r1 = ic["atr"] * sl_atr_mult
        wall = ic["call_wall"] if d == 1 else ic["put_wall"]
        if wall and 0 < (wall - ic["spot"]) * d < r1:
            b.append(f"{'Call' if d == 1 else 'Put'} wall {wall:.0f} too close (<1R)")
    if demo_mode:
        pnl, slc = st_["pnl"], st_["sl_hits"]
    else:
        pnl, slc = journal_today_summary(now.date().isoformat(), "INDEX")
    if slc >= max_sl_day:
        b.append(f"Max SL hits reached ({slc})")
    if pnl <= -abs(daily_loss_limit):
        b.append(f"Daily loss limit hit (Rs {pnl:,.0f})")
    return b


def run_signal_engine(bull: float, bear: float, ic: dict) -> dict:
    now = now_ist()
    day = now.strftime("%Y-%m-%d")
    skey = f"sigstate:{'demo' if demo_mode else 'live'}:{PRIMARY_INDEX_NAME}:{day}"
    stt = SNAP.get(skey)
    persist = (not demo_mode) or bool(save_demo_db)

    if stt is None:
        stt = {**default_state(day), **(kv_get(skey) or {})} if persist else default_state(day)
        SNAP[skey] = stt

    min_gap = max(8.0, 0.7 * float(refresh_sec))
    if time.time() - stt["last_eval"] < min_gap:
        return stt
    stt["last_eval"] = time.time()
    if not ic["ok"]:
        stt["blockers"] = ["Index data unavailable"]
        return stt

    spot, atr = ic["spot"], ic["atr"]
    want = "LONG" if (bull >= enter_th and bull > bear) else ("SHORT" if (bear >= enter_th and bear > bull) else "FLAT")

    def log_event(ev, sl=0.0, tgt=0.0, reason=""):
        stt["last_event"] = f"{now:%H:%M:%S} {ev}"
        if persist:
            log_to_db(day, now.strftime("%H:%M:%S"), ev, spot, bull, bear, ic["pcr"] or 0.0, ic["vix"], sl, tgt, reason)

    # ---------- in position ----------
    if stt["side"] in ("LONG", "SHORT"):
        d = 1 if stt["side"] == "LONG" else -1
        mv = (spot - stt["entry"]) * d
        stt["mfe"], stt["mae"] = max(stt["mfe"], mv), min(stt["mae"], mv)
        stt["peak"] = max(stt["peak"], spot) if d == 1 else min(stt["peak"] or spot, spot)
        r0 = abs(stt["entry"] - stt["sl0"]) or 1.0
        if use_trail:
            if mv >= float(be_r) * r0:
                stt["sl"] = max(stt["sl"], stt["entry"]) if d == 1 else min(stt["sl"], stt["entry"])
            if mv >= max(1.5, float(be_r) + 0.3) * r0 and atr > 0:
                tr = stt["peak"] - d * atr
                stt["sl"] = max(stt["sl"], tr) if d == 1 else min(stt["sl"], tr)

        running_pnl = mv * ic["lot"] * int(idx_lots)
        if persist and stt.get("db_id"):
            journal_update_open_trade(stt["db_id"], spot, stt["sl"], mv, running_pnl, stt["mfe"], stt["mae"])

        reason = None
        if (d == 1 and spot <= stt["sl"]) or (d == -1 and spot >= stt["sl"]):
            reason = "SL HIT" if mv < 0 else "TRAIL SL HIT"
        elif (d == 1 and spot >= stt["tgt"]) or (d == -1 and spot <= stt["tgt"]):
            reason = "TARGET HIT"
        elif now.time() >= eod_exit and not demo_mode:
            reason = "EOD SQUARE-OFF"
        elif (stt["side"] == "LONG" and bull < exit_th) or (stt["side"] == "SHORT" and bear < exit_th):
            reason = "POWER FADE (hysteresis exit)"
        elif (want != "FLAT" and want != stt["side"]):
            reason = "OPPOSITE SIGNAL"
        elif require_idx and ic["trend_dir"] == -d:
            reason = "INDEX TREND FLIP"

        if reason:
            pts = mv
            pnl = pts * ic["lot"] * int(idx_lots)
            stt["pnl"] += pnl
            if "SL" in reason and pnl < 0:
                stt["sl_hits"] += 1
            if persist:
                journal_close_trade(stt.get("db_id", 0), {
                    "dt": day, "symbol": PRIMARY_INDEX_NAME, "instrument_type": "INDEX",
                    "side": stt["side"], "entry_time": stt["t_entry"], "exit_time": now.strftime("%H:%M:%S"),
                    "entry": stt["entry"], "exit": spot, "sl": stt["sl"], "tgt": stt["tgt"],
                    "pts": round(pts, 2), "pnl_rs": round(pnl, 2), "lots": int(idx_lots),
                    "lot_size": ic["lot"], "exit_reason": reason, "mfe": round(stt["mfe"], 2),
                    "mae": round(stt["mae"], 2), "bull_pwr": stt["bull0"], "pcr": stt["pcr0"],
                    "vix": stt["vix0"], "mode": "DEMO" if demo_mode else "LIVE",
                    "sl0": stt["sl0"],
                })
            log_event(f"EXIT {stt['side']}", stt["sl"], stt["tgt"], reason)
            send_telegram(f"🔔 {PRIMARY_INDEX_NAME} EXIT {stt['side']} @ {spot:.1f} | {reason} | {pts:+.1f} pts | Rs {pnl:+,.0f}")
            stt.update({
                "side": "FLAT", "pend": "FLAT", "pend_n": 0, "entry": 0.0, "sl": 0.0, "sl0": 0.0, "tgt": 0.0,
                "peak": 0.0, "mfe": 0.0, "mae": 0.0, "db_id": 0,
            })
        stt["blockers"] = []
    # ---------- flat ----------
    else:
        stt["blockers"] = []
        if not index_trading_on:
            stt["blockers"] = ["Index trading BAND hai (sidebar: 'Index trading (paper) ON' se chalu karo)"]
            stt["pend"], stt["pend_n"] = "FLAT", 0
        elif want == "FLAT":
            stt["pend"], stt["pend_n"] = "FLAT", 0
        else:
            bl = entry_blockers(want, bull, bear, ic, now, stt)
            stt["blockers"] = bl
            if bl:
                stt["pend"], stt["pend_n"] = "FLAT", 0
            else:
                stt["pend_n"] = stt["pend_n"] + 1 if stt["pend"] == want else 1
                stt["pend"] = want
                if stt["pend_n"] >= confirm_n and atr > 0:
                    d = 1 if want == "LONG" else -1
                    r1 = max(atr * sl_atr_mult, spot * 0.0015)
                    sl, tgt = spot - d * r1, spot + d * r1 * rr_mult
                    wall = ic["call_wall"] if d == 1 else ic["put_wall"]
                    if wall_filter and wall and 1.2 * r1 <= (wall - spot) * d < rr_mult * r1:
                        tgt = wall - d * 0.1 * r1
                    db_id = 0
                    if persist:
                        db_id = journal_open_trade({
                            "dt": day, "symbol": PRIMARY_INDEX_NAME, "instrument_type": "INDEX",
                            "side": want, "entry_time": now.strftime("%H:%M:%S"),
                            "entry": spot, "sl": sl, "tgt": tgt,
                            "lots": int(idx_lots), "lot_size": ic["lot"],
                            "bull_pwr": bull, "pcr": ic["pcr"] or 0.0, "vix": ic["vix"],
                            "mode": "DEMO" if demo_mode else "LIVE",
                        })
                    stt.update({
                        "side": want, "entry": spot, "sl": sl, "sl0": sl, "tgt": tgt, "peak": spot,
                        "t_entry": now.strftime("%H:%M:%S"), "mfe": 0.0, "mae": 0.0, "bull0": bull,
                        "pcr0": ic["pcr"] or 0.0, "vix0": ic["vix"], "pend": "FLAT", "pend_n": 0, "db_id": db_id,
                    })
                    log_event(f"ENTRY {want}", sl, tgt, f"Bull {bull}% / Bear {bear}%")
                    send_telegram(f"🚀 {PRIMARY_INDEX_NAME} {want} @ {spot:.1f}\nSL {sl:.1f} | TGT {tgt:.1f}\n"
                                  f"Bull {bull}% Bear {bear}% | PCR {ic['pcr']} | VIX {ic['vix']}")
    if persist:
        kv_set(skey, stt)
    with SNAP_LOCK:
        hist = SNAP.setdefault("pwr_hist", [])
        hist.append({"t": now.strftime("%H:%M:%S"), "Bull %": bull, "Bear %": bear})
        del hist[:-400]
    return stt


def stk_halt_reason(day: str) -> str:
    k = f"stk_halt:{day}"
    if k not in SNAP:
        SNAP[k] = kv_get(k) or ""
    return SNAP[k]


def stk_set_halt(day: str, why: str) -> None:
    audit("HALT", "", "", why)
    SNAP[f"stk_halt:{day}"] = why
    kv_set(f"stk_halt:{day}", why)
    send_telegram(f"⛔ STOCK TRADING HALT: {why}")


def stk_profit_guard(day: str, pnl: float) -> str:
    """Din ka profit bachao: target pura ya peak se giveback => sirf NAYE trade band (khule trade chalte rahenge)."""
    k = f"stk_peak:{day}"
    if k not in SNAP:
        SNAP[k] = float(kv_get(k) or 0.0)
    if pnl > SNAP[k]:
        SNAP[k] = float(pnl)
        kv_set(k, float(pnl))
    pk = SNAP[k]
    if float(stk_profit_lock) > 0 and pnl >= float(stk_profit_lock):
        return f"Din ka profit target Rs {float(stk_profit_lock):,.0f} pura (P&L Rs {pnl:,.0f})"
    if pk >= float(giveback_min_peak) and pnl <= pk * (1 - float(giveback_pct) / 100.0):
        return f"Profit giveback: peak Rs {pk:,.0f} se {float(giveback_pct):.0f}% wapas gaya (abhi Rs {pnl:,.0f})"
    return ""


def _stk_entry_why(day: str, sym: str) -> str:
    """v7.8.2: _stk_entry_ok jaisa hi guard, par roke to WAJAH lauta (khaali = entry theek)."""
    _h = stk_halt_reason(day)
    if _h:
        return f"⛔ Trading HALT: {_h}"
    pnl, cons, ntr, sl_hits = stk_day_stats(day, "DEMO" if demo_mode else "LIVE")
    if pnl <= -abs(float(stk_loss_limit)):
        return f"⛔ Din ka loss limit (P&L Rs {pnl:,.0f} / limit -{abs(float(stk_loss_limit)):,.0f})"
    if sl_hits >= int(stk_max_sl_day):
        return f"⛔ Aaj {sl_hits} SL hit ho chuke (limit {int(stk_max_sl_day)})"
    if cons >= int(max_consec_losses):
        return f"⛔ Lagataar {cons} loss (limit {int(max_consec_losses)}) - aaj naye trade band"
    if ntr >= int(max_stk_trades_day):
        return f"⛔ Aaj ke {ntr} trade poore (limit {int(max_stk_trades_day)}/din)"
    cd = SNAP.get(f"stk_cd:{day}", {}).get(sym)
    if not cd:
        return ""
    if cd.get("blocked"):
        return "⛔ Is stock me aaj SL lag chuka - dobara entry nahi"
    if cd["n"] >= STK_MAX_PER_SYM:
        return f"⛔ Is stock me aaj {cd['n']} trade ho chuke (max {STK_MAX_PER_SYM})"
    last_trade_result = float(cd.get("last_result", 0.0))
    cooldown_mins = 60 if last_trade_result < 0 else STK_COOLDOWN_MIN
    left = cooldown_mins * 60 - (time.time() - cd["t"])
    if left > 0:
        return f"⏳ Cooldown: {left / 60:.0f} min baaki ({'loss' if last_trade_result < 0 else 'pichle exit'} ke baad {cooldown_mins} min)"
    return ""


def _stk_entry_ok(day: str, sym: str) -> bool:
    """Guard: halt / daily loss / stk_max_sl_day / lagataar loss / trades-per-day / stock par SL block / loss-based cooldown."""
    return not _stk_entry_why(day, sym)


def _stk_min_ok(day: str, now: datetime) -> bool:
    d = SNAP.setdefault(f"stk_min:{day}", {})
    return d.get(now.strftime("%H:%M"), 0) < int(max_new_per_min)


def _stk_confirmed(day: str, sym: str, want: str, ltp: float = 0.0) -> bool:
    """Signal kam se kam stk_confirm_n alag cycles tak lagataar bana rahe (jhoothe signal kam).
    v7.8: pehli baar dikhne ka time/LTP bhi yaad rakhta hai (confirm_log / trade_journal ke liye)."""
    pk = SNAP.setdefault(f"stk_pend:{day}", {})
    p = pk.get(sym)
    if not p or p["side"] != want:
        if p:
            confirm_log_write(day, sym, p, "FLIP (ulta signal)", ltp)
        _t = time.time()
        p = pk[sym] = {"side": want, "n": 1, "t": _t, "t0": _t, "tf": now_ist().strftime("%H:%M:%S"),
                       "ltp0": float(ltp or 0.0), "need": int(stk_confirm_n), "mode": "DEMO" if demo_mode else "LIVE"}
    elif time.time() - p["t"] >= max(10.0, 0.7 * float(refresh_sec)):
        p["n"] += 1
        p["t"] = time.time()
    hit = p["n"] >= int(stk_confirm_n)
    if hit:
        p["conf"] = True
    return hit


def _cinfo(p, route: str) -> dict:
    """v7.8: pending-signal dict se trade ke liye confirm info."""
    if not p:
        return {}
    return {"n": int(p.get("n", 0)), "sec": round(time.time() - float(p.get("t0") or time.time()), 1),
            "ltp0": float(p.get("ltp0") or 0.0), "need": int(p.get("need") or stk_confirm_n), "route": route}


# ====== SECTION: ML TRADE-QUALITY MODEL (numpy logistic regression, bina extra library) ======
ML_FEATS = ["score_abs", "side", "adx", "volx", "rs_side", "rank", "atr_pct", "hour", "vix", "mid_lull"]


def ml_feats(r: dict, want: str, ltp: float, now: datetime, vix: float) -> dict:
    sd = 1 if want == "LONG" else -1
    hr = now.hour + now.minute / 60.0
    return {
        "score_abs": abs(safe_float(r.get("_score"))), "side": float(sd), "adx": safe_float(r.get("ADX (14)")),
        "volx": min(safe_float(r.get("Vol Spike x")), 5.0),
        "rs_side": float(np.clip(safe_float(r.get("RS vs Index %")) * sd, -3, 3)),
        "rank": safe_float(r.get("Rank")), "atr_pct": (safe_float(r.get("ATR (5m)")) / ltp * 100.0) if ltp > 0 else 0.0,
        "hour": hr, "vix": safe_float(vix), "mid_lull": 1.0 if 12.0 <= hr <= 13.25 else 0.0,
    }


def _auc(y: np.ndarray, p: np.ndarray) -> float:
    pos, neg = int((y == 1).sum()), int((y == 0).sum())
    if pos == 0 or neg == 0:
        return 0.5
    order = np.argsort(p, kind="mergesort")
    ranks = np.empty(len(p))
    ranks[order] = np.arange(1, len(p) + 1)
    for v in np.unique(p):                     # ties => average rank
        m = p == v
        if m.sum() > 1:
            ranks[m] = ranks[m].mean()
    return float((ranks[y == 1].sum() - pos * (pos + 1) / 2.0) / (pos * neg))


def _logreg_fit(X: np.ndarray, y: np.ndarray, l2: float = 1.0, iters: int = 600, lr: float = 0.1):
    w, b = np.zeros(X.shape[1]), 0.0
    n = len(y)
    for _ in range(iters):
        p = 1.0 / (1.0 + np.exp(-np.clip(X @ w + b, -30, 30)))
        g = p - y
        w -= lr * (X.T @ g / n + l2 * w / n)
        b -= lr * float(g.mean())
    return w, b


def ml_train(j: pd.DataFrame, min_valid_trades: int = 100) -> dict:
    """Journal ke band stock trades se model. Time-ordered 70/30 split par test AUC naapta hai (look-ahead nahi)."""
    out = {"valid": False, "n": 0, "feats": ML_FEATS, "trained_at": now_ist().strftime("%Y-%m-%d %H:%M")}
    if j is None or j.empty:
        out["reason"] = "journal khali"
        return out
    d = j.copy()
    for c in ("P&L Rs", "Bull%/Score", "ADX", "VolX", "RS vs Idx %", "Rank", "ATR", "Entry", "VIX"):
        d[c] = pd.to_numeric(d[c], errors="coerce")
    d = d[(d["ADX"] > 0) & (d["VolX"] > 0) & d["P&L Rs"].notna()].copy()
    d = d.sort_values(["Date", "In"]).reset_index(drop=True)
    out["n"] = len(d)
    if len(d) < 40:
        out["reason"] = f"sirf {len(d)} feature-wale trades (kam se kam 40 chahiye, bharosa ke liye {min_valid_trades}+)"
        return out
    sd = np.where(d["Side"].astype(str).str.upper() == "LONG", 1.0, -1.0)
    hr = d["In"].astype(str).str.split(":").apply(lambda x: float(x[0]) + float(x[1]) / 60.0 if len(x) > 1 else 10.0)
    X = np.column_stack([
        d["Bull%/Score"].abs().fillna(0), sd, d["ADX"].fillna(0), d["VolX"].clip(upper=5).fillna(0),
        (d["RS vs Idx %"].fillna(0) * sd).clip(-3, 3), d["Rank"].fillna(0),
        (d["ATR"].fillna(0) / d["Entry"].replace(0, np.nan) * 100.0).fillna(0), hr, d["VIX"].fillna(0),
        ((hr >= 12.0) & (hr <= 13.25)).astype(float),
    ]).astype(float)
    y = (d["P&L Rs"].values > 0).astype(float)
    k = int(len(d) * 0.7)
    mu, sg = X[:k].mean(axis=0), X[:k].std(axis=0)
    sg[sg == 0] = 1.0
    w, b = _logreg_fit((X[:k] - mu) / sg, y[:k])
    pt = 1.0 / (1.0 + np.exp(-np.clip(((X[k:] - mu) / sg) @ w + b, -30, 30)))
    out["auc_test"] = round(_auc(y[k:], pt), 3)
    out["acc_test"] = round(float(((pt >= 0.5) == (y[k:] == 1)).mean()), 3)
    out["base_win_test"] = round(float(y[k:].mean()), 3)
    out["calib_gap"] = round(abs(float(pt.mean()) - float(y[k:].mean())), 3)       # predicted vs asli win rate (out-of-sample)
    mu, sg = X.mean(axis=0), X.std(axis=0)
    sg[sg == 0] = 1.0
    w, b = _logreg_fit((X - mu) / sg, y)
    out.update({"mu": mu.tolist(), "sg": sg.tolist(), "w": w.tolist(), "b": float(b), "base_win": round(float(y.mean()), 3)})
    out["valid"] = bool(len(d) >= min_valid_trades and out["auc_test"] >= 0.55 and out["calib_gap"] <= 0.15)
    out["reason"] = ("OK" if out["valid"] else
                     f"model ignore: trades {len(d)} (< {min_valid_trades}), test AUC {out['auc_test']} (>= 0.55 chahiye) "
                     f"ya calibration gap {out['calib_gap']} (<= 0.15 chahiye)")
    return out


def ml_predict(model: dict, feats: dict) -> float:
    x = np.array([float(feats.get(f, 0.0)) for f in model["feats"]])
    z = ((x - np.array(model["mu"])) / np.array(model["sg"])) @ np.array(model["w"]) + float(model["b"])
    return float(1.0 / (1.0 + math.exp(-max(-30.0, min(30.0, z)))))


def ml_model_get():
    if "ml_model" not in SNAP:
        SNAP["ml_model"] = kv_get("ml_model")
    return SNAP["ml_model"]


def ml_collect_training_data() -> pd.DataFrame:
    """Asli (LIVE paper) band trades + (option ON ho to) Backtest ke simulated trades."""
    frames = []
    try:
        j = fetch_journal(limit=5000, status_filter="CLOSED", inst_filter="EQUITY_INTRADAY", mode_filter="LIVE")
        if j is not None and not j.empty:
            frames.append(j)
    except Exception:
        pass
    if ml_use_bt:
        try:
            with db() as conn:
                rows = conn.execute("SELECT dt, tin, side, score, adx, volx, rs, rank_v, atr, entry, pnl FROM bt_trades").fetchall()
            if rows:
                b = pd.DataFrame(rows, columns=["Date", "In", "Side", "Bull%/Score", "ADX", "VolX", "RS vs Idx %", "Rank", "ATR",
                                                "Entry", "P&L Rs"])
                b["VIX"], b["Out"], b["Symbol"] = 0.0, "", ""
                frames.append(b)
        except Exception:
            pass
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


def bt_save_trades(t: pd.DataFrame) -> None:
    """Backtest ke trades (features ke saath) DB me - ML training ke liye optional data."""
    if t is None or t.empty:
        return
    try:
        recs = [(r["Date"], r["Symbol"], r["Side"], r["In"], safe_float(r.get("Score")), safe_float(r.get("ADX")),
                 safe_float(r.get("VolX")), safe_float(r.get("RS vs Idx %")), safe_float(r.get("Rank")), safe_float(r.get("ATR")),
                 safe_float(r.get("Entry")), safe_float(r.get("P&L Rs"))) for r in t.to_dict("records")]
        with db() as conn:
            conn.executemany("INSERT OR REPLACE INTO bt_trades (dt, sym, side, tin, score, adx, volx, rs, rank_v, atr, entry, pnl) "
                             "VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", recs)
    except Exception:
        pass


def suggest_params(j: pd.DataFrame) -> list:
    """Asli trades me kaunsa bucket lagataar haar/jeet raha hai - SIRF salaah (code apne aap kuch nahi badalta)."""
    if j is None or j.empty or len(j) < 30:
        return []
    d = j.copy()
    for c in ("P&L Rs", "Bull%/Score", "ADX", "VolX"):
        d[c] = pd.to_numeric(d[c], errors="coerce")
    d["Entry hour"] = d["In"].astype(str).str.split(":").str[0].str.zfill(2) + ":00"
    d["Score"] = d["Bull%/Score"].abs().astype("Int64").astype(str)
    d["Volume spike"] = pd.cut(d["VolX"], [0, 1.2, 1.5, 2.0, 100], labels=["<1.2x", "1.2-1.5x", "1.5-2x", "2x+"]).astype(str)
    d["ADX"] = pd.cut(d["ADX"], [0, 20, 25, 35, 200], labels=["<20", "20-25", "25-35", "35+"]).astype(str)
    d["Exit"] = d["Reason"].astype(str).str.split("(").str[0].str.strip()
    out = []
    for col in ("Entry hour", "Side", "Score", "Volume spike", "ADX", "Sector"):
        if col not in d.columns:
            continue
        g = d[~d[col].isin(["nan", "", "<NA>"])].groupby(col)["P&L Rs"].agg(n="count", net="sum", win=lambda x: (x > 0).mean() * 100.0)
        for k, r_ in g.iterrows():
            if r_["n"] >= 12:
                out.append((col, str(k), int(r_["n"]), float(r_["win"]), float(r_["net"])))
    bad = sorted([o for o in out if o[4] < 0 and o[3] < 35], key=lambda z: z[4])[:3]
    good = sorted([o for o in out if o[4] > 0 and o[3] >= 50], key=lambda z: -z[4])[:3]
    msgs = [f"⚠ {c} = {k}: {n} trades, win {w:.0f}%, net ₹{net:+,.0f} - isme entry kam/band karne par vichaar karo" for c, k, n, w, net in bad]
    msgs += [f"✅ {c} = {k}: {n} trades, win {w:.0f}%, net ₹{net:+,.0f} - yahi pattern behtar chal raha hai" for c, k, n, w, net in good]
    return msgs


def ml_auto_train_if_due(day: str) -> None:
    """Roz market band hone ke baad (15:35+) ek baar: model dobara train, history save, salaah banao.
    Trade rokne ka kaam tabhi hota hai jab sidebar me ML filter > 0 ho."""
    if demo_mode or not ml_auto:
        return
    if now_ist().time() < dtime(15, 35) or kv_get(f"ml_trained:{day}"):
        return
    kv_set(f"ml_trained:{day}", True)
    try:
        new = ml_train(ml_collect_training_data())
        prev = kv_get("ml_model")
        active, note = new, new.get("reason", "")
        if not new.get("valid") and prev and prev.get("valid"):
            try:
                age = (now_ist().replace(tzinfo=None) - datetime.strptime(prev["trained_at"], "%Y-%m-%d %H:%M")).days
            except Exception:
                age = 99
            if age <= 5:
                active, note = prev, f"naya model valid nahi ({new.get('reason')}); {prev.get('trained_at')} wala valid model active rakha"
        kv_set("ml_model", active)
        SNAP["ml_model"] = active
        live = fetch_journal(limit=5000, status_filter="CLOSED", inst_filter="EQUITY_INTRADAY", mode_filter="LIVE")
        sug = suggest_params(live)
        kv_set("ml_suggestions", sug)
        with db() as conn:
            conn.execute("INSERT INTO ml_history (dt, tm, n, auc, acc, base, gap, valid, note) VALUES (?,?,?,?,?,?,?,?,?)",
                         (day, now_ist().strftime("%H:%M:%S"), int(new.get("n", 0)), new.get("auc_test"), new.get("acc_test"),
                          new.get("base_win_test"), new.get("calib_gap"), int(bool(new.get("valid"))), note[:300]))
        audit("ML TRAIN", "", "", f"n={new.get('n', 0)} AUC={new.get('auc_test')} gap={new.get('calib_gap')} valid={new.get('valid')}")
        msg = (f"🤖 ML auto-train {day}: trades {new.get('n', 0)} | test AUC {new.get('auc_test', '-')} | "
               f"calibration gap {new.get('calib_gap', '-')} | {'USE HOGA' if active.get('valid') else 'IGNORE'}")
        if sug:
            msg += "\n" + "\n".join(sug[:2])
        send_telegram(msg)
    except Exception as e:
        ERR_LOG.append((now_ist().strftime("%H:%M:%S"), -1, "ml auto-train", str(e)[:140]))


def _skip_log(now: datetime, sym: str, want: str, why: str) -> None:
    rs = SNAP.setdefault("risk_skips", [])
    line = f"{now:%H:%M:%S} {sym} {want} skip: {why}"
    if not rs or rs[-1][9:] != line[9:]:
        rs.append(line)
        del rs[:-8]
        audit("SKIP", sym, want, why)


def live_partial(day: str, sym: str, qty_part: int) -> None:
    """Live position ka aadha hissa MARKET se band + broker SL ka qty kam (SL-M modify)."""
    with LIVE_LOCK:
        p = _lp(day).get(sym)
        if not p or not p.get("filled") or not p.get("sl_oid") or p.get("exit_pending"):
            return
        qty_part = int(qty_part)
        if qty_part <= 0 or qty_part >= int(p["qty"]):
            return
        exit_side = "SELL" if p["side"] == "LONG" else "BUY"
        ok, oid, msg = upx_place(p["ikey"], exit_side, qty_part, "MARKET", 0.0, "TERMPART")
        if not ok:
            live_log(day, sym, "PARTIAL EXIT", exit_side, qty_part, "", "FAILED", msg)
            return
        live_log(day, sym, "PARTIAL EXIT", exit_side, qty_part, oid, "PLACED", "partial profit")
        p["qty"] = int(p["qty"]) - qty_part
        if not upx_modify_sl(p["sl_oid"], p["qty"], p["sl_trig"]):
            live_log(day, sym, "SL MODIFY", "", p["qty"], p["sl_oid"], "FAILED", f"SL qty {p['qty']} update nahi hua - Upstox me khud check karo")
            send_telegram(f"🚨 {sym} partial ke baad broker SL qty update FAIL - khud check karo!")
        _lp_save(day)


def _held_min(pos: dict, now: datetime) -> float:
    try:
        t0 = datetime.strptime(str(pos.get("t_entry", "")), "%H:%M:%S").time()
        return (now - datetime.combine(now.date(), t0, tzinfo=IST)).total_seconds() / 60.0
    except Exception:
        return 0.0


def corr_block(sym: str, want: str, st_map: dict, store: dict):
    """Naye stock ka khule trades ke saath (side-adjusted) correlation. Sabse zyada wala (effective, stock, raw rho) ya None."""
    if not corr_guard_on or not st_map or not store:
        return None
    a = store.get(sym)
    if not a:
        return None
    sa = pd.Series(a[1], index=pd.DatetimeIndex(a[0]))
    worst = None
    for k, p in st_map.items():
        b = store.get(k)
        if not b or k == sym:
            continue
        j = pd.concat([sa, pd.Series(b[1], index=pd.DatetimeIndex(b[0]))], axis=1, join="inner").dropna()
        if len(j) < int(corr_min_pts):
            continue
        rho = float(j.iloc[:, 0].corr(j.iloc[:, 1]))
        if np.isnan(rho):
            continue
        eff = rho * (1.0 if want == p["side"] else -1.0)
        if eff > float(corr_max) and (worst is None or eff > worst[0]):
            worst = (eff, k, rho)
    return worst


def _stk_risk_ok(st_map: dict, sym: str, want: str, new_risk: float, new_notional: float = 0.0, corr_store=None) -> tuple:
    """Pre-trade compliance: direction / sector / total-open-risk + (capital > 0 ho to) position notional aur gross exposure limits."""
    cap = float(capital_rs)
    if cap > 0 and new_notional > 0 and new_notional > float(max_pos_pct) / 100.0 * cap:
        return False, f"position notional Rs {new_notional:,.0f} > {float(max_pos_pct):.0f}% capital"
    if not st_map:
        return True, ""
    n_dir = sum(1 for p in st_map.values() if p["side"] == want)
    if n_dir >= int(max_same_dir):
        return False, f"{want} direction limit ({n_dir}/{int(max_same_dir)})"
    grp = sector_group_of(sector_of(sym))
    if grp != "OTHER":                                     # v7.9: sector GROUP + same group me ulti bet block
        same = [(k, p) for k, p in st_map.items() if sector_group_of(p.get("sector") or sector_of(k)) == grp]
        if sec_no_hedge:
            opp = [k for k, p in same if p["side"] != want]
            if opp:
                return False, f"{grp} me {opp[0]} ka {'SHORT' if want == 'LONG' else 'LONG'} khula hai - same sector me ulta {want} nahi"
        if len(same) >= int(max_per_sector):
            return False, f"{grp} sector limit ({len(same)}/{int(max_per_sector)}: {', '.join(k for k, _ in same)})"
    cb = corr_block(sym, want, st_map, corr_store if corr_store is not None else SNAP.get("ret1m", {}))
    if cb:
        return False, f"correlation {cb[2]:+.2f} ({cb[1]} ke saath, effective {cb[0]:.2f} > {float(corr_max):.2f}) - ek saath girne ka khatra"
    if float(max_open_risk) > 0:
        cur = sum(abs(p["entry"] - p.get("sl0", p["sl"])) * p["qty"] for p in st_map.values())
        if cur + new_risk > float(max_open_risk):
            return False, f"total open risk Rs {cur + new_risk:,.0f} > Rs {float(max_open_risk):,.0f}"
    if cap > 0 and new_notional > 0:
        gross = sum(p["entry"] * p["qty"] for p in st_map.values())
        if gross + new_notional > float(max_gross_x) * cap:
            return False, f"gross exposure Rs {gross + new_notional:,.0f} > {float(max_gross_x):.1f}x capital"
    return True, ""


def pb_reason(r: dict, side_txt: str) -> str:
    """v7.6: STRONG signal par chase kyun nahi? '' = turant entry theek. LONG: RSI >= pb_rsi; SHORT: RSI <= 100-pb_rsi; volume < pb_vol."""
    rsi, vol = safe_float(r.get("RSI (14)"), 50.0), safe_float(r.get("Vol Spike x"), 1.0)
    why = []
    if side_txt == "LONG" and rsi >= float(pb_rsi):
        why.append(f"RSI {rsi:.0f} garam")
    if side_txt == "SHORT" and rsi <= 100.0 - float(pb_rsi):
        why.append(f"RSI {rsi:.0f} oversold")
    if vol < float(pb_vol):
        why.append(f"volume {vol:.2f}x kamzor")
    return ", ".join(why)


def pb_levels(r: dict, side: int, ltp: float) -> tuple:
    """v7.6: (entry level, cancel/invalidation level). LONG: level LTP se neeche; SHORT: upar. Level na bane to (None, None)."""
    vw, a15, a5 = _num(r.get("VWAP")), _num(r.get("ATR (15m)")), _num(r.get("ATR (5m)"))
    zlo, zhi = _num(r.get("Zone Lo")), _num(r.get("Zone Hi"))
    unit = a15 if a15 > 0 else a5 * 2.0
    if ltp <= 0 or unit <= 0:
        return None, None
    mode = str(pb_level_mode)
    cands = []
    if side == 1:
        if mode.startswith(("VWAP ya", "Sirf VWAP")) and 0 < vw < ltp:
            cands.append(vw)
        if mode.startswith(("VWAP ya", "Sirf 15m")) and 0 < zhi < ltp:
            cands.append(zhi)
        if mode.startswith("ATR") or not cands:
            cands.append(ltp - float(pb_atr) * unit)
        lvl = max(cands)                                   # jo price ke sabse paas
        inv = lvl - float(pb_inval_atr) * unit
    else:
        if mode.startswith(("VWAP ya", "Sirf VWAP")) and vw > ltp:
            cands.append(vw)
        if mode.startswith(("VWAP ya", "Sirf 15m")) and zlo > ltp:
            cands.append(zlo)
        if mode.startswith("ATR") or not cands:
            cands.append(ltp + float(pb_atr) * unit)
        lvl = min(cands)
        inv = lvl + float(pb_inval_atr) * unit
    return round(lvl, 2), round(inv, 2)


# ====== v7.9: ENGINE LOCK + TICK FEED (WebSocket / REST 1s) + entry gates ======
@st.cache_resource
def _engine_lock():
    return threading.RLock()


ENGINE_LOCK = _engine_lock()


def _feed_mkt_hours() -> bool:
    n = now_ist()
    return n.weekday() < 5 and dtime(9, 14) <= n.time() <= dtime(15, 31)


def _ltp_from_msg(m) -> list:
    """Upstox V3 feed (SDK decoded dict) se [(instrument_key, ltp)]. ltpc / full / index mode sab."""
    out = []
    if not isinstance(m, dict):
        return out
    for k, v in (m.get("feeds") or {}).items():
        if not isinstance(v, dict):
            continue
        lc = v.get("ltpc")
        if not lc:
            ff = v.get("fullFeed") or v.get("firstLevelWithGreeks") or {}
            for sub in ("marketFF", "indexFF"):
                if isinstance(ff.get(sub), dict) and ff[sub].get("ltpc"):
                    lc = ff[sub]["ltpc"]
                    break
            if not lc and isinstance(ff.get("ltpc"), dict):
                lc = ff["ltpc"]
        try:
            px = float((lc or {}).get("ltp") or 0.0)
        except Exception:
            px = 0.0
        if px > 0:
            out.append((k, px))
    return out


def _feed_px_in(store: dict, k: str, px: float, src: str) -> None:
    store["px"][k] = (px, time.time(), src)
    store["n_" + src] = store.get("n_" + src, 0) + 1
    cb = store.get("cb")
    if cb:
        try:
            cb(k, px)
        except Exception as e:
            store["cb_err"] = f"{now_ist():%H:%M:%S} {str(e)[:120]}"


@st.cache_resource
def _tick_feed() -> dict:
    """v7.9: background threads. (a) WebSocket V3 (upstox-python-sdk), (b) REST LTP har 1 sec - sirf un keys ka
    jinka WS tick 2.5 sec se nahi aaya. Thread sirf store use karta hai; SL/close ka kaam store['cb'] (har run me
    naya) karta hai - isliye sidebar ki latest settings hi lagti hain."""
    store = {"enabled": False, "tok": "", "want": set(), "want_t": 0.0, "px": {}, "hit": {}, "cb": None,
             "ws_ok": False, "ws_status": "start", "rest_status": "-", "cb_err": ""}

    def ws_worker():
        try:
            import upstox_client                                       # pip install upstox-python-sdk
        except Exception:
            store["ws_status"] = "SDK nahi (pip install upstox-python-sdk) - REST 1s fallback chal raha"
            return
        while True:
            try:
                if not (store["enabled"] and store["tok"] and store["want"] and _feed_mkt_hours()):
                    store["ws_ok"] = False
                    store["ws_status"] = "idle (koi khula trade nahi / market band)"
                    time.sleep(2)
                    continue
                tok = store["tok"]
                cfg = upstox_client.Configuration()
                cfg.access_token = tok
                streamer = upstox_client.MarketDataStreamerV3(upstox_client.ApiClient(cfg))
                try:
                    streamer.auto_reconnect(False)
                except Exception:
                    pass
                ws = {"open": False, "subs": set()}

                def _on_open(*_a):
                    ws["open"] = True
                    store["ws_ok"] = True
                    store["ws_status"] = f"CONNECTED {now_ist():%H:%M:%S}"

                def _on_close(*_a):
                    ws["open"] = False
                    store["ws_ok"] = False
                    store["ws_status"] = f"CLOSED {now_ist():%H:%M:%S}"

                def _on_err(*a):
                    store["ws_status"] = f"ERROR {now_ist():%H:%M:%S} {str(a[-1] if a else '')[:80]}"

                def _on_msg(m):
                    for k, px in _ltp_from_msg(m):
                        _feed_px_in(store, k, px, "WS")

                streamer.on("open", _on_open)
                streamer.on("close", _on_close)
                streamer.on("error", _on_err)
                streamer.on("message", _on_msg)
                threading.Thread(target=streamer.connect, daemon=True, name="tick-ws-connect").start()
                t0 = time.time()
                while store["enabled"] and store["tok"] == tok and _feed_mkt_hours():
                    if ws["open"]:
                        want = set(store["want"])
                        add, rem = want - ws["subs"], ws["subs"] - want
                        if add:
                            streamer.subscribe(sorted(add), "ltpc")
                            ws["subs"] |= add
                        if rem:
                            streamer.unsubscribe(sorted(rem))
                            ws["subs"] -= rem
                    elif time.time() - t0 > 20:
                        break                                          # open nahi hua / band ho gaya => reconnect
                    if not store["want"] and time.time() - store.get("want_t", 0.0) > 300:
                        break                                          # 5 min koi trade nahi => socket band
                    time.sleep(0.3)
                try:
                    streamer.disconnect()
                except Exception:
                    pass
                store["ws_ok"] = False
                time.sleep(3)
            except Exception as e:
                store["ws_ok"] = False
                store["ws_status"] = f"ERROR {now_ist():%H:%M:%S} {str(e)[:80]}"
                time.sleep(5)

    def rest_worker():
        while True:
            try:
                keys = [k for k in store["want"] if k]
                if store["enabled"] and store["tok"] and keys and _feed_mkt_hours():
                    now_t = time.time()
                    stale = [k for k in keys if now_t - (store["px"].get(k) or (0, 0, ""))[1] > 2.5]
                    if stale:
                        r = requests.get(f"{V2}/market-quote/ltp", timeout=4,
                                         headers={"Accept": "application/json", "Authorization": f"Bearer {store['tok']}"},
                                         params={"instrument_key": ",".join(stale[:300])})
                        if r.status_code == 200:
                            for v in ((r.json() or {}).get("data") or {}).values():
                                k, px = v.get("instrument_token"), safe_float(v.get("last_price"))
                                if k and px > 0:
                                    _feed_px_in(store, k, px, "REST")
                            store["rest_status"] = f"OK {now_ist():%H:%M:%S} ({len(stale)} key)"
                        else:
                            store["rest_status"] = f"HTTP {r.status_code} {now_ist():%H:%M:%S}"
                            time.sleep(2)
            except Exception as e:
                store["rest_status"] = f"ERROR {str(e)[:80]}"
                time.sleep(2)
            time.sleep(1.0)

    threading.Thread(target=ws_worker, daemon=True, name="tick-ws").start()
    threading.Thread(target=rest_worker, daemon=True, name="tick-rest").start()
    return store


TICK = _tick_feed()


def tick_px(ikey) -> tuple:
    """(price, kitne sec purana). Tick nahi => (0, inf)."""
    v = TICK["px"].get(ikey) if ikey else None
    if not v:
        return 0.0, float("inf")
    return float(v[0]), time.time() - float(v[1])


def _pos_mark(pos: dict, ltp: float, atr: float) -> float:
    """v7.9: MFE/MAE/peak + breakeven/ATR trail (engine refresh aur har tick dono par). Return mv."""
    d = 1 if pos["side"] == "LONG" else -1
    mv = (ltp - pos["entry"]) * d
    pos["mfe"] = max(pos["mfe"], mv)
    pos["mae"] = min(pos["mae"], mv)
    pos["peak"] = max(pos.get("peak", ltp), ltp) if d == 1 else min(pos.get("peak", ltp) or ltp, ltp)
    r0 = abs(pos["entry"] - pos.get("sl0", pos["sl"])) or 1.0
    if use_trail:
        if mv >= float(be_r) * r0:
            pos["sl"] = max(pos["sl"], pos["entry"]) if d == 1 else min(pos["sl"], pos["entry"])
        if mv >= max(1.5, float(be_r) + 0.3) * r0 and atr > 0:
            tr = pos["peak"] - d * atr
            pos["sl"] = max(pos["sl"], tr) if d == 1 else min(pos["sl"], tr)
    return mv


def _tick_on_px(ikey: str, px: float) -> None:
    """v7.9: tick-thread callback. SL/target toote to PEHLE tick ke price par turant band."""
    day = now_ist().strftime("%Y-%m-%d")
    st_map = SNAP.get(f"stk_paper:{day}") or {}
    for sym, pos in list(st_map.items()):
        if pos.get("ikey") != ikey:
            continue
        d = 1 if pos["side"] == "LONG" else -1
        kind = ("SL" if (d == 1 and px <= pos["sl"]) or (d == -1 and px >= pos["sl"]) else
                "TGT" if (d == 1 and px >= pos["tgt"]) or (d == -1 and px <= pos["tgt"]) else "")
        if not kind:
            if ENGINE_LOCK.acquire(blocking=False):            # engine busy ho to agla tick
                try:
                    if st_map.get(sym) is pos:
                        _pos_mark(pos, px, float(pos.get("atr5") or 0.0))
                finally:
                    ENGINE_LOCK.release()
            continue
        TICK["hit"].setdefault(sym, {"db_id": pos["db_id"], "px": float(px), "kind": kind, "t": now_ist().strftime("%H:%M:%S")})
        if not ENGINE_LOCK.acquire(timeout=1.0):
            continue                                            # engine abhi chal raha - wo hit price se band karega
        try:
            hit = TICK["hit"].get(sym)
            if st_map.get(sym) is not pos or not hit or hit["db_id"] != pos["db_id"]:
                continue
            hp = float(hit["px"])
            _pos_mark(pos, hp, float(pos.get("atr5") or 0.0))
            mv = (hp - pos["entry"]) * d
            pnl = mv * pos["qty"] + pos.get("part_pnl", 0.0)
            reason = ("TARGET HIT" if hit["kind"] == "TGT" else ("SL HIT" if (mv < 0 and pnl < 0) else "TRAIL SL HIT")) + " (tick)"
            _pnl = _stk_close(day, sym, pos, hp, reason, now_ist(), st_map)
            SNAP.setdefault(f"stk_why:{day}", {})[sym] = f"🔚 Trade band: {reason} @ {hp:.2f} (P&L Rs {_pnl:+,.0f})"
        finally:
            ENGINE_LOCK.release()


def idx_dir_why(sym: str, want: str) -> str:
    """v7.9: index direction gate. '' = index saath hai."""
    if not idx_dir_gate or want not in ("LONG", "SHORT"):
        return ""
    if reverse_on:                                         # v7.9.1: want = SIGNAL ki disha
        _m = str(rev_idx_mode)
        if _m.startswith("Index gate off"):
            return ""
        if _m.startswith("Asli"):
            want = "SHORT" if want == "LONG" else "LONG"
    return _idx_dir_check(sym, want)


def _idx_dir_check(sym: str, want: str) -> str:
    side = 1 if want == "LONG" else -1
    ref = str(idx_dir_ref)
    if ref.startswith("Dono"):
        unds = ["NIFTY", "BANKNIFTY"]
    elif ref.startswith("Sirf NIFTY"):
        unds = ["NIFTY"]
    else:
        unds = ["BANKNIFTY"] if sector_of(sym) in FIN_SECTORS else ["NIFTY"]
    txt = {1: "UP", -1: "DOWN", 0: "flat"}
    for u in unds:
        cx = IDX_CTX.get(u) or {}
        nm = INDEX_CATALOG[u]["name"]
        if not cx.get("ok"):
            return f"🧭 {nm} ka data nahi - index direction verify nahi hui"
        t5, t15 = int(cx.get("trend_dir", 0) or 0), int(cx.get("mtf_dir", 0) or 0)
        if t5 == -side or t15 == -side:
            return f"🧭 {nm} {want} ke khilaaf (5m {txt[t5]}, 15m {txt[t15]})"
        if idx_dir_strict and t5 != side:
            return f"🧭 {nm} ka 5m trend {txt[t5]} - {want} ke liye index usi disha me chahiye"
    return ""


def _entry_times(day: str) -> list:
    k = f"stk_entry_ts:{day}"
    if k not in SNAP:
        out = []
        try:
            with db() as conn:
                rows = conn.execute("SELECT entry_time FROM trade_journal WHERE dt = ? AND instrument_type = 'EQUITY_INTRADAY' AND mode = ?",
                                    (day, "DEMO" if demo_mode else "LIVE")).fetchall()
            for (tm,) in rows:
                try:
                    t0 = datetime.strptime(f"{day} {tm}", "%Y-%m-%d %H:%M:%S").replace(tzinfo=IST)
                    out.append(t0.timestamp())
                except Exception:
                    pass
        except Exception:
            pass
        SNAP[k] = sorted(out)
    return SNAP[k]


def burst_why(day: str) -> str:
    """v7.9: burst_win min me burst_n entry ho chuki => burst_cd min ka cooldown."""
    if int(burst_n) <= 0:
        return ""
    k = f"stk_burst_cd:{day}"
    if k not in SNAP:
        SNAP[k] = float(kv_get(k) or 0.0)
        if not SNAP[k]:                                     # restart: DB ke entry time se dobara hisaab
            ts = _entry_times(day)
            for i in range(len(ts)):
                win = [t for t in ts[: i + 1] if ts[i] - t <= int(burst_win) * 60]
                if len(win) >= int(burst_n):
                    SNAP[k] = max(SNAP[k], ts[i] + int(burst_cd) * 60)
    left = SNAP[k] - time.time()
    if left > 0:
        return (f"🧊 Burst cooldown: {left / 60:.0f} min baaki ({int(burst_win)} min me {int(burst_n)} entry ho chuki thi - "
                f"ek saath bahut trade = ek saath SL)")
    return ""


def burst_record(day: str) -> None:
    ts = _entry_times(day)
    now_t = time.time()
    ts.append(now_t)
    if int(burst_n) <= 0:
        return
    recent = [t for t in ts if now_t - t <= int(burst_win) * 60]
    if len(recent) >= int(burst_n):
        k = f"stk_burst_cd:{day}"
        SNAP[k] = now_t + int(burst_cd) * 60
        kv_set(k, SNAP[k])
        audit("BURST COOLDOWN", "", "", f"{len(recent)} entry {int(burst_win)} min me => {int(burst_cd)} min naya entry band")
        send_telegram(f"🧊 {len(recent)} entry {int(burst_win)} min me - agle {int(burst_cd)} min naya stock entry band")


def entry_extra_why(day: str, sym: str, want: str) -> str:
    """v7.9: burst cooldown + index direction (sector rule _stk_risk_ok me)."""
    return burst_why(day) or idx_dir_why(sym, want)

def _stk_close(day: str, sym: str, pos: dict, ltp: float, reason: str, now: datetime, st_map: dict) -> float:
    """v7.9: khula stock paper trade band (engine aur tick-thread dono yahi bulate hain - ENGINE_LOCK ke andar)."""
    d = 1 if pos["side"] == "LONG" else -1
    mv = (ltp - pos["entry"]) * d
    pnl_rs = mv * pos["qty"] + pos.get("part_pnl", 0.0)
    _pv = SNAP.get("last_ic_pv") or (0.0, 0.0)
    journal_close_trade(pos["db_id"], {
        "dt": day, "symbol": sym, "instrument_type": "EQUITY_INTRADAY", "side": pos["side"],
        "entry_time": pos["t_entry"], "exit_time": now.strftime("%H:%M:%S"),
        "entry": pos["entry"], "exit": ltp, "sl": pos["sl"], "tgt": pos["tgt"],
        "pts": round(pnl_rs / max(1, pos.get("qty0", pos["qty"] + pos.get("part_qty", 0))), 2), "pnl_rs": round(pnl_rs, 2),
        "part_pnl": pos.get("part_pnl", 0.0),
        "lots": pos["lots"], "lot_size": pos["lot_size"], "exit_reason": reason,
        "mfe": round(pos["mfe"], 2), "mae": round(pos["mae"], 2),
        "bull_pwr": pos["score"], "pcr": _pv[0], "vix": _pv[1],
        "mode": "DEMO" if demo_mode else "LIVE", "sl0": pos.get("sl0", pos["sl"]),
    })
    cd = SNAP.setdefault(f"stk_cd:{day}", {}).setdefault(sym, {"n": 0, "t": 0.0, "last_result": 0.0})
    cd["t"] = time.time()          # cooldown shuru (count entry par already badh chuka hai)
    cd["last_result"] = round(pnl_rs, 2)
    if "SL HIT" in str(reason) and pnl_rs < 0:
        cd["blocked"] = True       # SL laga -> aaj is stock me dobara entry nahi
    live_exit(day, sym, reason)    # asli position bhi band (agar live chal raha tha)
    del st_map[sym]
    TICK["hit"].pop(sym, None)
    return pnl_rs


def _run_stock_paper_engine_core(df: pd.DataFrame, ic: dict):
    """Strong Buy / Strong Sell wale F&O stocks ka live paper trade DB mein open, trail/update aur close karta hai."""
    if not auto_paper_stocks or df.empty:
        return
    persist = (not demo_mode) or bool(save_demo_db)
    if not persist:
        return

    now = now_ist()
    day = now.strftime("%Y-%m-%d")
    map_key = f"stk_paper:{day}"
    if map_key not in SNAP:
        SNAP[map_key] = fetch_open_stock_trades(day)
        load_sig_flags(SNAP[map_key])
    st_map = SNAP[map_key]
    SNAP["last_ic_pv"] = (ic.get("pcr") or 0.0, ic.get("vix") or 0.0)
    cd_key = f"stk_cd:{day}"
    if cd_key not in SNAP:
        SNAP[cd_key] = fetch_stock_trade_counts(day)

    # Best rank wale pehle: positions ki limit me sabse achhe signal ko jagah mile
    recs = sorted(df.to_dict("records"), key=lambda x: -safe_float(x.get("Rank"), -9.0))
    pend_map = SNAP.setdefault(f"stk_pend:{day}", {})
    tg_exit_syms = {str(x).upper() for x in (kv_get("tg_exit_req") or [])}      # Telegram /exit SYMBOL
    if tg_exit_syms:
        kv_set("tg_exit_req", [])
    # ---- Master-loop safety: kill switch / MAX LOSS / MAX SL HITS => saare khule trade square-off + din bhar band
    halt_why = stk_halt_reason(day)
    if not halt_why:
        day_pnl, _c, _n, day_sl = stk_day_stats(day, "DEMO" if demo_mode else "LIVE")
        if os.path.exists(KILL_FILE):
            halt_why = "KILL_SWITCH file mili"
        elif day_pnl <= -abs(float(stk_loss_limit)):
            halt_why = f"MAX LOSS: din ka P&L Rs {day_pnl:,.0f} <= -{abs(float(stk_loss_limit)):,.0f}"
        elif day_sl >= int(stk_max_sl_day):
            halt_why = f"MAX SL HITS: aaj {day_sl} stock SL hit ho chuke (limit {int(stk_max_sl_day)})"
        if halt_why:
            stk_set_halt(day, halt_why)
            if halt_why.startswith("MAX SL") and not str(halt_mode).startswith("Sab turant"):
                live_halt_set(day, True)                   # v7.9: sirf naye LIVE entry band; khule apne SL par
            else:
                live_square_off_all(day)                   # asli positions bhi band + live entries band
    _dp, _c0, _n0, _sl0 = stk_day_stats(day, "DEMO" if demo_mode else "LIVE")
    SNAP["stk_lock_why"] = stk_profit_guard(day, _dp)
    force_reason = ""
    if halt_why:
        force_reason = ("KILL SWITCH" if halt_why.startswith("KILL") else
                        "MAX LOSS HALT" if halt_why.startswith("MAX LOSS") else
                        "MAX SL HALT" if halt_why.startswith("MAX SL") else "MANUAL HALT")
    hard_halt = bool(force_reason) and not (force_reason == "MAX SL HALT" and not str(halt_mode).startswith("Sab turant"))

    def _halt_exit(sym, pos, mv) -> str:
        """v7.9: MAX SL HALT = naye trade band. Khula trade: profit me (ya SL pehle se entry par) => SL >= entry,
        trail par chalta rahe; loss me => band (ya 'sab chalne do' mode me apne SL par)."""
        if not force_reason:
            return ""
        if hard_halt:
            return force_reason
        if pos.get("halt_keep"):
            return ""
        d = 1 if pos["side"] == "LONG" else -1
        be_done = (d == 1 and pos["sl"] >= pos["entry"]) or (d == -1 and pos["sl"] <= pos["entry"])
        if mv > 0 or be_done or str(halt_mode).startswith("Sab khule"):
            pos["halt_keep"] = True
            if mv > 0:
                pos["sl"] = max(pos["sl"], pos["entry"]) if d == 1 else min(pos["sl"], pos["entry"])
            audit("HALT KEEP", sym, pos["side"], f"{force_reason}: khula rahega, SL {pos['sl']:.2f}, move {mv:+.2f}")
            send_telegram(f"🟢 {sym} {pos['side']} khula rahega ({force_reason}) | SL {pos['sl']:.2f} | trail par")
            return ""
        return force_reason
    pb_map = SNAP.setdefault(f"stk_pb:{day}", {})          # v7.6: pending pullback orders {sym: {...}}
    WHY = {}                                                  # v7.8.2: har stock ki "Kyun nahi lagi" wajah (is refresh ki)
    SNAP[f"stk_why:{day}"] = WHY

    def _w(sym, txt):
        WHY[sym] = txt

    def _gate_why(sym, now_t, lag, want="") -> str:
        """v7.8.2: entry ke common guards - pehli rukaawat ki wajah ('' = sab theek)."""
        if lag > 5.0:
            return f"⏳ Data purana (lag {lag:.1f} min > 5)"
        _g = _stk_entry_why(day, sym)
        if _g:
            return _g
        if len(st_map) >= int(max_open_pos):
            return f"⛔ Max {int(max_open_pos)} positions pehle se khuli"
        if not _stk_min_ok(day, now_t):
            return f"⏳ Is minute me {int(max_new_per_min)} entry ho chuki - agle minute"
        if SNAP.get("stk_lock_why"):
            return f"🔒 Profit lock: {SNAP['stk_lock_why']}"
        _x = burst_why(day) or (idx_dir_why(sym, want) if want else "")     # v7.9
        if _x:
            return _x
        return ""

    def _pend_end(sym, outcome, ltp_now=0.0, trade_id=0, note=""):
        """v7.8: pending signal khatam - confirm_log me record karo (sirf tab jab pending tha)."""
        p = pend_map.pop(sym, None)
        if p:
            if outcome.startswith("BROKEN") and p.get("conf"):
                outcome = "BROKEN (confirm hua, entry nahi)"
            confirm_log_write(day, sym, p, outcome, ltp_now, trade_id, note)
        return p

    def _pb_cancel(sym, why):
        o = pb_map.pop(sym, None)
        if o:
            o["status"], o["why"] = "CANCEL", why
            SNAP.setdefault(f"stk_pb_done:{day}", []).append({**o, "sym": sym, "t_end": now_ist().strftime("%H:%M:%S")})
            audit("PULLBACK CANCEL", sym, o["side"], why)

    def _open_entry(r, sym, want, ltp, sl_v, tgt_v, now_confirm, how: str = "", cinfo=None) -> bool:
        """Naya paper trade kholo (+ LIVE ho to asli order). False = kisi guard ne roka."""
        if not (sl_v > 0 and tgt_v > 0):
            _w(sym, "⚠ SL / Target calculate nahi hua")
            return False
        _xg = entry_extra_why(day, sym, want)               # v7.9: burst cooldown + index direction (aakhri check)
        if _xg:
            _w(sym, _xg)
            return False
        sig_want = want                                      # v7.9.1: signal ki disha
        if reverse_on and want in ("LONG", "SHORT"):
            want = "SHORT" if sig_want == "LONG" else "LONG"
            sl_v, tgt_v, _rd, _rlab = calc_sl_tgt(ltp, 1 if want == "LONG" else -1, r)
            if not (sl_v == sl_v and tgt_v == tgt_v and sl_v > 0 and tgt_v > 0):
                _w(sym, "⚠ Reverse: ulti disha ka SL / Target nahi bana")
                return False
            how = f"REVERSE (signal {sig_want}, SL {_rlab})" + (f" | {how}" if how else "")
        lot_sz = int(r.get("_lot") or 0)
        if lot_sz <= 0 or not C["fut"].get(sym):
            _w(sym, "⚠ F&O futures / lot size nahi mila")
            return False                         # sirf F&O list wale stock (active futures + lot size) - warna trade nahi
        if sl_v > 0 and tgt_v > 0:
            lots = 1
            if risk_sizing:
                _one_lot_risk = abs(ltp - sl_v) * lot_sz
                if _one_lot_risk > 0:
                    lots = int(max(1, min(int(max_lots_stk), float(risk_per_trade) // _one_lot_risk)))
            qty = lot_sz * lots              # 1 lot ke shares (ya risk sizing me lots x shares)
            if use_cap_qty:                  # Capital ke hisab se: shares = (capital x leverage / max positions) / LTP
                _cq = cap_qty(ltp)
                if _cq < 1:
                    _skip_log(now_confirm, sym, want, f"capital ke hisse (Rs {cap_alloc():,.0f}) se 1 share bhi nahi (LTP {ltp:.2f})")
                    _w(sym, f"💰 Capital kam: hisse Rs {cap_alloc():,.0f} me 1 share bhi nahi")
                    return False
                lots, lot_sz, qty = 1, _cq, _cq
            _ml_p = 0.0
            if float(ml_min_prob) > 0:
                _mdl = ml_model_get()
                if _mdl and _mdl.get("valid"):
                    _ml_p = ml_predict(_mdl, ml_feats(r, sig_want, ltp, now_confirm, safe_float(ic.get("vix"))))
                    if _ml_p < float(ml_min_prob):
                        _skip_log(now_confirm, sym, want, f"ML jeetne ki sambhavna {_ml_p:.2f} < {float(ml_min_prob):.2f}")
                        _w(sym, f"🤖 ML filter: jeetne ki sambhavna {_ml_p:.2f} < {float(ml_min_prob):.2f}")
                        return False
            _ok_r, _why_r = _stk_risk_ok(st_map, sym, want, abs(ltp - sl_v) * qty, ltp * qty)
            if not _ok_r:
                _skip_log(now_confirm, sym, want, _why_r)
                _w(sym, f"⛔ Risk guard: {_why_r}")
                return False
            sc_val = float(r.get("_score", 0))
            db_id = journal_open_trade({
                "dt": day, "symbol": sym, "instrument_type": "EQUITY_INTRADAY", "side": want,
                "entry_time": now_confirm.strftime("%H:%M:%S"), "entry": ltp, "sl": sl_v, "tgt": tgt_v,
                "lots": lots, "lot_size": lot_sz, "bull_pwr": sc_val,
                "pcr": (safe_float(r.get("Stock PCR")) if use_stock_pcr and pcr_filter_on else 0.0) or ic.get("pcr") or 0.0,
                "vix": ic.get("vix") or 0.0,
                "mode": "DEMO" if demo_mode else "LIVE",
                "adx": r.get("ADX (14)"), "volx": r.get("Vol Spike x"), "rs_idx": r.get("RS vs Index %"),
                "rank_v": r.get("Rank"), "atr_v": r.get("ATR (5m)"), "sector": sector_of(sym), "ml_prob": _ml_p,
            })
            st_map[sym] = {
                "db_id": db_id, "side": want, "entry": ltp, "sl": sl_v, "sl0": sl_v, "tgt": tgt_v,
                "peak": ltp, "lots": lots, "lot_size": lot_sz, "qty": qty,
                "t_entry": now_confirm.strftime("%H:%M:%S"), "mfe": 0.0, "mae": 0.0, "score": sc_val,
                "sector": sector_of(sym), "qty0": qty, "part_qty": 0, "part_pnl": 0.0, "partial_done": False,
                "_sl_logged": sl_v, "ikey": C["eq"].get(sym), "atr5": float(r.get("ATR (5m)") or 0.0),
                "sig": sig_want, "rev": want != sig_want,
            }
            journal_set_sig(db_id, sig_want)
            burst_record(day)                                # v7.9
            cd = SNAP[cd_key].setdefault(sym, {"n": 0, "t": 0.0, "last_result": 0.0})
            cd["n"] += 1
            _mk = SNAP.setdefault(f"stk_min:{day}", {})
            _mk[now_confirm.strftime("%H:%M")] = _mk.get(now_confirm.strftime("%H:%M"), 0) + 1
            _pc = _pend_end(sym, "ENTRY", ltp, db_id, how or "seedhi entry")
            journal_set_confirm(db_id, cinfo or _cinfo(_pc, "DIRECT"))
            if want != sig_want and LIVE_ARMED and not rev_live:
                audit("REVERSE PAPER-ONLY", sym, want, "reverse trade - LIVE order nahi bheja (rev_live OFF)")
            else:
                live_entry(day, sym, want, qty, ltp, sl_v, C["eq"].get(sym))   # LIVE ON ho to asli order
        if how:
            audit("ENTRY " + how, sym, want, f"entry {ltp:.2f} SL {sl_v:.2f} TGT {tgt_v:.2f}")
        _w(sym, f"✅ Entry ho gayi: {want} @ {ltp:.2f} ({now_confirm:%H:%M:%S})"
                + (f" - 🔄 REVERSE (signal {sig_want})" if want != sig_want else ""))
        return True

    for r in recs:
        sym = r["Symbol"]
        ltp = float(r.get("LTP") or 0.0)
        atr = float(r.get("ATR (5m)") or 0.0)
        if ltp <= 0:
            _w(sym, "⚠ LTP nahi mila")
            continue
        act = str(r.get("Final Action", ""))
        want = "LONG" if act.startswith("🟢 STRONG BUY") else ("SHORT" if act.startswith("🔻 STRONG SELL") else "FLAT")
        ext_side = "FLAT"
        if pb_on and pb_ext:                                          # v7.6: EXTENDED signal = pullback ka umeedwar
            ext_side = "LONG" if act.startswith("🟡 BUY (EXTENDED") else ("SHORT" if act.startswith("🟡 SELL (EXTENDED") else "FLAT")
        sig = want if want != "FLAT" else ext_side
        data_lag = safe_float(r.get("Data Lag (min)"))
        stale_row = str(r.get("Scan", "")).startswith("full-scan") or (not demo_mode and LIVE_MKT and data_lag > 5.0)
        if sig == "FLAT" and not stale_row:
            _pend_end(sym, "BROKEN (signal toota)", ltp, note=act[:60])   # signal toota -> confirm count reset

        # v7.6.3: pending pullback ke dauraan usi disha me SAAF STRONG signal => order hatao, seedhi entry ka raasta (neeche)
        if (sym in pb_map and sym not in st_map and not stale_row and want == pb_map[sym]["side"]
                and not pb_reason(r, want)):
            _o = pb_map.pop(sym)
            _o["status"], _o["why"] = "UPGRADE", "saaf STRONG signal - seedhi entry"
            SNAP.setdefault(f"stk_pb_done:{day}", []).append({**_o, "sym": sym, "t_end": now_ist().strftime("%H:%M:%S")})
            audit("PULLBACK UPGRADE", sym, want, f"saaf STRONG (RSI {safe_float(r.get('RSI (14)')):.0f}, vol {safe_float(r.get('Vol Spike x')):.2f}x) - seedhi entry")

        # 1. Existing OPEN trade management
        if sym in st_map:
            pos = st_map[sym]
            d = 1 if pos["side"] == "LONG" else -1
            if not pos.get("ikey"):
                pos["ikey"] = C["eq"].get(sym)
            if atr > 0:
                pos["atr5"] = atr
            # v7.9: tick feed - SL/target pehle tick par toota ho to WAHI price; warna fresh tick price (refresh LTP se naya)
            _hit = TICK["hit"].pop(sym, None)
            if _hit and _hit.get("db_id") != pos["db_id"]:
                _hit = None
            _tpx, _tage = tick_px(pos.get("ikey"))
            _tick_fresh = bool(_hit) or (_tpx > 0 and _tage <= 10.0)
            if _hit:
                ltp = float(_hit["px"])
            elif _tpx > 0 and _tage <= 10.0:
                ltp = _tpx
            _w(sym, f"✅ Position khuli: {pos['side']} @ {pos['entry']:.2f} (SL {pos['sl']:.2f}, TGT {pos['tgt']:.2f})")
            mv = (ltp - pos["entry"]) * d
            if not stale_row or _tick_fresh:
                mv = _pos_mark(pos, ltp, atr)
                r0 = abs(pos["entry"] - pos.get("sl0", pos["sl"])) or 1.0
                if partial_on and not pos.get("partial_done") and mv >= float(partial_r) * r0:
                    _pq = int(round(pos["qty"] * float(partial_pct) / 100.0))
                    if 1 <= _pq < pos["qty"]:
                        pos["part_pnl"] = pos.get("part_pnl", 0.0) + mv * _pq
                        pos["qty"] -= _pq
                        pos["part_qty"] = pos.get("part_qty", 0) + _pq
                        pos["partial_done"] = True
                        pos["sl"] = max(pos["sl"], pos["entry"]) if d == 1 else min(pos["sl"], pos["entry"])
                        journal_partial(pos["db_id"], pos["part_qty"], pos["part_pnl"])
                        trade_event(pos["db_id"], "PARTIAL", ltp, mv * _pq, f"{_pq} qty")
                        send_telegram(f"💰 {sym} PARTIAL {pos['side']} {_pq} qty @ {ltp:.2f} | Rs {mv * _pq:+,.0f} | baaki SL = entry")
                        if partial_live and LIVE_ARMED:
                            live_partial(day, sym, _pq)

            _hreason = _halt_exit(sym, pos, mv)                    # v7.9 soft halt (SL entry par la sakta hai)
            _sl_prev = pos.get("_sl_logged", pos["sl"])
            if abs(pos["sl"] - _sl_prev) > 1e-9:                    # trailing / breakeven se SL badla => chart ke liye record
                trade_event(pos["db_id"], "SL_MOVE", pos["sl"], _sl_prev, "trail / breakeven")
                pos["_sl_logged"] = pos["sl"]
            pos.setdefault("_sl_logged", pos["sl"])
            pnl_rs = mv * pos["qty"] + pos.get("part_pnl", 0.0)
            _weff = ({"LONG": "SHORT", "SHORT": "LONG"}.get(want, want) if pos.get("rev") else want)   # v7.9.1
            reason = _hreason or None
            if reason:
                pass                                       # kill / max loss / (MAX SL HALT par loss wala) : turant band
            elif sym.upper() in tg_exit_syms:
                reason = "TELEGRAM EXIT"
            elif not demo_mode and LIVE_MKT and data_lag > 5.0 and not _tick_fresh:
                reason = f"STALE DATA FORCE EXIT (lag {data_lag:.1f}m > 5m)"
            elif stale_row and not _tick_fresh:
                continue                                   # two-tier full-scan cache: agle watchlist refresh ka wait karo
            elif (d == 1 and ltp <= pos["sl"]) or (d == -1 and ltp >= pos["sl"]):
                reason = "SL HIT" if (mv < 0 and pnl_rs < 0) else "TRAIL SL HIT"
            elif (d == 1 and ltp >= pos["tgt"]) or (d == -1 and ltp <= pos["tgt"]):
                reason = "TARGET HIT"
            elif not stale_row and ((pos["side"] == "LONG" and _weff == "SHORT") or (pos["side"] == "SHORT" and _weff == "LONG")):
                reason = "OPPOSITE SIGNAL"
            elif not stale_row and int(time_stop_min) > 0 and _held_min(pos, now) >= int(time_stop_min) \
                    and mv < 0.3 * (abs(pos["entry"] - pos.get("sl0", pos["sl"])) or 1.0):
                reason = f"TIME STOP ({_held_min(pos, now):.0f}m, profit < 0.3R)"
            elif now.time() >= eod_exit and not demo_mode:
                reason = "EOD SQUARE-OFF"

            if reason:
                pnl_rs = _stk_close(day, sym, pos, ltp, reason, now, st_map)
                _w(sym, f"🔚 Trade band: {reason} (P&L Rs {pnl_rs:+,.0f})")
            else:
                journal_update_open_trade(pos["db_id"], ltp, pos["sl"], mv, pnl_rs, pos["mfe"], pos["mae"])
                live_trail(day, sym, pos["sl"])

        # 2a. v7.6 PULLBACK pending order: wapsi ka intezaar -> level par entry / cancel
        elif sym in pb_map:
            o = pb_map[sym]
            if stale_row:
                _w(sym, f"↩ Pullback order pending (level {o['level']:.2f}) - fresh data ka wait")
                continue
            now_pb = now_ist()
            d = 1 if o["side"] == "LONG" else -1
            opp = (want == "SHORT" and d == 1) or (want == "LONG" and d == -1) or \
                  (ext_side == "SHORT" and d == 1) or (ext_side == "LONG" and d == -1)
            sc_now = safe_float(r.get("_score"))
            if time.time() > o["exp"]:
                _pb_cancel(sym, f"{int(pb_valid_min)} min me price level ({o['level']:.2f}) tak nahi aaya")
            elif opp:
                _pb_cancel(sym, "ulta signal aa gaya")
            elif (d == 1 and ltp < o["inval"]) or (d == -1 and ltp > o["inval"]):
                _pb_cancel(sym, f"price {ltp:.2f} invalidation {o['inval']:.2f} ke paar - trend toota")
            elif int(safe_float(r.get("_mtf"))) == -d or sc_now * d < 0:
                _pb_cancel(sym, f"15m trend / score ulta ho gaya (score {sc_now:+.0f})")
            elif r.get("_lock") or not r.get("_ok"):
                _pb_cancel(sym, "result lock / data nahi")
            elif not (demo_mode or (LIVE_MKT and entry_start <= now_pb.time() <= entry_end)):
                _pb_cancel(sym, "entry window band")
            elif (d == 1 and ltp <= o["level"]) or (d == -1 and ltp >= o["level"]):
                if (data_lag <= 5.0 and _stk_entry_ok(day, sym) and len(st_map) < int(max_open_pos)
                        and _stk_min_ok(day, now_pb) and not SNAP.get("stk_lock_why")
                        and not entry_extra_why(day, sym, o["side"])):
                    sl_v, tgt_v, _d, _lab = calc_sl_tgt(ltp, d, r)
                    ok_e = _open_entry(r, sym, o["side"], ltp, sl_v, tgt_v, now_pb,
                                       f"PULLBACK @ {o['level']:.2f} (SL {_lab})", cinfo=o.get("cinfo"))
                    if ok_e:
                        o["status"], o["why"] = "FILLED", f"entry {ltp:.2f}"
                        SNAP.setdefault(f"stk_pb_done:{day}", []).append({**o, "sym": sym, "t_end": now_pb.strftime("%H:%M:%S")})
                        pb_map.pop(sym, None)
                        send_telegram(f"↩ {sym} PULLBACK {o['side']} @ {ltp:.2f} | SL {sl_v:.2f} ({_lab}) | TGT {tgt_v:.2f}")
                    else:
                        _pb_cancel(sym, "level aaya par risk/capital guard ne roka")
                else:
                    _w(sym, "↩ Pullback level aaya par ruka: " + (_gate_why(sym, now_pb, data_lag, o["side"]) or "guard"))
                # guard abhi band (positions full / per-min limit) => order zinda, agle refresh me dobara
            if sym in pb_map and sym not in WHY:
                _w(sym, f"↩ Pullback order: {o['side']} level {o['level']:.2f} ka intezaar (LTP {ltp:.2f}, "
                        f"cancel {o['inval']:.2f}) - {o.get('why', '')}")
            elif sym not in pb_map and sym not in WHY:
                _lastpb = next((x for x in reversed(SNAP.get(f"stk_pb_done:{day}", [])) if x.get("sym") == sym), None)
                if _lastpb and _lastpb.get("status") == "CANCEL":
                    _w(sym, f"❌ Pullback cancel: {_lastpb.get('why', '')}")

        # 2. New trade ENTRY when FLAT (sirf fresh data, risk limit, mid-day lull aur loss-cooldown check ke saath)
        elif sig in ("LONG", "SHORT"):
            _g0 = _stk_entry_why(day, sym)
            if _g0:
                _w(sym, _g0)
                _pend_end(sym, "GUARD (din ki limit / cooldown)", ltp)
                continue
            now_entry = now_ist()
            in_mid_lull = bool(f_mid and dtime(12, 0) <= now_entry.time() <= dtime(13, 15))
            vol_sp = safe_float(r.get("Vol Spike x"))
            sc_abs = abs(safe_float(r.get("_score")))
            req_score = int(stk_min_score) + (1 if in_mid_lull else 0)
            if in_mid_lull and (vol_sp < float(f_mid_vol) or sc_abs < req_score):
                _w(sym, f"🕛 Mid-day (12:00-13:15) filter: volume {vol_sp:.2f}x (chahiye {float(f_mid_vol):.2f}x) / "
                        f"score {sc_abs:.0f} (chahiye {req_score})")
                _pend_end(sym, "MID-DAY F6 block", ltp)
                continue
            # v7.8.2: wahi shartein jo pehle ek lambi 'and' me thi - ab ek-ek karke, taaki wajah dikh sake
            if not (demo_mode or (LIVE_MKT and entry_start <= now_entry.time() <= entry_end)):
                _blk0 = ("🕒 Market band" if not LIVE_MKT
                         else f"🕒 Entry window ke bahar ({entry_start:%H:%M}-{entry_end:%H:%M})")
            elif stale_row:
                _blk0 = ("⏳ Full-scan cache row - watchlist refresh me fresh data ka wait"
                         if str(r.get("Scan", "")).startswith("full-scan") else f"⏳ Data purana (lag {data_lag:.1f} min > 5)")
            elif sc_abs < req_score:
                _blk0 = f"📉 Score {sc_abs:.0f} < entry ke liye min score {req_score}"
            else:
                _blk0 = _gate_why(sym, now_entry, data_lag, sig)
            if _blk0:
                _w(sym, _blk0)
                continue
            if not _stk_confirmed(day, sym, sig, ltp):
                _pc_ = pend_map.get(sym) or {}
                _w(sym, f"⏳ Confirm cycle {int(_pc_.get('n', 1))}/{int(stk_confirm_n)} - agle refresh par signal bana raha to entry")
                continue
            # Confirmation cycles poora hone ke waqt dubara mid-day lull aur risk limits strictly verify karein
            now_confirm = now_ist()
            if f_mid and dtime(12, 0) <= now_confirm.time() <= dtime(13, 15):
                if vol_sp < float(f_mid_vol) or sc_abs < int(stk_min_score) + 1:
                    _w(sym, f"🕛 Mid-day (12:00-13:15) dobara check me ruka: volume {vol_sp:.2f}x / score {sc_abs:.0f}")
                    _pend_end(sym, "MID-DAY F6 block", ltp)
                    continue
            _g2 = _stk_entry_why(day, sym)
            if _g2:
                _w(sym, _g2)
                _pend_end(sym, "GUARD (din ki limit / cooldown)", ltp)
                continue
            if reverse_on and rev_no_pb and want == "FLAT":   # v7.9.1: reverse mode me sirf STRONG signal, pullback nahi
                _w(sym, "🔄 Reverse mode: EXTENDED signal skip (sirf STRONG par ulti entry)")
                _pend_end(sym, "REVERSE: EXTENDED skip", ltp)
                continue
            # v7.6: chase nahi - garam / kamzor-volume / EXTENDED signal par pullback order
            _pb_why = pb_reason(r, sig) if (pb_on and not (reverse_on and rev_no_pb)) else ""
            if want == "FLAT":                       # v7.6.1: EXTENDED se aaya - STRONG wali baaki shartein yahan
                _blk = str(r.get("_pb_block") or "") or str(r.get("_pb_pcr") or "")
                _sp = safe_float(r.get("Spread %"), float("nan"))
                if not _blk and spread_guard_on and _sp == _sp and _sp > float(max_spread_pct):
                    _blk = f"spread {_sp:.2f}% zyada"
                if _blk:
                    _w(sym, f"🚫 Pullback block: {_blk}")
                    _pend_end(sym, "PULLBACK BLOCK", ltp, note=_blk)
                    continue
            if pb_on and (want == "FLAT" or _pb_why):
                _pb_why = _pb_why or "EXTENDED"
                _lvl, _inv = pb_levels(r, 1 if sig == "LONG" else -1, ltp)
                _pc = _pend_end(sym, "PULLBACK ORDER" if _lvl is not None else "PULLBACK level nahi bana", ltp, note=_pb_why)
                if _lvl is None:
                    _w(sym, f"⚠ Pullback chahiye ({_pb_why}) par level nahi bana")
                    continue
                _w(sym, f"↩ Pullback order bana: {_pb_why} | level {_lvl:.2f} ka intezaar (LTP {ltp:.2f})")
                pb_map[sym] = {"side": sig, "level": _lvl, "inval": _inv, "t0": now_confirm.strftime("%H:%M:%S"),
                               "exp": time.time() + int(pb_valid_min) * 60, "ltp0": ltp, "why": _pb_why,
                               "score": safe_float(r.get("_score")), "status": "PENDING",
                               "cinfo": _cinfo(_pc, "PULLBACK")}
                audit("PULLBACK ORDER", sym, sig, f"{_pb_why} | level {_lvl:.2f} | cancel {_inv:.2f} | LTP {ltp:.2f}")
                send_telegram(f"⏳ {sym} {sig} pullback order: {_pb_why} | level {_lvl:.2f} (LTP {ltp:.2f}) | {int(pb_valid_min)} min valid")
                continue
            sl_v = safe_float(r.get("SL"), 0.0)
            tgt_v = safe_float(r.get("Target"), 0.0)
            _open_entry(r, sym, want, ltp, sl_v, tgt_v, now_confirm)


def run_stock_paper_engine(df: pd.DataFrame, ic: dict):
    """v7.9: engine ENGINE_LOCK ke andar (tick-thread ke saath takraav nahi), phir tick feed ko khule trade batao."""
    with ENGINE_LOCK:
        _run_stock_paper_engine_core(df, ic)
    _day = now_ist().strftime("%Y-%m-%d")
    _m = SNAP.get(f"stk_paper:{_day}") or {}
    TICK["tok"] = "" if demo_mode else (TOKEN or "")
    TICK["enabled"] = bool(tick_sl_on and not demo_mode and TOKEN)
    TICK["want"] = {p.get("ikey") for p in _m.values() if p.get("ikey")}
    if TICK["want"]:
        TICK["want_t"] = time.time()
    TICK["cb"] = _tick_on_px if TICK["enabled"] else None


# ====== SECTION: LIVE TRADING (Equity Intraday, Upstox orders) ======
# Product "I" = Intraday (equity cash). Entry MARKET, broker-side SL-M order, trail = SL modify,
# exit = SL cancel + MARKET. Switch sidebar me hai (default OFF).
@st.cache_resource
def _live_lock():
    return threading.Lock()


LIVE_LOCK = _live_lock()
ORDER_V3 = "https://api-hft.upstox.com/v3/order"
ORDER_V2 = "https://api.upstox.com/v2/order"
LIVE_ARMED = bool(live_on_cb and (live_confirm or "").strip().upper() == "LIVE" and TOKEN and not demo_mode)


def _live_hdr() -> dict:
    return {"Accept": "application/json", "Content-Type": "application/json", "Authorization": f"Bearer {TOKEN}"}


def _tick(x: float) -> float:
    return round(round(float(x) / 0.05) * 0.05, 2)


def _is_cancelled(s: str) -> bool:
    s = str(s).lower()
    return s.startswith("cancel") or s.startswith("reject")


def live_log(day, sym, action, side, qty, oid, status, msg=""):
    try:
        with db() as conn:
            conn.execute(
                "INSERT INTO live_orders (dt, ts, symbol, action, side, qty, order_id, status, msg) VALUES (?,?,?,?,?,?,?,?,?)",
                (day, now_ist().strftime("%H:%M:%S"), sym, action, side, int(qty or 0), str(oid or ""), status, str(msg)[:250]),
            )
    except Exception:
        pass
    if status == "FAILED" or (action in ("ENTRY", "EXIT", "SL EXECUTED (broker)") and status in ("PLACED", "COMPLETE")):
        send_telegram(f"🔴 LIVE {sym} {action} {side} x{qty} {status} {msg}"[:300])
    if status == "FAILED":
        msgs = SNAP.setdefault("live_msgs", [])
        msgs.append(f"{now_ist():%H:%M:%S} {sym} {action}: {msg}")
        del msgs[:-10]


def _live_fail(msg: str) -> None:
    """Lagataar 4 order fail => naye live entries band (Upstox/network/margin me kuch gadbad)."""
    SNAP["live_fail_n"] = SNAP.get("live_fail_n", 0) + 1
    if SNAP["live_fail_n"] >= 4 and not SNAP.get("live_halt"):
        live_halt_set(now_ist().strftime("%Y-%m-%d"), True)
        msgs = SNAP.setdefault("live_msgs", [])
        msgs.append(f"{now_ist():%H:%M:%S} 4 lagataar order fail ({msg}) - naye live entries BAND")
        del msgs[:-10]


def upx_place(ikey: str, side: str, qty: int, order_type: str = "MARKET", trigger: float = 0.0, tag: str = "TERM"):
    body = {"quantity": int(qty), "product": "I", "validity": "DAY", "price": 0, "tag": tag[:20],
            "instrument_token": ikey, "order_type": order_type, "transaction_type": side,
            "disclosed_quantity": 0, "trigger_price": float(trigger), "is_amo": False}
    last_err = ""
    for attempt in range(2):
        try:
            r = requests.post(f"{ORDER_V3}/place", headers=_live_hdr(), json=body, timeout=10)
            js = r.json() if r.content else {}
        except Exception as e:
            last_err = str(e)[:200]
            if attempt == 0:
                time.sleep(0.5)
                continue
            _live_fail(last_err)
            return False, "", last_err
        if r.status_code in (401, 403):                    # token expire/galat: live orders band
            SNAP["live_auth_err"] = True
            live_halt_set(now_ist().strftime("%Y-%m-%d"), True)
        data = js.get("data") or {}
        ids = data.get("order_ids") or []
        oid = ids[0] if ids else data.get("order_id", "")
        if r.status_code == 200 and oid:
            SNAP["live_fail_n"] = 0
            return True, str(oid), ""
        last_err = f"HTTP {r.status_code}: {str(js)[:200]}"
        if r.status_code in (429, 500, 502, 503, 504) and attempt == 0:
            time.sleep(0.6)
            continue
        break
    _live_fail(last_err)
    return False, "", last_err


def upx_status(oid: str) -> dict:
    try:
        r = requests.get(f"{ORDER_V2}/details", headers=_live_hdr(), params={"order_id": oid}, timeout=10)
        js = r.json() if r.content else {}
        return js.get("data") or {}
    except Exception:
        return {}


def upx_cancel(oid: str) -> bool:
    try:
        r = requests.delete(f"{ORDER_V3}/cancel", headers=_live_hdr(), params={"order_id": oid}, timeout=10)
        return r.status_code == 200
    except Exception:
        return False


def upx_modify_sl(oid: str, qty: int, trigger: float) -> bool:
    body = {"order_id": oid, "quantity": int(qty), "validity": "DAY", "price": 0, "order_type": "SL-M",
            "disclosed_quantity": 0, "trigger_price": float(trigger)}
    try:
        r = requests.put(f"{ORDER_V3}/modify", headers=_live_hdr(), json=body, timeout=10)
        return r.status_code == 200
    except Exception:
        return False


def live_halt_set(day: str, val: bool) -> None:
    SNAP["live_halt"] = bool(val)
    kv_set(f"live_halt:{day}", bool(val))


def _lp(day: str) -> dict:
    k = f"live_pos:{day}"
    if k not in SNAP:
        SNAP[k] = kv_get(k) or {}
    return SNAP[k]


def _lp_save(day: str) -> None:
    kv_set(f"live_pos:{day}", SNAP.get(f"live_pos:{day}", {}))


def live_entries_today(day: str) -> int:
    try:
        with db() as conn:
            row = conn.execute("SELECT COUNT(*) FROM live_orders WHERE dt = ? AND action = 'ENTRY' AND status = 'PLACED'",
                               (day,)).fetchone()
        return int(row[0])
    except Exception:
        return 0


def fetch_live_orders(day_iso: str) -> pd.DataFrame:
    try:
        with db() as conn:
            return pd.read_sql_query(
                'SELECT ts AS "Time", symbol AS "Symbol", action AS "Action", side AS "Side", qty AS "Qty", '
                'order_id AS "Order ID", status AS "Status", msg AS "Message" '
                "FROM live_orders WHERE dt = ? ORDER BY id DESC", conn, params=(day_iso,))
    except Exception:
        return pd.DataFrame()


def _live_do_exit(day: str, sym: str, p: dict, reason: str) -> None:
    """LIVE_LOCK pakad ke hi bulana. Pehle broker SL cancel, phir MARKET exit. Double-exit se bachta hai."""
    lp = _lp(day)
    p["exit_pending"] = reason
    exit_side = "SELL" if p["side"] == "LONG" else "BUY"
    if not p["filled"]:
        s = str(upx_status(p["entry_oid"]).get("status", "")).lower()
        if s == "complete":
            p["filled"] = True
        elif _is_cancelled(s):
            lp.pop(sym, None)
            return
        else:
            upx_cancel(p["entry_oid"])
            s2 = str(upx_status(p["entry_oid"]).get("status", "")).lower()
            if s2 == "complete":
                p["filled"] = True
            elif _is_cancelled(s2):
                live_log(day, sym, "ENTRY CANCEL", p["side"], p["qty"], p["entry_oid"], "CANCELLED", reason)
                lp.pop(sym, None)
                return
            else:
                return                      # agle cycle me phir try hoga
    if p.get("sl_oid"):
        s = str(upx_status(p["sl_oid"]).get("status", "")).lower()
        if s == "complete":
            live_log(day, sym, "SL EXECUTED (broker)", exit_side, p["qty"], p["sl_oid"], "COMPLETE", reason)
            lp.pop(sym, None)
            return
        if not _is_cancelled(s):
            upx_cancel(p["sl_oid"])
            s2 = str(upx_status(p["sl_oid"]).get("status", "")).lower()
            if s2 == "complete":
                live_log(day, sym, "SL EXECUTED (broker)", exit_side, p["qty"], p["sl_oid"], "COMPLETE", reason)
                lp.pop(sym, None)
                return
            if not _is_cancelled(s2):
                live_log(day, sym, "EXIT", exit_side, p["qty"], p["sl_oid"], "FAILED", "SL cancel nahi hua - retry")
                return
        p["sl_oid"] = ""
    ok, oid, msg = upx_place(p["ikey"], exit_side, p["qty"], "MARKET", 0.0, "TERMEXIT")
    if ok:
        live_log(day, sym, "EXIT", exit_side, p["qty"], oid, "PLACED", reason)
        lp.pop(sym, None)
    else:
        live_log(day, sym, "EXIT", exit_side, p["qty"], "", "FAILED", msg)


def live_exit(day: str, sym: str, reason: str) -> None:
    with LIVE_LOCK:
        p = _lp(day).get(sym)
        if p:
            _live_do_exit(day, sym, p, reason)
            _lp_save(day)


def live_entry(day: str, sym: str, side: str, qty: int, ltp: float, sl: float, ikey) -> None:
    """Paper entry ke saath hi ek asli equity-intraday MARKET order (qty = 1 lot ke shares)."""
    if not (LIVE_ARMED and ikey and qty > 0) or SNAP.get("live_halt"):
        return
    with LIVE_LOCK:
        lp = _lp(day)
        if sym in lp:
            return
        tx = "BUY" if side == "LONG" else "SELL"
        if live_entries_today(day) >= int(live_max_trades):
            live_log(day, sym, "ENTRY", tx, qty, "", "FAILED", f"Max live trades/din ({int(live_max_trades)}) ho gaye")
            return
        if qty * ltp > float(live_max_value):
            live_log(day, sym, "ENTRY", tx, qty, "", "FAILED", f"Order value Rs {qty * ltp:,.0f} > limit Rs {float(live_max_value):,.0f}")
            return
        ok, oid, msg = upx_place(ikey, tx, int(qty), "MARKET", 0.0, "TERMENTRY")
        if not ok:
            live_log(day, sym, "ENTRY", tx, qty, "", "FAILED", msg)
            return
        live_log(day, sym, "ENTRY", tx, qty, oid, "PLACED", f"{side} @ ~{ltp:.2f}, SL {sl:.2f}")
        lp[sym] = {"side": side, "qty": int(qty), "ikey": ikey, "entry_oid": oid, "filled": False,
                   "sl_oid": "", "sl_trig": 0.0, "sl": float(sl), "last_mod": 0.0, "sl_try": 0.0, "exit_pending": "",
                   "sig_px": float(ltp)}
        _lp_save(day)
    for _ in range(3):
        time.sleep(0.7)
        live_housekeeping(day, only=sym)
        if sym not in _lp(day) or _lp(day)[sym].get("filled"):
            break


def live_housekeeping(day: str, only=None) -> None:
    """Har cycle: entry fill check -> broker SL-M lagao; pending exits retry."""
    with LIVE_LOCK:
        lp = _lp(day)
        for sym in list(lp):
            if only and sym != only:
                continue
            p = lp[sym]
            if p.get("exit_pending"):
                _live_do_exit(day, sym, p, p["exit_pending"])
                continue
            if not p["filled"]:
                d_ = upx_status(p["entry_oid"])
                s = str(d_.get("status", "")).lower()
                if s == "complete":
                    p["filled"] = True
                    p["fill_t"] = time.time()
                    _avg, _slip = safe_float(d_.get("average_price")), ""
                    if _avg > 0 and p.get("sig_px"):
                        _cost = (_avg - p["sig_px"]) * (1 if p["side"] == "LONG" else -1) * p["qty"]
                        SNAP["live_slip_rs"] = SNAP.get("live_slip_rs", 0.0) + _cost
                        _slip = f" | signal {p['sig_px']:.2f} | slippage cost Rs {_cost:+,.0f}"
                    live_log(day, sym, "ENTRY FILL", p["side"], p["qty"], p["entry_oid"], "COMPLETE",
                             f"avg {d_.get('average_price')}{_slip}")
                elif _is_cancelled(s):
                    live_log(day, sym, "ENTRY", p["side"], p["qty"], p["entry_oid"], "FAILED",
                             f"Order {s}: {d_.get('status_message') or ''}")
                    lp.pop(sym, None)
                    continue
                else:
                    continue
            if p["filled"] and not p.get("sl_oid") and time.time() - p.get("fill_t", time.time()) > UNPROT_GRACE_SEC:
                live_log(day, sym, "UNPROTECTED", "", p["qty"], "", "FAILED",
                         f"{UNPROT_GRACE_SEC}s se broker SL nahi laga - position SQUARE-OFF")
                send_telegram(f"🚨 UNPROTECTED LIVE POSITION {sym} ({p['side']} x{p['qty']}): SL nahi laga, turant square-off kiya ja raha hai!")
                _live_do_exit(day, sym, p, "UNPROTECTED (SL nahi laga)")
                continue
            if p["filled"] and not p.get("sl_oid") and time.time() - p.get("sl_try", 0.0) >= SL_RETRY_SEC:
                p["sl_try"] = time.time()
                exit_side = "SELL" if p["side"] == "LONG" else "BUY"
                trig = _tick(p["sl"])
                ok, oid, msg = upx_place(p["ikey"], exit_side, p["qty"], "SL-M", trig, "TERMSL")
                if ok:
                    p["sl_oid"], p["sl_trig"] = oid, trig
                    live_log(day, sym, "SL ORDER", exit_side, p["qty"], oid, "PLACED", f"trigger {trig}")
                else:
                    live_log(day, sym, "SL ORDER", exit_side, p["qty"], "", "FAILED", msg)
                    send_telegram(f"🚨 {sym} Broker SL ORDER FAIL ({msg}) - UNPROTECTED position ko turant close karne ki koshish!")
                    _live_do_exit(day, sym, p, f"UNPROTECTED: SL order fail ({msg[:80]})")
        _lp_save(day)


def live_trail(day: str, sym: str, new_sl: float) -> None:
    with LIVE_LOCK:
        p = _lp(day).get(sym)
        if not p:
            return
        p["sl"] = float(new_sl)
        if not p.get("sl_oid"):
            return
        trig = _tick(new_sl)
        if abs(trig - p["sl_trig"]) >= 0.05 and time.time() - p.get("last_mod", 0.0) >= 20:
            if upx_modify_sl(p["sl_oid"], p["qty"], trig):
                live_log(day, sym, "SL MODIFY", "", p["qty"], p["sl_oid"], "COMPLETE", f"trigger {p['sl_trig']} -> {trig}")
                p["sl_trig"] = trig
            else:
                live_log(day, sym, "SL MODIFY", "", p["qty"], p["sl_oid"], "FAILED", f"trigger {trig}")
            p["last_mod"] = time.time()
            _lp_save(day)


def live_square_off_all(day: str) -> None:
    live_halt_set(day, True)
    for sym in list(_lp(day)):
        live_exit(day, sym, "KILL SWITCH")


def live_eod_flatten(day: str) -> None:
    """EOD par asli positions paper-engine se alag bhi band (paper trade band ho ya na ho)."""
    for sym in list(_lp(day)):
        live_exit(day, sym, "EOD SQUARE-OFF (live)")


def live_account_mtm_check(day: str) -> None:
    """Upstox account ka asli MTM (har 30s). live_max_loss se zyada loss => saare live position band + halt."""
    if demo_mode or not TOKEN or not (LIVE_ARMED or _lp(day)):
        return
    if time.time() - SNAP.get("live_mtm_t", 0.0) < 30:
        return
    SNAP["live_mtm_t"] = time.time()
    try:
        r = requests.get(f"{V2}/portfolio/short-term-positions", headers=_live_hdr(), timeout=10)
        if r.status_code in (401, 403):
            SNAP["live_auth_err"] = True
            return
        if r.status_code != 200:
            return
        tot = 0.0
        for x in (r.json().get("data") or []):
            tot += safe_float(x.get("pnl")) if x.get("pnl") is not None else safe_float(x.get("realised")) + safe_float(x.get("unrealised"))
        SNAP["live_mtm"] = tot
        if tot <= -abs(float(live_max_loss)) and not stk_halt_reason(day):
            stk_set_halt(day, f"MAX LOSS (Upstox account MTM Rs {tot:,.0f} <= -{abs(float(live_max_loss)):,.0f})")
            live_square_off_all(day)
    except Exception:
        pass


# ====== SECTION: GOOGLE SHEET SYNC ======
@st.cache_resource
def _gs_client():
    """Service-account se gspread client. Fail hone par exception (cache nahi hota)."""
    import gspread
    from google.oauth2.service_account import Credentials
    info = dict(st.secrets["gcp_service_account"])
    creds = Credentials.from_service_account_info(
        info, scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"])
    return gspread.authorize(creds)


def _gs_val(v):
    try:
        if v is None or (isinstance(v, float) and math.isnan(v)):
            return ""
        if isinstance(v, (np.integer,)):
            return int(v)
        if isinstance(v, (np.floating,)):
            return "" if math.isnan(float(v)) else float(v)
        return v if isinstance(v, (int, float)) else str(v)
    except Exception:
        return ""


def _gs_ws(sh, title: str, header: list):
    try:
        ws = sh.worksheet(title)
    except Exception:
        ws = sh.add_worksheet(title=title, rows=2000, cols=max(26, len(header)))
    try:
        if ws.col_count < len(header):
            ws.add_cols(len(header) - ws.col_count)
    except Exception:
        pass
    if ws.row_values(1) != [str(h) for h in header]:
        ws.update(values=[header], range_name="A1")
    return ws


def _gs_upsert(ws, rows: list):
    """rows[i][0] = unique Key. Purani key wali row update, nayi append."""
    if not rows:
        return
    def _col_letter(n):
        out = ""
        while n > 0:
            n, rem = divmod(n - 1, 26)
            out = chr(65 + rem) + out
        return out
    col_letter = _col_letter(len(rows[0]))
    pos = {v: i + 1 for i, v in enumerate(ws.col_values(1)) if i > 0}
    upd, new = [], []
    for r in rows:
        k = str(r[0])
        if k in pos:
            upd.append({"range": f"A{pos[k]}:{col_letter}{pos[k]}", "values": [r]})
        else:
            new.append(r)
    if upd:
        ws.batch_update(upd, value_input_option="USER_ENTERED")
    if new:
        ws.append_rows(new, value_input_option="USER_ENTERED")


def _gs_worker(gc, trade_rows: list, trade_header: list, sum_rows: list, sum_header: list, hashes: dict, dash=None):
    SNAP["gs_busy"] = True
    try:
        last_err = ""
        for attempt in range(3):
            try:
                sh = gc.open_by_key(GSHEET_ID)
                _gs_upsert(_gs_ws(sh, GS_TRADES_TAB, trade_header), trade_rows)
                _gs_upsert(_gs_ws(sh, GS_SUMMARY_TAB, sum_header), sum_rows)
                SNAP.setdefault("gs_hash", {}).update(hashes)
                if dash:
                    try:
                        _gs_dashboard(sh, dash)
                        SNAP["gs_dash_sig"] = dash.get("sig")
                        SNAP["gs_dash_err"] = ""
                    except Exception as e:
                        SNAP["gs_dash_err"] = str(e)[:250]
                SNAP["gs_err"] = ""
                SNAP["gs_ok_at"] = now_ist().strftime("%H:%M:%S")
                last_err = ""
                break
            except Exception as e:
                last_err = str(e)[:250]
                if attempt < 2:
                    time.sleep(5)
        if last_err:
            SNAP["gs_err"] = last_err
    finally:
        SNAP["gs_busy"] = False


def gsheet_sync(force_all: bool = False, blocking: bool = False):
    """Journal DB -> Google Sheet. Sirf badli hui rows bhejta hai (API quota bachane ke liye)."""
    if not gsheet_sync_on:
        return
    if SNAP.get("gs_busy") and not blocking:
        return
    if not force_all and time.time() - SNAP.get("gs_last", 0.0) < 20:
        return
    SNAP["gs_last"] = time.time()
    try:
        gc = _gs_client()
    except Exception as e:
        SNAP["gs_err"] = f"Credentials/secrets problem: {str(e)[:200]}"
        return
    jdf = fetch_journal(limit=5000 if force_all else 400)
    if jdf.empty:
        return
    t_header = ["Key"] + list(jdf.columns)
    old_h = {} if force_all else SNAP.get("gs_hash", {})
    t_rows, hashes = [], {}
    for rec in jdf.to_dict("records"):
        key = f"{rec['Date']}|{rec['Symbol']}|{rec['In']}|{rec['Side']}|{rec['Mode']}"
        vals = [_gs_val(rec[c]) for c in jdf.columns]
        h = tuple(vals)
        if old_h.get(key) != h:
            t_rows.append([key] + vals)
            hashes[key] = h
    if not t_rows:
        return
    s_header = ["Key", "Date", "Mode", "Total Trades", "Closed", "Open", "Wins", "Losses", "Win %",
                "Gross P&L Rs", "Open P&L Rs", "Best Trade Rs", "Worst Trade Rs"]
    s_rows = []
    for (dte, mde), g in jdf.groupby(["Date", "Mode"]):
        cl, op = g[g["Status"] == "CLOSED"], g[g["Status"] == "OPEN"]
        w, lo = int((cl["P&L Rs"] > 0).sum()), int((cl["P&L Rs"] <= 0).sum())
        s_rows.append([f"{dte}|{mde}", dte, mde, len(g), len(cl), len(op), w, lo,
                       round(w / len(cl) * 100, 1) if len(cl) else 0,
                       round(float(cl["P&L Rs"].sum()), 2), round(float(op["P&L Rs"].sum()), 2),
                       round(float(cl["P&L Rs"].max()), 2) if len(cl) else 0,
                       round(float(cl["P&L Rs"].min()), 2) if len(cl) else 0])
    dash = None
    try:
        dj = jdf if force_all else fetch_journal(limit=5000)
        cl = dj[dj["Status"] == "CLOSED"]
        sig = (len(cl), round(float(pd.to_numeric(cl["P&L Rs"], errors="coerce").fillna(0).sum()), 2))
        if force_all or sig != SNAP.get("gs_dash_sig"):
            dash = gs_dash_payload(dj)
            if dash:
                dash["sig"] = sig
    except Exception as e:
        SNAP["gs_dash_err"] = str(e)[:200]
    args = (gc, t_rows, t_header, s_rows, s_header, hashes, dash)
    if blocking:
        _gs_worker(*args)
    else:
        threading.Thread(target=_gs_worker, args=args, daemon=True).start()


# ====== SECTION: GOOGLE SHEET DASHBOARD (auto charts) ======
GS_DASH_TAB = "Dashboard"
GS_CALC_TAB = "Calc"
GS_BRK = 40.0          # brokerage Rs / trade (round trip) - dashboard ke Net P&L ke liye estimate
GS_CHG_PCT = 0.05      # charges + slippage % of turnover (estimate)
GS_NCOLS = 30


def _fnum(x, nd=2):
    try:
        v = float(x)
        return 0.0 if math.isnan(v) else round(v, nd)
    except Exception:
        return 0.0


def gs_dash_payload(jdf: pd.DataFrame):
    """Journal se KPI + insights + chart tables banata hai (sab python me - formulas ka risk nahi)."""
    if jdf is None or jdf.empty:
        return None
    closed = jdf[jdf["Status"] == "CLOSED"]
    if closed.empty:
        return None
    mode = "LIVE" if (closed["Mode"] == "LIVE").any() else "DEMO"
    d = closed[closed["Mode"] == mode].copy()
    d["P&L Rs"] = pd.to_numeric(d["P&L Rs"], errors="coerce").fillna(0.0)
    d = d.sort_values(["Date", "In"]).reset_index(drop=True)
    turn = d["Entry"].fillna(0) * d["Lots"].fillna(1) * d["LotSize"].fillna(1)
    d["Charges"] = GS_BRK + turn * GS_CHG_PCT / 100.0
    d["Net"] = d["P&L Rs"] - d["Charges"]
    n = len(d)
    wins, loss = d[d["Net"] > 0], d[d["Net"] <= 0]
    gp, gl = float(wins["Net"].sum()), abs(float(loss["Net"].sum()))
    pf = gp / gl if gl > 0 else (99.9 if gp > 0 else 0.0)
    cum = d["Net"].cumsum().values
    base = np.maximum.accumulate(np.r_[0.0, cum])[1:]
    mdd = float((cum - base).min()) if n else 0.0
    days = d["Date"].nunique()
    net, gross, chg = float(d["Net"].sum()), float(d["P&L Rs"].sum()), float(d["Charges"].sum())

    # ---- tables ----
    daily = d.groupby("Date").agg(Trades=("ID", "count"), Wins=("Net", lambda x: int((x > 0).sum())),
                                  Gross=("P&L Rs", "sum"), Net=("Net", "sum")).reset_index()
    daily["WinPct"] = (daily["Wins"] / daily["Trades"] * 100).round(1)
    daily["CumNet"] = daily["Net"].cumsum()
    daily = daily[["Date", "Trades", "Wins", "WinPct", "Gross", "Net", "CumNet"]]
    daily.columns = ["Date", "Trades", "Wins", "Win %", "Gross P&L", "Net P&L", "Cumulative Net"]

    def grp(col, label):
        g = d.groupby(col).agg(Trades=("ID", "count"), Net=("Net", "sum")).reset_index()
        g.columns = [label, "Trades", "Net P&L"]
        return g

    reason = grp("Reason", "Exit Reason").sort_values("Net P&L")
    sym = grp("Symbol", "Symbol").sort_values("Net P&L", ascending=False)
    if len(sym) > 15:
        sym = pd.concat([sym.head(8), sym.tail(7)])
    d["Hour"] = d["In"].astype(str).str[:2] + ":00"
    hour = grp("Hour", "Entry Hour").sort_values("Entry Hour")
    side = grp("Side", "Side")
    eq = pd.DataFrame({"Trade #": range(1, n + 1), "Cumulative Gross": d["P&L Rs"].cumsum().values,
                       "Cumulative Net": cum}).tail(2000)
    wl = pd.DataFrame({"Result": ["Profit trades", "Loss trades"], "Count": [len(wins), len(loss)]})

    # ---- insights (Hinglish) ----
    ins = []
    if net > 0:
        ins.append(f"✅ Abhi tak NET PROFIT: Rs {net:,.0f} ({n} trades, {days} din) - costs ke baad bhi.")
    else:
        ins.append(f"🔴 Abhi tak NET LOSS: Rs {net:,.0f} ({n} trades, {days} din). Gross Rs {gross:,.0f}, charges Rs {chg:,.0f}.")
    ins.append(f"Profit factor {pf:.2f} (1 se upar = achha) | Win rate {len(wins) / n * 100:.1f}% | "
               f"Avg win Rs {float(wins['Net'].mean()) if len(wins) else 0:,.0f} vs Avg loss Rs {float(loss['Net'].mean()) if len(loss) else 0:,.0f}")
    if n < 30:
        ins.append(f"⚠ Sirf {n} trades - abhi bahut kam. Kam se kam 30-50 trades / 20 din ke baad hi strategy ka faisla karo.")
    if len(hour) > 1:
        bh, wh = hour.sort_values("Net P&L").iloc[-1], hour.sort_values("Net P&L").iloc[0]
        ins.append(f"⏰ Sabse achha entry time: {bh['Entry Hour']} (Rs {bh['Net P&L']:,.0f}) | sabse kharab: {wh['Entry Hour']} (Rs {wh['Net P&L']:,.0f})")
    if len(sym) > 1:
        ins.append(f"📈 Best stock: {sym.iloc[0]['Symbol']} (Rs {sym.iloc[0]['Net P&L']:,.0f}) | 📉 Worst stock: "
                   f"{sym.iloc[-1]['Symbol']} (Rs {sym.iloc[-1]['Net P&L']:,.0f})")
    if len(reason) > 1:
        ins.append(f"🚪 Sabse zyada nuksaan wali exit: {reason.iloc[0]['Exit Reason']} (Rs {reason.iloc[0]['Net P&L']:,.0f}) | "
                   f"sabse achhi: {reason.iloc[-1]['Exit Reason']} (Rs {reason.iloc[-1]['Net P&L']:,.0f})")
    if len(side) > 1:
        ls = {r["Side"]: r["Net P&L"] for _, r in side.iterrows()}
        ins.append("↔  LONG vs SHORT: " + " | ".join(f"{k}: Rs {v:,.0f}" for k, v in ls.items()))
    if len(wins) and "MFE" in d.columns:
        mfe_w = float((d.loc[d["Net"] > 0, "MFE"].fillna(0) * d.loc[d["Net"] > 0, "Lots"].fillna(1) * d.loc[d["Net"] > 0, "LotSize"].fillna(1)).mean())
        ins.append(f"💡 Jeet wale trades me ausat Rs {mfe_w:,.0f} tak ka profit aaya tha, par mila Rs {float(wins['P&L Rs'].mean()):,.0f} - "
                   "farak bada ho to target/trailing dhyan se dekho.")
    if mdd < 0:
        ins.append(f"📉 Max drawdown: Rs {mdd:,.0f} - itna loss jhelne ki capital/hausla chahiye.")

    kpis = [
        ("Data mode", mode), ("Trades (closed)", n), ("Trading days", days),
        ("Profit trades", len(wins)), ("Loss trades", len(loss)), ("Win rate %", round(len(wins) / n * 100, 1)),
        ("Gross P&L Rs", _fnum(gross, 0)), ("Charges (est) Rs", _fnum(chg, 0)), ("NET P&L Rs", _fnum(net, 0)),
        ("Profit factor (net)", round(pf, 2)),
        ("Avg win Rs", _fnum(wins["Net"].mean() if len(wins) else 0, 0)),
        ("Avg loss Rs", _fnum(loss["Net"].mean() if len(loss) else 0, 0)),
        ("Expectancy / trade Rs", _fnum(net / n, 0)),
        ("Best trade Rs", _fnum(d["Net"].max(), 0)), ("Worst trade Rs", _fnum(d["Net"].min(), 0)),
        ("Max drawdown Rs", _fnum(mdd, 0)),
    ]

    # ---- grids ----
    tables = [(daily, 0), (reason, 8), (sym, 12), (hour, 16), (side, 20), (eq, 24), (wl, 28)]
    height = max(len(t) for t, _ in tables) + 1
    grid = [[""] * GS_NCOLS for _ in range(height)]
    sizes = {}
    for t, c0 in tables:
        for j, col in enumerate(t.columns):
            grid[0][c0 + j] = str(col)
        for i, rec in enumerate(t.itertuples(index=False), start=1):
            for j, v in enumerate(rec):
                grid[i][c0 + j] = _gs_val(v)
        sizes[c0] = len(t)

    dgrid = [[""] * 4 for _ in range(max(len(kpis), len(ins)) + 4)]
    dgrid[0][0] = "📊 STRATEGY DASHBOARD (apne aap update hota hai)"
    dgrid[1][0] = (f"Data: {mode} paper trades | Trades: {n} | Din: {days} | Updated: {now_ist():%Y-%m-%d %H:%M:%S} | "
                   f"Charges est: Rs {GS_BRK:.0f}/trade + {GS_CHG_PCT}% turnover")
    dgrid[3][0], dgrid[3][1], dgrid[3][3] = "KPI", "Value", "Insights - strategy kaise chal rahi hai"
    for i, (k, v) in enumerate(kpis):
        dgrid[4 + i][0], dgrid[4 + i][1] = k, _gs_val(v)
    for i, t in enumerate(ins):
        dgrid[4 + i][3] = t
    return {"calc_grid": grid, "dash_grid": dgrid, "sizes": sizes, "sig": None}


def _gs_chart_requests(dash_id: int, calc_id: int, sizes: dict) -> list:
    def rng(c, n, header=True):
        return {"sourceRange": {"sources": [{"sheetId": calc_id, "startRowIndex": 0 if header else 1,
                                             "endRowIndex": n + 1, "startColumnIndex": c, "endColumnIndex": c + 1}]}}

    def basic(title, ctype, dom_c, ser_cs, n, slot, x_title="", y_title=""):
        row, col = divmod(slot, 2)
        spec = {"title": title, "basicChart": {
            "chartType": ctype, "legendPosition": "BOTTOM_LEGEND" if len(ser_cs) > 1 else "NO_LEGEND",
            "axis": [{"position": "BOTTOM_AXIS", "title": x_title}, {"position": "LEFT_AXIS", "title": y_title}],
            "domains": [{"domain": rng(dom_c, n)}],
            "series": [{"series": rng(c, n), "targetAxis": "LEFT_AXIS"} for c in ser_cs],
            "headerCount": 1}}
        return {"addChart": {"chart": {"spec": spec, "position": {"overlayPosition": {
            "anchorCell": {"sheetId": dash_id, "rowIndex": 21 + row * 17, "columnIndex": 0},
            "offsetXPixels": col * 600, "widthPixels": 580, "heightPixels": 330}}}}}

    pie_spec = {"title": "Profit vs Loss trades", "pieChart": {
        "legendPosition": "RIGHT_LEGEND", "domain": rng(28, 2, header=False), "series": rng(29, 2, header=False)}}
    pie = {"addChart": {"chart": {"spec": pie_spec, "position": {"overlayPosition": {
        "anchorCell": {"sheetId": dash_id, "rowIndex": 21 + 3 * 17, "columnIndex": 0},
        "offsetXPixels": 600, "widthPixels": 580, "heightPixels": 330}}}}}
    s = sizes
    reqs = [
        basic("Cumulative P&L (trade by trade)", "LINE", 24, [25, 26], max(s[24], 1), 0, "Trade #", "Rs"),
        basic("Daily Net P&L", "COLUMN", 0, [5], max(s[0], 1), 1, "Date", "Rs"),
        basic("Daily Win Rate %", "COLUMN", 0, [3], max(s[0], 1), 2, "Date", "%"),
        basic("Net P&L by Exit Reason", "COLUMN", 8, [10], max(s[8], 1), 3, "Exit reason", "Rs"),
        basic("Net P&L by Stock (best/worst)", "COLUMN", 12, [14], max(s[12], 1), 4, "Stock", "Rs"),
        basic("Net P&L by Entry Hour", "COLUMN", 16, [18], max(s[16], 1), 5, "Hour", "Rs"),
        basic("LONG vs SHORT Net P&L", "COLUMN", 20, [22], max(s[20], 1), 6, "Side", "Rs"),
        pie,
    ]
    return reqs


def _gs_dashboard(sh, dash: dict) -> None:
    try:
        calc = sh.worksheet(GS_CALC_TAB)
    except Exception:
        calc = sh.add_worksheet(title=GS_CALC_TAB, rows=100, cols=GS_NCOLS)
    new_dash = False
    try:
        dws = sh.worksheet(GS_DASH_TAB)
    except Exception:
        dws = sh.add_worksheet(title=GS_DASH_TAB, rows=120, cols=12)
        new_dash = True
    grid = dash["calc_grid"]
    calc.clear()
    calc.resize(rows=max(len(grid) + 5, 50), cols=GS_NCOLS)
    calc.update(values=grid, range_name="A1")
    dws.clear()
    dws.update(values=dash["dash_grid"], range_name="A1")

    reqs = []
    meta = sh.fetch_sheet_metadata()
    for sm in meta.get("sheets", []):
        if sm["properties"]["sheetId"] == dws.id:
            for ch in sm.get("charts", []):
                reqs.append({"deleteEmbeddedObject": {"objectId": ch["chartId"]}})
    reqs += _gs_chart_requests(dws.id, calc.id, dash["sizes"])
    reqs.append({"updateDimensionProperties": {"range": {"sheetId": dws.id, "dimension": "COLUMNS",
                                                         "startIndex": 0, "endIndex": 1},
                                               "properties": {"pixelSize": 220}, "fields": "pixelSize"}})
    for r0 in (0, 3):
        reqs.append({"repeatCell": {"range": {"sheetId": dws.id, "startRowIndex": r0, "endRowIndex": r0 + 1},
                                    "cell": {"userEnteredFormat": {"textFormat": {"bold": True}}},
                                    "fields": "userEnteredFormat.textFormat.bold"}})
    sh.batch_update({"requests": reqs})
    if new_dash:
        try:
            dws.update_index(0)
        except Exception:
            pass


def send_day_summary(day: str) -> None:
    """Market band hone ke baad ek baar Telegram par din ka summary."""
    if demo_mode or not (tg_alerts and TG_TOKEN and TG_CHAT):
        return
    if now_ist().time() < dtime(15, 31) or kv_get(f"day_summary_sent:{day}"):
        return
    try:
        j = fetch_journal(limit=2000, status_filter="CLOSED", mode_filter="LIVE")
        j = j[j["Date"] == day] if not j.empty else j
        if j.empty:
            kv_set(f"day_summary_sent:{day}", True)
            return
        pnl = pd.to_numeric(j["P&L Rs"], errors="coerce").fillna(0.0)
        w, n = int((pnl > 0).sum()), len(j)
        rsn = j["Reason"].astype(str).str.split("(").str[0].str.strip().value_counts().head(4)
        msg = (f"📊 {day} DAY SUMMARY\nTrades {n} | Jeet {w} | Win {w / n * 100:.0f}%\n"
               f"Gross P&L Rs {pnl.sum():+,.0f} | Best {pnl.max():+,.0f} | Worst {pnl.min():+,.0f}\n"
               f"Exit: " + ", ".join(f"{k} {v}" for k, v in rsn.items()))
        if stk_halt_reason(day):
            msg += f"\nHalt: {stk_halt_reason(day)}"
        send_telegram(msg)
        kv_set(f"day_summary_sent:{day}", True)
    except Exception:
        pass


gsheet_sync_on = bool(gsheet_on_cb)
_day_now = now_ist().strftime("%Y-%m-%d")
if "live_halt" not in SNAP:
    SNAP["live_halt"] = bool(kv_get(f"live_halt:{_day_now}"))
if stk_resume:
    SNAP[f"stk_halt:{_day_now}"] = ""
    kv_set(f"stk_halt:{_day_now}", "")
_hb_now, _hb_last = time.time(), SNAP.get("hb_last")
if _hb_last and auto_refresh and LIVE_MKT and _hb_now - _hb_last > 120:     # app beech me ruka (EOD/SL ka khatra)
    SNAP.setdefault("hb_gaps", []).append((now_ist().strftime("%H:%M:%S"), int(_hb_now - _hb_last)))
SNAP["hb_last"] = _hb_now
sig = run_signal_engine(bull_pwr, bear_pwr, ictx)
run_stock_paper_engine(df_all, ictx)

WHY_COL = "Kyun nahi lagi"


def add_why_col(df: pd.DataFrame) -> pd.DataFrame:
    """v7.8.2: paper engine ne har stock par kya socha - scanner table me seedha dikhao."""
    if df is None or df.empty or "Final Action" not in df.columns:
        return df
    _day = now_ist().strftime("%Y-%m-%d")
    if not auto_paper_stocks:
        base = "⚙ Auto Paper-Trade OFF hai (sidebar)"
    elif demo_mode and not save_demo_db:
        base = "⚙ Demo mode me DB save OFF - paper trade nahi lagti"
    else:
        base = ""
    wm = SNAP.get(f"stk_why:{_day}", {}) or {}
    out = []
    for _r in df.to_dict("records"):
        _a = str(_r.get("Final Action", ""))
        _strong = _a.startswith(("🟢 STRONG", "🔻 STRONG"))
        if base and _strong:
            out.append(base)
        elif wm.get(_r.get("Symbol")):
            out.append(wm[_r["Symbol"]])
        else:
            out.append("— (engine ne abhi check nahi kiya)" if _strong else "")
    df = df.copy()
    df[WHY_COL] = out
    return df


df_all = add_why_col(df_all)

if not _IS_BG:
    _pb_day = now_ist().strftime("%Y-%m-%d")
    _pb_open, _pb_done = SNAP.get(f"stk_pb:{_pb_day}", {}), SNAP.get(f"stk_pb_done:{_pb_day}", [])
    with st.sidebar.expander(f"↩ Pullback orders: {len(_pb_open)} pending | {len(_pb_done)} band", expanded=bool(_pb_open)):
        if _pb_open:
            _ltp_now = dict(zip(df_all["Symbol"], df_all["LTP"])) if not df_all.empty else {}
            show_df(pd.DataFrame([{"Stock": k, "Side": v["side"], "Kyun": v["why"], "Level": v["level"], "Cancel": v["inval"],
                                        "LTP": _ltp_now.get(k), "Banaya": v["t0"],
                                        "Baaki min": max(0, int((v["exp"] - time.time()) / 60))} for k, v in _pb_open.items()])) 
        if _pb_done:
            st.caption("Aaj ke band orders")
            show_df(pd.DataFrame([{"Stock": x["sym"], "Side": x["side"], "Status": x["status"], "Kaaran": x["why"],
                                        "Level": x["level"], "Banaya": x["t0"], "Band": x.get("t_end", "")} for x in _pb_done[-30:]])) 
        if not _pb_open and not _pb_done:
            st.caption("Abhi koi pullback order nahi.")

_live_day = now_ist().strftime("%Y-%m-%d")
if live_resume:
    live_halt_set(_live_day, False)
    SNAP["live_fail_n"] = 0
    SNAP.pop("live_auth_err", None)
if live_kill:
    live_square_off_all(_live_day)
if not demo_mode and now_ist().time() >= eod_exit and _lp(_live_day):
    live_eod_flatten(_live_day)
live_account_mtm_check(_live_day)
if _lp(_live_day):
    live_housekeeping(_live_day)
gsheet_sync()
send_day_summary(_day_now)
ml_auto_train_if_due(_day_now)
collect_daily_pcr(_day_now)

# ---- HALT / safety status ----
_sh = stk_halt_reason(_day_now)
if _sh:
    st.error(f"⛔ **NAYE STOCK TRADE AAJ KE LIYE BAND**: {_sh}. Dobara chalu karna ho to sidebar me '🔓 halt hatao'."
             + (" Profit wale khule trade apne trail SL par chal rahe hain." if _sh.startswith("MAX SL") and not str(halt_mode).startswith("Sab turant") else ""))
if tick_sl_on and not demo_mode:
    _nws, _nrs = TICK.get("n_WS", 0), TICK.get("n_REST", 0)
    st.caption(f"⚡ Tick SL feed: WS {TICK.get('ws_status')} | REST {TICK.get('rest_status')} | ticks WS {_nws} / REST {_nrs} | "
               f"watch {len(TICK.get('want') or [])} trade" + (f" | cb error: {TICK['cb_err']}" if TICK.get("cb_err") else ""))
if burst_why(_day_now):
    st.info(burst_why(_day_now))
for _rk in SNAP.get("risk_skips", [])[-3:]:
    st.caption(f"🛡 Risk limit: {_rk}")
if SNAP.get("stk_lock_why"):
    st.info(f"💰 **NAYE TRADE BAND (profit/din bachao)**: {SNAP['stk_lock_why']}. Khule trade apne SL/target tak chalenge.")
if SNAP.get("live_mtm") is not None and LIVE_ARMED:
    st.caption(f"🏦 Upstox account MTM: Rs {SNAP['live_mtm']:,.0f} (max loss limit -{abs(float(live_max_loss)):,.0f})")
if os.path.exists(KILL_FILE):
    st.error(f"🛑 **{KILL_FILE}** file maujood hai - trading band. File hatao tabhi chalegi.")
if SNAP.get("live_auth_err"):
    st.error("🔒 Upstox token/auth error - LIVE orders band. Naya token daalo aur Upstox app me khuli positions KHUD check karo.")
for _g in SNAP.get("hb_gaps", [])[-2:]:
    st.warning(f"⏱ App {_g[1] // 60} min {_g[1] % 60} sec ruka raha ({_g[0]} par) - us beech SL/EOD check nahi hua. "
               "Computer sleep / network / hosting restart check karo.")

# ---- LIVE status ----
if LIVE_ARMED and not SNAP.get("live_halt"):
    sb.error("🔴 LIVE TRADING ACTIVE - asli orders ja rahe hain")
    st.error("🔴 **LIVE TRADING ACTIVE (Equity Intraday)** - signal aate hi Upstox ko asli order jayega. "
             "Band karne ke liye sidebar me LIVE off karo ya 🛑 button dabao.")
elif live_on_cb and SNAP.get("live_halt"):
    sb.warning("⏸ Live entries ruki hui hain (kill switch). '▶ dobara allow karo' dabao.")
elif live_on_cb:
    sb.warning("LIVE ON hai par confirm box me 'LIVE' likha nahi, ya token nahi / Demo mode hai.")
_pos_now = _lp(_live_day)
if _pos_now:
    st.warning("📌 Live open positions: " + ", ".join(f"{k} {v['side']} {v['qty']}" for k, v in _pos_now.items()))
for _m in SNAP.get("live_msgs", [])[-3:]:
    st.error(f"⚠ Live order problem: {_m}")

# ====== SECTION: TOP SUMMARY ======
m1, m2, m3, m4, m5, m6 = st.columns(6)
m1.metric(f"{PRIMARY_INDEX_NAME} Bull Power", f"{bull_pwr}%", delta="Bullish" if bull_pwr >= enter_th else "Below Thresh")
m2.metric(f"{PRIMARY_INDEX_NAME} Bear Power", f"{bear_pwr}%", delta="-Bearish" if bear_pwr >= enter_th else "Below Thresh")
m3.metric("Data Coverage", f"{coverage}%", delta="OK" if coverage >= min_cov else "LOW")
m4.metric("India VIX", f"{ictx['vix']:.2f}" if ictx["vix"] else "N/A", delta=f"{ictx['vix_chg']:+.2f}%" if ictx["vix"] else None,
          delta_color="inverse")
m5.metric(f"< {max_monthly_move_th:.0f}% Monthly Movers", f"{low_vol_count} / {len(df_all)}")
m6.metric("🔴 Result Lock", f"{len(result_wk_stocks)} Stocks")

if TWO_TIER:
    _nxt = max(0, int(SNAP.get("last_full", time.time()) + int(full_scan_min) * 60 - time.time()))
    _wl = SNAP.get("watch", [])
    st.info(f"🔁 Mode: **{'FULL SCAN' if FULL_SCAN else 'WATCHLIST ONLY'}** | Watchlist ({len(_wl)}): "
            f"{', '.join(_wl) or 'koi final share nahi'} | Next full rescan: {_nxt // 60:02d}:{_nxt % 60:02d} | "
            f"API calls (60s): {api_calls_last(60)}")
if not pcr_filter_on:
    st.caption("📊 PCR filter OFF (v7.7) - PCR sirf jaankari ke liye dikhta hai, entry block nahi karta.")
elif pcr_filter_on and use_stock_pcr:
    st.caption("📊 PCR: har stock ka apna (option chain) - Scanner me 'Stock PCR' column dekho. Index PCR stock entry me use nahi hota.")
elif pcr_filter_on:
    _pc, _pd = ictx.get("pcr"), ictx.get("pcr_delta")
    if _pc is None:
        st.caption("📊 PCR available nahi - normal route band, sirf Solo Mover Override se entry.")
    else:
        _lo, _sh_ = pcr_route(ictx, 1)[0], pcr_route(ictx, -1)[0]
        st.caption(f"📊 PCR {_pc:.2f}" + (f" ({_pd:+.2f})" if _pd is not None else "") +
                   f" → LONG normal: {'✅' if _lo else '❌'} | SHORT normal: {'✅' if _sh_ else '❌'}"
                   + ("" if (_lo or _sh_) else " | PCR beech me - sirf SOLO OVERRIDE wale stock"))
if MKT_CHOP and not basis_stock:
    st.warning("🟠 **MARKET CHOPPY - NO TRADE ZONE**: naye stock trade band. Karan: " + " | ".join(MKT_CHOP_WHY))
elif MKT_CHOP:
    st.caption("ℹ Index choppy hai (sirf jaankari) - stock entry par asar nahi; har stock ka apna choppy check chalta hai. Karan: " + " | ".join(MKT_CHOP_WHY))
if result_wk_stocks:
    st.error(f"🚨 **RESULT NO-TRADE WARNING** (`{lock_mode}` rule): **{', '.join(result_wk_stocks)}**")
if stale_cnt:
    st.warning(f"⏱ {stale_cnt} stocks ka data 5 min se zyada purana hai (API lag/limit) - signals dhyan se lein.")
if zone_filter and not df_all.empty:
    zn = df_all[df_all["_zone"]]["Symbol"].tolist()
    if zn:
        st.warning(f"🟠 **15m CONSOLIDATION - NO TRADE ZONE** ({len(zn)} stocks): {', '.join(zn)}")
if df_all.empty:
    st.warning("Koi stock data nahi aaya. Token/instrument map check karein (Diagnostics tab dekhein).")

# Filters for display
df_display = df_all.copy()
if ss["only_low_vol_10"] and not df_display.empty:
    df_display = df_display[(df_display["1M Move %"] > 0) & (df_display["1M Move %"] < max_monthly_move_th)]
    st.success(f"📉 **Filtered:** sirf < {max_monthly_move_th:.1f}% monthly move wale shares ({len(df_display)} stocks).")
if use_range_filter and not df_display.empty:
    df_display = df_display[(df_display["Avg Range Rs"] >= rng_min) & (df_display["Avg Range Rs"] <= rng_max)]
    st.info(f"📏 Avg daily range Rs {rng_min:.0f}-{rng_max:.0f} filter active ({len(df_display)} stocks).")


# ====== SECTION: STYLING ======
def highlight_result_and_signals(row):
    if row.get("Result Trade Lock") == LOCK_TXT:
        return ["background-color: rgba(255, 43, 43, 0.22); color: #ff4b4b; font-weight: bold;"] * len(row)
    styles = [""] * len(row)
    for idx, col_name in enumerate(row.index):
        v = str(row[col_name])
        if col_name in ("Final Action", "15m Zone") and "ZONE" in v and "toota" not in v:
            styles[idx] = "background-color: rgba(255, 152, 0, 0.22); color: #ffb74d; font-weight: bold;"
        elif col_name == "Final Action":
            if "STRONG BUY" in v:
                styles[idx] = "background-color: rgba(0, 200, 83, 0.20); color: #00e676; font-weight: bold;"
            elif "STRONG SELL" in v:
                styles[idx] = "background-color: rgba(255, 82, 82, 0.20); color: #ff5252; font-weight: bold;"
            elif "EXTENDED" in v or "against" in v:
                styles[idx] = "background-color: rgba(255, 193, 7, 0.18); color: #ffd54f; font-weight: bold;"
        elif col_name.startswith("Low Vol") and "YES" in v:
            styles[idx] = "background-color: rgba(33, 150, 243, 0.18); color: #64b5f6; font-weight: bold;"
    return styles


FMT = {"Weight %": "{:.2f}%", "LTP": "{:.2f}", "Day %": "{:+.2f}%", "RS vs Index %": "{:+.2f}%", "1M Move %": "{:.2f}%",
       "Avg Range Rs": "{:.2f}", "RSI (14)": "{:.1f}", "ADX (14)": "{:.1f}", "Vol Spike x": "{:.2f}", "ATR (5m)": "{:.2f}",
       "SL": "{:.2f}", "Target": "{:.2f}", "Lots": "{:.0f}", "Qty": "{:.0f}", "Rank": "{:.2f}", "OI Chg %": "{:+.2f}%",
       "Data Lag (min)": "{:.1f}", "Zone Lo": "{:.2f}", "Zone Hi": "{:.2f}",
       "Spread %": "{:.2f}%", "Stock PCR": "{:.2f}", "PCR 20d avg": "{:.2f}", "PCR band ±": "{:.2f}", "PCR Δ(10m)": "{:+.2f}", "ΔOI PCR": "{:.2f}",
       "PCR total OI (lots)": "{:,.0f}", "Bull Power %": "{:.0f}%", "Bear Power %": "{:.0f}%",
       "PCR base (avg)": "{:.2f}", "Base din": "{:.0f}", "VWAP": "{:.2f}", "ATR (15m)": "{:.2f}", "Sector Day %": "{:+.2f}%"}
SHOW_ORDER = ["Symbol", "Exch", "Scan", "Final Action", WHY_COL, "Entry Route", "Spread %", "Bull Power %", "Bear Power %", "Stock PCR", "PCR 20d avg", "PCR band ±", "PCR Δ(10m)", "ΔOI PCR", "PCR base (avg)", "Base din", "OI Writing", "PCR total OI (lots)", "PCR Status", "Filter Score (-8..+8)", "Rank", "LTP", "VWAP", "ATR (15m)", "Day %", "Sector", "Sector Day %", "RS vs Index %", "Idx Align", "15m Zone", "Zone Lo", "Zone Hi",
              "SL", "Target", "Lots", "Qty", "1M Move %", lv_col, "Avg Range Rs", "Result Date", "Result Week",
              "Date Source", "Result Trade Lock", "5m EMA (9/21)", "15m MTF", "VWAP Status", "ORB (15m)", "RSI (14)",
              "ADX (14)", "Vol Spike x", "ATR (5m)", "F&O OI Buildup", "OI Chg %", "Weight %", "Data Lag (min)"]


def styled(df: pd.DataFrame):
    cols = [c for c in SHOW_ORDER if c in df.columns]
    d = df[cols]
    fm = {k: v for k, v in FMT.items() if k in d.columns}
    return d.style.apply(highlight_result_and_signals, axis=1).format(fm, na_rep="—")


# ====== SECTION: DAY REPORT + UPSTOX REAL TRADES (helpers) ======
def _color_pnl(s):
    return ["color: #00e676; font-weight: bold;" if (isinstance(v, (int, float)) and v > 0)
            else "color: #ff5252; font-weight: bold;" if (isinstance(v, (int, float)) and v < 0) else ""
            for v in s]


def upstox_get(path: str, tok: str):
    """Read-only Upstox call (orders/portfolio endpoints). Koi order place nahi hota."""
    try:
        r = requests.get(
            V2 + path,
            headers={"Accept": "application/json", "Authorization": f"Bearer {tok}"},
            timeout=10,
        )
        try:
            js = r.json()
        except Exception:
            js = {}
        return r.status_code, js
    except Exception as e:
        return 0, {"error": str(e)}


def pair_trades_fifo(trades: list) -> tuple:
    """Upstox ke BUY/SELL fills ko FIFO se round-trip trades me jodta hai."""
    def ts_of(t):
        return str(t.get("exchange_timestamp") or t.get("order_timestamp") or "")

    by = defaultdict(list)
    for t in sorted(trades, key=ts_of):
        by[t.get("trading_symbol") or t.get("instrument_token")].append(t)

    out, still_open = [], []
    for sym, lst in by.items():
        book = deque()  # (side, qty, price, ts)
        for t in lst:
            side = str(t.get("transaction_type", "")).upper()
            q = int(t.get("quantity") or 0)
            p = float(t.get("average_price") or 0.0)
            ts = ts_of(t)
            while q > 0 and book and book[0][0] != side:
                s0, q0, p0, t0 = book[0]
                m = min(q, q0)
                pnl = (p - p0) * m if s0 == "BUY" else (p0 - p) * m
                out.append({
                    "Symbol": sym, "Side": "LONG" if s0 == "BUY" else "SHORT", "Qty": m,
                    "Entry Time": t0[-8:], "Exit Time": ts[-8:],
                    "Entry": round(p0, 2), "Exit": round(p, 2), "Gross P&L Rs": round(pnl, 2),
                })
                q -= m
                if m == q0:
                    book.popleft()
                else:
                    book[0] = (s0, q0 - m, p0, t0)
            if q > 0:
                book.append((side, q, p, ts))
        for s0, q0, p0, t0 in book:
            still_open.append({"Symbol": sym, "Side": "LONG" if s0 == "BUY" else "SHORT",
                               "Open Qty": q0, "Avg Price": round(p0, 2), "Since": t0[-8:]})
    return pd.DataFrame(out), pd.DataFrame(still_open)


def render_day_report():
    st.subheader("📒 Day Report - poore din ke trades ek jagah")

    c1, c2, c3, c4 = st.columns(4)
    day = c1.date_input("Date", value=today_date, key="dr_day")
    mode = c2.selectbox("Mode", ["ALL", "LIVE", "DEMO"], index=0, key="dr_mode")
    brk = c3.number_input("Brokerage Rs / trade (round trip)", value=40.0, min_value=0.0, step=5.0, key="dr_brk")
    cpct = c4.number_input("Charges + slippage % of turnover", value=0.05, min_value=0.0, step=0.01, key="dr_cp",
                           help="Estimate hai (STT, exchange, GST, slippage). Apne contract note se match karke badlo.")

    jdf = fetch_journal(limit=5000, mode_filter=mode)
    d = pd.DataFrame() if jdf.empty else jdf[jdf["Date"] == day.isoformat()].copy()

    if d.empty:
        st.info(f"{day} ko koi paper trade record nahi hai.")
    else:
        d = d.sort_values("In").reset_index(drop=True)
        d["Turnover"] = d["Entry"] * d["Lots"].fillna(1) * d["LotSize"].fillna(1)
        d["Charges"] = (brk + d["Turnover"] * cpct / 100.0).round(2)
        d["Net P&L"] = (d["P&L Rs"].fillna(0.0) - d["Charges"]).round(2)
        if "Signal" in d.columns:                          # v7.9.1: signal ki disha me lete to (same entry/exit)
            _rv = d["Signal"].isin(["LONG", "SHORT"]) & (d["Signal"] != d["Side"])
            d["Signal-side Net"] = np.where(_rv, (-d["P&L Rs"].fillna(0.0) - d["Charges"]).round(2), d["Net P&L"])

        def _mins(r):
            try:
                a = pd.to_datetime(f"{r['Date']} {r['In']}")
                b = pd.to_datetime(f"{r['Date']} {r['Out']}")
                return round((b - a).total_seconds() / 60.0, 1)
            except Exception:
                return float("nan")
        d["Mins"] = d.apply(_mins, axis=1)

        closed = d[d["Status"] == "CLOSED"].copy()
        opened = d[d["Status"] == "OPEN"].copy()
        wins, losses = closed[closed["Net P&L"] > 0], closed[closed["Net P&L"] <= 0]
        gross = float(closed["P&L Rs"].sum()) if not closed.empty else 0.0
        chg = float(closed["Charges"].sum()) if not closed.empty else 0.0
        net = float(closed["Net P&L"].sum()) if not closed.empty else 0.0
        gw, gl = float(wins["Net P&L"].sum()), abs(float(losses["Net P&L"].sum()))
        pf = gw / gl if gl > 0 else (99.9 if gw > 0 else 0.0)
        wr = len(wins) / len(closed) * 100.0 if not closed.empty else 0.0
        exp = net / len(closed) if not closed.empty else 0.0

        a = st.columns(6)
        a[0].metric("Total trades", len(d), delta=f"{len(closed)} closed / {len(opened)} open")
        a[1].metric("Profit trades", len(wins))
        a[2].metric("Loss trades", len(losses))
        a[3].metric("Win rate", f"{wr:.1f}%")
        a[4].metric("Gross P&L", f"₹{gross:+,.0f}")
        a[5].metric("NET P&L (costs ke baad)", f"₹{net:+,.0f}", delta=f"charges ₹{chg:,.0f}", delta_color="inverse")
        b = st.columns(6)
        b[0].metric("Profit factor", f"{pf:.2f}")
        b[1].metric("Expectancy / trade", f"₹{exp:+,.0f}")
        b[2].metric("Best trade", f"₹{closed['Net P&L'].max():+,.0f}" if not closed.empty else "-")
        b[3].metric("Worst trade", f"₹{closed['Net P&L'].min():+,.0f}" if not closed.empty else "-")
        if not closed.empty:
            cum = closed.sort_values("Out")["Net P&L"].cumsum()
            b[4].metric("Max drawdown", f"₹{float((cum - cum.cummax()).min()):,.0f}")
        b[5].metric("Open running P&L", f"₹{float(opened['P&L Rs'].sum()):+,.0f}" if not opened.empty else "₹0")

        if not closed.empty:
            if net < 0 and gross > 0:
                st.warning("⚠ Gross profit tha lekin brokerage/charges ke baad NET loss - strategy ka edge costs se chhota hai.")
            elif net < 0:
                st.error("🔴 Aaj ka NET result loss me hai.")
            else:
                st.success("🟢 NET result profit me hai. (Ek din se strategy prove nahi hoti - kam se kam 20-30 din ka data dekho.)")

        if "Signal-side Net" in closed.columns:
            _rc = closed[closed["Signal"].isin(["LONG", "SHORT"]) & (closed["Signal"] != closed["Side"])]
            if not _rc.empty:
                st.info(f"🔄 Reverse trades: {len(_rc)} | inka NET ₹{float(_rc['Net P&L'].sum()):+,.0f} | "
                        f"agar signal ki disha me lete (same entry/exit): ₹{float(_rc['Signal-side Net'].sum()):+,.0f} | "
                        f"reverse jeeta {int((_rc['Net P&L'] > 0).sum())}/{len(_rc)}. 30+ trade ke baad hi faisla karo.")
        cols = ["In", "Out", "Mins", "Symbol", "Type", "Side", "Signal", "Status", "Entry", "LTP/Exit", "SL", "Target",
                "Reason", "Pts", "P&L Rs", "Charges", "Net P&L", "Signal-side Net", "MFE", "MAE", "Mode", "Special Note"]
        cols = [c for c in cols if c in d.columns]
        st.markdown("#### 🕒 Trade timeline (entry time → exit time)")
        show_df(d[cols].style.apply(_color_pnl, subset=["P&L Rs", "Net P&L", "Pts"]).format(
            {"Entry": "{:.2f}", "LTP/Exit": "{:.2f}", "SL": "{:.2f}", "Target": "{:.2f}", "P&L Rs": "{:+,.0f}",
             "Net P&L": "{:+,.0f}", "Signal-side Net": "{:+,.0f}", "Charges": "{:.0f}", "Pts": "{:+.2f}"}, na_rep="—"))

        if not closed.empty:
            st.markdown("#### 🔻 Sabse bade 5 loss (kab aur kyun)")
            show_df(closed.sort_values("Net P&L").head(5)[["In", "Out", "Symbol", "Side", "Entry", "LTP/Exit",
                                                           "Reason", "Net P&L", "MFE", "MAE"]])
            g1, g2, g3 = st.columns(3)
            closed["Hour"] = closed["In"].astype(str).str[:2] + ":00"
            with g1:
                st.markdown("**Entry-hour wise**")
                show_df(closed.groupby("Hour").agg(Trades=("ID", "count"), Net=("Net P&L", "sum"),
                                                   Win_Pct=("Net P&L", lambda x: round((x > 0).mean() * 100, 1)))
                        .round(0).reset_index())
            with g2:
                st.markdown("**Symbol wise**")
                show_df(closed.groupby(["Symbol", "Side"]).agg(Trades=("ID", "count"), Net=("Net P&L", "sum"))
                        .round(0).reset_index().sort_values("Net"))
            with g3:
                st.markdown("**Exit reason wise**")
                show_df(closed.groupby("Reason").agg(Trades=("ID", "count"), Net=("Net P&L", "sum"))
                        .round(0).reset_index().sort_values("Net"))
            if len(closed) >= 2:
                eq = closed.sort_values("Out").copy()
                eq["Cumulative Net P&L"] = eq["Net P&L"].cumsum()
                st.markdown("#### 💹 Intraday equity curve")
                st.line_chart(eq.reset_index(drop=True)["Cumulative Net P&L"])

        st.download_button("⬇ Download Day Report CSV", d[cols].to_csv(index=False).encode("utf-8"),
                           file_name=f"day_report_{day.isoformat()}.csv", mime="text/csv")

    st.divider()
    st.markdown("### 🔴 Live order log (Upstox ko bheje gaye orders)")
    if SNAP.get("live_slip_rs") is not None:
        st.caption(f"Aaj ki live entry slippage ka total cost: Rs {SNAP['live_slip_rs']:+,.0f} (+ = signal price se mehnga fill)")
    _lo = fetch_live_orders(day.isoformat())
    if _lo.empty:
        st.info("Is din koi live order nahi bheja gaya.")
    else:
        show_df(_lo)
    st.divider()
    st.markdown("### 📊 Google Sheet sync")
    st.caption(f"Sheet: https://docs.google.com/spreadsheets/d/{GSHEET_ID}  |  Tabs: {GS_DASH_TAB} (graphs), {GS_TRADES_TAB}, {GS_SUMMARY_TAB}, {GS_CALC_TAB}")
    if not gsheet_sync_on:
        st.info("Sidebar me 'Google Sheet auto-sync' off hai.")
    elif SNAP.get("gs_err"):
        st.error(f"Sheet sync error: {SNAP['gs_err']}")
    elif SNAP.get("gs_ok_at"):
        st.success(f"Last sync OK: {SNAP['gs_ok_at']}")
    else:
        st.info("Abhi tak sync nahi hua (naya trade/badlav aate hi chalega).")
    if SNAP.get("gs_dash_err"):
        st.error(f"Dashboard error: {SNAP['gs_dash_err']}")
    if st.button("⬆ Poori history + 📊 Dashboard Google Sheet me abhi banao / refresh karo", key="gs_full"):
        with st.spinner("Sheet update ho rahi hai..."):
            gsheet_sync(force_all=True, blocking=True)
        st.rerun()

    # ---------------------------------------------------- real Upstox account
    st.divider()
    st.markdown("### 🏦 Upstox account ke ASLI trades (aaj, read-only)")
    st.caption("Yeh sirf data padhta hai, order nahi dalta. 401 aaye to token me order/portfolio access nahi hai "
               "(market-data-only token se yeh endpoints nahi chalte) ya token expire ho gaya.")
    if demo_mode or not TOKEN:
        st.info("Token daalo (Demo mode me yeh section off hai).")
        return
    if st.button("🔄 Upstox se aaj ke trades fetch karo", key="dr_fetch"):
        code, js = upstox_get("/order/trades/get-trades-for-day", TOKEN)
        pcode, pjs = upstox_get("/portfolio/short-term-positions", TOKEN)
        st.session_state["dr_up"] = (code, js, pcode, pjs)
    if "dr_up" not in st.session_state:
        return
    code, js, pcode, pjs = st.session_state["dr_up"]
    if code != 200:
        st.error(f"Trades API error {code}: {str(js)[:200]}")
    else:
        trades = js.get("data") or []
        if not trades:
            st.info("Aaj Upstox account me koi executed trade nahi hai.")
        else:
            rt, left = pair_trades_fifo(trades)
            if not rt.empty:
                rt["Charges (est)"] = (brk + (rt["Entry"] * rt["Qty"]) * cpct / 100.0).round(2)
                rt["Net P&L Rs"] = (rt["Gross P&L Rs"] - rt["Charges (est)"]).round(2)
                w = int((rt["Net P&L Rs"] > 0).sum())
                x = st.columns(4)
                x[0].metric("Real round-trips", len(rt))
                x[1].metric("Profit / Loss", f"{w} / {len(rt) - w}")
                x[2].metric("Real gross P&L", f"₹{rt['Gross P&L Rs'].sum():+,.0f}")
                x[3].metric("Real net (est)", f"₹{rt['Net P&L Rs'].sum():+,.0f}")
                show_df(rt.style.apply(_color_pnl, subset=["Gross P&L Rs", "Net P&L Rs"]))
            if not left.empty:
                st.warning("Abhi bhi open positions (fills adhoore jude hain):")
                show_df(left)
            with st.expander("Raw fills (Upstox)"):
                show_df(pd.DataFrame(trades))
    if pcode == 200 and (pjs.get("data") or []):
        with st.expander("Positions (Upstox) - realised/unrealised P&L"):
            show_df(pd.DataFrame(pjs["data"]))


def render_confirm_report():
    """v7.8: kitne refresh cycle par kitne signal / trade pass ho rahe hain + har cycle bucket ka win % aur P&L."""
    st.divider()
    st.subheader("🔁 Confirm cycles - kitne cycle par kitne signal / trade pass")
    c1, c2 = st.columns(2)
    nd = c1.slider("Pichhle kitne din", 1, 60, 10, key="cr_days")
    md = c2.selectbox("Mode", ["ALL", "LIVE", "DEMO"], index=0, key="cr_mode")
    since = (now_ist().date() - timedelta(days=int(nd))).isoformat()
    try:
        with db() as conn:
            q = "SELECT dt, sym, side, t_first, t_end, cycles, secs, need, outcome, ltp_first, ltp_end, trade_id, note, mode FROM confirm_log WHERE dt >= ?"
            prm = [since]
            if md != "ALL":
                q += " AND mode = ?"
                prm.append(md)
            cl = pd.read_sql_query(q + " ORDER BY id", conn, params=tuple(prm))
            qj = ("SELECT id, dt, symbol, side, entry, pnl_rs, confirm_n, confirm_sec, confirm_ltp0, confirm_set, confirm_route, mode "
                  "FROM trade_journal WHERE status = 'CLOSED' AND instrument_type = 'EQUITY_INTRADAY' AND confirm_n IS NOT NULL AND dt >= ?")
            pj = [since]
            if md != "ALL":
                qj += " AND mode = ?"
                pj.append(md)
            tj = pd.read_sql_query(qj, conn, params=tuple(pj))
    except Exception as e:
        st.warning(f"Confirm data nahi padh paya: {e}")
        return
    if cl.empty and tj.empty:
        st.info("Abhi confirm cycles ka koi record nahi. v7.8 chalne ke baad har stock signal (entry / pullback / toota) yahan aayega.")
        return
    st.caption(f"Abhi setting: {int(stk_confirm_n)} cycle. 'Cycles' = signal lagataar kitne refresh tak bana raha. "
               "Jo signal 1 cycle par toot gaye, wo 1-cycle setting par trade ban jaate - yahi dekh kar setting tay karo.")
    if not cl.empty:
        cl["Cycles"] = cl["cycles"].clip(upper=5).astype(int).astype(str).replace({"5": "5+"})
        def _olab(o):
            o = str(o)
            if o.startswith("BROKEN (confirm hua"):
                return "Toota (confirm ke baad)"
            if o.startswith("BROKEN") or o.startswith("FLIP"):
                return "Toota (confirm se pehle)"
            return o.split("(")[0].strip()
        cl["Outcome"] = cl["outcome"].map(_olab)
        pv = pd.crosstab(cl["Cycles"], cl["Outcome"], margins=True, margins_name="Total")
        st.markdown("**Signals: cycle ke hisaab se kya hua**")
        show_df(pv.reset_index(), hide_index=True)
        sd = np.where(cl["side"].astype(str).str.upper() == "LONG", 1.0, -1.0)
        ok = (cl["ltp_first"] > 0) & (cl["ltp_end"] > 0)
        cl["Move % (side)"] = np.where(ok, (cl["ltp_end"] - cl["ltp_first"]) / cl["ltp_first"].where(ok, 1.0) * 100.0 * sd, np.nan)
        brk = cl[cl["Outcome"] == "Toota (confirm se pehle)"]
        if not brk.empty:
            g = brk.groupby("Cycles").agg(Signals=("sym", "count"), Avg_move=("Move % (side)", "mean"),
                                          Avg_sec=("secs", "mean")).reset_index()
            g["Avg_move"], g["Avg_sec"] = g["Avg_move"].round(3), g["Avg_sec"].round(0)
            st.markdown("**Toote signal: pehli baar dikhne se tootne tak price kis taraf gaya** "
                        "(+ = signal ki disha me; - = ulta, yaani confirm ne bachaya)")
            show_df(g.rename(columns={"Avg_move": "Avg move % (side)", "Avg_sec": "Avg sec"}))
    if not tj.empty:
        sd = np.where(tj["side"].astype(str).str.upper() == "LONG", 1.0, -1.0)
        ok = tj["confirm_ltp0"] > 0
        tj["Late %"] = np.where(ok, (tj["entry"] - tj["confirm_ltp0"]) / tj["confirm_ltp0"].where(ok, 1.0) * 100.0 * sd, np.nan)
        tj["Cycles"] = tj["confirm_n"].clip(upper=5).astype(int).astype(str).replace({"5": "5+"})
        g = tj.groupby(["Cycles", "confirm_route"]).agg(Trades=("id", "count"), Wins=("pnl_rs", lambda x: int((x > 0).sum())),
                                                         Net=("pnl_rs", "sum"), Avg=("pnl_rs", "mean"),
                                                         Late=("Late %", "mean"), Sec=("confirm_sec", "mean")).reset_index()
        g["Win %"] = (g["Wins"] / g["Trades"] * 100).round(1)
        g[["Net", "Avg"]] = g[["Net", "Avg"]].round(0)
        g["Late"], g["Sec"] = g["Late"].round(3), g["Sec"].round(0)
        st.markdown("**Band trades: entry kitne cycle par hui, aur natija**")
        show_df(g.rename(columns={"confirm_route": "Route", "Late": "Entry late % (pehle signal se)", "Sec": "Avg sec"})
                [["Cycles", "Route", "Trades", "Wins", "Win %", "Net", "Avg", "Entry late % (pehle signal se)", "Avg sec"]])
        if len(tj) < 30:
            st.caption(f"Sirf {len(tj)} trades - pattern pakka mat maano, 30+ trades ka intezaar karo.")
    with st.expander("Confirm log (raw)"):
        show_df(cl.tail(300))
        st.download_button("⬇ confirm_log CSV", cl.to_csv(index=False).encode("utf-8"), "confirm_log.csv", "text/csv", key="cr_dl")


def render_filter_analysis():
    render_confirm_report()
    st.divider()
    st.subheader("🔬 Filter analysis - kaun sa bucket jeet/haar de raha hai")
    st.caption("Band hue stock trades ke entry-time features se. Naye v5.6 trades me ADX/VolX/RS/Sector save hote hain; "
               "purane trades me ye 'n/a' dikhenge.")
    fm = st.selectbox("Mode", ["ALL", "LIVE", "DEMO"], index=0, key="fa_mode")
    j = fetch_journal(limit=5000, status_filter="CLOSED", inst_filter="EQUITY_INTRADAY", mode_filter=fm)
    if j.empty or len(j) < 10:
        st.info("Abhi 10 se kam band trades hain - analysis ke liye kam se kam 30-50 trades chahiye.")
        return
    d = j.copy()
    for c in ("P&L Rs", "Bull%/Score", "ADX", "VolX", "RS vs Idx %"):
        d[c] = pd.to_numeric(d[c], errors="coerce")
    if len(d) < 30:
        st.warning(f"Sirf {len(d)} trades - natija pakka mat maano (30+ ho tab hi pattern dekho).")
    sg = np.where(d["Side"].astype(str).str.upper() == "LONG", 1, -1)
    d["Score |abs|"] = d["Bull%/Score"].abs().astype("Int64").astype(str)
    d["Entry hour"] = d["In"].astype(str).str.split(":").str[0].str.zfill(2) + ":00"
    d["Vol spike"] = pd.cut(d["VolX"], [0, 1.2, 1.5, 2.0, 100], labels=["<1.2", "1.2-1.5", "1.5-2", "2+"]).astype(str)
    d["ADX"] = pd.cut(d["ADX"], [0, 20, 25, 35, 200], labels=["<20", "20-25", "25-35", "35+"]).astype(str)
    d["RS (side ke hisaab se)"] = pd.cut(d["RS vs Idx %"] * sg, [-100, 0, 0.5, 1.0, 100],
                                          labels=["<0", "0-0.5", "0.5-1", "1+"]).astype(str)
    d["Exit"] = d["Reason"].astype(str).str.split("(").str[0].str.strip()
    d["Sector"] = d["Sector"].replace("", "n/a").fillna("n/a")
    d = d.replace({"nan": "n/a"})
    cols = ["Side", "Score |abs|", "Entry hour", "Vol spike", "ADX", "RS (side ke hisaab se)", "Sector", "Exit"]
    tabs = st.tabs(cols)
    for tb, col in zip(tabs, cols):
        with tb:
            g = d.groupby(col).agg(Trades=("ID", "count"), Wins=("P&L Rs", lambda x: int((x > 0).sum())),
                                   Net=("P&L Rs", "sum"), Avg=("P&L Rs", "mean")).reset_index()
            g["Win %"] = (g["Wins"] / g["Trades"] * 100).round(1)
            g[["Net", "Avg"]] = g[["Net", "Avg"]].round(0)
            show_df(g[[col, "Trades", "Wins", "Win %", "Net", "Avg"]])

    st.markdown("#### 🤖 ML trade-quality model")
    st.caption("Entry ke features (score, ADX, volume, RS, ATR%, time, VIX) se 'jeetne ki sambhavna'. Time-ordered 70/30 split par test AUC dikhata hai. "
               "AUC 0.5 = andaaza lagana, 0.55+ = kuch signal. Model tabhi trade rokta hai jab sidebar me ML filter > 0 ho, "
               "100+ trades hon aur AUC >= 0.55 ho.")
    if st.button("Model train karo (journal ke band trades se)", key="ml_train_btn"):
        mdl = ml_train(ml_collect_training_data())
        kv_set("ml_model", mdl)
        SNAP["ml_model"] = mdl
    mdl = ml_model_get()
    if not mdl:
        st.info("Abhi koi trained model nahi hai.")
    else:
        mm = st.columns(4)
        mm[0].metric("Trades (train+test)", mdl.get("n", 0))
        mm[1].metric("Test AUC", mdl.get("auc_test", "-"))
        mm[2].metric("Test win% (base)", f"{mdl.get('base_win_test', 0) * 100:.0f}%" if mdl.get("base_win_test") is not None else "-")
        mm[3].metric("Status", "USE HOGA" if mdl.get("valid") else "IGNORE")
        st.caption(f"{mdl.get('reason', '')} | trained {mdl.get('trained_at', '')}")
        if mdl.get("w"):
            coef = pd.DataFrame({"Feature": mdl["feats"], "Weight (+ = jeet ki taraf)": [round(x, 3) for x in mdl["w"]]})
            show_df(coef.sort_values("Weight (+ = jeet ki taraf)", key=lambda z: z.abs(), ascending=False))
    st.markdown("##### 📚 Auto-train history (roz 15:35 ke baad)")
    try:
        with db() as conn:
            hist = conn.execute("SELECT dt, tm, n, auc, acc, base, gap, valid, note FROM ml_history ORDER BY rowid DESC LIMIT 30").fetchall()
        if hist:
            hdf = pd.DataFrame(hist, columns=["Date", "Time", "Trades", "Test AUC", "Acc", "Base win", "Calib gap", "Valid", "Note"])
            hdf["Valid"] = hdf["Valid"].map({1: "✅", 0: "❌"})
            show_df(hdf)
        else:
            st.caption("Abhi auto-train ka koi record nahi (roz 15:35 ke baad, LIVE paper mode me, ML auto-train ON ho tab).")
    except Exception:
        pass
    sug = kv_get("ml_suggestions") or []
    st.markdown("##### 💡 Sudhaar ki salaah (sirf salaah - code apne aap kuch nahi badalta)")
    if sug:
        for line in sug:
            st.write(line)
        st.caption("Ye asli trades ke buckets se aati hain (har bucket me 12+ trades). Chhote sample me ye sanyog bhi ho sakta hai - "
                   "badalne se pehle Backtest tab me check karo.")
    else:
        st.caption("Abhi salaah ke liye 30+ trades aur har bucket me 12+ trades chahiye.")


# ====== SECTION: BACKTEST (candle replay - sidebar ke saare settings ke saath) ======


def bt_hist_1m(ikey: str, d_from: str, d_to: str, with_oi: bool = False) -> pd.DataFrame:
    ck = f"bt1m{'oi' if with_oi else ''}:{ikey}:{d_from}:{d_to}"
    cached = HIST_STORE.get(ck)
    if cached and time.time() - cached[0] < 21600:
        return cached[1]
    code, js = http_json(f"{V2}/historical-candle/{quote(ikey, safe='')}/1minute/{d_to}/{d_from}",
                         auth_headers(TOKEN), timeout=15)
    raw = _candles_from(js, code)
    df = parse_candles(raw)
    if with_oi and raw and not df.empty and all(len(r) >= 7 for r in raw[:3]):
        oi = pd.DataFrame([[r[0], r[6]] for r in raw if len(r) >= 7], columns=["ts", "oi"])
        oi["ts"] = pd.to_datetime(oi["ts"], utc=True).dt.tz_convert(IST)
        oi["oi"] = pd.to_numeric(oi["oi"], errors="coerce")
        df = df.merge(oi.drop_duplicates("ts"), on="ts", how="left")
    if code == 200:
        HIST_STORE[ck] = (time.time(), df)
    return df


def bt_load_pcr(und: str) -> dict:
    """DB me save PCR history -> {date: DataFrame(ts, pcr, pcr_delta)}"""
    out = {}
    try:
        with db() as conn:
            rows = conn.execute("SELECT dt, tm, pcr, pcr_delta FROM pcr_hist WHERE und = ? ORDER BY dt, tm", (und,)).fetchall()
    except Exception:
        return out
    if not rows:
        return out
    d = pd.DataFrame(rows, columns=["dt", "tm", "pcr", "pcr_delta"])
    d["ts"] = pd.to_datetime(d["dt"] + " " + d["tm"]).dt.tz_localize(IST)
    for dt_, g in d.groupby("dt"):
        out[date.fromisoformat(dt_)] = g[["ts", "pcr", "pcr_delta"]].sort_values("ts").reset_index(drop=True)
    return out


def _bt_oi(fdf, t):
    """Futures candles (oi column ke saath) se OI change % aur price change % (oi_window min)."""
    if fdf is None or fdf.empty or "oi" not in fdf.columns:
        return 0.0, 0.0, False
    k = int(fdf["ts"].searchsorted(pd.Timestamp(t)))
    if k <= 0:
        return 0.0, 0.0, False
    cur_oi, cur_px = float(fdf["oi"].iloc[k - 1] or 0.0), float(fdf["c"].iloc[k - 1])
    j = int(fdf["ts"].searchsorted(pd.Timestamp(t - timedelta(minutes=int(oi_window))), side="right")) - 1
    if j < 0 or cur_oi <= 0:
        return 0.0, 0.0, False
    bo, bp = float(fdf["oi"].iloc[j] or 0.0), float(fdf["c"].iloc[j])
    if bo <= 0 or bp <= 0:
        return 0.0, 0.0, False
    return (cur_oi - bo) / bo * 100.0, (cur_px - bp) / bp * 100.0, True


def bt_sim_trade(dd: pd.DataFrame, i0: int, d: int, risk: float, atr: float, qty: int, force_ts=None) -> dict:
    """1-min candles par ek trade ka lifecycle. Ek hi candle me SL aur target dono chhue to SL pehle maana jata hai (conservative)."""
    o_, h_, l_, c_ = dd["o"].values, dd["h"].values, dd["l"].values, dd["c"].values
    ts_ = dd["ts"].tolist()
    entry = float(o_[i0])
    sl = entry - d * risk
    tgt = entry + d * risk * float(rr_mult)
    peak, mfe = entry, 0.0
    qty_rem, part_pnl, part_done = int(qty), 0.0, False
    t0 = ts_[i0]

    def fin(k, px, why):
        pnl = part_pnl + (px - entry) * d * qty_rem
        return {"exit_ts": ts_[k], "exit_px": float(px), "reason": why, "pnl": float(pnl), "entry": entry,
                "qty": int(qty), "mfe": float(mfe), "entry_ts": t0}

    for k in range(i0, len(ts_)):
        ts, o, h, l, c = ts_[k], float(o_[k]), float(h_[k]), float(l_[k]), float(c_[k])
        if force_ts is not None and ts >= force_ts:
            return fin(k, o, "HALT (SL/loss limit)")
        if (d == 1 and l <= sl) or (d == -1 and h >= sl):
            px = o if ((d == 1 and o < sl) or (d == -1 and o > sl)) else sl
            return fin(k, px, "SL HIT" if (px - entry) * d < 0 else "TRAIL SL HIT")
        if partial_on and not part_done:
            lvl = entry + d * float(partial_r) * risk
            if (d == 1 and h >= lvl) or (d == -1 and l <= lvl):
                pq = int(round(qty_rem * float(partial_pct) / 100.0))
                if 1 <= pq < qty_rem:
                    part_pnl += (lvl - entry) * d * pq
                    qty_rem -= pq
                    part_done = True
                    sl = max(sl, entry) if d == 1 else min(sl, entry)
        if (d == 1 and h >= tgt) or (d == -1 and l <= tgt):
            return fin(k, tgt, "TARGET HIT")
        peak = max(peak, h) if d == 1 else min(peak, l)
        mfe = max(mfe, (peak - entry) * d)
        mv = (c - entry) * d
        if use_trail:
            if mv >= float(be_r) * risk:
                sl = max(sl, entry) if d == 1 else min(sl, entry)
            if mv >= max(1.5, float(be_r) + 0.3) * risk and atr > 0:
                tr = peak - d * atr
                sl = max(sl, tr) if d == 1 else min(sl, tr)
        if int(time_stop_min) > 0 and (ts - t0).total_seconds() / 60.0 >= int(time_stop_min) and mv < 0.3 * risk:
            return fin(k, c, "TIME STOP")
        if ts.time() >= eod_exit:
            return fin(k, c, "EOD SQUARE-OFF")
    return fin(len(ts_) - 1, float(c_[-1]), "EOD SQUARE-OFF")


def _bt_day(day, idx_df, data, fdata, lot_of, pcr_day, step_min, orig_pcr_on, meta, spcr_day=None, spcr_base=None) -> list:
    g = globals()
    all_days = sorted({x for x in idx_df["ts"].dt.date.unique() if x < day})
    pday = all_days[-1] if all_days else None

    def two_day(df):
        m = df["ts"].dt.date == day
        if pday is not None:
            m |= df["ts"].dt.date == pday
        return df[m].reset_index(drop=True)

    def prev_close(df):
        p = df[df["ts"].dt.date == pday] if pday is not None else df.iloc[0:0]
        return float(p["c"].iloc[-1]) if not p.empty else 0.0

    two = {s_: two_day(df) for s_, df in data.items()}
    two = {s_: v for s_, v in two.items() if (v["ts"].dt.date == day).sum() > 30}
    dayd = {s_: v[v["ts"].dt.date == day].reset_index(drop=True) for s_, v in two.items()}
    pcl = {s_: prev_close(data[s_]) for s_ in two}
    ftwo = {s_: (two_day(fdata[s_]) if s_ in fdata and not fdata[s_].empty else None) for s_ in two}
    idx2 = two_day(idx_df)
    ipc = prev_close(idx_df)
    if not two or idx2.empty:
        return []
    lock_map = {}
    for s_ in two:
        try:
            lock_map[s_] = bool(resolve_earnings_status(s_, custom_earnings_map, day, lock_mode, int(pre_days),
                                                         int(post_days), lock_pattern)["is_result_week"])
        except Exception:
            lock_map[s_] = False
    spcr_day = spcr_day or {}
    have_pcr = bool(spcr_day) if use_stock_pcr else (pcr_day is not None and not pcr_day.empty)
    g["pcr_filter_on"] = bool(orig_pcr_on and have_pcr)
    stock_pcr_active = bool(orig_pcr_on and use_stock_pcr and have_pcr)
    if orig_pcr_on:
        (meta["pcr_days_used"] if have_pcr else meta["pcr_days_off"]).append(day.isoformat())
    n_prev = 0
    if step_min <= 1 and int(stk_confirm_n) > 1:
        n_prev = int(math.ceil((int(stk_confirm_n) - 1) * max(10.0, 0.7 * float(refresh_sec)) / 60.0))
    sig_hist = deque(maxlen=max(1, n_prev))
    per_step_cap = int(max_new_per_min) * (1 if step_min <= 1 else 3)

    open_, closed = [], []
    st_ = {"halted": False, "peak": 0.0}

    def day_stats():
        cl = sorted(closed, key=lambda z: z["res"]["exit_ts"])
        pnl = sum(x["res"]["pnl"] for x in cl)
        slh = sum(1 for x in cl if "SL HIT" in x["res"]["reason"] and x["res"]["pnl"] < 0)
        cons = 0
        for x in reversed(cl):
            if x["res"]["pnl"] < 0:
                cons += 1
            else:
                break
        return pnl, slh, cons

    def halt_now(h):
        st_["halted"] = True
        for tr in list(open_):
            if tr["res"]["exit_ts"] > h:
                tr["res"] = bt_sim_trade(dayd[tr["sym"]], tr["i0"], tr["d"], tr["risk"], tr["atr"], tr["qty"], force_ts=h)
            open_.remove(tr)
            closed.append(tr)

    def settle(upto):
        for tr in sorted([x for x in open_ if x["res"]["exit_ts"] <= upto], key=lambda z: z["res"]["exit_ts"]):
            if tr not in open_:
                continue
            open_.remove(tr)
            closed.append(tr)
            if not st_["halted"]:
                pnl, slh, _c = day_stats()
                if slh >= int(stk_max_sl_day) or pnl <= -abs(float(stk_loss_limit)):
                    halt_now(tr["res"]["exit_ts"])

    t = datetime.combine(day, entry_start, tzinfo=IST)
    if step_min > 1:
        t = t.replace(minute=(t.minute // step_min) * step_min, second=0)
    t_end = datetime.combine(day, entry_end, tzinfo=IST)
    ml_mdl = ml_model_get() if float(ml_min_prob) > 0 else None
    while t <= t_end and not st_["halted"]:
        settle(t)
        if st_["halted"]:
            break
        tk = pd.Timestamp(t)
        k_i = int(idx2["ts"].searchsorted(tk))
        iup = idx2.iloc[:k_i]
        if len(iup) < 40:
            t += timedelta(minutes=step_min)
            continue
        im = analyze_candles(iup, 0.0, live=False)
        ipx = float(iup["c"].iloc[-1])
        ic = {"ok": bool(im["ok"]), "spot": ipx, "chg_pct": round((ipx - ipc) / ipc * 100.0, 2) if ipc > 0 else 0.0,
              "adx": im["adx"], "atr": im["atr"], "m": im, "pcr": None, "pcr_delta": None, "vix": 0.0,
              "trend_dir": trend_dir(ipx, im),
              "mtf_dir": (1 if im["ema9_15m"] > im["ema21_15m"] else -1 if im["ema9_15m"] < im["ema21_15m"] else 0)
              if im["ok"] and im["ema9_15m"] > 0 else 0}
        if have_pcr and pcr_day is not None and not pcr_day.empty:
            kp = int(pcr_day["ts"].searchsorted(tk)) - 1
            if kp >= 0:
                ic["pcr"] = float(pcr_day["pcr"].iloc[kp])
                dv = pcr_day["pcr_delta"].iloc[kp]
                ic["pcr_delta"] = None if pd.isna(dv) else float(dv)
        ic["zone_txt"], ic["zone"] = zone_state(ipx, im)
        ic["z_hi"], ic["z_lo"] = im["z15_hi"], im["z15_lo"]
        g["MKT_CHOP"], g["MKT_CHOP_WHY"] = market_chop_state(ic)
        rows, ltp_map, ret_store = [], {}, {}
        for s_, tw in two.items():
            up = tw.iloc[:int(tw["ts"].searchsorted(tk))]
            if len(up) < 40:
                continue
            ltp = float(up["c"].iloc[-1])
            ltp_map[s_] = ltp
            _c1 = up[["ts", "c"]].tail(int(corr_window) + 1)
            ret_store[s_] = (_c1["ts"].iloc[1:].values, np.log(_c1["c"].astype(float)).diff().dropna().values)
            m = analyze_candles(up, 0.0, live=False)
            if not m["ok"] or ltp <= 0:
                continue
            oi_chg, px_chg, oi_ready = _bt_oi(ftwo.get(s_), t)
            sc = score_stock_filters(ltp, pcl.get(s_, 0.0), m, oi_chg, px_chg, oi_ready, float(adx_min))
            rows.append({"Symbol": s_, "LTP": ltp, "Day %": sc["chg_pct"], "ATR (5m)": m["atr"], "ADX (14)": m["adx"],
                         "Vol Spike x": m["vol_spike"], "_score": sc["net_score"], "_mtf": sc["mtf_d"], "_orb": sc["orb_d"],
                         "_fut": sc["fut_d"], "_extL": sc["ext_long"], "_extS": sc["ext_short"], "_whyL": sc["why_long"],
                         "_whyS": sc["why_short"], "_lock": lock_map.get(s_, False), "_ok": True, "_zone": sc["in_zone"],
                         "_lot": lot_of(s_), "_tdir": trend_dir(ltp, m), "_vwx": int(m.get("vwap_cross", 0) or 0)})
        if rows:
            fdf = finalize_actions(pd.DataFrame(rows), ic)
            cand = fdf[fdf["Final Action"].astype(str).str.startswith(("🟢 STRONG", "🔻 STRONG"))]
            cand = cand.sort_values("Rank", ascending=False, na_position="last").to_dict("records")
        else:
            cand = []
        cur_sig = {(r_["Symbol"], "LONG" if str(r_["Final Action"]).startswith("🟢") else "SHORT") for r_ in cand}
        confirmed = (lambda s_, w_: all((s_, w_) in h_ for h_ in sig_hist)) if (n_prev and len(sig_hist) >= n_prev) \
            else (lambda s_, w_: n_prev == 0)
        run = sum((ltp_map.get(x["sym"], x["res"]["entry"]) - x["res"]["entry"]) * x["d"] * x["qty"] for x in open_)
        cl_pnl, slh, cons = day_stats()
        tot = cl_pnl + run
        st_["peak"] = max(st_["peak"], tot)
        if tot <= -abs(float(stk_loss_limit)):
            halt_now(t)
            break
        lock = (float(stk_profit_lock) > 0 and tot >= float(stk_profit_lock)) or \
               (st_["peak"] >= float(giveback_min_peak) and tot <= st_["peak"] * (1 - float(giveback_pct) / 100.0))
        n_total = len(open_) + len(closed)
        new_n = 0
        for r in cand:
            s_ = r["Symbol"]
            if lock or slh >= int(stk_max_sl_day) or cons >= int(max_consec_losses) or n_total >= int(max_stk_trades_day):
                break
            if new_n >= per_step_cap or len(open_) >= int(max_open_pos):
                break
            want = "LONG" if str(r["Final Action"]).startswith("🟢") else "SHORT"
            d = 1 if want == "LONG" else -1
            if not confirmed(s_, want):
                continue
            if stock_pcr_active:
                dfp, pv, pd_ = spcr_day.get(s_), None, None
                if dfp is not None and len(dfp):
                    kp_ = int(dfp["ts"].searchsorted(tk)) - 1
                    if kp_ >= 0:
                        pv = float(dfp["pcr"].iloc[kp_])
                        dv_ = dfp["pcr_delta"].iloc[kp_]
                        pd_ = None if pd.isna(dv_) else float(dv_)
                if not stock_pcr_decision(1 if want == "LONG" else -1, pv, pd_, (spcr_base or {}).get(s_), None, None, "", False)[0]:
                    continue
            lull = bool(f_mid and dtime(12, 0) <= t.time() <= dtime(13, 15))
            if abs(r["_score"]) < int(stk_min_score) + (1 if lull else 0) or (lull and r["Vol Spike x"] < float(f_mid_vol)):
                continue
            same = [x for x in open_ + closed if x["sym"] == s_]
            if any(x in open_ for x in same) or len(same) >= STK_MAX_PER_SYM:
                continue
            blocked = False
            for x in same:
                if "SL HIT" in x["res"]["reason"] and x["res"]["pnl"] < 0:
                    blocked = True
                cd = 60 if x["res"]["pnl"] < 0 else STK_COOLDOWN_MIN
                if (t - x["res"]["exit_ts"]).total_seconds() < cd * 60:
                    blocked = True
            if blocked:
                continue
            atr = float(r["ATR (5m)"])
            lot = int(r["_lot"] or 0)
            if atr <= 0 or lot <= 0 or s_ not in dayd:
                continue
            risk = atr * float(sl_atr_mult)
            lots = 1
            if risk_sizing:
                lots = int(max(1, min(int(max_lots_stk), float(risk_per_trade) // (risk * lot))))
            qty = lot * lots
            if use_cap_qty:
                cq = cap_qty(float(r["LTP"]))
                if cq < 1:
                    continue
                qty = cq
            ml_p = 0.0
            if ml_mdl and ml_mdl.get("valid"):
                ml_p = ml_predict(ml_mdl, ml_feats(r, want, float(r["LTP"]), t, 0.0))
                if ml_p < float(ml_min_prob):
                    continue
            pos_map = {x["sym"]: {"side": x["side"], "sector": sector_of(x["sym"]), "entry": x["res"]["entry"],
                                  "sl": 0, "sl0": x["res"]["entry"] - x["d"] * x["risk"], "qty": x["qty"]} for x in open_}
            ok_r, _why = _stk_risk_ok(pos_map, s_, want, risk * qty, float(r["LTP"]) * qty, ret_store)
            if not ok_r:
                continue
            i0 = int(dayd[s_]["ts"].searchsorted(tk))
            if i0 >= len(dayd[s_]) - 1:
                continue
            res = bt_sim_trade(dayd[s_], i0, d, risk, atr, qty)
            open_.append({"sym": s_, "side": want, "d": d, "i0": i0, "risk": risk, "atr": atr, "qty": qty, "res": res,
                          "score": r["_score"], "volx": r["Vol Spike x"], "adx": r["ADX (14)"], "rank": r["Rank"],
                          "route": str(r.get("Entry Route", "-")), "oi": r["_fut"], "ml": ml_p,
                          "rs": safe_float(r.get("RS vs Index %"))})
            new_n += 1
            n_total += 1
        if n_prev:
            sig_hist.append(cur_sig)
        t += timedelta(minutes=step_min)
    settle(datetime.combine(day, dtime(23, 59), tzinfo=IST))
    out = []
    for x in closed + open_:
        r_ = x["res"]
        out.append({"Date": day.isoformat(), "Symbol": x["sym"], "Sector": sector_of(x["sym"]), "Side": x["side"],
                    "In": r_["entry_ts"].strftime("%H:%M"), "Out": r_["exit_ts"].strftime("%H:%M"), "Qty": x["qty"],
                    "Entry": round(r_["entry"], 2), "Exit": round(r_["exit_px"], 2), "P&L Rs": round(r_["pnl"], 2),
                    "Reason": r_["reason"], "Score": x["score"], "VolX": round(x["volx"], 2), "ADX": round(x["adx"], 1),
                    "OI dir": x["oi"], "Route": x["route"], "ML Prob": round(x["ml"], 2), "MFE": round(r_["mfe"], 2),
                    "RS vs Idx %": round(x.get("rs", 0.0), 2), "Rank": round(safe_float(x["rank"]), 2), "ATR": round(x["atr"], 2)})
    return out


_BT_APPLIED = [
    ("Stock ENTRY min score", "stk_min_score"), ("Bias strength (min net score)", "min_net"), ("Min ADX(5m)", "adx_min"),
    ("Index 5m trend confirm", "require_idx"), ("15m MTF confirm", "require_mtf"), ("ORB confirm", "require_orb"),
    ("Futures OI buildup confirm", "require_fut"), ("Result-week lock", "exclude_result_wk"),
    ("SL = ATR x", "sl_atr_mult"), ("Target R:R", "rr_mult"), ("Breakeven + ATR trail", "use_trail"), ("Breakeven R", "be_r"),
    ("Chase filter LONG (VWAP se ATR x)", "ext_atr"), ("Chase filter SHORT (VWAP se ATR x)", "ext_atr_s"), ("F1 Day/Prev High-Low wall", "f_wall"), ("F2 Wick rejection", "f_wick"),
    ("F3 RS vs Index", "f_rs"), ("F4 Volume spike", "f_vol"), ("F5 Min ATR %", "f_minatr"), ("F6 Mid-day lull", "f_mid"),
    ("15m consolidation zone", "zone_filter"), ("Market choppy filter", "chop_filter"), ("Solo override", "solo_on"),
    ("OI window (min)", "oi_window"), ("OI threshold %", "oi_th"), ("Price threshold %", "px_th"),
    ("Entry window start", "entry_start"), ("Entry window end", "entry_end"), ("EOD square-off", "eod_exit"),
    ("Max khule positions", "max_open_pos"), ("Max naye entry / min", "max_new_per_min"), ("Direction limit", "max_same_dir"),
    ("Sector limit", "max_per_sector"), ("Total open risk Rs", "max_open_risk"), ("ATR risk sizing", "risk_sizing"),
    ("Time-stop (min)", "time_stop_min"), ("Partial profit", "partial_on"), ("ML min probability", "ml_min_prob"),
    ("Stock daily loss limit", "stk_loss_limit"), ("Max SL hits / din (stock)", "stk_max_sl_day"), ("Max trades / din", "max_stk_trades_day"),
    ("Lagataar loss limit", "max_consec_losses"), ("Din ka profit lock", "stk_profit_lock"), ("Giveback %", "giveback_pct"),
]
_BT_NA = [("Index engine: entry power / confirm / lots / loss limit / VIX / OI wall", "enter_th"),
          ("Live trading / Telegram / Google Sheet / refresh / scan-tier / watchlist", "refresh_sec")]


def bt_settings_report(step_min: int, mode: str) -> pd.DataFrame:
    g = globals()
    rows = []
    for lab, var in _BT_APPLIED:
        val = g.get(var)
        rows.append({"Setting": lab, "Value": str(val), "Backtest me": "✅ lagu"})
    rows.append({"Setting": "PCR source / limits", "Value": f"{g.get('pcr_source')} | {g.get('spcr_mode')} | fixed LONG > {g.get('spcr_long')} / SHORT < {g.get('spcr_short')}",
                 "Backtest me": "✅ jis din PCR history DB me ho, warna us din PCR skip"})
    rows.append({"Setting": "PCR filter", "Value": str(g.get("pcr_filter_on")),
                 "Backtest me": "✅ jis din PCR history DB me ho, warna us din skip (neeche dekho)"})
    rows.append({"Setting": "Stock confirm cycles", "Value": str(g.get("stk_confirm_n")),
                 "Backtest me": "✅ lagu (1-min step)" if step_min <= 1 else "⚠ 5-min step me skip - 1-min step chuno"})
    rows.append({"Setting": "Mode", "Value": "Sidebar jaisa", "Backtest me": "-"})
    for lab, var in _BT_NA:
        rows.append({"Setting": lab, "Value": "-", "Backtest me": "— sirf live / index engine ke liye"})
    return pd.DataFrame(rows)


def bt_load_pcr_stocks(syms: list) -> dict:
    """Stock-wise PCR history: {sym: {date: DataFrame(ts, pcr, pcr_delta)}}"""
    out = {}
    if not syms:
        return out
    try:
        q = ",".join("?" * len(syms))
        with db() as conn:
            rows = conn.execute(f"SELECT und, dt, tm, pcr, pcr_delta FROM pcr_hist WHERE und IN ({q}) ORDER BY dt, tm", tuple(syms)).fetchall()
    except Exception:
        return out
    if not rows:
        return out
    d = pd.DataFrame(rows, columns=["und", "dt", "tm", "pcr", "pcr_delta"])
    d["ts"] = pd.to_datetime(d["dt"] + " " + d["tm"]).dt.tz_localize(IST)
    for (u, dt_), g in d.groupby(["und", "dt"]):
        out.setdefault(u, {})[date.fromisoformat(dt_)] = g[["ts", "pcr", "pcr_delta"]].sort_values("ts").reset_index(drop=True)
    return out


def bt_load_pcr_daily(syms: list) -> dict:
    """Daily PCR snapshots: {sym: [(date, pcr), ...]} (puraane se naya)"""
    out = {}
    if not syms:
        return out
    try:
        q = ",".join("?" * len(syms))
        with db() as conn:
            rows = conn.execute(f"SELECT sym, dt, pcr FROM pcr_daily WHERE sym IN ({q}) ORDER BY dt", tuple(syms)).fetchall()
    except Exception:
        return out
    for sy, dt_, p in rows:
        out.setdefault(sy, []).append((date.fromisoformat(dt_), float(p)))
    return out


def run_backtest(syms: list, n_days: int, loader, fut_loader, idx_df: pd.DataFrame, lot_of, mode: str = "sidebar",
                 step_min: int = 5, pcr_days: dict = None, prog=None):
    meta = {"pcr_days_used": [], "pcr_days_off": [], "settings": None, "oi_syms": 0}
    if idx_df is None or idx_df.empty:
        return pd.DataFrame(), meta
    days_all = sorted({x for x in idx_df["ts"].dt.date.unique()})
    today = now_ist().date()
    days = [x for x in days_all if x < today or (x == today and not market_open())][-int(n_days):]
    data, fdata = {}, {}
    for s_ in syms:
        df = loader(s_)
        if df is not None and not df.empty:
            data[s_] = df.sort_values("ts").reset_index(drop=True)
            if fut_loader is not None:
                fd = fut_loader(s_)
                if fd is not None and not fd.empty and "oi" in fd.columns and fd["oi"].notna().any():
                    fdata[s_] = fd.sort_values("ts").reset_index(drop=True)
    meta["oi_syms"] = len(fdata)
    g = globals()
    saved = {}

    def setg(k, v):
        saved.setdefault(k, g.get(k))
        g[k] = v

    for k in ("pcr_filter_on", "MKT_CHOP", "MKT_CHOP_WHY"):
        saved[k] = g.get(k)
    orig_pcr = bool(g.get("pcr_filter_on"))
    trades = []
    try:
        g["pcr_filter_on"] = orig_pcr
        meta["settings"] = bt_settings_report(int(step_min), mode)
        spcr_all = bt_load_pcr_stocks(list(data)) if g.get("use_stock_pcr") else {}
        spcr_daily = bt_load_pcr_daily(list(data)) if g.get("use_stock_pcr") and g.get("spcr_adaptive") else {}
        for i, day in enumerate(days):
            sp_day = {s_: v[day] for s_, v in spcr_all.items() if day in v}
            sp_base = {s_: _spcr_base_stats([p for d_, p in v if d_ < day][-int(g["spcr_days"]):]) for s_, v in spcr_daily.items()}
            trades += _bt_day(day, idx_df, data, fdata, lot_of, (pcr_days or {}).get(day), int(step_min), orig_pcr, meta, sp_day, sp_base)
            if prog is not None:
                prog.progress((i + 1) / max(1, len(days)))
    finally:
        for k, v in saved.items():
            g[k] = v
    return pd.DataFrame(trades), meta


def bt_summary(t: pd.DataFrame) -> dict:
    if t.empty:
        return {}
    t = t.sort_values(["Date", "Out"]).copy()
    turn = t["Entry"] * t["Qty"]
    t["Charges"] = GS_BRK + turn * GS_CHG_PCT / 100.0
    t["Net"] = t["P&L Rs"] - t["Charges"]
    n, w = len(t), int((t["P&L Rs"] > 0).sum())
    gp, gl = float(t.loc[t["P&L Rs"] > 0, "P&L Rs"].sum()), abs(float(t.loc[t["P&L Rs"] < 0, "P&L Rs"].sum()))
    cum = t["Net"].cumsum()
    return {"n": n, "wins": w, "win": w / n * 100.0, "gross": float(t["P&L Rs"].sum()), "net": float(t["Net"].sum()),
            "pf": (gp / gl) if gl > 0 else (99.9 if gp > 0 else 0.0), "dd": float((cum - cum.cummax()).min()),
            "days": t["Date"].nunique(), "t": t}


def render_backtest():
    st.subheader("🧪 Backtest - purane din ke 1-min candles par replay")
    st.caption("Sidebar ke SAARE stock settings lagu hote hain (score, F1-F6 filters, zone, choppy, SL/target/trail, partial, time-stop, "
               "risk limits, din ke halts, ML, earnings lock, futures OI buildup). PCR filter tab lagta hai jab us din ka PCR history DB me ho "
               "(v5.8 live chalne par har minute save hota hai). Fill agli 1-min candle ke open par; SL/target same candle me dono chhuein to SL pehle. "
               "Ye sahi disha deta hai, exact live result nahi.")
    if not demo_mode and not TOKEN:
        st.info("Backtest ke liye Upstox token chahiye (ya sidebar me Demo mode).")
        return
    c1, c2 = st.columns(2)
    n_days = c1.slider("Kitne pichhle trading din", 1, 15, 5, key="bt_days")
    top = sorted(SYMBOLS, key=lambda z: -W.get(z, 0.0))[:15]
    bsyms = c2.multiselect("Stocks (zyada = zyada API calls / der)", SYMBOLS, default=top, key="bt_syms")
    c3, c4 = st.columns(2)
    c3.caption("Filters: sidebar jaisa (jo abhi set hai). v7.8: Strict mode hata diya.")
    step_lab = c4.radio("Replay step", ["5 min (tez)", "1 min (confirm cycles bhi lagu, dheema)"], index=0, key="bt_step")
    mode = "sidebar"
    step_min = 1 if step_lab.startswith("1") else 5
    pcr_all = bt_load_pcr(IDX_UND)
    st.caption(f"PCR history DB me: {len(pcr_all)} din ({', '.join(sorted(d_.isoformat() for d_ in pcr_all)[-5:]) or 'abhi koi nahi'}). "
               "Jis din ka PCR nahi, us din PCR filter skip hoga.")
    if st.button("▶ Backtest chalao", key="bt_run"):
        if not bsyms:
            st.warning("Kam se kam 1 stock chuno.")
        else:
            prog = st.progress(0.0)
            with st.spinner("Candles fetch + replay ho raha hai..."):
                if demo_mode:
                    loader = lambda s_: demo_stock_inputs(s_)["df1m"]
                    fut_loader = None
                    idxd = synth_candles(zlib.crc32(IDX_UND.encode()), DEMO_BASE.get(IDX_UND, 20000.0),
                                         drift=demo_mkt_drift(), vol_scale=0.6)
                else:
                    today_ = now_ist().date()
                    d_to = today_.isoformat()
                    d_from = (today_ - timedelta(days=min(29, int(n_days * 1.6) + 6))).isoformat()
                    loader = lambda s_: bt_candles(s_, bundle["eq"][s_], d_from, d_to, n_days) if s_ in bundle["eq"] else pd.DataFrame()
                    fut_loader = lambda s_: (bt_hist_1m(bundle["fut"][s_], d_from, d_to, with_oi=True)
                                             if bundle["fut"].get(s_) else pd.DataFrame())
                    _ifk = (bundle["idx"].get(IDX_UND) or (None, 0))[0]
                    idxd = bt_candles(f"INDEX:{IDX_UND}", _ifk or PRIMARY_INDEX_KEY, d_from, d_to, n_days)
                lot_of = lambda s_: int(bundle["lot_map"].get(s_, 0))
                res = run_backtest(bsyms, n_days, loader, fut_loader, idxd, lot_of, mode, step_min, pcr_all, prog)
            st.session_state["bt_res"] = res
            bt_save_trades(res[0])
    res = st.session_state.get("bt_res")
    if res is None:
        return
    df_res, meta = res
    if meta.get("settings") is not None:
        with st.expander("⚙ Is backtest me lagu hue settings", expanded=False):
            show_df(meta["settings"])
    st.caption(f"Futures OI data: {meta.get('oi_syms', 0)} stocks | PCR filter lagu din: {len(meta.get('pcr_days_used', []))} | "
               f"PCR history na hone se skip: {len(meta.get('pcr_days_off', []))}")
    sm = bt_summary(df_res)
    if not sm:
        st.warning("Is setting par koi trade nahi bana (ya data nahi aaya).")
        return
    a = st.columns(6)
    a[0].metric("Trades", sm["n"], delta=f"{sm['days']} din")
    a[1].metric("Win rate", f"{sm['win']:.1f}%", delta=f"{sm['wins']}W / {sm['n'] - sm['wins']}L")
    a[2].metric("Gross P&L", f"₹{sm['gross']:+,.0f}")
    a[3].metric("Net (costs ke baad)", f"₹{sm['net']:+,.0f}")
    a[4].metric("Profit factor", f"{sm['pf']:.2f}")
    a[5].metric("Max drawdown", f"₹{sm['dd']:,.0f}")
    if sm["n"] < 30:
        st.warning(f"Sirf {sm['n']} trades - natija pakka mat maano. Zyada din / stocks chuno.")
    t = sm["t"]
    g1, g2 = st.columns(2)
    with g1:
        st.markdown("**Din ke hisaab se**")
        show_df(t.groupby("Date").agg(Trades=("Symbol", "count"), Wins=("P&L Rs", lambda x: int((x > 0).sum())),
                                      Net=("Net", "sum")).round(0).reset_index())
    with g2:
        st.markdown("**Exit reason ke hisaab se**")
        show_df(t.groupby("Reason").agg(Trades=("Symbol", "count"), Wins=("P&L Rs", lambda x: int((x > 0).sum())),
                                        Net=("Net", "sum")).round(0).reset_index().sort_values("Net"))
    st.markdown("**Sab trades**")
    show_df(t.drop(columns=["Charges"], errors="ignore"))
    st.download_button("⬇ Backtest trades CSV", t.to_csv(index=False).encode("utf-8"),
                       file_name=f"backtest_{now_ist():%Y%m%d_%H%M}.csv", mime="text/csv")


# ====== SECTION: RISK DESK (institutional risk analytics) ======
def risk_metrics(j: pd.DataFrame, capital: float = 0.0) -> dict:
    """Band hue trades se institutional risk/performance metrics. (Kam trades = kam bharosa.)"""
    if j is None or j.empty:
        return {}
    d = j.copy()
    for c in ("P&L Rs", "Entry", "Lots", "LotSize", "MFE", "MAE"):
        d[c] = pd.to_numeric(d[c], errors="coerce").fillna(0.0)
    d = d.sort_values(["Date", "Out"]).reset_index(drop=True)
    qty = (d["Lots"] * d["LotSize"]).clip(lower=1)
    d["Charges"] = GS_BRK + d["Entry"] * qty * GS_CHG_PCT / 100.0
    d["Net"] = d["P&L Rs"] - d["Charges"]
    pnl, net = d["P&L Rs"].values, d["Net"].values
    n = len(d)
    wins, losses = pnl[pnl > 0], pnl[pnl < 0]
    aw = float(wins.mean()) if len(wins) else 0.0
    al = float(losses.mean()) if len(losses) else 0.0
    gp, gl = float(wins.sum()), abs(float(losses.sum()))
    win = len(wins) / n
    payoff = (aw / abs(al)) if al < 0 else 0.0
    cum = np.cumsum(net)
    peak = np.maximum.accumulate(np.concatenate([[0.0], cum]))[1:]
    mdd = float((cum - peak).min()) if n else 0.0
    day = d.groupby("Date")["Net"].sum()
    nd = len(day)
    sharpe = sortino = calmar = None
    if nd >= 5 and day.std(ddof=1) > 0:
        sharpe = float(day.mean() / day.std(ddof=1) * math.sqrt(252))
        dn = day[day < 0]
        dstd = float(np.sqrt((dn ** 2).sum() / nd)) if len(dn) else 0.0
        sortino = float(day.mean() / dstd * math.sqrt(252)) if dstd > 0 else None
        if mdd < 0:
            calmar = float(day.mean() * 252 / abs(mdd))
    p5 = float(np.percentile(pnl, 5)) if n >= 20 else None
    p1 = float(np.percentile(pnl, 1)) if n >= 100 else None
    var95 = -p5 if p5 is not None else None
    cvar95 = -float(pnl[pnl <= p5].mean()) if p5 is not None and (pnl <= p5).any() else None
    var99 = -p1 if p1 is not None else None
    kelly = (win - (1 - win) / payoff) if payoff > 0 else None
    mf = d[d["MFE"] > 0]
    cap_eff = float(np.median(mf["P&L Rs"] / (mf["MFE"] * qty.loc[mf.index]))) if len(mf) else None
    streak = best = 0
    for v in pnl:
        streak = streak + 1 if v < 0 else 0
        best = max(best, streak)
    return {"n": n, "days": nd, "win": win * 100.0, "avg_win": aw, "avg_loss": al, "payoff": payoff,
            "pf": (gp / gl) if gl > 0 else (99.9 if gp > 0 else 0.0), "expectancy": float(pnl.mean()),
            "gross": float(pnl.sum()), "charges": float(d["Charges"].sum()), "net": float(net.sum()),
            "cost_drag": (float(d["Charges"].sum()) / gp * 100.0) if gp > 0 else None, "mdd": mdd,
            "mdd_pct": (mdd / capital * 100.0) if capital > 0 else None, "sharpe": sharpe, "sortino": sortino,
            "calmar": calmar, "var95": var95, "cvar95": cvar95, "var99": var99, "kelly": kelly,
            "capture": cap_eff, "max_loss_streak": best, "best": float(pnl.max()), "worst": float(pnl.min()), "d": d}


def mc_bootstrap(pnls: np.ndarray, n_trades: int = 100, sims: int = 5000, dd_limit: float = 50000.0, seed: int = 7) -> dict:
    """Trade P&L ko random resample karke agle n_trades ka sambhavit daayra (i.i.d. maan kar)."""
    pnls = np.asarray(pnls, dtype=float)
    if len(pnls) < 10:
        return {}
    rng = np.random.default_rng(seed)
    paths = np.cumsum(rng.choice(pnls, size=(sims, int(n_trades)), replace=True), axis=1)
    peak = np.maximum.accumulate(np.concatenate([np.zeros((sims, 1)), paths], axis=1), axis=1)[:, 1:]
    dd = (paths - peak).min(axis=1)
    fin = paths[:, -1]
    return {"p5": float(np.percentile(fin, 5)), "p25": float(np.percentile(fin, 25)), "p50": float(np.percentile(fin, 50)),
            "p75": float(np.percentile(fin, 75)), "p95": float(np.percentile(fin, 95)),
            "p_loss": float((fin < 0).mean() * 100.0), "p_dd": float((dd <= -abs(dd_limit)).mean() * 100.0),
            "dd_p50": float(np.percentile(dd, 50)), "dd_p5": float(np.percentile(dd, 5))}


def stress_open_positions(pos_rows: list) -> pd.DataFrame:
    """Khule positions par scenario P&L. Index shock = beta 1 maan kar. SL-capped = SL lagne par loss risk tak hi."""
    risk = sum(p["risk"] for p in pos_rows)
    out = [{"Scenario": "Sab positions ka SL hit", "P&L Rs": -risk, "SL ke saath P&L Rs (gap nahi)": -risk},
           {"Scenario": "Gap: SL ke 1.5x par band (slippage)", "P&L Rs": -1.5 * risk, "SL ke saath P&L Rs (gap nahi)": -1.5 * risk}]
    for sh in (-3, -2, -1, 1, 2, 3):
        un = sum(p["side_n"] * p["notional"] * sh / 100.0 for p in pos_rows)
        cp = sum(max(p["side_n"] * p["notional"] * sh / 100.0, -p["risk"]) for p in pos_rows)
        out.append({"Scenario": f"Index {sh:+d}% (beta 1)", "P&L Rs": un, "SL ke saath P&L Rs (gap nahi)": cp})
    return pd.DataFrame(out).round(0)


def _open_pos_rows() -> list:
    day = now_ist().strftime("%Y-%m-%d")
    mp = SNAP.get(f"stk_paper:{day}", {}) or {}
    ltps = {}
    try:
        ltps = dict(zip(df_all["Symbol"], df_all["LTP"]))
    except Exception:
        pass
    rows = []
    for sym, p in mp.items():
        ltp = float(ltps.get(sym) or p["entry"])
        d_ = 1 if p["side"] == "LONG" else -1
        rows.append({"sym": sym, "side": p["side"], "side_n": d_, "sector": p.get("sector") or sector_of(sym), "qty": p["qty"],
                     "entry": p["entry"], "ltp": ltp, "notional": ltp * p["qty"],
                     "risk": abs(p["entry"] - p.get("sl0", p["sl"])) * p["qty"],
                     "pnl": (ltp - p["entry"]) * d_ * p["qty"] + p.get("part_pnl", 0.0)})
    return rows


def render_risk_desk():
    st.subheader("🏛 Risk Desk - institutional risk view")
    st.caption("Exposure, limits, stress test aur trade-level risk statistics. Ye risk dikhane ke tools hain - profit ki guarantee nahi. "
               "Kam trades par statistics pakka nahi hote (neeche chetavani dikhegi).")
    c1, c2 = st.columns(2)
    capital = float(c1.number_input("Capital Rs (% metrics ke liye)", value=int(capital_rs) if int(capital_rs) > 0 else 500000,
                                    min_value=10000, step=50000, key="rd_cap"))
    fm = c2.selectbox("Mode", ["LIVE", "DEMO", "ALL"], index=0 if not demo_mode else 1, key="rd_mode")

    # ---- 1. Limits utilisation
    st.markdown("#### 1) Limits utilisation (aaj)")
    day = now_ist().strftime("%Y-%m-%d")
    rows = _open_pos_rows()
    dp, cons, ntr, slh = stk_day_stats(day, "DEMO" if fm == "DEMO" else "LIVE")
    n_long = sum(1 for r in rows if r["side"] == "LONG")
    n_short = len(rows) - n_long
    open_risk = sum(r["risk"] for r in rows)
    gross = sum(r["notional"] for r in rows)
    lim = [("Din ka P&L vs loss limit", max(0.0, -dp), float(stk_loss_limit), f"Rs {dp:+,.0f} / limit -Rs {float(stk_loss_limit):,.0f}"),
           ("Khule positions", len(rows), int(max_open_pos), f"{len(rows)} / {int(max_open_pos)}"),
           ("LONG positions", n_long, int(max_same_dir), f"{n_long} / {int(max_same_dir)}"),
           ("SHORT positions", n_short, int(max_same_dir), f"{n_short} / {int(max_same_dir)}"),
           ("Aaj ke SL hits", slh, int(stk_max_sl_day), f"{slh} / {int(stk_max_sl_day)}"),
           ("Aaj ke trades", ntr, int(max_stk_trades_day), f"{ntr} / {int(max_stk_trades_day)}")]
    if float(max_open_risk) > 0:
        lim.append(("Total open risk", open_risk, float(max_open_risk), f"Rs {open_risk:,.0f} / Rs {float(max_open_risk):,.0f}"))
    if int(capital_rs) > 0:
        lim.append(("Gross exposure", gross, float(max_gross_x) * float(capital_rs),
                    f"Rs {gross:,.0f} / Rs {float(max_gross_x) * float(capital_rs):,.0f}"))
    for lab, used, cap_, txt in lim:
        frac = min(1.0, used / cap_) if cap_ > 0 else 0.0
        st.caption(f"{'🔴' if frac >= 0.9 else '🟡' if frac >= 0.6 else '🟢'} {lab}: {txt}")
        st.progress(frac)

    # ---- 2. Exposure
    st.markdown("#### 2) Khule positions - exposure")
    if not rows:
        st.info("Abhi koi khula stock position nahi.")
    else:
        pdf = pd.DataFrame(rows)
        gl_long = float(pdf.loc[pdf["side"] == "LONG", "notional"].sum())
        gl_short = float(pdf.loc[pdf["side"] == "SHORT", "notional"].sum())
        sec = pdf.groupby("sector")["notional"].sum().sort_values(ascending=False)
        share = pdf["notional"] / pdf["notional"].sum()
        hhi = float((share ** 2).sum())
        m = st.columns(5)
        m[0].metric("Gross exposure", f"₹{gl_long + gl_short:,.0f}", delta=f"{(gl_long + gl_short) / capital:.1f}x capital")
        m[1].metric("Net exposure", f"₹{gl_long - gl_short:+,.0f}")
        m[2].metric("Open risk (SL tak)", f"₹{open_risk:,.0f}", delta=f"{open_risk / capital * 100:.2f}% capital")
        m[3].metric("Top sector", f"{sec.index[0]} {sec.iloc[0] / sec.sum() * 100:.0f}%")
        m[4].metric("Concentration (HHI)", f"{hhi:.2f}", delta="1.0 = sab ek me" if hhi > 0.4 else "theek")
        show_df(pdf.rename(columns={"sym": "Symbol", "side": "Side", "sector": "Sector", "qty": "Qty", "entry": "Entry", "ltp": "LTP",
                                    "notional": "Notional Rs", "risk": "Risk to SL Rs", "pnl": "Open P&L Rs"})
                .drop(columns=["side_n"]).round(2))
        st.markdown("#### 3) Stress test (khule positions)")
        show_df(stress_open_positions(rows))
        st.caption("Index shock me beta 1 maana hai (asli beta alag ho sakta hai). 'SL ke saath' column me har position ka loss uske SL risk tak seemit maana hai (gap nahi); faayde target tak seemit nahi dikhaye gaye.")

    # ---- 4. Performance & risk stats
    st.markdown("#### 4) Performance aur risk statistics (band trades)")
    j = fetch_journal(limit=5000, status_filter="CLOSED", inst_filter="EQUITY_INTRADAY", mode_filter=fm)
    rm = risk_metrics(j, capital)
    if not rm:
        st.info("Abhi band trades nahi hain.")
    else:
        if rm["n"] < 30:
            st.warning(f"Sirf {rm['n']} trades / {rm['days']} din - VaR, Sharpe jaise numbers pakka nahi. 30+ trades aur 20+ din chahiye.")
        na = lambda v, f: "n/a" if v is None else f.format(v)
        r1 = st.columns(5)
        r1[0].metric("Trades / din", f"{rm['n']} / {rm['days']}")
        r1[1].metric("Win rate", f"{rm['win']:.1f}%")
        r1[2].metric("Payoff (avg win/loss)", f"{rm['payoff']:.2f}")
        r1[3].metric("Profit factor", f"{rm['pf']:.2f}")
        r1[4].metric("Expectancy / trade", f"₹{rm['expectancy']:+,.0f}")
        r2 = st.columns(5)
        r2[0].metric("Gross P&L", f"₹{rm['gross']:+,.0f}")
        r2[1].metric("Charges", f"₹{rm['charges']:,.0f}", delta=na(rm["cost_drag"], "{:.0f}% of gross profit"))
        r2[2].metric("Net P&L", f"₹{rm['net']:+,.0f}")
        r2[3].metric("Max drawdown", f"₹{rm['mdd']:,.0f}", delta=na(rm["mdd_pct"], "{:.1f}% capital"))
        r2[4].metric("Lagataar loss (max)", rm["max_loss_streak"])
        r3 = st.columns(5)
        r3[0].metric("VaR 95% (1 trade)", na(rm["var95"], "₹{:,.0f}"))
        r3[1].metric("CVaR 95% (1 trade)", na(rm["cvar95"], "₹{:,.0f}"))
        r3[2].metric("Sharpe (din, 252)", na(rm["sharpe"], "{:.2f}"))
        r3[3].metric("Sortino", na(rm["sortino"], "{:.2f}"))
        r3[4].metric("Calmar", na(rm["calmar"], "{:.2f}"))
        r4 = st.columns(3)
        r4[0].metric("Kelly fraction", na(rm["kelly"], "{:.1%}"),
                     delta="negative = edge nahi" if rm["kelly"] is not None and rm["kelly"] < 0 else None)
        r4[1].metric("MFE capture (median)", na(rm["capture"], "{:.0%}"))
        r4[2].metric("Best / Worst trade", f"₹{rm['best']:+,.0f} / ₹{rm['worst']:+,.0f}")
        st.caption("VaR/CVaR = ek trade ka 95% worst-case (empirical). Kelly = optimal risk fraction ka sankhyaatmak andaaza; "
                   "negative aaye to abhi edge saabit nahi. Sharpe/Sortino/Calmar 5+ din ke daily net P&L par.")

        # ---- 5. Monte Carlo
        st.markdown("#### 5) Monte Carlo (agle trades ka sambhavit daayra)")
        k1, k2 = st.columns(2)
        nt = int(k1.number_input("Agle kitne trades", value=100, min_value=10, max_value=1000, step=10, key="rd_nt"))
        ddl = float(k2.number_input("Drawdown limit Rs", value=int(capital * 0.1), min_value=1000, step=5000, key="rd_dd"))
        mc = mc_bootstrap(rm["d"]["Net"].values, nt, 5000, ddl)
        if not mc:
            st.info("Monte Carlo ke liye kam se kam 10 trades chahiye.")
        else:
            q = st.columns(5)
            for col, (lab, key) in zip(q, (("5% worst", "p5"), ("25%", "p25"), ("Median", "p50"), ("75%", "p75"), ("95% best", "p95"))):
                col.metric(lab, f"₹{mc[key]:+,.0f}")
            q2 = st.columns(3)
            q2[0].metric("Loss ki sambhavna", f"{mc['p_loss']:.0f}%")
            q2[1].metric(f"DD > ₹{ddl:,.0f} ki sambhavna", f"{mc['p_dd']:.0f}%")
            q2[2].metric("Median max drawdown", f"₹{mc['dd_p50']:,.0f}")
            st.caption(f"{nt} trades ke 5,000 random resample (charges ke baad). Assumption: trades ek-doosre se alag - asli me ek jaise trade "
                       "saath haarte hain, isliye asli drawdown isse bada ho sakta hai.")

        # ---- 6. Sector / reason attribution
        st.markdown("#### 6) Attribution")
        d_ = rm["d"]
        a1, a2 = st.columns(2)
        if "Sector" in d_.columns:
            d_["Sector"] = d_["Sector"].replace("", "n/a").fillna("n/a")
            with a1:
                show_df(d_.groupby("Sector").agg(Trades=("Symbol", "count"), Net=("Net", "sum")).round(0).reset_index().sort_values("Net"))
        with a2:
            d_["Exit"] = d_["Reason"].astype(str).str.split("(").str[0].str.strip()
            show_df(d_.groupby("Exit").agg(Trades=("Symbol", "count"), Net=("Net", "sum")).round(0).reset_index().sort_values("Net"))

    # ---- 7. Audit log
    st.markdown("#### 7) Audit / compliance log (entry, exit, halt, limit-skip)")
    try:
        with db() as conn:
            rows_a = conn.execute("SELECT dt, tm, event, symbol, side, detail FROM audit_log ORDER BY id DESC LIMIT 150").fetchall()
        if rows_a:
            show_df(pd.DataFrame(rows_a, columns=["Date", "Time", "Event", "Symbol", "Side", "Detail"]))
        else:
            st.info("Audit log abhi khali hai.")
    except Exception as e:
        st.caption(f"Audit log nahi padh paya: {e}")


# ====== SECTION: TRADE CHARTS (SVG - koi extra library nahi) ======
CHART_TFS = {"1m": 1, "3m": 3, "5m": 5, "10m": 10, "15m": 15, "30m": 30, "60m": 60}


def _nice_ticks(lo: float, hi: float, n: int = 6) -> list:
    span = max(hi - lo, 1e-9)
    step = 10 ** math.floor(math.log10(span / n))
    for m_ in (1, 2, 2.5, 5, 10):
        if span / (step * m_) <= n:
            step *= m_
            break
    v, out = math.ceil(lo / step) * step, []
    while v <= hi + 1e-9:
        out.append(round(v, 4))
        v += step
    return out


def fetch_trade_events(trade_id: int) -> list:
    out = []
    try:
        with db() as conn:
            rows = conn.execute("SELECT dt, tm, kind, price, price2, note FROM trade_events WHERE trade_id = ? ORDER BY id", (int(trade_id),)).fetchall()
        for dt_, tm_, kind, p1, p2, note in rows:
            out.append({"t": datetime.strptime(f"{dt_} {tm_}", "%Y-%m-%d %H:%M:%S").replace(tzinfo=IST),
                        "kind": kind, "price": p1, "price2": p2, "note": note})
    except Exception:
        pass
    return out


UP_COL, DN_COL = "#0ecb81", "#f6465d"            # hari (upar) / laal (neeche) candle


def save_candles_df(sym: str, df: pd.DataFrame) -> None:
    """1-min candles + unse bane sabhi time frame (3m...60m) DB me."""
    if df is None or df.empty or demo_mode:
        return
    try:
        rows = [(sym, pd.Timestamp(r.ts).tz_convert(IST).strftime("%Y-%m-%d %H:%M:%S"), float(r.o), float(r.h), float(r.l), float(r.c), float(r.v))
                for r in df[["ts", "o", "h", "l", "c", "v"]].itertuples(index=False)]
        with db() as conn:
            conn.executemany("INSERT OR REPLACE INTO candles_1m (sym, ts, o, h, l, c, v) VALUES (?,?,?,?,?,?,?)", rows)
            tf_ = tf_rows(sym, df[["ts", "o", "h", "l", "c", "v"]].sort_values("ts").reset_index(drop=True), recent_only=False)
            if tf_:
                conn.executemany("INSERT OR REPLACE INTO candles_tf (sym, tf, ts, o, h, l, c, v) VALUES (?,?,?,?,?,?,?,?)", tf_)
    except Exception as e:
        try:
            ERR_LOG.append((now_ist().strftime("%H:%M:%S"), -1, "candles-save", str(e)[:120]))
        except Exception:
            pass


def load_candles_range(sym: str, tf: str, d_from: str, d_to: str) -> pd.DataFrame:
    """DB se kisi bhi time frame ke candles (tf: 1m,3m,5m,10m,15m,30m,60m,1D). ts tz-aware IST."""
    try:
        lo, hi = f"{d_from} 00:00:00", f"{d_to} 23:59:59"
        with db() as conn:
            if tf == "1m":
                rows = conn.execute("SELECT ts, o, h, l, c, v FROM candles_1m WHERE sym = ? AND ts >= ? AND ts <= ? ORDER BY ts", (sym, lo, hi)).fetchall()
            else:
                rows = conn.execute("SELECT ts, o, h, l, c, v FROM candles_tf WHERE sym = ? AND tf = ? AND ts >= ? AND ts <= ? ORDER BY ts", (sym, tf, lo, hi)).fetchall()
        if not rows:
            return pd.DataFrame()
        d = pd.DataFrame(rows, columns=["ts", "o", "h", "l", "c", "v"])
        d["ts"] = pd.to_datetime(d["ts"]).dt.tz_localize(IST)
        return d
    except Exception:
        return pd.DataFrame()


def load_candles_db(sym: str, day_iso: str) -> pd.DataFrame:
    return load_candles_range(sym, "1m", day_iso, day_iso)


def candle_db_summary() -> pd.DataFrame:
    """Har time frame ke liye DB me kitne rows / stocks / kaun se din."""
    out = []
    try:
        with db() as conn:
            r = conn.execute("SELECT COUNT(*), COUNT(DISTINCT sym), MIN(substr(ts,1,10)), MAX(substr(ts,1,10)) FROM candles_1m").fetchone()
            out.append({"Time frame": "1m", "Rows": r[0], "Stocks": r[1], "Pehla din": r[2], "Aakhri din": r[3]})
            for tf_, cnt, ns_, d0, d1 in conn.execute("SELECT tf, COUNT(*), COUNT(DISTINCT sym), MIN(substr(ts,1,10)), MAX(substr(ts,1,10)) FROM candles_tf GROUP BY tf").fetchall():
                out.append({"Time frame": tf_, "Rows": cnt, "Stocks": ns_, "Pehla din": d0, "Aakhri din": d1})
    except Exception:
        pass
    order = {"1m": 0, "3m": 1, "5m": 2, "10m": 3, "15m": 4, "30m": 5, "60m": 6, "1D": 7}
    return pd.DataFrame(sorted(out, key=lambda x: order.get(x["Time frame"], 9)))


def bt_candles(sym_label: str, ikey: str, d_from: str, d_to: str, need_days: int) -> pd.DataFrame:
    """Backtest ke liye 1-min candles: pehle DB (agar kaafi din hain), warna Upstox se laakar DB me save."""
    dbdf = load_candles_range(sym_label, "1m", d_from, d_to)
    if not dbdf.empty:
        full_days = int((dbdf.groupby(dbdf["ts"].dt.date).size() >= 300).sum())
        if full_days >= int(need_days) + 1:
            return dbdf
    api = bt_hist_1m(ikey, d_from, d_to)
    if api is not None and not api.empty:
        save_candles_df(sym_label, api)
        return pd.concat([x for x in (dbdf, api) if x is not None and not x.empty], ignore_index=True).drop_duplicates("ts", keep="last").sort_values("ts").reset_index(drop=True)
    return dbdf


def backfill_candles(syms: list, n_days: int, prog=None) -> dict:
    """Upstox se pichhle n_days ke 1-min candles laakar DB me (1m + sabhi time frame). Index bhi."""
    today_ = now_ist().date()
    d_to, d_from = today_.isoformat(), (today_ - timedelta(days=min(29, int(n_days * 1.6) + 6))).isoformat()
    todo = [(s_, C["eq"].get(s_)) for s_ in syms if C["eq"].get(s_)]
    _ifk = (bundle["idx"].get(IDX_UND) or (None, 0))[0]
    todo.append((f"INDEX:{IDX_UND}", _ifk or PRIMARY_INDEX_KEY))
    ok, rows_n = 0, 0
    for i, (lab, ik) in enumerate(todo):
        try:
            df = bt_hist_1m(ik, d_from, d_to)
            if df is not None and not df.empty:
                save_candles_df(lab, df)
                ok += 1
                rows_n += len(df)
        except Exception:
            pass
        if prog is not None:
            prog.progress((i + 1) / max(1, len(todo)))
    return {"stocks": ok, "rows": rows_n, "from": d_from, "to": d_to}


def chart_candles(sym: str, day_iso: str) -> pd.DataFrame:
    """Us din ke 1-min candles: pehle DB (candles_1m), phir Upstox (aaj: intraday, purana din: historical - DB me save bhi)."""
    try:
        if demo_mode:
            df = demo_stock_inputs(sym)["df1m"]
            return df[df["ts"].dt.date == df["ts"].dt.date.max()].reset_index(drop=True)
        dbdf = load_candles_db(sym, day_iso)
        ik = C["eq"].get(sym)
        today = now_ist().date().isoformat()
        live = pd.DataFrame()
        if day_iso == today and ik:
            live = fetch_intraday(ik, TOKEN, 20)
            live = live[live["ts"].dt.date.astype(str) == day_iso] if live is not None and not live.empty else pd.DataFrame()
        elif day_iso != today and len(dbdf) < 300 and ik:
            live = bt_hist_1m(ik, day_iso, day_iso)
            live = live[live["ts"].dt.date.astype(str) == day_iso] if live is not None and not live.empty else pd.DataFrame()
            save_candles_df(sym, live)
        parts = [x for x in (dbdf, live) if x is not None and not x.empty]
        if not parts:
            return pd.DataFrame()
        out = pd.concat(parts, ignore_index=True).drop_duplicates("ts", keep="last").sort_values("ts").reset_index(drop=True)
        return out
    except Exception:
        return pd.DataFrame()


def _ts_of(day_iso: str, hms: str):
    try:
        return datetime.strptime(f"{day_iso} {hms}", "%Y-%m-%d %H:%M:%S").replace(tzinfo=IST)
    except Exception:
        return None


CHART_JS = r"""
(function(){
 var svg=document.getElementById('tc'); if(!svg) return;
 var m=JSON.parse(svg.getAttribute('data-m'));
 var g=svg.querySelector('#xh'), vx=svg.querySelector('#vx'), hy=svg.querySelector('#hy'),
     pb=svg.querySelector('#pbox'), pt=svg.querySelector('#ptag'), hd=svg.querySelector('#hdr');
 function fmt(i){
   var chg=m.o[0]?((m.c[i]-m.o[0])/m.o[0]*100):0;
   return m.t[i]+'   O '+m.o[i].toFixed(2)+'   H '+m.h[i].toFixed(2)+'   L '+m.l[i].toFixed(2)+'   C '+m.c[i].toFixed(2)+
          '   Vol '+Math.round(m.v[i]).toLocaleString()+'   ('+(chg>=0?'+':'')+chg.toFixed(2)+'% din ki shuruaat se)';
 }
 function colorOf(i){ return m.c[i]>=m.o[i] ? m.up : m.dn; }
 function show(i){ hd.textContent=fmt(i); hd.setAttribute('fill',colorOf(i)); }
 function hide(){ g.style.display='none'; show(m.n-1); }
 function move(cx,cy){
   var p=svg.createSVGPoint(); p.x=cx; p.y=cy;
   var q=p.matrixTransform(svg.getScreenCTM().inverse());
   if(q.x<m.L||q.x>m.L+m.pw||q.y<m.T||q.y>m.T+m.ph){ hide(); return; }
   var i=Math.floor((q.x-m.L)/m.stp); i=Math.max(0,Math.min(m.n-1,i));
   var x=m.L+m.stp*(i+0.5);
   g.style.display='';
   vx.setAttribute('x1',x); vx.setAttribute('x2',x);
   hy.setAttribute('y1',q.y); hy.setAttribute('y2',q.y);
   var price=m.hi-(q.y-m.T)/m.ph*(m.hi-m.lo);
   pb.setAttribute('y',q.y-9); pt.setAttribute('y',q.y+4); pt.textContent=price.toFixed(2);
   show(i);
 }
 svg.addEventListener('mousemove',function(e){move(e.clientX,e.clientY);});
 svg.addEventListener('touchmove',function(e){ if(e.touches&&e.touches[0]) move(e.touches[0].clientX,e.touches[0].clientY); },{passive:true});
 svg.addEventListener('touchstart',function(e){ if(e.touches&&e.touches[0]) move(e.touches[0].clientX,e.touches[0].clientY); },{passive:true});
 svg.addEventListener('mouseleave',hide);
 svg.addEventListener('touchend',function(){ setTimeout(hide,1500); });
 show(m.n-1);
})();
"""


def build_trade_chart_svg(sym: str, tf_label: str, c1m: pd.DataFrame, tr: dict, evs: list, show_vwap: bool = True, show_ema: bool = False,
                          W: int = 960, H: int = 600) -> str:
    """Terminal-style candlestick (hari/laal) + volume + VWAP/EMA + (trade ho to) entry / trailing SL / target / partial / exit.
    Crosshair aur OHLC readout CHART_JS se (html wrapper me)."""
    if c1m is None or c1m.empty:
        return ""
    tr = tr or {}
    has_trade = safe_float(tr.get("entry")) > 0
    mins = CHART_TFS.get(tf_label, 5)
    c = c1m if mins == 1 else resample_session(c1m, mins)         # DB me jo candles save hote hain unhi se mel khata hai
    n = len(c)
    if n < 2:
        return ""
    tsn = c["ts"].values
    esc_ = html.escape
    side = str(tr.get("side", "LONG")).upper()
    long_ = side == "LONG"
    L, R, T, B = 68, 104, 92, 34
    vol_h, gap = 64, 14
    price_h = H - T - B - vol_h - gap
    pw = W - L - R
    stp = pw / n
    cw = max(1.6, min(14.0, stp * 0.62))
    halo = ' stroke="#0e1117" stroke-width="3" paint-order="stroke"'

    def xi(i):
        return L + stp * (i + 0.5)

    def idx_of(t):
        if t is None:
            return None
        k = int(np.searchsorted(tsn, np.datetime64(t.astimezone(timezone.utc).replace(tzinfo=None)), side="right")) - 1
        return max(0, min(n - 1, k))

    entry_i = idx_of(tr.get("entry_ts")) if has_trade else 0
    exit_i = (idx_of(tr.get("exit_ts")) if tr.get("exit_ts") is not None else n - 1) if has_trade else n - 1
    entry_i = 0 if entry_i is None else entry_i
    levels = [float(c["h"].max()), float(c["l"].min())]
    if has_trade:
        for k_ in ("entry", "sl0", "sl_now", "tgt"):
            v = safe_float(tr.get(k_))
            if v > 0:
                levels.append(v)
        for e in evs:
            if e["kind"] in ("SL_MOVE", "PARTIAL", "EXIT") and safe_float(e["price"]) > 0:
                levels.append(float(e["price"]))
    hi, lo = max(levels), min(levels)
    pad = (hi - lo) * 0.06 or hi * 0.01
    hi, lo = hi + pad, lo - pad

    def yp(p):
        return T + (hi - p) / (hi - lo) * price_h

    def tlabel(i):
        tt = pd.Timestamp(c["ts"].iloc[i])
        tt = tt.tz_convert(IST) if tt.tzinfo else tt
        return f"{tt:%H:%M}"

    meta = {"L": L, "T": T, "pw": pw, "ph": price_h, "stp": round(stp, 3), "n": n, "hi": round(hi, 4), "lo": round(lo, 4), "up": UP_COL, "dn": DN_COL,
            "t": [tlabel(i) for i in range(n)], "o": [round(float(x), 2) for x in c["o"]], "h": [round(float(x), 2) for x in c["h"]],
            "l": [round(float(x), 2) for x in c["l"]], "c": [round(float(x), 2) for x in c["c"]], "v": [int(x) for x in c["v"]]}
    o = [f'<svg id="tc" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="100%" data-m="{esc_(json.dumps(meta), quote=True)}" '
         f'style="background:#0e1117;border-radius:8px;font-family:Arial,Helvetica,sans-serif;touch-action:pan-y">']
    # header
    pnl = safe_float(tr.get("pnl"))
    status = tr.get("status", "")
    title = f"{sym}  |  {tf_label}" + (f"  |  {side}  |  {status}  |  P&L Rs {pnl:+,.0f}" if has_trade else "  |  1-min candles se")
    o.append(f'<text x="{L}" y="22" fill="#e6e6e6" font-size="15" font-weight="bold">{esc_(title)}</text>')
    if has_trade:
        sub = (f"Entry {safe_float(tr.get('entry')):.2f}  |  SL {safe_float(tr.get('sl0')):.2f}  |  Target {safe_float(tr.get('tgt')):.2f}"
               + (f"  |  Exit {safe_float(tr.get('exit')):.2f} ({esc_(str(tr.get('reason', '')))})" if status == "CLOSED" else ""))
        o.append(f'<text x="{L}" y="40" fill="#9aa0a6" font-size="12">{sub}</text>')
        lg = [(UP_COL, "Hari candle / jeet"), (DN_COL, "Laal candle / SL / haar"), ("#ff9800", "Trailing SL"), ("#66bb6a", "Target"), ("#ffd54f", "VWAP / Partial"), ("#42a5f5", "Entry price")]
    else:
        lg = [(UP_COL, "Hari candle (close >= open)"), (DN_COL, "Laal candle (close < open)"), ("#ffd54f", "VWAP"), ("#4fc3f7", "EMA9"), ("#ba68c8", "EMA21")]
    lx = L
    for col_l, txt in lg:
        o.append(f'<rect x="{lx}" y="48" width="9" height="9" fill="{col_l}" rx="2"/><text x="{lx + 13}" y="56" fill="#9aa0a6" font-size="10">{esc_(txt)}</text>')
        lx += 138
    _i = n - 1
    _chg = (meta["c"][_i] - meta["o"][0]) / meta["o"][0] * 100 if meta["o"][0] else 0.0
    _hd0 = (f'{meta["t"][_i]}   O {meta["o"][_i]:.2f}   H {meta["h"][_i]:.2f}   L {meta["l"][_i]:.2f}   C {meta["c"][_i]:.2f}   '
            f'Vol {meta["v"][_i]:,}   ({_chg:+.2f}% din ki shuruaat se)')
    o.append(f'<text id="hdr" x="{L}" y="78" fill="{UP_COL if meta["c"][_i] >= meta["o"][_i] else DN_COL}" font-size="12" font-weight="bold">{esc_(_hd0)}</text>')
    # grid + y labels
    for v in _nice_ticks(lo, hi, 6):
        y = yp(v)
        o.append(f'<line x1="{L}" y1="{y:.1f}" x2="{W - R}" y2="{y:.1f}" stroke="#262b36" stroke-width="1"/>')
        o.append(f'<text x="{L - 6}" y="{y + 4:.1f}" fill="#9aa0a6" font-size="11" text-anchor="end">{v:,.2f}</text>')
    every = max(1, int(round(n / 8)))
    for i in range(0, n, every):
        o.append(f'<text x="{xi(i):.1f}" y="{H - 10}" fill="#9aa0a6" font-size="11" text-anchor="middle">{tlabel(i)}</text>')
    # volume
    vmax = float(c["v"].max()) or 1.0
    vy0 = T + price_h + gap + vol_h
    for i in range(n):
        vh = float(c["v"].iloc[i]) / vmax * vol_h
        up = c["c"].iloc[i] >= c["o"].iloc[i]
        o.append(f'<rect x="{xi(i) - cw / 2:.1f}" y="{vy0 - vh:.1f}" width="{cw:.1f}" height="{max(vh, 0.5):.1f}" fill="{UP_COL if up else DN_COL}" opacity="0.55"/>')
    # candles (hari / laal)
    for i in range(n):
        op, hh, ll, cl = (float(c[k].iloc[i]) for k in ("o", "h", "l", "c"))
        col = UP_COL if cl >= op else DN_COL
        y_top, y_bot = yp(max(op, cl)), yp(min(op, cl))
        o.append(f'<line x1="{xi(i):.1f}" y1="{yp(hh):.1f}" x2="{xi(i):.1f}" y2="{yp(ll):.1f}" stroke="{col}" stroke-width="1.2"/>'
                 f'<rect x="{xi(i) - cw / 2:.1f}" y="{y_top:.1f}" width="{cw:.1f}" height="{max(y_bot - y_top, 1.2):.1f}" fill="{col}"/>')
    # day high / low labels
    ih, il = int(c["h"].values.argmax()), int(c["l"].values.argmin())
    o.append(f'<text x="{xi(ih):.1f}" y="{yp(float(c["h"].iloc[ih])) - 6:.1f}" fill="#e6e6e6" font-size="10"{halo} text-anchor="middle">H {float(c["h"].iloc[ih]):.2f}</text>')
    o.append(f'<text x="{xi(il):.1f}" y="{yp(float(c["l"].iloc[il])) + 14:.1f}" fill="#e6e6e6" font-size="10"{halo} text-anchor="middle">L {float(c["l"].iloc[il]):.2f}</text>')
    # overlays: VWAP / EMA
    if show_vwap and len(c1m) > 2:
        tp = (c1m["h"] + c1m["l"] + c1m["c"]) / 3.0
        vw = (tp * c1m["v"]).cumsum() / c1m["v"].replace(0, np.nan).cumsum()
        t1 = c1m["ts"].values
        pts = []
        for i in range(n):
            end = tsn[i] + np.timedelta64(mins, "m")
            k = int(np.searchsorted(t1, end, side="left")) - 1
            if k >= 0 and pd.notna(vw.iloc[k]):
                pts.append(f"{xi(i):.1f},{yp(float(vw.iloc[k])):.1f}")
        if len(pts) > 1:
            o.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="#ffd54f" stroke-width="1.4" opacity="0.9"><title>VWAP</title></polyline>')
    if show_ema:
        for span_, col_ in ((9, "#4fc3f7"), (21, "#ba68c8")):
            em = c["c"].ewm(span=span_, adjust=False).mean()
            o.append(f'<polyline points="{" ".join(f"{xi(i):.1f},{yp(float(em.iloc[i])):.1f}" for i in range(n))}" fill="none" stroke="{col_}" stroke-width="1.2"><title>EMA{span_}</title></polyline>')
    x_end = W - R
    if has_trade:
        xe = xi(entry_i)
        tgt, ent, sl0 = safe_float(tr.get("tgt")), safe_float(tr.get("entry")), safe_float(tr.get("sl0"))
        if tgt > 0:
            o.append(f'<line x1="{xe:.1f}" y1="{yp(tgt):.1f}" x2="{x_end}" y2="{yp(tgt):.1f}" stroke="#66bb6a" stroke-width="1.4" stroke-dasharray="6 4"/>')
            o.append(f'<text x="{x_end + 4}" y="{yp(tgt) + 4:.1f}" fill="#66bb6a" font-size="11">TARGET {tgt:.2f}</text>')
        if ent > 0:
            o.append(f'<line x1="{xe:.1f}" y1="{yp(ent):.1f}" x2="{x_end}" y2="{yp(ent):.1f}" stroke="#42a5f5" stroke-width="1.1" stroke-dasharray="2 4"/>')
            o.append(f'<text x="{x_end + 4}" y="{yp(ent) + 4:.1f}" fill="#42a5f5" font-size="11">ENTRY {ent:.2f}</text>')
        if sl0 > 0:
            o.append(f'<line x1="{xe:.1f}" y1="{yp(sl0):.1f}" x2="{x_end}" y2="{yp(sl0):.1f}" stroke="{DN_COL}" stroke-width="1.2" stroke-dasharray="6 4" opacity="0.8"/>')
            o.append(f'<text x="{x_end + 4}" y="{yp(sl0) + 4:.1f}" fill="{DN_COL}" font-size="11">SL {sl0:.2f}</text>')
        moves = [e for e in evs if e["kind"] == "SL_MOVE"]
        path_pts, cur_sl, cur_i = [], sl0, entry_i
        if moves:
            for e in moves:
                mi = idx_of(e["t"])
                mi = max(entry_i, min(mi if mi is not None else entry_i, exit_i))
                path_pts += [(xi(cur_i), cur_sl), (xi(mi), cur_sl)]
                cur_sl, cur_i = float(e["price"]), mi
            path_pts += [(xi(cur_i), cur_sl), (xi(exit_i if exit_i >= cur_i else cur_i), cur_sl)]
        else:
            sl_now = safe_float(tr.get("sl_now"))
            if sl_now > 0 and sl0 > 0 and abs(sl_now - sl0) > 1e-9:       # purana trade (events nahi): sirf antim SL
                path_pts = [(xi(entry_i), sl0), (xi(entry_i), sl_now), (xi(max(exit_i, entry_i)), sl_now)]
        if len(path_pts) > 1:
            o.append(f'<polyline points="{" ".join(f"{x:.1f},{yp(p):.1f}" for x, p in path_pts)}" fill="none" stroke="#ff9800" stroke-width="2"><title>Trailing SL path</title></polyline>')
            o.append(f'<text x="{x_end + 4}" y="{yp(path_pts[-1][1]) + 16:.1f}" fill="#ff9800" font-size="11">TRAIL SL {path_pts[-1][1]:.2f}</text>')
        for e in moves:
            mi = idx_of(e["t"])
            if mi is not None:
                o.append(f'<g><title>SL {e["price2"]:.2f} -> {e["price"]:.2f} @ {e["t"]:%H:%M:%S} ({esc_(e["note"])})</title>'
                         f'<circle cx="{xi(max(entry_i, min(mi, exit_i))):.1f}" cy="{yp(float(e["price"])):.1f}" r="3.6" fill="#ff9800" stroke="#0e1117" stroke-width="1"/></g>')
        ey = yp(ent) if ent > 0 else yp(float(c["c"].iloc[entry_i]))
        col_e = UP_COL if long_ else DN_COL
        tri = (f"{xe:.1f},{ey - 4:.1f} {xe - 8:.1f},{ey + 12:.1f} {xe + 8:.1f},{ey + 12:.1f}" if long_
               else f"{xe:.1f},{ey + 4:.1f} {xe - 8:.1f},{ey - 12:.1f} {xe + 8:.1f},{ey - 12:.1f}")
        o.append(f'<g><title>ENTRY {side} {ent:.2f} @ {tr.get("entry_hms", "")}</title><polygon points="{tri}" fill="{col_e}" stroke="#fff" stroke-width="1"/></g>')
        o.append(f'<text x="{xe:.1f}" y="{ey + (28 if long_ else -18):.1f}" fill="{col_e}" font-size="11"{halo} font-weight="bold" text-anchor="middle">ENTRY {ent:.2f}</text>')
        for e in evs:
            if e["kind"] == "PARTIAL":
                pi_ = idx_of(e["t"])
                px_, py_ = xi(pi_), yp(float(e["price"]))
                o.append(f'<g><title>PARTIAL {esc_(e["note"])} @ {float(e["price"]):.2f}  Rs {float(e["price2"]):+,.0f}</title>'
                         f'<polygon points="{px_:.1f},{py_ - 7:.1f} {px_ + 7:.1f},{py_:.1f} {px_:.1f},{py_ + 7:.1f} {px_ - 7:.1f},{py_:.1f}" fill="#ffd54f" stroke="#fff" stroke-width="1"/></g>')
                o.append(f'<text x="{px_:.1f}" y="{py_ - 11:.1f}" fill="#ffd54f" font-size="11"{halo} text-anchor="middle">PARTIAL Rs {float(e["price2"]):+,.0f}</text>')
        if status == "CLOSED" and tr.get("exit_ts") is not None and safe_float(tr.get("exit")) > 0:
            xv, yv = xi(exit_i), yp(safe_float(tr["exit"]))
            colx = UP_COL if pnl > 0 else DN_COL
            o.append(f'<g><title>EXIT {esc_(str(tr.get("reason", "")))} @ {safe_float(tr["exit"]):.2f}  Rs {pnl:+,.0f}</title>'
                     f'<line x1="{xv - 7:.1f}" y1="{yv - 7:.1f}" x2="{xv + 7:.1f}" y2="{yv + 7:.1f}" stroke="{colx}" stroke-width="3"/>'
                     f'<line x1="{xv - 7:.1f}" y1="{yv + 7:.1f}" x2="{xv + 7:.1f}" y2="{yv - 7:.1f}" stroke="{colx}" stroke-width="3"/></g>')
            lab = f'EXIT {str(tr.get("reason", ""))[:22]}  Rs {pnl:+,.0f}'
            anchor, tx = ("end", xv - 10) if xv > W * 0.6 else ("start", xv + 10)
            o.append(f'<text x="{tx:.1f}" y="{yv - 10:.1f}" fill="{colx}" font-size="11"{halo} font-weight="bold" text-anchor="{anchor}">{esc_(lab)}</text>')
    # last price tag (terminal jaisa)
    lp = float(c["c"].iloc[-1])
    lcol = UP_COL if lp >= float(c["o"].iloc[-1]) else DN_COL
    o.append(f'<line x1="{L}" y1="{yp(lp):.1f}" x2="{x_end}" y2="{yp(lp):.1f}" stroke="{lcol}" stroke-width="0.9" stroke-dasharray="1 3"/>')
    o.append(f'<rect x="{x_end}" y="{yp(lp) - 9:.1f}" width="{R - 6}" height="18" fill="{lcol}" rx="2"/>'
             f'<text x="{x_end + (R - 6) / 2:.1f}" y="{yp(lp) + 4:.1f}" fill="#0e1117" font-size="11" font-weight="bold" text-anchor="middle">{lp:,.2f}</text>')
    # crosshair layer (JS isko chalata hai)
    o.append(f'<g id="xh" style="display:none;pointer-events:none"><line id="vx" x1="0" y1="{T}" x2="0" y2="{T + price_h + gap + vol_h}" stroke="#9aa0a6" stroke-width="0.8" stroke-dasharray="3 3"/>'
             f'<line id="hy" x1="{L}" y1="0" x2="{x_end}" y2="0" stroke="#9aa0a6" stroke-width="0.8" stroke-dasharray="3 3"/>'
             f'<rect id="pbox" x="{x_end}" y="0" width="{R - 6}" height="18" fill="#2a2f3a" rx="2"/>'
             f'<text id="ptag" x="{x_end + (R - 6) / 2:.1f}" y="0" fill="#e6e6e6" font-size="11" text-anchor="middle"></text></g>')
    o.append('</svg>')
    return "".join(o)


def show_html(content: str, height: int) -> None:
    body = f'<div style="width:100%">{content}</div><script>{CHART_JS}</script>' if 'id="tc"' in content else f'<div style="width:100%">{content}</div>'
    try:
        import streamlit.components.v1 as _comp
        _comp.html(body, height=height, scrolling=False)
    except Exception:
        st.markdown(content, unsafe_allow_html=True)


def render_charts_tab():
    st.subheader("📈 Charts - candlestick (hari/laal), entry, trailing SL, target aur exit")
    st.caption("Table me jis trade ke saamne '📈 Chart' tick karoge, uska chart neeche aayega. Hari candle = close >= open, laal candle = close < open. "
               "Chart par ungli ya mouse le jao to crosshair aur us candle ka OHLC/volume upar dikhega. ▲/▼ entry, narangi line trailing SL ka raasta, "
               "hari dashed target, laal dashed shuruaati SL, peela ◆ partial, ✕ exit. Candles DB (candles_1m) me save hote hain, isliye purane din ke chart bhi dikhte hain. "
               "Trailing SL ka poora raasta sirf v7.1 ke baad ke trades ka record hota hai.")
    c1, c2, c3 = st.columns(3)
    fm = c1.selectbox("Mode", ["LIVE", "DEMO", "ALL"], index=1 if demo_mode else 0, key="ch_mode")
    tf_label = c2.radio("Time frame", list(CHART_TFS), index=2, horizontal=True, key="ch_tf")
    opts = list(c3.multiselect("Extra lines", ["VWAP", "EMA 9/21"], default=["VWAP"], key="ch_opts") or [])
    j = fetch_journal(limit=800, status_filter="ALL", inst_filter="EQUITY_INTRADAY", mode_filter=fm)
    if j.empty:
        st.info("Abhi koi stock trade nahi hai - neeche 'Koi bhi stock ka chart' se kisi bhi stock ka chart dekho.")
    else:
        days = sorted(j["Date"].astype(str).unique(), reverse=True)[:15]
        day_iso = st.selectbox("Din", days, index=0, key="ch_day")
        jd = j[j["Date"].astype(str) == day_iso].copy().sort_values("ID", ascending=False)
        all_open = st.checkbox("Sab khule (OPEN) trades ke chart dikhao", value=False, key="ch_allopen")
        show = jd[["ID", "Symbol", "Side", "Status", "In", "Out", "Entry", "LTP/Exit", "SL", "Target", "P&L Rs", "Reason"]].copy()
        show.insert(0, "📈 Chart", jd["Status"].eq("OPEN").values if all_open else False)
        try:
            edited = st.data_editor(show, hide_index=True, key="ch_table", disabled=[c for c in show.columns if c != "📈 Chart"],
                                    column_config={"📈 Chart": st.column_config.CheckboxColumn("📈 Chart", help="Tick karo - chart neeche dikhega")})
        except Exception:
            edited = show
        picked = edited[edited["📈 Chart"] == True]          # noqa: E712
        if picked.empty:
            st.info("Chart dekhne ke liye upar table me kisi trade ke saamne '📈 Chart' tick karo.")
        for _, row in picked.head(12).iterrows():
            tr_row = jd[jd["ID"] == row["ID"]].iloc[0]
            evs = fetch_trade_events(int(row["ID"]))
            c1m = chart_candles(str(row["Symbol"]), day_iso)
            sl_now = safe_float(tr_row["SL"])
            ent_ev = next((e for e in evs if e["kind"] == "ENTRY"), None)
            sl0 = safe_float(ent_ev["price2"]) if ent_ev else sl_now
            exit_ts = _ts_of(day_iso, str(tr_row["Out"])) if str(tr_row["Status"]) == "CLOSED" else None
            tr = {"side": tr_row["Side"], "status": tr_row["Status"], "entry": safe_float(tr_row["Entry"]), "entry_ts": _ts_of(day_iso, str(tr_row["In"])),
                  "entry_hms": str(tr_row["In"]), "exit": safe_float(tr_row["LTP/Exit"]), "exit_ts": exit_ts, "sl0": sl0, "sl_now": sl_now,
                  "tgt": safe_float(tr_row["Target"]), "pnl": safe_float(tr_row["P&L Rs"]), "reason": tr_row["Reason"]}
            svg = build_trade_chart_svg(str(row["Symbol"]), tf_label, c1m, tr, evs, show_vwap="VWAP" in opts, show_ema="EMA 9/21" in opts)
            st.markdown(f"**{row['Symbol']}** · {tr_row['Side']} · {tr_row['Status']} · ID {int(row['ID'])}")
            if svg:
                show_html(svg, 640)
            else:
                st.warning(f"{row['Symbol']}: is din ke candles nahi mile (token / holiday / Upstox data).")
            if evs:
                with st.expander("Is trade ke events (entry, SL move, partial, exit)"):
                    show_df(pd.DataFrame([{"Time": f"{e['t']:%H:%M:%S}", "Event": e["kind"], "Price": round(float(e["price"]), 2),
                                           "Detail": (f"pehle SL {e['price2']:.2f}" if e["kind"] == "SL_MOVE" else
                                                      f"SL {e['price2']:.2f}" if e["kind"] == "ENTRY" else f"Rs {e['price2']:+,.0f}"),
                                           "Note": e["note"]} for e in evs]))
    # ---- koi bhi stock ka chart
    st.markdown("---")
    st.markdown("#### 🔍 Koi bhi stock ka chart")
    k1, k2 = st.columns(2)
    sym2 = k1.selectbox("Stock", list(SYMBOLS), index=0, key="ch_free_sym")
    try:
        with db() as conn:
            dbdays = [r[0] for r in conn.execute("SELECT DISTINCT substr(ts, 1, 10) FROM candles_1m WHERE sym = ? ORDER BY 1 DESC LIMIT 20", (sym2,)).fetchall()]
    except Exception:
        dbdays = []
    today_iso = now_ist().date().isoformat()
    opts_days = [today_iso] + [d_ for d_ in dbdays if d_ != today_iso]
    day2 = k2.selectbox("Din ", opts_days, index=0, key="ch_free_day")
    with st.expander("💾 Candles ka DB - sabhi time frame (dekho / backfill / CSV download)"):
        st.caption("Har scan par 1m aur sabhi time frame (3m, 5m, 10m, 15m, 30m, 60m) ke candles DB me save hote hain, aur daily (1D) bhi. "
                   "Backtest pehle isi DB se data leta hai. Time frame NSE session (9:15) se aligned hote hain (60m: 9:15, 10:15 ...).")
        sm = candle_db_summary()
        if sm.empty:
            st.info("DB me abhi candles nahi hain - app live scan chalane par ya neeche backfill se bharte hain.")
        else:
            show_df(sm)
        b1, b2 = st.columns(2)
        nbf = b1.slider("Backfill: pichhle kitne trading din", 1, 25, 10, key="bf_days")
        nsy = b2.slider("Backfill: kitne stocks (weight ke hisaab se top)", 5, len(SYMBOLS), min(30, len(SYMBOLS)), key="bf_syms")
        if st.button("📥 Backfill chalao (Upstox se candles DB me)", key="bf_run"):
            if demo_mode or not TOKEN:
                st.warning("Backfill ke liye asli Upstox token chahiye (demo mode me nahi).")
            else:
                pr = st.progress(0.0)
                with st.spinner("Candles laa kar DB me save ho rahe hain..."):
                    top = sorted(SYMBOLS, key=lambda z: -W.get(z, 0.0))[:int(nsy)]
                    rep_ = backfill_candles(top, int(nbf), pr)
                st.success(f"{rep_['stocks']} instruments, {rep_['rows']:,} 1-min candles ({rep_['from']} se {rep_['to']}) DB me save.")
        e1, e2, e3 = st.columns(3)
        ex_sym = e1.selectbox("Export: stock", [f"INDEX:{IDX_UND}"] + list(SYMBOLS), key="ex_sym")
        ex_tf = e2.selectbox("Export: time frame", ["1m", "3m", "5m", "10m", "15m", "30m", "60m", "1D"], index=2, key="ex_tf")
        ex_days = e3.slider("Export: pichhle kitne calendar din", 1, 60, 10, key="ex_days")
        d_to_ = now_ist().date()
        exdf = load_candles_range(ex_sym, ex_tf, (d_to_ - timedelta(days=int(ex_days))).isoformat(), d_to_.isoformat())
        if exdf.empty:
            st.caption("Is selection ke liye DB me candles nahi mile.")
        else:
            out_ = exdf.assign(ts=exdf["ts"].dt.strftime("%Y-%m-%d %H:%M:%S"))
            st.caption(f"{len(out_):,} candles ({out_['ts'].iloc[0]} se {out_['ts'].iloc[-1]})")
            st.download_button(f"⬇ {ex_sym} {ex_tf} candles CSV", out_.to_csv(index=False).encode("utf-8"),
                               file_name=f"{ex_sym.replace(':', '_')}_{ex_tf}_{d_to_:%Y%m%d}.csv", mime="text/csv", key="ex_dl")
    if st.checkbox("Is stock ka chart dikhao", value=False, key="ch_free_on"):
        svg2 = build_trade_chart_svg(sym2, tf_label, chart_candles(sym2, day2), {}, [], show_vwap="VWAP" in opts, show_ema="EMA 9/21" in opts)
        if svg2:
            show_html(svg2, 640)
        else:
            st.warning("Candles nahi mile (token / holiday / data).")


# ====== SECTION: TABS ======
tab6, tab1, tab2, tab3, tab4, tab5, tab7, tab8, tab9, tab10 = st.tabs([
    "🧭 All Indices",
    "📊 F&O Scanner + Top Picks",
    "📉 Low-Vol Movers",
    "🎯 Signal Engine & Paper Trade DB",
    "📅 Result Dates",
    "🛠 Diagnostics",
    "📒 Day Report",
    "🧪 Backtest",
    "🏛 Risk Desk",
    "📈 Charts",
])

with tab1:
    st.subheader(f"📊 {universe_mode} — Institutional Filter Matrix & Earnings Lock")
    st.caption(("Stock mode: har filter us STOCK ke apne data par - trend, RS (sector peers ke mukable), choppy aur Bull/Bear Power % (us stock ke apne signals; "
                "score +8 = 100%). Upar ka weighted Signal Power sirf Index engine ke liye hai.") if basis_stock else
               "Index mode: filters Nifty/BankNifty ke haal par (purana tareeka).")
    if not df_all.empty:
        picks = df_all[df_all["Final Action"].str.startswith(("🟢", "🔻"))].sort_values("Rank", ascending=False).head(8)
        st.markdown("#### 🏆 Top Picks (clean signals, rank-wise)")
        if picks.empty:
            st.caption("Abhi koi clean STRONG signal nahi - sabr. (Result-locked / extended / against-index stocks yahan nahi aate.)")
        else:
            show_df(picks[["Symbol", "Final Action"] + ([WHY_COL] if WHY_COL in picks.columns else []) + ["Rank", "Filter Score (-8..+8)", "LTP", "RS vs Index %", "SL", "Target",
                           "Lots", "Qty"]].style.format({k: v for k, v in FMT.items() if k in
                          ["LTP", "RS vs Index %", "SL", "Target", "Lots", "Qty", "Rank"]}, na_rep="—"))
        st.markdown("#### Full Matrix")
        if not df_display.empty:
            show_df(styled(df_display))
            st.download_button("⬇ Download Scanner CSV", df_display[[c for c in SHOW_ORDER if c in df_display.columns]]
                               .to_csv(index=False).encode("utf-8"),
                               file_name=f"fno_scanner_{now_ist():%Y%m%d_%H%M}.csv", mime="text/csv")
        else:
            st.warning("Koi stock filter criteria se match nahi hua.")

with tab2:
    st.subheader(f"📉 Low-Beta F&O Shares (Monthly High-Low Range < {max_monthly_move_th:.1f}%)")
    st.caption("Option selling / Iron Condor / low-beta intraday setups ke liye. 0% (data missing) wale stocks nahi ginte.")
    if not df_all.empty:
        lv = df_all[(df_all["1M Move %"] > 0) & (df_all["1M Move %"] < max_monthly_move_th)].sort_values("1M Move %")
        if not lv.empty:
            show_df(styled(lv))
        else:
            st.info(f"Abhi koi bhi share {max_monthly_move_th:.1f}% monthly move ke neeche nahi hai.")

with tab3:
    st.subheader(f"🎯 {PRIMARY_INDEX_NAME} Signal Engine & Paper Trade Analytics")
    if IDX_UND not in ("NIFTY", "BANKNIFTY"):
        st.caption("ℹ Bull/Bear power chune hue stock universe se aata hai (breadth proxy) - is index ke apne constituents se nahi.")
    side = sig["side"]
    badge = {"LONG": "#00c853", "SHORT": "#ff5252", "FLAT": "#9e9e9e"}[side]
    live_pts = ((ictx["spot"] - sig["entry"]) * (1 if side == "LONG" else -1)) if side != "FLAT" else 0.0
    st.markdown(
        f"<div style='padding:14px;border-radius:10px;border:1px solid {badge};'>"
        f"<span style='font-size:26px;font-weight:700;color:{badge}'>{esc(side)}</span> &nbsp; "
        f"<span>Spot <b>{ictx['spot']:.2f}</b> ({ictx['chg_pct']:+.2f}%) | Src: {esc(ictx['src'])}</span><br>"
        + (f"Entry <b>{sig['entry']:.1f}</b> @ {esc(sig['t_entry'])} | SL <b>{sig['sl']:.1f}</b> | TGT <b>{sig['tgt']:.1f}</b> | "
           f"Live <b>{live_pts:+.1f} pts</b> (Rs {live_pts * ictx['lot'] * int(idx_lots):+,.0f})<br>" if side != "FLAT" else
           f"Confirming: <b>{esc(sig['pend'])}</b> {sig['pend_n']}/{confirm_n}<br>")
        + f"Last event: {esc(sig['last_event'])} | Today Index P&L: Rs {sig['pnl']:+,.0f} | SL hits: {sig['sl_hits']}</div>",
        unsafe_allow_html=True,
    )
    if sig["blockers"]:
        st.warning("⛔ Entry blocked: " + " | ".join(sig["blockers"]))
    if not ictx["ok"]:
        st.error("Index data nahi aaya (token/market/instrument). Diagnostics tab dekhein.")

    if zone_filter and ictx["zone"]:
        st.warning(f"🟠 **15m CONSOLIDATION - NO TRADE ZONE**: {ictx['z_lo']:.0f} – {ictx['z_hi']:.0f} "
                   f"(range {ictx['z_rng']}x ATR15). Breakout (buffer ke saath) ka wait karein.")
    a, b, c_, d_ = st.columns(4)
    a.metric("Index 5m Trend", {1: "BULL 🟢", -1: "BEAR 🔴", 0: "FLAT ⚪"}[ictx["trend_dir"]])
    b.metric("15m MTF", {1: "BULL 🟢", -1: "BEAR 🔴", 0: "FLAT ⚪"}[ictx["mtf_dir"]])
    c_.metric("ORB", {1: "BREAKOUT 🔼", -1: "BREAKDOWN 🔽", 0: "INSIDE" if ictx["orb_ready"] else "FORMING"}[ictx["orb_dir"]])
    d_.metric("Index Futures OI", ictx["fut_text"])
    e, f, g, h_ = st.columns(4)
    e.metric("PCR (ATM ±800)", ictx["pcr"] if ictx["pcr"] is not None else "N/A",
             delta=f"{ictx['pcr_delta']:+.2f} / {oi_window}m" if ictx["pcr_delta"] is not None else None)
    f.metric("PCR of OI Change", ictx["pcr_oi_chg"] if ictx["pcr_oi_chg"] is not None else "N/A")
    g.metric("Max Pain", f"{ictx['max_pain']:.0f}" if ictx["max_pain"] else "N/A")
    h_.metric("ATR(5m) / ADX", f"{ictx['atr']:.1f} / {ictx['adx']:.0f}")
    st.markdown(
        f"**OI Walls** → Resistance (Call): `{ictx['call_wall'] if ictx['call_wall'] else 'N/A'}` | "
        f"Support (Put): `{ictx['put_wall'] if ictx['put_wall'] else 'N/A'}` | Expiry: `{ictx['expiry'] or 'N/A'}`  \n"
        f"**Gamma regime:** {esc(ictx['gex_text'])}" + (f" (ratio {ictx['gex_ratio']})" if ictx["gex_ratio"] is not None else "")
    )
    mi = ictx["m"]
    if mi["ok"]:
        st.caption(f"VWAP {mi['vwap']} (±1σ {mi['vwap_dn1']}–{mi['vwap_up1']}, ±2σ {mi['vwap_dn2']}–{mi['vwap_up2']}) | "
                   f"ORH/ORL {mi['orh']}/{mi['orl']} | Day H/L {mi['day_high']}/{mi['day_low']} | EMA9/21(5m) {mi['ema9']}/{mi['ema21']}")
    if mi["ok"] and mi["z15_hi"] > 0:
        st.caption(f"15m Zone: {mi['z15_lo']}–{mi['z15_hi']} | range {mi['z15_rng_atr']}x ATR15 | "
                   f"ADX15 {mi['adx15']} | Consolidation: {'YES' if mi['z15_cons'] else 'NO'} | Status: {ictx['zone_txt']}")
    with SNAP_LOCK:
        hist = list(SNAP.get("pwr_hist", []))
    if len(hist) >= 2:
        st.markdown("#### Bull / Bear Power (session)")
        st.line_chart(pd.DataFrame(hist).set_index("t"))

    st.divider()
    st.markdown("### 📈 Live Paper Trade Journal & Deep Analysis (`bni_institutional_signals.db`)")
    f_col1, f_col2, f_col3, f_col4 = st.columns([1.3, 1.3, 1.3, 2.1])
    with f_col1:
        j_status = st.selectbox("Status Filter", ["ALL", "OPEN", "CLOSED"], index=0)
    with f_col2:
        j_type = st.selectbox("Instrument Filter", ["ALL", "INDEX", "EQUITY_INTRADAY"], index=0)
    with f_col3:
        j_mode = st.selectbox("Mode Filter", ["ALL", "LIVE", "DEMO"], index=0)
    with f_col4:
        j_limit = st.slider("Max rows from DB", 50, 2000, 300, step=50)

    jdf = fetch_journal(limit=j_limit, status_filter=j_status, inst_filter=j_type, mode_filter=j_mode)

    if not jdf.empty:
        closed_df = jdf[jdf["Status"] == "CLOSED"].copy()
        open_df = jdf[jdf["Status"] == "OPEN"].copy()

        total_pnl = float(closed_df["P&L Rs"].fillna(0).sum()) if not closed_df.empty else 0.0
        open_pnl = float(open_df["P&L Rs"].fillna(0).sum()) if not open_df.empty else 0.0
        wins_df = closed_df[closed_df["P&L Rs"] > 0]
        loss_df = closed_df[closed_df["P&L Rs"] < 0]
        win_rate = (len(wins_df) / len(closed_df) * 100.0) if not closed_df.empty else 0.0
        gross_win = float(wins_df["P&L Rs"].sum()) if not wins_df.empty else 0.0
        gross_loss = abs(float(loss_df["P&L Rs"].sum())) if not loss_df.empty else 0.0
        pf = (gross_win / gross_loss) if gross_loss > 0 else (99.9 if gross_win > 0 else 0.0)
        avg_win = float(wins_df["P&L Rs"].mean()) if not wins_df.empty else 0.0
        avg_loss = float(loss_df["P&L Rs"].mean()) if not loss_df.empty else 0.0

        k1, k2, k3, k4, k5, k6 = st.columns(6)
        k1.metric("Closed Net P&L", f"₹{total_pnl:+,.0f}", delta=f"{len(closed_df)} closed")
        k2.metric("Open Running P&L", f"₹{open_pnl:+,.0f}", delta=f"{len(open_df)} active open")
        k3.metric("Win Rate", f"{win_rate:.1f}%", delta=f"{len(wins_df)}W / {len(loss_df)}L")
        k4.metric("Profit Factor", f"{pf:.2f}")
        k5.metric("Avg Win", f"₹{avg_win:+,.0f}")
        k6.metric("Avg Loss", f"₹{avg_loss:+,.0f}")

        show_df(jdf)

        dl1, dl2 = st.columns(2)
        with dl1:
            st.download_button(
                "⬇ Download Paper Trade Journal (CSV for Excel Analysis)",
                jdf.to_csv(index=False).encode("utf-8"),
                file_name=f"paper_trades_db_{now_ist():%Y%m%d_%H%M}.csv",
                mime="text/csv",
                use_container_width=True,
            )
        with dl2:
            if os.path.exists(DB_PATH):
                with open(DB_PATH, "rb") as _dbf:
                    st.download_button(
                        "🗄 Download Full SQLite DB Backup (.db)",
                        data=_dbf.read(),
                        file_name=f"bni_institutional_signals_{now_ist():%Y%m%d}.db",
                        mime="application/octet-stream",
                        use_container_width=True,
                    )

        if not closed_df.empty:
            b_col1, b_col2 = st.columns(2)
            with b_col1:
                with st.expander("📊 Symbol & Side-wise Performance Breakdown", expanded=True):
                    sym_grp = (
                        closed_df.groupby(["Symbol", "Side"])
                        .agg(
                            Trades=("ID", "count"),
                            Win_Pct=("P&L Rs", lambda x: round((x > 0).mean() * 100, 1)),
                            Net_PnL_Rs=("P&L Rs", lambda x: round(x.sum(), 2)),
                            Avg_MFE=("MFE", lambda x: round(x.mean(), 2)),
                            Avg_MAE=("MAE", lambda x: round(x.mean(), 2)),
                        )
                        .reset_index()
                        .sort_values("Net_PnL_Rs", ascending=False)
                    )
                    show_df(sym_grp)
            with b_col2:
                with st.expander("🏁 Exit Reason & Daily Breakdown", expanded=True):
                    rsn_grp = (
                        closed_df.groupby("Reason")
                        .agg(
                            Trades=("ID", "count"),
                            Win_Pct=("P&L Rs", lambda x: round((x > 0).mean() * 100, 1)),
                            Net_PnL_Rs=("P&L Rs", lambda x: round(x.sum(), 2)),
                        )
                        .reset_index()
                        .sort_values("Net_PnL_Rs", ascending=False)
                    )
                    show_df(rsn_grp)

        if len(closed_df) >= 2:
            eq_df = closed_df.iloc[::-1].copy()
            eq_df["Cumulative P&L (Rs)"] = eq_df["P&L Rs"].cumsum()
            st.markdown("#### 💹 Cumulative Equity Curve (Closed Trades)")
            st.line_chart(eq_df.set_index("ID")["Cumulative P&L (Rs)"])
    else:
        st.info("Database mein abhi is filter ke saath koi paper trade record nahi hai. Jaise hi signal confirm hoga, yahan LIVE dikhega.")

    st.markdown("#### Signal Event Log")
    ldf = fetch_db_logs(60)
    if not ldf.empty:
        show_df(ldf)

with tab4:
    st.subheader("📅 Result Dates - Exact date set karo (Auto Week + Red No-Trade Lock)")
    st.markdown(
        f"Rule abhi: **{lock_mode}**"
        + (f" (result se {pre_days} trading din pehle se {post_days} din baad tak lock)" if lock_mode == "Window" else " (result usi hafte me ho to lock)")
        + ". Jin stocks ki exact date nahi hai unke liye sirf *approx pattern* use hota hai - NSE board-meeting calendar se exact date bharna behtar hai."
    )
    cur = load_custom_earnings()
    edit_df = pd.DataFrame({"Symbol": SYMBOLS, "Result Date": [to_date(cur.get(s)) for s in SYMBOLS]})
    edited = st.data_editor(
        edit_df, hide_index=True, use_container_width=True, disabled=["Symbol"], key="earn_editor",
        column_config={"Result Date": st.column_config.DateColumn("Result Date", format="YYYY-MM-DD")},
    )
    cs1, cs2 = st.columns(2)
    with cs1:
        if st.button("💾 Save All Result Dates", use_container_width=True):
            for _, r in edited.iterrows():
                d_ = to_date(r["Result Date"])
                if d_:
                    save_earnings_date(r["Symbol"], d_.isoformat())
                else:
                    delete_earnings_date(r["Symbol"])
            st.success("Result dates save ho gayi.")
            st.rerun()
    with cs2:
        up = st.file_uploader("CSV upload (columns: Symbol, Result Date)", type=["csv"])
        if up is not None and st.button("📥 Import CSV", use_container_width=True):
            try:
                cdf = pd.read_csv(up)
                cdf.columns = [str(c).strip().title() for c in cdf.columns]
                n = 0
                for _, r in cdf.iterrows():
                    d_, sym = to_date(r.get("Result Date")), str(r.get("Symbol", "")).upper().strip()
                    if d_ and sym:
                        save_earnings_date(sym, d_.isoformat())
                        n += 1
                st.success(f"{n} dates import ho gayi.")
                st.rerun()
            except Exception as e:
                st.error(f"CSV error: {e}")
    if not df_all.empty:
        st.markdown("#### Current lock status")
        show_df(df_all[["Symbol", "Result Date", "Result Week", "Date Source", "Result Trade Lock"]]
                .style.apply(highlight_result_and_signals, axis=1))

with tab5:
    st.subheader("🛠 Diagnostics")
    d1, d2, d3, d4 = st.columns(4)
    d1.metric("API calls (60s)", api_calls_last(60))
    d2.metric("API calls (30m) / 2000", api_calls_last(1800))
    d3.metric("Stock candle TTL (s)", eff_ttl)
    d4.metric("Stocks with data", f"{int(df_all['_ok'].sum()) if not df_all.empty else 0} / {len(SYMBOLS)}")
    miss_eq = [s for s in SYMBOLS if s not in bundle["eq"]]
    miss_fut = [s for s in SYMBOLS if s not in bundle["fut"]]
    st.caption(f"Cash map missing: {miss_eq or 'none'} | Futures map missing: {miss_fut or 'none'} | "
               f"Index fut: {bundle['idx'].get(IDX_UND, ('-', 0))[0]} (lot {ictx['lot']}) | DB: {DB_PATH}")
    _gaps = SNAP.get("hb_gaps", [])
    if _gaps:
        st.markdown("#### ⏱ App ruka (2 min se zyada gap)")
        show_df(pd.DataFrame(_gaps[::-1], columns=["Time", "Gap (sec)"]))
    errs = list(ERR_LOG)[-40:]
    if errs:
        st.markdown("#### Recent API / processing errors")
        show_df(pd.DataFrame(errs[::-1], columns=["Time", "Code", "Where", "Detail"]))
    else:
        st.success("Koi recent error nahi.")
    st.info("⚠ Yeh tool decision-support hai, financial advice nahi. Pehle paper/demo me forward-test karein, "
            "phir chhote size se live jayein. Signals guarantee nahi - SL hamesha follow karein.")

# ====== SECTION: ALL INDICES TAB ======
with tab6:
    st.subheader("All Indices - NSE + BSE (technical + option chain snapshot)")
    if not scan_all_idx:
        st.info("Sidebar me 'Scan ALL indices' on karein - abhi sirf engine wala index dikh raha hai.")
    _dm = {1: "BULL 🟢", -1: "BEAR 🔴", 0: "FLAT ⚪"}
    _nan = float("nan")
    irows = []
    for _u, _cx in IDX_CTX.items():
        irows.append({
            "Index": INDEX_CATALOG[_u]["name"], "Exch": INDEX_CATALOG[_u]["exch"],
            "Spot": _cx["spot"] if _cx["ok"] else _nan, "Day %": _cx["chg_pct"] if _cx["ok"] else _nan,
            "5m Trend": _dm[_cx["trend_dir"]], "15m MTF": _dm[_cx["mtf_dir"]],
            "ORB": {1: "BREAKOUT 🔼", -1: "BREAKDOWN 🔽", 0: "INSIDE" if _cx["orb_ready"] else "FORMING"}[_cx["orb_dir"]],
            "Fut OI": _cx["fut_text"], "RSI": _cx["rsi"], "ADX": _cx["adx"], "ATR(5m)": _cx["atr"],
            "PCR": _cx["pcr"] if _cx["pcr"] is not None else _nan,
            "Max Pain": _cx["max_pain"] or _nan, "Call Wall": _cx["call_wall"] or _nan, "Put Wall": _cx["put_wall"] or _nan,
            "Gamma": _cx["gex_text"].split(" - ")[0], "15m Zone": _cx["zone_txt"],
            "Lot": _cx["lot"], "Data": "OK" if _cx["ok"] else "NO DATA",
        })
    if irows:
        _fm = {"Spot": "{:.2f}", "Day %": "{:+.2f}%", "RSI": "{:.1f}", "ADX": "{:.1f}", "ATR(5m)": "{:.2f}", "PCR": "{:.2f}",
               "Max Pain": "{:.0f}", "Call Wall": "{:.0f}", "Put Wall": "{:.0f}"}
        show_df(pd.DataFrame(irows).style.format(_fm, na_rep="—"))
        _bad = [r["Index"] for r in irows if r["Data"] != "OK"]
        if _bad:
            st.warning("Data nahi aaya: " + ", ".join(_bad) + " - Diagnostics tab me error code dekho; index key INDEX_CATALOG me check karo.")

# ====== SECTION: DAY REPORT TAB ======
with tab7:
    render_day_report()
    render_filter_analysis()

with tab8:
    render_backtest()

with tab9:
    render_risk_desk()

with tab10:
    render_charts_tab()


# ====== SECTION: AUTO REFRESH ======
if auto_refresh and (LIVE_MKT or demo_mode):
    try:
        from streamlit_autorefresh import st_autorefresh  # pip install streamlit-autorefresh (non-blocking)
        st_autorefresh(interval=int(refresh_sec) * 1000, key="auto_ref")
    except Exception:
        time.sleep(int(refresh_sec))
        st.rerun()

