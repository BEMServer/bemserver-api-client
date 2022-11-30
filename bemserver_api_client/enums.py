"""BEMServer API client enums"""
import enum


class DataFormat(enum.Enum):
    csv = "application/csv"
    json = "application/json"


class Aggregation(enum.Enum):
    avg = "avg"
    sum = "sum"
    min = "min"
    max = "max"
    count = "count"
