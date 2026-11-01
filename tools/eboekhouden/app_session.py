"""Shared App authentication/context reads using the existing bounded transport."""
import app_probe as core


class AppAuthentication:
    def __init__(self, transport):
        self.transport = transport
        self.secrets = []

    def login(self, login, expected_admin):
        response = self.transport.request("POST", "/api/v4/auth/login", {"username": login.username, "password": login.password})
        if not isinstance(response, dict) or response.get("twoFactorCodeRequired") is not False:
            raise core.app.Stop("APP_TWO_FACTOR_OR_LOGIN_FLOW_UNKNOWN")
        if response.get("loginOk") is not True or not isinstance(response.get("token"), str) or not response["token"]:
            raise core.app.Stop("APP_LOGIN_NOT_CONFIRMED")
        self.token = response["token"]
        self.secrets.extend((login.username, login.password, self.token))
        self.admin = self.admin_now()
        if self.admin[0] != expected_admin:
            raise core.app.Stop("APP_ADMINISTRATION_MISMATCH")

    def admin_now(self):
        return core.app.active_administration(self.transport.request("GET", "/api/v4/auth/userinfo", token=self.token))

    def require_same_admin(self):
        if self.admin_now() != self.admin:
            raise core.app.Stop("APP_ADMINISTRATION_CHANGED")

    def read_mutation(self, transport, number, day):
        return core.app.project_record(self.read_mutation_raw(transport, number, day), tuple(self.secrets))

    def read_mutation_raw(self, transport, number, day):
        # Each separately bounded before/after read gets the existing eight-call
        # filter transport; one read's cap cannot exhaust the other's budget.
        return core.read_filtered_one(transport, core.app.SessionReader(transport, self.token),
                                      self.token, number, day, self.admin)
