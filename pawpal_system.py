from dataclasses import dataclass, field
from enum import IntEnum
from typing import Optional


class Priority(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


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
        else:
            pet.remove_task(task)

        return self.all_tasks()
    
        




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