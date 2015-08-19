from google.appengine.ext import ndb
from app.models.franchise import FranchiseList


class InstructorCurriculum(ndb.Model):
    """Sub-model intended only for use in Instructor.curriculums field"""
    curriculum_title = ndb.StringProperty()
    curriculum_id = ndb.IntegerProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)


class Instructor(ndb.Model):
    full_name = ndb.StringProperty()
    user_id = ndb.IntegerProperty()
    email = ndb.StringProperty()
    franchises = ndb.StructuredProperty(modelclass=FranchiseList, repeated=True)
    curriculums = ndb.StructuredProperty(modelclass=InstructorCurriculum, repeated=True)
    city = ndb.StringProperty()
    manager_notes = ndb.TextProperty()
    manager_grade = ndb.IntegerProperty()  # manager grades instructor about these exact job requirements
    skills = ndb.StringProperty(repeated=True)  # programming skills that instructor has (e.g.: PHP, Python, SQL, ...)
    active = ndb.BooleanProperty(default=False)
    created = ndb.DateTimeProperty(auto_now_add=True)
    deleted = ndb.BooleanProperty(default=False)

    @property
    def get_id(self):
        return self.key.id()

    @classmethod
    def create(cls, full_name, user_id, email, franchises, city=None):
        instructor = cls(full_name=full_name, user_id=user_id, email=email.lower(), franchises=franchises, city=city)
        instructor.put()
        return instructor

    @classmethod
    def update(cls, instructor, email, city):
        instructor.email = email.lower()
        instructor.city = city
        instructor.put()
        return instructor

    @classmethod
    def add_or_create(cls, full_name, user_id, email, franchises, city=None):
        instructor = cls.query(Instructor.email == email.lower()).get()

        if instructor:
            if instructor.deleted:
                instructor.deleted = False
                instructor.put()

            existing_franchises = instructor.franchises
            if franchises[0] not in existing_franchises:
                existing_franchises.append(franchises[0])
                instructor.franchises = existing_franchises
                if not instructor.city:
                    instructor.city = city
                instructor.put()
        else:
            instructor = cls.create(full_name=full_name, email=email.lower(), user_id=user_id, franchises=franchises, city=city)

        return instructor

    @classmethod
    def add_curriculum(cls, instructor, curriculum_id, curriculum_title):
        curriculum_exists = False

        for curr in instructor.curriculums:
            if curr.curriculum_id == int(curriculum_id):
                curriculum_exists = True

        if not curriculum_exists:
            instructor_curriculum = InstructorCurriculum(curriculum_title=curriculum_title, curriculum_id=int(curriculum_id))
            instructor.curriculums.append(instructor_curriculum)
            instructor.put()
            return True
        else:
            return False

    @classmethod
    def remove_curriculum(cls, instructor, curriculum_id):
        for curr in instructor.curriculums:
            if curr.curriculum_id == curriculum_id:
                instructor.curriculums.remove(curr)
                instructor.put()
                break

        return True