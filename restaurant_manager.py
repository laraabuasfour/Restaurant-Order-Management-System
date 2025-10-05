#!/usr/bin/env python3
"""
Restaurant Order Management System
Reads invoice text files one item per order from a folder
and creates a daily sales summary.
"""

from __future__ import annotations
import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Tuple
import sys

# Menu items with their units it is used in the summary display
menu_units = {
    "hummous": "dishes",
    "fool": "dishes",
    "falafel": "portions",
    "tea": "cups",
    "cola": "cans",
    "water": "bottles",
}

# valid items and order types for checking input
valid_items = set(menu_units.keys())
valid_order_type = {"in", "out"}

# structure for holding one order data
@dataclass
class Order:
    kind: str  # in or out
    item: str  # item name
    quantity: int
    price_per_item: float
    total_price: float
    source_file: Path  # which file this was read from

def parse_invoice_text(text: str, src: Path) -> Order:
    """
    Read one invoice file and convert it into an Order.
    Extra lines are ignored.
    """

    # split each line into key:value and put in dictionary
    data: Dict[str, str] = {}
    for line in text.splitlines():
        if ":" not in line:   # skip lines without ":"
            continue
        k, v = line.split(":", 1)
        k = k.strip().lower()   # normalize key
        v = v.strip()           # clean value
        data[k] = v

    # check that required fields exist
    required = ["ordertype", "item", "quantity", "priceperitem", "totalprice"]
    missing = [r for r in required if r not in data]
    if missing:
        raise ValueError(f"Missing keys {missing} in invoice '{src.name}'.")

    # check order type is valid
    kind = data["ordertype"].strip().lower()
    if kind not in valid_order_type:
        raise ValueError(f"Invalid OrderType '{data['ordertype']}' in '{src.name}'.")

    # check item is valid
    item = data["item"].strip().lower()
    if item not in valid_items:
        raise ValueError(f"Invalid Item '{data['item']}' in '{src.name}'.")

    # convert quantity to integer
    try:
        qty = int(data["quantity"])
    except Exception:
        raise ValueError(f"Quantity must be an integer in '{src.name}'.")

    # convert prices to float
    try:
        ppi = float(data["priceperitem"])
        tot = float(data["totalprice"])
    except Exception:
        raise ValueError(f"PricePerItem/TotalPrice must be numeric in '{src.name}'.")

    # warn if total price does not match quantity * price per item
    if abs((qty * ppi) - tot) > 1e-2:
        print(f"[WARN] TotalPrice != Quantity * PricePerItem in '{src.name}'", file=sys.stderr)

    # return an Order object with parsed data
    return Order(kind=kind, item=item, quantity=qty,
                 price_per_item=ppi, total_price=tot, source_file=src)

def summarize_orders(orders: Tuple[Order, ...]) -> str:
    """Create the daily sales summary string."""

    # initialize counters for totals
    counts = {
        "total_orders": 0,
        "in": {item: 0 for item in valid_items},
        "out": {item: 0 for item in valid_items},
        "in_total": 0,
        "out_total": 0,
    }

    # go through each order and update counters
    for o in orders:
        counts["total_orders"] += 1
        counts[o.kind + "_total"] += 1
        counts[o.kind][o.item] += o.quantity

    # helper function to format one section (in or out)
    def format_section(kind: str, title: str) -> str:
        lines = [f"{title}: {counts[kind + '_total']}"]
        display_order = ["hummous", "fool", "falafel", "tea", "cola", "water"]
        for item in display_order:
            unit = menu_units[item]
            lines.append(f"{item.capitalize()} ({unit}): {counts[kind][item]}")
        return "\n".join(lines)

    # build final summary text
    header = ["Daily Sales Summary:", "--------------------", f"Total orders: {counts['total_orders']}"]
    in_section = format_section("in", "Orders In-Restaurant")
    out_section = format_section("out", "Orders Takeaway")

    return "\n".join(header) + "\n\n" + in_section + "\n\n\n" + out_section + "\n"

def read_invoices_dir(path: Path) -> Tuple[Order, ...]:
    """Load all .txt invoice files from a folder and turn them into orders."""

    if not path.exists() or not path.is_dir():
        raise FileNotFoundError(f"Invoices directory not found: {path}")
    orders = []
    for file in sorted(path.glob("*.txt")):   # loop through all txt files
        text = file.read_text(encoding="utf-8", errors="ignore")
        order = parse_invoice_text(text, file)
        orders.append(order)
    return tuple(orders)

def write_summary(summary_text: str, out_path: Path) -> None:
    """Save the summary text into the output file."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(summary_text, encoding="utf-8")

def main(argv=None) -> int:
     # define command-line arguments
    parser = argparse.ArgumentParser(
        description="Restaurant Order Management System: read invoices and produce daily summary."
    )
    parser.add_argument(
        "--invoices-dir",
        default="invoices",
        help="Directory containing invoice .txt files (default: invoices)",
    )
    parser.add_argument(
        "--out",
        default="summary.txt",
        help="Path to write the daily summary file (default: summary.txt)",
    )
    # parse arguments from the command line
    args = parser.parse_args(argv)

    # get paths for invoices folder and output summary file
    inv_dir = Path(args.invoices_dir)
    out_path = Path(args.out)
    
    
    orders = read_invoices_dir(inv_dir) # read all invoices and build Order objects
    summary_text = summarize_orders(orders) # create the sales summary text
    write_summary(summary_text, out_path)  # write the summary into the output file

     # print the summary to the terminal
    print(summary_text)
    print(f"Summary written to: {out_path.resolve()}")  # print message to confirm summary was written
    return 0

if __name__ == "__main__":
    raise SystemExit(main())  # run main() when executed directly
