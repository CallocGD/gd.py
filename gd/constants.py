from typing_extensions import Literal

EMPTY_BYTES = bytes()

EMPTY = str()
SPACE = " "

BACKSLASH = "\\"
SLASH = "/"

UNKNOWN = "unknown"
UNNAMED = "unnamed"

COMPLETED = 100

DEFAULT_DELAY = 10.0
DEFAULT_RECONNECT = True

DEFAULT_RESOLUTION = -1

DEFAULT_SIMPLE = False
DEFAULT_FRIEND_STATE = False

DEFAULT_UPDATE = True

DEFAULT_AMOUNT = 0
DEFAULT_REWARD = 0

CHESTS_SLICE = 5
QUESTS_SLICE = 5

DEFAULT_COLOR_1_ID = 0
DEFAULT_COLOR_2_ID = 3

DEFAULT_GLOW = False

DEFAULT_ID = 0

ROBTOP_ACCOUNT_ID = 71
ROBTOP_ID = 16
ROBTOP_NAME = "RobTop"

DEFAULT_SIZE = 0.0

DEFAULT_RECORD = 0

DEFAULT_SPECIAL = 0

DEFAULT_COUNT = 100

DEFAULT_VERSION = 1
DEFAULT_OBJECT_COUNT = 0
DEFAULT_COINS = 0

DEFAULT_HIGH_OBJECT_COUNT = False

DEFAULT_ORB_PERCENTAGE = 0

DEFAULT_ICON_ID = 1

DEFAULT_STARS = 0
DEFAULT_DEMONS = 0
DEFAULT_DIAMONDS = 0
DEFAULT_ORBS = 0
DEFAULT_RANK = 0
DEFAULT_CREATOR_POINTS = 0
DEFAULT_SECRET_COINS = 0
DEFAULT_USER_COINS = 0

DEFAULT_JUMPS = 0
DEFAULT_SECONDS = 0
DEFAULT_PLAYED = False

DEFAULT_SEND = False

DEFAULT_ATTEMPTS = 0
DEFAULT_COMPLETIONS = 0

DEFAULT_LOW_DETAIL = False
DEFAULT_LOW_DETAIL_TOGGLED = False

DEFAULT_LEVEL_ORDER = 0

DEFAULT_KEYS = 0

DEFAULT_PLACE = 0

DEFAULT_ACTIVE = True
DEFAULT_BANNED = not DEFAULT_ACTIVE

DEFAULT_NEW = 0

DEFAULT_SENT = False

DEFAULT_READ = False
DEFAULT_UNREAD = not DEFAULT_READ

DEFAULT_CONTENT_PRESENT = False

DEFAULT_DENOMINATOR = 0
DEFAULT_NUMERATOR = 0

DEFAULT_DOWNLOADS = 0

DEFAULT_RATING = 0

DEFAULT_CLICKS = 0

DEFAULT_DEMON = False
DEFAULT_AUTO = False

DEFAULT_SCORE = 0

DEFAULT_EDITABLE = True
DEFAULT_VERIFIED = False
DEFAULT_UPLOADED = False
DEFAULT_PLAYABLE = True
DEFAULT_UNLOCKED = False

DEFAULT_FIRST_COIN_VERIFIED = False
DEFAULT_SECOND_COIN_VERIFIED = False
DEFAULT_THIRD_COIN_VERIFIED = False

DEFAULT_TWO_PLAYER = False

# DEFAULT_PLATFORMER = False

DEFAULT_VERIFIED_COINS = False

DEFAULT_EPIC = False

DEFAULT_GAUNTLET = False
DEFAULT_UNLISTED = False

DEFAULT_FAVORITE = False

DEFAULT_SPAM = False

ZERO_PAGE = range(1)

COMMENT_PAGE_SIZE = 20

DEFAULT_LOAD_AFTER_POST = True

DEFAULT_GET_DATA = True
DEFAULT_USE_CLIENT = False

DEFAULT_SERVER_STYLE = True
DEFAULT_RETURN_DEFAULT = True

DEFAULT_FROM_NEWGROUNDS = False

DEFAULT_WITH_BAR = False

DEFAULT_PAGE = 0

DEFAULT_PAGES_COUNT = 10
DEFAULT_PAGES = range(DEFAULT_PAGES_COUNT)

DEFAULT_CHEST_COUNT = 0

DEFAULT_WIDTH = 250
DEFAULT_HEIGHT = 250

DEFAULT_ENCODING = "utf-8"
DEFAULT_ERRORS = "strict"

TIMELY_ID_ADD = 100_000

READ: Literal["r"] = "r"
READ_BINARY: Literal["rb"] = "rb"
WRITE: Literal["w"] = "w"
WRITE_BINARY: Literal["wb"] = "wb"
