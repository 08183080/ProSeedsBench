# 协议模糊测试结果分析报告
生成时间: 2025-12-28 19:53:47

## 覆盖率对比

| Fuzzer | 行覆盖率(%) | 分支覆盖率(%) |
|--------|------------|-------------|
| xpgfuzz | 11.40 | 7.40 |
| chatafl | 13.90 | 10.00 |
| aflnet | 13.80 | 9.90 |

## 状态空间对比

| Fuzzer | 最大节点数 | 最大边数 |
|--------|-----------|---------|
| xpgfuzz | 5 | 4 |
| chatafl | 7 | 15 |
| aflnet | 7 | 11 |

## Fuzzer统计信息

### aflnet

- 总路径数: 612
- 执行次数: 82746
- 执行速度: 1.84 exec/s
- 唯一崩溃: 0
- 唯一挂起: 3

### chatafl

- 总路径数: 593
- 执行次数: 83180
- 执行速度: 0.82 exec/s
- 唯一崩溃: 0
- 唯一挂起: 3

### xpgfuzz

- 总路径数: 348
- 执行次数: 82255
- 执行速度: 0.83 exec/s
- 唯一崩溃: 0
- 唯一挂起: 5

## 高价值种子统计

### aflnet

总计: 349 个高价值种子

| 类型 | 数量 |
|------|------|
| coverage_seed | 237 |
| hang_seed | 3 |
| late_discovery_seed | 99 |
| new_path_seed | 10 |

### chatafl

总计: 344 个高价值种子

| 类型 | 数量 |
|------|------|
| coverage_seed | 241 |
| hang_seed | 3 |
| late_discovery_seed | 83 |
| new_path_seed | 17 |

### xpgfuzz

总计: 210 个高价值种子

| 类型 | 数量 |
|------|------|
| coverage_seed | 163 |
| hang_seed | 5 |
| late_discovery_seed | 38 |
| new_path_seed | 4 |

