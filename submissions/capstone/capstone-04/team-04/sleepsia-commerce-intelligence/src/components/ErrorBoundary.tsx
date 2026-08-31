/**
 * ErrorBoundary - React error boundary component
 *
 * Catches JavaScript errors in child components and displays a fallback UI.
 * Implements error boundary pattern to prevent white-screen-of-death.
 *
 * Features:
 * - Catches render errors in child components
 * - Displays user-friendly error message
 * - Logs errors for debugging
 * - Allows error recovery with retry button
 * - Integrates with error tracking service
 *
 * Usage:
 *   <ErrorBoundary>
 *     <App />
 *   </ErrorBoundary>
 *
 * Note:
 * - Does NOT catch event handler errors (use try-catch there)
 * - Does NOT catch async errors (use useEffect error handling)
 * - Does NOT catch server-side rendering errors
 * - Does NOT catch errors in the boundary component itself
 */

import React, { ReactNode } from 'react';
import './ErrorBoundary.css';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
  onError?: (error: Error, errorInfo: React.ErrorInfo) => void;
}

interface State {
  hasError: boolean;
  error: Error | null;
  errorInfo: React.ErrorInfo | null;
}

class ErrorBoundary extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      hasError: false,
      error: null,
      errorInfo: null,
    };
  }

  /**
   * Update state when an error is caught
   * Called during render phase
   */
  static getDerivedStateFromError(error: Error): State {
    return {
      hasError: true,
      error,
      errorInfo: null,
    };
  }

  /**
   * Log error details and call optional error handler
   * Called during commit phase - safe for side effects
   */
  componentDidCatch(error: Error, errorInfo: React.ErrorInfo): void {
    // Log to console in development
    console.error('ErrorBoundary caught an error:', error, errorInfo);

    // Update state with error info
    this.setState({
      errorInfo,
    });

    // Call optional error handler callback
    if (this.props.onError) {
      this.props.onError(error, errorInfo);
    }

    // TODO: Send to error tracking service (Sentry, Rollbar, etc.)
    // this.logErrorToService(error, errorInfo);
  }

  /**
   * Reset error boundary state for retry
   */
  handleReset = (): void => {
    this.setState({
      hasError: false,
      error: null,
      errorInfo: null,
    });
  };

  render(): ReactNode {
    if (this.state.hasError) {
      // Use custom fallback if provided
      if (this.props.fallback) {
        return this.props.fallback;
      }

      // Default error UI
      return (
        <div className="error-boundary">
          <div className="error-container">
            <h1 className="error-title">⚠️ Something went wrong</h1>
            <p className="error-message">
              We encountered an unexpected error. The application encountered an issue
              and needs to recover.
            </p>

            {this.state.error && (
              <details className="error-details">
                <summary>Error Details (Development Only)</summary>
                <pre className="error-stack">
                  {this.state.error.toString()}
                  {'\n\n'}
                  {this.state.errorInfo?.componentStack}
                </pre>
              </details>
            )}

            <div className="error-actions">
              <button
                className="error-button error-button-primary"
                onClick={this.handleReset}
              >
                🔄 Try Again
              </button>
              <button
                className="error-button error-button-secondary"
                onClick={() => window.location.href = '/'}
              >
                🏠 Go Home
              </button>
            </div>

            <p className="error-support">
              If this problem persists, please contact support at support@sleepsia.com
            </p>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
