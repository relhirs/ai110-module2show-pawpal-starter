# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## ✨ Features

PawPal+'s scheduling engine (`pawpal_system.py`) implements the following behaviors:

- **Priority-based greedy scheduling** (`build_schedule`) — fills the owner's declared availability by assigning the highest-priority pending tasks first, splitting any leftover slot time so it can be reused by the next task.
- **Chronological sorting** (`sort_by_time`) — returns every one of an owner's tasks ordered by scheduled start time, with unscheduled tasks always pushed to the end of the list.
- **Conflict warnings** (`assign_task`) — rejects a task assignment if its time slot exactly matches a slot already in use, preventing two tasks from double-booking the same time.
- **Daily/weekly/monthly recurrence** (`mark_complete`) — completing a recurring task (`Recurrence.DAILY`, `WEEKLY`, or `MONTHLY`) removes it and automatically creates its next occurrence, with the time slot shifted forward by 24 hours, 7 days, or 30 days respectively.
- **Pet-based filtering** (`filter_by_pet_name`) — retrieves just the tasks belonging to one specific pet, useful for per-pet views.
- **In-place task editing** (`edit_task` / `Task.edit`) — updates a task's title, duration, or priority without disturbing its pet assignment or schedule slot.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
```text
(venv) ~/CodePath AI101/Project/Week 5 ➜ python -m pytest
================================================================= test session starts ==================================================================
platform darwin -- Python 3.14.6, pytest-9.1.1, pluggy-1.6.0
rootdir: /Users/relhirsch/CodePath AI101/Project/Week 5
plugins: anyio-4.14.1
collected 5 items                                                                                                                                      

tests/test_pawpal.py .....                                                                                                                       [100%]

================================================================== 5 passed in 0.02s ===================================================================
these test cover: Sorting Correctness: Verify tasks are returned in chronological order.


Recurrence Logic: Confirm that marking a daily task complete creates a new task for the following day.


Conflict Detection: Verify that the Scheduler flags duplicate times.
```
# Run with coverage:
pytest --cov
```

Sample test output:

```text
=== Alice's Schedule ===
  [  scheduled] Walk Coco              (Coco, HIGH, 9:00 AM - 9:30 AM)
  [  scheduled] Feed Dino              (Dino, HIGH, 10:00 AM - 10:15 AM)

=== Bob's Schedule ===
  [  scheduled] Clean Spiky's Tank     (Spiky, HIGH, 8:00 AM - 8:20 AM)

```

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | sort_by_time | sorts tasks by start time |
| Filtering | filter_by_pet_name | returns tasks that are associated with the specified pet name |
| Conflict handling | assign_task | ensures that no task can override another with a same time conflict |
| Recurring tasks | mark_complete | recreates the task for the specified recurring time after it's been completed |

## 📖 Demo Walkthrough

### Main UI features

The Streamlit app (`app.py`) lets a user:

- Enter an owner name, which creates a `PetOwner` and a `Scheduler` for the session.
- Add one or more pets (name + species) via a form.
- Schedule a task for a pet: title, duration, priority, and a start time. This builds a `TimeSlot` and calls `Scheduler.assign_task`.
- View all of an owner's tasks in a table sorted chronologically by `Scheduler.sort_by_time`.
- Click **Generate schedule** to run `Scheduler.build_schedule`, which greedily fills the owner's availability with pending tasks (highest priority first) and reports which tasks did or didn't fit.

### Example workflow

1. **Add a pet** — enter "Mochi" (dog) and submit. Mochi appears in the pets table with a task count of 0.
2. **Schedule a task** — add "Morning walk", 20 minutes, high priority, for Mochi, starting at 08:00. `assign_task` succeeds, and the task appears in the "Current tasks" table at `08:00`.
3. **Try to double-book** — add another task for Mochi also starting at 08:00. `assign_task` raises a `ValueError` because that `TimeSlot` is already taken; the UI catches it and shows a warning instead of crashing, and the duplicate is not added.
4. **View today's schedule** — click **Generate schedule**. `build_schedule` assigns the owner's declared availability to pending tasks, priority first, and displays the result as a table, plus a success/warning message noting whether every task fit.

### Key Scheduler behaviors shown

- **Sorting** — the "Current tasks" table always reflects `sort_by_time`'s chronological order, so newly added tasks slot into the right position automatically.
- **Conflict warnings** — attempting to assign a task to an already-used `TimeSlot` is blocked by `assign_task` and surfaced as a Streamlit warning rather than an unhandled error.
- **Recurrence** — not wired into the UI yet, but exercised directly in `main.py` and `tests/test_pawpal.py`: completing a `Recurrence.DAILY` task via `mark_complete` removes it and creates a new task for the same time 24 hours later.

### Sample CLI output (`python main.py`)

`main.py` builds two owners with pets and tasks, then deliberately tries to assign a second task ("Feed Coco") to the exact same 9:00–9:30 AM slot already used by "Walk Coco" to exercise the conflict check. Since the script doesn't catch the exception the way `app.py` does, the conflict surfaces as an uncaught error:

```text
$ python main.py
Traceback (most recent call last):
  File "main.py", line 74, in <module>
    scheduler1.assign_task(task=task4, pet=coco)
    ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^
  File "pawpal_system.py", line 103, in assign_task
    raise ValueError(f"{task.slot} already exists and cannot be overridden")
ValueError: TimeSlot(start_minute=540, end_minute=570) already exists and cannot be overridden
```

If the conflicting `assign_task` call is skipped, `print_schedule` calls `build_schedule`, which greedily reassigns each task to Alice's declared availability (`time1`, `time2`, `time3`), and produces:

```text
=== Alice's Schedule ===
[  scheduled] Walk Coco              (Coco, HIGH, 9:00 AM - 9:30 AM)
[  scheduled] Feed Dino              (Dino, HIGH, 10:00 AM - 10:15 AM)
```
