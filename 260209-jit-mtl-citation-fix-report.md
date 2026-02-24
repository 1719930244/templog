# JIT_MTL 论文引用验证与修复报告

> **生成时间**: 2026-02-09
> **项目路径**: `/home/szw/OVERLEAF/JIT_MTL/source/`
> **Bib 文件**: `refer.bib`
> **验证方式**: 对 69 篇被引用文献逐一进行网络搜索交叉验证

---

## 一、总体统计

| 指标 | 数量 |
|------|------|
| Bib 中定义的条目总数 | **84** |
| Tex 中实际引用的条目 | **69** |
| 引用了但未定义（致命错误） | **0** ✅ |
| 定义了但未引用（冗余条目） | **15** |
| 🔴 需要修复的错误 | **1** |
| 🟡 建议更新 venue 的条目 | **3** |
| 🟠 重复/错误的冗余条目 | **1** |

---

## 二、🔴 必须修复的错误

### 2.1 `gao2023retrieval` — 作者列表有两处错误

**文件位置**: `refer.bib` 第 11-18 行

**当前（错误）**:
```bibtex
author={Gao, Yunfan and Xiong, Yun and Gao, Xinyu and Jia, Kangxiang and Pan, Jinliu and Bi, Yuxi and Dai, Yixin and Sun, Jiawei and Wang, Haofen and Wang, Haofen},
```

**修改为（正确）**:
```bibtex
author={Gao, Yunfan and Xiong, Yun and Gao, Xinyu and Jia, Kangxiang and Pan, Jinliu and Bi, Yuxi and Dai, Yi and Sun, Jiawei and Wang, Meng and Wang, Haofen},
```

**错误详情**:

| # | 位置 | 错误值 | 正确值 | 错误类型 |
|---|------|--------|--------|---------|
| 1 | 第 7 位作者 | `Dai, Yixin` | `Dai, Yi` | 名字被错误扩展 |
| 2 | 第 10 位作者 | `Wang, Haofen`（重复） | `Wang, Meng` | 第 9 位作者被复制 |

**验证来源**: [arXiv:2312.10997](https://arxiv.org/abs/2312.10997)
**影响**: 参考文献列表中会显示 `...Haofen Wang, and Haofen Wang`，同一作者出现两次。

---

## 三、🟡 建议更新的条目（arXiv → 正式发表）

以下条目在 bib 中标注为 arXiv preprint，但实际已在正式会议/期刊发表。更新为正式信息更规范。

### 3.1 `loshchilov2017decoupled` — 已发表于 ICLR 2019

**当前**:
```bibtex
@article{loshchilov2017decoupled,
  title={Decoupled weight decay regularization},
  author={Loshchilov, Ilya and Hutter, Frank},
  journal={arXiv preprint arXiv:1711.05101},
  year={2017}
}
```

**建议修改为**:
```bibtex
@inproceedings{loshchilov2019decoupled,
  title={Decoupled weight decay regularization},
  author={Loshchilov, Ilya and Hutter, Frank},
  booktitle={International Conference on Learning Representations},
  year={2019}
}
```

**验证来源**: [ICLR 2019 Poster](https://iclr.cc/virtual/2019/poster/935)

> ⚠️ 注意：如果更改 key 从 `loshchilov2017decoupled` 到 `loshchilov2019decoupled`，需要同步更新 `.tex` 文件中的 `\cite{}`。

### 3.2 `guo2022unixcoder` — 已发表于 ACL 2022

**当前**:
```bibtex
@article{guo2022unixcoder,
  title={Unixcoder: Unified cross-modal pre-training for code representation},
  author={Guo, Daya and Lu, Shuai and Duan, Nan and Wang, Yanlin and Zhou, Ming and Yin, Jian},
  journal={arXiv preprint arXiv:2203.03850},
  year={2022}
}
```

**建议修改为**:
```bibtex
@inproceedings{guo2022unixcoder,
  title={UniXcoder: Unified Cross-Modal Pre-training for Code Representation},
  author={Guo, Daya and Lu, Shuai and Duan, Nan and Wang, Yanlin and Zhou, Ming and Yin, Jian},
  booktitle={Proceedings of the 60th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)},
  pages={7212--7225},
  year={2022}
}
```

**验证来源**: [arXiv:2203.03850](https://arxiv.org/abs/2203.03850)

### 3.3 `niu2023empirical` — 已发表于 ICSE 2023

**当前**:
```bibtex
@article{niu2023empirical,
  title={An Empirical Comparison of Pre-Trained Models of Source Code},
  author={Niu, Changan and Li, Chuanyi and Ng, Vincent and Chen, Dongxiao and Ge, Jidong and Luo, Bin},
  journal={arXiv preprint arXiv:2302.04026},
  year={2023}
}
```

**建议修改为**:
```bibtex
@inproceedings{niu2023empirical,
  title={An Empirical Comparison of Pre-Trained Models of Source Code},
  author={Niu, Changan and Li, Chuanyi and Ng, Vincent and Chen, Dongxiao and Ge, Jidong and Luo, Bin},
  booktitle={Proceedings of the 45th IEEE/ACM International Conference on Software Engineering},
  year={2023}
}
```

**验证来源**: [UT Dallas Faculty Profile](https://profiles.utdallas.edu/vince)

---

## 四、🟠 冗余/重复条目（建议删除）

### 4.1 `ross2017focal` — Focal Loss 论文的错误副本

此条目与 `lin2017focal` 是同一篇论文，但作者名严重错误：

```bibtex
@inproceedings{ross2017focal,
  title={Focal loss for dense object detection},
  author={Ross, T-YLPG and Doll{\'a}r, GKHP},  % ← 乱码作者名
  booktitle={proceedings of the IEEE conference on computer vision and pattern recognition},
  pages={2980--2988},
  year={2017}
}
```

**建议**: 直接删除此条目。论文中使用的是正确的 `lin2017focal`。

---

## 五、未被引用的冗余条目（15 个）

以下条目定义在 `refer.bib` 中但论文正文从未引用，建议在最终提交前清理：

| # | Key | 标题 |
|---|-----|------|
| 1 | `ahmad2021unified` | Unified pre-training for program understanding and generation |
| 2 | `bui2021self` | Self-supervised contrastive learning for code retrieval... |
| 3 | `canfora2013multi` | Multi-objective cross-project defect prediction |
| 4 | `gao2021simcse` | SimCSE: Simple contrastive learning of sentence embeddings |
| 5 | `guo2025deepseek` | DeepSeek-R1: Incentivizing reasoning capability in LLMs... |
| 6 | `hai2016deceptive` | Deceptive review spam detection... |
| 7 | `jain2020contrastive` | Contrastive code representation learning |
| 8 | `jaiswal2020survey` | A survey on contrastive self-supervised learning |
| 9 | `liu2023contrabert` | ContraBERT: Enhancing code pre-trained models... |
| 10 | `lu2021codexglue` | CodeXGLUE: A machine learning benchmark... |
| 11 | `mao2023cross` | Cross-entropy loss functions: Theoretical analysis... |
| 12 | `neelakantan2022text` | Text and code embeddings by contrastive pre-training |
| 13 | `ross2017focal` | Focal loss for dense object detection (重复错误条目) |
| 14 | `shi2023cocosoda` | CoCoSoDa: Effective contrastive learning for code search |
| 15 | `wattanakriengkrai2020predicting` | Predicting defective lines using a model-agnostic technique |

---

## 六、年份使用"在线首发"日期的条目（可接受）

以下条目的 `year` 使用 IEEE 早期在线发表日期，而非卷号对应年份。这在 SE 领域是常见做法：

| Key | bib year | 卷号对应年份 |
|-----|----------|-------------|
| `kamei2012large` | 2012 | TSE vol.39(6) → 2013 |
| `yan2020just` | 2020 | TSE vol.48(1) → 2022 |
| `chen2021defectchecker` | 2021 | TSE vol.48(7) → 2022 |
| `pornprasit2022deeplinedp` | 2022 | TSE vol.49(1) → 2023 |

---

## 七、验证通过的引用（65 篇）

以下引用经网络搜索验证，标题、作者、年份、会议/期刊信息均正确无误：

`an2024code` `arisholm2010systematic` `bacchelli2013expectations` `chen2018multi`
`chen2024jit` `chen2024multi` `collobert2008unified` `falaki2023attention`
`feng2020codebert` `fontana2024multitask` `goodfellow2014generative` `hanley1982meaning`
`he2020momentum` `herbold2022fine` `herzig2013s` `hindle2016naturalness`
`hinton2009deep` `hoang2019deepjit` `hoang2020cc2vec` `huang2024multi`
`hui2024qwen2` `kaneko2020encoder` `lecun2015deep` `lin2017focal`
`lin2023cct5` `ling2003auc` `liu2016jointly` `nafi2019clcdsa`
`ni2019multitask` `ni2022best` `ni2022just` `ni2023unifying`
`niu2022deep` `niu2022spt` `niu2023rat` `pascarella2019fine`
`pornprasit2021jitline` `qiu2020jito` `ribeiro2016should` `rigatti2017random`
`robbes2019leveraging` `roziere2023code` `sahar2024irjit` `shen2020survey`
`sogaard2016deep` `tang2023just` `vaswani2017attention` `vo2024just`
`wang2021codet5` `wu2023decoder` `yang2014unified` `yang2015deep`
`yang2017tlel` `yang2020using` `yang2023deep` `yang2024multi`
`young2018replication` `zeng2021deep` `zhang2018overview` `zhang2024just`
`zou2024ccaf`
