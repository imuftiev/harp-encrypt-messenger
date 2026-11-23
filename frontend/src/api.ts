export type User = { username: string; email: string };
export type Receipt = {
  message_id: string;
  sender_id: string;
  receiver: string;
  encrypt_type: 'PLAIN';
  created_at: string;
};

type ErrorBody = {
  error?: { code?: string; message?: string; request_id?: string };
  detail?: string | { loc: (string | number)[]; msg: string }[];
};

export class ApiError extends Error {
  constructor(readonly status: number, readonly body?: ErrorBody) {
    const detail = body?.detail;
    super(body?.error?.message ?? (
      typeof detail === 'string' ? detail :
      Array.isArray(detail) ? detail.map(({ loc, msg }) => `${loc.at(-1)} — ${msg}`).join(', ') :
      `Ошибка сервера (HTTP ${status}).`
    ));
  }
}

async function request<T>(path: string, options: { token?: string; body?: object } = {}): Promise<T> {
  const headers = new Headers({ Accept: 'application/json' });
  if (options.token) headers.set('Authorization', `Bearer ${options.token}`);
  if (options.body) headers.set('Content-Type', 'application/json');

  let response: Response;
  try {
    response = await fetch(`/api${path}`, {
      method: options.body ? 'POST' : 'GET',
      headers,
      body: options.body ? JSON.stringify(options.body) : undefined,
    });
  } catch {
    throw new Error('Не удалось подключиться к API. Проверьте соединение.');
  }

  const data = await response.json().catch(() => undefined);
  if (!response.ok) throw new ApiError(response.status, data);
  if (data === undefined) throw new Error('API вернул ответ в неожиданном формате.');
  return data as T;
}

export const api = {
  signUp: (body: { username: string; email: string; password: string }) =>
    request<User>('/users/signup', { body }),
  login: (body: { login: string; password: string }) =>
    request<{ access_token: string; token_type: string }>('/auth/login/', { body }),
  me: (token: string) => request<User>('/users/me', { token }),
  async findUser(username: string) {
    // The static GET routes shadow these names. A slash cannot be a path segment.
    if (['all', 'email', 'me', '.', '..'].includes(username) || username.includes('/')) {
      const users = await request<User[]>('/users/all');
      return users.find((user) => user.username === username) ?? null;
    }

    try {
      return await request<User>(`/users/${encodeURIComponent(username)}`);
    } catch (error) {
      if (error instanceof ApiError && error.body?.error?.code === 'user_not_found') return null;
      throw error;
    }
  },
  send: (token: string, receiver: string, message: string) =>
    request<Receipt>('/messages/', { token, body: { receiver, message, encrypt_type: 'PLAIN' } }),
};
