from mods import mod_info

from timetable_schedule import run_script
from optimizer import save_timetables

if __name__ == "__main__":
    mod_info()
    save_timetables()
    run_script()