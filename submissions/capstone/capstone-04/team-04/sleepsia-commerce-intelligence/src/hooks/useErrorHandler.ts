/**
 * useErrorHandler - Custom React hook for error handling
 *
 * Provides a convenient way to handle and display errors in functional components.
 * Unlike error boundaries, this hook handles async errors, event handler errors,
 * and promise rejections.
 *
 * Features:
 * - Handles async/await errors
 * - Catches event handler errors
 * - Tracks error state
 * - Provides error recovery
 * - Integrates with error tracking service
 *
 * Usage:
 *   const { error, setError, clearError } = useErrorHandler();
 *   try {
 *     await riskyOperation();
 *   } catch (err) {
 *     setError(err as Error);
 *   }
 *
 * Example:
 *   function MyComponent() {
 *     const { error, setError, clearError, withErrorHandling } = useErrorHandler();
 *
 *     const fetchData = withErrorHandling(async () => {
 *       const response = await fetch('/api/data');
 *       return response.json();
 *     });
 *
 *     if (error) {
 *       return (
 *         <div>
 *           Error: {error.message}
 *           <button onClick={clearError}>Dismiss</button>
 *         </div>
 *       );
 *     }
 *
 *     return <button onClick={fetchData}>Load Data</button>;
 *   }
 */

import { useState, useCallback } from 'react';

interface ErrorInfo {
  message: string;
  code?: string;
  timestamp: number;
  context?: Record<string, unknown>;
}

interface UseErrorHandlerReturn {
  error: ErrorInfo | null;
  setError: (error: Error | string, context?: Record<string, unknown>) => void;
  clearError: () => void;
  withErrorHandling: <T, Args extends unknown[]>(
    fn: (...args: Args) => Promise<T>
  ) => (...args: Args) => Promise<T | null>;
}

/**
 * Hook for handling errors in functional components
 *
 * @param onError Optional callback when error occurs
 * @returns Object with error state and handlers
 */
export function useErrorHandler(
  onError?: (error: ErrorInfo) => void
): UseErrorHandlerReturn {
  const [error, setErrorState] = useState<ErrorInfo | null>(null);

  /**
   * Set error state with optional context
   */
  const setError = useCallback(
    (err: Error | string, context?: Record<string, unknown>) => {
      const errorInfo: ErrorInfo = {
        message: typeof err === 'string' ? err : err.message,
        code: err instanceof Error && (err as any).code ? (err as any).code : undefined,
        timestamp: Date.now(),
        context,
      };

      setErrorState(errorInfo);

      // Log error for debugging
      console.error('useErrorHandler:', errorInfo);

      // Call optional error handler
      onError?.(errorInfo);

      // TODO: Send to error tracking service
      // logErrorToService(errorInfo);
    },
    [onError]
  );

  /**
   * Clear error state
   */
  const clearError = useCallback(() => {
    setErrorState(null);
  }, []);

  /**
   * Wrap async functions with error handling
   * Returns null on error (after calling setError)
   */
  const withErrorHandling = useCallback(
    <T, Args extends unknown[]>(
      fn: (...args: Args) => Promise<T>
    ): ((...args: Args) => Promise<T | null>) => {
      return async (...args: Args): Promise<T | null> => {
        try {
          return await fn(...args);
        } catch (err) {
          const error = err instanceof Error ? err : new Error(String(err));
          setError(error, { args: args.length > 0 ? args : undefined });
          return null;
        }
      };
    },
    [setError]
  );

  return {
    error,
    setError,
    clearError,
    withErrorHandling,
  };
}

/**
 * Alternative: useAsyncError - for handling errors in async effects
 *
 * Usage:
 *   const throwError = useAsyncError();
 *
 *   useEffect(() => {
 *     (async () => {
 *       try {
 *         await riskyOperation();
 *       } catch (err) {
 *         throwError(err);
 *       }
 *     })();
 *   }, []);
 */
export function useAsyncError(): (error: Error) => void {
  const [, setError] = useState();

  return useCallback(
    (error: Error) => {
      setError(() => {
        throw error;
      });
    },
    [setError]
  );
}

export default useErrorHandler;
