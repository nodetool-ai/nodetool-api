from nodetool.common.replicate_codegen import (
    create_replicate_namespace,
    create_replicate_node,
)
from nodetool.metadata.types import AudioRef, ImageRef, VideoRef
import argparse
import dotenv

"""
This script generates source code for all replicate nodes 
using information from Replicate's model API.
"""

replicate_nodes = [
    {
        "node_name": "AdInpaint",
        "namespace": "image.generate",
        "model_id": "logerzhu/ad-inpaint",
        "return_type": ImageRef,
        "overrides": {"image_path": ImageRef},
    },
    {
        "node_name": "ConsistentCharacter",
        "model_id": "fofr/consistent-character",
        "namespace": "image.generate",
        "return_type": ImageRef,
        "overrides": {"subject": ImageRef},
    },
    {
        "node_name": "PulidBase",
        "model_id": "fofr/pulid-base",
        "namespace": "image.generate",
        "return_type": ImageRef,
        "overrides": {"face_image": ImageRef},
    },
    {
        "model_id": "lucataco/proteus-v0.4",
        "node_name": "Proteus",
        "namespace": "image.generate",
        "return_type": ImageRef,
        "overrides": {"image": ImageRef, "mask": ImageRef},
    },
    {
        "node_name": "SDXLClipInterrogator",
        "namespace": "image.analyze",
        "model_id": "lucataco/sdxl-clip-interrogator",
        "return_type": "str",
        "overrides": {"image": ImageRef},
    },
    {
        "model_id": "lucataco/moondream2",
        "namespace": "image.analyze",
        "node_name": "Moondream2",
        "return_type": "str",
        "overrides": {"image": ImageRef},
    },
    {
        "model_id": "abiruyt/text-extract-ocr",
        "node_name": "TextExtractOCR",
        "namespace": "image.ocr",
        "return_type": "str",
        "overrides": {"image": ImageRef},
    },
    {
        "model_id": "mickeybeurskens/latex-ocr",
        "node_name": "LatexOCR",
        "namespace": "image.ocr",
        "return_type": "str",
        "overrides": {"image": ImageRef},
    },
    {
        "model_id": "fofr/face-to-many",
        "node_name": "FaceToMany",
        "namespace": "image.face",
        "return_type": ImageRef,
        "overrides": {"image": ImageRef},
    },
    {
        "node_name": "BecomeImage",
        "namespace": "image.face",
        "model_id": "fofr/become-image",
        "return_type": ImageRef,
        "overrides": {"image": ImageRef, "image_to_become": ImageRef},
    },
    {
        "model_id": "tencentarc/photomaker",
        "node_name": "PhotoMaker",
        "namespace": "image.face",
        "return_type": ImageRef,
        "overrides": {"image": ImageRef},
    },
    {
        "model_id": "tencentarc/photomaker-style",
        "node_name": "PhotoMakerStyle",
        "namespace": "image.face",
        "return_type": ImageRef,
        "overrides": {
            "input_image": ImageRef,
            "input_image2": ImageRef,
            "input_image3": ImageRef,
            "input_image4": ImageRef,
        },
    },
    {
        "model_id": "fofr/face-to-sticker",
        "node_name": "FaceToSticker",
        "namespace": "image.face",
        "return_type": ImageRef,
        "overrides": {"image": ImageRef},
    },
    {
        "model_id": "zsxkib/instant-id",
        "node_name": "InstantId",
        "namespace": "image.face",
        "return_type": ImageRef,
        "overrides": {"image": ImageRef, "pose_image": ImageRef},
    },
    {
        "node_name": "RealEsrGan",
        "namespace": "image.upscale",
        "model_id": "daanelson/real-esrgan-a100",
        "return_type": ImageRef,
        "overrides": {"image": ImageRef},
    },
    {
        "node_name": "ClarityUpscaler",
        "namespace": "image.upscale",
        "model_id": "philz1337x/clarity-upscaler",
        "return_type": ImageRef,
        "overrides": {"image": ImageRef},
    },
    {
        "node_name": "MagicImageRefiner",
        "namespace": "image.upscale",
        "model_id": "batouresearch/magic-image-refiner",
        "return_type": ImageRef,
        "overrides": {"image": ImageRef, "mask": ImageRef},
    },
    {
        "node_name": "ruDallE_SR",
        "namespace": "image.upscale",
        "model_id": "cjwbw/rudalle-sr",
        "return_type": ImageRef,
        "overrides": {"image": ImageRef},
    },
    {
        "node_name": "HighResolutionControlNetTile",
        "namespace": "image.upscale",
        "model_id": "batouresearch/high-resolution-controlnet-tile",
        "return_type": ImageRef,
        "overrides": {"image": ImageRef},
    },
    {
        "node_name": "UltimateSDUpscale",
        "namespace": "image.upscale",
        "model_id": "fewjative/ultimate-sd-upscale",
        "return_type": ImageRef,
        "overrides": {"image": ImageRef},
    },
    {
        "node_name": "Maxim",
        "model_id": "google-research/maxim",
        "namespace": "image.enhance",
        "return_type": ImageRef,
        "overrides": {"image": ImageRef},
    },
    {
        "node_name": "SwinIR",
        "namespace": "image.upscale",
        "model_id": "jingyunliang/swinir",
        "return_type": ImageRef,
        "overrides": {"image": ImageRef},
    },
    {
        "node_name": "Swin2SR",
        "namespace": "image.upscale",
        "model_id": "mv-lab/swin2sr",
        "return_type": ImageRef,
        "overrides": {"image": ImageRef},
    },
    {
        "model_id": "stability-ai/stable-diffusion",
        "node_name": "StableDiffusion",
        "namespace": "image.generate",
        "return_type": ImageRef,
    },
    {
        "model_id": "usamaehsan/controlnet-1.1-x-realistic-vision-v2.0",
        "node_name": "Controlnet_Realistic_Vision",
        "namespace": "image.generate",
        "return_type": ImageRef,
        "overrides": {"image": ImageRef},
    },
    {
        "model_id": "stability-ai/sdxl",
        "node_name": "StableDiffusionXL",
        "namespace": "image.generate",
        "return_type": ImageRef,
        "overrides": {"image": ImageRef, "mask": ImageRef},
    },
    {
        "model_id": "lucataco/juggernaut-xl-v9",
        "node_name": "Juggernaut_XL_V9",
        "namespace": "image.generate",
        "return_type": ImageRef,
        "overrides": {"image": ImageRef, "mask": ImageRef},
    },
    {
        "model_id": "fofr/epicrealismxl-lightning-hades",
        "node_name": "EpicRealismXL_Lightning_Hades",
        "namespace": "image.generate",
        "return_type": ImageRef,
    },
    {
        "model_id": "swartype/sdxl-pixar",
        "node_name": "SDXL_Pixar",
        "namespace": "image.generate",
        "return_type": ImageRef,
        "overrides": {"image": ImageRef, "mask": ImageRef},
    },
    {
        "model_id": "fofr/sdxl-emoji",
        "node_name": "SDXL_Emoji",
        "namespace": "image.generate",
        "return_type": ImageRef,
        "overrides": {"image": ImageRef, "mask": ImageRef},
    },
    {
        "model_id": "lucataco/sdxl-inpainting",
        "node_name": "StableDiffusionInpainting",
        "namespace": "image.generate",
        "return_type": ImageRef,
        "overrides": {"image": ImageRef},
    },
    {
        "model_id": "lucataco/realvisxl-v2.0",
        "node_name": "RealVisXL_V2",
        "namespace": "image.generate",
        "return_type": ImageRef,
        "overrides": {"image": ImageRef, "mask": ImageRef},
    },
    {
        "model_id": "lucataco/realvisxl2-lcm",
        "node_name": "RealVisXL2_LCM",
        "namespace": "image.generate",
        "return_type": ImageRef,
        "overrides": {"image": ImageRef, "mask": ImageRef},
    },
    {
        "model_id": "fofr/realvisxl-v3-multi-controlnet-lora",
        "node_name": "RealVisXL_V3_Multi_Controlnet_Lora",
        "namespace": "image.generate",
        "return_type": ImageRef,
        "overrides": {
            "image": ImageRef,
            "mask": ImageRef,
            "controlnet_1_image": ImageRef,
            "controlnet_2_image": ImageRef,
            "controlnet_3_image": ImageRef,
        },
    },
    {
        "model_id": "batouresearch/open-dalle-1.1-lora",
        "node_name": "OpenDalle_Lora",
        "namespace": "image.generate",
        "return_type": ImageRef,
        "overrides": {
            "image": ImageRef,
            "mask": ImageRef,
        },
    },
    {
        "model_id": "usamaehsan/controlnet-x-ip-adapter-realistic-vision-v5",
        "node_name": "Controlnet_X_IP_Adapter_Realistic_Vision_V5",
        "namespace": "image.generate",
        "return_type": ImageRef,
        "overrides": {
            "image": ImageRef,
            "lineart_image": ImageRef,
            "scribble_image": ImageRef,
            "tile_image": ImageRef,
            "brightness_image": ImageRef,
            "inpainting_image": ImageRef,
            "mask_image": ImageRef,
        },
    },
    {
        "model_id": "lucataco/sdxl-controlnet",
        "node_name": "SDXL_Controlnet",
        "namespace": "image.generate",
        "return_type": ImageRef,
        "overrides": {"image": ImageRef},
    },
    {
        "model_id": "catacolabs/sdxl-ad-inpaint",
        "node_name": "SDXL_Ad_Inpaint",
        "namespace": "image.generate",
        "return_type": ImageRef,
        "overrides": {"image": ImageRef},
    },
    {
        "node_name": "OldPhotosRestoration",
        "namespace": "image.enhance",
        "model_id": "microsoft/bringing-old-photos-back-to-life",
        "return_type": ImageRef,
        "overrides": {"image": ImageRef},
    },
    {
        "node_name": "Kandinsky",
        "namespace": "image.generate",
        "model_id": "ai-forever/kandinsky-2.2",
        "return_type": ImageRef,
        "overrides": {"image": ImageRef},
    },
    {
        "node_name": "StableDiffusionXLLightning",
        "namespace": "image.generate",
        "model_id": "bytedance/sdxl-lightning-4step",
        "return_type": ImageRef,
    },
    {
        "node_name": "PlaygroundV2",
        "namespace": "image.generate",
        "model_id": "playgroundai/playground-v2.5-1024px-aesthetic",
        "return_type": ImageRef,
        "overrides": {"image": ImageRef},
    },
    {
        "node_name": "VideoMorpher",
        "model_id": "fofr/video-morpher",
        "return_type": VideoRef,
        "namespace": "video.generate",
        "overrides": {
            "subject_image_1": ImageRef,
            "subject_image_2": ImageRef,
            "subject_image_3": ImageRef,
            "subject_image_4": ImageRef,
            "style_image": ImageRef,
        },
    },
    {
        "node_name": "StyleTransfer",
        "model_id": "fofr/style-transfer",
        "return_type": ImageRef,
        "namespace": "image.generate",
        "overrides": {"structure_image": ImageRef, "style_image": ImageRef},
    },
    {
        "node_name": "HotshotXL",
        "namespace": "video.generate",
        "model_id": "lucataco/hotshot-xl",
        "return_type": VideoRef,
    },
    {
        "node_name": "AnimateDiff",
        "namespace": "video.generate",
        "model_id": "zsxkib/animate-diff",
        "return_type": VideoRef,
    },
    {
        "node_name": "Tooncrafter",
        "namespace": "video.generate",
        "model_id": "fofr/tooncrafter",
        "return_type": VideoRef,
        "overrides": {
            "image_1": ImageRef,
            "image_2": ImageRef,
            "image_3": ImageRef,
            "image_4": ImageRef,
            "image_5": ImageRef,
            "image_6": ImageRef,
            "image_7": ImageRef,
            "image_8": ImageRef,
            "image_9": ImageRef,
            "image_10": ImageRef,
        },
    },
    {
        "node_name": "Zeroscope_V2_XL",
        "namespace": "video.generate",
        "model_id": "anotherjesse/zeroscope-v2-xl",
        "return_type": VideoRef,
    },
    {
        "node_name": "RobustVideoMatting",
        "namespace": "video.generate",
        "model_id": "arielreplicate/robust_video_matting",
        "return_type": VideoRef,
        "overrides": {"input_video": VideoRef},
    },
    {
        "node_name": "StableDiffusionInfiniteZoom",
        "namespace": "video.generate",
        "model_id": "arielreplicate/stable_diffusion_infinite_zoom",
        "return_type": VideoRef,
    },
    {
        "node_name": "AnimateDiffIllusions",
        "namespace": "video.generate",
        "model_id": "zsxkib/animatediff-illusions",
        "return_type": VideoRef,
        "overrides": {"controlnet_video": VideoRef},
    },
    {
        "node_name": "Illusions",
        "namespace": "image.generate",
        "model_id": "fofr/illusions",
        "return_type": ImageRef,
        "overrides": {
            "image": ImageRef,
            "control_image": ImageRef,
            "mask_image": ImageRef,
        },
    },
    {
        "model_id": "daanelson/minigpt-4",
        "node_name": "MiniGPT4",
        "namespace": "image.analyze",
        "return_type": "str",
    },
    {
        "model_id": "lucataco/nsfw_image_detection",
        "node_name": "NSFWImageDetection",
        "namespace": "image.analyze",
        "return_type": "str",
    },
    {
        "model_id": "yorickvp/llava-v1.6-34b",
        "node_name": "Llava34B",
        "namespace": "image.analyze",
        "return_type": "str",
        "overrides": {"image": ImageRef},
    },
    {
        "model_id": "salesforce/blip",
        "node_name": "Blip",
        "namespace": "image.analyze",
        "return_type": "str",
        "overrides": {"image": ImageRef},
    },
    {
        "model_id": "andreasjansson/blip-2",
        "node_name": "Blip2",
        "namespace": "image.analyze",
        "return_type": "str",
        "overrides": {"image": ImageRef},
    },
    {
        "model_id": "pharmapsychotic/clip-interrogator",
        "node_name": "ClipInterrogator",
        "namespace": "image.analyze",
        "return_type": str,
        "overrides": {"image": ImageRef},
    },
    {
        "node_name": "Llava13b",
        "namespace": "image.analyze",
        "model_id": "yorickvp/llava-13b",
        "return_type": str,
        "overrides": {"image": ImageRef},
    },
    {
        "model_id": "andreasjansson/clip-features",
        "node_name": "ClipFeatures",
        "namespace": "image.analyze",
        "return_type": list[dict],
    },
    {
        "model_id": "meta/meta-llama-3-8b",
        "node_name": "Llama3_8B",
        "namespace": "text.generate",
        "return_type": str,
    },
    {
        "model_id": "meta/meta-llama-3-70b",
        "node_name": "Llama3_70B",
        "namespace": "text.generate",
        "return_type": str,
    },
    {
        "model_id": "meta/meta-llama-3-8b-instruct",
        "node_name": "Llama3_8B_Instruct",
        "namespace": "text.generate",
        "return_type": str,
    },
    {
        "model_id": "meta/meta-llama-3-70b-instruct",
        "node_name": "Llama3_70B_Instruct",
        "namespace": "text.generate",
        "return_type": str,
    },
    {
        "model_id": "snowflake/snowflake-arctic-instruct",
        "node_name": "Snowflake_Arctic_Instruct",
        "namespace": "text.generate",
        "return_type": str,
    },
    {
        "model_id": "ryan5453/demucs",
        "node_name": "Demucs",
        "namespace": "audio.separate",
        "overrides": {"audio": AudioRef},
        "return_type": {
            "vocals": AudioRef,
            "drums": AudioRef,
            "bass": AudioRef,
            "other": AudioRef,
        },
    },
    {
        "model_id": "openai/whisper",
        "node_name": "Whisper",
        "namespace": "audio.transcribe",
        "return_type": str,
        "overrides": {"audio": AudioRef},
    },
    {
        "model_id": "vaibhavs10/incredibly-fast-whisper",
        "node_name": "IncrediblyFastWhisper",
        "namespace": "audio.transcribe",
        "return_type": str,
        "overrides": {"audio": AudioRef},
    },
    {
        "node_name": "AudioSuperResolution",
        "namespace": "audio.enhance",
        "model_id": "nateraw/audio-super-resolution",
        "return_type": AudioRef,
        "overrides": {"input_file": AudioRef},
    },
    {
        "node_name": "RemoveBackground",
        "namespace": "image.process",
        "model_id": "cjwbw/rembg",
        "return_type": ImageRef,
        "overrides": {"image": ImageRef},
    },
    {
        "node_name": "ModNet",
        "namespace": "image.process",
        "model_id": "pollinations/modnet",
        "return_type": ImageRef,
        "overrides": {"image": ImageRef},
    },
    {
        "node_name": "CodeFormer",
        "namespace": "image.enhance",
        "model_id": "lucataco/codeformer",
        "return_type": ImageRef,
        "overrides": {"image": ImageRef},
    },
    {
        "node_name": "RealisticVoiceCloning",
        "namespace": "audio.generate",
        "model_id": "zsxkib/realistic-voice-cloning",
        "return_type": AudioRef,
        "overrides": {"song_input": AudioRef},
    },
    {
        "node_name": "TortoiseTTS",
        "model_id": "afiaka87/tortoise-tts",
        "namespace": "audio.generate",
        "return_type": AudioRef,
        "overrides": {"custom_voice": AudioRef},
    },
    {
        "model_id": "adirik/styletts2",
        "node_name": "StyleTTS2",
        "namespace": "audio.generate",
        "return_type": AudioRef,
        "overrides": {"reference": AudioRef},
    },
    {
        "node_name": "Riffusion",
        "namespace": "audio.generate",
        "model_id": "riffusion/riffusion",
        "return_type": AudioRef,
        "output_key": "audio",
        "overrides": {"song_input": AudioRef},
    },
    {
        "node_name": "Bark",
        "namespace": "audio.generate",
        "model_id": "suno-ai/bark",
        "return_type": AudioRef,
        "output_key": "audio_out",
    },
    {
        "node_name": "MusicGen",
        "namespace": "audio.generate",
        "model_id": "meta/musicgen",
        "return_type": AudioRef,
    },
    {
        "node_name": "VideoLlava",
        "namespace": "video.analyze",
        "model_id": "nateraw/video-llava",
        "return_type": str,
        "overrides": {"video_path": VideoRef, "image_path": ImageRef},
    },
    {
        "node_name": "AudioToWaveform",
        "namespace": "video.generate",
        "model_id": "fofr/audio-to-waveform",
        "return_type": VideoRef,
        "overrides": {"audio": AudioRef},
    },
]

if __name__ == "__main__":
    dotenv.load_dotenv()

    parser = argparse.ArgumentParser()
    parser.add_argument("--namespace", help="Specify the namespace argument")
    args = parser.parse_args()

    if args.namespace:
        nodes = []
        for node in replicate_nodes:
            if node["namespace"] == args.namespace:
                nodes.append(node)

        print(f"Creating namespace: {args.namespace}")
        create_replicate_namespace(args.namespace, nodes)
    else:
        nodes_by_namespace = {}
        for node in replicate_nodes:
            if node["namespace"] not in nodes_by_namespace:
                nodes_by_namespace[node["namespace"]] = []
            nodes_by_namespace[node["namespace"]].append(node)

        for namespace, nodes in nodes_by_namespace.items():
            print(f"Creating namespace: {namespace}")
            create_replicate_namespace(namespace, nodes)
