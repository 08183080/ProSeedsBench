#!/usr/bin/env python3
"""
基于Fuzzing结果丰富HTTP协议初始种子

功能：
1. 基于覆盖分析生成针对性种子（认证、HTTP方法、HTTP头）
2. 从高价值种子中提取有效模式
3. 生成新的初始种子文件
"""

import json
import os
import base64
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

class SeedEnricher:
    def __init__(self, analysis_dir: str, output_dir: str):
        self.analysis_dir = Path(analysis_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 加载分析结果
        self.load_analysis_results()
        
    def load_analysis_results(self):
        """加载fuzzing分析结果"""
        try:
            with open(self.analysis_dir / "high_value_seeds.json", 'r') as f:
                self.high_value_seeds = json.load(f)
            with open(self.analysis_dir / "function_coverage" / "seed_generation_config.json", 'r') as f:
                self.seed_config = json.load(f)
            with open(self.analysis_dir / "comprehensive_insights.md", 'r') as f:
                self.insights = f.read()
        except Exception as e:
            print(f"Warning: Could not load some analysis files: {e}")
            self.high_value_seeds = {}
            self.seed_config = {}
            self.insights = ""
    
    def generate_auth_seeds(self) -> List[Dict[str, str]]:
        """生成认证相关种子"""
        seeds = []
        
        # Basic认证变体
        basic_credentials = [
            ("admin", "password"),
            ("user", "123456"),
            ("test", "test"),
            ("", ""),  # 空凭证
            ("user:pass", "with:colon"),  # 特殊字符
        ]
        
        for username, password in basic_credentials:
            cred = base64.b64encode(f"{username}:{password}".encode()).decode()
            seed = {
                "name": f"http_requests_get_basic_auth_{username or 'empty'}.raw",
                "content": f"""GET /hello.txt HTTP/1.1
Host: 127.0.0.1:8080
User-Agent: curl/8.0.1
Accept: */*
Authorization: Basic {cred}

"""
            }
            seeds.append(seed)
        
        # Digest认证
        digest_seeds = [
            {
                "name": "http_requests_get_digest_auth.raw",
                "content": """GET /hello.txt HTTP/1.1
Host: 127.0.0.1:8080
User-Agent: curl/8.0.1
Accept: */*
Authorization: Digest username="user", realm="test", nonce="abc123", uri="/hello.txt", response="response_hash"

"""
            },
            {
                "name": "http_requests_get_digest_auth_full.raw",
                "content": """GET /hello.txt HTTP/1.1
Host: 127.0.0.1:8080
User-Agent: curl/8.0.1
Accept: */*
Authorization: Digest username="admin", realm="Protected Area", nonce="dcd98b7102dd2f0e8b11d0f600bfb0c093", uri="/hello.txt", qop=auth, nc=00000001, cnonce="0a4f113b", response="6629fae49393a05397450978507c4ef1", opaque="5ccc069c403ebaf9f0171e9517f40e41"

"""
            }
        ]
        seeds.extend(digest_seeds)
        
        # Bearer Token
        bearer_seeds = [
            {
                "name": "http_requests_get_bearer_token.raw",
                "content": """GET /hello.txt HTTP/1.1
Host: 127.0.0.1:8080
User-Agent: curl/8.0.1
Accept: */*
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9

"""
            },
            {
                "name": "http_requests_get_bearer_token_long.raw",
                "content": """GET /hello.txt HTTP/1.1
Host: 127.0.0.1:8080
User-Agent: curl/8.0.1
Accept: */*
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c

"""
            }
        ]
        seeds.extend(bearer_seeds)
        
        # 无效认证（测试错误处理）
        invalid_auth_seeds = [
            {
                "name": "http_requests_get_invalid_auth.raw",
                "content": """GET /hello.txt HTTP/1.1
Host: 127.0.0.1:8080
User-Agent: curl/8.0.1
Accept: */*
Authorization: InvalidScheme invalid_credentials

"""
            },
            {
                "name": "http_requests_get_malformed_basic.raw",
                "content": """GET /hello.txt HTTP/1.1
Host: 127.0.0.1:8080
User-Agent: curl/8.0.1
Accept: */*
Authorization: Basic not_base64_encoded

"""
            }
        ]
        seeds.extend(invalid_auth_seeds)
        
        return seeds
    
    def generate_http_method_seeds(self) -> List[Dict[str, str]]:
        """生成各种HTTP方法的种子"""
        seeds = []
        
        # POST方法（带不同Content-Type）
        post_seeds = [
            {
                "name": "http_requests_post_json.raw",
                "content": """POST /api/data HTTP/1.1
Host: 127.0.0.1:8080
User-Agent: curl/8.0.1
Accept: application/json
Content-Type: application/json
Content-Length: 18

{"key": "value"}
"""
            },
            {
                "name": "http_requests_post_form.raw",
                "content": """POST /form HTTP/1.1
Host: 127.0.0.1:8080
User-Agent: curl/8.0.1
Accept: */*
Content-Type: application/x-www-form-urlencoded
Content-Length: 11

name=value
"""
            },
            {
                "name": "http_requests_post_text.raw",
                "content": """POST /upload HTTP/1.1
Host: 127.0.0.1:8080
User-Agent: curl/8.0.1
Accept: */*
Content-Type: text/plain
Content-Length: 5

hello
"""
            },
            {
                "name": "http_requests_post_empty.raw",
                "content": """POST /empty HTTP/1.1
Host: 127.0.0.1:8080
User-Agent: curl/8.0.1
Accept: */*
Content-Length: 0

"""
            }
        ]
        seeds.extend(post_seeds)
        
        # PUT方法
        put_seeds = [
            {
                "name": "http_requests_put_file.raw",
                "content": """PUT /file.txt HTTP/1.1
Host: 127.0.0.1:8080
User-Agent: curl/8.0.1
Accept: */*
Content-Type: text/plain
Content-Length: 12

Hello World
"""
            }
        ]
        seeds.extend(put_seeds)
        
        # HEAD方法
        head_seeds = [
            {
                "name": "http_requests_head_simple.raw",
                "content": """HEAD /hello.txt HTTP/1.1
Host: 127.0.0.1:8080
User-Agent: curl/8.0.1
Accept: */*

"""
            }
        ]
        seeds.extend(head_seeds)
        
        # PATCH方法
        patch_seeds = [
            {
                "name": "http_requests_patch_json.raw",
                "content": """PATCH /resource/1 HTTP/1.1
Host: 127.0.0.1:8080
User-Agent: curl/8.0.1
Accept: application/json
Content-Type: application/json
Content-Length: 15

{"status":"ok"}
"""
            }
        ]
        seeds.extend(patch_seeds)
        
        # TRACE方法
        trace_seeds = [
            {
                "name": "http_requests_trace_simple.raw",
                "content": """TRACE /hello.txt HTTP/1.1
Host: 127.0.0.1:8080
User-Agent: curl/8.0.1
Accept: */*

"""
            }
        ]
        seeds.extend(trace_seeds)
        
        return seeds
    
    def generate_header_variant_seeds(self) -> List[Dict[str, str]]:
        """生成HTTP头变体种子"""
        seeds = []
        
        # Range头
        range_seeds = [
            {
                "name": "http_requests_get_range_bytes.raw",
                "content": """GET /hello.txt HTTP/1.1
Host: 127.0.0.1:8080
User-Agent: curl/8.0.1
Accept: */*
Range: bytes=0-1023

"""
            },
            {
                "name": "http_requests_get_range_start.raw",
                "content": """GET /hello.txt HTTP/1.1
Host: 127.0.0.1:8080
User-Agent: curl/8.0.1
Accept: */*
Range: bytes=100-

"""
            }
        ]
        seeds.extend(range_seeds)
        
        # If-Modified-Since
        if_modified_seeds = [
            {
                "name": "http_requests_get_if_modified_since.raw",
                "content": """GET /hello.txt HTTP/1.1
Host: 127.0.0.1:8080
User-Agent: curl/8.0.1
Accept: */*
If-Modified-Since: Wed, 21 Oct 2015 07:28:00 GMT

"""
            }
        ]
        seeds.extend(if_modified_seeds)
        
        # Cookie
        cookie_seeds = [
            {
                "name": "http_requests_get_cookie.raw",
                "content": """GET /hello.txt HTTP/1.1
Host: 127.0.0.1:8080
User-Agent: curl/8.0.1
Accept: */*
Cookie: session=abc123; user=test

"""
            }
        ]
        seeds.extend(cookie_seeds)
        
        # Referer
        referer_seeds = [
            {
                "name": "http_requests_get_referer.raw",
                "content": """GET /hello.txt HTTP/1.1
Host: 127.0.0.1:8080
User-Agent: curl/8.0.1
Accept: */*
Referer: http://example.com/page

"""
            }
        ]
        seeds.extend(referer_seeds)
        
        # Connection变体
        connection_seeds = [
            {
                "name": "http_requests_get_connection_close.raw",
                "content": """GET /hello.txt HTTP/1.1
Host: 127.0.0.1:8080
User-Agent: curl/8.0.1
Accept: */*
Connection: close

"""
            },
            {
                "name": "http_requests_get_connection_keepalive.raw",
                "content": """GET /hello.txt HTTP/1.1
Host: 127.0.0.1:8080
User-Agent: curl/8.0.1
Accept: */*
Connection: keep-alive

"""
            }
        ]
        seeds.extend(connection_seeds)
        
        # 多个头的组合
        multi_header_seeds = [
            {
                "name": "http_requests_get_multi_headers.raw",
                "content": """GET /hello.txt HTTP/1.1
Host: 127.0.0.1:8080
User-Agent: curl/8.0.1
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Connection: keep-alive
Cookie: session=abc123

"""
            }
        ]
        seeds.extend(multi_header_seeds)
        
        return seeds
    
    def generate_path_variant_seeds(self) -> List[Dict[str, str]]:
        """生成路径变体种子"""
        seeds = []
        
        path_variants = [
            ("/", "root"),
            ("/index.html", "index"),
            ("/api/v1/data", "api"),
            ("/path/to/file.txt", "nested"),
            ("/file%20with%20spaces.txt", "encoded"),
            ("/file?param=value", "query"),
            ("/file#fragment", "fragment"),
            ("/very/long/path/to/resource/file.txt", "long"),
        ]
        
        for path, suffix in path_variants:
            seed = {
                "name": f"http_requests_get_path_{suffix}.raw",
                "content": f"""GET {path} HTTP/1.1
Host: 127.0.0.1:8080
User-Agent: curl/8.0.1
Accept: */*

"""
            }
            seeds.append(seed)
        
        return seeds
    
    def generate_all_seeds(self) -> List[Dict[str, str]]:
        """生成所有种子"""
        all_seeds = []
        
        print("Generating authentication seeds...")
        all_seeds.extend(self.generate_auth_seeds())
        
        print("Generating HTTP method seeds...")
        all_seeds.extend(self.generate_http_method_seeds())
        
        print("Generating header variant seeds...")
        all_seeds.extend(self.generate_header_variant_seeds())
        
        print("Generating path variant seeds...")
        all_seeds.extend(self.generate_path_variant_seeds())
        
        return all_seeds
    
    def save_seeds(self, seeds: List[Dict[str, str]]):
        """保存种子到文件"""
        seed_list = []
        
        for seed in seeds:
            filepath = self.output_dir / seed["name"]
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(seed["content"])
            seed_list.append({
                "name": seed["name"],
                "path": str(filepath),
                "size": len(seed["content"])
            })
            print(f"Saved: {seed['name']}")
        
        # 保存种子清单
        manifest = {
            "generated_at": datetime.now().isoformat(),
            "total_seeds": len(seeds),
            "seeds": seed_list,
            "categories": {
                "auth": len([s for s in seeds if "auth" in s["name"]]),
                "methods": len([s for s in seeds if any(m in s["name"] for m in ["post", "put", "head", "patch", "trace"])]),
                "headers": len([s for s in seeds if "header" in s["name"] or "range" in s["name"] or "cookie" in s["name"] or "referer" in s["name"] or "connection" in s["name"]]),
                "paths": len([s for s in seeds if "path_" in s["name"]])
            }
        }
        
        manifest_path = self.output_dir / "seed_manifest.json"
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, indent=2, ensure_ascii=False)
        
        print(f"\nTotal seeds generated: {len(seeds)}")
        print(f"Manifest saved to: {manifest_path}")
        
        return manifest

def main():
    # 配置路径
    analysis_dir = "/home/apple/ProSeedsBench/http_analysis_output"
    output_dir = "/home/apple/ProSeedsBench/seeds/HTTP/Lighttpd1/in-lighttpd1"
    
    print("=" * 60)
    print("HTTP Protocol Seed Enrichment from Fuzzing Results")
    print("=" * 60)
    
    # 创建enricher
    enricher = SeedEnricher(analysis_dir, output_dir)
    
    # 生成所有种子
    seeds = enricher.generate_all_seeds()
    
    # 保存种子
    manifest = enricher.save_seeds(seeds)
    
    # 打印摘要
    print("\n" + "=" * 60)
    print("Seed Generation Summary")
    print("=" * 60)
    print(f"Total seeds: {manifest['total_seeds']}")
    print(f"Categories:")
    for category, count in manifest['categories'].items():
        print(f"  - {category}: {count}")
    print("=" * 60)

if __name__ == "__main__":
    main()

