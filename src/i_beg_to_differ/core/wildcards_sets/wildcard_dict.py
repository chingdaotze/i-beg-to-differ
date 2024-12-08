from typing import Dict

from .wildcard_field import WildcardField
from .wildcard_sets import WildcardSets


class WildcardDict:

    values: Dict[WildcardField, WildcardField]
    wildcard_sets: WildcardSets

    def __init__(
        self,
        values: Dict[str, str] | None = None,
        wildcard_sets: WildcardSets | None = None,
    ):
        self.wildcard_sets = wildcard_sets

        if values is None:
            values = {}

        self.values = {
            WildcardField(
                base_value=key,
                wildcard_sets=self.wildcard_sets,
            ): WildcardField(
                base_value=value,
                wildcard_sets=self.wildcard_sets,
            )
            for key, value in values.items()
        }

    def to_wildcard_field(
        self,
        base_value: str,
    ) -> WildcardField:

        return WildcardField(
            base_value=base_value,
            wildcard_sets=self.wildcard_sets,
        )

    def __setitem__(
        self,
        key: str,
        value: str,
    ) -> None:

        self.values[
            self.to_wildcard_field(
                base_value=key,
            )
        ] = self.to_wildcard_field(
            base_value=value,
        )

    def __getitem__(
        self,
        item: str,
    ) -> str:

        return str(
            self.values[
                self.to_wildcard_field(
                    base_value=item,
                )
            ],
        )

    def __delitem__(
        self,
        key: str,
    ) -> None:

        del self.values[
            self.to_wildcard_field(
                base_value=key,
            )
        ]
