import { Routes } from '@angular/router';
import {Login} from './features/login/login';
import {Registration} from './features/registration/registration';
import {AppRoutes} from './core/constants/app-routes';
import {guestGuard} from './core/guards/guest-guard';
import {authGuard} from './core/guards/auth-guard';
import {Lots} from './features/lots/lots';

export const routes: Routes = [
   { path: '',
     redirectTo: AppRoutes.lots,
     pathMatch: 'full' },

  { path: AppRoutes.login,
    canActivate: [guestGuard],
    component: Login },

  { path: AppRoutes.registration,
    canActivate: [authGuard],
    component: Registration},

  { path: AppRoutes.lots,
    canActivate: [guestGuard],
    component: Lots}

];
