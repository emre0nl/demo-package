
from sdks.novavision.src.helper.package import PackageHelper
from components.Package.src.models.PackageModel import PackageModel, PackageConfigs, ConfigExecutor, FirstExecutor, FirstResponse, FirstOutputs, SecondExecutor, SecondResponse, SecondOutputs, OutputImage, OutputImage2


def build_response_first(context):
    outputImage = OutputImage(value=context.image)
    Outputs = FirstOutputs(outputImage=outputImage)
    firstResponse = FirstResponse(outputs=Outputs)
    firstExecutor = FirstExecutor(value=firstResponse)
    executor = ConfigExecutor(value=firstExecutor)
    packageConfigs = PackageConfigs(executor=executor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)
    packageModel = package.build_model(context)
    return packageModel


def build_response_second(context):
    outputImage = OutputImage(value=context.image)
    outputImage2 = OutputImage2(value=context.image2)
    Outputs = SecondOutputs(outputImage=outputImage, outputImage2=outputImage2)
    secondResponse = SecondResponse(outputs=Outputs)
    secondExecutor = SecondExecutor(value=secondResponse)
    executor = ConfigExecutor(value=secondExecutor)
    packageConfigs = PackageConfigs(executor=executor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)
    packageModel = package.build_model(context)
    return packageModel
