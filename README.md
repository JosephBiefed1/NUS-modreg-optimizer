# NUS-modreg-optimizer
# University Timetable Scheduling Optimization

## Project Description
This project aims to optimize university timetable scheduling using a genetic algorithm. The goal is to prioritize back-to-back schedules and select e-learning lectures to minimize the number of days students need to attend in-person classes. The project reads timetable data from a JSON file and visualizes the resulting optimized schedule.

## Features
- **Genetic Algorithm**: Utilizes a genetic algorithm to find the optimal timetable.
- **Back-to-Back Scheduling**: Prioritizes back-to-back classes to reduce gaps between lectures.
- **E-Learning Selection**: Selects e-learning lectures to minimize the number of days with in-person classes.
- **Visualization**: Provides a visual representation of the optimized timetable.

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/university-timetable-optimization.git
    cd university-timetable-optimization
    ```

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage
1. Select your timetable according to the format in select_mods.txt.
2. Run the optimization script:
    ```bash
    python main.py
    ```
3. View the resulting optimized timetable.
