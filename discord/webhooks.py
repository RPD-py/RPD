# -*- coding: utf-8 -*-
# cython: language_level=3
# Copyright (c) 2021-present VincentRPS

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE
"""Implementation of Discord Webhooks."""

import typing

from .api.rest import RESTClient, Route
from .embed import Embed
from .file import *
from .snowflake import Snowflakeish

__all__: typing.List[str] = ["Webhook"]


class Webhook:
    """The base class for interperting Webhooks

    .. versionadded:: 0.3.0

    Parameters
    ----------
    id
        The webhook id
    token
        The webhook token

    Attributes
    ----------
    rest
        An instance of RESTClient.
    """

    def __init__(self, webhook_id, webhook_token):
        self.id = webhook_id
        self.token = webhook_token
        self.rest = RESTClient()

    def fetch_webhook(self):
        """Fetch the current Webhook from the API."""
        return self.request("GET", f"/webhooks/{self.id}/{self.token}")

    def modify_webhook(
        self, name: typing.Optional[str] = None, avatar: typing.Optional[str] = None
    ):
        """Modify the Webhook

        Parameters
        ----------
        name
            Change the name
        avatar
            Change the avatar
        """
        json = {}
        if name:
            json["name"] = name
        if avatar:
            json["avatar"] = avatar
        return self.rest.send(
            Route(
                "PATCH",
                f"/webhooks/{self.id}/{self.token}",
                webhook_id=self.id,
                webhook_token=self.token,
            ),
            json=json,
        )

    def delete_webhook(self):
        """Deletes the Webhook"""
        return self.rest.send(
            Route(
                "DELETE",
                f"/webhooks/{self.id}/{self.token}",
                webhook_id=self.id,
                webhook_token=self.token,
            )
        )

    def fetch_message(self, message: Snowflakeish):
        """Fetches a Webhook message."""
        return self.rest.send(
            Route(
                "GET",
                f"/webhooks/{self.id}/{self.token}/messages/{message}",
                webhook_id=self.id,
                webhook_token=self.token,
            )
        )

    def edit_message(
        self,
        message: Snowflakeish,
        content: typing.Optional[str] = None,
        allowed_mentions: typing.Optional[bool] = None,
    ):
        """Edits a Webhook message

        Parameters
        ----------
        message
            The Message ID
        content
            Change the content
        allowed_mentions
            A allowed mentions object
        """
        json = {}
        if content:
            json["content"] = content
        elif allowed_mentions:
            json["allowed_mentions"] = allowed_mentions
        return self.rest.send(
            Route(
                "POST",
                f"/webhooks/{self.id}/{self.token}/messages/{message}",
                webhook_id=self.id,
                webhook_token=self.token,
            ),
            json=json,
        )

    def delete_message(
        self,
        message: Snowflakeish,
    ):
        """Deletes a message

        Parameters
        ----------
        message
            The message to delete
        """
        return self.rest.send(
            Route(
                "DELETE",
                f"/webhooks/{self.id}/{self.token}/messages/{message}",
                webhook_id=self.id,
                webhook_token=self.token,
            )
        )

    def execute(
        self,
        content: typing.Optional[str] = None,
        username: typing.Optional[str] = None,
        avatar_url: typing.Optional[str] = None,
        tts: typing.Optional[bool] = None,
        allowed_mentions: typing.Optional[bool] = None,
        embed: typing.Optional[Embed] = None,
        embeds: typing.Optional[typing.List[Embed]] = None,
        flags: typing.Optional[typing.Any] = None,
    ):
        """Execute the Webhook

        Parameters
        ----------
        content: :class:`str`
            The content to send.
        username: :class:`str`
            The username the Webhook should have
        avatar_url: :class:`str`
            The avatar the Webhook should have
        tts: :class:`bool`
            If the message should have tts enabled
        allowed_mentions
            A allowed mentions object
        """
        json = {}
        if content:
            json["content"] = content
        if username:
            json["username"] = username
        if avatar_url:
            json["avatar_url"] = avatar_url
        if tts:
            json["tts"] = tts
        if allowed_mentions:
            json["allowed_mentions"] = allowed_mentions
        if embed:
            if isinstance(embed, Embed):
                emb = [embed.obj]
            else:
                emb = [embed]
        if embeds:
            if isinstance(embeds, Embed):
                emb = [embed.obj for embed in embeds]
            else:
                emb = embeds
        if embed or embeds:
            json["embeds"] = emb

        if flags:
            json["flags"] = flags

        return self.rest.send(
            Route(
                "POST",
                f"/webhooks/{self.id}/{self.token}",
                webhook_id=self.id,
                webhook_token=self.token,
            ),
            json=json,
        )
