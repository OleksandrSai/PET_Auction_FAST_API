import {Injectable, OnDestroy, OnInit} from '@angular/core';
import {Observable, shareReplay, Subscription} from 'rxjs';
import {LotInterface} from '../../shared/interfaces/lot';
import {HttpClient} from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class LotService implements OnDestroy {

  private lotsCache = new Map<string, Observable<LotInterface[]>>();
  private subscriptions: Subscription[] = [];

  constructor(private http: HttpClient) {}

  getAllLots(page: number, pageSize: number, forceRefresh: boolean = false): Observable<LotInterface[]> {
  const cacheKey = `${page}-${pageSize}`;

    if (this.lotsCache.has(cacheKey) && !forceRefresh) {
      return this.lotsCache.get(cacheKey)!;
    }

    const request$ = this.http.get<LotInterface[]>(`/api/v1/lot/`, {
      params: {
        page: page.toString(),
        page_size: pageSize.toString(),
      }
    }).pipe(
      shareReplay(1)
    );

    this.lotsCache.set(cacheKey, request$);

    const sub = request$.subscribe({
      error: () => this.lotsCache.delete(cacheKey)
    });

    this.subscriptions.push(sub);

    return request$;
  }

  ngOnDestroy(): void {
    this.subscriptions.forEach(sub => sub.unsubscribe());
  }

}
