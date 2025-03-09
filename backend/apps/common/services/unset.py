__all__ = ['UNSET', 'UnsetType']


class UnsetType:
    """Специальный объект для обозначения не заполненного значения."""

    def __repr__(self) -> str:
        return 'UNSET'


UNSET = UnsetType()
