-- 5 комнат с самой большой разницей в возрасте студентов
select rooms.name
from rooms
    join students on students.room = rooms.id
group by rooms.id
order by max(age(students.birthday)) - min(age(students.birthday)) desc
limit 5;