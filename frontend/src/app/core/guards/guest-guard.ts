import {CanActivateFn, Router} from '@angular/router';
import {inject} from '@angular/core';
import {AuthService} from '../services/auth-service';

export const guestGuard: CanActivateFn = () => {
  const authService = inject(AuthService);
  const flagNotAuth = authService.flagNotAuth();

  if (!flagNotAuth) {
    return true;
  }

  const router = inject(Router);
  router.navigate(['/']);
  return false;
};
