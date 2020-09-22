from gd.abstract_entity import AbstractEntity
from gd.async_iter import async_iterable
from gd.async_utils import run_blocking
from gd.color import Color
from gd.datetime import datetime
from gd.enums import (
    CommentState,
    CommentStrategy,
    CommentType,
    FriendState,
    FriendRequestState,
    IconType,
    Role,
    MessageState,
)
from gd.filters import Filters
from gd.icon_factory import connect_images, factory, to_bytes
from gd.model import (  # type: ignore
    CommentUserModel,
    CreatorModel,
    LeaderboardUserModel,
    LevelLeaderboardUserModel,
    ListUserModel,
    ProfileUserModel,
    SearchUserModel,
)
from gd.text_utils import make_repr
from gd.typing import AsyncIterator, Iterable, Optional, Union, TYPE_CHECKING

if TYPE_CHECKING:
    import PIL.Image  # type: ignore  # noqa

    from gd.client import Client  # noqa
    from gd.comment import Comment  # noqa
    from gd.friend_request import FriendRequest  # noqa
    from gd.level import Level  # noqa
    from gd.message import Message  # noqa

__all__ = ("User",)

PAGES = range(10)
CONCURRENT = True


class User(AbstractEntity):
    def __repr__(self) -> str:
        info = {"name": repr(self.name), "id": self.id, "account_id": self.account_id}
        return make_repr(self, info)

    def __str__(self) -> str:
        return str(self.name)

    @classmethod
    def from_model(
        cls,
        model: Union[
            CommentUserModel,
            CreatorModel,
            LeaderboardUserModel,
            LevelLeaderboardUserModel,
            ListUserModel,
            ProfileUserModel,
            SearchUserModel,
        ],
        *,
        client: Optional["Client"] = None,
    ) -> "User":
        return cls.from_dict(model.to_dict(), client=client)

    @property
    def icon_set(self) -> "User":
        return self  # for backwards compatibility

    @property
    def name(self) -> str:
        """:class:`str`: String representing name of the user."""
        return self.options.get("name", "")

    @property
    def account_id(self) -> int:
        """:class:`int`: Account ID of the user."""
        return self.options.get("account_id", 0)

    def is_registered(self) -> bool:
        """:class:`bool`: Indicates whether user is registered or not."""
        return self.id > 0 and self.account_id > 0

    @property
    def stars(self) -> int:
        """:class:`int`: Amount of stars the user has."""
        return self.options.get("stars", 0)

    @property
    def demons(self) -> int:
        """:class:`int`: Amount of demons the user has beaten."""
        return self.options.get("demons", 0)

    @property
    def cp(self) -> int:
        """:class:`int`: Amount of Creator Points the user has."""
        return self.options.get("cp", 0)

    @property
    def diamonds(self) -> int:
        """:class:`int`: Amount of diamonds the user has."""
        return self.options.get("diamonds", 0)

    @property
    def coins(self) -> int:
        """:class:`int`: Number of coins the user has."""
        return self.options.get("coins", 0)

    @property
    def user_coins(self) -> int:
        """:class:`int`: Amount of User Coins user has."""
        return self.options.get("user_coins", 0)

    def get_place(self) -> int:
        """:class:`int`: User's place in leaderboard. ``0`` if not set."""
        return self.options.get("place", 0)

    def set_place(self, place: int = 0) -> None:
        """Set the ``self.place`` to ``place`` argument."""
        self.options.update(place=place)

    place = property(get_place, set_place)

    def has_cp(self) -> bool:
        """:class:`bool`: Indicates if a user has Creator Points."""
        return self.cp > 0

    @property
    def role(self) -> Role:
        """:class:`.Role`: A status level of the user."""
        return Role.from_value(self.options.get("role", 0))

    @property
    def rank(self) -> Optional[int]:
        """Optional[:class:`int`]: A global rank of the user.
        ``None`` if the user is not on the leaderboard.
        """
        return self.options.get("global_rank")

    @property
    def youtube(self) -> str:
        """:class:`str`: A youtube name of the user."""
        return self.options.get("youtube", "")

    @property
    def youtube_link(self) -> str:
        """:class:`str`: A link to the user's youtube channel."""
        return f"https://youtube.com/channel/{self.youtube}"

    @property
    def twitter(self) -> str:
        """:class:`str`: A twitter name of the user."""
        return self.options.get("twitter", "")

    @property
    def twitter_link(self) -> str:
        """:class:`str`: A link to the user's twitter page."""
        return f"https://twitter.com/{self.twitter}"

    @property
    def twitch(self) -> str:
        """:class:`str`: A twitch name of the user."""
        return self.options.get("twitch", "")

    @property
    def twitch_link(self) -> str:
        """:class:`str`: A link to the user's twitch channel."""
        return f"https://twitch.tv/{self.twitch}"

    @property
    def message_state(self) -> MessageState:
        """:class:`.MessageState`: A type indicating user's message inbox state."""
        return MessageState.from_value(self.options.get("message_state", 0))

    @property
    def friend_request_state(self) -> FriendRequestState:
        """:class:`.FriendRequestState`: A type indicating user's friend requests state."""
        return FriendRequestState.from_value(self.options.get("friend_request_state", 0))

    @property
    def comment_state(self) -> CommentState:
        """:class:`.CommentState`: A type indicating user's comment history policy."""
        return CommentState.from_value(self.options.get("comment_state", 0))

    @property
    def friend_state(self) -> FriendState:
        """:class:`.FriendState`: A type indicating relation between client and user."""
        return FriendState.from_value(self.options.get("friend_state", 0))

    def is_mod(self, role: Optional[Union[int, str, Role]] = None) -> bool:
        """:class:`bool`: Indicates if a user is Geometry Dash (Elder) Moderator.
        For instance, *RobTop* is an Elder Moderator, that means:
        ``robtop.is_mod() -> True`` and ``robtop.is_mod("elder_moderator") -> True``.
        """
        if self.role is None:  # pragma: no cover
            return False

        if role is None:
            return self.role is not Role.USER

        return self.role >= Role.from_value(role)

    @property
    def record_percent(self) -> int:
        return self.options.get("record_percent", -1)

    @property
    def recorded_at(self) -> Optional[datetime]:
        return self.options.get("recorded_at")

    @property
    def icon_type(self) -> IconType:
        return IconType.from_value(self.options.get("icon_type", 0))

    @property
    def icon(self) -> int:
        """:class:`int`: ID of user's icon."""
        return self.options.get("icon_id", 0)

    @property
    def cube(self) -> int:
        """:class:`int`: ID of user's cube."""
        return self.options.get("cube_id", 0)

    @property
    def ship(self) -> int:
        """:class:`int`: ID of user's ship."""
        return self.options.get("ship_id", 0)

    @property
    def ball(self) -> int:
        """:class:`int`: ID of user's ball."""
        return self.options.get("ball_id", 0)

    @property
    def ufo(self) -> int:
        """:class:`int`: ID of user's UFO."""
        return self.options.get("ufo_id", 0)

    @property
    def wave(self) -> int:
        """:class:`int`: ID of user's wave."""
        return self.options.get("wave_id", 0)

    @property
    def robot(self) -> int:
        """:class:`int`: ID of user's robot."""
        return self.options.get("robot_id", 0)

    @property
    def spider(self) -> int:
        """:class:`int`: ID of user's spider."""
        return self.options.get("spider_id", 0)

    @property
    def death_effect(self) -> int:
        """:class:`int`: ID of user's death effect."""
        return self.options.get("death_effect_id", 0)

    @property
    def color_1_id(self) -> int:
        return self.options.get("color_1_id", 0)

    @property
    def color_2_id(self) -> int:
        return self.options.get("color_2_id", 3)

    @property
    def color_1(self) -> Color:
        return Color.with_id(self.color_1_id)

    @property
    def color_2(self) -> Color:
        return Color.with_id(self.color_2_id)

    def has_glow(self) -> bool:
        return bool(self.options.get("has_glow"))

    has_glow_outline = has_glow

    def get_id_by_type(self, icon_type: Union[int, str, IconType]) -> int:
        return getattr(self, IconType.from_value(icon_type).name.lower())

    async def get_user(self) -> "User":
        return await self.client.get_user(self.account_id)

    async def update(self) -> None:
        new = await self.get_user()
        self.options.update(new.options)

    async def send(
        self, subject: Optional[str] = None, body: Optional[str] = None
    ) -> Optional["Message"]:
        """Send the message to ``self``. Requires logged client.

        Parameters
        ----------
        subject: :class:`str`
            The subject of the message.

        body: :class:`str`
            The body of the message.

        Raises
        ------
        :exc:`.MissingAccess`
            Failed to send a message.

        Returns
        -------
        Optional[:class:`.Message`]
            Sent message.
        """
        return await self.client.send_message(self, subject, body)

    async def block(self) -> None:
        """Block a user. Requires logged in client.

        Raises
        ------
        :exc:`.MissingAccess`
            Failed to block a user.
        """
        await self.client.block(self)

    async def unblock(self) -> None:
        """Unblock a user. Requires logged in client.

        Raises
        ------
        :exc:`.MissingAccess`
            Failed to unblock a user.
        """
        await self.client.unblock(self)

    async def unfriend(self) -> None:
        """Try to unfriend a user. Requires logged in client.

        Raises
        ------
        :exc:`.MissingAccess`
            Failed to unfriend a user.
        """
        await self.client.unfriend(self)

    async def send_friend_request(self, message: Optional[str] = None) -> Optional["FriendRequest"]:
        """Send a friend request to a user.

        .. note::

            This function does not raise any error if request was already sent.

        Parameters
        ----------
        message: Optional[:class:`str`]
            A message to attach to a request.

        Raises
        ------
        :exc:`.MissingAccess`
            Failed to send a friend request to user.

        Returns
        -------
        Optional[:class:`.FriendRequest`]
            Sent friend request.
        """
        return await self.client.send_friend_request(self, message)

    @async_iterable
    def get_levels_on_page(self, page: int = 0) -> AsyncIterator["Level"]:
        """Fetches user's levels on a given page.

        Parameters
        ----------
        page: :class:`int`
            Page to look for levels at.

        Returns
        -------
        AsyncIterator[:class:`.Level`]
            All levels found.
        """
        return self.client.search_levels_on_page(page=page, filters=Filters.by_user(), user=self)

    @async_iterable
    def get_levels(
        self, pages: Iterable[int] = PAGES, concurrent: bool = CONCURRENT
    ) -> AsyncIterator["Level"]:
        """Gets levels on specified pages.

        Parameters
        ----------
        pages: Iterable[:class:`int`]
            Pages to look at, represented as a finite iterable.

        Returns
        -------
        AsyncIterator[:class:`.Level`]
            All levels found.
        """
        return self.client.search_levels(
            pages=pages, filters=Filters.by_user(), user=self, concurrent=concurrent
        )

    @async_iterable
    def get_profile_comments_on_page(self, page: int = 0) -> AsyncIterator["Comment"]:
        """Gets user's profile comments on a specific page.
        """
        return self.client.get_user_comments_on_page(user=self, type=CommentType.PROFILE, page=page)

    get_comments_on_page = get_profile_comments_on_page

    @async_iterable
    def get_comment_history_on_page(
        self, strategy: Union[int, str, CommentStrategy] = CommentStrategy.RECENT, page: int = 0,
    ) -> AsyncIterator["Comment"]:
        """Retrieves user's level comments. (history)
        """
        return self.client.get_user_comments_on_page(user=self, type=CommentType.LEVEL, page=page)

    @async_iterable
    def get_profile_comments(
        self, pages: Optional[Iterable[int]] = PAGES, concurrent: bool = CONCURRENT
    ) -> AsyncIterator["Comment"]:
        """Gets user's profile comments on specific pages.
        """
        return self.client.get_user_comments(
            user=self, type=CommentType.PROFILE, pages=pages, concurrent=concurrent
        )

    get_comments = get_profile_comments

    @async_iterable
    def get_comment_history(
        self,
        strategy: Union[int, str, CommentStrategy] = CommentStrategy.RECENT,
        pages: Optional[Iterable[int]] = PAGES,
        concurrent: bool = CONCURRENT,
    ) -> AsyncIterator["Comment"]:
        """Gets user's level (history) comments on specific pages.
        """
        return self.client.get_user_comments(
            user=self, type=CommentType.LEVEL, pages=pages, concurrent=concurrent
        )

    async def generate(
        self, type: Union[int, str, IconType] = "icon", as_image: bool = False,
    ) -> Union[bytes, "PIL.Image.Image"]:
        """Generate an image of an icon.

        Parameters
        ----------
        type: Optional[Union[:class:`int`, :class:`str`, :class:`.IconType`]]
            Type of an icon to generate. If not given or ``"icon"``, picks current icon.

        as_image: :class:`bool`
            Whether to return an image or bytes of an image.

        Returns
        -------
        Union[:class:`bytes`, :class:`PIL.Image.Image`]
            Bytes or an image, based on ``as_image``.
        """
        if type == "icon":
            icon_type, icon_id = self.icon_type, self.icon

        else:
            icon_type = IconType.from_value(type)
            icon_id = self.get_id_by_type(icon_type)

        result = await run_blocking(
            factory.generate,  # type: ignore
            icon_type=icon_type,
            icon_id=icon_id,
            color_1=self.color_1,
            color_2=self.color_2,
            glow_outline=self.has_glow_outline(),
        )

        if as_image:
            return result

        return await run_blocking(to_bytes, result)

    @async_iterable
    async def generate_many(
        self, *types: Union[int, str, IconType], as_image: bool = False,
    ) -> Union[AsyncIterator[bytes], AsyncIterator["PIL.Image.Image"]]:
        r"""Generate images of icons.

        Parameters
        ----------
        \*types: Union[:class:`int`, :class:`str`, :class:`.IconType`]
            Types of icons to generate. If ``"icon"`` is given, picks current main icon.

        as_image: :class:`bool`
            Whether to return images or bytes of images.

        Returns
        -------
        Union[AsyncIterator[:class:`bytes`], AsyncIterator[:class:`PIL.Image.Image`]]
            Bytes or images, based on ``as_image``.
        """
        if not types:
            raise TypeError("No types were given.")

        for type in types:
            image = await self.generate(type=type, as_image=as_image)
            yield image

    async def generate_image(
        self, *types: Union[int, str, IconType], as_image: bool = False,
    ) -> Union[bytes, "PIL.Image.Image"]:
        r"""Generate images of icons and connect them into one image.

        Parameters
        ----------
        \*types: Iterable[Optional[Union[:class:`int`, :class:`str`, :class:`.IconType`]]]
            Types of icons to generate. If ``"icon"`` is given, picks current main icon.

        as_image: :class:`bool`
            Whether to return an image or bytes of an image.

        Returns
        -------
        Union[:class:`bytes`, :class:`PIL.Image.Image`]
            Bytes or an image, based on ``as_image``.
        """
        images = await self.generate_many(*types, as_image=True).flatten()
        result = await run_blocking(connect_images, images)

        if as_image:
            return result

        return await run_blocking(to_bytes, result)

    async def generate_full(self, as_image: bool = False) -> Union[bytes, "PIL.Image.Image"]:
        """Generate an image of the full icon set.

        Parameters
        ----------
        as_image: :class:`bool`
            Whether to return an image or bytes of an image.

        Returns
        -------
        Union[:class:`bytes`, :class:`PIL.Image.Image`]
            Bytes or an image, based on ``as_image``.
        """
        return await self.generate_image(*self.ALL_TYPES, as_image=as_image)

    ALL_TYPES = ("cube", "ship", "ball", "ufo", "wave", "robot", "spider")
