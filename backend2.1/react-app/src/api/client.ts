const API_BASE = import.meta.env.VITE_API_BASE;
if (!API_BASE) throw new Error("VITE_API_BASE is not set");

export function setAuthToken(token: string | null): void {
    if (token) {
        localStorage.setItem('jwt_token', token);
    } else {
        localStorage.removeItem('jwt_token');
    }
}

export function getAuthToken(): string | null {
    return localStorage.getItem('jwt_token');
}

export interface TokenResp {
    access_token: string;
    token_type: string;
}

export interface UserRead {
    id: number;
    username: string;
    bio: string;
}

interface FetchOptions extends RequestInit {
    body?: string;
}

async function apiFetch<T>(path: string, options: FetchOptions = {}): Promise<T> {
    const token = getAuthToken();
    const headers: Record<string, string> = {
        'Content-Type': 'application/json',
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
        ...options.headers as Record<string, string>,
    };
    const res = await fetch(`${API_BASE}${path}`, { ...options, headers });
    if (!res.ok) {
        const errorData = await res.json().catch(() => ({}));
        const message = (errorData as any).detail || res.statusText;
        throw new Error(message);
    }
    if (res.status === 204) return null as unknown as T;
    return res.json();
}

export function register(username: string, password: string): Promise<UserRead> {
    return apiFetch<UserRead>('/auth/register', {
        method: 'POST',
        body: JSON.stringify({ username, password }),
    });
}

export function login(username: string, password: string): Promise<TokenResp> {
    return apiFetch<TokenResp>('/auth/login', {
        method: 'POST',
        body: JSON.stringify({ username, password }),
    }).then(data => {
        setAuthToken(data.access_token);
        return data;
    });
}

export function deleteUser(): Promise<void> {
    return apiFetch('/auth/user', { method: 'DELETE' }).then(() => {
        setAuthToken(null);
    });
}

export function getProfile(): Promise<UserRead> {
    return apiFetch<UserRead>('/auth/user', { method: 'GET' });
}

export function updateProfile(data: { username?: string; password?: string; bio?: string }): Promise<UserRead> {
    return apiFetch<UserRead>('/auth/user', {
        method: 'PATCH',
        body: JSON.stringify(data),
    });
}

export function logout(): Promise<null> {
    setAuthToken(null);
    return apiFetch<null>('/auth/logout', { method: 'POST' });
}
