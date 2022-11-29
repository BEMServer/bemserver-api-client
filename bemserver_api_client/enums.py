"""BEMServer API client enums"""
import enum


class DataFormat(enum.Enum):
    csv = "application/csv"
    json = "application/json"
