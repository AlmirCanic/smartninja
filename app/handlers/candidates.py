from app.handlers.base import Handler
from app.utils.decorators import employer_required


class EmployerCandidatesListHandler(Handler):
    @employer_required
    def get(self):
        return self.render_template("employer/candidates_list.html")