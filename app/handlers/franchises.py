from app.handlers.base import Handler
from app.models.franchise import Franchise
from app.utils.decorators import admin_required
from app.utils.other import logga


class AdminFranchiseListHandler(Handler):
    @admin_required
    def get(self):
        franchise_list = Franchise.query(Franchise.deleted == False).fetch()

        params = {"franchises": franchise_list}
        self.render_template("admin/franchise_list.html", params)


class AdminFranchiseAddHandler(Handler):
    @admin_required
    def get(self):
        self.render_template("admin/franchise_add.html")

    @admin_required
    def post(self):
        title = self.request.get("title")
        full_company_name = self.request.get("company")
        street = self.request.get("street")
        city = self.request.get("city")
        zip = self.request.get("zip")
        country = self.request.get("country")
        website = self.request.get("website")
        tax_number = self.request.get("tax-number")

        Franchise.create(title=title, full_company_name=full_company_name, street=street, city=city, zip=zip,
                         country=country, website=website, tax_number=tax_number)

        self.redirect_to("admin-franchise-list")


class AdminFranchiseDetailsHandler(Handler):
    @admin_required
    def get(self, franchise_id):
        franchise = Franchise.get_by_id(int(franchise_id))
        params = {"franchise": franchise}
        self.render_template("admin/franchise_details.html", params)


class AdminFranchiseEditHandler(Handler):
    @admin_required
    def get(self, franchise_id):
        franchise = Franchise.get_by_id(int(franchise_id))
        params = {"franchise": franchise}
        self.render_template("admin/franchise_edit.html", params)

    @admin_required
    def post(self, franchise_id):
        franchise = Franchise.get_by_id(int(franchise_id))

        title = self.request.get("title")
        full_company_name = self.request.get("company")
        street = self.request.get("street")
        city = self.request.get("city")
        zip = self.request.get("zip")
        country = self.request.get("country")
        website = self.request.get("website")
        tax_number = self.request.get("tax-number")

        Franchise.update(franchise=franchise, title=title, full_company_name=full_company_name, street=street,
                         city=city, zip=zip, country=country, website=website, tax_number=tax_number)

        self.redirect_to("admin-franchise-details", franchise_id=franchise_id)


class AdminFranchiseDeleteHandler(Handler):
    @admin_required
    def get(self, franchise_id):
        franchise = Franchise.get_by_id(int(franchise_id))
        params = {"franchise": franchise}
        self.render_template("admin/franchise_delete.html", params)

    @admin_required
    def post(self, franchise_id):
        franchise = Franchise.get_by_id(int(franchise_id))
        franchise.deleted = True
        franchise.put()
        logga("Franchise %s deleted." % franchise_id)
        self.redirect_to("admin-franchise-list")