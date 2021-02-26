from __future__ import annotations
from typing import Dict
from requests_oauthlib import OAuth2Session
from uuid import uuid4
from discord import Member

import config


class AuthUser:
    _users: Dict[str, AuthUser] = dict()  # {user ID: AuthUser object}
    _server_user: AuthUser = None

    def __init__(self, member: Member, id=None):
        self.member = member

        if id is None:
            self.id: str = str(uuid4())
        else:
            self.id = id

        self.oauth_client: OAuth2Session = OAuth2Session(
            config.CLIENT_ID,
            redirect_uri=config.REDIRECT_URI,
            scope=config.OAUTH_SCOPES,
            auto_refresh_url=f"{config.AUTH_URL}/oauth/token",
            auto_refresh_kwargs={
                "client_id": config.CLIENT_ID,
                "client_secret": config.CLIENT_SECRET
            },
            token_updater=lambda t: print("refreshed token for user " + member.display_name)
        )

        self._users[self.id] = self

    @classmethod
    def from_id(cls, id: str) -> AuthUser:
        return cls._users.get(id)

    @classmethod
    def server_user(cls, member=None) -> AuthUser:
        if cls._server_user is None:
            cls._server_user = cls(member, "server")

        return cls._server_user

    def start_auth_flow(self) -> str:
        authorization_url, state = self.oauth_client.authorization_url(
            f"{config.AUTH_URL}/oauth/authorize",
            state=self.id
        )
        return authorization_url

    def get_access_token(self, code: str):
        self.oauth_client.fetch_token(
            f"{config.AUTH_URL}/oauth/token",
            code=code
        )

    def get_user_info(self) -> Dict:
        return self.oauth_client.get(f"{config.AUTH_URL}/user.json").json()

    def get_questionnaire(self, id: int) -> Dict:
        url: str = f"{config.AUTH_URL}/manage/questionnaires/{id}.json"
        return self.oauth_client.get(url).json()

    def check_in_user(self, id: int):
        url: str = f"{config.AUTH_URL}/manage/questionnaires/{id}/check_in.json"
        self.oauth_client.patch(url, params={"check_in": "true"})
