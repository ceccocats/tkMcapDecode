
# tkMcapDecode

`tkMcapDecode` is a Python utility designed to decode `.mcap` log files. It extracts and converts specific topics from the logs into a structured, usable format.

## Installation & Usage

### 1. Install Dependencies
Ensure you have the required Python packages installed by running:
```
pip install -r requirements.txt
```
### 2. Decode an MCAP File
Run the decoding script and pass the path to your `.mcap` file as an argument:
```
python3 decode_mcap.py file_to_read.mcap
```

## Extracted Data: Radar Point Cloud

The script extracts various topics from the `.mcap` file. For the radar point cloud, the `decodeCloud` function parses the raw data into a custom NumPy array (`points`) based on the dtype defined in `cloud.py`. This standard array format makes it easy to manipulate or convert the data for downstream applications


Below is the structure of the decoded `PointRadarInfo` data:

| Field | Type | Description |
| :--- | :--- | :--- |
| `x`, `y`, `z` | `float32` | 3D spatial coordinates of the point. |
| `intensity` | `float32` | Normalized intensity value (range: 0 to 1). |
| `snr` | `float32` | Signal-to-Noise Ratio. |
| `max_unambiguous_velocity` | `float32` | The maximum unambiguous velocity of the radar. |
| `radial_ambiguous_velocity` | `float32` | The ambiguous radial velocity for each individual point. |
| `radial_unambiguous_velocity`| `float32` | *Placeholder field (currently left at `0`).* |
| `compensated_vx` | `float32` | *Placeholder field (currently left at `0`).* |
| `compensated_vy` | `float32` | *Placeholder field (currently left at `0`).* |
| `time` | `float32` | *Placeholder field (currently left at `0`).* |

> **Note:** The raw data may contain an `st_0` field, but this is automatically ignored and discarded by the decoding function.



