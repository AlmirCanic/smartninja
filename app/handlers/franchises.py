from app.handlers.base import Handler
from app.models.franchise import Franchise
from app.utils.decorators import admin_required


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
        street = self.request.get("street")
        city = self.request.get("city")
        zip = self.request.get("zip")
        country = self.request.get("country")
        website = self.request.get("website")
        tax_number = self.request.get("tax-number")

        Franchise.create(title=title, street=street, city=city, zip=zip, country=country, website=website,
                         tax_number=tax_number)

        self.redirect_to("admin-franchise-list")