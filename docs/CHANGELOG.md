# Changelog — Logical Vehicle Consistency Module

> 本项目改动记录，用于追踪进度和汇报产出。

---

## v0.1 — 调参优化（2026-06-16）

### 改动内容

修改了 build_logical_vehicle_consistency_v1.py 的运行参数：

| 参数 | 改前 | 改后 | 说明 |
|---|---|---|---|
| --max-gap-frames | 10 | 20 | 放宽 tracklet 关联的最大允许缺帧数 |
| --max-link-distance-px | 80 | 120 | 放宽 tracklet 关联的最大允许位移 |

### 验证结果

- logical_vehicle_summary: 36 → 35
- accepted_links: 85 → 88
- lv_0041 断裂从 26 段改善为 2 段

---

## v0.2 — 误杀降低 + 跨 raw 恢复（2026-06-16）

### 改动 1：降低短静态目标的误杀率

文件: tools/logical_vehicle_consistency.py
函数: build_target_validity_report()

short_static_false_positive 从 AUTO_EXCLUDE 降级为 REVIEW_ONLY_IF_UNCERTAIN。

### 改动 2：放松跨 raw 恢复阈值

文件: tools/logical_vehicle_consistency.py
函数: apply_cross_raw_recovery_merges()

max_center_distance_per_frame: 1.0 → 1.8
max_center_distance_px: 45.0 → 72.0
max_size_ratio: 1.35 → 1.50

### 验证结果

| 指标 | 改前（基线） | 改后 |
|---|---|---|
| AUTO_EXCLUDE（误杀） | 6 个 | 0 个 |
| 需人工审查 | 10 个 | 12 个 |
| 自动 tracklet 链接 | 85 个 | 88 个 |
| 跨 raw 恢复自动合并 | 1/3 | 1/3 |

---

## v0.3 — 窗口视频生成（2026-06-16）

产出在 tmp/logical_vehicle_consistency_v3/ 目录下：

- window_01~04/ 四段短窗口视频
- logical_vehicle_id_final.mp4 / debug.mp4 / review.mp4
- 18 个 CSV 报告文件

---

## 待修复（已确认需改动）

### P0 — 遮挡缺帧插值

方案：在 tools/logical_vehicle_consistency.py 中新增 fill_occlusion_gaps()
- 对 1~3 帧缺口做线性插值
- 插值帧标记为 interpolated

状态: 待开发

### P1 — 路边静态车辆排除

方案：
- 新增 static_vehicle 质量判定
- 恢复 AUTO_EXCLUDE 逻辑

状态: 待开发

### P2 — 渲染优化

方案：修改 tools/build_logical_vehicle_id_video.py
- 标签加白底背景
- 提高颜色饱和度

状态: 待开发

---

## 输出目录

| 目录 | 内容 |
|---|---|
| tmp/logical_vehicle_consistency_check/ | v0 基线版 |
| tmp/logical_vehicle_consistency_v2/ | v0.1 调参版 |
| tmp/logical_vehicle_consistency_v3/ | v0.3 完整版（含视频） |
## ???
### P0 ? ?????? ?
??: tools/logical_vehicle_consistency.py
????: fill_occlusion_gaps()
- ???? logical vehicle ????
- ? 1~3 ????????
- ?????? interpolated????????
- ?? occlusion_gap_review.csv ??
??: 71 ?????????? 91 ?

### P1 ? ?????? ?
??: tools/logical_vehicle_consistency.py
??: target_quality_reasons(), build_target_validity_report()
- ?? static_vehicle ???????<0.5px/? ? ???<10px?
- ???????????????
??: ??? lv_0038 + 4 ???/????

### P2 ? ? raw ???? ?
??: tools/logical_vehicle_consistency.py
??: apply_cross_raw_recovery_merges()
- max_center_distance_px: 45?120
- max_center_distance_per_frame: 1.0?3.0
- max_size_ratio: 1.35?1.50
- fragment_max_frames: 60?80
- ?????? min(??)/max(??)?????
??: lv_0021+lv_0036 ?????35?34 ?????

### P2 ? ???? ?
??: tools/build_logical_vehicle_id_video.py
- ?? Windows ?????arial.ttf/calibri.ttf/segoeui.ttf????????????
- ???????????????????
- ????????+?????????

## ??????

- ????????????????????? YOLO ?????
- P2 ???????
