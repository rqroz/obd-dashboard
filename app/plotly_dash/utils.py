"""
Utility module for common functions/logic.
"""
import dash_html_components as html

from app.database import DATABASE
from app.controllers.obd.session import SessionController
from app.utils.auth import AuthHandler

from app.plotly_dash.constants import Colors


def get_default_label(text):
    """
    Generates a simple label element.

    Args:
        - text (str): Text of the label.

    Returns:
        - (html.Label): Label component set with default text color and the informed text.
    """
    return html.Label(
        text,
        style={
            'color': Colors.TEXT,
            'padding': '1rem',
        },
    )


def get_session_controller(user=None):
    """
    Gets an instance of the SessionController based on <user>.
    If <user> is not informed, will resolve it from current request.

    Raises:
        - AuthHandlerException: If user is not informed and request is not authenticated.

    Args:
        - user (app.models.user.User): User instance.

    Returns:
        - (app.controllers.obd.session.SessionController): Instance of the SessionController.
    """
    if not user:
        user = AuthHandler.handle_auth_request()
    return SessionController(user_id=user.id, db_session=DATABASE.session)


def get_session_dropdown_options(user):
    """
    Generates a list of dicts mapping labels and values on each of the sessions for the current user.
    The list is supposed to be used as options for dropdowns generated by Dash.

    Args:
        - user (app.models.user.User): Current authenticated user.

    Returns:
        - (List[dict]): List of options.
    """
    session_controller = get_session_controller(user)
    return [
        {'label': session.date.strftime('%d/%m/%Y %H:%M'), 'value': session.id}
        for session
        in session_controller.get_all(fields=['id', 'date'])
    ]
