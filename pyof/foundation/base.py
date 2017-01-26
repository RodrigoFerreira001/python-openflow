"""Base and fundamental classes used all over the library.

Besides classes, several constants are defined here. We designed
python-openflow in a manner to make it easy to create new messages and OpenFlow
structs. You can realize that when you see a message class definition.

A **struct** here is a group of basic attributes and/or struct attributes (i.e.
:class:`~.common.header.Header`). A **message** here is like a struct, but all
messages have a header attribute (i.e.
:class:`~.asynchronous.packet_in.PacketIn`).

The main classes of this module are :class:`GenericStruct`,
:class:`GenericMessage`, :class:`GenericBitMask` and :class:`GenericType`.
These classes are used in all parts of this library.
"""

# System imports
import importlib
import inspect
import re
import struct
from collections import OrderedDict
from copy import copy, deepcopy
from enum import Enum
from random import randint
from pyof.foundation.constants import UBINT32_MAX_VALUE as MAXID

# Local source tree imports
from pyof.foundation.exceptions import (BadValueException, PackException,
                                        UnpackException, ValidationError)

# Third-party imports


# This will determine the order on sphinx documentation.
__all__ = ('GenericStruct', 'GenericMessage', 'GenericType', 'GenericBitMask',
           'MetaStruct', 'MetaBitMask')

# Classes


class GenericType:
    """Foundation class for all custom attributes.

    Base class for :class:`~.UBInt8`, :class:`~.Char`
    and others.
    """

    _fmt = None

    def __init__(self, value=None, enum_ref=None):
        """The constructor takes the optional parameters below.

        Args:
            value: The type's value.
            enum_ref (:class:`type`): If :attr:`value` is from an Enum, specify
                its type.
        """
        self._value = value
        self.enum_ref = enum_ref

    def __repr__(self):
        return "{}({})".format(type(self).__name__, self._value)

    def __str__(self):
        return '{}'.format(str(self._value))

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.pack() == other.pack()
        elif hasattr(other, 'value'):
            return self.value == other.value
        return self.value == other

    def __ne__(self, other):
        return self._value != other

    def __gt__(self, other):
        return self._value > other

    def __ge__(self, other):
        return self._value >= other

    def __lt__(self, other):
        return self._value <= other

    def __le__(self, other):
        return self._value <= other

    def __add__(self, other):
        return self.value + other

    def __radd__(self, other):
        return self.value + other

    def __sub__(self, other):
        return self.value - other

    def __rsub__(self, other):
        return self.value - other

    def __or__(self, other):
        return self.value | other

    def __ror__(self, other):
        return self.value | other

    def __and__(self, other):
        return self.value & other

    def __rand__(self, other):
        return self.value & other

    def __xor__(self, other):
        return self.value ^ other

    def __rxor__(self, other):
        return self.value ^ other

    @property
    def value(self):
        """Return this type's value.

        The value of an enum, bitmask, etc.
        """
        if self.isenum():
            if isinstance(self._value, self.enum_ref):
                return self._value.value
            return self._value
        elif self.is_bitmask():
            return self._value.bitmask
        else:
            return self._value

    def pack(self, value=None):
        r"""Pack the value as a binary representation.

        Considering an example with UBInt8 class, that inherits from
        GenericType:

        >>> from pyof.foundation.basic_types import UBInt8
        >>> objectA = UBInt8(1)
        >>> objectB = 5
        >>> objectA.pack()
        b'\x01'
        >>> objectA.pack(objectB)
        b'\x05'

        Args:
            value: If the value is None, then we will pack the value of the
                current instance. Otherwise, if value is an instance of the
                same type as the current instance, then we call the pack of the
                value object. Otherwise, we will use the current instance pack
                method on the passed value.

        Returns:
            bytes: The binary representation.

        Raises:
            :exc:`~.exceptions.BadValueException`: If the value does not
                fit the binary format.
        """
        if isinstance(value, type(self)):
            return value.pack()

        if value is None:
            value = self.value
        elif 'value' in dir(value):
            # if it is enum or bitmask gets only the 'int' value
            value = value.value

        try:
            return struct.pack(self._fmt, value)
        except struct.error:
            msg = '{} could not pack {} = {}.'.format(type(self).__name__,
                                                      type(value).__name__,
                                                      value)
            raise PackException(msg)

    def unpack(self, buff, offset=0):
        """Unpack *buff* into this object.

        This method will convert a binary data into a readable value according
        to the attribute format.

        Args:
            buff (bytes): Binary buffer.
            offset (int): Where to begin unpacking.

        Raises:
            :exc:`~.exceptions.UnpackException`: If unpack fails.
        """
        try:
            self._value = struct.unpack_from(self._fmt, buff, offset)[0]
            if self.enum_ref:
                self._value = self.enum_ref(self._value)
        except (struct.error, TypeError, ValueError) as e:
            msg = '{}; fmt = {}, buff = {}, offset = {}.'.format(e, self._fmt,
                                                                 buff, offset)
            raise UnpackException(msg)

    def get_size(self, value=None):
        """Return the size in bytes of this type.

        Returns:
            int: Size in bytes.
        """
        return struct.calcsize(self._fmt)

    def is_valid(self):
        """Check whether the value fits the binary format.

        Assert that :func:`pack` succeeds.

        Returns:
            bool: Whether the value is valid for this type.
        """
        try:
            self.pack()
            return True
        except BadValueException:
            return False

    def isenum(self):
        """Test whether it is an :class:`~Enum`.

        Returns:
            bool: Whether it is an :class:`~Enum`.
        """
        return self.enum_ref and issubclass(self.enum_ref, Enum)

    def is_bitmask(self):
        """Test whether it is a :class:`GenericBitMask`.

        Returns:
            bool: Whether it is a :class:`GenericBitMask`.
        """
        return self._value and issubclass(type(self._value), GenericBitMask)


class MetaBitMask(type):
    """MetaClass to create a special BitMaskEnum type.

    You probably do not need to use this class. Inherit from
    :class:`GenericBitMask` instead.

    This metaclass converts the declared class attributes into elements of an
    enum. It also replaces the :meth:`__dir__` and :meth:`__getattr__` methods,
    so the resulting class will behave as an :class:`~Enum` class (you can
    access object.ELEMENT and recover either values or names).
    """

    def __new__(mcs, name, bases, classdict):
        """Convert class attributes into enum elements."""
        _enum = OrderedDict([(key, value) for key, value in classdict.items()
                             if key[0] != '_' and not
                             hasattr(value, '__call__') and not
                             isinstance(value, property)])
        if _enum:
            classdict = {key: value for key, value in classdict.items()
                         if key[0] == '_' or hasattr(value, '__call__') or
                         isinstance(value, property)}
            classdict['_enum'] = _enum
        return type.__new__(mcs, name, bases, classdict)

    def __getattr__(cls, name):
        return cls._enum[name]

    def __dir__(cls):
        res = dir(type(cls)) + list(cls.__dict__.keys())
        if cls is not GenericBitMask:
            res.extend(cls._enum)
        return res


class GenericBitMask(object, metaclass=MetaBitMask):
    """Base class for enums that use bitmask values."""

    def __init__(self, bitmask=None):
        """The constructor has the optional parameter below.

        Args:
            bitmask: Bitmask value.
        """
        self.bitmask = bitmask
        self._enum = {}

    def __str__(self):
        return "{}".format(self.bitmask)

    def __repr__(self):
        return "{}({})".format(type(self).__name__, self.bitmask)

    @property
    def names(self):
        """List of selected enum names.

        Returns:
            list: Enum names.
        """
        result = []
        for key, value in self.iteritems():
            if value & self.bitmask:
                result.append(key)
        return result

    def iteritems(self):
        """Generator for attributes' name-value pairs.

        Returns:
            generator: Attributes' (name, value) tuples.
        """
        for key, value in self._enum.items():
            yield (key, value)


class MetaStruct(type):
    """MetaClass that dinamically handles openflow version of class attributes.

    See more about it at:
        https://github.com/kytos/python-openflow/wiki/Version-Inheritance

    You do not need to use this class. Inherit from :class:`GenericStruct`
    instead.
    """

    # pylint: disable=unused-argument
    @classmethod
    def __prepare__(mcs, name, bases, **kwargs):
        return OrderedDict()

    def __new__(cls, name, bases, classdict, **kwargs):
        """Inherit attributes from parent class and update their versions.

        Here is the moment that the new class is going to be created. During
        this process, two things may be done.

        Firstly, we will look if the type of any parent classes is this
        MetaStruct. We will inherit from the first parent class that fits this
        requirement. If any is found, then we will get all attributes from this
        class and place them as class attributes on the class being created.

        Secondly, for each class attribute being inherited, we will make sure
        that the pyof version of this attribute is the same as the version of
        the current class being created. If it is not, then we will find out
        which is the class and module of that attribute, look for a version
        that matches the version of the current class and replace that
        attribute with the correct version.

        See this link for more information on why this is being done:
            - https://github.com/kytos/python-openflow/wiki/Version-Inheritance
        """
        #: Retrieving class attributes management markers
        removed_attributes = classdict.pop('_removed_attributes', [])
        # renamed_attributes = classdict.pop('_renamed_attributes', [])
        # reordered_attributes = classdict.pop('_reordered_attributes', {})

        # curr_module = classdict.get('__module__')
        # curr_version = MetaStruct.get_pyof_mod_version(curr_module)
        mod = inspect.currentframe().f_back.f_locals['__name__']
        curr_version = MetaStruct.get_pyof_mod_version(mod)

        inherited_attributes = None
        new_attributes = None

        #: looking for (kytos) class attributes defined on the bases
        #: classes so we can copy them into the current class being created
        #: so we can "inherit" them as class attributes
        for base in bases:
            #: Check if we are inheriting from one of our classes.
            if isinstance(base, MetaStruct):
                inherited_attributes = OrderedDict()
                new_attributes = OrderedDict()
                for attr_name, obj in base._get_class_attributes():
                    inherited_attributes.update([(attr_name, obj)])
                    #: Get an updated version of this attribute,
                    #: considering the version of the current class being
                    #: created.
                    new_obj = MetaStruct.update_obj_version(obj, curr_version)

                    new_attributes.update([(attr_name, new_obj)])
                #: We are going to inherit just from the 'closest parent'
                #: Because of that we break the loop here.
                break

        #: If we have inherited something, then first we will remove the
        #: attributes marked to be removed on the 'removed_attributes' and
        #: after that we will update the inherited 'classdict' with the
        #: attributes from the current classdict.
        if new_attributes is not None:
            #: removing attributes set to be removed
            for attr_name in removed_attributes:
                new_attributes.pop(attr_name, None)

            #: Updating the inherited attributes with those defined on the
            #: body of the class being created.
            new_attributes.update(classdict)
            classdict = new_attributes

        return super().__new__(cls, name, bases, classdict, **kwargs)

    @staticmethod
    def get_pyof_mod_version(module_fullname):
        """Get the module pyof version based on the module fullname.

        Args:
            module_fullname (str): The fullname of the module
                (e.g.: pyof.v0x01.common.header)

        Returns:
            version (str): The module version, on the format 'v0x0?' if any. Or
            None (None): If there isn't a version on the fullname.
        """
        ver_module_re = re.compile(r'(pyof\.)(v0x\d+)(\..*)')
        matched = ver_module_re.match(module_fullname)
        if matched:
            version = matched.group(2)
            # module = matched.group(3)
            return version
        return None

    @staticmethod
    def get_updated_pyof_class(cls_name, module_fullname, version):
        """Replace the OF Version of a module fullname.

        Get's a module name (eg. 'pyof.v0x01.common.header') and returns it on
        a new 'version' (eg. 'pyof.v0x02.common.header').

        Args:
            module_fullname (str): The fullname of the module
                (e.g.: pyof.v0x01.common.header)
            version (str): The version to be 'inserted' on the module fullname.

        Returns:
            None (None): if the requested version is the same as the one of the
                module_fullname or if the module_fullname is not a 'OF version'
                specific module.
            new_module_fullname (str): The new module fullname, with the
                replaced version, on the format "pyof.v0x01.common.header".
        """
        try:
            module_version = MetaStruct.get_pyof_mod_version(module_fullname)
            new_mod = module_fullname.replace(module_version, version)
            #: Loads the module
            new_mod = importlib.import_module(new_mod)
            #: Get the class from the loaded module
            new_cls = getattr(new_mod, cls_name)
            return new_cls
        except Exception as message:
            return None

    @staticmethod
    def update_gtype(obj, new_version):
        """Update a GenericType type object.

        This method evaluates the object `enum_ref` and `value` and update them
        if necessary. This means that the `enum_ref` content, if there is one,
        will be updated (for the `new_version` version) and the `value` will
        also be updated to be in compliance with the new enum, if needed.

        Args:
            obj (:class:GenericType): An instance of GenericType.
            new_version (str): String on the format `v0x0?` with the required
                openflow version.

        Return:
            obj (:class:GenericType): A new instance of the same GenericType
                but with the `enum_ref` and `value` updated to the
                `new_version`.
        """
        new_obj = deepcopy(obj)
        if isinstance(obj, GenericType) and new_version is not None:
            old_enum = obj.enum_ref
            #: if we use '.value' here we will get only the str representation
            #: of the value, but we want the full value object. This is
            #: specially important if the value is a instance of Enum or a
            #: Bitmask object.
            old_value = obj._value

            if old_enum is None:
                new_obj._value = old_value
            elif old_enum.__name__ == 'PyofVersion':
                new_obj.enum_ref = old_enum
                new_obj._value = old_enum[new_version]
            else:
                #: get the newer version of the enum_ref and set it.
                new_enum = MetaStruct.update_obj_version(old_enum, new_version)
                new_obj.enum_ref = new_enum
                if old_value is not None:
                    new_obj._value = new_enum[old_value.name]
        return new_obj

    @staticmethod
    def update_enum_or_bitmask(cls, new_version):
        """Return a the Enum and/or BitMask on the `new_version`.

        Args:
            cls (:class:`enum.Enum` or :class:`GenericBitMask`): A reference
                for a class of type :class:`Enum` or :class:`GenericBitMask`.
            new_version (str): String on the format `v0x0?` with the required
                openflow version.
        Return:
            new_cls (class): The updated version of the enum class or the
                bitmask class.
        """
        new_cls = MetaStruct.get_updated_pyof_class(cls.__name__,
                                                    cls.__module__,
                                                    new_version)
        return new_cls

    @staticmethod
    def update_gstruct(old_struct, new_version):
        """Return an updated instance of GenericStruct.

        The method receives an instance of a GenericStruct (or GenericMessage),
        and update it the the `new_version` version of it. Besides only
        instantiating the newer version, each attribute of the struct will be
        evaluated to assure that its class attributes predefined values will
        also be inherited/copied to the new instance.
        We have to keep in mind that the class attributes of a generic struct
        are **instances** of other generic structs or generic types. Thus, it
        is not enought to just get a new instance of that attribute class, we
        also have to check for any contents passed to the attribute init.

        For example, the Header class does not contain a default value for the
        message_type attribute, so, its default is None. But when we define a
        new Message (:class:`GenericMessage`), we define the message_type of
        that Message class. So, when we are doing our update here of the header
        attribute of the Message class to a newer version, we need to set the
        `message_type` value on the newer class.

        This is not a trivial method, and the understandment of it may take
        some time. Do not edit anything if you are not absolutely sure about
        what you are doing.

        Inside this method other two methods were also defined, just to make
        the code a little bit more containerized.

        Args:
            old_struct (:class:`GenericStruct` or :class:`GenericMessage`):
                This method will receive an instance of :class:`GenericStruct`
                or :class:`GenericMessage`. This instance is the class
                attribute of some other class (eg: header instance for a
                Message).
            new_version (str): String on the format `v0x0?` with the required
                openflow version.
        Return:
            new_struct (:class:`GenericStruct` or :class:`GenericMessage`): The
                updated version of the given struct, with its attributes also
                updated and the attributes values inherited (and updated).
        """
        cls = type(old_struct)
        cls_name = cls.__name__
        cls_mod = cls.__module__
        new_cls = MetaStruct.get_updated_pyof_class(cls_name, cls_mod,
                                                    new_version)
        new_struct = new_cls()

        update_genstruct_attrs(old_struct, new_struct)

        return new_struct

    @staticmethod
    def update_obj_version(obj, new_version):
        """Return a class atrribute on a different pyof version.

        This method receives the class attribute (object) and an openflow
        version.

        A newer version of this attribute will be returned, and, since it is an
        instance of some class that serves as class attribute, it may have some
        predefined values (on the instance). In such cases, we will also get
        those predefined values and set their updated versions, if any, on the
        returned object.

        The work of this method consider some different cases of obj types:
        1) Enum and GenericBitMask: They are used on enum_refs and are
             always used as classes, never as instances.
        2) GenericTypes objects: that may or may not have a preset _value
             and enum_ref.
        3) TypeLists: Despite the fact that they inherit from GenericStruct,
             they have a _pyof_class attribute that needs to be checked and,
             if needed, updated.
        4) GenericStruct objects: we have to get the correct version of the
             struct. The update of the struct attributes are expected to be
             done by recursion.

        Example:
              >> from pyof.v0x01.common.header import Hello
              >> msg = Hello()
              >> obj = msg.header
              >> obj
              <pyof.v0x01.common.header.Header at 0x...>
              >> obj.version
              PyofVersion.v0x01
              >> obj.message_type
              <Type.OFPT_HELLO: 0>
              >> type(obj).message_type.enum_ref.__module__)
              pyof.v0x01.common.header
              >> new_version = 'v0x02'
              >> new_obj = MetaStruct.update_obj_version(obj, new_version)
              >> new_obj
              <pyof.v0x02.common.header.Header at 0x...>
              >> new_obj.version
              PyofVersion.v0x02
              >> new_obj.message_type
              <Type.OFPT_HELLO: 0>
              >> type(new_obj).message_type.enum_ref.__module__)
              pyof.v0x02.common.header

        Args:
            obj (object): the class attribute itself (an instance).
            new_version (string): the pyof version in which you want the object
                'obj'.

        Return:
            obj: An updated instance of the passed class attribute.
        """
        #: If the module does not starts with 'pyof.', then this is not an
        #: object defined inside the pyof scope, so we won't do anything with
        #: it, as much as if no 'new_version' is passed or the obj is None.
        #: So we just return a copy of the object.
        if obj is None or new_version is None:
            return copy(obj)
        elif inspect.isclass(obj):
            if not obj.__module__.startswith('pyof.'):
                return copy(obj)
        elif not type(obj).__module__.startswith('pyof.'):
            return copy(obj)

        #: Update the object based on some cases.
        if inspect.isclass(obj) and issubclass(obj, Enum):
            #: This came from an enum_ref
            new_obj = MetaStruct.update_enum_or_bitmask(obj, new_version)
        elif inspect.isclass(obj) and issubclass(obj, GenericBitMask):
            #: This came from an enum_ref
            new_obj = MetaStruct.update_enum_or_bitmask(obj, new_version)
        elif isinstance(obj, GenericType):
            new_obj = MetaStruct.update_gtype(obj, new_version)
        elif type(obj).__name__ == 'FixedTypeList':
            new_obj = MetaStruct.update_fixedTypeList(obj, new_version)
        else:
            new_obj = MetaStruct.update_gstruct(obj, new_version)

        return new_obj


class GenericStruct(object, metaclass=MetaStruct):
    """Class inherited by all OpenFlow structs.

    If you need to insert a method that will be used by all structs, this is
    the place to code it.

    .. note:: A struct on this library's context is like a struct in C. It
              has a list of attributes and theses attributes can be structs,
              too.
    """

    def __init__(self):
        """Contructor takes no argument and stores attributes' deep copies."""
        for name, value in self._get_class_attributes():
            setattr(self, name, deepcopy(value))

    def __eq__(self, other):
        """Check whether two structures have the same structure and values.

        Compare the binary representation of structs to decide whether they
        are equal or not.

        Args:
            other (GenericStruct): The struct to be compared with.
        """
        return self.pack() == other.pack()

    @staticmethod
    def _attr_fits_into_class(attr, cls):
        if not isinstance(attr, cls):
            try:
                struct.pack(cls._fmt, attr)  # pylint: disable=protected-access
            except struct.error:
                return False
        return True

    @staticmethod
    def _is_pyof_attribute(obj):
        """Return True if the object is a kytos attribute.

        To be a kytos attribute the item must be an instance of either
        GenericType or GenericStruct.

        returns:
            True: if the obj is a kytos attribute
            False: if the obj is not a kytos attribute
        """
        return isinstance(obj, GenericType) or isinstance(obj, GenericStruct)

    def _validate_attributes_type(self):
        """Validate the type of each attribute."""
        for _attr, _class in self._get_attributes():
            if isinstance(_attr, _class):
                return True
            elif issubclass(_class, GenericType):
                if GenericStruct._attr_fits_into_class(_attr, _class):
                    return True
            elif not isinstance(_attr, _class):
                return False
        return True

    @classmethod
    def _get_class_attributes(cls):
        """Return a generator for class attributes' names and value.

        This method strict relies on the PEP 520 (Preserving Class Attribute
        Definition Order), implemented on Python 3.6. So, if this behaviour
        changes this whole lib can loose its functionality (since the
        attributes order are a strong requirement.) For the same reason, this
        lib will not work on python versions earlier than 3.6.

        .. code-block:: python3

            for _name, _value in self._get_class_attributes():
                print("attribute name: {}".format(_name))
                print("attribute type: {}".format(_value))

        returns:
            generator: tuples with attribute name and value.
        """
        #: see this method docstring for a important notice about the use of
        #: cls.__dict__
        for name, value in cls.__dict__.items():
            # gets only our (kytos) attributes. this ignores methods, dunder
            # methods and attributes, and common python type attributes.
            if GenericStruct._is_pyof_attribute(value):
                yield (name, value)

    def _get_instance_attributes(self):
        """Return a generator for instance attributes' name and value.

        .. code-block:: python3

            for _name, _value in self._get_instance_attributes():
                print("attribute name: {}".format(_name))
                print("attribute value: {}".format(_value))

        returns:
            generator: tuples with attribute name and value.
        """
        for name, value in self.__dict__.items():
            if name in map((lambda x: x[0]), self._get_class_attributes()):
                yield (name, value)

    def _get_attributes(self):
        """Return a generator for instance and class attribute.

        .. code-block:: python3

            for instance_attribute, class_attribute in self._get_attributes():
                print("Instance Attribute: {}".format(instance_attribute))
                print("Class Attribute: {}".format(class_attribute))

        Returns:
            generator: Tuples with instance attribute and class attribute
        """
        return map((lambda i, c: (i[1], c[1])),
                   self._get_instance_attributes(),
                   self._get_class_attributes())

    def _unpack_attribute(self, name, obj, buff, begin):
        attribute = deepcopy(obj)
        setattr(self, name, attribute)
        if len(buff) == 0:
            size = 0
        else:
            try:
                attribute.unpack(buff, begin)
                size = attribute.get_size()
            except UnpackException as e:
                child_cls = type(self).__name__
                msg = '{}.{}; {}'.format(child_cls, name, e)
                raise UnpackException(msg)
        return size

    def get_size(self, value=None):
        """Calculate the total struct size in bytes.

        For each struct attribute, sum the result of each one's ``get_size()``
        method.

        Args:
            value: In structs, the user can assign other value instead of a
                class' instance.

        Returns:
            int: Total number of bytes used by the struct.

        Raises:
            Exception: If the struct is not valid.
        """
        if value is None:
            return sum(cls_val.get_size(obj_val) for obj_val, cls_val in
                       self._get_attributes())
        elif isinstance(value, type(self)):
            return value.get_size()
        else:
            msg = "{} is not an instance of {}".format(value,
                                                       type(self).__name__)
            raise PackException(msg)

    def pack(self, value=None):
        """Pack the struct in a binary representation.

        Iterate over the class attributes, according to the
        order of definition, and then convert each attribute to its byte
        representation using its own ``pack`` method.

        Returns:
            bytes: Binary representation of the struct object.

        Raises:
            :exc:`~.exceptions.ValidationError`: If validation fails.
        """
        if value is None:
            if not self.is_valid():
                error_msg = "Error on validation prior to pack() on class "
                error_msg += "{}.".format(type(self).__name__)
                raise ValidationError(error_msg)
            else:
                message = b''
                # pylint: disable=no-member
                for instance_attr, class_attr in self._get_attributes():
                    message += class_attr.pack(instance_attr)
                return message
        elif isinstance(value, type(self)):
            return value.pack()
        else:
            msg = "{} is not an instance of {}".format(value,
                                                       type(self).__name__)
            raise PackException(msg)

    def unpack(self, buff, offset=0):
        """Unpack a binary struct into this object's attributes.

        Update this object attributes based on the unpacked values of *buff*.
        It is an inplace method and it receives the binary data of the struct.

        Args:
            buff (bytes): Binary data package to be unpacked.
            offset (int): Where to begin unpacking.
        """
        begin = offset
        for name, value in self._get_class_attributes():
            size = self._unpack_attribute(name, value, buff, begin)
            begin += size

    def is_valid(self):
        """Check whether all struct attributes in are valid.

        This method will check whether all struct attributes have a proper
        value according to the OpenFlow specification. For instance, if you
        have a struct with an attribute of type :class:`UBInt8()`
        and you assign a string value to it, this method will return False.

        Returns:
            bool: Whether the struct is valid.
        """
        return True
        # pylint: disable=unreachable
        return self._validate_attributes_type()


class GenericMessage(GenericStruct):
    """Base class that is the foundation for all OpenFlow messages.

    To add a method that will be used by all messages, write it here.

    .. note:: A Message on this library context is like a Struct but has a
              also a :attr:`header` attribute.
    """

    header = None

    def __init__(self, xid=None):
        """Initialize header's xid."""
        super().__init__()
        self.header.xid = randint(0, MAXID) if xid is None else xid

    def __init_subclass__(cls, **kwargs):
        if cls.header is None or cls.header.__class__.__name__ != 'Header':
            msg = "The header attribute must be implemented on the class "
            msg += cls.__name__ + "."
            raise NotImplementedError(msg)
        super().__init_subclass__(**kwargs)

    def _validate_message_length(self):
        return self.header.length == self.get_size()

    def is_valid(self):
        """Check whether a message is valid or not.

        This method will validate the Message content. During the validation
        process, we check whether the attributes' values are valid according to
        the OpenFlow specification. Call this method if you want to verify
        whether the message is ready to pack.

        Returns:
            bool: Whether the message is valid.
        """
        return True
        # pylint: disable=unreachable
        return super().is_valid() and self._validate_message_length()

    def pack(self, value=None):
        """Pack the message into a binary data.

        One of the basic operations on a Message is the pack operation. During
        the packing process, we convert all message attributes to binary
        format.

        Since that this is usually used before sending the message to a switch,
        here we also call :meth:`update_header_length`.

        .. seealso:: This method call its parent's :meth:`GenericStruct.pack`
            after :meth:`update_header_length`.

        Returns:
            bytes: A binary data thats represents the Message.

        Raises:
            Exception: If there are validation errors.
        """
        if value is None:
            self.update_header_length()
            return super().pack()
        elif isinstance(value, type(self)):
            return value.pack()
        else:
            msg = "{} is not an instance of {}".format(value,
                                                       type(self).__name__)
            raise PackException(msg)

    def unpack(self, buff, offset=0):
        """Unpack a binary message into this object's attributes.

        Unpack the binary value *buff* and update this object attributes based
        on the results. It is an inplace method and it receives the binary data
        of the message **without the header**.

        Args:
            buff (bytes): Binary data package to be unpacked, without the
                header.
            offset (int): Where to begin unpacking.
        """
        begin = offset
        for name, value in self._get_class_attributes():
            if type(value).__name__ != "Header":
                size = self._unpack_attribute(name, value, buff, begin)
                begin += size

    def update_header_length(self):
        """Update the header length attribute based on current message size.

        When sending an OpenFlow message we need to inform the message length
        on the header. This is mandatory.
        """
        self.header.length = self.get_size()
