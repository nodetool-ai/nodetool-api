from pydantic import Field
from genflow.metadata.types import ImageTensor
from genflow.metadata.types import asset_to_ref
from genflow.models.asset import Asset
from genflow.metadata.types import FolderRef
from genflow.metadata.types import AssetRef
from genflow.workflows.processing_context import ProcessingContext
from genflow.metadata.types import AudioRef
from genflow.metadata.types import ImageRef
from genflow.metadata.types import TextRef
from genflow.workflows.genflow_node import InputNode
from genflow.metadata.types import VideoRef


class FloatInputNode(InputNode):
    """
    Represents a float parameter for the workflow.
    input, parameter, float, number
    """

    value: float = 0.0
    min: float = 0
    max: float = 100

    async def process(self, context: ProcessingContext) -> float:
        return min(max(self.value, self.min), self.max)

    def get_json_schema(self):
        return {
            "type": "number",
            "description": self.description,
            "default": self.value,
            "minimum": self.min,
            "maximum": self.max,
        }


class BoolInputNode(InputNode):
    """
    Represents a boolean parameter for the workflow.
    input, parameter, boolean, bool
    """

    value: bool = False

    async def process(self, context: ProcessingContext) -> bool:
        return self.value

    def get_json_schema(self):
        return {
            "type": "boolean",
            "description": self.description,
            "default": self.value,
        }


class IntInputNode(InputNode):
    """
    Represents an integer parameter for the workflow.
    input, parameter, integer, number
    """

    value: int = 0
    min: int = 0
    max: int = 100

    async def process(self, context: ProcessingContext) -> int:
        return min(max(self.value, self.min), self.max)

    def get_json_schema(self):
        return {
            "type": "integer",
            "description": self.description,
            "default": self.value,
            "minimum": self.min,
            "maximum": self.max,
        }


class StringInputNode(InputNode):
    """
    Represents a string parameter for the workflow.
    input, parameter, string, text
    """

    value: str = ""

    async def process(self, context: ProcessingContext) -> str:
        return self.value

    def get_json_schema(self):
        return {
            "type": "string",
            "description": self.description,
            "default": self.value,
        }


class ChatInputNode(InputNode):
    """
    Represents a chat message parameter for the workflow.
    input, parameter, chat, message
    """

    value: str = ""

    async def process(self, context: ProcessingContext) -> str:
        return self.value

    def get_json_schema(self):
        return {
            "type": "string",
            "description": self.description,
            "default": self.value,
        }


class TextInputNode(InputNode):
    """
    Represents a text parameter for the workflow.
    input, parameter, text
    """

    value: TextRef = Field(TextRef(), description="The text to use as input.")

    async def process(self, context: ProcessingContext) -> TextRef:
        return self.value

    def get_json_schema(self):
        return {
            "type": "string",
            "description": self.description,
            "default": self.value,
        }


class AssetSchemaMixin:
    def get_json_schema(self):
        return {
            "type": "object",
            "properties": {
                "uri": {
                    "type": "string",
                    "description": "The URI of the image.",
                    "format": "uri",
                },
                "asset_id": {
                    "type": "string",
                    "description": "The Asset ID of the image.",
                },
            },
        }


class ImageInputNode(AssetSchemaMixin, InputNode):
    """
    Represents an image parameter for the workflow.
    input, parameter, image
    """

    value: ImageRef = Field(ImageRef(), description="The image to use as input.")

    async def process(self, context: ProcessingContext) -> ImageRef:
        return self.value


class VideoInputNode(AssetSchemaMixin, InputNode):
    """
    Represents a video parameter for the workflow.
    input, parameter, video
    """

    value: VideoRef = Field(VideoRef(), description="The video to use as input.")

    async def process(self, context: ProcessingContext) -> VideoRef:
        return self.value


class AudioInputNode(AssetSchemaMixin, InputNode):
    """
    Represents an audio parameter for the workflow.
    input, parameter, audio
    """

    value: AudioRef = Field(AudioRef(), description="The audio to use as input.")

    async def process(self, context: ProcessingContext) -> AudioRef:
        return self.value


class FolderNode(AssetSchemaMixin, InputNode):
    """
    Represents a folder parameter for the workflow.
    input, parameter, folder
    """

    folder: FolderRef = Field(FolderRef(), description="The folder to use as input.")
    limit: int = 1000

    async def process(self, context: ProcessingContext) -> list[AssetRef]:
        if self.folder.is_empty():
            return []

        assets, cursor = Asset.paginate(
            user_id=context.user_id,
            parent_id=self.folder.asset_id,
            limit=self.limit,
        )

        return [asset_to_ref(asset) for asset in assets]


class ImageFolderNode(FolderNode):
    """
    Represents an image folder parameter for the workflow.
    input, parameter, folder, image
    """

    async def process(self, context: ProcessingContext) -> list[ImageRef]:
        assets = await super().process(context)
        images = [asset for asset in assets if isinstance(asset, ImageRef)]
        return images


class AudioFolderNode(FolderNode):
    """
    Repesents an audio folder parameter for the workflow.
    input, parameter, folder, audio
    """

    async def process(self, context: ProcessingContext) -> list[AudioRef]:
        assets = await super().process(context)
        audios = [asset for asset in assets if isinstance(asset, AudioRef)]
        return audios


class VideoFolderNode(FolderNode):
    """
    Represents a video folder parameter for the workflow.
    input, parameter, folder, video
    """

    async def process(self, context: ProcessingContext) -> list[VideoRef]:
        assets = await super().process(context)
        videos = [asset for asset in assets if isinstance(asset, VideoRef)]
        return videos


class TextFolderNode(FolderNode):
    """
    Represents a text folder parameter for the workflow.
    input, parameter, folder, text
    """

    async def process(self, context: ProcessingContext) -> list[TextRef]:
        assets = await super().process(context)
        texts = [asset for asset in assets if isinstance(asset, TextRef)]
        return texts


class ComfyInputImageNode(AssetSchemaMixin, InputNode):
    """
    Represents an image parameter for the workflow.
    input, parameter, image
    """

    value: ImageRef = Field(ImageRef(), description="The image to use as input.")

    async def process(self, context: ProcessingContext) -> ImageTensor:
        from PIL import Image, ImageOps, ImageSequence
        import torch
        import numpy as np

        img = await context.to_pil(self.value)

        output_images = []
        output_masks = []
        for i in ImageSequence.Iterator(img):
            i = ImageOps.exif_transpose(i)
            image = i.convert("RGB")
            image = np.array(image).astype(np.float32) / 255.0
            image = torch.from_numpy(image)[None,]
            if "A" in i.getbands():
                mask = np.array(i.getchannel("A")).astype(np.float32) / 255.0
                mask = 1.0 - torch.from_numpy(mask)
            else:
                mask = torch.zeros((64, 64), dtype=torch.float32, device="cpu")
            output_images.append(image)
            output_masks.append(mask.unsqueeze(0))

        if len(output_images) > 1:
            output_image = torch.cat(output_images, dim=0)
            output_mask = torch.cat(output_masks, dim=0)
        else:
            output_image = output_images[0]
            output_mask = output_masks[0]

        return output_image  # type: ignore
