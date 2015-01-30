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


class AdminPartnerEditHandler(Handler):
    @admin_required
    def get(self, partner_id):
        partner = Partner.get_by_id(int(partner_id))
        params = {"partner": partner}
        self.render_template("admin/partner_edit.html", params)

    @admin_required
    def post(self, partner_id):
        title = self.request.get("title")
        country = self.request.get("country")
        website = self.request.get("website")
        logo = self.request.get("logo")
        summary = self.request.get("summary")
        description = self.request.get("description")

        partner = Partner.get_by_id(int(partner_id))

        Partner.update(partner=partner, title=title, country=country, website=website, logo=logo, summary=summary,
                       description=description)

        self.redirect_to("admin-partner-details", partner_id=partner_id)


# PUBLIC

class PublicPartnersHandler(Handler):
    def get(self):
        partners = Partner.query(Partner.deleted == False).fetch()
        params = {"partners": partners}
        self.render_template("public/partners.html", params=params)