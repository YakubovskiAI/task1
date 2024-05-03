-- Список комнат где живут разнополые студенты
select rooms.name
from rooms
    join students on students.room = rooms.id
group by rooms.id
having count(distinct students.sex) = 2;