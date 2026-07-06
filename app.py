from datetime import time

import streamlit as st

from pawpal_system import Pet, PetOwner as Owner, Priority, Scheduler, Task, TimeSlot


def minutes_to_label(total_minutes: int) -> str:
    """Format a minute-of-day offset as an HH:MM clock label."""
    hours, minutes = divmod(total_minutes % (24 * 60), 60)
    return f"{hours:02d}:{minutes:02d}"

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name=owner_name)
owner = st.session_state.owner

if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler(owner=owner)
scheduler = st.session_state.scheduler

st.markdown("### Adding a Pet")
with st.form("add_pet_form"):
    pet_name = st.text_input("Pet name", value="Mochi")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    add_pet_submitted = st.form_submit_button("Add pet")

if add_pet_submitted:
    owner.add_pet(Pet(name=pet_name, species=species, owner=owner))
    st.success(f"Added {pet_name} the {species}.")

if owner.pets:
    st.write("Pets:")
    st.table(
        [{"name": p.name, "species": p.species, "tasks": len(p.tasks)} for p in owner.pets]
    )
else:
    st.info("No pets yet. Add one above.")

st.markdown("### Scheduling a Task")
st.caption("Add a few tasks. In your final version, these should feed into your scheduler.")

if owner.pets:
    with st.form("schedule_task_form"):
        task_title = st.text_input("Task title", value="Morning walk")
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
        priority_label = st.selectbox("Priority", ["low", "medium", "high"], index=2)
        pet_name_choice = st.selectbox("Pet", [p.name for p in owner.pets])
        start_time = st.time_input("Start time", value=time(8, 0))
        schedule_task_submitted = st.form_submit_button("Add task")

    if schedule_task_submitted:
        start_minute = start_time.hour * 60 + start_time.minute
        task = Task(
            title=task_title,
            duration_minutes=int(duration),
            priority=Priority[priority_label.upper()],
            slot=TimeSlot(start_minute, start_minute + int(duration)),
        )
        selected_pet = next(p for p in owner.pets if p.name == pet_name_choice)
        try:
            scheduler.assign_task(task, selected_pet)
        except ValueError:
            time_range = f"{minutes_to_label(task.slot.start_minute)}–{minutes_to_label(task.slot.end_minute)}"
            st.warning(f"⚠️ Conflict: {time_range} is already booked for another task.")
        else:
            st.success(f"Assigned '{task_title}' to {pet_name_choice} at {minutes_to_label(start_minute)}.")
else:
    st.info("Add a pet before scheduling tasks.")

sorted_tasks = scheduler.sort_by_time()
if sorted_tasks:
    st.write("Current tasks (sorted by scheduled time):")
    st.table(
        [
            {
                "time": minutes_to_label(t.slot.start_minute) if t.slot is not None else "Unscheduled",
                "title": t.title,
                "pet": t.pet.name if t.pet is not None else "Unassigned",
                "duration_minutes": t.duration_minutes,
                "priority": t.priority.name,
            }
            for t in sorted_tasks
        ]
    )
else:
    st.info("No tasks yet. Add one above.")

st.markdown("### Owner Availability")
st.caption("Build Schedule only fills in time windows you've added here.")

if "availability_slots" not in st.session_state:
    st.session_state.availability_slots = []

with st.form("availability_form"):
    avail_start = st.time_input("Available from", value=time(8, 0), key="avail_start")
    avail_end = st.time_input("Available until", value=time(17, 0), key="avail_end")
    add_availability_submitted = st.form_submit_button("Add availability window")

if add_availability_submitted:
    start_minute = avail_start.hour * 60 + avail_start.minute
    end_minute = avail_end.hour * 60 + avail_end.minute
    if end_minute <= start_minute:
        st.warning("⚠️ End time must be after start time.")
    else:
        st.session_state.availability_slots.append(TimeSlot(start_minute, end_minute))
        st.success(f"Added availability {minutes_to_label(start_minute)}–{minutes_to_label(end_minute)}.")

owner.set_availability(st.session_state.availability_slots)

if owner.availability:
    st.table(
        [
            {"from": minutes_to_label(s.start_minute), "until": minutes_to_label(s.end_minute)}
            for s in owner.availability
        ]
    )
    if st.button("Clear availability"):
        st.session_state.availability_slots = []
        owner.set_availability([])
        st.rerun()
else:
    st.info("No availability windows yet. Add one above before building a schedule.")

st.divider()

st.subheader("Build Schedule")
st.caption("Greedily fills the owner's available time slots, highest priority first.")

if st.button("Generate schedule"):
    schedule = scheduler.build_schedule()
    unscheduled = [t for t in scheduler.all_tasks() if t.title not in schedule]

    if not schedule:
        st.warning("⚠️ No tasks could be scheduled. Add tasks and owner availability first.")
    elif unscheduled:
        st.warning(
            f"⚠️ Scheduled {len(schedule)} task(s), but {len(unscheduled)} could not fit "
            "into the available time slots."
        )
    else:
        st.success(f"✅ All {len(schedule)} task(s) scheduled successfully.")

    if schedule:
        scheduled_tasks = sorted(schedule.values(), key=lambda t: t.slot.start_minute)
        st.table(
            [
                {
                    "time": f"{minutes_to_label(t.slot.start_minute)}–{minutes_to_label(t.slot.end_minute)}",
                    "title": t.title,
                    "pet": t.pet.name if t.pet is not None else "Unassigned",
                    "priority": t.priority.name,
                }
                for t in scheduled_tasks
            ]
        )

    if unscheduled:
        st.write("Unscheduled tasks:")
        st.table(
            [
                {"title": t.title, "pet": t.pet.name if t.pet is not None else "Unassigned", "priority": t.priority.name}
                for t in unscheduled
            ]
        )
