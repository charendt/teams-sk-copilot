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
    features: List[Union[FixedInterest, Fees, VariableInterest]] = Field(..., discriminator='type')
