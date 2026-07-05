# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

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

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
