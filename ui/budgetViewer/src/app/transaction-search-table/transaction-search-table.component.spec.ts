import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TransactionSearchTableComponent } from './transaction-search-table.component';

describe('TransactionSearchTableComponent', () => {
  let component: TransactionSearchTableComponent;
  let fixture: ComponentFixture<TransactionSearchTableComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ TransactionSearchTableComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(TransactionSearchTableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
