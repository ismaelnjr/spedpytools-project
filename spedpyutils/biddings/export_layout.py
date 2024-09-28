from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class ExportLayout:
    class Meta:
        name = "export_layout"

    data_source_config: Optional["ExportLayout.DataSourceConfig"] = field(
        default=None,
        metadata={
            "type": "Element",
            "required": True,
        },
    )
    tabs: Optional["ExportLayout.Tabs"] = field(
        default=None,
        metadata={
            "type": "Element",
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
    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )

    @dataclass
    class DataSourceConfig:
        data_source: List["ExportLayout.DataSourceConfig.DataSource"] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "min_occurs": 1,
            },
        )
        clazz_path: Optional[str] = field(
            default=None,
            metadata={
                "type": "Attribute",
                "required": True,
            },
        )

        @dataclass
        class DataSource:
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

    @dataclass
    class Tabs:
        tab: List["ExportLayout.Tabs.Tab"] = field(
            default_factory=list,
            metadata={
                "type": "Element",
                "min_occurs": 1,
            },
        )

        @dataclass
        class Tab:
            column: List["ExportLayout.Tabs.Tab.Column"] = field(
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
                    "required": True,
                },
            )
            data_source: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                    "required": True,
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
