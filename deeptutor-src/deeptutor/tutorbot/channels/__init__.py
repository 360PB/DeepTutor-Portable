"""Chat channels module with plugin architecture."""

from deeptutor.tutorbot.channels.base import BaseChannel
from deeptutor.tutorbot.channels.manager import ChannelManager

__all__ = ["BaseChannel", "ChannelManager"]
