"""
M-9: Monitoring and metrics collection

Comprehensive metrics and monitoring infrastructure for:
- API endpoint latency
- Database query performance
- External API calls
- Error rates
- Business metrics
"""

import time
import logging
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Dict, List, Any, Optional
from functools import wraps


logger = logging.getLogger(__name__)


class MetricsCollector:
    """Central metrics collection and reporting"""

    def __init__(self):
        self.metrics: Dict[str, List[float]] = defaultdict(list)
        self.counters: Dict[str, int] = defaultdict(int)
        self.errors: Dict[str, int] = defaultdict(int)
        self.start_time = datetime.utcnow()

    def record_latency(self, operation: str, duration_ms: float) -> None:
        """Record operation latency"""
        self.metrics[f"{operation}_latency_ms"].append(duration_ms)
        logger.info(f"Recorded latency: {operation}={duration_ms}ms")

    def record_error(self, error_type: str, operation: str) -> None:
        """Record error occurrence"""
        key = f"{operation}_{error_type}"
        self.errors[key] += 1
        self.counters["total_errors"] += 1
        logger.warning(f"Recorded error: {key}")

    def increment_counter(self, counter_name: str, amount: int = 1) -> None:
        """Increment counter"""
        self.counters[counter_name] += amount

    def get_average_latency(self, operation: str) -> float:
        """Get average latency for operation"""
        key = f"{operation}_latency_ms"
        values = self.metrics[key]
        if not values:
            return 0.0
        return sum(values) / len(values)

    def get_p95_latency(self, operation: str) -> float:
        """Get 95th percentile latency"""
        key = f"{operation}_latency_ms"
        values = sorted(self.metrics[key])
        if not values:
            return 0.0
        index = int(len(values) * 0.95)
        return values[min(index, len(values) - 1)]

    def get_error_rate(self, operation: str) -> float:
        """Get error rate for operation"""
        total_key = f"{operation}_total"
        total = self.counters.get(total_key, 1)
        error_count = sum(
            count for key, count in self.errors.items()
            if key.startswith(operation)
        )
        return error_count / total if total > 0 else 0.0

    def get_report(self) -> Dict[str, Any]:
        """Get comprehensive metrics report"""
        uptime = datetime.utcnow() - self.start_time
        return {
            "uptime_seconds": uptime.total_seconds(),
            "metrics": dict(self.metrics),
            "counters": dict(self.counters),
            "errors": dict(self.errors),
            "timestamp": datetime.utcnow().isoformat()
        }


# Global metrics collector instance
_metrics = MetricsCollector()


def record_operation_latency(operation_name: str):
    """Decorator to record operation latency"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            try:
                result = func(*args, **kwargs)
                return result
            finally:
                duration_ms = (time.time() - start) * 1000
                _metrics.record_latency(operation_name, duration_ms)

        return wrapper

    return decorator


def record_api_call(endpoint: str):
    """Decorator to record API call metrics"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            _metrics.increment_counter(f"{endpoint}_calls")

            try:
                result = func(*args, **kwargs)
                _metrics.increment_counter(f"{endpoint}_success")
                return result
            except Exception as e:
                _metrics.record_error(type(e).__name__, endpoint)
                _metrics.increment_counter(f"{endpoint}_failed")
                raise
            finally:
                duration_ms = (time.time() - start) * 1000
                _metrics.record_latency(f"{endpoint}_api", duration_ms)

        return wrapper

    return decorator


def record_database_query(query_type: str):
    """Decorator to record database query metrics"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            _metrics.increment_counter(f"{query_type}_queries")

            try:
                result = func(*args, **kwargs)
                _metrics.increment_counter(f"{query_type}_success")
                return result
            except Exception as e:
                _metrics.record_error("database_error", query_type)
                raise
            finally:
                duration_ms = (time.time() - start) * 1000
                _metrics.record_latency(f"{query_type}_query", duration_ms)

        return wrapper

    return decorator


class AlertThreshold:
    """Alert thresholds for monitoring"""

    # Latency thresholds (ms)
    API_LATENCY_WARNING = 500
    API_LATENCY_CRITICAL = 2000
    DB_QUERY_WARNING = 1000
    DB_QUERY_CRITICAL = 5000

    # Error rate thresholds
    ERROR_RATE_WARNING = 0.05  # 5%
    ERROR_RATE_CRITICAL = 0.10  # 10%

    # Request thresholds
    CONSECUTIVE_ERRORS_WARNING = 5
    CONSECUTIVE_ERRORS_CRITICAL = 10


class AlertManager:
    """Alert management and triggering"""

    def __init__(self):
        self.alerts: List[Dict[str, Any]] = []
        self.acknowledged: set = set()

    def check_latency_alert(self, operation: str, p95_latency: float) -> None:
        """Check and trigger latency alerts"""
        if p95_latency > AlertThreshold.API_LATENCY_CRITICAL:
            self.trigger_alert(
                "CRITICAL",
                f"API latency critical: {operation}={p95_latency}ms",
                {"operation": operation, "latency_ms": p95_latency}
            )
        elif p95_latency > AlertThreshold.API_LATENCY_WARNING:
            self.trigger_alert(
                "WARNING",
                f"API latency high: {operation}={p95_latency}ms",
                {"operation": operation, "latency_ms": p95_latency}
            )

    def check_error_rate_alert(self, operation: str, error_rate: float) -> None:
        """Check and trigger error rate alerts"""
        if error_rate > AlertThreshold.ERROR_RATE_CRITICAL:
            self.trigger_alert(
                "CRITICAL",
                f"Error rate critical: {operation}={error_rate*100:.1f}%",
                {"operation": operation, "error_rate": error_rate}
            )
        elif error_rate > AlertThreshold.ERROR_RATE_WARNING:
            self.trigger_alert(
                "WARNING",
                f"Error rate high: {operation}={error_rate*100:.1f}%",
                {"operation": operation, "error_rate": error_rate}
            )

    def trigger_alert(self, severity: str, message: str, context: Dict) -> None:
        """Trigger alert"""
        alert = {
            "timestamp": datetime.utcnow().isoformat(),
            "severity": severity,
            "message": message,
            "context": context
        }
        self.alerts.append(alert)
        logger.error(f"ALERT [{severity}]: {message}")

    def acknowledge_alert(self, alert_id: int) -> None:
        """Acknowledge alert"""
        self.acknowledged.add(alert_id)

    def get_unacknowledged_alerts(self) -> List[Dict]:
        """Get unacknowledged critical alerts"""
        return [
            alert for i, alert in enumerate(self.alerts)
            if alert["severity"] == "CRITICAL" and i not in self.acknowledged
        ]


class HealthCheck:
    """Health check status"""

    def __init__(self):
        self.status: Dict[str, bool] = {
            "database": False,
            "gemini_api": False,
            "cache": False,
            "overall": False
        }
        self.last_check = datetime.utcnow()

    def check_database_health(self) -> bool:
        """Check database health"""
        try:
            # Would perform actual health check
            self.status["database"] = True
            return True
        except Exception as e:
            logger.error(f"Database health check failed: {str(e)}")
            self.status["database"] = False
            return False

    def check_api_health(self) -> bool:
        """Check API health"""
        try:
            # Would perform actual health check
            self.status["gemini_api"] = True
            return True
        except Exception as e:
            logger.error(f"API health check failed: {str(e)}")
            self.status["gemini_api"] = False
            return False

    def get_overall_health(self) -> bool:
        """Get overall system health"""
        self.status["overall"] = all(self.status.values())
        self.last_check = datetime.utcnow()
        return self.status["overall"]

    def get_health_report(self) -> Dict[str, Any]:
        """Get health report"""
        return {
            "status": self.status,
            "overall": self.get_overall_health(),
            "last_check": self.last_check.isoformat()
        }


# Global instances
_alerts = AlertManager()
_health = HealthCheck()


def get_metrics() -> MetricsCollector:
    """Get global metrics collector"""
    return _metrics


def get_alerts() -> AlertManager:
    """Get global alert manager"""
    return _alerts


def get_health() -> HealthCheck:
    """Get global health checker"""
    return _health
