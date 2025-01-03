# **rating_platform_tests**

## Описание проекта
**rating_platform** — это система для оценки студентами преподавателей и учебных заведений.  
Тестирование построено на **Selenium**.

---

## Стек технологий
- **Selenium 4**

---

## Prerequisites (Предварительные требования)
1. Вы должны запустить локально или использовать хостинг для запуска проекта **rating_platform**.

Подробнее:
https://github.com/NikitaMelnikovq/rating_platform_backend/

https://github.com/acuraels/Student-voice-Front-end

2. В проекте должны быть созданы по одному профилю преподавателя и администратора.
Рекомендации:
```bash
python
from institute.models import Institute
institute = Institute.objects.create(id=77, name='ИРИТ-РТФ')
institute.save()

user = User.objects.create(username='admin', password='admin', role='admin', first_name='Админ', surname='Админов', last_name='Админович', institute_id=77)
user.set_password('admin')
user.save()

user = User.objects.create(username='teacher', password='teacher', role='teacher', first_name='Преподавательский', surname='Преподаватель', institute_id=77)
user.set_password('teacher')
user.save()
```

3. В этом проекте должен быть создан файл ".env" со следующими переменными.
```bash
URL='...'
USERNAME_ADMIN=admin
PASSWORD_ADMIN=admin
USERNAME_TEACHER=teacher
PASSWORD_TEACHER=teacher
TEXT_DISCIPLINE='...'
```
4. Активируйте виртуальное окружение, установите связи.

5. Рекомендуемый порядок запуска тестов:

```bash
pytest AuthorizationAdministrator.py
pytest CreateUser.py
pytest EditUser.py
pytest CreateDeleteDiscipline.py
pytest SearchDiscipline.py
pytest CreateLesson.py
pytest GenerateQRcode.py
pytest EditLesson.py
pytest SeachLesson.py
pytest FeedbackForm.py
pytest LessonStatistic.py
pytest Rating.py
pytest RatingReportComment.py
pytest RatingExcelDownload.py
pytest TeacherStatistic.py
```