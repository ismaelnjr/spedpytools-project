from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class HierarquicalSchema:
    class Meta:
        name = "hierarquical-schema"

    tables_list: Optional["HierarquicalSchema.TablesList"] = field(
        default=None,
        metadata={
            "name": "tables-list",
            "type": "Element",
            "required": True,
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )

    @dataclass
    class TablesList:
        table: List["HierarquicalSchema.TablesList.Table"] = field(
            default_factory=list,
            metadata={
                "type": "Element",
            },
        )

        @dataclass
        class Table:
            column: List["HierarquicalSchema.TablesList.Table.Column"] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                },
            )
            id: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                    "required": True,
                },
            )
            name: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                },
            )
            index: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                },
            )
            parent: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                },
            )

            @dataclass
            class Column:
                value: str = field(
                    default="",
                    metadata={
                        "required": True,
                    },
                )
                name: Optional[str] = field(
                    default=None,
                    metadata={
                        "type": "Attribute",
                    },
                )
                type_value: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "type",
                        "type": "Attribute",
                    },
                )
                dateformat: Optional[str] = field(
                    default=None,
                    metadata={
                        "type": "Attribute",
                    },
                )
                key: Optional[str] = field(
                    default=None,
                    metadata={
                        "type": "Attribute",
                    },
                )
