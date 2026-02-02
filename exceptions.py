"""
异常定义模块
定义项目中使用的自定义异常类
"""


class AnalyzerError(Exception):
    """分析器基类异常 - 所有分析相关异常的父类"""

    pass


class GitOperationError(AnalyzerError):
    """Git 操作异常 - 当 Git 命令执行失败时抛出"""

    pass


class DataCollectionError(AnalyzerError):
    """数据采集异常 - 当数据采集过程出错时抛出"""

    pass


class VisualizationError(AnalyzerError):
    """可视化异常 - 当图表生成失败时抛出"""

    pass


class ConfigurationError(AnalyzerError):
    """配置异常 - 当配置无效或缺失时抛出"""

    pass


class ParseError(AnalyzerError):
    """解析异常 - 当代码解析失败时抛出"""

    pass


class TraceError(AnalyzerError):
    """追踪异常 - 当动态追踪出错时抛出"""

    pass
