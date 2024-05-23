-- Список комнат и количество студентов в каждой из них
select rooms.name, count(students.id) as students_amount
from rooms
    join students on students.room = rooms.id
group by rooms.id
order by rooms.id;