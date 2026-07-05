from dataclasses import dataclass, field
from enum import IntEnum, Enum, auto
from typing import Optional


class Priority(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3

class Recurrence(Enum):
    DAILY = auto()
    WEEKLY = auto()
    MONTHLY = auto()
    NO_REPEAT = auto()
    
   




@dataclass
class TimeSlot:
    start_minute: int
    end_minute: int

    @property
    def duration_minutes(self) -> int:
        """Return the length of the slot in minutes."""
        return self.end_minute - self.start_minute


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: Priority
    pet: Optional["Pet"] = None
    slot: Optional[TimeSlot] = None
    recurring: Recurrence = Recurrence.NO_REPEAT

    def edit(self, title: Optional[str] = None, duration_minutes: Optional[int] = None, priority: Optional[Priority] = None, ) -> None:
        """Update any provided fields on the task, leaving the rest unchanged."""
        if title is not None:
            self.title = title
        if duration_minutes is not None:
            self.duration_minutes = duration_minutes
        if priority is not None:
            self.priority = priority


@dataclass
class PetOwner:
    name: str
    availability: list[TimeSlot] = field(default_factory=list)
    pets: list["Pet"] = field(default_factory=list)

    def add_pet(self, pet: "Pet") -> None:
        """Attach the pet to this owner and add it to their pet list."""
        pet.owner = self
        self.pets.append(pet)

    def set_availability(self, slots: list[TimeSlot]) -> None:
        """Replace this owner's available time slots."""
        self.availability = slots



@dataclass
class Pet:
    name: str
    species: str
    owner: PetOwner
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Assign the task to this pet and add it to its task list."""
        task.pet = self
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Unassign the task from this pet and remove it from its task list."""
        task.pet = None
        self.tasks.remove(task)


@dataclass
class Scheduler:
    owner: PetOwner

    def all_tasks(self) -> list[Task]:
        """Return every task belonging to any pet owned by this scheduler's owner."""
        return [task for pet in self.owner.pets for task in pet.tasks]

    def assign_task(self, task: Task, pet: Pet) -> None:
        """Assign the task to the given pet, if that pet belongs to this scheduler's owner."""
        if pet.owner is not self.owner:
            raise ValueError(f"{pet.name} does not belong to {self.owner.name}")
        every_task = self.all_tasks()
        
        for stored_task in every_task:
            if stored_task.slot == task.slot:
                raise ValueError(f"{task.slot} already exists and cannot be overridden")
            


        pet.add_task(task)

    def edit_task(self, task: Task, **changes) -> None:
        """Apply the given field changes to a task owned by this scheduler's owner."""
        if task.pet is None or task.pet.owner is not self.owner:
            raise ValueError("task is not assigned to a pet owned by this scheduler's owner")
        task.edit(**changes)

    def mark_complete(self, task: Task, pet: Pet) -> list[Task]:
        """Remove the completed task from its pet and return the owner's remaining tasks."""
        if pet.owner is not self.owner:
            raise ValueError(f"{pet.name} does not belong to {self.owner.name}")
       
        pet.remove_task(task)

        recurrence_offsets = {
            Recurrence.DAILY: 24 * 60,
            Recurrence.WEEKLY: 7 * 24 * 60,
            Recurrence.MONTHLY: 30 * 24 * 60
        }
        offset = recurrence_offsets.get(task.recurring)

        if offset is not None:
            next_slot = (TimeSlot(task.slot.start_minute + offset, task.slot.end_minute + offset) if task.slot is not None else None)
            next_task = Task(
                title=task.title,
                duration_minutes=task.duration_minutes,
                priority=task.priority,
                slot=next_slot,
                recurring=task.recurring
            )

            pet.add_task(next_task)

        return self.all_tasks()
    
    def sort_by_time(self) -> list[Task]:
        """Return this owner's tasks ordered by scheduled start time, unscheduled tasks last."""
        return sorted(
            self.all_tasks(),
            key=lambda task: (task.slot is None, task.slot.start_minute if task.slot else 0),
        )
    
    def filter_by_pet_name(self, pet: Pet) -> list[Task]:
        """Return all of this owner's tasks belonging to the pet with the given name."""
        results = []

        for task in self.all_tasks():
            if task.pet.name == pet.name:
                results.append(task.title)
        return results



    def build_schedule(self) -> dict[str, Task]:
        """Greedily assign available time slots to tasks, highest priority first."""
        schedule: dict[str, Task] = {}
        remaining_slots = sorted(self.owner.availability, key=lambda s: s.start_minute)
        pending_tasks = sorted(self.all_tasks(), key=lambda t: t.priority, reverse=True)

        for task in pending_tasks:
            for i, slot in enumerate(remaining_slots):
                if slot.duration_minutes < task.duration_minutes:
                    continue

                task.slot = TimeSlot(slot.start_minute, slot.start_minute + task.duration_minutes)
                schedule[task.title] = task

                leftover_start = slot.start_minute + task.duration_minutes
                if leftover_start < slot.end_minute:
                    remaining_slots[i] = TimeSlot(leftover_start, slot.end_minute)
                else:
                    remaining_slots.pop(i)
                break

        return schedule