#!/usr/bin/env python3
"""
快速整合种子 - 第一步: 整合已有种子和精选高价值种子

功能:
1. 整合已有的生成种子 (35个左右)
2. 从高价值种子中精选小且有效的种子
3. 生成初步的种子清单
"""

import json
import os
import shutil
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

class QuickSeedConsolidator:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.analysis_dir = self.base_dir / "http_analysis_output"
        self.source_seeds_dir = self.base_dir / "enriched_seeds" / "HTTP" / "Lighttpd1" / "try" / "in-lighttpd1"
        self.target_seeds_dir = self.base_dir / "seeds" / "HTTP" / "Lighttpd1" / "in-lighttpd1"
        self.high_value_seeds_dir = self.analysis_dir / "high_value_seeds"
        
        # 创建目标目录
        self.target_seeds_dir.mkdir(parents=True, exist_ok=True)
        
    def backup_existing_seeds(self):
        """备份现有种子"""
        backup_dir = self.target_seeds_dir.parent / "in-lighttpd1.backup"
        if self.target_seeds_dir.exists() and any(self.target_seeds_dir.glob("*.raw")):
            if backup_dir.exists():
                shutil.rmtree(backup_dir)
            shutil.copytree(self.target_seeds_dir, backup_dir)
            print(f"✅ 已备份现有种子到: {backup_dir}")
    
    def consolidate_generated_seeds(self) -> List[str]:
        """整合已生成的种子"""
        consolidated = []
        
        if not self.source_seeds_dir.exists():
            print(f"⚠️  源种子目录不存在: {self.source_seeds_dir}")
            return consolidated
        
        # 复制所有.raw文件
        for seed_file in self.source_seeds_dir.glob("*.raw"):
            target_file = self.target_seeds_dir / seed_file.name
            
            # 如果目标文件已存在,跳过(避免覆盖)
            if target_file.exists():
                print(f"⏭️  跳过已存在的种子: {seed_file.name}")
                continue
            
            shutil.copy2(seed_file, target_file)
            consolidated.append(seed_file.name)
            print(f"✅ 复制种子: {seed_file.name}")
        
        return consolidated
    
    def load_high_value_seeds(self) -> Dict[str, List[Dict]]:
        """加载高价值种子信息"""
        json_file = self.analysis_dir / "high_value_seeds.json"
        if not json_file.exists():
            print(f"⚠️  高价值种子JSON文件不存在: {json_file}")
            return {}
        
        with open(json_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def select_high_value_seeds(self, max_size_kb: int = 50, max_count: int = 100) -> List[Dict]:
        """从高价值种子中精选"""
        all_seeds = self.load_high_value_seeds()
        selected = []
        
        # 优先级权重
        priority_weights = {
            'coverage_seed': 3,
            'new_path_seed': 2,
            'late_discovery_seed': 1,
            'hang_seed': 1,
            'unknown': 0
        }
        
        all_candidates = []
        for fuzzer, seed_list in all_seeds.items():
            for seed in seed_list:
                size_kb = seed.get('size', 0) / 1024
                seed_type = seed.get('type', 'unknown')
                priority = priority_weights.get(seed_type, 0)
                
                # 筛选条件: 大小限制
                if size_kb <= max_size_kb:
                    all_candidates.append({
                        'fuzzer': fuzzer,
                        'seed': seed,
                        'size_kb': size_kb,
                        'priority': priority
                    })
        
        # 按优先级和大小排序 (优先级高 + 大小小 = 更好)
        all_candidates.sort(key=lambda x: (-x['priority'], x['size_kb']))
        
        # 选择前N个
        selected_candidates = all_candidates[:max_count]
        
        print(f"\n📊 高价值种子精选统计:")
        print(f"   候选总数: {len(all_candidates)}")
        print(f"   精选数量: {len(selected_candidates)}")
        print(f"   平均大小: {sum(x['size_kb'] for x in selected_candidates) / len(selected_candidates):.2f} KB")
        
        # 统计类型分布
        type_counts = {}
        for candidate in selected_candidates:
            seed_type = candidate['seed'].get('type', 'unknown')
            type_counts[seed_type] = type_counts.get(seed_type, 0) + 1
        
        print(f"   类型分布:")
        for seed_type, count in sorted(type_counts.items(), key=lambda x: -x[1]):
            print(f"     - {seed_type}: {count}")
        
        return [c['seed'] for c in selected_candidates]
    
    def copy_high_value_seeds(self, selected_seeds: List[Dict]) -> List[str]:
        """复制精选的高价值种子"""
        copied = []
        skipped_not_found = 0
        skipped_exists = 0
        
        print(f"   准备复制 {len(selected_seeds)} 个精选的高价值种子...")
        
        for seed in selected_seeds:
            source_path = Path(seed.get('path', ''))
            
            if not source_path.exists():
                skipped_not_found += 1
                continue
            
            # 生成新文件名 (简化)
            seed_name = seed.get('name', 'unknown')
            # 清理文件名,保留原始ID
            new_name = f"high_value_{seed_name.replace(':', '_').replace('+', '_').replace(',', '_')}.raw"
            target_path = self.target_seeds_dir / new_name
            
            # 如果目标已存在,跳过
            if target_path.exists():
                skipped_exists += 1
                continue
            
            try:
                shutil.copy2(source_path, target_path)
                copied.append(new_name)
                # 每10个打印一次进度
                if len(copied) % 10 == 0:
                    print(f"   ✅ 已复制 {len(copied)} 个...")
            except Exception as e:
                print(f"   ⚠️  复制失败 {source_path.name}: {e}")
                skipped_not_found += 1
        
        if skipped_not_found > 0:
            print(f"   ⏭️  跳过 {skipped_not_found} 个种子 (文件路径不存在)")
        if skipped_exists > 0:
            print(f"   ⏭️  跳过 {skipped_exists} 个种子 (目标文件已存在)")
        
        return copied
    
    def generate_manifest(self, generated_seeds: List[str], high_value_seeds: List[str]) -> Dict:
        """生成种子清单"""
        all_seeds = []
        total_size = 0
        
        for seed_file in sorted(self.target_seeds_dir.glob("*.raw")):
            size = seed_file.stat().st_size
            total_size += size
            
            seed_type = "unknown"
            if seed_file.name.startswith("http_requests_"):
                seed_type = "generated"
            elif seed_file.name.startswith("high_value_"):
                seed_type = "high_value"
            
            all_seeds.append({
                "name": seed_file.name,
                "size": size,
                "size_kb": round(size / 1024, 2),
                "type": seed_type
            })
        
        # 按类别统计
        categories = {
            "auth": len([s for s in all_seeds if "auth" in s["name"]]),
            "method": len([s for s in all_seeds if any(m in s["name"] for m in ["post", "put", "head", "patch", "trace", "delete", "options"])]),
            "header": len([s for s in all_seeds if any(h in s["name"] for h in ["range", "cookie", "referer", "connection", "if_modified"])]),
            "generated": len([s for s in all_seeds if s["type"] == "generated"]),
            "high_value": len([s for s in all_seeds if s["type"] == "high_value"])
        }
        
        manifest = {
            "generated_at": datetime.now().isoformat(),
            "total_seeds": len(all_seeds),
            "total_size_bytes": total_size,
            "total_size_kb": round(total_size / 1024, 2),
            "total_size_mb": round(total_size / 1024 / 1024, 2),
            "categories": categories,
            "seeds": all_seeds
        }
        
        # 保存清单
        manifest_path = self.target_seeds_dir / "seed_manifest.json"
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
        
        return manifest
    
    def print_summary(self, manifest: Dict):
        """打印摘要"""
        print(f"\n{'='*60}")
        print("📦 种子整合摘要")
        print(f"{'='*60}")
        print(f"总种子数: {manifest['total_seeds']}")
        print(f"总大小: {manifest['total_size_mb']:.2f} MB ({manifest['total_size_kb']:.2f} KB)")
        print(f"平均大小: {manifest['total_size_kb'] / manifest['total_seeds']:.2f} KB/种子")
        print(f"\n类别分布:")
        for category, count in manifest['categories'].items():
            print(f"  - {category}: {count}")
        print(f"\n种子清单已保存: {self.target_seeds_dir / 'seed_manifest.json'}")
        print(f"{'='*60}\n")
    
    def run(self):
        """执行整合流程"""
        print("🚀 开始快速整合种子...\n")
        
        # 1. 备份现有种子
        self.backup_existing_seeds()
        
        # 2. 整合已生成的种子
        print("\n📋 步骤1: 整合已生成的种子")
        generated = self.consolidate_generated_seeds()
        print(f"✅ 整合了 {len(generated)} 个已生成的种子\n")
        
        # 3. 精选高价值种子
        print("\n📋 步骤2: 从高价值种子中精选")
        selected = self.select_high_value_seeds(max_size_kb=50, max_count=100)
        
        # 4. 复制高价值种子
        print("\n📋 步骤3: 复制精选的高价值种子")
        if len(selected) > 0:
            high_value = self.copy_high_value_seeds(selected)
            print(f"✅ 复制了 {len(high_value)} 个高价值种子\n")
            
            if len(high_value) == 0:
                print("⚠️  警告: 没有成功复制任何高价值种子")
                print("   可能原因: 高价值种子文件路径不存在")
                print(f"   提示: 检查 high_value_seeds.json 中的路径是否正确\n")
        else:
            print("⚠️  没有找到符合条件的高价值种子")
            high_value = []
        
        # 5. 生成清单
        print("📋 步骤4: 生成种子清单")
        manifest = self.generate_manifest(generated, high_value)
        
        # 6. 打印摘要
        self.print_summary(manifest)
        
        print("✨ 整合完成!")
        print(f"\n种子目录: {self.target_seeds_dir}")
        print(f"下一步: 查看 seed_manifest.json 了解详细信息")

def main():
    consolidator = QuickSeedConsolidator()
    consolidator.run()

if __name__ == "__main__":
    main()

