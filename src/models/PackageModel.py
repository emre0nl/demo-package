
from pydantic import Field, validator
from typing import List, Optional, Union, Literal
from sdks.novavision.src.base.model import Package, Image, Inputs, Configs, Outputs, Response, Request, Output, Input, Config

class InputImage2(Input):
    name: Literal["inputImage2"] = "inputImage2"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Image 2"

class InputImage(Input):
    name: Literal["inputImage"] = "inputImage"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Image"

class OutputImage2(Output):
    name: Literal["outputImage2"] = "outputImage2"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Image 2"

class OutputImage(Output):
    name: Literal["outputImage"] = "outputImage"
    value: Union[List[Image],Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"

    class Config:
        title = "Image"


class KeepSideFalse(Config):
    name: Literal["False"] = "False"
    value: Literal[False] = False
    type: Literal["bool"] = "bool"
    field: Literal["option"] = "option"

    class Config:
        title = "Disable"


class KeepSideTrue(Config):
    name: Literal["True"] = "True"
    value: Literal[True] = True
    type: Literal["bool"] = "bool"
    field: Literal["option"] = "option"

    class Config:
        title = "Enable"


class KeepSideBBox(Config):
    """
        Rotate image without catting off sides.
    """
    name: Literal["KeepSide"] = "KeepSide"
    value: Union[KeepSideTrue, KeepSideFalse]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"

    class Config:
        title = "Keep Sides"


class Degree(Config):
    """
        Positive angles specify counterclockwise rotation while negative angles indicate clockwise rotation.
    """
    name: Literal["Degree"] = "Degree"
    value: int = Field(ge=-359.0, le=359.0,default=0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    placeHolder: Literal["[-359, 359]"] = "[-359, 359]"

    class Config:
        title = "Angle"

class Angle90(Config):
    name: Literal["Angle90"] = "Angle90"
    value: Literal[90] = 90
    type: Literal["number"] = "number"
    field: Literal["option"] = "option"

    class Config:
        title = "90°"


class Angle180(Config):
    name: Literal["Angle180"] = "Angle180"
    value: Literal[180] = 180
    type: Literal["number"] = "number"
    field: Literal["option"] = "option"

    class Config:
        title = "180°"


class Angle270(Config):
    name: Literal["Angle270"] = "Angle270"
    value: Literal[270] = 270
    type: Literal["number"] = "number"
    field: Literal["option"] = "option"

    class Config:
        title = "270°"

class PresetAngle(Config):
    """
        Rotate image by a fixed angle.
    """
    name: Literal["PresetAngle"] = "PresetAngle"
    value: Union[Angle90, Angle180, Angle270]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"

    class Config:
        title = "Preset Angle"


class Scale(Config):
    """
        Scale factor applied while rotating.
    """
    name: Literal["Scale"] = "Scale"
    value: float = Field(gt=0, le=5, default=1.0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    placeHolder: Literal["(0, 5]"] = "(0, 5]"

    class Config:
        title = "Scale"

class RotatePreset(Config):
    name: Literal["Preset"] = "Preset"
    presetAngle: PresetAngle    
    scale: Scale                
    value: Literal["Preset"] = "Preset"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Preset"

class RotateManual(Config):
    name: Literal["Manual"] = "Manual"
    degree: Degree             
    keepSide: KeepSideBBox     
    value: Literal["Manual"] = "Manual"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Manual"

class RotateMode(Config):
    name: Literal["RotateMode"] = "RotateMode"
    value: Union[RotateManual, RotatePreset]
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Mode"

class SecondOutputs(Outputs):
    outputImage: OutputImage
    outputImage2: OutputImage2

class FirstOutputs(Outputs):
    outputImage: OutputImage
class SecondResponse(Response):
    outputs: SecondOutputs
class FirstResponse(Response):
    outputs: FirstOutputs

class SecondConfigs(Configs):
    rotateMode: RotateMode
class FirstConfigs(Configs):
    rotateMode: RotateMode

class SecondInputs(Inputs):
    inputImage: InputImage
    inputImage2: InputImage2
class FirstInputs(Inputs):
    inputImage: InputImage

class SecondRequest(Request):
    inputs: Optional[SecondInputs]
    configs: SecondConfigs

    class Config:
        json_schema_extra = {
            "target": "configs"
        }

class FirstRequest(Request):
    inputs: Optional[FirstInputs]
    configs: FirstConfigs

    class Config:
        json_schema_extra = {
            "target": "configs"
        }

class SecondExecutor(Config):
    name: Literal["Second"] = "Second"
    value: Union[SecondRequest, SecondResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Dual Rotate"
        json_schema_extra = {
            "target": {
                "value": 0
            }
        }

class FirstExecutor(Config):
    name: Literal["First"] = "First"
    value: Union[FirstRequest, FirstResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Package"
        json_schema_extra = {
            "target": {
                "value": 0
            }
        }


class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[FirstExecutor, SecondExecutor]
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Task"

class PackageConfigs(Configs):
    executor: ConfigExecutor


class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name: Literal["Package"] = "Package"
