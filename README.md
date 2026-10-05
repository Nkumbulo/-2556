# LUTHO Intelligence — LUTHO-2556

**Company:** LUTHO Intelligence · **Flagship model:** LUTHO-2556 · **Legacy / lab:** LUT-2556 · **CLI:** `lutho-2556 --run`

LUTHO-2556 is a desktop diagnostic command center. The first production module is the **iPhone Panic Analyzer**
(evidence-first parser, signature engine, correlation). **Imba**, the ImbaLink-2556 assistant, explains what LUTHO found,
and **ImbaLink Desk** is the glass desktop overlay.

## Run

```powershell
pip install -e .[dev,usb]    # installs lutho-2556, imdesk, pytest and USB support (pymobiledevice3)
lutho-2556 --run             # or: python -m lutho  /  python run.py (no install needed)
lutho-2556 --run --imbalink  # also launch the ImbaLink Desk overlay (Windows)
lutho-2556 --simulate-iphone # start with a SIMULATED iPhone on the Live page (demo data, no phone needed)
lutho-2556 --doctor          # step-by-step, read-only check of the USB path (run it with an iPhone attached)
lutho-2556 --version
```

## Test

```powershell
pytest -q                          # unit + UI + ImbaLink suites (UI tests need PySide6)
python tools/smoke_ui.py           # structural UI smoke test, no Qt required
python tools/verify_imbalink.py    # static ImbaLink architecture checks
```

## Pages (sidebar order)

| # | Page | What it is |
|---|------|------------|
| 1 | **Overview** | Live stats, quick actions, latest activity |
| 2 | **Synthesize** | Chat with **Imba**, grounded in what LUTHO has loaded |
| 3 | **Diagnostics** | iPhone frame + device picker; drop a log: verdict card + Summary / Evidence / Raw tabs |
| 4 | **Live iPhone** | **Read an iPhone over USB**: device info, health findings, logs -> verdict, repair guide, optional saved record |
| 5 | **Intelligence** | **Prototype:** node graph - wire device intelligence together, add a command, **Synthesize** one source of truth (sample data) |
| 6 | **Reports** | Every report ingested this session |
| – | **ImbaLink Desk** (LAB TOOLS) | Desktop overlay + Control Center |

The iPhone frame shows the device behind the loaded log (model, iOS, verdict). Reading from a connected iPhone is planned; the app has the seam for it (`Workspace.add_reports`) but it is not built yet.

Only **iPhone** has a working analyzer. Other devices in the picker are staged `LAB` entries: selecting one disables
log ingestion instead of faking a result.

## Layout

```text
src/lutho/
  domain/         PanicReport, device taxonomy, intelligence packs, live-iPhone model (pure data)
  parsing/        .ips / .json -> PanicReport
  analysis/       signatures, classification, correlation     (+ data/signatures.json)
  assistant/      Imba: context, providers, engine            (no Qt)
  application/    Workspace, IntelWorkspace, live-iPhone service/parsing/health/records (no Qt)
  integrations/   ImbaLink service (Qt + imba_desk); usb/ = read-only iPhone backends (no Qt)
  resources/      bundled sample log
  ui/             main window, sidebar, pages/, widgets/, theme/ (+ qss/)
  services.py     composition root: build long-lived services
  bootstrap.py    composition root: QApplication + window
  cli.py          argument parsing and entry point (--simulate-iphone, --doctor)
  doctor.py       read-only USB diagnostics report
src/imba_desk/    standalone ImbaLink Desk engine (own architecture, see docs/imbalink-architecture.md)
tests/            unit/  ui/  imbalink/
tools/            smoke_ui.py, fake_qt.py, verify_imbalink.py
docs/             architecture.md, imbalink-*.md
```

Read [docs/architecture.md](docs/architecture.md) for the dependency rule and how to extend each layer.

## Live iPhone over USB

Plug in an iPhone and LUTHO reads **device info** (model, iOS, serial, activation, Find My, storage), **battery** and the **logs on the phone**,
turns them into prioritised **health findings** ("Find My is ON - ask the owner to turn it off before any restore"), reads the **panic logs**
straight into the analyzer for a verdict, builds a **repair-guide command** from what is actually wrong, and lets you **save a record**
(a folder with `device.json` and, if you choose, the raw logs) with your job notes. Nothing is saved unless you press Save.

* **Read-only.** LUTHO never writes to, erases from or changes the iPhone; a test enforces it.
* **Privacy.** No phone number, contacts, messages, photos or app data are collected. Identifiers can be masked on screen and in saved files.
* **Needs** `pip install pymobiledevice3` and, on Windows, the Apple Devices app or iTunes (it provides the Apple Mobile Device Service).
* **Try it without a phone:** `lutho-2556 --simulate-iphone` (every screen is labelled SIMULATED, and saved records say `"simulated": true`).
* **First test with a real phone:** run `lutho-2556 --doctor` and share the output; it shows exactly which step works.
* The USB adapter has not yet been verified on a physical phone. See [docs/live-iphone.md](docs/live-iphone.md).

## Intelligence graph (prototype, fake data)

The Intelligence page is a node canvas in the style of After Effects: drag from a port to another port to wire them.

```text
[iPhone 16] ─────────────────────┐
[Galaxy S24] ──► [P60] ──────────┼──►  [Synthesis]  ──►  one source of truth
[Command: "repair guide for no charging and random reboots"] ──┘
```

* **Add** puts more models on the canvas (iPhone 16, Galaxy S24, P60, Pixel 9, iPhone 13) or a **Command** node.
  Double-click a Command node to type your own command; double-click a wire to remove it; **Delete** removes the selection.
* **Synthesize** (or Ctrl+Enter) merges every model connected upstream of the Synthesis node into ONE source of truth:
  circuits that several models share are matched, their symptoms and checks are merged with "which models support it",
  and the result is a unified overview, shared-circuit comparison and repair guide. The command steers focus and mode.
* **All intelligence packs are fictional sample data** (`src/lutho/resources/prototype/intel_packs.json`) and every screen says so.
  They contain no real voltages, part numbers or specs. The merging logic itself is real and tested.

## Imba (Synthesize)

Imba answers only from loaded evidence (latest report, matched signatures, recurring patterns, overlay state) and says
so when nothing is loaded. The built-in provider is **local and offline** (rule-routed, not a language model). To put a
real model behind the chat, implement `ImbaProvider` and pass it to `build_services`:

```python
class MyModelProvider:
    name = "my-model"
    def reply(self, message, history, context):   # runs on a worker thread
        ...                                         # `context` is the grounded ImbaContext
        return "text"

services = build_services(provider=MyModelProvider())
```
