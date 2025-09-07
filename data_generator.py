import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

class SyntheticESCDataGenerator:
    def __init__(self, chamber: str = "Chamber_1"):
        self.chamber = chamber

        # Define value ranges based on your sample
        self.value_ranges = {
            "ESC_Bias_Voltage": (-95, -85),
            "ESC_Clamp_Voltage": (3400, 3450),
            "ESC_Coolant_Flow_AI": (3.5, 4.0),
            "ESC_Current_Temp": (20.0, 21.0),
            "Inner_ESC_Heater_Temp": (34, 37),
            "Inner_ESC_Temp_Output_Value": (22, 24),
            "MidInner_ESC_Heater_Temp": (20, 24),
            "MidInner_ESC_Temp_Output_Value": (32.5, 34),
            "MidOuter_ESC_Heater_Temp": (15, 19),
            "MidOuter_ESC_Temp_Output_Value": (31.5, 33),
            "Outer_ESC_Heater_Temp": (13, 18),
            "Outer_ESC_Temp_Output_Value": (31.5, 33),
        }

        # Steps sequence to alternate between
        self.steps = ["SION", "SION_OE"]

    def _generate_row(self, timestamp: pd.Timestamp, step: str):
        row = {
            "timestamp": timestamp,
            "chamber": self.chamber,
            "step": step
        }

        # Generate each numeric column with some random noise
        for col, (low, high) in self.value_ranges.items():
            row[col] = np.round(np.random.uniform(low, high), 5)

        # Simple label — mostly zeros, occasional stress
        row["Possible_ESC_Thermal_Stress"] = 1.0 if random.random() < 0.01 else 0.0

        return row

    def generate(self, n_rows: int = 100, start_time: str | datetime = "2025-06-10 00:00:00"):
        rows = []
        timestamp = pd.to_datetime(start_time)

        for i in range(n_rows):
            step = self.steps[i % len(self.steps)]  # alternate steps
            row = self._generate_row(timestamp, step)
            rows.append(row)
            timestamp += timedelta(seconds=1)  # increment by 1 second

        return pd.DataFrame(rows)


# Example usage:
if __name__ == "__main__":
    gen = SyntheticESCDataGenerator()
    df = gen.generate(10, start_time="2025-07-01 08:00:00")
    print(df)
