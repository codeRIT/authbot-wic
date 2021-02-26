from auth_user import AuthUser
from bottle import Bottle, request, run, static_file, template
from oauthlib.oauth2.rfc6749.errors import InvalidGrantError

import config

app = Bottle()
callback_func = None


@app.route('/callback')
def callback():
    try:
        user_id: str = request.params["state"]
        user: AuthUser
        if user_id == "server":
            user = AuthUser.server_user()
        else:
            user = AuthUser.from_id(user_id)

        print("USER: " + str(user))
        user.get_access_token(request.params["code"])
        callback_func(user)

        return template("success")
    # except AttributeError:  # user hasn't started the auth flow yet
        # return template("failure", reason="Authorization flow hasn't begun yet.")
    except InvalidGrantError:  # user is re-using an access code
        return template("failure", reason="Invalid authorization grant.")
    except KeyError:  # query parameters missing
        return template("failure", reason="Parameters missing")


@app.route("/static/<filename:path>")
def static(filename: str):
    return static_file(filename, root="static")


def run_server(event_loop, callback):
    def cb(user):
        event_loop.call_soon_threadsafe(callback, user)

    global callback_func
    callback_func = cb

    print("bottle server running!")
    run(app, host=config.HOST, port=int(config.PORT))
