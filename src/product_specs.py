from typing import Union, List, Literal
from pydantic import Field
from semantic_kernel.kernel_pydantic import KernelBaseModel

class Feature(KernelBaseModel):
    type: str   # type discriminator field
    description: str

    class Config:
        # Enable discriminated unions if needed
        fields = {'type': 'type'}
        discriminator = 'type'

class FixedInterest(Feature):
    type: Literal["FixedInterest"] = "FixedInterest"  # discriminator value
    value: float

class Fees(Feature):
    type: Literal["Fees"] = "Fees"  # discriminator value
    value: float
    frequency: str

class VariableInterest(Feature):
    type: Literal["VariableInterest"] = "VariableInterest"  # discriminator value
    value: float

class Product(KernelBaseModel):
    name: str
    currency: str
    features: List[Union[FixedInterest, Fees, VariableInterest]]

    class Config:
        json_schema_extra = {
            "features": {
                "discriminator": "type"  # Ensure proper JSON serialization
            }
        }


# Sample product
product = Product(
    name="Savings Account",
    currency="USD",
    features=[
        FixedInterest(description="Fixed rate", value=5.0),
        Fees(description="Monthly maintenance fee", value=10.0, frequency="monthly"),
        VariableInterest(description="Floating rate", value=3.5),
    ]
)

# Serialization
print(product.model_dump_json(indent=2))