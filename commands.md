# LUTHO-2556 commands

```powershell
# Install (editable) with dev tools
pip install -e .[dev]

# Run
lutho-2556 --run
lutho-2556 --run --imbalink     # + ImbaLink Desk overlay
lutho-2556 --simulate-iphone    # Live iPhone page with a SIMULATED phone
lutho-2556 --doctor             # read-only USB check (run with an iPhone attached)
python -m lutho                 # same, without the console script
python run.py                   # from a checkout, no install

# Standalone ImbaLink Desk
imdesk

# Checks
pytest -q
python tools/smoke_ui.py
python tools/verify_imbalink.py
```
