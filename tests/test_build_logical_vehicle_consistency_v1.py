from pathlib import Path
import sys
import unittest

MODULE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(MODULE_ROOT / "tools"))

from build_logical_vehicle_consistency_v1 import (
    debug_render_rows,
    equal_frame_windows,
    final_render_rows,
    logical_video_output_paths,
    logical_window_output_paths,
    review_render_rows,
)


class BuildLogicalVehicleConsistencyV1Test(unittest.TestCase):
    def test_declares_final_debug_and_review_video_outputs(self):
        output_dir = Path("outputs/logical_vehicle_consistency_v1")

        paths = logical_video_output_paths(output_dir)

        self.assertEqual(
            paths,
            {
                "final": output_dir / "logical_vehicle_id_final.mp4",
                "debug": output_dir / "logical_vehicle_id_debug.mp4",
                "review": output_dir / "logical_vehicle_id_review.mp4",
            },
        )

    def test_declares_three_window_slice_final_outputs(self):
        output_dir = Path("outputs/logical_vehicle_consistency_v1")

        paths = logical_window_output_paths(output_dir, window_count=3)

        self.assertEqual(set(paths), {"window_01", "window_02", "window_03"})
        self.assertEqual(paths["window_01"], output_dir / "window_01" / "logical_vehicle_id_final.mp4")
        self.assertEqual(paths["window_03"], output_dir / "window_03" / "logical_vehicle_id_final.mp4")

    def test_equal_frame_windows_cover_full_clip_without_overlap(self):
        windows = equal_frame_windows(total_frames=2000, window_count=3)

        self.assertEqual(windows, [(0, 667), (667, 1334), (1334, 2000)])

    def test_final_render_rows_passes_only_accepted_auto_keep_rows_to_renderer(self):
        rows = [
            {"logical_vehicle_id": "lv_0001", "association_status": "accepted", "final_gate_status": "AUTO_KEEP"},
            {"logical_vehicle_id": "lv_0002", "association_status": "accepted", "final_gate_status": "AUTO_EXCLUDE"},
            {"logical_vehicle_id": "lv_0003", "association_status": "duplicate_suppressed", "final_gate_status": "AUTO_KEEP"},
        ]

        final_rows = final_render_rows(rows)

        self.assertEqual([row["logical_vehicle_id"] for row in final_rows], ["lv_0001"])

    def test_debug_render_rows_passes_all_accepted_rows_to_renderer(self):
        rows = [
            {"logical_vehicle_id": "lv_0001", "association_status": "accepted", "final_gate_status": "AUTO_KEEP"},
            {"logical_vehicle_id": "lv_0002", "association_status": "accepted", "final_gate_status": "AUTO_EXCLUDE"},
            {"logical_vehicle_id": "lv_0003", "association_status": "accepted", "final_gate_status": "REVIEW_ONLY_IF_UNCERTAIN"},
            {"logical_vehicle_id": "lv_0004", "association_status": "duplicate_suppressed", "final_gate_status": "AUTO_KEEP"},
        ]

        debug_rows = debug_render_rows(rows)

        self.assertEqual([row["logical_vehicle_id"] for row in debug_rows], ["lv_0001", "lv_0002", "lv_0003"])

    def test_review_render_rows_passes_uncertain_and_suppressed_rows_to_renderer(self):
        rows = [
            {"logical_vehicle_id": "lv_0001", "association_status": "accepted", "final_gate_status": "AUTO_KEEP"},
            {"logical_vehicle_id": "lv_0002", "association_status": "accepted", "final_gate_status": "AUTO_EXCLUDE"},
            {"logical_vehicle_id": "lv_0003", "association_status": "accepted", "final_gate_status": "REVIEW_ONLY_IF_UNCERTAIN"},
            {"logical_vehicle_id": "lv_0004", "association_status": "duplicate_suppressed", "final_gate_status": "AUTO_KEEP"},
            {"logical_vehicle_id": "lv_0005", "association_status": "fragment_suppressed", "final_gate_status": "AUTO_KEEP"},
        ]

        review_rows = review_render_rows(rows)

        self.assertEqual(
            [row["logical_vehicle_id"] for row in review_rows],
            ["lv_0002", "lv_0003", "lv_0004", "lv_0005"],
        )

    def test_review_render_rows_passes_quality_risk_auto_keep_rows_to_renderer(self):
        rows = [
            {"logical_vehicle_id": "lv_0001", "association_status": "accepted", "final_gate_status": "AUTO_KEEP", "quality_status": "QUALITY_PASS"},
            {"logical_vehicle_id": "lv_0002", "association_status": "accepted", "final_gate_status": "AUTO_KEEP", "quality_status": "RISK_REVIEW"},
        ]

        review_rows = review_render_rows(rows)

        self.assertEqual([row["logical_vehicle_id"] for row in review_rows], ["lv_0002"])


if __name__ == "__main__":
    unittest.main()
