import {Injectable, signal} from '@angular/core';
import {Observable, tap} from 'rxjs';
import {HttpClient} from '@angular/common/http';
import {AuthResponse} from '../../shared/interfaces/auth-response';
import {User} from '../../shared/interfaces/user';
import {jwtDecode} from 'jwt-decode';
import {takeUntilDestroyed} from '@angular/core/rxjs-interop';
import {DecodedToken} from '../../shared/interfaces/decoded-token';

@Injectable({
  providedIn: 'root'
})

export class AuthService {

  constructor(private http: HttpClient) { }

  token: string | null = null;
  credentials: { login: string; userId: string } | null = null;

  public flagNotAuth = signal<boolean>(false);

  login(user: User): Observable<AuthResponse> {
    return this.http.post<AuthResponse>('/api/v1/auth/login/', user).pipe(
      tap(({ access_token, refresh_token, token_type }) => {
        this.setToken(access_token, refresh_token, token_type);
        this.flagNotAuth.set(false)
      }),
      takeUntilDestroyed()
    );
  }

  refreshToken(refreshToken: string): Observable<AuthResponse> {
    return this.http.post<AuthResponse>('/api/v1/auth/refresh/', {
      refresh_token: refreshToken
    }).pipe(
      takeUntilDestroyed()
    )
  }

   decodeToken(): DecodedToken | null {
    try {
      const token = this.getToken();
      if (!token) return null;
      return jwtDecode<DecodedToken>(token);
    } catch (error) {
      console.error('Ошибка декодирования токена:', error);
      return null;
    }
  }

  getUsername(): string | null {
    const decoded = this.decodeToken();
    return decoded?.login ?? null;
  }

  setToken(access_token: string, refresh_token: string | null, token_type: string): void {
    const fullAccessToken: string = `${token_type} ${access_token}`;
    const fullRefreshToken: string = `${token_type} ${refresh_token}`;
    localStorage.setItem('access_token', fullAccessToken);
    localStorage.setItem('refresh_token', fullRefreshToken);
    this.token = access_token;
  }

  getToken(): string | null {
    return this.token;
  }
  logout(): void {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    this.flagNotAuth.set(true)
  }

}

