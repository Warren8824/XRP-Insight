# Scheduler

The scheduler module is responsible for running periodic tasks, specifically the data collection process.

## Key Components

- `job()`: The main job function that runs the data collection process.
- `run_scheduler()`: Sets up and runs the scheduler.

## Usage

The scheduler is set to run the data collection job every 15 minutes. To start the scheduler:

```python
from src.scheduler.tasks import run_scheduler

run_scheduler()
```

## Customization
To modify the schedule or add new jobs, edit the `run_scheduler()` function in `src/scheduler/tasks.py`.
