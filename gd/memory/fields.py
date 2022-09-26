from __future__ import annotations

from abc import abstractmethod
from typing import (
    TYPE_CHECKING,
    Any,
    Generic,
    Iterator,
    Optional,
    Tuple,
    Type,
    TypeVar,
    Union,
    overload,
)

from attrs import define, field
from typing_extensions import Never, Protocol

from gd.binary_constants import (
    F32_SIZE,
    F64_SIZE,
    I8_SIZE,
    I16_SIZE,
    I32_SIZE,
    I64_SIZE,
    U8_SIZE,
    U16_SIZE,
    U32_SIZE,
    U64_SIZE,
)
from gd.enums import ByteOrder
from gd.memory.state import AbstractState
from gd.platform import PlatformConfig
from gd.typing import AnyType, StringDict, is_instance

__all__ = ("Field",)

T = TypeVar("T")


class FieldProtocol(Protocol[T]):
    @abstractmethod
    def read(self, state: AbstractState, address: int, order: ByteOrder = ByteOrder.NATIVE) -> T:
        ...

    @abstractmethod
    def write(
        self, state: AbstractState, address: int, value: T, order: ByteOrder = ByteOrder.NATIVE
    ) -> None:
        ...

    @abstractmethod
    def compute_size(self, config: PlatformConfig) -> int:
        ...

    @abstractmethod
    def compute_alignment(self, config: PlatformConfig) -> int:
        ...


FROZEN_FIELD = "this field is frozen"
CAN_NOT_DELETE_FIELDS = "can not delete fields"

DEFAULT_OFFSET = 0
DEFAULT_FROZEN = False


B = TypeVar("B", bound="Base")

F = TypeVar("F", bound="AnyField")


@define()
class Field(FieldProtocol[T]):
    offset: int = field(default=DEFAULT_OFFSET, repr=hex)

    def copy(self: F) -> F:
        return type(self)(self.offset)


AnyField = Field[Any]


def fetch_fields_iterator(base: Type[B]) -> Iterator[Tuple[str, AnyField]]:
    for type in reversed(base.mro()):
        for name, value in vars(type).items():
            if is_instance(value, Field):
                yield (name, value)


def fetch_fields(base: Type[B]) -> StringDict[AnyField]:
    return dict(fetch_fields_iterator(base))


@define()
class ActualField(Generic[T]):
    field: Field[T]

    @overload
    def __get__(self, instance: None, type: Optional[Type[B]] = ...) -> Field[T]:
        ...

    @overload
    def __get__(self, instance: B, type: Optional[Type[B]]) -> T:
        ...

    def __get__(self, instance: Optional[B], type: Optional[Type[B]] = None) -> Union[Field[T], T]:
        if instance is None:
            return self.field

        if is_instance(instance, Base):
            return self.field.read(
                instance.state, instance.address + self.field.offset, instance.order
            )

        return self.field

    def __set__(self, instance: B, value: T) -> None:
        self.field.write(
            instance.state, instance.address + self.field.offset, value, instance.order
        )

    def __delete__(self, instance: B) -> Never:
        raise AttributeError(CAN_NOT_DELETE_FIELDS)


@define()
class I8(Field[int]):
    def read(self, state: AbstractState, address: int, order: ByteOrder = ByteOrder.NATIVE) -> int:
        return state.read_i8(address, order)

    def write(
        self, state: AbstractState, address: int, value: int, order: ByteOrder = ByteOrder.NATIVE
    ) -> None:
        state.write_i8(address, value, order)

    def compute_size(self, config: PlatformConfig) -> int:
        return I8_SIZE

    def compute_alignment(self, config: PlatformConfig) -> int:
        return I8_SIZE


@define()
class U8(Field[int]):
    def read(self, state: AbstractState, address: int, order: ByteOrder = ByteOrder.NATIVE) -> int:
        return state.read_u8(address, order)

    def write(
        self, state: AbstractState, address: int, value: int, order: ByteOrder = ByteOrder.NATIVE
    ) -> None:
        state.write_u8(address, value, order)

    def compute_size(self, config: PlatformConfig) -> int:
        return U8_SIZE

    def compute_alignment(self, config: PlatformConfig) -> int:
        return U8_SIZE


@define()
class I16(Field[int]):
    def read(self, state: AbstractState, address: int, order: ByteOrder = ByteOrder.NATIVE) -> int:
        return state.read_i16(address, order)

    def write(
        self, state: AbstractState, address: int, value: int, order: ByteOrder = ByteOrder.NATIVE
    ) -> None:
        state.write_i16(address, value, order)

    def compute_size(self, config: PlatformConfig) -> int:
        return I16_SIZE

    def compute_alignment(self, config: PlatformConfig) -> int:
        return I16_SIZE


@define()
class U16(Field[int]):
    def read(self, state: AbstractState, address: int, order: ByteOrder = ByteOrder.NATIVE) -> int:
        return state.read_u16(address, order)

    def write(
        self, state: AbstractState, address: int, value: int, order: ByteOrder = ByteOrder.NATIVE
    ) -> None:
        state.write_u16(address, value, order)

    def compute_size(self, config: PlatformConfig) -> int:
        return U16_SIZE

    def compute_alignment(self, config: PlatformConfig) -> int:
        return U16_SIZE


@define()
class I32(Field[int]):
    def read(self, state: AbstractState, address: int, order: ByteOrder = ByteOrder.NATIVE) -> int:
        return state.read_i32(address, order)

    def write(
        self, state: AbstractState, address: int, value: int, order: ByteOrder = ByteOrder.NATIVE
    ) -> None:
        state.write_i32(address, value, order)

    def compute_size(self, config: PlatformConfig) -> int:
        return I32_SIZE

    def compute_alignment(self, config: PlatformConfig) -> int:
        return I32_SIZE


@define()
class U32(Field[int]):
    def read(self, state: AbstractState, address: int, order: ByteOrder = ByteOrder.NATIVE) -> int:
        return state.read_u32(address, order)

    def write(
        self, state: AbstractState, address: int, value: int, order: ByteOrder = ByteOrder.NATIVE
    ) -> None:
        state.write_u32(address, value, order)

    def compute_size(self, config: PlatformConfig) -> int:
        return U32_SIZE

    def compute_alignment(self, config: PlatformConfig) -> int:
        return U32_SIZE


@define()
class I64(Field[int]):
    def read(self, state: AbstractState, address: int, order: ByteOrder = ByteOrder.NATIVE) -> int:
        return state.read_i64(address, order)

    def write(
        self, state: AbstractState, address: int, value: int, order: ByteOrder = ByteOrder.NATIVE
    ) -> None:
        state.write_i64(address, value, order)

    def compute_size(self, config: PlatformConfig) -> int:
        return I64_SIZE

    def compute_alignment(self, config: PlatformConfig) -> int:
        return I64_SIZE


@define()
class U64(Field[int]):
    def read(self, state: AbstractState, address: int, order: ByteOrder = ByteOrder.NATIVE) -> int:
        return state.read_u64(address, order)

    def write(
        self, state: AbstractState, address: int, value: int, order: ByteOrder = ByteOrder.NATIVE
    ) -> None:
        state.write_u64(address, value, order)

    def compute_size(self, config: PlatformConfig) -> int:
        return U64_SIZE

    def compute_alignment(self, config: PlatformConfig) -> int:
        return U64_SIZE


@define()
class ISize(Field[int]):
    def read(self, state: AbstractState, address: int, order: ByteOrder = ByteOrder.NATIVE) -> int:
        return state.read_isize(address, order)

    def write(
        self, state: AbstractState, address: int, value: int, order: ByteOrder = ByteOrder.NATIVE
    ) -> None:
        state.write_isize(address, value, order)

    def compute_size(self, config: PlatformConfig) -> int:
        size = {8: I8_SIZE, 16: I16_SIZE, 32: I32_SIZE, 64: I64_SIZE}

        return size[config.bits]

    def compute_alignment(self, config: PlatformConfig) -> int:
        alignment = {8: I8_SIZE, 16: I16_SIZE, 32: I32_SIZE, 64: I64_SIZE}

        return alignment[config.bits]


@define()
class USize(Field[int]):
    def read(self, state: AbstractState, address: int, order: ByteOrder = ByteOrder.NATIVE) -> int:
        return state.read_usize(address, order)

    def write(
        self, state: AbstractState, address: int, value: int, order: ByteOrder = ByteOrder.NATIVE
    ) -> None:
        state.write_usize(address, value, order)

    def compute_size(self, config: PlatformConfig) -> int:
        size = {8: U8_SIZE, 16: U16_SIZE, 32: U32_SIZE, 64: U64_SIZE}

        return size[config.bits]

    def compute_alignment(self, config: PlatformConfig) -> int:
        alignment = {8: U8_SIZE, 16: U16_SIZE, 32: U32_SIZE, 64: U64_SIZE}

        return alignment[config.bits]


class F32(Field[float]):
    def read(
        self, state: AbstractState, address: int, order: ByteOrder = ByteOrder.NATIVE
    ) -> float:
        return state.read_f32(address, order)

    def write(
        self, state: AbstractState, address: int, value: float, order: ByteOrder = ByteOrder.NATIVE
    ) -> None:
        state.write_f32(address, value, order)

    def compute_size(self, config: PlatformConfig) -> int:
        return F32_SIZE

    def compute_alignment(self, config: PlatformConfig) -> int:
        return F32_SIZE


class F64(Field[float]):
    def read(
        self, state: AbstractState, address: int, order: ByteOrder = ByteOrder.NATIVE
    ) -> float:
        return state.read_f64(address, order)

    def write(
        self, state: AbstractState, address: int, value: float, order: ByteOrder = ByteOrder.NATIVE
    ) -> None:
        state.write_f64(address, value, order)

    def compute_size(self, config: PlatformConfig) -> int:
        return F64_SIZE

    def compute_alignment(self, config: PlatformConfig) -> int:
        return F64_SIZE


class Byte(Field[int]):
    def read(self, state: AbstractState, address: int, order: ByteOrder = ByteOrder.NATIVE) -> int:
        return state.read_byte(address, order)

    def write(
        self, state: AbstractState, address: int, value: int, order: ByteOrder = ByteOrder.NATIVE
    ) -> None:
        state.write_byte(address, value, order)

    def compute_size(self, config: PlatformConfig) -> int:
        return I8_SIZE

    def compute_alignment(self, config: PlatformConfig) -> int:
        return I8_SIZE


class UByte(Field[int]):
    def read(self, state: AbstractState, address: int, order: ByteOrder = ByteOrder.NATIVE) -> int:
        return state.read_ubyte(address, order)

    def write(
        self, state: AbstractState, address: int, value: int, order: ByteOrder = ByteOrder.NATIVE
    ) -> None:
        state.write_ubyte(address, value, order)

    def compute_size(self, config: PlatformConfig) -> int:
        return U8_SIZE

    def compute_alignment(self, config: PlatformConfig) -> int:
        return U8_SIZE


class Short(Field[int]):
    def read(self, state: AbstractState, address: int, order: ByteOrder = ByteOrder.NATIVE) -> int:
        return state.read_short(address, order)

    def write(
        self, state: AbstractState, address: int, value: int, order: ByteOrder = ByteOrder.NATIVE
    ) -> None:
        state.write_short(address, value, order)

    def compute_size(self, config: PlatformConfig) -> int:
        return I16_SIZE

    def compute_alignment(self, config: PlatformConfig) -> int:
        return I16_SIZE


class UShort(Field[int]):
    def read(self, state: AbstractState, address: int, order: ByteOrder = ByteOrder.NATIVE) -> int:
        return state.read_ushort(address, order)

    def write(
        self, state: AbstractState, address: int, value: int, order: ByteOrder = ByteOrder.NATIVE
    ) -> None:
        state.write_ushort(address, value, order)

    def compute_size(self, config: PlatformConfig) -> int:
        return U16_SIZE

    def compute_alignment(self, config: PlatformConfig) -> int:
        return U16_SIZE


class Int(Field[int]):
    def read(self, state: AbstractState, address: int, order: ByteOrder = ByteOrder.NATIVE) -> int:
        return state.read_int(address, order)

    def write(
        self, state: AbstractState, address: int, value: int, order: ByteOrder = ByteOrder.NATIVE
    ) -> None:
        state.write_int(address, value, order)

    def compute_size(self, config: PlatformConfig) -> int:
        if config.bits < 32:
            return I16_SIZE

        return I32_SIZE

    def compute_alignment(self, config: PlatformConfig) -> int:
        if config.bits < 32:
            return I16_SIZE

        return I32_SIZE


class UInt(Field[int]):
    def read(self, state: AbstractState, address: int, order: ByteOrder = ByteOrder.NATIVE) -> int:
        return state.read_uint(address, order)

    def write(
        self, state: AbstractState, address: int, value: int, order: ByteOrder = ByteOrder.NATIVE
    ) -> None:
        state.write_uint(address, value, order)

    def compute_size(self, config: PlatformConfig) -> int:
        if config.bits < 32:
            return U16_SIZE

        return U32_SIZE

    def compute_alignment(self, config: PlatformConfig) -> int:
        if config.bits < 32:
            return U16_SIZE

        return U32_SIZE


class Long(Field[int]):
    def read(self, state: AbstractState, address: int, order: ByteOrder = ByteOrder.NATIVE) -> int:
        return state.read_long(address, order)

    def write(
        self, state: AbstractState, address: int, value: int, order: ByteOrder = ByteOrder.NATIVE
    ) -> None:
        state.write_long(address, value, order)

    def compute_size(self, config: PlatformConfig) -> int:
        if config.bits > 32 and not config.platform.is_windows():
            return I64_SIZE

        return I32_SIZE

    def compute_alignment(self, config: PlatformConfig) -> int:
        if config.bits > 32 and not config.platform.is_windows():
            return I64_SIZE

        return I32_SIZE


class ULong(Field[int]):
    def read(self, state: AbstractState, address: int, order: ByteOrder = ByteOrder.NATIVE) -> int:
        return state.read_ulong(address, order)

    def write(
        self, state: AbstractState, address: int, value: int, order: ByteOrder = ByteOrder.NATIVE
    ) -> None:
        state.write_ulong(address, value, order)

    def compute_size(self, config: PlatformConfig) -> int:
        if config.bits > 32 and not config.platform.is_windows():
            return U64_SIZE

        return U32_SIZE

    def compute_alignment(self, config: PlatformConfig) -> int:
        if config.bits > 32 and not config.platform.is_windows():
            return U64_SIZE

        return U32_SIZE


class LongLong(Field[int]):
    def read(self, state: AbstractState, address: int, order: ByteOrder = ByteOrder.NATIVE) -> int:
        return state.read_longlong(address, order)

    def write(
        self, state: AbstractState, address: int, value: int, order: ByteOrder = ByteOrder.NATIVE
    ) -> None:
        state.write_longlong(address, value, order)

    def compute_size(self, config: PlatformConfig) -> int:
        return I64_SIZE

    def compute_alignment(self, config: PlatformConfig) -> int:
        return I64_SIZE


class ULongLong(Field[int]):
    def read(self, state: AbstractState, address: int, order: ByteOrder = ByteOrder.NATIVE) -> int:
        return state.read_ulonglong(address, order)

    def write(
        self, state: AbstractState, address: int, value: int, order: ByteOrder = ByteOrder.NATIVE
    ) -> None:
        state.write_ulonglong(address, value, order)

    def compute_size(self, config: PlatformConfig) -> int:
        return U64_SIZE

    def compute_alignment(self, config: PlatformConfig) -> int:
        return U64_SIZE


@define()
class Size(Field[int]):
    def read(self, state: AbstractState, address: int, order: ByteOrder = ByteOrder.NATIVE) -> int:
        return state.read_size(address, order)

    def write(
        self, state: AbstractState, address: int, value: int, order: ByteOrder = ByteOrder.NATIVE
    ) -> None:
        state.write_size(address, value, order)

    def compute_size(self, config: PlatformConfig) -> int:
        size = {8: I8_SIZE, 16: I16_SIZE, 32: I32_SIZE, 64: I64_SIZE}

        return size[config.bits]

    def compute_alignment(self, config: PlatformConfig) -> int:
        size = {8: I8_SIZE, 16: I16_SIZE, 32: I32_SIZE, 64: I64_SIZE}

        return size[config.bits]


class Float(Field[float]):
    def read(
        self, state: AbstractState, address: int, order: ByteOrder = ByteOrder.NATIVE
    ) -> float:
        return state.read_float(address, order)

    def write(
        self, state: AbstractState, address: int, value: float, order: ByteOrder = ByteOrder.NATIVE
    ) -> None:
        state.write_float(address, value, order)

    def compute_size(self, config: PlatformConfig) -> int:
        return F32_SIZE

    def compute_alignment(self, config: PlatformConfig) -> int:
        return F32_SIZE


class Double(Field[float]):
    def read(
        self, state: AbstractState, address: int, order: ByteOrder = ByteOrder.NATIVE
    ) -> float:
        return state.read_double(address, order)

    def write(
        self, state: AbstractState, address: int, value: float, order: ByteOrder = ByteOrder.NATIVE
    ) -> None:
        state.write_double(address, value, order)

    def compute_size(self, config: PlatformConfig) -> int:
        return F64_SIZE

    def compute_alignment(self, config: PlatformConfig) -> int:
        return F64_SIZE


# import cycle solution
from gd.memory.array import Array

UNSIZED_ARRAY = "array is unsized"

AF = TypeVar("AF", bound="AnyArrayField")


@define()
class ArrayField(Field[Array[T]]):
    type: Field[T] = field()
    length: Optional[int] = field(default=None)

    offset: int = field(default=DEFAULT_OFFSET, repr=hex)

    array_type: Type[Array[T]] = field(default=Array[T], repr=False)

    def read(
        self, state: AbstractState, address: int, order: ByteOrder = ByteOrder.NATIVE
    ) -> Array[T]:
        return self.array_type(state, address, self.type, self.length, order)

    def write(
        self,
        state: AbstractState,
        address: int,
        value: Array[T],
        order: ByteOrder = ByteOrder.NATIVE,
    ) -> None:
        pass  # do nothing

    def compute_size(self, config: PlatformConfig) -> int:
        length = self.length

        if length is None:
            raise TypeError(UNSIZED_ARRAY)

        return self.type.compute_size(config) * length

    def compute_alignment(self, config: PlatformConfig) -> int:
        return self.type.compute_alignment(config)

    def copy(self: AF) -> AF:
        return type(self)(self.type, self.length, self.offset, self.array_type)


AnyArrayField = ArrayField[Any]


# import cycle solution
from gd.memory.base import Base
