import datetime
from decimal import Decimal
from typing import Any, List, Type, TYPE_CHECKING

from .exceptions import ValidationError
from .utils import (
    validate_email,
    validate_ncf,
    validate_phone_number,
    validate_rnc,
    validate_unit_measure,
)
from .config import (
    NCF_B,
    NCF_E,
    UNIT_MEASURES,
)


if TYPE_CHECKING:
    from .forms import Form


class NOT_IMPLEMENTED:
    pass


class Field:
    # Función que se utilizará para en `parse_value(value)`.
    parser = None

    def __init__(
        self,
        dgii_name: str | None = None,
        null: bool = True,
        choices: list | tuple | dict = None,
        validators: list = None,
        default: Any = NOT_IMPLEMENTED,
        editable: bool = True,
        help_text: str = None,
    ):
        self.dgii_name = str(dgii_name) if dgii_name else None
        self.null = bool(null)
        self.choices = self.get_choices(choices) if choices else None
        self.validators = list(validators or [])
        self.default = default
        self.editable = editable
        self.help_text = help_text or ''
        # Instancia del formulario
        # (se asigna al procesar el campo en el método __init__ del formulario)
        self.__parent = None

    def __str__(self):
        return self.dgii_name or super().__str__()

    @property
    def parent(self):
        return self.__parent

    @parent.setter
    def parent(self, form: 'Form'):
        if not getattr(form, 'is_form', None):
            raise TypeError(
                f'El argumento `form` debe ser una instancia de `Form` no un {type(form)}.'
            )
        self.__parent = form

    @property
    def value(self):
        raise NotImplementedError()

    def get_default(self, form):
        if self.default == NOT_IMPLEMENTED:
            raise NotImplementedError(
                'No se indicó un valor para el atributo "default" para el '
                f'campo {self} en {form}.'
            )
        # Obtenemos un valor de otro atributo del formulario.
        if isinstance(self.default, Attr):
            return getattr(form, self.default.name)
        # Intentamos tratar el valor default como un método.
        if callable(self.default):
            try:
                return self.default(form)
            except:
                return self.default()
        # El valor es literal, lo devolvemos tal cual.
        return self.default

    def get_choices(self, choices):
        return list(choices)

    def parse_value(self, form: 'Form', name: str, value: Any):
        return self.parser(value) if self.parser else value

    def validate(self, form: 'Form', name: str, value: Any):
        if (value is None) or (value == ''):
            value = None
            if self.null is False:
                raise ValidationError(
                    f'El valor de {name} en {form} no puede ser nulo.'
                )
        else:
            value = self.parse_value(form, name, value)
            for validator in self.validators:
                value = self.__apply_validator(form, name, value, validator)
        return value

    def __apply_validator(self, form, name: str, value, validator: Any):
        args = []
        if isinstance(validator, (list, tuple)):
            validator, validator_args = validator
            for validator_arg in validator_args:
                if isinstance(validator_arg, Attr):
                    args.append(getattr(form, validator_arg.name))
                else:
                    args.append(validator_arg)
        return validator(value, *args)


class StrField(Field):
    """Campo que representa una cadena de texto."""

    parser = str

    def __init__(
        self,
        dgii_name: str | None = None,
        null: bool = True,
        choices: list | tuple | dict = None,
        validators: list = None,
        min_length: int | None = None,
        max_length: int | None = None,
        default: Any = NOT_IMPLEMENTED,
        editable: bool = True,
        help_text: str = None,
    ):
        super().__init__(
            dgii_name=dgii_name,
            null=null,
            choices=choices,
            validators=validators,
            default=default,
            editable=editable,
            help_text=help_text,
        )
        self.min_length = int(min_length) if min_length else None
        self.max_length = int(max_length) if max_length else None

    def validate(self, form: 'Form', name: str, value: Any):
        value = super().validate(form, name, value)
        if value is not None:
            if self.min_length is not None and len(value) < self.min_length:
                raise ValidationError(f'{form} {name} debe tener al menos {self.min_length} caracteres.')
            if self.max_length is not None and len(value) > self.max_length:
                raise ValidationError(f'{form} {name} debe tener como máximo {self.max_length} caracteres.')
        return value


class EmailField(StrField):
    """Campo que representa un email."""

    def __init__(
        self,
        dgii_name: str | None = None,
        null: bool = True,
        max_length: int = 80,
        choices: list | tuple | dict = None,
        validators: list = None,
        default: Any = NOT_IMPLEMENTED,
        editable: bool = True,
        help_text: str = None,
    ):
        super().__init__(
            dgii_name=dgii_name,
            null=null,
            choices=choices,
            max_length=max_length,
            validators=validators,
            default=default,
            editable=editable,
            help_text=help_text,
        )

    def validate(self, form: 'Form', name: str, value: Any):
        value = super().validate(form, name, value)
        if value is not None:
            value = validate_email(value)
        return value


class PhoneField(StrField):
    """Campo que representa un número telefónico."""

    def __init__(
        self,
        dgii_name: str | None = None,
        null: bool = True,
        max_length: int = 12,
        choices: list | tuple | dict = None,
        validators: list = None,
        default: Any = NOT_IMPLEMENTED,
        editable: bool = True,
        help_text: str = None,
    ):
        super().__init__(
            dgii_name=dgii_name,
            null=null,
            choices=choices,
            max_length=max_length,
            validators=validators,
            default=default,
            editable=editable,
            help_text=help_text,
        )

    def validate(self, form: 'Form', name: str, value: Any):
        value = super().validate(form, name, value)
        if value is not None:
            value = validate_phone_number(value)
        return value


class IntField(Field):
    """Campo que representa un número entero."""

    parser = int

    def __init__(
        self,
        dgii_name: str | None = None,
        null: bool = True,
        choices: list | tuple | dict = None,
        validators: list = None,
        min_value: int | None = 0,
        max_value: int | None = 20,
        default: Any = NOT_IMPLEMENTED,
        editable: bool = True,
        help_text: str = None,
    ):
        super().__init__(
            dgii_name=dgii_name,
            null=null,
            choices=choices,
            validators=validators,
            default=default,
            editable=editable,
            help_text=help_text,
        )
        self.min_value = int(min_value) if min_value else None
        self.max_value = int(max_value) if max_value else None

    def validate(self, form: 'Form', name: str, value: Any):
        value = super().validate(form, name, value)
        if value is not None:
            if self.min_value is not None and value < self.min_value:
                raise ValidationError(f"{name} debe ser mayor o igual a {self.min_value}.")
            if self.max_value is not None and value > self.max_value:
                raise ValidationError(f"{name} debe ser menor o igual a {self.max_value}.")
        return value


class RNCField(IntField):
    """Campo que representa un RNC."""

    def __init__(
        self,
        dgii_name: str | None = None,
        null: bool = True,
        validators: list = None,
        default: Any = NOT_IMPLEMENTED,
        editable: bool = True,
        help_text: str = None,
    ):
        super().__init__(
            dgii_name=dgii_name,
            null=null,
            validators=validators,
            default=default,
            editable=editable,
            help_text=help_text,
        )
        self.max_value = 99999999999

    def validate(self, form: 'Form', name: str, value: int):
        if value is not None:
            value = validate_rnc(value)
        value = super().validate(form, name, value)
        return value


class NCFField(StrField):
    """Campo que representa un Número de Comprobante Fiscal (NCF)."""

    def __init__(
        self,
        dgii_name: str | None = None,
        serie: str = NCF_E,
        null: bool = True,
        validators: list = None,
        default: Any = NOT_IMPLEMENTED,
        editable: bool = True,
        help_text: str = None,
    ):
        super().__init__(
            dgii_name=dgii_name,
            null=null,
            validators=validators,
            default=default,
            editable=editable,
            help_text=help_text,
        )

        self.serie = serie

        if self.serie == NCF_E:
            self.min_length = 13
            self.max_length = 13
        elif self.serie == NCF_B:
            self.min_length = 11
            self.max_length = 11
        else:
            self.min_length = 11
            self.max_length = 13

    def validate(self, form: 'Form', name: str, value: str):
        value = super().validate(form, name, value)
        if value is not None:
            value = validate_ncf(value, specific_serie=self.serie)
        return value


class DecimalField(IntField):
    """Campo que representa un número decimal."""

    parser = Decimal

    def __init__(
        self,
        dgii_name: str | None = None,
        null: bool = True,
        validators: list = None,
        max_digits: int = 16,
        decimal_places: int = 2,
        min_value: Decimal | None = 0,
        max_value: Decimal | None = None,
        default: Any = NOT_IMPLEMENTED,
        editable: bool = True,
        help_text: str = None,
    ):
        super().__init__(
            dgii_name=dgii_name,
            null=null,
            validators=validators,
            default=default,
            editable=editable,
            help_text=help_text,
        )

        self.max_digits = int(max_digits) if max_digits else None
        self.min_value = Decimal(min_value) if min_value else None
        self.decimal_places = int(decimal_places) if decimal_places else None

        if max_value:
            self.max_value = Decimal(max_value)
        elif self.max_digits:
            str_num = '9' * (self.max_digits - self.decimal_places or 0)
            if self.decimal_places:
                str_num += ('.' + '9'*self.decimal_places)
            self.max_value = Decimal(str_num)
        else:
            self.max_value = None

    def validate(self, form: 'Form', name: str, value: Decimal):
        value = super().validate(form, name, value)
        if value is not None:
            if self.decimal_places:
                value = round(value, self.decimal_places)
            if self.min_value is not None and value < self.min_value:
                raise ValidationError(f"{name} debe ser mayor o igual a {self.min_value}.")
            if self.max_value is not None and value > self.max_value:
                raise ValidationError(f"{name} debe ser menor o igual a {self.max_value}.")
        return value


class DateField(Field):
    """Campo que representa una fecha."""

    parser = datetime.date
    _format = '%Y-%m-%d'

    def __init__(
        self,
        dgii_name: str | None = None,
        null: bool = True,
        choices: list | tuple | dict = None,
        validators: list = None,
        default: Any = NOT_IMPLEMENTED,
        editable: bool = True,
        help_text: str = None,
    ):
        super().__init__(
            dgii_name=dgii_name,
            null=null,
            choices=choices,
            validators=validators,
            default=default,
            editable=editable,
            help_text=help_text,
        )

    def parse_value(self, form: 'Form', name: str, value: datetime.date):
        if isinstance(value, datetime.date):
            pass
        elif isinstance(value, datetime.datetime):
            value = value.date()
        elif isinstance(value, str):
            try:
                value = datetime.datetime.strptime(value, self._format).date()
            except ValidationError as e:
                raise ValidationError(e)
        else:
            raise ValidationError('El valor "%s" no es una fecha.')
        return value


class UnitMeasureField(IntField):
    """Campo que representa una unidad de medida permitida."""

    def __init__(
        self,
        dgii_name: str | None = None,
        null: bool = True,
        default: Any = NOT_IMPLEMENTED,
        editable: bool = True,
        help_text: str = None,
    ):
        self.min_value = 1
        self.max_value = 99
        super().__init__(
            dgii_name=dgii_name,
            null=null,
            choices=UNIT_MEASURES,
            default=default,
            editable=editable,
            help_text=help_text,
        )

    def validate(self, form: 'Form', name: str, value: int):
        value = super().validate(form, name, value)
        if value is not None:
            value = validate_unit_measure(value)
        return value


class FormField(Field):
    """
    Un campo para permitir indicar un formulario como atributo de otro formulario.
    """

    def __init__(
        self,
        dgii_name: str | None,
        form_class: Type['Form'],
        null: bool = True,
        validators: list = None,
        default: Any = NOT_IMPLEMENTED,
        editable: bool = True,
        help_text: str = None,
    ):
        """
        Campo para permitir indicar un formulario como atributo de otro formulario.

        Args:
        ----------------
        - dgii_name (str | None): El nombre del campo en el formato DGII.
        - null (bool): Indica si el campo puede tener valor nulo.
        - validators (list): Una lista de validadores para aplicar al campo.
        - form_class (Type[Field]): La clase del formulario que se utilizará como atributo.
        - default (Any): El valor por defecto del campo. `NOT_IMPLEMENTED` si no se proporciona.
        - editable (bool): Indica si el campo es editable.

        Ejemplo de uso:
        ----------------
        ```
        form = FormField(
            'Other',
            form_class=Form,
        )
        ```
        """
        self.form_class = form_class
        super().__init__(
            dgii_name=dgii_name,
            null=null,
            validators=validators,
            default=default,
            editable=editable,
            help_text=help_text,
        )

    def parse_value(self, form: 'Form', name: str, value: 'Form'):
        if not isinstance(value, self.form_class):
            raise ValidationError(
                f'El form {value} en {self} debe ser un {self.form_class}.'
            )
        return value


class ListField(Field):
    """Campo que representa un listado de valores."""

    parser = list

    def __init__(
        self,
        dgii_name: str | None = None,
        null: bool = True,
        choices: list | tuple | dict = None,
        validators: list = None,
        field_class: Type[Field] = StrField,
        min_length: int | None = None,
        max_length: int | None = None,
        help_text: str = None,
    ):
        super().__init__(
            dgii_name=dgii_name,
            null=null,
            choices=choices,
            validators=validators,
            help_text=help_text,
        )
        self.field_class = field_class
        self.min_length = int(min_length) if min_length else None
        self.max_length = int(max_length) if max_length else None

    def validate(self, form: 'Form', name: str, value: List):
        validate_values = []
        for _value in value:
            field = self.field_class()
            _value = field.validate(form, name, _value)

            # Solo se incluyen los items con valores
            if value is not None:
                validate_values.append(_value)

        if self.min_length is not None and len(validate_values) < self.min_length:
            raise ValidationError(f"{form}.{name}. debe tener al menos {self.min_length} valores.")
        if self.max_length is not None and len(validate_values) > self.max_length:
            raise ValidationError(f"{form}.{name}. debe tener como máximo {self.max_length} valores.")

        return validate_values


class ListFormField(Field):
    """Campo que representa un listado de formularios."""

    parser = list

    def __init__(
        self,
        dgii_name,
        form_class: Type['Form'],
        max_length: int,
        min_length: int | None = None,
        null: bool = True,
        choices: list | tuple | dict = None,
        validators: list = None,
        help_text: str = None,
    ):
        super().__init__(
            dgii_name=dgii_name,
            null=null,
            choices=choices,
            validators=validators,
            help_text=help_text,
        )
        self.form_class = form_class
        self.min_length = int(min_length) if min_length else None
        self.max_length = int(max_length) if max_length else None

    def parse_value(self, form: 'Form', name: str, value: List['Form']):
        if not isinstance(value, (list, tuple)):
            raise ValidationError(f'{form}.{name}. El valor "{value}" debe ser un listado de valores.')
        for form_instance in value:
            if not isinstance(form_instance, self.form_class):
                raise ValidationError(f'{form}.{name}. El form {form_instance} en {self} debe ser un {self.form_class}.')
        return value

    def validate(self, form: 'Form', name: str, value: List['Form']):
        value = super().validate(form, name, value)
        if value is not None:
            if self.min_length is not None and len(value) < self.min_length:
                raise ValidationError(f"{form}.{name}. debe tener al menos {self.min_length} objetos.")
            if self.max_length is not None and len(value) > self.max_length:
                raise ValidationError(f"{form}.{name}. debe tener como máximo {self.max_length} objetos.")
        return value


class Attr:
    """
    Representa el nombre de un atributo de formulario,
    cuyo valor se extraerá del formulario.
    """

    def __init__(self, name: str):
        """
        Args:
        ---------
        - name (str): Nombre del campo del formulario que se utilizará como:
            `getattr(form, name)`

        Ejemplos:
        ---------
        ```
        municipality = StrField(
            'Municipio',
            validators=[
                (validate_municipality, [Attr('province')]),
            ],
        )
        ```

        En el ejemplo anterior, se utiliza `Attr('province')` para acceder al
        attributo `province` en el formulario, cuando toque ejecutar ese validador
        `validate_municipality` y así pasarle como argumento el valor de `province`.

        Ejemplo: Si el valor de `province` es 10001 y el de `municipality` es
        80006, entonces cuando se ejecute el validador será así:
        `validate_municipality(80006, 10001)`
        """
        self.name = name

    def __repr__(self):
        return f'Attr({self.name})'