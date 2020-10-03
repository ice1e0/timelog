""" Module to handle timelog files """

from datetime import datetime, timedelta
import sys
import re

from .colors import *
from .timelog import TimeLog


def parse_file(file: str, verbose: int, format: str):

    timelogs = []

    with open(file, 'r') as f:
        lines = f.readlines()

    current_date = None
    current_project = None
    current_timelog = None
    line_num = 0
    for full_line in lines:
        line_num += 1
        line = full_line[:-1]

        intent = 0
        pos = 0

        # count up for taps used at the beginning
        while pos < len(line) and line[pos] == '\t':
            intent += 1
            pos += 1

        if len(line) == pos:
            continue # empty line

        if verbose >= 3:
            sys.stdout.write(CYAN)
            print(line[pos:])
            sys.stdout.write(RESET)

        operator = None
        timelog_entry = None

        if line[pos] == '#':
            
            header_level = 0
            while pos < len(line) and line[pos] == '#':
                pos += 1
                header_level += 1

            if line[pos] != ' ':
                sys.stdout.write(RED)
                print(f'invalid char at line {line_num} pos {pos+1} "{line[pos]}", expected space')
                sys.stdout.write(RESET)

            project_name = line[pos:].strip()
            current_project = project_name

            if verbose >= 2:
                sys.stdout.write(GREEN)
                print(f'-- new project at header level {header_level}: {project_name}')                
                sys.stdout.write(RESET)
            continue # project line

        if re.search('[0-9]{4,4}-[0-9]{2,2}-[0-9]{2,2}', line):
            current_date = datetime.strptime(line, '%Y-%m-%d')
            current_timelog = None
            if verbose >= 2:
                sys.stdout.write(GREEN)
                print(f'-- current date changed: {current_date}')
                sys.stdout.write(RESET)
            continue

        if line[pos] == '-' or line[pos] == '+':
            operator = line[pos]
            pos += 1

            if not current_timelog:
                sys.stdout.write(RED)
                print(f'You can not use operator {operator} without preceeding timelog entry')
                sys.stdout.write(RESET)

        # try reading time or hour definition

        start_time = None
        end_time = None
        if re.search('[0-9]{2,2}:[0-9]{2,2}-[0-9]{2,2}:[0-9]{2,2}.*', line):
            start_time = datetime.strptime(line[pos:pos+4], '%H:%M')
            end_time   = datetime.strptime(line[pos+6:pos+11], '%H:%M')
            timelog_entry = TimeLog(
                date=current_date,
                from_time=start_time,
                to_time=end_time,
                project=current_project,
                text=line[pos+12:].strip()
            )
        else:
            number, pos = read_number(line, pos)
            if number:
                if line[pos] == 'm':
                    timelog_entry = TimeLog(
                        date=current_date,
                        duration_in_hours=number/60,
                        project=current_project,
                        text=line[pos+1:].strip()
                    )
                if line[pos] == 'h':
                    timelog_entry = TimeLog(
                        date=current_date,
                        duration_in_hours=number,
                        project=current_project,
                        text=line[pos+1:].strip()
                    )

        if timelog_entry:
            if operator:
                timelog_entry.is_negative = operator == '-'
                current_timelog.subitems.append(timelog_entry)

                if verbose >= 1:
                    sys.stdout.write(GREEN)
                    print(f'-- new supplement entry: {timelog_entry}')
                    sys.stdout.write(RESET)
            else:
                current_timelog = timelog_entry
                timelogs.append(current_timelog)

                if verbose >= 1:
                    sys.stdout.write(GREEN)
                    print(f'-- new entry: {current_timelog}')
                    sys.stdout.write(RESET)

            continue

        sys.stdout.write(RED)
        print(f'invalid line from part {line[pos:]}')
        sys.stdout.write(RESET)

    if format == 'csv':
        print('date,duration_in_hours,from_time,to_time,project,text')
        for time_log in timelogs:
            date_str      = time_log.date.strftime('%Y-%m-%d')
            from_time_str = time_log.from_time.strftime('%H:%M') if time_log.from_time else ''
            to_time_str   = time_log.to_time.strftime('%H:%M')   if time_log.from_time else ''
            print(f'{date_str},{time_log.duration_in_hours_total:.2f},{from_time_str},{to_time_str},"{time_log.project}","{time_log.text}"')
    else:
        for time_log in timelogs:
            print(time_log)

def read_number(str: str, pos: int):
    number_str = ''
    has_decimal_point = False

    while pos < len(str):
        if ord(str[pos]) >= ord('0') and ord(str[pos]) <= ord('9'):
            number_str += str[pos]
            pos += 1
            continue
        elif str[pos] == '.':
            number_str += str[pos]
            if has_decimal_point:
                raise Exception('Two decimal points in a number!!!')
            has_decimal_point = True
            pos += 1
            continue
        else:
            break

    if len(number_str) > 0:
        if has_decimal_point:
            return float(number_str), pos
        else:
            return int(number_str), pos
    return None, pos
