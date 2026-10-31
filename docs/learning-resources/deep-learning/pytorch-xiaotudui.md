# PyTorch 深度学习快速入门教程（绝对通俗易懂！）

## 资源展示

![小土堆 PyTorch 入门课程展示图](../../assets/images/learning-resources/pytorch-xiaotudui.jpg){ width="360" loading="lazy" }

| 项目 | 内容 |
| --- | --- |
| 类型 | 视频课程 |
| 主讲 | 小土堆 |
| 平台 | Bilibili |
| 主题 | 深度学习入门、PyTorch、数据加载与模型训练 |

[课程视频](https://www.bilibili.com/video/BV1hE411t7RN) · [PyTorch 数据集与数据加载官方教程](https://docs.pytorch.org/tutorials/beginner/basics/data_tutorial.html)

## 内容概要

课程通过操作演示串联深度学习的基本工作流程，包括环境配置、Jupyter Notebook、Dataset 与 DataLoader、TensorBoard 指标记录、神经网络搭建、损失计算和反向传播。重点是将各组件组合成能够运行的训练过程。

## 资源评述

课程适合作为 PyTorch 实践入门资料，尤其有助于建立对数据加载、批处理和训练循环的整体认识。已有训练经验时，可以按具体问题回看相关部分；需要补充模型原理时，可结合[动手学深度学习](dive-into-deep-learning.md)。

## 学习参考

- 将样本与标签的对应关系作为数据管线检查的重点，确认读取、变换与打乱操作保持一致。
- 训练前查看一个批次的图像、标签、形状、数据类型与数值范围，尽早发现输入问题。
- 模型不收敛时，除了检查网络与优化器，也应核对标签编码、预处理和损失函数所要求的输入形式。
- 理解 Dataset 如何描述单个样本，以及 DataLoader 如何组织批次，有助于迁移到自定义数据集。
