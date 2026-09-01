# 阶段 1 换文件夹，Ch1 按课切片

阶段 0（0001–0016）已过关。用户要求规划后续并控制知识密度，新阶段用新文件夹管理。决定：课件进 `lessons/phase-1/`，练习进 `playground/phase-1/`，速查进 `reference/phase-1/`；课号继续 0017+，全目录仍由 `assets/curriculum.js` 驱动。书 Ch1 是概念地图，不整章塞一课——拆成 0017 公式、0018 Agency/Harness、0019 最小 loop、0020 失败先查 harness。L02 五子系统与框架对照表本阶段不排。

## Implications
- 下一课是 **0017**（公式），不是直接跑 North s01，也不是一次读完 Ch1 / L01
- 导航必须按 `lessons/` 相对路径生成，跨目录的上一课/下一课才能跳
- 阶段 2 再跑 `s01` 的 `code.py`
