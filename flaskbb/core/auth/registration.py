# -*- coding: utf-8 -*-
"""
    flaskbb.core.auth.services
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    This modules provides services used in authentication and authorization
    across FlaskBB.

    :copyright: (c) 2014-2018 by the FlaskBB Team.
    :license: BSD, see LICENSE for more details.
"""

from abc import abstractmethod

import attr

from ..._compat import ABC


@attr.s(hash=True, cmp=False, repr=True, frozen=True)
class UserRegistrationInfo(object):
    """
    User registration object, contains all relevant information for validating
    and creating a new user.
    """
    username = attr.ib()
    password = attr.ib(repr=False)
    email = attr.ib()
    language = attr.ib()
    group = attr.ib()


class UserValidator(ABC):
    """
    Used to validate user registrations and stop the registration process
    by raising a :class:`~flaskbb.core.exceptions.ValidationError`.
    """

    @abstractmethod
    def validate(self, user_info):
        """
        This method is abstract.

        :param user_info: The provided registration information.
        :type user_info: :class:`~flaskbb.core.auth.registration.UserRegistrationInfo`
        """  # noqa

    def __call__(self, user_info):
        return self.validate(user_info)


class RegistrationFailureHandler(ABC):
    """
    Used to handle failures in the registration process.
    """

    @abstractmethod
    def handle_failure(self, user_info, failures):
        pass

    def __call__(self, user_info, failures):
        self.handle_failure(user_info, failures)


class RegistrationPostProcessor(ABC):
    """
    Used to post proccess successful registrations by the time this
    interface is called, the user has already been persisted into the
    database.
    """

    @abstractmethod
    def post_process(self, user):
        pass

    def __call__(self, user):
        self.post_process(user)


class UserRegistrationService(ABC):
    """
    Used to manage the registration process. A default implementation is
    provided however, this interface is provided in case alternative
    flows are needed.
    """

    @abstractmethod
    def register(self, user_info):
        """
        This method is abstract.

        :param user_info: The provided user registration information.
        :type user_info: :class:`~flaskbb.core.auth.registration.UserRegistrationInfo`
        """  # noqa
        pass
