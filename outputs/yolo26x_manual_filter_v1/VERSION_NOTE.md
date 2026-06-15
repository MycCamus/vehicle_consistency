# manual_filter_v1 Manual Track Exclusion

- input_exclusion_ids: `0013,0012,0083,0080,0204,0203,0283,0312,0401,0423,0537,0480,0505,0604`
- normalized_exclusion_ids: `mot_0013,mot_0012,mot_0083,mot_0080,mot_0204,mot_0203,mot_0283,mot_0312,mot_0401,mot_0423,mot_0537,mot_0480,mot_0505,mot_0604`
- target_review_candidates_before_filter: `52`
- candidate_excluded_by_manual_filter: `10`
- already_auto_excluded_ids: `mot_0204,mot_0203,mot_0312,mot_0401`
- missing_ids: ``
- final_target_tracks: `42`

This version only removes manually listed track ids from the yolo26x target-review candidates.
It does not add vehicles, merge fragments, infer lanes, or create SUMO events.
