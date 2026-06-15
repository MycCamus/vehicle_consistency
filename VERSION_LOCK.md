# Version Lock

Locked version:

```text
outputs/logical_vehicle_consistency_v1/
```

Package date: 2026-06-12

## Source Chain

```text
inputs/video_clips/MVI_0866_520_560.mp4
inputs/model_weights/yolo26x.pt
  -> outputs/yolo26x_trial/target_tracks/detections_tracked.csv
  -> outputs/yolo26x_manual_filter_v1/target_tracks_final.csv
  -> outputs/logical_vehicle_consistency_v1/
```

## Locked Metrics

- logical_vehicle_track_rows: 19,597
- logical_vehicle_summary_rows: 46
- duplicate_groups: 980
- accepted_links: 83
- ambiguous_links: 6
- validation checks: 2 PASS

## Version Rule

`outputs/logical_vehicle_consistency_v1/` is the authoritative result for this package. The scripts in `tools/` are included for audit and continuation, but later script changes must write to a new output version directory instead of overwriting this locked result.
