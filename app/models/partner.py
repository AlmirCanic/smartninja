from google.appengine.ext import ndb


class Partner(ndb.Model):
    title = ndb.StringProperty()
    summary = ndb.StringProperty()
    website = ndb.StringProperty()
    country = ndb.StringProperty()
    logo = ndb.StringProperty()
    description = ndb.TextProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    deleted = ndb.BooleanProperty(default=False)
    partner_id = ndb.IntegerProperty()  # needed because structuredproperty in course doesnt have an id

    @property
    def get_id(self):
        return self.key.id()

    @classmethod
    def create(cls, title, summary, website, country, logo, description):
        partner = cls(title=title, summary=summary, website=website, description=description, country=country, logo=logo)
        partner.put()
        partner.partner_id = partner.get_id
        partner.put()
        return partner

    @classmethod
    def update(cls, partner, title, summary, website, country, logo, description):
        partner.title = title
        partner.summary = summary
        partner.website = website
        partner.country = country
        partner.logo = logo
        partner.description = description
        partner.put()
        return partner


class PartnerUserCourse(ndb.Model):
    user_id = ndb.IntegerProperty()
    user_name = ndb.StringProperty()
    user_email = ndb.StringProperty()
    course_id = ndb.IntegerProperty()
    course_title = ndb.StringProperty()
    course_city = ndb.StringProperty()
    course_start_date = ndb.DateProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    deleted = ndb.BooleanProperty(default=False)

    @property
    def get_id(self):
        return self.key.id()

    @classmethod
    def create(cls, user_id, user_name, user_email, course):
        puc = cls(user_id=user_id, user_name=user_name, user_email=user_email.lower(), course_id=course.get_id,
                  course_title=course.title, course_city=course.city, course_start_date=course.start_date)
        puc.put()
        return puc

    @classmethod
    def update(cls, puc, user_id, user_name, user_email, course):
        puc.user_id = user_id
        puc.user_name = user_name
        puc.user_email = user_email.lower()
        puc.course_id = course.get_id
        puc.course_title = course.title
        puc.course_city = course.city
        puc.course_start_date = course.start_date
        puc.put()
        return puc

    @classmethod
    def delete(cls, puc):
        puc.deleted = True
        puc.put()