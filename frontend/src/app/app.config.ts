import {
  ApplicationConfig,
  importProvidersFrom,
  provideBrowserGlobalErrorListeners,
  provideZoneChangeDetection
} from '@angular/core';
import { provideRouter } from '@angular/router';

import { routes } from './app.routes';
import { provideClientHydration, withEventReplay } from '@angular/platform-browser';
import {provideHttpClient, withFetch} from '@angular/common/http';
import {en_US, provideNzI18n} from 'ng-zorro-antd/i18n';
import {NzIconModule, provideNzIcons} from 'ng-zorro-antd/icon';
import {PlusOutline} from '@ant-design/icons-angular/icons';

export const appConfig: ApplicationConfig = {
  providers: [
    provideHttpClient(
      withFetch()
    ),
    provideNzIcons([PlusOutline]),
    importProvidersFrom(NzIconModule),
    provideBrowserGlobalErrorListeners(),
    provideZoneChangeDetection({ eventCoalescing: true }),
    provideRouter(routes), provideClientHydration(withEventReplay()),
    provideNzI18n(en_US)
  ]
};
