import { getAuth, signInWithPopup, GoogleAuthProvider, onAuthStateChanged, User } from 'firebase/auth';
import { initializeApp } from 'firebase/app';

// Firebase configuration - Using placeholder config for Google OAuth flow
// Note: Firebase is used here primarily for Google OAuth authentication
// For production, update these values from your Firebase project settings
const firebaseConfig = {};

// Initialize Firebase app
const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);

const provider = new GoogleAuthProvider();
provider.addScope('https://www.googleapis.com/auth/gmail.compose');
provider.addScope('https://www.googleapis.com/auth/gmail.readonly');
provider.setCustomParameters({
  prompt: 'consent',
  access_type: 'offline',
});

const TOKEN_STORAGE_KEY = 'sleepsia_google_access_token';
const TOKEN_TIMESTAMP_KEY = 'sleepsia_google_access_token_ts';
const USER_STORAGE_KEY = 'sleepsia_google_user_email';

let isSigningIn = false;
let cachedAccessToken: string | null = typeof window !== 'undefined' ? localStorage.getItem(TOKEN_STORAGE_KEY) : null;

export const isAccessTokenFresh = (): boolean => {
  if (typeof window === 'undefined') return false;
  const token = localStorage.getItem(TOKEN_STORAGE_KEY);
  const ts = localStorage.getItem(TOKEN_TIMESTAMP_KEY);
  if (!token || !ts) return false;
  const elapsedMs = Date.now() - Number(ts);
  // OAuth tokens typically expire in 3600 seconds (60 mins); consider expired after 50 minutes (3000 seconds)
  return elapsedMs < 50 * 60 * 1000;
};

export const syncTokenWithBackend = async (
  accessToken: string | null,
  email?: string | null
): Promise<boolean> => {
  if (!accessToken) return false;
  try {
    const res = await fetch('/api/auth/sync-google-token', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${accessToken}`,
      },
      body: JSON.stringify({
        accessToken,
        email: email || (typeof window !== 'undefined' ? localStorage.getItem(USER_STORAGE_KEY) : null),
      }),
    });
    const json = await res.json();
    return Boolean(json.success);
  } catch (err) {
    console.warn('[GoogleAuth] Failed to sync token with backend:', err);
    return false;
  }
};

export const initAuth = (
  onAuthSuccess?: (user: User, token: string | null) => void,
  onAuthFailure?: () => void
) => {
  return onAuthStateChanged(auth, async (user: User | null) => {
    if (user) {
      const storedToken = typeof window !== 'undefined' ? localStorage.getItem(TOKEN_STORAGE_KEY) : null;
      if (storedToken && isAccessTokenFresh()) {
        cachedAccessToken = storedToken;
        // Keep backend scheduler synchronized with current active Gmail credentials
        syncTokenWithBackend(cachedAccessToken, user.email);
      } else {
        cachedAccessToken = null;
      }
      if (onAuthSuccess) onAuthSuccess(user, cachedAccessToken);
    } else {
      cachedAccessToken = null;
      if (typeof window !== 'undefined') {
        localStorage.removeItem(TOKEN_STORAGE_KEY);
        localStorage.removeItem(TOKEN_TIMESTAMP_KEY);
        localStorage.removeItem(USER_STORAGE_KEY);
      }
      if (onAuthFailure) onAuthFailure();
    }
  });
};

export const googleSignIn = async (): Promise<{ user: User; accessToken: string } | null> => {
  if (!auth) {
    throw new Error('Firebase authentication not initialized. Please check your configuration.');
  }

  try {
    isSigningIn = true;
    console.log('[GoogleAuth] Starting sign-in process...');

    const result = await signInWithPopup(auth, provider);
    console.log('[GoogleAuth] Sign-in successful, extracting credentials...');

    const credential = GoogleAuthProvider.credentialFromResult(result);
    if (!credential?.accessToken) {
      console.error('[GoogleAuth] No access token in credential');
      throw new Error('Failed to get Google OAuth access token. Please authorize the requested Gmail permissions.');
    }

    cachedAccessToken = credential.accessToken;
    console.log('[GoogleAuth] Access token obtained, storing locally...');

    if (typeof window !== 'undefined') {
      localStorage.setItem(TOKEN_STORAGE_KEY, cachedAccessToken);
      localStorage.setItem(TOKEN_TIMESTAMP_KEY, Date.now().toString());
      if (result.user.email) {
        localStorage.setItem(USER_STORAGE_KEY, result.user.email);
      }
    }

    // Immediately synchronize token with backend scheduler
    console.log('[GoogleAuth] Syncing token with backend...');
    const syncSuccess = await syncTokenWithBackend(cachedAccessToken, result.user.email);
    console.log('[GoogleAuth] Backend sync result:', syncSuccess);

    return { user: result.user, accessToken: cachedAccessToken };
  } catch (error: any) {
    console.error('[GoogleAuth] Sign-in error:', error);

    // Handle specific error types
    if (error.code === 'auth/popup-closed-by-user') {
      throw new Error('Sign-in was cancelled. Please try again.');
    } else if (error.code === 'auth/popup-blocked') {
      throw new Error('Sign-in popup was blocked. Please enable popups and try again.');
    } else if (error.code === 'auth/network-request-failed') {
      throw new Error('Network error. Please check your internet connection and try again.');
    }

    throw error;
  } finally {
    isSigningIn = false;
  }
};

export const getAccessToken = async (): Promise<string | null> => {
  if (cachedAccessToken && isAccessTokenFresh()) return cachedAccessToken;
  if (typeof window !== 'undefined') {
    const stored = localStorage.getItem(TOKEN_STORAGE_KEY);
    if (stored && isAccessTokenFresh()) {
      cachedAccessToken = stored;
      return stored;
    }
  }
  return null;
};

export const logout = async () => {
  await auth.signOut();
  cachedAccessToken = null;
  if (typeof window !== 'undefined') {
    localStorage.removeItem(TOKEN_STORAGE_KEY);
    localStorage.removeItem(TOKEN_TIMESTAMP_KEY);
    localStorage.removeItem(USER_STORAGE_KEY);
  }
};

