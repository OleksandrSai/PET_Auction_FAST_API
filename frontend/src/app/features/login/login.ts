import { Component } from '@angular/core';
import {RouterLink} from '@angular/router';
import {AppRoutes} from '../../core/constants/app-routes';
import {Subscription} from 'rxjs';

@Component({
  selector: 'app-login',
  imports: [
    RouterLink
  ],
  templateUrl: './login.html',
  standalone: true,
  styleUrl: './login.scss'
})
export class Login {

  protected readonly AppRoutes = AppRoutes;

  aSub: Subscription | undefined;
  constructor() {}

  login(){

  }

  ngOnInit(){

  }
}
