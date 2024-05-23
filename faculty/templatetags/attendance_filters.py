from django import template

register = template.Library()

@register.filter(name='get_status')
def get_status(attendance_list, student_id):
    for attendance in attendance_list:
        if attendance.student.id == student_id:
            return attendance.status
    return False



@register.filter
def get_item(list, index):
    try:
        return list[index]
    except IndexError:
        return None

@register.filter
def is_selected(schedule_list, day, time):
    for schedule in schedule_list:
        if schedule.day == day.id and schedule.time == time.id and schedule.subject is not None:
            return True
    return False


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


