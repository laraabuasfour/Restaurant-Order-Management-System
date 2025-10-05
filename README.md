# Python Project – Restaurant Order Management System

This project satisfies the ENCS3130 Linux Lab Python project requirements by reading all **invoice text files** for a day and producing a **Daily Sales Summary** that includes:
- total orders.
- in restaurant vs takeaway counts.
- item quantities per type (Hummous, Fool, Falafel, Tea, Cola, Water).

## Invoice Format (one order per file)
key:value format (case‑insensitive keys; extra lines are OK). **One item per order**:

```
OrderType: IN
Item: Hummous
Quantity: 2
PricePerItem: 5.0
TotalPrice: 10.0
```

- `OrderType` is `IN` (in‑restaurant) or `OUT` (takeaway).
- `Item` must be one of: `Hummous`, `Fool`, `Falafel`, `Tea`, `Cola`, `Water`.
- `Quantity` is an integer.
- `PricePerItem` and `TotalPrice` are numeric. The program tolerates up to `±0.01` rounding difference between `Quantity*PricePerItem` and `TotalPrice` (it prints a warning instead of failing).

## How to Run
From the `restaurant_order_mgmt/` folder:
 
- Run the file `restaurant_manager.py` 
- The program will process the invoices in the `invoices/` folder automatically.

-The output is saved in a file called **`summary.txt`** inside the project folder, and the same summary is also printed to the terminal.


## Example Output
```
Daily Sales Summary:
--------------------
Total orders: 8

Orders In-Restaurant: 4
Hummous (dishes): 2
Fool (dishes): 1
Falafel (portions): 0
Tea (cups): 2
Cola (cans): 0
Water (bottles): 4


Orders Takeaway: 4
Hummous (dishes): 3
Fool (dishes): 0
Falafel (portions): 3
Tea (cups): 0
Cola (cans): 1
Water (bottles): 1
```
