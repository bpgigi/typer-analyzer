class AnalyzerError(Exception):
    """分析器基类异常"""
    pass


class GitOperationError(AnalyzerError):
    """Git操作异常"""
    pass


class DataCollectionError(AnalyzerError):
    """数据采集异常"""
    pass


class VisualizationError(AnalyzerError):
    """可视化异常"""
    pass


class ConfigurationError(AnalyzerError):
    """配置异常"""
    pass
