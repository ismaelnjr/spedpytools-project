from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class HierarquicalSchema:
    class Meta:
        name = "hierarquical_schema"

    table_list: List["HierarquicalSchema.TableList"] = field(
        default_factory=list,
        metadata={
            "type": "Element",
            "min_occurs": 1,
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
    clazz_path: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )

    @dataclass
    class TableList:
        table: List["HierarquicalSchema.TableList.Table"] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "min_occurs": 1,
            },
        )
        group_id: Optional[str] = field(
            default=None,
            metadata={
                "type": "Attribute",
                "required": True,
            },
        )
        description: Optional[str] = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )

        @dataclass
        class Table:
            column: List["HierarquicalSchema.TableList.Table.Column"] = field(
                default_factory=list,
                metadata={
                    "type": "Element",
                    "min_occurs": 1,
                },
            )
            id: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                    "required": True,
                },
            )
            description: Optional[str] = field(
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
            exclude: bool = field(
                default=False,
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
                        "required": True,
                    },
                )
