import os
import time
import sys
import csv
import platform
import psutil

class ProcessMonitor(object):
    def __init__(self, process_name, duration, interval=5):
        self.process_name = process_name
        self.duration = duration
        self.interval = interval

    def get_open_handles(self, proc):
        system = platform.system()

        if system == 'Windows':
            # Get handles for Windows
            return proc.num_handles()
        else:
            # Get file descriptors for Unix-like systems
            return proc.num_fds()

    def monitor_process(self):
        output_directory = os.path.join(os.getcwd(), "output")
        os.makedirs(output_directory, exist_ok=True)
        output_file = os.path.join(output_directory, f"{self.process_name}.csv")

        with open(output_file, 'a', newline='') as csvfile:
            fieldnames = ['Process Name', 'PID', 'CPU (%)', 'CPU (AVG%)', 'Memory (%)', 'Memory (AVG%)', 'Open File Descriptors']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Check if the file is empty and write the header if needed
            if csvfile.tell() == 0:
                writer.writeheader()

            end_time = time.time() + self.duration
            cpu_total = 0.0
            memory_total = 0.0
            total_samples = 0
            last_memory_usage = 0
            memory_increased_each_sample = True
            memory_spike_alert_level = 1.2
            memory_spike_happened = False
            succeded = True

            while time.time() < end_time:
                # Get all running processes
                try:
                    process_found = False
                    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                            if self.process_name.lower() in proc.info['name'].lower():
                                process_found = True
                                current_memory_usage = proc.info['memory_percent']
                                current_cpu_usage = proc.info['cpu_percent']
                                process_name = proc.info['name']
                                process_id = proc.info['pid']
                                cpu_total += current_cpu_usage
                                memory_total += current_memory_usage
                                total_samples += 1

                                if (total_samples > 1):
                                    if (last_memory_usage > current_memory_usage):
                                        memory_increased_each_sample = False
                                    if (current_memory_usage/last_memory_usage > memory_spike_alert_level):
                                        memory_spike_happened = True

                                last_memory_usage = current_memory_usage

                                writer.writerow({
                                    'Process Name': process_name,
                                    'PID': process_id,
                                    'CPU (%)': current_cpu_usage,
                                    'CPU (AVG%)': round(cpu_total / total_samples, 2),
                                    'Memory (%)': current_memory_usage,
                                    'Memory (AVG%)': round(memory_total / total_samples, 2),
                                    'Open File Descriptors': self.get_open_handles(proc)
                                })
                    if not process_found:
                        raise psutil.NoSuchProcess(pid=process_id, name=process_name)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    print('Process might have terminated or inaccessible due to permissions.')
                    succeded = False
                    break
                time.sleep(self.interval)

        if succeded:
            if memory_spike_happened:
                print('Alert: Memory spikes happened.')
            if memory_increased_each_sample:
                print('Alert: Memory increased per sample collected.')


if __name__ == "__main__":
    if len(sys.argv) < 4 or len(sys.argv) > 5:
        print("Usage: python monitor_process.py <process_name> <duration_seconds> [<sampling_interval_seconds>]")
        sys.exit(1)

    process_name = sys.argv[1]
    duration = int(sys.argv[2])
    interval = int(sys.argv[3]) if len(sys.argv) == 5 else 5

    monitor = ProcessMonitor(process_name, duration, interval)

    monitor.monitor_process()
