-- 5 комнат, где самый маленький средний возраст студентов
select rooms.name
from rooms
    join students on students.room = rooms.id
group by rooms.id
order by avg(age(students.birthday))
limit 5