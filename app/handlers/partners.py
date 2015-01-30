from app.utils.decorators import admin_required
from app.handlers.base import Handler
from app.models.partner import Partner


class AdminPartnersListHandler(Handler):
    @admin_required
    def get(self):
        partners = Partner.query(Partner.deleted == False).fetch()
        params = {"partners": partners}
        self.render_template("admin/partners_list.html", params)


class AdminPartnerAddHandler(Handler):
    @admin_required
    def get(self):
        params = {}
        self.render_template("admin/partner_add.html", params)

    @admin_required
    def post(self):
        title = self.request.get("title")
        country = self.request.get("country")
        website = self.request.get("website")
        logo = self.request.get("logo")
        summary = self.request.get("summary")
        description = self.request.get("description")

        Partner.create(title=title, country=country, website=website, logo=logo, summary=summary, description=description)

        self.redirect_to("admin-partners-list")


class AdminPartnerDetailsHandler(Handler):
    @admin_required
    def get(self, partner_id):
        partner = Partner.get_by_id(int(partner_id))
        params = {"partner": partner}
        self.render_template("admin/partner_details.html", params)


class AdminPartnerDeleteHandler(Handler):
    @admin_required
    def get(self, partner_id):
        partner = Partner.get_by_id(int(partner_id))
        params = {"partner": partner}
        self.render_template("admin/partner_delete.html", params)

    @admin_required
    def post(self, partner_id):
        partner = Partner.get_by_id(int(partner_id))
        partner.deleted = True
        partner.put()
        self.redirect_to("admin-partners-list")
"""

class AdminUserEditHandler(Handler):
    @admin_required
    def get(self, user_id):
        user = User.get_by_id(int(user_id))
        params = {"this_user": user}
        self.render_template("admin/user_edit.html", params)

    @admin_required
    def post(self, user_id):
        user = User.get_by_id(int(user_id))
        first_name = self.request.get("first_name")
        last_name = self.request.get("last_name")
        address = self.request.get("address")
        summary = self.request.get("summary")
        photo_url = self.request.get("photo_url")
        phone_number = self.request.get("phone_number")
        instructor = bool(self.request.get("instructor"))
        User.update(user=user, first_name=first_name, last_name=last_name, address=address, phone_number=phone_number,
                    summary=summary, photo_url=photo_url, instructor=instructor)
        self.redirect_to("user-details", user_id=int(user_id))

"""