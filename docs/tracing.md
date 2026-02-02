# PySnooper 动态追踪指南

本模块使用 PySnooper 对 Typer 框架进行动态执行追踪分析。

## 功能概述

### 1. 核心类追踪
- `Typer()` 实例化过程
- `Command()` 命令注册流程
- `Context()` 上下文传递

### 2. 选项解析追踪
- `Option()` 参数处理
- `Argument()` 位置参数解析
- 类型转换过程

### 3. 回调函数追踪
- `@app.callback` 装饰器执行
- 命令链调用顺序
- 错误处理流程

## 使用方法

```python
from analyzers.dynamic_tracer import DynamicTracer

tracer = DynamicTracer(target_path="path/to/typer")
tracer.trace_typer_init()
tracer.trace_command_execution()
tracer.export_results("data/traces/")
```

## 输出文件

| 文件 | 内容 |
|------|------|
| execution_summary.csv | 执行时间、调用次数统计 |
| variable_changes.csv | 变量变化记录 |
| trace_*.log | 详细追踪日志 |

## 生成图表

- 执行时间线图
- 性能热点散点图
- 变量变化轨迹图
- 调用链桑基图
- 执行时长小提琴图
- 内存使用面积图
- 函数调用频次图
