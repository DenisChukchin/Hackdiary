import random
from datacenter.models import Schoolkid, Mark, Chastisement
from datacenter.models import Lesson, Commendation
from commendation_variations import COMMENDATIONS


def fix_marks(student):
    student_marks = Mark.objects.filter(schoolkid=student, points__in=[2, 3])
    return student_marks.update(points=random.randint(4, 5))


def remove_chastisements(student):
    student_behave = Chastisement.objects.filter(schoolkid=student)
    return student_behave.delete()


def create_commendation(student, lesson):
    which_lesson = Lesson.objects.filter(
        year_of_study=student.year_of_study,
        group_letter=student.group_letter,
        subject__title=lesson
    ).order_by("?").first()

    return Commendation.objects.create(
               text=random.choice(COMMENDATIONS),
               created=which_lesson.date,
               schoolkid=student,
               subject=which_lesson.subject,
               teacher=which_lesson.teacher
           )


def main():
    full_name = input("Введите ФИО: ")
    lesson = input("Введите название предмета: ")
    try:
        student = Schoolkid.objects.get(full_name__contains=full_name)
        fix_marks(student)
        remove_chastisements(student)
        create_commendation(student, lesson)
        return print("Красный диплом не за горами :-)")
    except Schoolkid.DoesNotExist:
        return print("Неправильно ввели ФИО ученика! "
                     "Проверьте формат ввода: Иванов Иван Иванович")
    except Schoolkid.MultipleObjectsReturned:
        return print("Таких в списке несколько! Уточните ФИО ученика! "
                     "Проверьте формат ввода: Иванов Иван Иванович")
    except AttributeError:
        return print("Проверь орфографию и формат ввода! "
                     "Название предмета нужно вводить "
                     "в таком виде: Физкультура")


if __name__ == "__main__":
    main()
