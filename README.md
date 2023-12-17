# Process Monitor

The Process Monitor is a Python script designed to monitor specific processes running on your system. It tracks various metrics such as CPU usage, memory usage, and the number of open file descriptors over a specified duration.

## Requirements

- Python 3.x
- Libraries: `os`, `time`, `sys`, `csv`, `platform`, `psutil`

## Installation

Ensure you have Python 3.x installed on your system. To install the required libraries, run the following command:

python install_dependencies.py

## Usage

To use the Process Monitor script, follow these steps:

1. **Clone the Repository:** Download or clone this repository to your local machine.

2. **Run the Script:** Open a terminal or command prompt and navigate to the directory containing the `monitor_process.py` file.

3. **Execute the Script:** Run the script by entering the following command:

python monitor_process.py <process_name> <duration_seconds> [<sampling_interval_seconds>]

Replace `<process_name>` with the name of the process you want to monitor, `<duration_seconds>` with the duration (in seconds) for monitoring, and `<sampling_interval_seconds>` (optional) with the interval between each sampling (default is 5 seconds if not specified).

For example:

python monitor_process.py chrome 60 5

This command will monitor the 'chrome' process for 60 seconds with a sampling interval of 5 seconds.

4. **View Output:** The script generates a CSV file named `<process_name>.csv` in the 'output' directory, containing information about CPU usage, memory usage, and open file descriptors during the monitoring period.

## Output

The generated CSV file includes the following fields:

- Process Name
- PID (Process ID)
- CPU (%)
- CPU (AVG%)
- Memory (%)
- Memory (AVG%)
- Open File Descriptors

## Notes

- If the process terminates or becomes inaccessible due to permissions during monitoring, appropriate alerts will be displayed.
- Memory spike and increase alerts will be raised based on the observed behavior during the monitoring period.