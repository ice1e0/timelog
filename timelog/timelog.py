from datetime import datetime, timedelta


class Task():
    """A task time is booked on"""

    def __init__(self, id: str, subject: str, description: str):
        self.id = id
        self.subject = subject
        self.description = description


class Project():
    """A project working is done for"""

    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name
        self.tasks = []

    def add_task(self, task: Task):
        self.tasks.append(task)


class LogType():
    WORK = 'work'
    MEETING = 'meet'


class TimeLog():
    """A time log entry"""

    def __init__(self, date: datetime.date, from_time: datetime.time = None,
                 to_time: datetime.time = None, duration_in_hours: int = None, project: str = None,
                 text: str = None, is_negative: bool = False, is_supplement: bool = False) -> None:
        if all(v is None for v in [from_time, to_time, duration_in_hours]):
            raise ValueError("You have to provide a from/to time (via from_time, to_time) or duration_in_hours")
        #if duration_in_hours is not None and all(v is not None for v in [from_time, to_time]):
            #raise ValueError("You can not provide a from/to time (via from_time, to_time) and a duration_in_hours at the same time")
            #this is still valid, you simply worked longer than 12AM
        if duration_in_hours is None and all(v is None for v in [from_time, to_time]):
            raise ValueError("You have to provide both, from_time and to_time")

        self.date = date
        self.from_time = from_time
        self.to_time = to_time
        if not duration_in_hours:
            if from_time == to_time:
                raise ValueError("You can not provide from_time and to_time with the same value, to_time must be greater then from_time")
            if to_time < from_time:
                to_time += timedelta(days=1)
                #raise ValueError("You can not provide a from_time which is greater then to_time")
            timespan = (to_time - from_time)
            self.duration_in_hours = timespan.total_seconds() / 60 / 60
        else:
            if duration_in_hours <= 0 and not is_supplement:
                raise ValueError("duration_in_hours must not be zero or negative")

            self.duration_in_hours = duration_in_hours

        self.project = project
        self.text = text
        self.is_negative = is_negative
        self.subitems = []

    @property
    def duration_in_hours_total(self):
        total = self.duration_in_hours
        for subitem in self.subitems:
            if subitem.is_negative:
                total -= subitem.duration_in_hours_total
            else:
                total += subitem.duration_in_hours_total
        return total

    def __str__(self):
        return_str = self.date.strftime('%Y-%m-%d')
        if self.from_time:
            return_str += " {}-{}".format(self.from_time.strftime('%H:%M'), self.to_time.strftime('%H:%M'))
        else:
            return_str += ' - no time -'
        return_str += ' ' + '{0:.2g}'.format(self.duration_in_hours) + 'h ' + self.project + ' -> ' + self.text

        for subitem in self.subitems:
            return_str += '\n\t'
            if subitem.is_negative:
                return_str += '- '
            else:
                return_str += '+ '
            return_str += str(subitem)

        return return_str
