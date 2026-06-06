"""
telemetry.py — OpenTelemetry tracing for Azure AI Foundry IQ
Sends traces to Azure Monitor (Application Insights) if connection string is set,
otherwise logs spans to stdout for local development.
"""
import logging
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

logger = logging.getLogger(__name__)

_tracer: trace.Tracer | None = None


def setup_tracing(connection_string: str = "") -> trace.Tracer:
    global _tracer
    provider = TracerProvider()

    if connection_string:
        try:
            from azure.monitor.opentelemetry.exporter import AzureMonitorTraceExporter
            exporter = AzureMonitorTraceExporter(connection_string=connection_string)
            provider.add_span_processor(BatchSpanProcessor(exporter))
            logger.info("[Telemetry] Azure Monitor tracing enabled")
        except Exception as e:
            logger.warning(f"[Telemetry] Azure Monitor setup failed, falling back to console: {e}")
            provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
    else:
        logger.info("[Telemetry] Console tracing enabled (set APPLICATIONINSIGHTS_CONNECTION_STRING for Azure Monitor)")

    trace.set_tracer_provider(provider)
    _tracer = trace.get_tracer("research-intelligence-agent")
    return _tracer


def get_tracer() -> trace.Tracer:
    if _tracer is None:
        return setup_tracing()
    return _tracer
