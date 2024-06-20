#!/usr/bin/python3
"""A script for parsing HTTP request logs."""
import re
import sys


def extract_input(input_line):
    """Extracts sections of a line of an HTTP request log."""
    log_fmt = r'^\s*(\S+)\s* - \[(\d{2}/\w+/\d{4}:\d{2}:\d{2}:\d{2} \+\d{4})\] "GET /projects/260 HTTP/1.1" (\d{3}) (\d+)'
    match = re.match(log_fmt, input_line)
    if match:
        return {
            'status_code': match.group(3),
            'file_size': int(match.group(4))
        }
    return None


def print_statistics(total_file_size, status_codes_stats):
    """Prints the accumulated statistics of the HTTP request log."""
    print(f"File size: {total_file_size}", flush=True)
    for status_code in sorted(status_codes_stats.keys()):
        if status_codes_stats[status_code] > 0:
            print(f"{status_code}: {status_codes_stats[status_code]}", flush=True)


def update_metrics(line, total_file_size, status_codes_stats):
    """Updates the metrics from a given HTTP request log."""
    line_info = extract_input(line)
    if line_info:
        status_code = line_info['status_code']
        if status_code in status_codes_stats:
            status_codes_stats[status_code] += 1
        total_file_size += line_info['file_size']
    return total_file_size


def run():
    """Starts the log parser."""
    line_num = 0
    total_file_size = 0
    status_codes_stats = {str(code): 0 for code in [200, 301, 400, 401, 403, 404, 405, 500]}

    try:
        while True:
            line = sys.stdin.readline()
            if not line:
                break
            total_file_size = update_metrics(line, total_file_size, status_codes_stats)
            line_num += 1
            if line_num % 10 == 0:
                print_statistics(total_file_size, status_codes_stats)
    except KeyboardInterrupt:
        print_statistics(total_file_size, status_codes_stats)
        raise
    print_statistics(total_file_size, status_codes_stats)


if __name__ == '__main__':
    run()
