"""
协议实现的 DeepWiki Agent

该模块提供了一个 Agent 类，用于分析协议实现的 GitHub 仓库，
通过 DeepWiki 提取所有实现方法和每个方法的关键逻辑。

功能:
    1. 分析协议实现的 GitHub 仓库
    2. 提取所有协议命令/方法的实现
    3. 获取每个命令的处理模块
    4. 提取每个方法的关键逻辑
    5. 生成结构化的 JSON 输出

使用方法:
    # 基本用法
    agent = ProtocolDeepWikiAgent()
    result = agent.analyze_repository("proftpd/proftpd")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    # 保存到文件
    agent.save_to_json(result, "output.json")
    
    # 命令行用法
    python protocol_dkagent.py proftpd/proftpd [output_path]

输出格式:
    {
        "target": "实现名称",
        "implementation_details": "实现细节概述",
        "custom_commands": [
            {
                "command_name": "命令名称",
                "handling_module": "处理模块",
                "critical_logic": "关键逻辑"
            },
            ...
        ]
    }

依赖:
    - mcp: MCP 客户端库
    - asyncio: 异步支持
"""

import json
import re
import asyncio
from typing import Dict, List, Optional, Any
from pathlib import Path
from mcp import ClientSession
from mcp.client.sse import sse_client


class ProtocolDeepWikiAgent:
    """
    协议实现的 DeepWiki Agent
    
    通过 DeepWiki MCP 工具分析协议实现仓库，提取：
    1. 所有协议命令/方法的实现
    2. 每个命令的处理模块
    3. 每个方法的关键逻辑
    """
    
    def __init__(self):
        """初始化 Agent"""
        self.repo_name = None
        self.raw_data = {}
    
    def analyze_repository(self, repo_name: str) -> Dict[str, Any]:
        """
        分析协议实现仓库，提取所有实现方法和关键逻辑
        
        Args:
            repo_name: GitHub 仓库名称，格式为 "owner/repo" (如 "proftpd/proftpd")
            
        Returns:
            包含以下结构的字典:
            {
                "target": "实现名称",
                "implementation_details": "实现细节概述",
                "custom_commands": [
                    {
                        "command_name": "命令名称",
                        "handling_module": "处理模块",
                        "critical_logic": "关键逻辑"
                    },
                    ...
                ]
            }
        """
        self.repo_name = repo_name
        print(f"[*] 开始分析仓库: {repo_name}")
        
        # 1. 获取仓库的文档结构
        print("[*] 步骤 1/3: 获取仓库文档结构...")
        structure = self._get_wiki_structure(repo_name)
        
        # 2. 提取所有实现方法和关键逻辑
        print("[*] 步骤 2/3: 提取所有实现方法和关键逻辑...")
        methods_info = self._extract_all_methods(repo_name)
        
        # 3. 获取实现细节概述
        print("[*] 步骤 3/3: 获取实现细节概述...")
        implementation_details = self._get_implementation_details(repo_name)
        
        # 4. 构建结果
        result = {
            "target": self._extract_target_name(repo_name),
            "implementation_details": implementation_details,
            "custom_commands": methods_info
        }
        
        print(f"[+] 分析完成！共提取 {len(methods_info)} 个实现方法")
        return result
    
    def _get_wiki_structure(self, repo_name: str) -> Dict:
        """
        获取仓库的 DeepWiki 文档结构
        
        Args:
            repo_name: GitHub 仓库名称
            
        Returns:
            文档结构信息
        """
        try:
            return asyncio.run(self._async_get_wiki_structure(repo_name))
        except Exception as e:
            print(f"[!] 获取文档结构失败: {e}")
            return {}
    
    async def _async_get_wiki_structure(self, repo_name: str) -> Dict:
        """异步获取文档结构"""
        DEEPWIKI_SERVER_URL = "https://mcp.deepwiki.com/sse"
        try:
            async with sse_client(DEEPWIKI_SERVER_URL) as (read_stream, write_stream):
                async with ClientSession(read_stream, write_stream) as session:
                    await session.initialize()
                    result = await session.call_tool("read_wiki_structure", {"repoName": repo_name})
                    if result.content:
                        # 解析结果
                        if isinstance(result.content, list):
                            return {"structure": [item.text if hasattr(item, 'text') else str(item) for item in result.content]}
                        return {"structure": str(result.content)}
        except Exception as e:
            print(f"[!] 异步获取文档结构失败: {e}")
            return {}
    
    def _extract_all_methods(self, repo_name: str) -> List[Dict[str, str]]:
        """
        提取所有协议实现方法和关键逻辑
        
        Args:
            repo_name: GitHub 仓库名称
            
        Returns:
            方法信息列表，每个元素包含 command_name, handling_module, critical_logic
        """
        # 构建查询问题，要求提取所有命令及其实现细节
        question = """请提取该协议实现的所有命令（包括标准命令和扩展命令），
对于每个命令，请提供：
1. 命令名称
2. 处理该命令的模块或函数
3. 该命令的关键处理逻辑（包括参数解析、状态检查、错误处理、潜在的漏洞触发点等）

请以 JSON 格式返回，格式如下：
{
  "commands": [
    {
      "command_name": "命令名称",
      "handling_module": "处理模块/函数",
      "critical_logic": "关键逻辑描述"
    }
  ]
}

只返回 JSON，不要其他解释文字。"""
        
        try:
            # 使用 MCP 工具提问
            response = asyncio.run(self._async_ask_question(repo_name, question))
            
            # 解析响应
            methods = self._parse_methods_response(response)
            return methods
            
        except Exception as e:
            print(f"[!] 提取方法信息失败: {e}")
            # 如果直接提取失败，尝试分步骤提取
            return self._extract_methods_stepwise(repo_name)
    
    async def _async_ask_question(self, repo_name: str, question: str) -> str:
        """异步提问"""
        DEEPWIKI_SERVER_URL = "https://mcp.deepwiki.com/sse"
        try:
            async with sse_client(DEEPWIKI_SERVER_URL) as (read_stream, write_stream):
                async with ClientSession(read_stream, write_stream) as session:
                    await session.initialize()
                    result = await session.call_tool("ask_question", {
                        "repoName": repo_name,
                        "question": question
                    })
                    if result.content:
                        # 提取文本内容
                        if isinstance(result.content, list):
                            return "\n".join([item.text if hasattr(item, 'text') else str(item) for item in result.content])
                        return str(result.content)
                    return ""
        except Exception as e:
            print(f"[!] 异步提问失败: {e}")
            return ""
    
    def _parse_methods_response(self, response: Any) -> List[Dict[str, str]]:
        """
        解析 DeepWiki 返回的方法信息
        
        Args:
            response: DeepWiki 返回的响应
            
        Returns:
            方法信息列表
        """
        methods = []
        
        # 如果响应是字符串，尝试提取 JSON
        if isinstance(response, str):
            # 尝试提取 JSON 部分
            json_match = re.search(r'\{[\s\S]*\}', response)
            if json_match:
                try:
                    data = json.loads(json_match.group())
                    if isinstance(data, dict) and "commands" in data:
                        methods = data["commands"]
                    elif isinstance(data, list):
                        methods = data
                except json.JSONDecodeError:
                    pass
            
            # 如果 JSON 解析失败，尝试从文本中提取结构化信息
            if not methods:
                methods = self._parse_text_response(response)
        
        # 如果响应是字典或列表，直接使用
        elif isinstance(response, dict):
            if "commands" in response:
                methods = response["commands"]
            else:
                methods = [response]
        elif isinstance(response, list):
            methods = response
        
        # 确保每个方法都有必需的字段
        normalized_methods = []
        for method in methods:
            if isinstance(method, dict):
                normalized_methods.append({
                    "command_name": method.get("command_name", method.get("name", "")),
                    "handling_module": method.get("handling_module", method.get("module", "")),
                    "critical_logic": method.get("critical_logic", method.get("logic", ""))
                })
        
        return normalized_methods
    
    def _parse_text_response(self, text: str) -> List[Dict[str, str]]:
        """
        从文本响应中解析方法信息（备用方案）
        
        Args:
            text: 文本响应
            
        Returns:
            方法信息列表
        """
        methods = []
        lines = text.split('\n')
        
        current_method = {}
        for line in lines:
            line = line.strip()
            if not line:
                if current_method:
                    methods.append(current_method)
                    current_method = {}
                continue
            
            # 匹配命令名称
            if re.match(r'^命令[：:]\s*(.+)', line) or re.match(r'^Command[：:]\s*(.+)', line, re.I):
                if current_method:
                    methods.append(current_method)
                current_method = {"command_name": "", "handling_module": "", "critical_logic": ""}
                match = re.search(r'[：:]\s*(.+)', line)
                if match:
                    current_method["command_name"] = match.group(1).strip()
            
            # 匹配处理模块
            elif re.match(r'^处理模块[：:]\s*(.+)', line) or re.match(r'^Module[：:]\s*(.+)', line, re.I):
                match = re.search(r'[：:]\s*(.+)', line)
                if match:
                    current_method["handling_module"] = match.group(1).strip()
            
            # 匹配关键逻辑
            elif re.match(r'^关键逻辑[：:]\s*(.+)', line) or re.match(r'^Logic[：:]\s*(.+)', line, re.I):
                match = re.search(r'[：:]\s*(.+)', line)
                if match:
                    current_method["critical_logic"] = match.group(1).strip()
            elif current_method and "critical_logic" in current_method:
                # 继续累积关键逻辑
                current_method["critical_logic"] += " " + line
        
        if current_method:
            methods.append(current_method)
        
        return methods
    
    def _extract_methods_stepwise(self, repo_name: str) -> List[Dict[str, str]]:
        """
        分步骤提取方法信息（备用方案）
        
        Args:
            repo_name: GitHub 仓库名称
            
        Returns:
            方法信息列表
        """
        methods = []
        
        # 步骤1: 获取所有命令列表
        question1 = "请列出该协议实现支持的所有命令（包括标准命令和扩展命令），只返回命令名称列表，用逗号分隔。"
        try:
            response1 = asyncio.run(self._async_ask_question(repo_name, question1))
            commands = self._extract_command_list(response1)
            
            # 步骤2: 对每个命令获取详细信息
            for cmd in commands[:20]:  # 限制前20个命令以避免超时
                question2 = f"请详细说明命令 {cmd} 的处理模块和关键逻辑。"
                try:
                    response2 = asyncio.run(self._async_ask_question(repo_name, question2))
                    method_info = self._extract_single_method_info(cmd, response2)
                    if method_info:
                        methods.append(method_info)
                except Exception as e:
                    print(f"[!] 提取命令 {cmd} 信息失败: {e}")
                    continue
        except Exception as e:
            print(f"[!] 分步骤提取失败: {e}")
        
        return methods
    
    def _extract_command_list(self, response: Any) -> List[str]:
        """从响应中提取命令列表"""
        commands = []
        if isinstance(response, str):
            # 尝试提取逗号分隔的命令
            parts = re.split(r'[,，\n]', response)
            for part in parts:
                part = part.strip()
                if part and len(part) < 50:  # 过滤掉过长的文本
                    commands.append(part)
        return commands
    
    def _extract_single_method_info(self, command_name: str, response: Any) -> Optional[Dict[str, str]]:
        """从响应中提取单个方法的信息"""
        if isinstance(response, str):
            # 尝试提取模块和逻辑信息
            module_match = re.search(r'处理模块[：:]\s*(.+?)(?:\n|$)', response)
            logic_match = re.search(r'关键逻辑[：:]\s*(.+?)(?:\n\n|\Z)', response, re.DOTALL)
            
            return {
                "command_name": command_name,
                "handling_module": module_match.group(1).strip() if module_match else "",
                "critical_logic": logic_match.group(1).strip() if logic_match else response[:500]
            }
        return None
    
    def _get_implementation_details(self, repo_name: str) -> str:
        """
        获取实现细节概述
        
        Args:
            repo_name: GitHub 仓库名称
            
        Returns:
            实现细节概述文本
        """
        question = """请提供该协议实现的整体架构和核心组件概述，
包括主要模块、数据流、状态机等关键信息。"""
        
        try:
            response = asyncio.run(self._async_ask_question(repo_name, question))
            
            if isinstance(response, str):
                return response
            elif isinstance(response, dict):
                return json.dumps(response, ensure_ascii=False, indent=2)
            else:
                return str(response)
        except Exception as e:
            print(f"[!] 获取实现细节失败: {e}")
            return ""
    
    def _extract_target_name(self, repo_name: str) -> str:
        """
        从仓库名称中提取目标实现名称
        
        Args:
            repo_name: GitHub 仓库名称，格式为 "owner/repo"
            
        Returns:
            实现名称（通常是 repo 部分）
        """
        if '/' in repo_name:
            return repo_name.split('/')[-1]
        return repo_name
    
    def save_to_json(self, result: Dict[str, Any], output_path: str):
        """
        将分析结果保存到 JSON 文件
        
        Args:
            result: 分析结果字典
            output_path: 输出文件路径
        """
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"[+] 结果已保存到: {output_path}")


def main():
    """示例用法"""
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python protocol_dkagent.py <repo_name> [output_path]")
        print("示例: python protocol_dkagent.py proftpd/proftpd")
        sys.exit(1)
    
    repo_name = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else f"{repo_name.replace('/', '_')}_analysis.json"
    
    # 创建 Agent 并分析
    agent = ProtocolDeepWikiAgent()
    result = agent.analyze_repository(repo_name)
    
    # 保存结果
    agent.save_to_json(result, output_path)
    
    # 打印摘要
    print("\n" + "="*60)
    print("分析结果摘要:")
    print("="*60)
    print(f"目标实现: {result['target']}")
    print(f"实现方法数量: {len(result['custom_commands'])}")
    print(f"\n前5个方法:")
    for i, cmd in enumerate(result['custom_commands'][:5], 1):
        print(f"  {i}. {cmd['command_name']} -> {cmd['handling_module']}")
    print("="*60)


if __name__ == "__main__":
    main()

