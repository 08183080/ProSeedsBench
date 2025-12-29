#!/usr/bin/env python3
"""
快速摘要工具 - 从分析结果中提取关键指标
"""

import json
from pathlib import Path

def load_json(filepath):
    """加载JSON文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def print_section(title):
    """打印章节标题"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def main():
    base_dir = Path(__file__).parent
    
    print_section("协议模糊测试结果快速摘要")
    
    # 1. 覆盖率对比
    print_section("1. 覆盖率对比")
    coverage = load_json(base_dir / "coverage_analysis.json")
    print(f"{'Fuzzer':<12} {'行覆盖率':<12} {'分支覆盖率':<12} {'排名':<6}")
    print("-" * 50)
    
    sorted_fuzzers = sorted(coverage.items(), 
                           key=lambda x: x[1]['line_cov_max'], 
                           reverse=True)
    for i, (fuzzer, data) in enumerate(sorted_fuzzers, 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉"
        print(f"{fuzzer:<12} {data['line_cov_max']:>6.2f}%     "
              f"{data['branch_cov_max']:>6.2f}%     {medal}")
    
    # 2. 状态空间对比
    print_section("2. 状态空间探索能力")
    states = load_json(base_dir / "states_analysis.json")
    print(f"{'Fuzzer':<12} {'最大节点':<10} {'最大边数':<10} {'复杂度':<10}")
    print("-" * 50)
    
    sorted_states = sorted(states.items(), 
                          key=lambda x: x[1]['max_edges'], 
                          reverse=True)
    for fuzzer, data in sorted_states:
        complexity = "高" if data['max_edges'] > 10 else "中" if data['max_edges'] > 5 else "低"
        print(f"{fuzzer:<12} {data['max_nodes']:<10} {data['max_edges']:<10} {complexity:<10}")
    
    # 3. Fuzzer统计
    print_section("3. Fuzzer执行统计")
    stats = load_json(base_dir / "fuzzer_stats.json")
    print(f"{'Fuzzer':<12} {'执行次数':<12} {'速度(exec/s)':<15} {'总路径数':<10} {'挂起':<6}")
    print("-" * 70)
    
    for fuzzer, data in stats.items():
        execs = int(data.get('execs_done', 0))
        speed = float(data.get('execs_per_sec', 0))
        paths = int(data.get('paths_total', 0))
        hangs = int(data.get('unique_hangs', 0))
        print(f"{fuzzer:<12} {execs:<12} {speed:<15.2f} {paths:<10} {hangs:<6}")
    
    # 4. 高价值种子统计
    print_section("4. 高价值种子统计")
    seeds = load_json(base_dir / "high_value_seeds.json")
    print(f"{'Fuzzer':<12} {'总种子数':<10} {'覆盖率种子':<12} {'新路径':<10} {'挂起':<6}")
    print("-" * 60)
    
    total_seeds = 0
    for fuzzer, seed_list in seeds.items():
        total = len(seed_list)
        total_seeds += total
        by_type = {}
        for seed in seed_list:
            seed_type = seed.get('type', 'unknown')
            by_type[seed_type] = by_type.get(seed_type, 0) + 1
        
        coverage_count = by_type.get('coverage_seed', 0)
        new_path = by_type.get('new_path_seed', 0)
        hangs = by_type.get('hang_seed', 0)
        
        print(f"{fuzzer:<12} {total:<10} {coverage_count:<12} {new_path:<10} {hangs:<6}")
    
    print(f"\n总计高价值种子: {total_seeds} 个")
    
    # 5. 函数覆盖摘要（如果存在）
    func_cov_file = base_dir / "function_coverage" / "xpgfuzz_function_coverage.json"
    if func_cov_file.exists():
        print_section("5. 函数级覆盖摘要 (xpgfuzz)")
        func_cov = load_json(func_cov_file)
        
        total_funcs = 0
        uncovered_funcs = 0
        partially_covered = 0
        
        for filename, file_info in func_cov.get('function_coverage', {}).items():
            for func in file_info.get('functions', []):
                total_funcs += 1
                if func['line_coverage_pct'] == 0:
                    uncovered_funcs += 1
                elif func['line_coverage_pct'] < 50:
                    partially_covered += 1
        
        print(f"总函数数: {total_funcs}")
        print(f"完全未覆盖: {uncovered_funcs} ({uncovered_funcs/total_funcs*100:.1f}%)")
        print(f"部分覆盖: {partially_covered} ({partially_covered/total_funcs*100:.1f}%)")
        print(f"覆盖充足: {total_funcs - uncovered_funcs - partially_covered} "
              f"({(total_funcs - uncovered_funcs - partially_covered)/total_funcs*100:.1f}%)")
    
    # 6. 关键发现
    print_section("6. 关键发现")
    
    # 找出最佳fuzzer
    best_fuzzer = sorted_fuzzers[0][0]
    best_coverage = sorted_fuzzers[0][1]['line_cov_max']
    
    # 找出状态空间最复杂的
    best_state = sorted_states[0][0]
    best_edges = sorted_states[0][1]['max_edges']
    
    # 找出执行最快的
    fastest = max(stats.items(), key=lambda x: float(x[1].get('execs_per_sec', 0) or 0))
    fastest_speed = float(fastest[1].get('execs_per_sec', 0) or 0)
    
    print(f"✅ 覆盖率最佳: {best_fuzzer} ({best_coverage:.2f}%)")
    print(f"✅ 状态空间最复杂: {best_state} ({best_edges} 条边)")
    print(f"✅ 执行速度最快: {fastest[0]} ({fastest_speed:.2f} exec/s)")
    print(f"✅ 高价值种子总数: {total_seeds} 个")
    
    # 7. 改进建议
    print_section("7. 快速改进建议")
    print("1. 合并所有fuzzer的高价值种子库（总计903个种子）")
    print("2. 添加认证相关的初始种子（mod_auth.c完全未覆盖）")
    print("3. 优化xpgfuzz的状态空间建模（当前仅4条边）")
    print("4. 学习chatafl的种子生成策略（种子更精简）")
    print("5. 考虑添加HTTP/2协议支持（h2.c完全未覆盖）")
    
    print(f"\n{'='*60}")
    print("详细分析报告请查看: comprehensive_insights.md")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()

