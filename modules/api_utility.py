from rich.progress import Progress
from threading import Thread
import time

def api_call() -> None:

    """Calls flask-api (not coded) to fetch the required information from Caesar's Sportsbook."""

    time.sleep(1)

def progress_bar(load_time_seconds: int) -> None:

    """Displays the progress bar for fetching the data with the flask-api. The bar doesn't move in response to api call, but is rather an estimate of how long it would nornamlly take."""

    load_time = load_time_seconds / 100
    
    with Progress() as progress:
        
        push_progress = progress.add_task("Loading Bets :moneybag:")

        for _ in range(100):
            progress.update(push_progress, advance = 1)
            time.sleep(load_time)

def await_api_call(load_time_seconds: int = 1) -> None:

    """Api call wrapper that shows progress bar whilst simultaneously fetching the data with the flask-api."""

    Thread(target = api_call, args = ()).start()
    progress_bar(load_time_seconds)