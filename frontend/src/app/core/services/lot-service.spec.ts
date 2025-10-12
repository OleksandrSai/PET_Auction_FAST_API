import { TestBed } from '@angular/core/testing';

import { LotService } from './lot-service';

describe('LotService', () => {
  let service: LotService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(LotService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
