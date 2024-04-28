import csv
import sys
from tabulate import tabulate
from datetime import datetime


def create(file_path):
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        function_stats = {}

        for row in csv_reader:
            function_name = row['function_name']
            timestamp = datetime.strptime(row['timestamp'], '%Y-%m-%d %H:%M:%S.%f').timestamp() * 1000

            if function_name not in function_stats:
                function_stats[function_name] = {'Num. of calls': 0, 'Total Time (ms)': 0}

            if row['event'] == 'start':
                function_stats[function_name]['Num. of calls'] += 1
                function_stats[function_name]['start_time'] = timestamp
            elif row['event'] == 'stop':
                start_time = function_stats[function_name]['start_time']
                elapsed_time = timestamp - start_time
                function_stats[function_name]['Total Time (ms)'] += elapsed_time

        result = []
        headers = ["Function Name", "Num. of calls", "Total Time (ms)", "Average Time (ms)"]

        for function_name, stats in function_stats.items():
            num_calls = stats['Num. of calls']
            total_time = stats['Total Time (ms)']
            average_time = total_time / num_calls  if num_calls > 0 else 0

            result.append([function_name, num_calls, total_time, average_time])

    result_table = tabulate(result, headers, tablefmt="github")
    return result_table

if __name__ == "__main__":
    # Use: python3 reporting.py trace_file.log
    assert len(sys.argv) == 2, "Usage: python3 reporting.py trace_file.log"
    print(create(sys.argv[1]))