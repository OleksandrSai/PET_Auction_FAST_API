import { ComponentFixture, TestBed } from '@angular/core/testing';

import { LotStatus } from './lot-status';

describe('LotStatus', () => {
  let component: LotStatus;
  let fixture: ComponentFixture<LotStatus>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [LotStatus]
    })
    .compileComponents();

    fixture = TestBed.createComponent(LotStatus);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
