import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Lots } from './lots';

describe('Lots', () => {
  let component: Lots;
  let fixture: ComponentFixture<Lots>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Lots]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Lots);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
