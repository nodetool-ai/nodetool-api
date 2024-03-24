from enum import Enum
import pydub
from genflow.nodes.openai import calculate_cost
from genflow.workflows.genflow_node import GenflowNode
from pydantic import Field
from io import BytesIO
from pydub import AudioSegment
from genflow.metadata.types import AudioRef
from genflow.workflows.processing_context import ProcessingContext
from genflow.common.environment import Environment


class CreateSpeech(GenflowNode):
    """
    This node converts text to speech using OpenAI's TTS model.

    ### Applications
    - Creating voiceovers for videos.
    - Creating voiceovers for presentations.
    - Creating voiceovers for podcasts.
    """

    class TtsModel(str, Enum):
        tts_1 = "tts-1"
        tts_1_hd = "tts-1-hd"

    class Voice(str, Enum):
        ALLOY = "alloy"
        ECHO = "echo"
        FABLE = "fable"
        ONYX = "onyx"
        NOVA = "nova"
        SHIMMER = "shimmer"

    model: TtsModel = Field(title="Model", default=TtsModel.tts_1)
    voice: Voice = Field(title="Voice", default=Voice.ALLOY)
    input: str = Field(title="Input", default="")
    speed: float = Field(title="Speed", default=1.0, ge=0.25, le=4.0)

    async def process(self, context: ProcessingContext) -> AudioRef:
        client = Environment.get_openai_client()
        res = await client.audio.speech.create(
            input=self.input,
            model=self.model.value,
            voice=self.voice.value,
            speed=self.speed,
            response_format="mp3",
        )
        cost = calculate_cost(self.model.value, len(self.input), 0)

        await context.create_prediction(
            provider="openai",
            node_id=self.id,
            node_type=self.get_node_type(),
            model=self.model.value,
            cost=cost,
        )
        segment = AudioSegment.from_mp3(BytesIO(res.content))
        audio = await context.audio_from_segment(segment)  # type: ignore
        return audio


class TranscribeNode(GenflowNode):
    """
    Transcribes an audio file.

    The TranscribeAudioNode converts spoken words in an audio file to written text. It is used for creating written records from audio data and is particularly useful in applications involving data analysis, accessibility, and content creation.

    #### Applications
    - Data Analysis: Transcribed text can be further analyzed to derive insights.
    - Accessibility: Helps in making content available to those with hearing impairments.
    - Content Creation: Useful in creating transcripts for podcasts or interviews.
    """

    audio: AudioRef = Field(
        default=AudioRef(), description="The audio file to transcribe."
    )

    async def process(self, context: ProcessingContext) -> str:
        audio_bytes = await context.to_io(self.audio)
        audio_segment: pydub.AudioSegment = pydub.AudioSegment.from_file(audio_bytes)
        audio_bytes.seek(0)

        client = Environment.get_openai_client()
        res = await client.audio.transcriptions.create(
            model="whisper-1", file=("file.mp3", audio_bytes, "audio/mp3")
        )

        await context.create_prediction(
            provider="openai",
            node_id=self.id,
            node_type=self.get_node_type(),
            model="whisper-1",
            cost=calculate_cost("whisper-1", int(audio_segment.duration_seconds)),
        )
        return res.text


class TranslateNode(GenflowNode):
    """
    Translates an audio to english.
    """

    audio: AudioRef = Field(
        default=AudioRef(), description="The audio file to transcribe."
    )
    temperature: float = Field(
        default=0.0, description="The temperature to use for the translation."
    )

    async def process(self, context: ProcessingContext) -> str:
        audio_bytes = await context.to_io(self.audio)
        audio: pydub.AudioSegment = pydub.AudioSegment.from_file(audio_bytes)
        audio_bytes.seek(0)
        client = Environment.get_openai_client()
        res = await client.audio.translations.create(
            model="whisper-1",
            file=("file.mp3", audio_bytes, "audio/mp3"),
            temperature=self.temperature,
        )
        cost = calculate_cost("whisper-1", int(audio.duration_seconds))
        await context.create_prediction(
            provider="openai",
            node_id=self.id,
            node_type=self.get_node_type(),
            model="whisper-1",
            cost=cost,
        )
        return res.text
