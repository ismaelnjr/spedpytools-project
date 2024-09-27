from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class ArquivoDigitalSchema:
    class Meta:
        name = "arquivo_digital_schema"

    bloco: List["ArquivoDigitalSchema.Bloco"] = field(
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
    class Bloco:
        registro: List["ArquivoDigitalSchema.Bloco.Registro"] = field(
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

        @dataclass
        class Registro:
            campo: List["ArquivoDigitalSchema.Bloco.Registro.Campo"] = field(
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
            class Campo:
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
