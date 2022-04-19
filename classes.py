class User:
    def __init__(self, user_name, password):
        self.username = user_name
        self.password = password
        self.my_courses = list()
        self.subscribe_courses = list()

    def create_course(self, name):
        self.my_courses.append(Course(name, self))


class Course:
    def __init__(self, name, owner: User):
        self.name = name
        self.owner = owner
        self.tacks = list()


class Task:
    def __init__(self, name, parent_course: Course):
        self.name = name
        self.parent_course = parent_course


a = User("dema_stat", "qwertyasdf228666")
a.create_course("Прога на питоне")
for i in a.my_courses:
    print(i.name, i.owner.username)

