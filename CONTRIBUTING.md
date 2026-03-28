# Contributing

## 1. 只改数据，不手改生成页

请只修改这些文件：

- `data/image_2d.jsonl`
- `data/video.jsonl`
- `data/object_3d.jsonl`
- `data/scene_3d.jsonl`
- `data/world_4d.jsonl`

不要手改：

- `README.md`
- `00-surveys-and-foundations/*`
- `10-image-2d/*`
- `20-video/*`
- `30-3d-object-asset/*`
- `40-3d-scene/*`
- `50-4d-dynamic-scene-world/*`
- `90-topics/*`

这些文件全部由 `python scripts/build.py` 自动生成。

---

## 2. 当前 seed scope

当前种子仓库优先覆盖：

- 时间：`2025-01-01 ~ 2026-03-28`
- 优先级：**代表性 + 开源优先 + 检索价值**
- 方向：image / video / 3D object / 3D scene / 4D world

---

## 3. 新增论文的规则

### 必须
- 每篇工作只能进入一个 `data/*.jsonl`
- 必须有：
  - `id`
  - `title`
  - `venue`
  - `task`

### 推荐
- `domain`
- `representation`
- `method`
- `conditioning`
- `open_source`
- `paper`
- `repo`
- `summary`

### 严格分类规则
- 按**最终产物**分类
- `autonomous-driving / indoor / human-avatar` 只能是 tag，不是主目录
- `diffusion / autoregressive / 3DGS / BEV / occupancy` 只能是 tag，不是主目录

---

## 4. 写 summary 的建议

一句话足够，模板如下：

```text
做什么 + 主要技术路线 + 为什么值得收录
```

例如：

```text
流式向量图世界模型，把 driving simulation 从像素空间挪到 lane-agent graph 表示。
```

如果你不写 `summary`，生成器会自动给出一句模板化 TL;DR。

---

## 5. 提交流程

```bash
python scripts/build.py
git add .
git commit -m "data: add <paper-id>"
git push
```

---

## 6. 不确定链接时怎么做

如果你不能 100% 确认：
- `paper` 留空
- `repo` 留空

生成器会自动回退到：
- paper search
- GitHub repository search

这样比写错链接更好。
