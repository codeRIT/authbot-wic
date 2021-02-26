import asyncio

from auth_user import AuthUser
from typing import Dict, NoReturn
from discord import Role
from discord import File
from discord.channel import TextChannel
from discord.client import Client
from discord.utils import get
from discord.message import Message
from discord.reaction import Reaction
from discord.user import User
from discord.errors import HTTPException
from requests_oauthlib import OAuth2Session
from threading import Thread
import logging
import pprint
import os
import sys

import config
import messages
import callback_server


os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

client: Client = Client()

# I know this is bad and I am sorry
_register_message: Message
_setup_channel: TextChannel

oauth = OAuth2Session(
    config.CLIENT_ID,
    redirect_uri=config.REDIRECT_URI,
    scope=config.OAUTH_SCOPES
)


@client.event
async def on_ready() -> NoReturn:
    print("running now!")


@client.event
async def on_message(message: Message) -> NoReturn:
    if message.author == client.user:
        return

    channel: TextChannel = message.channel

    # send ADMIN user DM,
    # THEN send this message
    # on a different event trigger

    if message.content.startswith(config.PREFIX + "setup"):
        # Generate and send setup flow to whoever ran the command

        AuthUser.server_user(message.author)

        # Save channel so we can send the user-facing setup message after admin setup
        global _setup_channel
        _setup_channel = message.channel

        auth_url: str = AuthUser.server_user().start_auth_flow()
        await AuthUser.server_user().member.send(messages.setup_message(auth_url))

@client.event
async def on_reaction_add(reaction: Reaction, user: User):

    if _register_message is None:
        logging.error("User " + str(user) + " reacted to a non-setup message.")
        return

    # Ignore emoji reactions not on the setup message
    if _register_message != reaction.message:
        return

    if user == client.user:
        return

    # Generate the user's auth URL
    # TODO: rename to build_auth_url (same for server)
    auth_url: str = AuthUser(user).start_auth_flow()

    try:
        await user.send(messages.user_setup(user.display_name, auth_url))
    except HTTPException as exc:
        logging.error("HTTPException sending message to user " + str(user))
        logging.info("\t" + str(exc))

    logging.info("--------")
    logging.info("Sent message to " + str(user))
    logging.info("--------")


async def handle_auth(user: AuthUser):

    logging.info("Handle auth")

    # Don't attempt to auth someone setting up the server :)
    if user == AuthUser.server_user():
        # But DO send the user setup message now that the admin setup is complete
        logging.info("Server authed!")
        await send_register_message()
        return

    user_info: Dict = user.get_user_info()
    questionnaire: Dict = AuthUser.server_user().get_questionnaire(user_info["questionnaire_id"])

    pp = pprint.PrettyPrinter(width=120, compact=True, indent=4)
    logging.info("--------")


    # Check if user object (HM) exists
    if user_info is None:
        logging.error("user_info is None -- probably called /register before /setup")
        logging.info(user)
        logging.info("--------")
        return

    # Check if questionnaire exists
    if questionnaire is None or questionnaire.get("error") is not None:
        logging.error("bad: could not retrieve questionnaire")
        log_user(user)
        await user.member.send("bad: could not retrieve questionnaire")
        logging.info("--------")
        return

    # Log user and questionnaire params of interest
    log_user(user)
    logging.info("acc_status: " + str(questionnaire.get("acc_status")))
    logging.info("country: " + str(questionnaire.get("country")))

    # Questionnaire parsing
    if questionnaire["country"] is None:
        logging.error("bad: country not set")
        await user.member.send(messages.MISSING_INFORMATION)
    elif not questionnaire["all_agreements_accepted"]:
        logging.error("bad: agreements not accepted")
        await user.member.send(messages.MISSING_INFORMATION)
    else:
        if questionnaire["acc_status"] not in ["accepted", "rsvp_confirmed", "rsvp_denied"]:
            logging.error("bad: not accepted, status is " + questionnaire["acc_status"])
        else:
            await setup_user(user, user_info["first_name"] + " " + user_info["last_name"])
            logging.info("good")
            await set_role(user)
            AuthUser.server_user().check_in_user(user_info["questionnaire_id"])

        # will send the appropriate message for accepted/denied/waitlisted/etc.
        await user.member.send(messages.ACC_STATUS_MESSAGES[questionnaire["acc_status"]])

    logging.info("--------")



async def setup_user(user: AuthUser, name: str):
    await user.member.edit(nick=name)

async def send_register_message():

    logging.info("Sending setup message")

    if _setup_channel is None:
        logging.error("_setup_channel not defined")
        return

    # Send the WiCHacks image first
    await _setup_channel.send(file=File('./static/wichacks.jpg'))

    global _register_message
    _register_message = await _setup_channel.send(messages.REGISTER_MESSAGE)

    await _register_message.add_reaction(emoji="👩‍💻")  # :woman_technologist:

async def set_role(user: AuthUser):

    logging.info("--------")
    logging.info("setting role")

    role = get(user.member.guild.roles, name=config.REGISTRATION_ROLE)

    if role is None:
        logging.error("Registration role is not set for user:")
        log_user(user)
        logging.info(user.member)
        logging.info("--------")
        return

    logging.info("user roles: " + str(user.member.roles))
    logging.info("our role: " + str(role))

    if role in user.member.roles:
        logging.warning("Registration role is already set for user:")
        log_user(user)
        logging.info(user.member)
        logging.info("--------")
        return

    # Add role to user
    await user.member.add_roles(role)
    logging.info("Successfully added " + str(role) + " for member " + str(user.member))
    log_user(user)
    logging.info("--------")

def log_user(user: AuthUser):
    logging.info("first_name: " + user.get_user_info().get("first_name"))
    logging.info("last_name: " + user.get_user_info().get("last_name"))
    logging.info("email: " + user.get_user_info().get("email"))


def run_create_task_for_callback(user: AuthUser):
    asyncio.create_task(handle_auth(user))

if __name__ == "__main__":

    logging.getLogger().setLevel(logging.INFO)

    loop = asyncio.get_event_loop()

    server_thread: Thread = Thread(target=callback_server.run_server, args=(loop, run_create_task_for_callback), daemon=True)
    server_thread.start()

    try:
        loop.run_until_complete(client.start(config.AUTH_TOKEN))
    except KeyboardInterrupt:
        loop.run_until_complete(client.logout())
        # cancel all tasks lingering
    finally:
        loop.close()
        sys.exit(0)
