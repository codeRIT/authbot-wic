import inspect
from typing import Dict
import config


REGISTER_MESSAGE: str = inspect.cleandoc("""*Welcome to WiCHacks!*

    *To Check-In*: Before you access our Discord server, we’ll need to verify your account. Please click the emoji below to get started

    *Notes:*
    *Please make sure that you have a country on your WiCHacks application
    *Please allow “Allow direct message from server members" to get a message from our bot

    If you are a volunteer or mentor, please message in #check-in-desk for assisstance """)

def setup_message(url: str):
    return f"Click this link to setup authbot-py: {url}"

def user_setup(name: str, auth_url: str) -> str:
    return inspect.cleandoc(f"""Hi {name}! Welcome to WiCHacks. There's a few things I need to have you do in order to check you in.
    First, open the following link to connect your WiCHacks registration to your Discord: {auth_url}
    """)


PENDING = inspect.cleandoc("""Uh oh, it looks like you haven't received an acceptance to WiCHacks.
        If you do receive an acceptance just react with a :bricks: in WiCHacks's Discord server and I can get you set up!""")

ACCEPTED = RSVP_CONFIRMED = inspect.cleandoc("Awesome, you're all set to join! I've given you access to the channels and reformatted your name to match the event requirements.")

WAITLIST = LATE_WAITLIST = inspect.cleandoc("""Hang tight, it looks like you haven't received an acceptance to WiCHacks and you're on the waitlist.
        If you do receive an acceptance just react with a :bricks: in WiCHacks's Discord server and I can get you set up!""")

DENIED = inspect.cleandoc("""Uh oh, it looks like you haven't received an acceptance to WiCHacks. We were overjoyed with the number of applicants we received, but unfortunately we can not accept everyone due to capacity.
        We invite you to apply again next year. There are plenty of other hackathons this season, and it may not be too late to apply for those. Checkout https://mlh.io to find out more information.""")

RSVP_DENIED = inspect.cleandoc("""Uh oh, it looks like you told us you weren't coming. We've updated your RSVP to say you are here.
        You're all set to join! I've given you access to the channels and reformatted your name to match the event requirements.""")

MISSING_INFORMATION = inspect.cleandoc(f"""Uh oh, it looks like you account is missing some information! Go here to the following link to fix the problem: {config.APPLY_URL}.
        Once done, come back and react with a :bricks: in WiCHacks's Discord server and I can get you set up!""")


ACC_STATUS_MESSAGES: Dict[str, str] = {
    "pending": PENDING,
    "accepted": ACCEPTED,
    "rsvp_confirmed": RSVP_CONFIRMED,
    "waitlist": WAITLIST,
    "late_waitlist": LATE_WAITLIST,
    "denied": DENIED,
    "rsvp_denied": RSVP_DENIED
}
