from pathlib import Path
import sys
import unittest

MODULE_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(MODULE_ROOT / "tools"))

from build_logical_vehicle_id_video import detection_label, final_color_map, final_detection_label, rows_by_frame


class LogicalVehicleConsistencyVideoTest(unittest.TestCase):
    def test_final_label_shows_only_logical_vehicle_id(self):
        row = {
            "logical_vehicle_id": "lv_0014",
            "raw_track_id": "mot_0384",
            "class_name": "car",
            "confidence": "0.8123",
        }

        self.assertEqual(final_detection_label(row), "lv_0014")

    def test_debug_label_shows_logical_and_raw_ids(self):
        row = {
            "logical_vehicle_id": "lv_0014",
            "raw_track_id": "mot_0384",
            "class_name": "car",
            "confidence": "0.8123",
            "association_status": "accepted",
            "final_gate_status": "AUTO_KEEP",
        }

        self.assertEqual(detection_label(row, "debug"), "lv_0014/mot_0384 accepted car 0.81")

    def test_review_label_marks_gate_and_suppression_context(self):
        row = {
            "logical_vehicle_id": "lv_0014",
            "raw_track_id": "mot_0384",
            "class_name": "car",
            "confidence": "0.8123",
            "association_status": "duplicate_suppressed",
            "final_gate_status": "REVIEW_ONLY_IF_UNCERTAIN",
        }

        self.assertEqual(detection_label(row, "review"), "lv_0014/mot_0384 DUP REVIEW car 0.81")

    def test_review_label_marks_quality_risk_context(self):
        row = {
            "logical_vehicle_id": "lv_0041",
            "raw_track_id": "mot_0622",
            "class_name": "car",
            "confidence": "0.3895",
            "association_status": "accepted",
            "final_gate_status": "AUTO_KEEP",
            "quality_status": "RISK_REVIEW",
        }

        self.assertEqual(detection_label(row, "review"), "lv_0041/mot_0622 QUALITY car 0.39")

    def test_unknown_render_mode_is_rejected(self):
        row = {"logical_vehicle_id": "lv_0014", "raw_track_id": "mot_0384"}

        with self.assertRaises(ValueError):
            detection_label(row, "unknown")

    def test_rows_by_frame_keeps_all_supplied_final_rows(self):
        rows = [
            {
                "frame_id": "1",
                "logical_vehicle_id": "lv_0001",
                "raw_track_id": "mot_0001",
                "association_status": "accepted",
                "final_gate_status": "AUTO_KEEP",
            },
            {
                "frame_id": "1",
                "logical_vehicle_id": "lv_0002",
                "raw_track_id": "mot_0002",
                "association_status": "accepted",
                "final_gate_status": "AUTO_EXCLUDE",
            },
        ]

        grouped = rows_by_frame(rows)

        self.assertEqual([row["logical_vehicle_id"] for row in grouped[1]], ["lv_0001", "lv_0002"])

    def test_final_color_map_assigns_unique_highlight_colors(self):
        rows = [
            {"logical_vehicle_id": "lv_0001"},
            {"logical_vehicle_id": "lv_0002"},
            {"logical_vehicle_id": "lv_0001"},
        ]

        colors = final_color_map(rows)

        self.assertEqual(set(colors), {"lv_0001", "lv_0002"})
        self.assertNotEqual(colors["lv_0001"], colors["lv_0002"])
        self.assertTrue(all(max(color) >= 180 for color in colors.values()))

    def test_debug_color_map_remains_stable_per_logical_id(self):
        rows = [
            {"logical_vehicle_id": "lv_0001", "raw_track_id": "mot_0001", "association_status": "accepted", "class_name": "car", "confidence": "0.7000"},
            {"logical_vehicle_id": "lv_0001", "raw_track_id": "mot_0002", "association_status": "accepted", "class_name": "car", "confidence": "0.9000"},
        ]

        colors = final_color_map(rows, mode="debug")

        self.assertEqual(set(colors), {"lv_0001"})


if __name__ == "__main__":
    unittest.main()
