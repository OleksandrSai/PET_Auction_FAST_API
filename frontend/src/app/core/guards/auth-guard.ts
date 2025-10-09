import { inject } from '@angular/core';
import {
  CanActivateFn,
  Router,
  ActivatedRouteSnapshot,
  RouterStateSnapshot,
  UrlTree
} from '@angular/router';
import {AppRoutes} from '../constants/app-routes';
import {AuthService} from '../services/auth-service';


export const authGuard: CanActivateFn = (
  route: ActivatedRouteSnapshot,
  state: RouterStateSnapshot
): boolean | UrlTree => {
  const authService = inject(AuthService);
  const router = inject(Router);

  if (authService.flagNotAuth()) {
    return true;
  } else {
    return router.createUrlTree([AppRoutes.login], {
      queryParams: { accessDenied: true },
    });
  }
};
