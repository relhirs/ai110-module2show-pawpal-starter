from pawpal_system import Priority, Task, PetOwner, Pet, Scheduler, TimeSlot

owner1 = PetOwner(name="Alice")
scheduler1 = Scheduler(owner=owner1)

owner2 = PetOwner(name="Bob")
scheduler2 = Scheduler(owner=owner2)

coco = Pet(name="Coco", species="Dog", owner=owner1)
owner1.add_pet(coco)

dino = Pet(name="Dino", species="Dog", owner=owner1)
owner1.add_pet(dino)

spiky = Pet(name="Spiky", species="Lizard", owner=owner2)
owner2.add_pet(spiky)


time1 = TimeSlot(start_minute=9 * 60, end_minute=(9 * 60) + 30)  # 9:00 AM to 9:30 AM
time2 = TimeSlot(start_minute=10 * 60, end_minute=(10 * 60) + 30) # 10:00 AM to 10:30 AM
time3 = TimeSlot(start_minute=(5 + 12) * 60, end_minute=(5 + 12) * 60 + 30) # 5:00 PM to 5:30 PM
time4 = TimeSlot(start_minute=8 * 60, end_minute=(8 * 60) + 30) # 8:00 AM to 8:30 AM
time5 = TimeSlot(start_minute=(4 + 12) * 60, end_minute=(4 + 12) * 60 + 10) # 4:00 PM to 4:10 PM
time6 = TimeSlot(start_minute=9 * 60, end_minute=(9 * 60) + 30)  # 9:00 AM to 9:30 AM


task1 = Task(title="Walk Coco", duration_minutes=30, priority=Priority.HIGH, pet=coco, slot = time1)
task2 = Task(title="Feed Dino", duration_minutes=15, priority=Priority.HIGH, pet=dino, slot=time4)
task3 = Task(title="Clean Spiky's Tank", duration_minutes=20, priority=Priority.HIGH, pet=spiky, slot=time3)
task4 = Task(title="Feed Coco", duration_minutes=30, priority=Priority.HIGH, pet=coco, slot = time6)



coco.add_task(task=task1)
dino.add_task(task=task2)
spiky.add_task(task=task3)

owner1.set_availability(slots=[time1, time2, time3]) #should work since these are 30 and 15 min long 
owner2.set_availability(slots=[time4, time5]) #should only assign task for time4 since time5 is 10 min long 


def format_minutes(minutes: int) -> str:
    hour, minute = divmod(minutes, 60)
    period = "AM" if hour < 12 else "PM"
    display_hour = hour % 12 or 12
    return f"{display_hour}:{minute:02d} {period}"


def print_schedule(owner: PetOwner, scheduler: Scheduler) -> None:
    print(f"=== {owner.name}'s Schedule ===")
    scheduled_titles = set(scheduler.build_schedule())
    for task in scheduler.all_tasks():
        status = "scheduled" if task.title in scheduled_titles else "UNSCHEDULED"
        if task.slot is not None:
            time_range = f"{format_minutes(task.slot.start_minute)} - {format_minutes(task.slot.end_minute)}"
        else:
            time_range = "no time slot"
        pet_name = task.pet.name if task.pet is not None else "Unassigned"
        print(f"[{status:>11}] {task.title:<22} ({pet_name}, {task.priority.name}, {time_range})")

def print_updated_schedule(owner: PetOwner, tasks: list[Task]) -> None:
    print(f"=== {owner.name}'s Updated Schedule")

    for task in tasks:
        status = "scheduled" if task else "UNSCHEDULED"
        if task.slot is not None:
            time_range = f"{format_minutes(task.slot.start_minute)} - {format_minutes(task.slot.end_minute)}"
        else:
            time_range = "no time slot"
        pet_name = task.pet.name if task.pet is not None else "Unassigned"
        
        print(f"[{status:>11}] {task.title:<22} ({pet_name}, {task.priority.name}, {time_range})")

scheduler1.assign_task(task=task4, pet=coco)    

# print()
print_schedule(owner1, scheduler1)
# print()
# print_schedule(owner2, scheduler2)

# updated_schedule1 = scheduler1.mark_complete(task1, coco)

# print("\n", f"{owner1.name} has completed a task: {task1.title}. Below is her updated schedule")

# print()
# print()

# print_updated_schedule(owner1, updated_schedule1)

# coco_tasks = scheduler1.filter_by_pet_name(coco)
# scheduler1_tasks = scheduler1.all_tasks()
# result = []
# for task in scheduler1_tasks:
#     result.append(task.title)


# print(result)