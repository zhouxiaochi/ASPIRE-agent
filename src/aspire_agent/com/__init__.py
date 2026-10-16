"""Small COM-facing operations with duck-typed test doubles."""
from .operations import OperationError, connect_stream, create_heat_stream, create_heater_block, create_material_stream, create_mixer_block, list_block_ports
from .setters import set_heater, set_mixer
__all__ = ["OperationError", "connect_stream", "create_heat_stream", "create_heater_block", "create_material_stream", "create_mixer_block", "list_block_ports", "set_heater", "set_mixer"]
