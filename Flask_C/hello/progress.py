import pypyodbc


class Lookup:
    def __init__(self, items):
        self.items = items

    def __iter__(self):
        for item in self.items:
            yield (item)


connection = pypyodbc.connect('Driver={SQL Server}; Server=LAPTOP-RUUC0E0L; Database=Users; trusted_connection=yes')
cursor = connection.cursor()

select1 = ("SELECT candidatename,candidatename "
           "FROM candidatedel ")

cursor.execute(select1)
result1 = cursor.fetchall()

result2 = [('Non', '--Select--'),
           ('Round1', 'Round 1'),
           ('Round2', 'Round 2'),
           ('Round3', 'Round 3'),
           ('Round4', 'Round 4'),
           ('HR', 'HR'),
           ('Offer', 'Offer'),
           ('Joined', 'Joined')]

result3 = [('1', '--Select--'),
           ('Scheduled', 'Scheduled'),
           ('Selected', 'Selected'),
           ('Rejected', 'Rejected'),
           ('On Hold', 'On Hold'),
           ('Offer Rolled out', 'Offer Rolled out'),
           ('Offer Accepted', 'Offer Accepted'),
           ('Offer Declined', 'Offer Declined')]

choices = [('Skills', 'Skills'),
           ('Job ID', 'Job ID'),
           ('Notice Period', 'Notice Period'),
           ('Status', 'Status')]

select2 = ("SELECT distinct skill,skill "
           "FROM candidatedel")

cursor.execute(select2)
result4 = cursor.fetchall()
skill = [("%", '--Select--')]
skill.extend(result4)

select3 = ("SELECT job_id,job_id "
           "FROM candidatedel")

cursor.execute(select3)
result5 = cursor.fetchall()
job = [("%", '--Select--')]
job.extend(result5)

