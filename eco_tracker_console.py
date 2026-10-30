#!/usr/bin/env python3
"""
Earth Pulse: Real-Time Environmental Impact Tracker
Continuously computes and visualizes environmental metrics second-by-second.

Configured Rates (per second):
- 🌡️ Carbon Emissions: +0.000003
- 🌫️ Air Pollution: +0.000001
- 🌱 Soil Pollution & Erosion: +0.000001
- 🏜️ Land Degradation: +0.000001
- 🐾 Living Organisms Affected: +0.00002
- ♻️ Plastic Waste Found & Dumped: +0.000003
- 🔄 Plastic Recycled: +0.000002
- 🌳 Plants & Trees Destroyed: +0.000001
"""

import sys
import time
import os
import math
from datetime import datetime
import argparse

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')

# ANSI color codes
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"
WHITE = "\033[97m"

# Specified environmental metrics and their exact second-by-second increments
METRICS = {
    "carbon_emissions": {
        "rate": 0.000003,
        "name": "Carbon Emissions",
        "icon": "🌡️ ",
        "color": RED,
        "category": "Atmosphere"
    },
    "air_pollution": {
        "rate": 0.000001,
        "name": "Air Pollution",
        "icon": "🌫️ ",
        "color": YELLOW,
        "category": "Atmosphere"
    },
    "soil_pollution": {
        "rate": 0.000001,
        "name": "Soil Pollution & Erosion",
        "icon": "🌱",
        "color": MAGENTA,
        "category": "Geosphere"
    },
    "land_degradation": {
        "rate": 0.000001,
        "name": "Land Degradation",
        "icon": "🏜️ ",
        "color": YELLOW,
        "category": "Geosphere"
    },
    "organisms_affected": {
        "rate": 0.000020,
        "name": "Living Organisms Affected",
        "icon": "🐾",
        "color": RED,
        "category": "Biosphere"
    },
    "plastic_dumped": {
        "rate": 0.000003,
        "name": "Plastic Waste Found & Dumped",
        "icon": "♻️ ",
        "color": CYAN,
        "category": "Waste & Oceans"
    },
    "plastic_recycled": {
        "rate": 0.000002,
        "name": "Plastic Recycled",
        "icon": "🔄",
        "color": GREEN,
        "category": "Recovery & Circular"
    },
    "trees_destroyed": {
        "rate": 0.000001,
        "name": "Plants & Trees Destroyed",
        "icon": "🌳",
        "color": GREEN,
        "category": "Biosphere"
    }
}

def format_value(val: float) -> str:
    """Formats cumulative values with 6 decimal places."""
    return f"{val:.6f}"

def clear_screen():
    """Clear terminal screen cross-platform."""
    if os.name == 'nt':
        os.system('cls')
    else:
        sys.stdout.write("\033[2J\033[H")
        sys.stdout.flush()

def render_dashboard(elapsed_seconds: float, mode: str, multiplier: float):
    """Renders the ANSI dashboard to stdout without per-second increment displays."""
    now = datetime.now()
    now_str = now.strftime("%Y-%m-%d %H:%M:%S")

    # Time calculations
    hours = int(elapsed_seconds // 3600)
    minutes = int((elapsed_seconds % 3600) // 60)
    seconds = int(elapsed_seconds % 60)
    ms = int((elapsed_seconds * 1000) % 1000)
    time_display = f"{hours:02d}:{minutes:02d}:{seconds:02d}.{ms//100:01d}"

    # Mode offset if today or year
    if mode == "today":
        midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
        offset_seconds = (now - midnight).total_seconds()
    elif mode == "year":
        year_start = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        offset_seconds = (now - year_start).total_seconds()
    else:
        offset_seconds = 0.0

    effective_seconds = offset_seconds + (elapsed_seconds * multiplier)

    # Dynamic pulse indicator
    pulse_char = "●" if int(elapsed_seconds * 2) % 2 == 0 else "○"
    pulse_color = GREEN if pulse_char == "●" else CYAN

    w = 78
    lines = []
    lines.append(f"{CYAN}╔{'═' * (w - 2)}╗{RESET}")
    lines.append(f"{CYAN}║{BOLD}{WHITE}{' 🌍 REAL-TIME ENVIRONMENTAL IMPACT TRACKER ':^{w-2}}{RESET}{CYAN}║{RESET}")
    lines.append(f"{CYAN}║{DIM}{'Live Continuous Indicator Monitor (Updating Every Second)':^{w-2}}{RESET}{CYAN}║{RESET}")
    lines.append(f"{CYAN}╠{'═' * (w - 2)}╣{RESET}")

    status_bar = f" {pulse_color}{pulse_char}{RESET} {BOLD}Clock:{RESET} {now_str}  │  {BOLD}Mode:{RESET} {mode.upper()}  │  {BOLD}Elapsed:{RESET} {CYAN}{time_display}{RESET}"
    lines.append(f"{CYAN}║{RESET}{status_bar:<{w + 14}}{CYAN}║{RESET}")
    lines.append(f"{CYAN}╠{'═' * (w - 2)}╣{RESET}")
    
    # Notice: per-second rate column removed as requested
    header_str = f"{BOLD}{' ENVIRONMENTAL INDICATOR':<36}{'LIVE VALUE':<20}{'CATEGORY':<18}{RESET}"
    lines.append(f"{CYAN}║{RESET} {header_str:<{w + 5}}{CYAN}║{RESET}")
    lines.append(f"{CYAN}╠{'─' * (w - 2)}╣{RESET}")

    for key, data in METRICS.items():
        cumul_val = effective_seconds * data["rate"]
        cumul_str = format_value(cumul_val)
        name_str = f"{data['icon']} {data['name']}"

        lines.append(
            f"{CYAN}║{RESET} {data['color']}{name_str:<34}{RESET} "
            f"{BOLD}{WHITE}{cumul_str:<18}{RESET} "
            f"{DIM}{data['category']:<18}{RESET}{CYAN}║{RESET}"
        )

    # Plastic Net Balance
    waste_val = effective_seconds * METRICS["plastic_dumped"]["rate"]
    recycled_val = effective_seconds * METRICS["plastic_recycled"]["rate"]
    net_plastic = waste_val - recycled_val

    lines.append(f"{CYAN}╠{'─' * (w - 2)}╣{RESET}")
    net_str = f" 📊 Net Unrecycled Plastic Waste: {BOLD}{RED}{format_value(net_plastic)}{RESET}"
    lines.append(f"{CYAN}║{RESET}{net_str:<{w + 12}}{CYAN}║{RESET}")
    lines.append(f"{CYAN}╠{'═' * (w - 2)}╣{RESET}")

    # Real-time event ticker without per-second rate numbers
    events = [
        "🌡️ Atmospheric carbon emissions updated",
        "🌳 Forest canopy and plant loss registered",
        "🔄 Plastic recycling stream recorded",
        "♻️ Plastic waste dumping tracked",
        "🐾 Living organisms displacement updated",
        "🌱 Topsoil erosion and soil pollution updated",
        "🌫️ Air quality pollution concentration updated",
        "🏜️ Land degradation & desertification tracked"
    ]
    cur_event = events[int(elapsed_seconds) % len(events)]
    ticker_text = f"  {YELLOW}▶ [LIVE STATUS]{RESET} {cur_event}"
    lines.append(f"{CYAN}║{RESET}{ticker_text:<{w + 7}}{CYAN}║{RESET}")
    lines.append(f"{CYAN}╠{'─' * (w - 2)}╣{RESET}")
    lines.append(f"{CYAN}║{DIM} Press {BOLD}Ctrl+C{RESET}{DIM} anytime to pause and view the final session summary.     {RESET}{CYAN}║{RESET}")
    lines.append(f"{CYAN}╚{'═' * (w - 2)}╝{RESET}")

    clear_screen()
    print("\n".join(lines), flush=True)

def main():
    parser = argparse.ArgumentParser(description="Real-Time Environmental Impact Tracker")
    parser.add_argument("--mode", choices=["session", "today", "year"], default="session",
                        help="Time baseline: 'session' (since started), 'today' (since midnight), or 'year' (since Jan 1)")
    parser.add_argument("--speed", type=float, default=1.0, help="Simulation speed multiplier (default: 1.0)")
    parser.add_argument("--refresh", type=float, default=0.5, help="Refresh interval in seconds (default: 0.5s)")
    args = parser.parse_args()

    start_time = time.time()
    print("Starting Real-Time Environmental Tracker...")
    time.sleep(0.4)

    try:
        while True:
            elapsed = time.time() - start_time
            render_dashboard(elapsed, args.mode, args.speed)
            time.sleep(args.refresh)
    except KeyboardInterrupt:
        total_elapsed = time.time() - start_time
        print(f"\n\n{GREEN}{BOLD}═════════════════════════════════════════════════════════════════{RESET}")
        print(f"{GREEN}{BOLD}           SESSION COMPLETED - FINAL SUMMARY                      {RESET}")
        print(f"{GREEN}{BOLD}═════════════════════════════════════════════════════════════════{RESET}")
        print(f"Tracking Duration: {total_elapsed:.1f} seconds ({total_elapsed/60:.2f} minutes)")
        print(f"Mode:              {args.mode.upper()}\n")

        print(f"{BOLD}Final Accumulated Values:{RESET}")
        report_lines = [
            f"Environmental Impact Summary ({datetime.now().strftime('%Y-%m-%d %H:%M:%S')})",
            f"Tracking Duration: {total_elapsed:.1f} seconds\n"
        ]
        
        for key, data in METRICS.items():
            tot = total_elapsed * data["rate"] * args.speed
            summary_item = f"  • {data['icon']} {data['name']}: {format_value(tot)}"
            print(summary_item)
            report_lines.append(summary_item)

        report_path = os.path.join(os.path.dirname(__file__), "last_session_report.txt")
        try:
            with open(report_path, "w", encoding="utf-8") as f:
                f.write("\n".join(report_lines) + "\n")
            print(f"\n{CYAN}📄 Session report saved to: {report_path}{RESET}")
        except Exception:
            pass

        print(f"{GREEN}{BOLD}═════════════════════════════════════════════════════════════════{RESET}\n")

if __name__ == "__main__":
    main()
