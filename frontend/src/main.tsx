import { StrictMode, useEffect, useState } from 'react';
import type { FormEvent } from 'react';
import { createRoot } from 'react-dom/client';
import { api, ApiError } from './api';
import type { Receipt, User } from './api';
import './style.css';

type Session = { token: string; user: User };
type Sent = { receipt: Receipt; text: string };
const messageLimit = 255;
const initial = (name: string) => Array.from(name)[0]?.toUpperCase();

function HarpMark() {
  return <span className="mark" aria-hidden="true"><i /><i /><i /><i /></span>;
}

function Auth({ onLogin, notice }: { onLogin: (session: Session) => void; notice: string }) {
  const [signUp, setSignUp] = useState(false);
  const [login, setLogin] = useState('');
  const [error, setError] = useState('');
  const [status, setStatus] = useState(notice);
  const [busy, setBusy] = useState(false);

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const form = event.currentTarget;
    const data = new FormData(form);
    const password = String(data.get('password'));
    setError('');
    setStatus('');
    setBusy(true);
    try {
      if (signUp) {
        const user = await api.signUp({
          username: String(data.get('username')),
          email: String(data.get('email')),
          password,
        });
        setLogin(user.username);
        setStatus('Аккаунт создан. Введите пароль, чтобы войти.');
        setSignUp(false);
      } else {
        const { access_token: token } = await api.login({ login, password });
        const user = await api.me(token);
        onLogin({ token, user });
      }
    } catch (failure) {
      setError(failure instanceof ApiError && failure.body?.error?.code === 'INVALID'
        ? 'Проверьте имя пользователя, почту и пароль.'
        : (failure as Error).message);
    } finally {
      setBusy(false);
    }
  }

  return <section className="card auth">
    <div className="tabs" role="group" aria-label="Доступ к аккаунту">
      <button type="button" disabled={busy} aria-pressed={!signUp} onClick={() => { setSignUp(false); setError(''); setStatus(''); }}>Вход</button>
      <button type="button" disabled={busy} aria-pressed={signUp} onClick={() => { setSignUp(true); setError(''); setStatus(''); }}>Регистрация</button>
    </div>
    <h1>{signUp ? 'Создайте аккаунт' : 'Вход в Harp'}</h1>
    <form onSubmit={submit} key={String(signUp)}>
      {signUp ? <>
        <label>Имя пользователя<input name="username" autoComplete="username" required minLength={3} maxLength={16} /></label>
        <label>Почта<input name="email" type="email" autoComplete="email" required /></label>
      </> : <label>Имя пользователя или почта<input name="login" autoComplete="username" value={login} onChange={(event) => setLogin(event.target.value)} required /></label>}
      <label>Пароль<input name="password" type="password" autoComplete={signUp ? 'new-password' : 'current-password'} required /></label>
      {status && <p className="notice" role="status">{status}</p>}
      {error && <p className="error" role="alert">{error}</p>}
      <button className="primary" disabled={busy}>{busy ? 'Подождите…' : signUp ? 'Создать аккаунт' : 'Войти'}</button>
    </form>
  </section>;
}

function Messenger({ session, expire }: { session: Session; expire: () => void }) {
  const [username, setUsername] = useState('');
  const [recipient, setRecipient] = useState<User | null>(null);
  const [body, setBody] = useState('');
  const [sent, setSent] = useState<Sent[]>([]);
  const [searching, setSearching] = useState(false);
  const [sending, setSending] = useState(false);
  const [searchError, setSearchError] = useState('');
  const [sendError, setSendError] = useState('');
  const [sendStatus, setSendStatus] = useState('');
  const bodyLength = Array.from(body).length;

  async function search(event: FormEvent) {
    event.preventDefault();
    if (searching || sending || !username) return;
    setRecipient(null);
    setSearchError('');
    setSendError('');
    setSendStatus('');
    setSearching(true);
    try {
      const user = await api.findUser(username);
      setRecipient(user);
      if (!user) setSearchError('Пользователь с таким именем не найден.');
    } catch (failure) {
      setSearchError((failure as Error).message);
    } finally {
      setSearching(false);
    }
  }

  async function send(event: FormEvent) {
    event.preventDefault();
    if (!recipient || !body.trim() || bodyLength > messageLimit || sending) return;
    setSending(true);
    setSendError('');
    setSendStatus('');
    try {
      const receipt = await api.send(session.token, recipient.username, body);
      setSent((current) => [{ receipt, text: body }, ...current]);
      setBody('');
      setSendStatus('Сообщение сохранено сервером.');
    } catch (failure) {
      if (failure instanceof ApiError && failure.status === 401) {
        expire();
        return;
      }
      setSendError((failure as Error).message);
    } finally {
      setSending(false);
    }
  }

  return <>
    <h1 className="page-title">Новое сообщение</h1>
    <div className="workspace">
      <section className="card compose" aria-labelledby="recipient-title">
        <h2 id="recipient-title">Получатель</h2>
        <form onSubmit={search}>
          <label htmlFor="recipient">Точное имя пользователя</label>
          <div className="search">
            <input id="recipient" value={username} required disabled={searching || sending}
              onChange={(event) => {
                setUsername(event.target.value);
                setRecipient(null);
                setSearchError('');
                setSendError('');
                setSendStatus('');
              }} />
            <button className="secondary" disabled={searching || sending}>{searching ? 'Поиск…' : 'Найти'}</button>
          </div>
          {searchError && <p className="error" role="alert">{searchError}</p>}
        </form>
        {recipient && <div className="recipient" role="status">
          <span className="avatar" aria-hidden="true">{initial(recipient.username)}</span>
          <div><strong>{recipient.username}</strong><small>Получатель выбран</small></div>
        </div>}
        <form className="message-form" onSubmit={send}>
          <label>Сообщение<textarea value={body} required disabled={sending} rows={5}
            onChange={(event) => { setBody(event.target.value); setSendStatus(''); }} aria-describedby="message-format message-length" /></label>
          <div className="meta"><span id="message-format">Обычный текст · без шифрования</span>
            <span id="message-length" className={bodyLength > messageLimit ? 'error' : ''}>{bodyLength} / {messageLimit}</span></div>
          {sendError && <p className="error" role="alert">{sendError}</p>}
          {sendStatus && <p className="notice" role="status">{sendStatus}</p>}
          <button className="primary" disabled={!recipient || !body.trim() || bodyLength > messageLimit || sending}>{sending ? 'Отправка…' : 'Отправить'}</button>
        </form>
      </section>
      <section className="card activity" aria-labelledby="activity-title">
        <h2 id="activity-title">Отправленные за сеанс</h2>
        {sent.length ? <ul>{sent.map(({ receipt, text }) => <li key={receipt.message_id}>
          <strong>{receipt.receiver}</strong>
          <p>{text}</p>
          <small>ID {receipt.message_id}</small>
        </li>)}</ul> : <p className="muted">Здесь появятся сообщения, сохранение которых подтвердил сервер.</p>}
      </section>
    </div>
  </>;
}

function AdminUsers({ expire }: { expire: () => void }) {
  const [users, setUsers] = useState<User[]>([]);
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  async function loadUsers() {
    setLoading(true);
    setError('');
    try {
      setUsers(await api.users());
    } catch (failure) {
      if (failure instanceof ApiError && failure.status === 401) {
        expire();
        return;
      }
      setError((failure as Error).message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => { void loadUsers(); }, []);

  const filteredUsers = users.filter((user) =>
    `${user.username} ${user.email}`.toLocaleLowerCase().includes(query.trim().toLocaleLowerCase())
  );

  return <>
    <div className="page-heading">
      <div><h1 className="page-title">Пользователи</h1><p className="muted">Зарегистрированные аккаунты</p></div>
      <button className="secondary" onClick={() => void loadUsers()} disabled={loading}>{loading ? 'Загрузка…' : 'Обновить'}</button>
    </div>
    <section className="card users-card" aria-label="Список пользователей">
      <div className="users-toolbar">
        <label htmlFor="user-filter">Поиск по имени или почте</label>
        <input id="user-filter" type="search" value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Начните вводить…" />
        {!loading && !error && <span className="user-count">{filteredUsers.length} из {users.length}</span>}
      </div>
      {error && <div className="empty-state"><p className="error" role="alert">{error}</p><button className="secondary" onClick={() => void loadUsers()}>Попробовать снова</button></div>}
      {loading && <p className="empty-state muted" role="status">Загружаем пользователей…</p>}
      {!loading && !error && filteredUsers.length === 0 && <p className="empty-state muted">{users.length ? 'Ничего не найдено.' : 'Пока нет зарегистрированных пользователей.'}</p>}
      {!loading && !error && filteredUsers.length > 0 && <div className="table-scroll"><table>
        <thead><tr><th>Пользователь</th><th>Электронная почта</th></tr></thead>
        <tbody>{filteredUsers.map((user) => <tr key={user.username}>
          <td><span className="user-name"><span className="avatar" aria-hidden="true">{initial(user.username)}</span>{user.username}</span></td>
          <td>{user.email}</td>
        </tr>)}</tbody>
      </table></div>}
    </section>
  </>;
}

function App() {
  const [session, setSession] = useState<Session | null>(null);
  const [notice, setNotice] = useState('');
  const [page, setPage] = useState<'messages' | 'users'>('messages');
  return <div className="shell">
    <header className="top">
      <div className="brand"><HarpMark /> Harp</div>
      {session && <div className="account"><nav className="nav-tabs" aria-label="Основная навигация">
        <button aria-current={page === 'messages' ? 'page' : undefined} onClick={() => setPage('messages')}>Сообщения</button>
        <button aria-current={page === 'users' ? 'page' : undefined} onClick={() => setPage('users')}>Админка</button>
      </nav><span>{session.user.username}</span>
        <button className="secondary" onClick={() => { setSession(null); setNotice(''); setPage('messages'); }}>Выйти</button></div>}
    </header>
    <main>
      {session ? page === 'users' ? <AdminUsers expire={() => {
        setSession(null);
        setNotice('Сеанс истёк. Войдите снова.');
      }} /> : <Messenger session={session} expire={() => {
        setSession(null);
        setNotice('Сеанс истёк. Войдите снова.');
      }} /> : <Auth onLogin={setSession} notice={notice} />}
    </main>
  </div>;
}

createRoot(document.getElementById('root')!).render(<StrictMode><App /></StrictMode>);
