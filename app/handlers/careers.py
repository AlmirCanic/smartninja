from google.appengine.api import memcache
from app.handlers.base import Handler
from app.utils.decorators import manager_required


class ManagerCareersDetailsHandler(Handler):
    """TEMPORARY: Remove this handler when loacl websites are ready"""
    @manager_required
    def get(self):
        forms_id = memcache.get(key="forms-id")
        height = memcache.get(key="forms-height")
        text = memcache.get(key="forms-text")

        params = {"form_id": forms_id, "height": height, "text": text}

        return self.render_template("manager/careers_details.html", params)


class ManagerCareersEditHandler(Handler):
    """TEMPORARY: Remove this handler when loacl websites are ready"""
    @manager_required
    def post(self):
        forms_id = self.request.get("forms-id")
        height = self.request.get("site-height")
        text = self.request.get("text")

        memcache.set(key="forms-id", value=forms_id)
        memcache.set(key="forms-height", value=height)
        memcache.set(key="forms-text", value=text)

        return self.redirect_to("manager-careers-details")